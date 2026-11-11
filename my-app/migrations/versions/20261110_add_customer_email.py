"""Add email to customers.

Revision ID: 20261110_customer_email
Revises: 697400571e57
Create Date: 2026-11-10
"""
from alembic import op
import sqlalchemy as sa


revision = "20261110_customer_email"
down_revision = "697400571e57"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("customers", sa.Column("email", sa.String(length=255), nullable=True))


def downgrade():
    op.drop_column("customers", "email")
