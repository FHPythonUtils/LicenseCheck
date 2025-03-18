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
	index_url: str = "https://pypi.org/simple",
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

	groups_cmd = [f"--group {group}" for group in groups]
	extras_cmd = [f"--extra {extra}" for extra in extras]
	command = (
		f"uv pip compile --index {index_url}"
		f" {' '.join(requirementsPaths)} {' '.join(extras_cmd)} {' '.join(groups_cmd)}"
	)

	result = subprocess.run(command, shell=True, capture_output=True, text=True, check=False)

	if result.returncode != 0:
		raise RuntimeError(result.stderr, result.stdout)

	reqs = requirements.parse(result.stdout)

	return {
		PackageInfo(name=x.name or "", version=next((y[1] for y in x.specs), None))
		for x in reqs
		if ucstr(x.name) not in skipDependencies
	}
