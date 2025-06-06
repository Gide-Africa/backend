"""updated summary gen by ai column to correct data type

Revision ID: 0c284404002f
Revises: 81309ea587d9
Create Date: 2025-06-06 03:58:39.638517

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0c284404002f'
down_revision: Union[str, None] = '81309ea587d9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        'summary',
        'summary_generated_by_ai',
        type=sa.Boolean(),
        existing_type=sa.Text()
    )

def downgrade() -> None:
    op.alter_column(
        'summary',
        'summary_generated_by_ai',
        type=sa.Text(),
        existing_type=sa.Boolean()
    )
