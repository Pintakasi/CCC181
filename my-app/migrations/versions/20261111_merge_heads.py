"""Merge customer and service migration branches.

Revision ID: 20261111_merge_heads
Revises: 20261111_phone_length, ca832af49b2d
Create Date: 2026-11-11
"""

revision = "20261111_merge_heads"
down_revision = ("20261111_phone_length", "ca832af49b2d")
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
