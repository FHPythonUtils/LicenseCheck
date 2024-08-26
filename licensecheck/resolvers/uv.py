"""Use uv to get packages from project/ requirements.txt."""

from __future__ import annotations

import shutil
import subprocess
import tempfile
from pathlib import Path

import requirements

from licensecheck.types import ucstr


def get_reqs(
	using: str,
	skipDependencies: list[ucstr],
	extras: list[str],
	requirementsPaths: list[str],
) -> set[ucstr]:
	if using == "requirements" and len(extras) > 0:
		msg = "You may not use extras with requirements.txt"
		raise RuntimeError(msg)

	for idx, requirement in enumerate(requirementsPaths):
		if not Path(requirement).exists():
			msg = f"Could not find specification of requirements ({requirement})."
			raise RuntimeError(msg)

		if not requirement.endswith("pyproject.toml") and requirement.endswith(".toml"):
			temp_dir_path = Path(tempfile.mkdtemp())
			destination_file = temp_dir_path / "pyproject.toml"
			shutil.copy(requirement, destination_file)
			requirementsPaths[idx] = destination_file.as_posix()

	extras_cmd = [f"--extra {extra}" for extra in extras]
	command = f"uv pip compile {' '.join(requirementsPaths)} {' '.join(extras_cmd)}"

	result = subprocess.run(command, shell=True, capture_output=True, text=True, check=False)

	if result.returncode != 0:
		raise RuntimeError(result.stderr)

	reqs = requirements.parse(result.stdout)
	reqs_out = [ucstr(x.name) for x in reqs]

	return set(reqs_out) - set(skipDependencies)
