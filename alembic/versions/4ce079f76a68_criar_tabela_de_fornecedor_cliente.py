"""Criar tabela de fornecedor cliente

Revision ID: 4ce079f76a68
Revises: 8bb97ccd2765
Create Date: 2023-11-11 21:27:13.281783

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '4ce079f76a68'
down_revision: Union[str, None] = '8bb97ccd2765'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('fonecedor_cliente',
                    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
                    sa.Column('nome', sa.String(length=255), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )


def downgrade() -> None:
    op.drop_table('fonecedor_cliente')
