from collections.abc import Callable

from fastapi import Request
from fastapi.exceptions import RequestValidationError


def strict_query_params(allowed_params: set[str]) -> Callable[[Request], None]:
    """
    Dependency to strictly validate that only allowed query parameters are present.
    Raises RequestValidationError (422) if undocumented parameters are found.
    """

    def validator(request: Request) -> None:
        errors = []
        for param in request.query_params:
            if param not in allowed_params:
                errors.append(
                    {
                        "loc": ("query", param),
                        "msg": "Extra inputs are not permitted",
                        "type": "extra_forbidden",
                    }
                )

        if errors:
            raise RequestValidationError(errors)

    return validator
