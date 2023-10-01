from dataclasses import dataclass, asdict, is_dataclass
from typing import Any, Optional, Dict

import orjson
from fastapi import Response


@dataclass
class DefaultResponse:
    ok: Optional[bool] = True
    data: Optional[Any] = None
    errors: Optional[Any] = None


class ResponseEnvelope(Response):
    media_type = "application/json"

    @staticmethod
    def __dataclass_to_dict(d: dataclass) -> dict:
        if not is_dataclass(d):
            return {}
        return asdict(d, dict_factory=lambda x: {k: v for (k, v) in x if v is not None})

    @staticmethod
    def __merge_dataclass_to_dict(*dicts) -> Dict:
        base = {}
        for d in dicts:
            if is_dataclass(d):
                d_dict = ResponseEnvelope.__dataclass_to_dict(d)
            elif isinstance(d, dict):
                d_dict = d
            else:
                continue
            base.update(d_dict)
        return base

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def render(self, content: Any) -> bytes:
        response_dict: Dict
        if isinstance(content, Exception):
            response_dict = ResponseEnvelope.__merge_dataclass_to_dict(DefaultResponse(ok=False, errors=str(content)))
        elif is_dataclass(content) or isinstance(content, dict):
            # Merge into default response
            response_dict = ResponseEnvelope.__merge_dataclass_to_dict(DefaultResponse(), content)
        else:
            response_dict = ResponseEnvelope.__dataclass_to_dict(DefaultResponse(data=content))

        return orjson.dumps(response_dict, option=orjson.OPT_INDENT_2)
