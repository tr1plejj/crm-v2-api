"""new fields for order

Revision ID: 3d3062a1b8a5
Revises: 8cb7f541e260
Create Date: 2024-11-26 22:55:22.765385

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3d3062a1b8a5'
down_revision: Union[str, None] = '8cb7f541e260'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('order', sa.Column('city', sa.String(), nullable=False))
    op.add_column('order', sa.Column('address', sa.String(), nullable=False))
    op.add_column('order', sa.Column('index', sa.Integer(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('order', 'index')
    op.drop_column('order', 'address')
    op.drop_column('order', 'city')
    # ### end Alembic commands ###