"""Correct columns in personal info

Revision ID: 4479dafc5581
Revises: 1bd6349f24de
Create Date: 2025-06-06 02:58:00.522296

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4479dafc5581'
down_revision: Union[str, None] = '1bd6349f24de'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        'personal_info',
        'phone_number',
        existing_type=sa.String(length=20),
        nullable=False
    )
    
    op.drop_column('personal_info', 'address')
    
    op.add_column('personal_info', sa.Column('location', sa.String(length=255), nullable=True))
    op.add_column('personal_info', sa.Column('linkedin_url', sa.String(length=255), nullable=True))
    op.add_column('personal_info', sa.Column('portfolio_url', sa.String(length=255), nullable=True))
    
    
def downgrade() -> None:
    op.alter_column(
        'personal_info',
        'phone_number',
        existing_type=sa.String(length=20),
        nullable=True
    )
    
    op.add_column('personal_info', sa.Column('address', sa.String(length=500), nullable=True))
    
    op.drop_column('personal_info', 'location')
    op.drop_column('personal_info', 'linkedin_url')
    op.drop_column('personal_info', 'portfolio_url')
    
   