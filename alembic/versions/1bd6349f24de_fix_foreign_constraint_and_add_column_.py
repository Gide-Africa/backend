"""Fix foreign constraint and add column in summary table

Revision ID: 1bd6349f24de
Revises: 99361b103c4b
Create Date: 2025-06-05 18:40:54.714379

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1bd6349f24de'
down_revision: Union[str, None] = '99361b103c4b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
   op.drop_constraint(
        'fk_summary_resume',
        'summary',  
        type_='foreignkey'
    )
   
   op.add_column(
        'summary',
        sa.Column('summary_generated_by_ai', sa.Text(), nullable=True)
    )
   
   op.alter_column('summary', 'resume_id', new_column_name='resume_version_id')
   
   op.create_foreign_key(   
        'fk_summary_resume_version',
        'summary',
        'resume_version',
        ['resume_version_id'],
        ['id'],
        ondelete='CASCADE'
    )


def downgrade() -> None:
    op.drop_constraint(
        'fk_summary_resume_version',
        'summary',
        type_='foreignkey'
    )
    
    op.alter_column('summary', 'resume_version_id', new_column_name='resume_id')
    
    op.drop_column('summary', 'summary_generated_by_ai')
    
    op.create_foreign_key(
        'fk_summary_resume',
        'summary',
        'resume',
        ['resume_id'],
        ['id'],
        ondelete='CASCADE'
    )
