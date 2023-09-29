import os
from typing import List

from dihub.constants import ProviderScope
from dihub.decorators import provider, export
from dotenv import load_dotenv


class EnvNotExistException(Exception):
    def __init__(self, key: str):
        super(EnvNotExistException, self).__init__("this %s: variable not exist" % key)


@export
@provider(scope=ProviderScope.LOCAL)
class Env:

    def __init__(self):
        load_dotenv()

    @classmethod
    def get_str(cls, key: str, default: str = None) -> str:
        if default is not None:
            val = os.getenv(key, default)
            if val == "":
                return default
            return val

        try:
            val = os.environ[key]
            return val
        except KeyError:
            raise EnvNotExistException(key)

    @classmethod
    def get_int(cls, key: str, default: int = None) -> int:
        if default is not None:
            return int(os.getenv(key, default))

        try:
            val = os.environ[key]
            if val == "":
                return 0
            return int(val)
        except KeyError:
            raise EnvNotExistException(key)
        except ValueError as e:
            raise ValueError("this %s: %s" % (key, str(e)))

    @classmethod
    def get_bool(cls, key: str, default: bool = None) -> bool:
        bool_map = {
            "TRUE": True,
            "FALSE": False,
            "1": True,
            "0": False,
        }
        if default is not None:
            val = os.getenv(key)
            if val is None:
                return default

            val = val.upper()
            if val in bool_map:
                return bool_map[val]
            raise ValueError("this %s: cannot convert value to bool" % key)

        try:
            val = os.environ[key]

            if val in bool_map:
                return bool_map[val]
            raise ValueError("this %s: cannot convert value to bool" % key)
        except KeyError:
            raise EnvNotExistException(key)

    @classmethod
    def get_str_list(cls, key: str, default: List[str] = None, separator=",") -> List[str]:
        if default is not None:
            val = os.getenv(key)
            if val is None:
                return default

            return val.split(separator)

        try:
            val = os.environ[key]
            return val.split(separator)
        except KeyError:
            raise EnvNotExistException(key)

    @classmethod
    def get_int_list(cls, key: str, default: List[int] = None, separator=',') -> List[int]:
        if default is not None:
            val = os.getenv(key)
            if val is None:
                return default

            val = val.split(separator)
            i_val = []
            try:
                for v in val:
                    i_val.append(int(v))

                return i_val
            except ValueError as e:
                raise ValueError("this %s: %s" % (key, str(e)))

        try:
            val = os.environ[key]

            val = val.split(separator)
            i_val = []
            for v in val:
                i_val.append(int(v))

            return i_val
        except KeyError:
            raise EnvNotExistException(key)
        except ValueError as e:
            raise ValueError("this %s: %s" % (key, str(e)))
