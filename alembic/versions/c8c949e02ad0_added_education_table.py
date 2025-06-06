"""Added Education Table

Revision ID: c8c949e02ad0
Revises: 766f814f1f35
Create Date: 2025-06-05 11:41:18.002688

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c8c949e02ad0'
down_revision: Union[str, None] = '766f814f1f35'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
   op.create_table(
        'education',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('resume_version_id', sa.Integer(), sa.ForeignKey('resume_version.id'), nullable=False),
        sa.Column('degree', sa.String(length=255), nullable=False),
        sa.Column('institution', sa.String(length=255), nullable=False),        
        sa.Column('start_date', sa.Date(), nullable=False), 
        sa.Column('end_date', sa.Date(), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(['resume_version_id'], ['resume_version.id'], ondelete='CASCADE', name='fk_education_resume_version')
    )
    


def downgrade() -> None:
    op.drop_table('education')
