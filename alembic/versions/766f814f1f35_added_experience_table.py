"""Added Experience Table

Revision ID: 766f814f1f35
Revises: c931305174b3
Create Date: 2025-06-05 11:37:09.418035

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '766f814f1f35'
down_revision: Union[str, None] = 'c931305174b3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'experience',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('resume_id', sa.Integer(), sa.ForeignKey('resume.id'), nullable=False),
        sa.Column('job_title', sa.String(length=255), nullable=False),
        sa.Column('company_name', sa.String(length=255), nullable=False),
        sa.Column('start_date', sa.Date(), nullable=False),
        sa.Column('end_date', sa.Date(), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(['resume_id'], ['resume.id'], ondelete='CASCADE', name='fk_experience_resume')
    )
    


def downgrade() -> None:
    op.drop_table('experience')
