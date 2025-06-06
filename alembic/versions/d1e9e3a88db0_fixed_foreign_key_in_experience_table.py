"""fixed foreign key in experience table

Revision ID: d1e9e3a88db0
Revises: 4479dafc5581
Create Date: 2025-06-06 03:45:12.584549

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd1e9e3a88db0'
down_revision: Union[str, None] = '4479dafc5581'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_constraint('fk_experience_resume', 'experience', type_='foreignkey')
    
    op.alter_column(
        'experience',
        'resume_id',
        new_column_name='resume_version_id'
    )
    
    op.alter_column(
        'experience',
        'description',
        existing_type=sa.Text(),
        nullable=False
    )
    
    op.add_column(
        'experience',
        sa.Column('desc_generated_by_ai', sa.Boolean(), nullable=True)
    )   
    
    op.create_foreign_key(  
        'fk_experience_resume_version',
        'experience',
        'resume_version',
        ['resume_version_id'],
        ['id'],
        ondelete='CASCADE'
    )
    

def downgrade() -> None:
    op.drop_constraint('fk_experience_resume_version', 'experience', type_='foreignkey')
    
    op.alter_column(
        'experience',
        'resume_version_id',
        new_column_name='resume_id'
    )
    
    op.alter_column(
        'experience',
        'description',
        existing_type=sa.Text(),
        nullable=True
    )
    
    op.drop_column('experience', 'desc_generated_by_ai')
    
    op.create_foreign_key(  
        'fk_experience_resume',
        'experience',
        'resume',
        ['resume_id'],
        ['id'],
        ondelete='CASCADE'
    )
