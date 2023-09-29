import sqlalchemy as sa

id = sa.Column("id", sa.BIGINT, primary_key=True, autoincrement=True)
created_at = sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.func.now())
updated_at = sa.Column("updated_at", sa.TIMESTAMP(timezone=True), server_default=sa.func.now())

common_columns = [id, created_at, updated_at]
