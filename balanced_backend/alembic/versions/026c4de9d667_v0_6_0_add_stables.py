"""v0.6.0-add-stables

Revision ID: 026c4de9d667
Revises: ef669e9ed598
Create Date: 2024-06-25 17:12:40.447851

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision = '026c4de9d667'
down_revision = 'ef669e9ed598'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tokens', sa.Column('is_stable', sa.Boolean(), nullable=True))
    op.add_column('tokens', sa.Column('in_stability_fund', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('tokens', 'in_stability_fund')
    op.drop_column('tokens', 'is_stable')
    # ### end Alembic commands ###
