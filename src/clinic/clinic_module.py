from dihub.decorators import module

from .clinic_controller import ClinicController
from .commands import command_handlers
from .queries import query_handlers
from .repositories import repositories


@module(providers=[ClinicController] + repositories + command_handlers + query_handlers)
class ClinicModule: ...
