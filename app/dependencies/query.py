from collections.abc import Callable

from fastapi import HTTPException, Request, status


def strict_query_params(allowed_params: set[str]) -> Callable[[Request], None]:
    """
    Dependency to strictly validate that only allowed query parameters are present.
    Raises 422 Unprocessable Entity if undocumented parameters are found.
    """

    def validator(request: Request) -> None:
        for param in request.query_params:
            if param not in allowed_params:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail=f"Unknown query parameter: {param}",
                )

    return validator
