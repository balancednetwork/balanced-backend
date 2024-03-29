"""v0.2.2-fix-daily-pkeys

Revision ID: 1caf97846db1
Revises: f6bb95edd03d
Create Date: 2023-03-25 01:13:01.786818

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision = '1caf97846db1'
down_revision = 'f6bb95edd03d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('daily_historicals', 'contract_name',
               existing_type=sa.VARCHAR(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('daily_historicals', 'contract_name',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###
