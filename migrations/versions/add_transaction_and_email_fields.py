"""Add Transaction model and email verification fields

Revision ID: add_transaction_email
Revises: 61492d684142
Create Date: 2025-12-04

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'add_transaction_email'
down_revision: Union[str, None] = '61492d684142'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add email verification fields to user table
    op.add_column('user', sa.Column('email_verified', sa.Boolean(), nullable=True, server_default='false'))
    op.add_column('user', sa.Column('email_verification_token', sa.String(length=100), nullable=True))
    op.add_column('user', sa.Column('password_reset_token', sa.String(length=100), nullable=True))
    op.add_column('user', sa.Column('password_reset_expires', sa.DateTime(), nullable=True))
    
    # Update ticket table with used_at field if it doesn't exist
    try:
        op.add_column('ticket', sa.Column('used_at', sa.DateTime(), nullable=True))
    except:
        pass  # Column might already exist
    
    # Create transaction table
    op.create_table('transaction',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('event_id', sa.Integer(), nullable=True),
        sa.Column('invitation_id', sa.Integer(), nullable=True),
        sa.Column('provider', sa.String(length=50), nullable=False),
        sa.Column('reference', sa.String(length=255), nullable=False),
        sa.Column('currency', sa.String(length=10), nullable=True, server_default='NGN'),
        sa.Column('amount', sa.Float(), nullable=False),
        sa.Column('platform_fee', sa.Float(), nullable=True, server_default='0.0'),
        sa.Column('organizer_amount', sa.Float(), nullable=True, server_default='0.0'),
        sa.Column('status', sa.String(length=50), nullable=True, server_default='initialized'),
        sa.Column('raw_response', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
        sa.ForeignKeyConstraint(['event_id'], ['event.id'], ),
        sa.ForeignKeyConstraint(['invitation_id'], ['invitation.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('reference')
    )
    op.create_index(op.f('ix_transaction_reference'), 'transaction', ['reference'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_transaction_reference'), table_name='transaction')
    op.drop_table('transaction')
    op.drop_column('ticket', 'used_at')
    op.drop_column('user', 'password_reset_expires')
    op.drop_column('user', 'password_reset_token')
    op.drop_column('user', 'email_verification_token')
    op.drop_column('user', 'email_verified')

