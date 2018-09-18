"""empty message

Revision ID: 126700bdf66a
Revises: 97e62ed32343
Create Date: 2018-09-18 13:30:41.459409

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '126700bdf66a'
down_revision = '97e62ed32343'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('events') as batch_op:
        batch_op.add_column(sa.Column('image', sa.String(1024)))

def downgrade():
    drop_column('events', 'image')
