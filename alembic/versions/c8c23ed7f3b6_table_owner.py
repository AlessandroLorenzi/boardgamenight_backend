"""table owner

Revision ID: c8c23ed7f3b6
Revises: fd9d1586fe69
Create Date: 2018-07-02 18:30:45.913508

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c8c23ed7f3b6'
down_revision = 'fd9d1586fe69'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('tables') as batch_op:
        batch_op.add_column(sa.Column('owner', sa.String(10)))
        batch_op.create_foreign_key (
         "fk_gamers_tables", "gamers",
         ["owner"], ["id"]
        )


def downgrade():
    drop_column('tables', 'owner')
