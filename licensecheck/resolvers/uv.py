"""Use uv to get packages from project/ requirements.txt."""

from __future__ import annotations

import shutil
import subprocess
import tempfile
from pathlib import Path

import requirements

from licensecheck.types import PackageInfo, ucstr


def get_reqs(
	skipDependencies: list[ucstr],
	groups: list[str],
	extras: list[str],
	requirementsPaths: list[str],
	index_url: str | None = "https://pypi.org/simple",
) -> set[PackageInfo]:
	for idx, requirement in enumerate(requirementsPaths):
		if not Path(requirement).exists():
			msg = f"Could not find specification of requirements ({requirement})."
			raise RuntimeError(msg)

		if not requirement.endswith("pyproject.toml") and requirement.endswith(".toml"):
			temp_dir_path = Path(tempfile.mkdtemp())
			destination_file = temp_dir_path / "pyproject.toml"
			shutil.copy(requirement, destination_file)
			requirementsPaths[idx] = destination_file.as_posix()

	groups_cmd = sum([("--group", group) for group in groups], ())
	extras_cmd = sum([("--extra", extra) for extra in extras], ())
	index_param = ("--index", index_url) if index_url else ()
	command = ["uv", "pip", "compile", *index_param, *requirementsPaths, *extras_cmd, *groups_cmd]

	result = subprocess.run(command, capture_output=True, text=True, check=False)

	if result.returncode != 0:
		raise RuntimeError(result.stderr, result.stdout)

	reqs = requirements.parse(result.stdout)

	return {
		PackageInfo(name=x.name or "", version=next((y[1] for y in x.specs), None))
		for x in reqs
		if ucstr(x.name) not in skipDependencies
	}
