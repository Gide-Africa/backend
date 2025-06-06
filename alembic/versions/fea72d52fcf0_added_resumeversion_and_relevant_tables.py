"""Added ResumeVersion and relevant tables

Revision ID: fea72d52fcf0
Revises: 822f8de0f4af
Create Date: 2025-06-05 09:50:46.403553

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fea72d52fcf0'
down_revision: Union[str, None] = '822f8de0f4af'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'resume_version',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('resume_id', sa.Integer(), sa.ForeignKey('resume.id'), nullable=False),
        sa.Column('version_number', sa.Integer(), nullable=False),              
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
    )
    

def downgrade() -> None:
    op.drop_table('resume_version')
    