"""Create index on GameHistory -> telegram_id

Revision ID: df92ec921509
Revises: 01_initial
Create Date: 2021-09-08 23:31:34.994806

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '02_create_telegram_id_index'
down_revision = '01_initial'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index(op.f('ix_gameshistory_telegram_id'), 'gameshistory', ['telegram_id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_gameshistory_telegram_id'), table_name='gameshistory')
    # ### end Alembic commands ###