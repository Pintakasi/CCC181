"""Allow customers to sign up with email only.

Revision ID: 20261110_email_only_customers
Revises: 20261110_customer_email
Create Date: 2026-11-10
"""
from alembic import op
import sqlalchemy as sa


revision = "20261110_email_only_customers"
down_revision = "20261110_customer_email"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("customers") as batch_op:
        batch_op.alter_column(
            "phone_number",
            existing_type=sa.String(length=15),
            nullable=True,
        )


def downgrade():
    with op.batch_alter_table("customers") as batch_op:
        batch_op.alter_column(
            "phone_number",
            existing_type=sa.String(length=15),
            nullable=False,
        )
