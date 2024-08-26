from __future__ import annotations

import contextlib
import re
from importlib import metadata
from pathlib import Path
from typing import Any

from packaging.requirements import Requirement
from packaging.utils import canonicalize_name

from licensecheck.session import session
from licensecheck.types import ucstr


def get_reqs(
	using: str,
	skipDependencies: list[ucstr],
	extras: list[str],
	pyproject: dict[str, Any],
	requirementsPaths: list[Path],
) -> set[ucstr]:
	"""Underlying machineary to get requirements.

	Args:
	----
		using (str): use requirements, poetry or PEP631.
		skipDependencies (list[str]): list of dependencies to skip.
		extras (str | None): to-do
		pyproject (dict[str, Any]): to-do
		requirementsPaths (list[Path]): to-do

	Returns:
	-------
		set[str]: set of requirement packages

	"""
	reqs = set()
	extrasReqs = {}

	def resolveReq(req: str, *, extra: bool = True) -> ucstr:
		requirement = Requirement(req)
		extras = {ucstr(extra) for extra in requirement.extras}
		name = ucstr(canonicalize_name(requirement.name))
		canonicalName = name
		if len(extras) > 0:
			canonicalName = ucstr(f"{name}[{next(iter(extras))}]")
			# Avoid overwriting the initial mapping in extrasReqs, only overwrite when extra is True
			if extra:
				extrasReqs[name] = extras
		return canonicalName if extra else name

	def resolveExtraReq(extraReq: str) -> ucstr | None:
		match = re.search(r"extra\s*==\s*[\"'](.*?)[\"']", extraReq)
		if match is None:
			return None
		return ucstr(match.group(1))

	if using == "poetry":
		try:
			project = pyproject["tool"]["poetry"]
			reqLists = [project["dependencies"]]
		except KeyError as error:
			msg = "Could not find specification of requirements (pyproject.toml)."
			raise RuntimeError(msg) from error
		for extra in extras:
			reqLists.append(
				project.get("group", {extra: {"dependencies": {}}})[extra]["dependencies"]
			)
			reqLists.append(project.get("dev-dependencies", {}))
		for reqList in reqLists:
			for req in reqList:
				reqs.add(resolveReq(req))
	# PEP631
	if using == "PEP631":
		try:
			project = pyproject["project"]
			reqLists = [project["dependencies"]]
		except KeyError as error:
			msg = "Could not find specification of requirements (pyproject.toml)."
			raise RuntimeError(msg) from error
		for extra in extras:
			reqLists.append(project["optional-dependencies"][extra])
		for reqList in reqLists:
			for req in reqList:
				reqs.add(resolveReq(req))

	# Requirements
	if using == "requirements":
		for reqPath in requirementsPaths:
			if not reqPath.exists():
				msg = f"Could not find specification of requirements ({reqPath})."
				raise RuntimeError(msg)

			for _line in reqPath.read_text(encoding="utf-8").splitlines():
				line = _line.rstrip("\\").strip()
				if not line or line[0] in {"#", "-"}:
					continue
				reqs.add(resolveReq(line))

	# Remove PYTHON if define as requirement
	with contextlib.suppress(KeyError):
		reqs.remove("PYTHON")
	# Remove skip dependencies
	for skipDependency in skipDependencies:
		with contextlib.suppress(KeyError):
			reqs.remove(skipDependency)

	# Get Dependencies, 1 deep
	requirementsWithDeps = reqs.copy()

	def update_dependencies(dependency: str) -> None:
		dep = resolveReq(dependency, extra=False)
		req = resolveReq(requirement, extra=False)
		extra = resolveExtraReq(dependency)
		if extra is not None:
			if req in extrasReqs and extra in extrasReqs.get(req, []):
				requirementsWithDeps.add(dep)
		else:
			requirementsWithDeps.add(dep)

	for requirement in reqs:
		try:
			pkgMetadata = metadata.metadata(requirement)
			for dependency in pkgMetadata.get_all("Requires-Dist") or []:
				update_dependencies(dependency)
		except metadata.PackageNotFoundError:  # noqa: PERF203
			request = session.get(
				f"https://pypi.org/pypi/{requirement.split('[')[0]}/json", timeout=60
			)
			response: dict = request.json()
			requires_dist: list = response.get("info", {}).get("requires_dist", []) or []
			for dependency in requires_dist:
				update_dependencies(dependency)

	return {r.split("[")[0] for r in requirementsWithDeps}
