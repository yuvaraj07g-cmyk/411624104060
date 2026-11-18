"""add gin index on metadata

Revision ID: 8c7e4a1f9b20
Revises: 3d1a9f6b2c4e
Create Date: 2026-11-18
"""

from typing import Sequence, Union

from alembic import op

revision: str = "8c7e4a1f9b20"
down_revision: Union[str, None] = "3d1a9f6b2c4e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_index(
        "ix_documents_metadata_gin",
        "documents",
        ["metadata"],
        postgresql_using="gin",
        postgresql_ops={"metadata": "jsonb_path_ops"},
    )


def downgrade() -> None:
    op.drop_index("ix_documents_metadata_gin", table_name="documents")
