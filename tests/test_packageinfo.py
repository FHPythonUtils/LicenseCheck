from __future__ import annotations

from email.message import Message
from pathlib import Path
from subprocess import CompletedProcess

import pytest
from packaging.requirements import Requirement

from licensecheck.models.constants import UNKNOWN
from licensecheck.models.packageinfo import PackageInfo
from licensecheck.packageinforesolver import (
	IndexPackageInfo,
	LocalPackageInfo,
	PackageInfoManager,
	RemotePackageInfo,
	_license_from_metadata,
	from_classifiers,
	normalize_license,
)

THISDIR = str(Path(__file__).resolve().parent)


@pytest.fixture
def package_info_manager() -> PackageInfoManager:
	"""Fixture to provide a PackageInfoManager instance."""
	return PackageInfoManager("https://pypi.org/")


@pytest.fixture
def local_package_info() -> LocalPackageInfo:
	return LocalPackageInfo(requests_package)


@pytest.fixture
def remote_package_info() -> RemotePackageInfo:
	return RemotePackageInfo("https://pypi.org/", requests_package)


def aux_packageinfo(package_name: str) -> PackageInfo:
	return PackageInfo(name=package_name)


def write_pyproject(directory: Path, contents: str) -> Path:
	directory.mkdir(parents=True, exist_ok=True)
	pyproject_path = directory / "pyproject.toml"
	pyproject_path.write_text(contents.strip(), encoding="utf-8")
	return pyproject_path


requests_package = aux_packageinfo("requests")


def test_getPackageInfoLocal(local_package_info: LocalPackageInfo) -> None:
	try:
		name = local_package_info.get_name()
		assert name == "requests"
	except ModuleNotFoundError:
		assert True


def test_getPackageInfoPypi(remote_package_info: RemotePackageInfo) -> None:
	pkg = remote_package_info

	assert pkg.get_name() == "requests"
	assert pkg.get_author() == "Kenneth Reitz"
	assert pkg.get_license() == "Apache-2.0"


def test_remote_package_info_uses_versioned_pypi_endpoint(
	monkeypatch: pytest.MonkeyPatch,
) -> None:
	pkg = RemotePackageInfo(
		"https://packages.example",
		PackageInfo(name="sample", version="1.2.3"),
	)
	requested_urls: list[str] = []

	def fake_make_req(
		url: str, headers: dict[str, str] | None = None
	) -> tuple[int, dict[str, object]]:
		del headers
		requested_urls.append(url)
		return 200, {
			"info": {
				"name": "sample",
				"version": "1.2.3",
				"license_expression": "MIT",
			}
		}

	monkeypatch.setattr(pkg, "make_req", fake_make_req)

	assert pkg.get_license() == "MIT"
	assert requested_urls == ["https://packages.example/pypi/sample/1.2.3/json"]


def test_index_package_info_uses_uv_configured_indexes(
	monkeypatch: pytest.MonkeyPatch,
) -> None:
	pkg = IndexPackageInfo(PackageInfo(name="private-package", version="1.2.3"))
	commands: list[list[str]] = []

	def fake_run(command: list[str], **_kwargs: object) -> CompletedProcess[str]:
		commands.append(command)
		target = Path(command[command.index("--target") + 1])
		metadata_path = target / "private_package-1.2.3.dist-info" / "METADATA"
		metadata_path.parent.mkdir()
		metadata_path.write_text(
			"""
Metadata-Version: 2.4
Name: private-package
Version: 1.2.3
License-Expression: LicenseRef-Example-Proprietary
""".strip(),
			encoding="utf-8",
		)
		return CompletedProcess(args=command, returncode=0, stdout="", stderr="")

	monkeypatch.setattr("licensecheck.packageinforesolver.subprocess.run", fake_run)

	assert pkg.get_name() == "private-package"
	assert pkg.get_version() == "1.2.3"
	assert pkg.get_license() == "LicenseRef-Example-Proprietary"
	assert commands == [
		[
			"uv",
			"pip",
			"install",
			"--color",
			"never",
			"--no-progress",
			"--no-deps",
			"--only-binary",
			":all:",
			"--target",
			commands[0][commands[0].index("--target") + 1],
			"private-package==1.2.3",
		]
	]


def test_resolve_requirements_uses_project_directory_and_default_index(
	tmp_path: Path,
	monkeypatch: pytest.MonkeyPatch,
) -> None:
	pyproject_path = write_pyproject(
		tmp_path / "project",
		"""
[project]
name = "project"
version = "1.0.0"
dependencies = ["private-package"]
""",
	)
	calls: list[tuple[list[str], dict[str, object]]] = []

	def fake_run(command: list[str], **kwargs: object) -> CompletedProcess[str]:
		calls.append((command, kwargs))
		return CompletedProcess(command, 0, "private-package==1.2.3\n", "")

	monkeypatch.setattr("licensecheck.packageinforesolver.subprocess.run", fake_run)
	manager = PackageInfoManager("https://packages.example/simple")
	manager.resolve_requirements({str(pyproject_path)}, set(), set(), set())

	command, kwargs = calls[0]
	assert command[command.index("--default-index") + 1] == "https://packages.example/simple"
	assert "--index" not in command
	assert kwargs["cwd"] == pyproject_path.parent


def test_package_manager_reads_metadata_from_resolved_private_source(
	package_info_manager: PackageInfoManager,
	tmp_path: Path,
	monkeypatch: pytest.MonkeyPatch,
) -> None:
	pyproject_path = write_pyproject(
		tmp_path / "project",
		"""
[project]
name = "project"
version = "1.0.0"
dependencies = ["private-package==1.2.3"]

[[tool.uv.index]]
name = "private"
url = "https://packages.example/simple"
explicit = true

[tool.uv.sources]
private-package = { index = "private" }
""",
	)
	commands: list[tuple[list[str], object]] = []

	def fake_run(command: list[str], **kwargs: object) -> CompletedProcess[str]:
		commands.append((command, kwargs.get("cwd")))
		if command[:3] == ["uv", "pip", "compile"]:
			return CompletedProcess(
				command,
				0,
				"""private-package==1.2.3
    # via project
    # from https://packages.example/simple
""",
				"",
			)

		target = Path(command[command.index("--target") + 1])
		metadata_path = target / "private_package-1.2.3.dist-info" / "METADATA"
		metadata_path.parent.mkdir()
		metadata_path.write_text(
			"""
Metadata-Version: 2.4
Name: private-package
Version: 1.2.3
License-Expression: LicenseRef-Private-Proprietary
""".strip(),
			encoding="utf-8",
		)
		return CompletedProcess(command, 0, "", "")

	def fail_public_lookup(*_args: object, **_kwargs: object) -> tuple[int, dict[str, object]]:
		pytest.fail("public metadata must not replace the resolved private artifact")

	monkeypatch.setattr("licensecheck.packageinforesolver.subprocess.run", fake_run)
	monkeypatch.setattr(RemotePackageInfo, "make_req", fail_public_lookup)

	package_info_manager.resolve_requirements({str(pyproject_path)}, set(), set(), set())
	package = package_info_manager.getPackages().pop()

	assert package.license == "LicenseRef-Private-Proprietary"
	install_command, install_cwd = commands[1]
	assert install_command[install_command.index("--index") + 1] == (
		"private=https://packages.example/simple"
	)
	assert install_cwd == pyproject_path.parent


def test_private_index_credentials_are_not_exposed_in_command(
	package_info_manager: PackageInfoManager,
	tmp_path: Path,
	monkeypatch: pytest.MonkeyPatch,
) -> None:
	private_index = "https://user:secret@packages.example/simple"
	pyproject_path = write_pyproject(
		tmp_path,
		f"""
[project]
name = "project"
version = "1.0.0"
dependencies = ["private-package==1.2.3"]

[tool.uv]
index-url = "{private_index}"
""",
	)
	install_call: tuple[list[str], dict[str, object]] | None = None

	def fake_run(command: list[str], **kwargs: object) -> CompletedProcess[str]:
		nonlocal install_call
		if command[:3] == ["uv", "pip", "compile"]:
			return CompletedProcess(
				command,
				0,
				"private-package==1.2.3\n    # from https://packages.example/simple\n",
				"",
			)

		install_call = command, kwargs
		target = Path(command[command.index("--target") + 1])
		metadata_path = target / "private_package-1.2.3.dist-info" / "METADATA"
		metadata_path.parent.mkdir()
		metadata_path.write_text(
			"""
Metadata-Version: 2.4
Name: private-package
Version: 1.2.3
License-Expression: LicenseRef-Private-Proprietary
""".strip(),
			encoding="utf-8",
		)
		return CompletedProcess(command, 0, "", "")

	monkeypatch.setattr("licensecheck.packageinforesolver.subprocess.run", fake_run)
	monkeypatch.setattr(
		RemotePackageInfo,
		"make_req",
		lambda *_args, **_kwargs: pytest.fail("the resolved private artifact must be used"),
	)

	package_info_manager.resolve_requirements({str(pyproject_path)}, set(), set(), set())
	package = package_info_manager.getPackages().pop()

	assert package.license == "LicenseRef-Private-Proprietary"
	assert install_call is not None
	install_command, install_kwargs = install_call
	assert "secret" not in " ".join(install_command)
	install_environment = install_kwargs["env"]
	assert isinstance(install_environment, dict)
	assert install_environment["UV_INDEX"] == private_index


def test_resolved_public_source_ignores_installed_private_homonym(
	package_info_manager: PackageInfoManager,
	tmp_path: Path,
	monkeypatch: pytest.MonkeyPatch,
) -> None:
	pyproject_path = write_pyproject(
		tmp_path,
		"""
[project]
name = "project"
version = "1.0.0"
dependencies = ["homonym==1.2.3"]
""",
	)
	installed_metadata = Message()
	installed_metadata["Name"] = "homonym"
	installed_metadata["Version"] = "1.2.3"
	installed_metadata["License-Expression"] = "LicenseRef-Private-Proprietary"

	def fake_run(command: list[str], **_kwargs: object) -> CompletedProcess[str]:
		if command[:3] != ["uv", "pip", "compile"]:
			pytest.fail("public metadata already declares a usable license")
		return CompletedProcess(
			command,
			0,
			"homonym==1.2.3\n    # from https://pypi.org/simple\n",
			"",
		)

	def fake_make_req(
		_self: RemotePackageInfo,
		url: str,
		headers: dict[str, str] | None = None,
	) -> tuple[int, dict[str, object]]:
		del url, headers
		return 200, {
			"info": {
				"name": "homonym",
				"version": "1.2.3",
				"license_expression": "MIT",
			}
		}

	monkeypatch.setattr("licensecheck.packageinforesolver.subprocess.run", fake_run)
	monkeypatch.setattr(
		"licensecheck.packageinforesolver.metadata.metadata",
		lambda _name: installed_metadata,
	)
	monkeypatch.setattr(RemotePackageInfo, "make_req", fake_make_req)

	package_info_manager.resolve_requirements({str(pyproject_path)}, set(), set(), set())
	package = package_info_manager.getPackages().pop()

	assert package.version == "1.2.3"
	assert package.license == "MIT"


def test_package_manager_uses_private_index_when_pypi_is_missing(
	package_info_manager: PackageInfoManager,
	monkeypatch: pytest.MonkeyPatch,
) -> None:
	def fake_make_req(
		_self: RemotePackageInfo,
		url: str,
		headers: dict[str, str] | None = None,
	) -> tuple[int, dict[str, object]]:
		del url, headers
		return 404, {}

	def fake_run(command: list[str], **_kwargs: object) -> CompletedProcess[str]:
		target = Path(command[command.index("--target") + 1])
		metadata_path = target / "private_package-1.2.3.dist-info" / "METADATA"
		metadata_path.parent.mkdir()
		metadata_path.write_text(
			"""
Metadata-Version: 2.4
Name: private-package
Version: 1.2.3
License-Expression: MIT
""".strip(),
			encoding="utf-8",
		)
		return CompletedProcess(args=command, returncode=0, stdout="", stderr="")

	monkeypatch.setattr(RemotePackageInfo, "make_req", fake_make_req)
	monkeypatch.setattr("licensecheck.packageinforesolver.subprocess.run", fake_run)
	package_info_manager.reqs = {Requirement("private-package==1.2.3")}

	package = package_info_manager.getPackages().pop()

	assert package.name == "private-package"
	assert package.version == "1.2.3"
	assert package.license == "MIT"
	assert package.errorCode == 0


def test_package_manager_uses_exact_artifact_when_pypi_license_is_missing(
	package_info_manager: PackageInfoManager,
	monkeypatch: pytest.MonkeyPatch,
) -> None:
	commands: list[list[str]] = []

	def fake_make_req(
		_self: RemotePackageInfo,
		url: str,
		headers: dict[str, str] | None = None,
	) -> tuple[int, dict[str, object]]:
		del url, headers
		return 200, {
			"info": {
				"name": "artifact-package",
				"version": "1.2.3",
			}
		}

	def fake_run(command: list[str], **_kwargs: object) -> CompletedProcess[str]:
		commands.append(command)
		target = Path(command[command.index("--target") + 1])
		metadata_path = target / "artifact_package-1.2.3.dist-info" / "METADATA"
		metadata_path.parent.mkdir()
		metadata_path.write_text(
			"""
Metadata-Version: 2.4
Name: artifact-package
Version: 1.2.3
License-Expression: MIT
""".strip(),
			encoding="utf-8",
		)
		return CompletedProcess(args=command, returncode=0, stdout="", stderr="")

	monkeypatch.setattr(RemotePackageInfo, "make_req", fake_make_req)
	monkeypatch.setattr("licensecheck.packageinforesolver.subprocess.run", fake_run)
	package_info_manager.reqs = {Requirement("artifact-package==1.2.3")}

	package = package_info_manager.getPackages().pop()

	assert package.name == "artifact-package"
	assert package.version == "1.2.3"
	assert package.license == "MIT"
	assert commands[0][-1] == "artifact-package==1.2.3"


def test_package_manager_ignores_installed_metadata_from_another_version(
	package_info_manager: PackageInfoManager,
	monkeypatch: pytest.MonkeyPatch,
) -> None:
	installed_metadata = Message()
	installed_metadata["Name"] = "artifact-package"
	installed_metadata["Version"] = "9.9.9"
	installed_metadata["License-Expression"] = "GPL-3.0-only"

	def fake_make_req(
		_self: RemotePackageInfo,
		url: str,
		headers: dict[str, str] | None = None,
	) -> tuple[int, dict[str, object]]:
		del url, headers
		return 200, {
			"info": {
				"name": "artifact-package",
				"version": "1.2.3",
			}
		}

	def fake_run(command: list[str], **_kwargs: object) -> CompletedProcess[str]:
		target = Path(command[command.index("--target") + 1])
		metadata_path = target / "artifact_package-1.2.3.dist-info" / "METADATA"
		metadata_path.parent.mkdir()
		metadata_path.write_text(
			"""
Metadata-Version: 2.4
Name: artifact-package
Version: 1.2.3
License-Expression: MIT
""".strip(),
			encoding="utf-8",
		)
		return CompletedProcess(args=command, returncode=0, stdout="", stderr="")

	monkeypatch.setattr(
		"licensecheck.packageinforesolver.metadata.metadata", lambda _name: installed_metadata
	)
	monkeypatch.setattr(RemotePackageInfo, "make_req", fake_make_req)
	monkeypatch.setattr("licensecheck.packageinforesolver.subprocess.run", fake_run)
	package_info_manager.reqs = {Requirement("artifact-package==1.2.3")}

	package = package_info_manager.getPackages().pop()

	assert package.version == "1.2.3"
	assert package.license == "MIT"


def test_getPackageInfoLocalNotFound() -> None:
	pkg = LocalPackageInfo(aux_packageinfo("this_package_does_not_exist"))
	assert pkg.get_size() is None


def test_getPackagePypiLocalNotFound() -> None:
	pkg = RemotePackageInfo("https://pypi.org/", aux_packageinfo("this_package_does_not_exist"))
	assert pkg.get_size() is None


def test_getPackages(package_info_manager: PackageInfoManager) -> None:
	package_info_manager.reqs = {Requirement("requests")}
	packages = package_info_manager.getPackages()
	package = packages.pop()
	assert package.name == "requests"
	assert package.author == "Kenneth Reitz"
	assert package.license == "Apache-2.0"


def test_getPackagesNotFound(package_info_manager: PackageInfoManager) -> None:
	package_info_manager.reqs = {Requirement("this_package_does_not_exist")}

	packages = package_info_manager.getPackages()
	package = packages.pop()

	assert package.name == "this-package-does-not-exist"
	assert package.errorCode == 404


def test_from_classifiers() -> None:
	lines = Path(f"{THISDIR}/data/pypiClassifiers.txt").read_text("utf-8").splitlines()
	licenses = [from_classifiers([rawLicense]) or UNKNOWN for rawLicense in lines]
	# Path(f"{THISDIR}/data/licenses.txt").write_text("\n".join(licenses), "utf-8")
	assert "\n".join(licenses) == Path(f"{THISDIR}/data/licenses.txt").read_text("utf-8")


def test_licenseFromEmptyClassifierlist() -> None:
	licenses = []
	licenses.append(from_classifiers([]))
	assert licenses == [None]


@pytest.mark.parametrize(
	("license_expression", "classifier", "legacy_license", "expected"),
	[
		(
			"MIT",
			"License :: Other/Proprietary License",
			"LicenseRef-Example-Proprietary",
			"MIT",
		),
		(
			None,
			"License :: Other/Proprietary License",
			"LicenseRef-Example-Proprietary",
			"LicenseRef-Example-Proprietary",
		),
		(
			None,
			"License :: Other/Proprietary License",
			"Apache 2.0",
			"Apache-2.0",
		),
		(
			None,
			"License :: OSI Approved :: MIT License",
			"unrecognized license text",
			"MIT License",
		),
	],
)
def test_explicit_license_metadata_precedes_classifiers_when_recognizable(
	license_expression: str | None,
	classifier: str,
	legacy_license: str,
	expected: str,
) -> None:
	assert _license_from_metadata(license_expression, [classifier], legacy_license) == expected


def test_getModuleSize() -> None:
	local_package_info = LocalPackageInfo(aux_packageinfo("this_package_does_not_exist"))
	local_package_info.get_size()


@pytest.mark.parametrize(
	("lice", "normalized"),
	[
		("mit", "mit"),
		("BSD-2-Clause", "BSD-2-Clause"),
		("BSD-2-Clause AND Apache-2.0", "Apache-2.0;; BSD-2-Clause"),
		(
			"BSD-2-Clause AND Apache-2.0 WITH LLVM-exception",
			"Apache-2.0 WITH LLVM-exception;; BSD-2-Clause",
		),
	],
)
def test_normalize_license(lice: str, normalized: str) -> None:
	assert normalize_license(lice) == normalized


@pytest.mark.parametrize(
	("contents", "name", "author", "homepage"),
	[
		(
			"""
[tool.poetry]
name = "poetry-local"
version = "1.2.3"
license = "MIT"
authors = ["Poetry Author <author@example.com>"]
homepage = "https://poetry.example"
""",
			"poetry-local",
			"Poetry Author <author@example.com>",
			"https://poetry.example",
		),
		(
			"""
[tool.flit.metadata]
module = "flit_local"
dist-name = "flit-local"
version = "1.2.3"
license = "MIT"
author = "Flit Author"
home-page = "https://flit.example"
""",
			"flit-local",
			"Flit Author",
			"https://flit.example",
		),
	],
)
def test_read_project_package_supports_legacy_metadata(
	tmp_path: Path,
	contents: str,
	name: str,
	author: str,
	homepage: str,
) -> None:
	pyproject_path = write_pyproject(tmp_path, contents)

	package = PackageInfoManager._read_project_package(pyproject_path)

	assert package is not None
	assert package.name == name
	assert package.version == "1.2.3"
	assert package.license == "MIT"
	assert package.author == author
	assert package.homePage == homepage


@pytest.mark.parametrize(
	("license_metadata", "expected"),
	[
		('license = "MIT OR GPL-3.0-only"', "GPL-3.0-only;; MIT"),
		(
			'classifiers = ["License :: OSI Approved :: MIT License"]',
			"MIT License",
		),
	],
)
def test_read_project_package_normalizes_license_metadata(
	tmp_path: Path,
	license_metadata: str,
	expected: str,
) -> None:
	pyproject_path = write_pyproject(
		tmp_path,
		f"""
[project]
name = "local-package"
version = "1.2.3"
{license_metadata}
""",
	)

	package = PackageInfoManager._read_project_package(pyproject_path)

	assert package is not None
	assert package.license == expected


def test_unpinned_requirement_does_not_crash(package_info_manager: PackageInfoManager) -> None:
	package_info_manager.reqs = {Requirement("sample")}

	packages = package_info_manager.getPackages()
	package: PackageInfo = packages.pop()

	assert package.name == "sample"
	assert package.errorCode == 0


def test_resolve_requirements_audits_editable_project(
	package_info_manager: PackageInfoManager,
	tmp_path: Path,
	monkeypatch: pytest.MonkeyPatch,
) -> None:
	write_pyproject(
		tmp_path / "local_dependency",
		"""
[project]
name = "local-dependency"
version = "1.2.3"
license = "LicenseRef-Example-Proprietary"
""",
	)
	pyproject_path = write_pyproject(
		tmp_path / "project",
		"""
[project]
name = "project"
version = "1.0.0"
dependencies = ["local-dependency"]

[tool.uv.sources]
local-dependency = { path = "../local_dependency", editable = true }
""",
	)

	def fake_run(command: list[str], **_kwargs: object) -> CompletedProcess[str]:
		return CompletedProcess(
			args=command,
			returncode=0,
			stdout="-e ../local_dependency\n",
			stderr="",
		)

	monkeypatch.setattr("licensecheck.packageinforesolver.subprocess.run", fake_run)

	package_info_manager.resolve_requirements(
		requirements_paths={str(pyproject_path)},
		groups=set(),
		extras=set(),
		skip_dependencies=set(),
	)
	package = package_info_manager.getPackages().pop()

	assert {str(requirement) for requirement in package_info_manager.reqs} == {
		"local-dependency==1.2.3"
	}
	assert package.name == "local-dependency"
	assert package.version == "1.2.3"
	assert package.license == "LicenseRef-Example-Proprietary"
	assert package.errorCode == 0


def test_resolved_requirement_version_is_preserved(
	package_info_manager: PackageInfoManager,
	monkeypatch: pytest.MonkeyPatch,
) -> None:
	def fake_make_req(
		_self: RemotePackageInfo,
		url: str,
		headers: dict[str, str] | None = None,
	) -> tuple[int, dict[str, object]]:
		del url, headers
		return 200, {
			"info": {
				"name": "sample",
				"version": "1.0.0",
				"license_expression": "MIT",
			}
		}

	def fail_artifact_fetch(*_args: object, **_kwargs: object) -> CompletedProcess[str]:
		pytest.fail("artifact metadata should not be fetched when PyPI declares a license")

	monkeypatch.setattr(RemotePackageInfo, "make_req", fake_make_req)
	monkeypatch.setattr("licensecheck.packageinforesolver.subprocess.run", fail_artifact_fetch)
	package_info_manager.reqs = {Requirement("sample==1.0.0.0")}

	package = package_info_manager.getPackages().pop()

	assert package.version == "1.0.0.0"


def test_resolve_requirements_handles_nested_editable_uv_sources(
	package_info_manager: PackageInfoManager, tmp_path: Path
) -> None:
	transitive_path = tmp_path / "transitive_dependency"
	transitive_path.mkdir()
	(transitive_path / "pyproject.toml").write_text(
		"""
[project]
name = "transitive-dependency"
version = "1.0.0"
""".strip(),
		encoding="utf-8",
	)

	nested_path = tmp_path / "nested_workspace_member"
	nested_path.mkdir()
	(nested_path / "pyproject.toml").write_text(
		"""
[project]
name = "nested-dependency"
version = "1.0.0"
""".strip(),
		encoding="utf-8",
	)

	dependency_path = tmp_path / "workspace_member"
	dependency_path.mkdir()
	(dependency_path / "pyproject.toml").write_text(
		f"""
[project]
name = "local-dependency"
version = "1.0.0"
dependencies = [
    "nested-dependency",
    "transitive-dependency @ {transitive_path.as_uri()}",
]

[tool.uv.sources]
nested-dependency = {{ path = "../nested_workspace_member", editable = true }}
""".strip(),
		encoding="utf-8",
	)

	project_path = tmp_path / "project"
	project_path.mkdir()
	pyproject_path = project_path / "pyproject.toml"
	pyproject_path.write_text(
		"""
[project]
name = "project"
version = "1.0.0"
dependencies = ["local-dependency"]

[tool.uv.sources]
local-dependency = { path = "../workspace_member", editable = true }
""".strip(),
		encoding="utf-8",
	)

	package_info_manager.resolve_requirements(
		requirements_paths={str(pyproject_path)},
		groups=set(),
		extras=set(),
		skip_dependencies=set(),
	)

	assert {requirement.name for requirement in package_info_manager.reqs} == {
		"local-dependency",
		"nested-dependency",
		"transitive-dependency",
	}


def test_resolve_requirements_handles_editable_uv_sources_in_monorepo(
	package_info_manager: PackageInfoManager, tmp_path: Path
) -> None:
	repository_path = tmp_path / "repository"
	libraries_path = repository_path / "libs"

	published_path = repository_path / "published_dependency"
	published_path.mkdir(parents=True)
	(published_path / "pyproject.toml").write_text(
		"""
[project]
name = "published-dependency"
version = "1.0.0"
""".strip(),
		encoding="utf-8",
	)

	sdk_path = libraries_path / "sdk_extensions"
	sdk_path.mkdir(parents=True)
	(sdk_path / "pyproject.toml").write_text(
		f"""
[project]
name = "sdk-extensions"
version = "1.0.0"
dependencies = ["published-dependency @ {published_path.as_uri()}"]
""".strip(),
		encoding="utf-8",
	)

	anomaly_path = libraries_path / "anomaly_detection"
	anomaly_path.mkdir()
	(anomaly_path / "pyproject.toml").write_text(
		"""
[project]
name = "anomaly-detection"
version = "1.0.0"
""".strip(),
		encoding="utf-8",
	)

	common_path = libraries_path / "service_common"
	common_path.mkdir()
	(common_path / "pyproject.toml").write_text(
		"""
[project]
name = "service-common"
version = "1.0.0"
dependencies = ["sdk-extensions", "anomaly-detection"]

[tool.uv.sources]
sdk-extensions = { path = "../sdk_extensions", editable = true }
anomaly-detection = { path = "../anomaly_detection", editable = true }
""".strip(),
		encoding="utf-8",
	)

	function_path = repository_path / "functions" / "reconciliation"
	function_path.mkdir(parents=True)
	pyproject_path = function_path / "pyproject.toml"
	pyproject_path.write_text(
		"""
[project]
name = "reconciliation"
version = "1.0.0"
dependencies = ["sdk-extensions", "service-common", "anomaly-detection"]

[tool.uv.sources]
sdk-extensions = { path = "../../libs/sdk_extensions", editable = true }
service-common = { path = "../../libs/service_common", editable = true }
anomaly-detection = { path = "../../libs/anomaly_detection", editable = true }

[tool.uv]
package = false
""".strip(),
		encoding="utf-8",
	)

	package_info_manager.resolve_requirements(
		requirements_paths={str(pyproject_path)},
		groups=set(),
		extras=set(),
		skip_dependencies=set(),
	)

	assert {requirement.name for requirement in package_info_manager.reqs} == {
		"anomaly-detection",
		"published-dependency",
		"sdk-extensions",
		"service-common",
	}


def test_resolve_requirements_does_not_skip_inactive_editable_source(
	package_info_manager: PackageInfoManager,
	tmp_path: Path,
	monkeypatch: pytest.MonkeyPatch,
) -> None:
	write_pyproject(
		tmp_path / "local-idna",
		"""
[project]
name = "idna"
version = "999"
license = "LicenseRef-Local-Proprietary"
""",
	)
	pyproject_path = write_pyproject(
		tmp_path / "project",
		"""
[project]
name = "project"
version = "1.0.0"
dependencies = ["idna==3.10"]

[tool.uv.sources]
idna = {
    path = "../local-idna",
    editable = true,
    marker = "python_version < '0'",
}
""",
	)

	def fake_run(*_args: object, **_kwargs: object) -> CompletedProcess[str]:
		return CompletedProcess(
			args=["uv", "pip", "compile"],
			returncode=0,
			stdout="idna==3.10\n",
			stderr="",
		)

	monkeypatch.setattr("licensecheck.packageinforesolver.subprocess.run", fake_run)

	def fake_make_req(
		_self: RemotePackageInfo,
		url: str,
		headers: dict[str, str] | None = None,
	) -> tuple[int, dict[str, object]]:
		del url, headers
		return 200, {
			"info": {
				"name": "idna",
				"version": "3.10",
				"license_expression": "BSD-3-Clause",
			}
		}

	monkeypatch.setattr(RemotePackageInfo, "make_req", fake_make_req)

	package_info_manager.resolve_requirements(
		requirements_paths={str(pyproject_path)},
		groups=set(),
		extras=set(),
		skip_dependencies=set(),
	)

	assert {str(requirement) for requirement in package_info_manager.reqs} == {"idna==3.10"}
	package = package_info_manager.getPackages().pop()
	assert package.version == "3.10"
	assert package.license == "BSD-3-Clause"
	assert "idna" not in package_info_manager.local_projects


def test_resolve_requirements_uses_uv_prerelease_setting(
	package_info_manager: PackageInfoManager,
	tmp_path: Path,
	monkeypatch: pytest.MonkeyPatch,
) -> None:
	pyproject_path = write_pyproject(
		tmp_path,
		"""
[project]
name = "project"
version = "1.0.0"
dependencies = ["prerelease-package"]

[tool.uv]
prerelease = "allow"
""",
	)
	commands: list[list[str]] = []

	def fake_run(command: list[str], **_kwargs: object) -> CompletedProcess[str]:
		commands.append(command)
		return CompletedProcess(
			args=command,
			returncode=0,
			stdout="prerelease-package==1.0.0.dev1\n",
			stderr="",
		)

	monkeypatch.setattr("licensecheck.packageinforesolver.subprocess.run", fake_run)

	package_info_manager.resolve_requirements(
		requirements_paths={str(pyproject_path)},
		groups=set(),
		extras=set(),
		skip_dependencies=set(),
	)

	assert commands[0][-2:] == ["--prerelease", "allow"]


def test_resolve_requirements_prefers_adjacent_uv_lock(
	package_info_manager: PackageInfoManager,
	tmp_path: Path,
	monkeypatch: pytest.MonkeyPatch,
) -> None:
	pyproject_path = write_pyproject(
		tmp_path,
		"""
[project]
name = "project"
version = "1.0.0"
dependencies = ["dependency>=1"]
""",
	)
	(tmp_path / "uv.lock").write_text("version = 1", encoding="utf-8")
	commands: list[list[str]] = []

	def fake_run(command: list[str], **_kwargs: object) -> CompletedProcess[str]:
		commands.append(command)
		return CompletedProcess(
			args=command,
			returncode=0,
			stdout="dependency==1.2.3\n",
			stderr="",
		)

	monkeypatch.setattr("licensecheck.packageinforesolver.subprocess.run", fake_run)

	package_info_manager.resolve_requirements(
		requirements_paths={str(pyproject_path)},
		groups=set(),
		extras=set(),
		skip_dependencies=set(),
	)

	assert commands[0][:4] == ["uv", "export", "--project", tmp_path.as_posix()]
	assert "--locked" in commands[0]
	assert {str(requirement) for requirement in package_info_manager.reqs} == {"dependency==1.2.3"}


def test_resolve_requirements_keeps_package_sharing_editable_directory_name(
	package_info_manager: PackageInfoManager, tmp_path: Path
) -> None:
	published_path = tmp_path / "published_idna"
	write_pyproject(
		published_path,
		"""
[project]
name = "idna"
version = "3.10"
""",
	)

	editable_path = tmp_path / "idna"
	write_pyproject(
		editable_path,
		"""
[project]
name = "internal-helper"
version = "1.0.0"
""",
	)

	pyproject_path = write_pyproject(
		tmp_path / "project",
		f"""
[project]
name = "project"
version = "1.0.0"
dependencies = [
    "internal-helper",
    "idna @ {published_path.as_uri()}",
]

[tool.uv.sources]
internal-helper = {{ path = "../idna", editable = true }}
""",
	)

	package_info_manager.resolve_requirements(
		requirements_paths={str(pyproject_path)},
		groups=set(),
		extras=set(),
		skip_dependencies=set(),
	)

	assert {requirement.name for requirement in package_info_manager.reqs} == {
		"idna",
		"internal-helper",
	}


def test_resolve_requirements_handles_editable_uv_workspace_source(
	package_info_manager: PackageInfoManager, tmp_path: Path
) -> None:
	published_path = tmp_path / "published_dependency"
	write_pyproject(
		published_path,
		"""
[project]
name = "published-dependency"
version = "1.0.0"
""",
	)

	workspace_path = tmp_path / "workspace"
	write_pyproject(
		workspace_path / "packages" / "local_dependency",
		f"""
[project]
name = "local-dependency"
version = "1.0.0"
dependencies = ["published-dependency @ {published_path.as_uri()}"]
""",
	)
	pyproject_path = write_pyproject(
		workspace_path,
		"""
[project]
name = "project"
version = "1.0.0"
dependencies = ["local-dependency"]

[tool.uv.sources]
local-dependency = { workspace = true }

[tool.uv.workspace]
members = ["packages/local_dependency"]
""",
	)

	package_info_manager.resolve_requirements(
		requirements_paths={str(pyproject_path)},
		groups=set(),
		extras=set(),
		skip_dependencies=set(),
	)

	assert {requirement.name for requirement in package_info_manager.reqs} == {
		"local-dependency",
		"published-dependency",
	}


def test_resolve_requirements_handles_editable_path_with_spaces(
	package_info_manager: PackageInfoManager, tmp_path: Path
) -> None:
	published_path = tmp_path / "published_dependency"
	write_pyproject(
		published_path,
		"""
[project]
name = "published-dependency"
version = "1.0.0"
""",
	)

	write_pyproject(
		tmp_path / "local dependency",
		f"""
[project]
name = "local-dependency"
version = "1.0.0"
dependencies = ["published-dependency @ {published_path.as_uri()}"]
""",
	)
	pyproject_path = write_pyproject(
		tmp_path / "project",
		"""
[project]
name = "project"
version = "1.0.0"
dependencies = ["local-dependency"]

[tool.uv.sources]
local-dependency = { path = "../local dependency", editable = true }
""",
	)

	package_info_manager.resolve_requirements(
		requirements_paths={str(pyproject_path)},
		groups=set(),
		extras=set(),
		skip_dependencies=set(),
	)

	assert {requirement.name for requirement in package_info_manager.reqs} == {
		"local-dependency",
		"published-dependency",
	}


def test_resolve_requirements_uses_local_project_license_metadata(
	package_info_manager: PackageInfoManager,
	tmp_path: Path,
	monkeypatch: pytest.MonkeyPatch,
) -> None:
	local_path = tmp_path / "local_dependency"
	write_pyproject(
		local_path,
		"""
[project]
name = "local-dependency"
version = "1.2.3"
license = "LicenseRef-Example-Proprietary"
""",
	)
	pyproject_path = write_pyproject(
		tmp_path / "project",
		"""
[project]
name = "project"
version = "1.0.0"
dependencies = ["local-dependency"]

[tool.uv.sources]
local-dependency = { path = "../local_dependency" }
""",
	)

	def fake_run(*_args: object, **_kwargs: object) -> CompletedProcess[str]:
		return CompletedProcess(
			args=["uv", "pip", "compile"],
			returncode=0,
			stdout=f"local-dependency @ {local_path.as_uri()}\n",
			stderr="",
		)

	monkeypatch.setattr("licensecheck.packageinforesolver.subprocess.run", fake_run)

	package_info_manager.resolve_requirements(
		requirements_paths={str(pyproject_path)},
		groups=set(),
		extras=set(),
		skip_dependencies=set(),
	)
	package = package_info_manager.getPackages().pop()

	assert package.name == "local-dependency"
	assert package.version == "1.2.3"
	assert package.license == "LicenseRef-Example-Proprietary"
	assert package.errorCode == 0


def test_resolve_requirements_falls_back_for_uv_lock(
	package_info_manager: PackageInfoManager, tmp_path: Path
) -> None:
	lock_path = tmp_path / "uv.lock"
	lock_path.write_text(
		"""
version = 1

[[package]]
name = "fallback-package"
version = "1.2.3"
""".strip(),
		encoding="utf-8",
	)

	package_info_manager.resolve_requirements(
		requirements_paths={str(lock_path)},
		groups=set(),
		extras=set(),
		skip_dependencies=set(),
	)

	assert {str(requirement) for requirement in package_info_manager.reqs} == {
		"fallback-package==1.2.3"
	}


def test_resolve_requirements_preserves_pyproject_resolution_error(
	package_info_manager: PackageInfoManager,
	tmp_path: Path,
	monkeypatch: pytest.MonkeyPatch,
) -> None:
	pyproject_path = write_pyproject(
		tmp_path,
		"""
[project]
name = "project"
version = "1.0.0"
dependencies = ["dependency"]
""",
	)

	def fake_run(*_args: object, **_kwargs: object) -> CompletedProcess[str]:
		return CompletedProcess(
			args=["uv", "pip", "compile"],
			returncode=1,
			stdout="",
			stderr="index unavailable",
		)

	monkeypatch.setattr("licensecheck.packageinforesolver.subprocess.run", fake_run)

	with pytest.raises(RuntimeError, match="index unavailable"):
		package_info_manager.resolve_requirements(
			requirements_paths={str(pyproject_path)},
			groups=set(),
			extras=set(),
			skip_dependencies=set(),
		)


def test_resolve_requirements_falls_back_when_uv_is_unavailable(
	package_info_manager: PackageInfoManager,
	tmp_path: Path,
	monkeypatch: pytest.MonkeyPatch,
) -> None:
	pyproject_path = write_pyproject(
		tmp_path,
		"""
[project]
name = "project"
version = "1.0.0"
dependencies = ["dependency"]
""",
	)
	fallback_calls: list[Path] = []

	def missing_uv(*_args: object, **_kwargs: object) -> CompletedProcess[str]:
		message = "uv"
		raise FileNotFoundError(message)

	def fake_gather(**kwargs: object) -> set[Requirement]:
		requirements_path = kwargs["requirementsPath"]
		assert isinstance(requirements_path, Path)
		fallback_calls.append(requirements_path)
		return {Requirement("dependency==1.2.3")}

	monkeypatch.setattr("licensecheck.packageinforesolver.subprocess.run", missing_uv)
	monkeypatch.setattr("licensecheck.packageinforesolver.gather", fake_gather)

	package_info_manager.resolve_requirements({str(pyproject_path)}, set(), set(), set())

	assert fallback_calls == [pyproject_path]
	assert {str(requirement) for requirement in package_info_manager.reqs} == {"dependency==1.2.3"}
