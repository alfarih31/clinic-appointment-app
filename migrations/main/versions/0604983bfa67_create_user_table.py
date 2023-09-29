"""create user table

Revision ID: 0604983bfa67
Revises: 
Create Date: 2023-09-28 11:48:35.272657

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

from migrations.constants import SUPER_ADMIN_ROLE_ID, REGULAR_ROLE_ID
from migrations.main.commons.columns import common_columns, updated_at, created_at, id

# revision identifiers, used by Alembic.
revision: str = '0604983bfa67'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    role_table = op.create_table("role", sa.Column("id", sa.SMALLINT, primary_key=True), sa.Column("name", sa.VARCHAR(length=255)), created_at,
                                 updated_at)
    op.bulk_insert(role_table, [
        {
            "id": SUPER_ADMIN_ROLE_ID,
            "name": "Super Admin"
        },
        {
            "id": REGULAR_ROLE_ID,
            "name": "Regular"
        }])

    op.create_table("user",
                    *common_columns,
                    sa.Column("full_name", sa.VARCHAR(length=255), nullable=False))

    op.create_table("user_auth",
                    *common_columns,
                    sa.Column("user_id", sa.BIGINT, sa.ForeignKey("user.id"), nullable=False),
                    sa.Column("username", sa.VARCHAR(length=255), unique=True, nullable=False),
                    sa.Column("credential", sa.VARCHAR(length=255), nullable=False))

    op.create_table("user_has_role",
                    sa.Column("user_id", sa.BIGINT, sa.ForeignKey("user.id"), nullable=False),
                    sa.Column("role_id", sa.SMALLINT, sa.ForeignKey("role.id"), nullable=False),
                    id,
                    created_at)


def downgrade() -> None:
    op.drop_table("user_auth")
    op.drop_table("user_has_role")
    op.drop_table("role")
    op.drop_table("user")
