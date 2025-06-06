"""Updated description Column Name to additional_info

Revision ID: c7a49f789287
Revises: d1e9e3a88db0
Create Date: 2025-06-06 03:52:30.204725

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c7a49f789287'
down_revision: Union[str, None] = 'd1e9e3a88db0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        'education',
        'description',
        new_column_name='additional_info'
    )


def downgrade() -> None:
    op.alter_column(
        'education',
        'additional_info',
        new_column_name='description'
    )
