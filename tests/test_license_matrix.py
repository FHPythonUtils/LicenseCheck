import logging

import pytest

from licensecheck.license_matrix import licenseType, ucstr
from licensecheck.types import L


@pytest.mark.parametrize("license_string", [ucstr("GNU LIBRARY"), ucstr("UPL-1.0")])
def test_gnu_library_and_upl_1_is_recognized_without_warnings(
	caplog: pytest.LogCaptureFixture, license_string: ucstr
) -> None:
	with caplog.at_level(logging.WARNING):
		# Correct license where found.
		license_type = licenseType(license_string)
		assert len(license_type) == 1
		assert isinstance(license_type.pop(), L)
		assert L.UNKNOWN not in license_type
		# No warnings were emitted.
		if len(caplog.records):
			assert license_string not in caplog.text
