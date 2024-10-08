"""Initial migration

Revision ID: 0303f461877a
Revises: 
Create Date: 2024-08-12 21:54:31.436347

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0303f461877a'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_parts_id', table_name='parts')
    op.drop_index('ix_parts_name', table_name='parts')
    op.drop_table('parts')
    op.drop_index('ix_changeover_times_from_part_id', table_name='changeover_times')
    op.drop_index('ix_changeover_times_id', table_name='changeover_times')
    op.drop_index('ix_changeover_times_to_part_id', table_name='changeover_times')
    op.drop_table('changeover_times')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('changeover_times',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('from_part_id', sa.INTEGER(), nullable=True),
    sa.Column('to_part_id', sa.INTEGER(), nullable=True),
    sa.Column('time', sa.FLOAT(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_changeover_times_to_part_id', 'changeover_times', ['to_part_id'], unique=False)
    op.create_index('ix_changeover_times_id', 'changeover_times', ['id'], unique=False)
    op.create_index('ix_changeover_times_from_part_id', 'changeover_times', ['from_part_id'], unique=False)
    op.create_table('parts',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.VARCHAR(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_parts_name', 'parts', ['name'], unique=1)
    op.create_index('ix_parts_id', 'parts', ['id'], unique=False)
    # ### end Alembic commands ###
