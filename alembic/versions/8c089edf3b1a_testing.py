"""Testing

Revision ID: 8c089edf3b1a
Revises: 6a0838786d9f
Create Date: 2025-05-29 14:50:28.831247

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8c089edf3b1a'
down_revision: Union[str, None] = '6a0838786d9f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "students",
        sa.Column("name", sa.String(), primary_key=True),
        sa.Column("inSchool", sa.Boolean, nullable=False)
    )


def downgrade() -> None:
    op.drop_table("students")
