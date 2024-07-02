"""поля_для_зарплаты_decimal_новая__версия

Revision ID: 518df83958fa
Revises: f9af4aaa9090
Create Date: 2024-07-01 18:45:03.307139

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '518df83958fa'
down_revision = 'f9af4aaa9090'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('jobs', sa.Column('salary_from', sa.DECIMAL(), nullable=True, comment='Зарплата от'))
    op.add_column('jobs', sa.Column('salary_to', sa.DECIMAL(), nullable=True, comment='Зарплата до'))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('jobs', 'salary_to')
    op.drop_column('jobs', 'salary_from')
    # ### end Alembic commands ###
