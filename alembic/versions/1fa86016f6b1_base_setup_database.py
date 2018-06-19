"""base setup database

Revision ID: 1fa86016f6b1
Revises:
Create Date: 2018-06-19 19:07:11.257776

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1fa86016f6b1'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'gamers',
        sa.Column('id', sa.String(10), primary_key=True),
        sa.Column('username', sa.String(80), unique=True),
        sa.Column('email', sa.String(80)),
        sa.Column('password', sa.String(60), unique=True)
    )
    op.create_table(
        'evants',
        sa.Column('id', sa.String(10), primary_key=True),
        sa.Column('name', sa.String(80)),
        sa.Column('startdate', sa.DateTime(80)),
        sa.Column('enddate', sa.DateTime(80)),
        sa.Column('org', sa.String(80)),
        sa.Column('place', sa.String(80))
    )
    op.create_table(
        'tables',
        sa.Column('id', sa.String(10), primary_key=True),
        sa.Column('game', sa.String(80)),
        sa.Column('event_id', sa.String(10), sa.ForeignKey('events.id'))
    )

def downgrade():
    op.drop_table('gamers')
    op.drop_table('events')
    op.drop_table('tables')
