"""Cria relacionamento entre fornecedor e conta

Revision ID: fcebf0dda5cd
Revises: 4ce079f76a68
Create Date: 2023-11-16 19:24:46.236127

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fcebf0dda5cd'
down_revision: Union[str, None] = '4ce079f76a68'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('conta_a_pagar_e_receber', sa.Column('fornecedor_cliente_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'conta_a_pagar_e_receber', 'fonecedor_cliente', ['fornecedor_cliente_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'conta_a_pagar_e_receber', type_='foreignkey')
    op.drop_column('conta_a_pagar_e_receber', 'fornecedor_cliente_id')
    # ### end Alembic commands ###
