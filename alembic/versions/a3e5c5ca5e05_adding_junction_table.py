"""Adding junction table"

Revision ID: a3e5c5ca5e05
Revises: bb06e54fa2e0
Create Date: 2021-12-31 21:15:22.500277

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'a3e5c5ca5e05'
down_revision = 'bb06e54fa2e0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Jobs_Applied',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('job_id', sa.Integer(), nullable=False),
    sa.Column('seeker_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['job_id'], ['Jobs.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['seeker_id'], ['Seekers.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_column('Seekers', 'jobs_applied')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Seekers', sa.Column('jobs_applied', postgresql.ARRAY(sa.INTEGER()), autoincrement=False, nullable=True))
    op.drop_table('Jobs_Applied')
    # ### end Alembic commands ###
