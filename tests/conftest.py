import logging
from typing import Generator

import pytest
from _pytest.logging import LogCaptureFixture
from _pytest.logging import caplog as _caplog
from loguru import logger

_ = _caplog


@pytest.fixture
def caplog(_caplog: LogCaptureFixture) -> Generator[LogCaptureFixture, None, None]:
	"""Wrapper over caplog fixture to fix loguru logs.

	Yields
	------
	_caplog: Pytest fixture
	"""

	class PropogateHandler(logging.Handler):
		def emit(self, record) -> None:
			logging.getLogger(record.name).handle(record)

	logger.add(PropogateHandler(), format="{message}")
	handler_id = logger.add(PropogateHandler(), format="{message}")
	yield _caplog
	logger.remove(handler_id)
