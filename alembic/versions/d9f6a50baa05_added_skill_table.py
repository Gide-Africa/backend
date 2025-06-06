"""Added Skill Table

Revision ID: d9f6a50baa05
Revises: c8c949e02ad0
Create Date: 2025-06-05 11:44:10.523298

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd9f6a50baa05'
down_revision: Union[str, None] = 'c8c949e02ad0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'skill',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('resume_version_id', sa.Integer(), sa.ForeignKey('resume_version.id'), nullable=False),
        sa.Column('skill_name', sa.String(length=255), nullable=False),
        sa.ForeignKeyConstraint(['resume_version_id'], ['resume_version.id'], ondelete='CASCADE', name='fk_skill_resume_version')
    )


def downgrade() -> None:
    op.drop_table('skill')