"""Criar tabela de contas a pagar e receber

Revision ID: 8bb97ccd2765
Revises:
Create Date: 2023-11-07 20:59:10.742264

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "8bb97ccd2765"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "conta_a_pagar_e_receber",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("descricao", sa.String(length=30), nullable=True),
        sa.Column("valor", sa.Numeric(), nullable=True),
        sa.Column("tipo", sa.String(length=30), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("conta_a_pagar_e_receber")
