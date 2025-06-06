"""Fic foeign key constarint in personal info

Revision ID: 99361b103c4b
Revises: d9f6a50baa05
Create Date: 2025-06-05 17:35:17.572750

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '99361b103c4b'
down_revision: Union[str, None] = 'd9f6a50baa05'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Fix the foreign key constraint
    op.drop_constraint('fk_personal_info_user', 'personal_info', type_='foreignkey')
    
    op.alter_column('personal_info', 'user_id', new_column_name='resume_version_id')
    
    op.create_foreign_key(
        'fk_personal_info_resume_version',
        'personal_info',
        'resume_version',
        ['resume_version_id'],
        ['id'],
        ondelete='CASCADE'
    )

def downgrade():
    # Revert the FK fix
    op.drop_constraint('fk_personal_info_resume_version', 'experience', type_='foreignkey')
    
    op.alter_column('personal_info', 'resume_version_id', new_column_name='resume_id')
    
    op.create_foreign_key(
        'fk_personal_info_resume',
        'personal_info',
        'resume',
        ['resume_id'],
        ['id'],
        ondelete='CASCADE'
    )
