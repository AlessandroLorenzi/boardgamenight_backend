"""event owner

Revision ID: fd9d1586fe69
Revises: 1fa86016f6b1
Create Date: 2018-06-22 21:14:32.521756

"""
from alembic import op

from sqlalchemy import MetaData, Table, Column, Integer, ForeignKey, String

meta = MetaData()

# revision identifiers, used by Alembic.
revision = 'fd9d1586fe69'
down_revision = '1fa86016f6b1'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('events') as batch_op:
        batch_op.add_column(Column('owner', String(10)))
        batch_op.create_foreign_key (
         "fk_gamers_events", "gamers",
         ["owner"], ["id"]
        )


def downgrade():
    drop_column('events', 'owner')
