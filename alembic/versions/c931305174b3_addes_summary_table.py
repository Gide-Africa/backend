"""Addes Summary Table

Revision ID: c931305174b3
Revises: b355696d894f
Create Date: 2025-06-05 11:33:51.345527

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c931305174b3'
down_revision: Union[str, None] = 'b355696d894f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'summary',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('resume_id', sa.Integer(), sa.ForeignKey('resume.id'), nullable=False),
        sa.Column('summary_text', sa.Text(), nullable=False),
        sa.ForeignKeyConstraint(['resume_id'], ['resume.id'], ondelete='CASCADE', name='fk_summary_resume')
    )
    

def downgrade() -> None:
    op.drop_table('summary')
    op.drop_constraint('fk_summary_resume', 'summary', type_='foreignkey')