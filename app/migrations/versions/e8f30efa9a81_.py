"""
Add last_modified_at column for games.

Revision ID: e8f30efa9a81
Revises: b7e6bb2a9bb3
Create Date: 2017-01-23 15:26:22.294104

"""
from alembic import context, op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'e8f30efa9a81'
down_revision = 'b7e6bb2a9bb3'
branch_labels = None
depends_on = None


def upgrade():
    """Upgrade database."""
    # The following is a ridiculous hack to force table recreation for SQLite to
    # enable the use of a default timestamp.
    recreate = 'auto'
    migrate_context = context.get_context()
    sqlite_dialect_class = None
    if getattr(sa.dialects, 'sqlite', False):
        sqlite_dialect_class = (sa.dialects.sqlite.pysqlite
                                .SQLiteDialect_pysqlite)
    if migrate_context.dialect.__class__ == sqlite_dialect_class:
        recreate = 'always'
    with op.batch_alter_table('games', recreate=recreate) as batch_op:
        batch_op.add_column(sa.Column('last_modified_at', sa.DateTime(),
                            nullable=False, server_default=sa.func.now()))


def downgrade():
    """Downgrade database."""
    with op.batch_alter_table('games') as batch_op:
        batch_op.drop_column('last_modified_at')
