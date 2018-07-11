"""empty message

Revision ID: 97e62ed32343
Revises: c8c23ed7f3b6
Create Date: 2018-07-11 18:55:29.329602

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '97e62ed32343'
down_revision = 'c8c23ed7f3b6'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'tablesubscriptions',
        sa.Column('gamer', sa.String(10), sa.ForeignKey('gamers.id'), primary_key=True),
        sa.Column('table', sa.String(10), sa.ForeignKey('tables.id'), primary_key=True),
    )


def downgrade():
    op.drop_table('tablesubscriptions')
