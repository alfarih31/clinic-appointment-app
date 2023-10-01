"""create clinic table

Revision ID: 889b360ea564
Revises: 0604983bfa67
Create Date: 2023-09-29 21:41:17.147686

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

from migrations.main.commons.columns import common_columns

# revision identifiers, used by Alembic.
revision: str = '889b360ea564'
down_revision: Union[str, None] = '0604983bfa67'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("clinic",
                    *common_columns,
                    sa.Column("name", sa.VARCHAR(length=255), nullable=False),
                    sa.Column("slug", sa.VARCHAR(length=255), nullable=False, unique=True))

    op.create_table("patient",
                    *common_columns,
                    sa.Column("user_id", sa.BIGINT, sa.ForeignKey("user.id"), nullable=False),
                    sa.Column("clinic_id", sa.BIGINT, sa.ForeignKey("clinic.id"), nullable=False))

    op.create_table("clinic_admin",
                    *common_columns,
                    sa.Column("user_id", sa.BIGINT, sa.ForeignKey("user.id"), nullable=False),
                    sa.Column("clinic_id", sa.BIGINT, sa.ForeignKey("clinic.id"), nullable=False))

    op.create_table("appointment",
                    *common_columns,
                    sa.Column("patient_id", sa.BIGINT, sa.ForeignKey("patient.id"), nullable=False),
                    sa.Column("queue", sa.SMALLINT, nullable=False),
                    sa.Column("status_id", sa.SMALLINT, nullable=False),
                    sa.Column("promised_start_date", sa.TIMESTAMP(timezone=True), nullable=False),
                    sa.Column("estimated_end_date", sa.TIMESTAMP(timezone=True), nullable=False),
                    sa.Column("promised_duration", sa.SMALLINT, nullable=False))


def downgrade() -> None:
    op.drop_table("appointment")
    op.drop_table("patient")
    op.drop_table("clinic_admin")
    op.drop_table("clinic")
