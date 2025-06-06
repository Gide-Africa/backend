"""Added Column Skill gen by ai

Revision ID: 81309ea587d9
Revises: c7a49f789287
Create Date: 2025-06-06 03:56:23.657863

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '81309ea587d9'
down_revision: Union[str, None] = 'c7a49f789287'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'skill',
        sa.Column('skill_generated_by_ai', sa.Boolean(), nullable=True)
    )


def downgrade() -> None:
    op.drop_column('skill', 'skill_generated_by_ai')
