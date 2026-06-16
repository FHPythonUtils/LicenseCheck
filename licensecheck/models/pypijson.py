from datetime import UTC, datetime

from pydantic import Field, HttpUrl

from licensecheck.models.defaultonnone import DefaultOnNoneModel

DEFAULT_URL = HttpUrl("http://example.com")


class Downloads(DefaultOnNoneModel):
	last_day: int = 0
	last_month: int = 0
	last_week: int = 0


class Digests(DefaultOnNoneModel):
	blake2b_256: str = ""
	md5: str = ""
	sha256: str = ""


class Info(DefaultOnNoneModel):
	author: str = ""
	author_email: str = ""
	bugtrack_url: str = ""
	classifiers: list[str] = Field(default_factory=list)
	description: str = ""
	description_content_type: str = ""
	docs_url: str = ""
	download_url: str = ""
	downloads: Downloads = Downloads()
	dynamic: list[str] = Field(default_factory=list)
	home_page: str = ""
	keywords: str = ""
	license: str = ""
	license_expression: str = ""
	license_files: list[str] | None = None
	maintainer: str = ""
	maintainer_email: str = ""
	name: str = ""
	package_url: HttpUrl = DEFAULT_URL
	platform: str = ""
	project_url: HttpUrl = DEFAULT_URL
	project_urls: dict[str, HttpUrl] = Field(default_factory=dict)
	provides_extra: list[str] = Field(default_factory=list)
	release_url: HttpUrl = DEFAULT_URL
	requires_dist: list[str] | None = None
	requires_python: str = ""
	summary: str = ""
	version: str = ""
	yanked: bool = False
	yanked_reason: str = ""


class File(DefaultOnNoneModel):
	comment_text: str = ""
	digests: Digests = Digests()
	downloads: int = 0
	filename: str = ""
	has_sig: bool = False
	md5_digest: str = ""
	packagetype: str = ""
	python_version: str = ""
	requires_python: str = ""
	size: int | None = None
	upload_time: datetime = datetime(1970, 1, 1, tzinfo=UTC)
	upload_time_iso_8601: datetime = datetime(1970, 1, 1, tzinfo=UTC)
	url: HttpUrl = DEFAULT_URL
	yanked: bool = False
	yanked_reason: str = ""


class OwnershipRole(DefaultOnNoneModel):
	role: str = ""
	user: str = ""


class Ownership(DefaultOnNoneModel):
	roles: list[OwnershipRole]
	organization: str = ""


class Vulnerability(DefaultOnNoneModel):
	# PyPI's schema can evolve; keep flexible unless you need validation.
	pass


class ProjectResponse(DefaultOnNoneModel):
	info: Info = Info()
	last_serial: int = 1
	urls: list[File] = Field(default_factory=list)
	vulnerabilities: list[dict] = Field(default_factory=list)
	ownership: Ownership | None = None
