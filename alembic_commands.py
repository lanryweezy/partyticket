import os
import sys
from alembic.config import Config as AlembicConfig
from alembic import command

# Add the current directory to the path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app import create_app, db

app = create_app()

# Create Alembic configuration
alembic_cfg = AlembicConfig("alembic.ini")
alembic_cfg.set_main_option("script_location", "migrations")

with app.app_context():
    # Generate a new migration (equivalent to 'flask db migrate')
    print("Generating new migration...")
    command.revision(alembic_cfg, message="Add relationships to models", autogenerate=True)

    # Apply migrations (equivalent to 'flask db upgrade')
    print("Applying migrations...")
    command.upgrade(alembic_cfg, "head")

print("Database migration process completed.")
