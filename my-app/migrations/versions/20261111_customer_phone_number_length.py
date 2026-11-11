"""Change phone_number length to 11.

Revision ID: 20261111_phone_length
Revises: 20261110_email_only_customers
Create Date: 2026-11-11
"""
# Change phone_number length to 11
from alembic import op
import sqlalchemy as sa


revision = "20261111_phone_length"
down_revision = "20261110_email_only_customers"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("customers") as batch_op:
        batch_op.alter_column(
            "phone_number",
            existing_type=sa.String(length=15),
            type_=sa.String(length=11),
            existing_nullable=True,
        )


def downgrade():
    with op.batch_alter_table("customers") as batch_op:
        batch_op.alter_column(
            "phone_number",
            existing_type=sa.String(length=11),
            type_=sa.String(length=15),
            existing_nullable=True,
        )
