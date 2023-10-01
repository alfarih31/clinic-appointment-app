from dihub.decorators import module, for_root, root
from dihub.plugins import ASGI
from dihub_cqrs import CQRSModule

from .auth import AuthModule
from .clinic import ClinicModule
from .fast_api import FastAPIModule, FastAPIProvider
from .shared.providers import Env
from .sql_alchemy import SqlAlchemyModule


@root(plugins=[ASGI(from_module=FastAPIModule, from_provider=FastAPIProvider)])
@module(imports=[
    for_root(CQRSModule),
    for_root(FastAPIModule),
    for_root(SqlAlchemyModule),
    for_root(AuthModule),
    ClinicModule],
    providers=[Env])
class App: ...
