"""seed super admin

Revision ID: f280fdf2d702
Revises:
Create Date: 2023-09-29 12:56:02.776133

"""
import logging
import random
import string
from typing import Sequence, Union

from alembic import op
from sqlalchemy.sql import table, column
from sqlalchemy.types import VARCHAR, BIGINT, SMALLINT

from migrations.constants import SUPER_ADMIN_ROLE_ID
from src.shared import BcryptHash, Env

# revision identifiers, used by Alembic.
revision: str = 'f280fdf2d702'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

env = Env()


def gen_random_string(length=8) -> str:
    return ''.join(random.choices(
        string.digits + string.ascii_letters, k=length))


SUPER_ADMIN_FULLNAME = "Super Admin %s" % gen_random_string()
SUPER_ADMIN_USERNAME = "superadmin@app.com"
SUPER_ADMIN_PASSWORD = gen_random_string(12)

user_table = table("user", column("id", BIGINT), column("full_name", VARCHAR(255)))
user_auth_table = table("user_auth", column("user_id", BIGINT), column("username", VARCHAR(255)), column("credential", VARCHAR(255)))
user_has_role_table = table("user_has_role", column("user_id", BIGINT), column("role_id", SMALLINT))


def upgrade() -> None:
    op.bulk_insert(user_table, [{
        "full_name": SUPER_ADMIN_FULLNAME,
    }])

    connection = op.get_bind()
    result = connection.execute(user_table.select().where(user_table.c.full_name == op.inline_literal(SUPER_ADMIN_FULLNAME)).limit(1))
    id, _ = result.one()

    #
    op.bulk_insert(user_auth_table, [{
        "user_id": id,
        "username": SUPER_ADMIN_USERNAME,
        "credential": BcryptHash.generate_hash(SUPER_ADMIN_PASSWORD, env.get_int("BCRYPT_SALT_ROUNDS"))
    }])

    op.bulk_insert(user_has_role_table, [
        {
            "user_id": id,
            "role_id": SUPER_ADMIN_ROLE_ID
        }
    ])

    logging.getLogger("alembic.runtime.migration").warning(
        "Save this generated Super Admin. This credential will only be displayed once!\n- username: %s\n- password: %s" % (
            SUPER_ADMIN_USERNAME, SUPER_ADMIN_PASSWORD))


def downgrade() -> None:
    connection = op.get_bind()
    result = connection.execute(user_auth_table.select().where(user_auth_table.c.username == op.inline_literal(SUPER_ADMIN_USERNAME)))

    connection.execute(user_auth_table.delete().where(user_auth_table.c.username == op.inline_literal(SUPER_ADMIN_USERNAME)))

    for user_id, *any in result.all():
        connection.execute(user_has_role_table.delete().where(user_has_role_table.c.user_id == op.inline_literal(user_id)))
        connection.execute(user_table.delete().where(user_table.c.id == op.inline_literal(user_id)))
