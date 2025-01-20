from .create_users_table import upgrade as create_users_table
from .create_api_configurations_table import upgrade as create_api_configurations_table
from .create_vendor_configurations_tables import (
    upgrade as create_vendor_configurations_tables,
)
from .create_budget_plans_table import upgrade as create_budget_plans_table

# List of migrations in order of execution
MIGRATIONS = [
    create_users_table,  # Must run first as api_configurations depends on it
    create_api_configurations_table,  # Runs after users table exists
    create_vendor_configurations_tables,
    create_budget_plans_table,  # New migration
]
