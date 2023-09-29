from dataclasses import dataclass, asdict
from typing import Any, Optional

import orjson
from fastapi import Response


@dataclass
class DefaultResponse:
    ok: Optional[bool] = True
    data: Optional[Any] = None
    errors: Optional[Any] = None


class ResponseEnvelope(Response):
    media_type = "application/json"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def render(self, content: Any) -> bytes:
        response: DefaultResponse
        if isinstance(content, Exception):
            response = DefaultResponse(ok=False, errors=str(content))
        else:
            response = DefaultResponse(data=content)

        return orjson.dumps(asdict(response, dict_factory=lambda x: {k: v for (k, v) in x if v is not None}), option=orjson.OPT_INDENT_2)
