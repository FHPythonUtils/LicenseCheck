from typing import Any

from pydantic import BaseModel, model_validator


class DefaultOnNoneModel(BaseModel):
	@model_validator(mode="before")
	@classmethod
	def default_on_none(cls, values: Any) -> Any | dict[Any, Any]:
		if not isinstance(values, dict):
			return values

		result = dict(values)

		for name, field in cls.model_fields.items():
			if name in result and result[name] is None:
				if field.default_factory is not None:
					result[name] = field.default_factory()
				elif field.default is not None:
					result[name] = field.default

		return result
