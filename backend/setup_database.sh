#!/bin/bash

# Database Setup Script for EasyAPI CRUD Demo
# This script sets up PostgreSQL database with proper permissions

set -e

# Configuration - Update these values
DB_NAME="easyapi_crud"
DB_USER="easyapi_user"
DB_PASSWORD="your_secure_password"
SCHEMA_NAME="easyapi"

echo "🚀 Setting up PostgreSQL database for EasyAPI CRUD Demo..."

# Check if PostgreSQL is running
if ! systemctl is-active --quiet postgresql; then
    echo "❌ PostgreSQL is not running. Please start it first:"
    echo "   sudo systemctl start postgresql"
    exit 1
fi

echo "📝 Creating database and user..."

# Create database and user as postgres superuser
sudo -u postgres psql << EOF
-- Create user if not exists
DO \$\$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = '$DB_USER') THEN
        CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';
    END IF;
END
\$\$;

-- Create database if not exists
SELECT 'CREATE DATABASE $DB_NAME OWNER $DB_USER'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = '$DB_NAME')\gexec

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;
EOF

echo "🔧 Setting up schema and permissions..."

# Connect to the new database and set up schema
sudo -u postgres psql $DB_NAME << EOF
-- Create schema
CREATE SCHEMA IF NOT EXISTS $SCHEMA_NAME;

-- Grant all privileges on schema
GRANT ALL PRIVILEGES ON SCHEMA $SCHEMA_NAME TO $DB_USER;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA $SCHEMA_NAME TO $DB_USER;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA $SCHEMA_NAME TO $DB_USER;

-- Set default privileges for future objects
ALTER DEFAULT PRIVILEGES IN SCHEMA $SCHEMA_NAME GRANT ALL ON TABLES TO $DB_USER;
ALTER DEFAULT PRIVILEGES IN SCHEMA $SCHEMA_NAME GRANT ALL ON SEQUENCES TO $DB_USER;

-- Set search path for user
ALTER USER $DB_USER SET search_path TO $SCHEMA_NAME, public;

-- Also grant permissions on public schema (fallback)
GRANT CREATE ON SCHEMA public TO $DB_USER;
GRANT USAGE ON SCHEMA public TO $DB_USER;
EOF

echo "✅ Database setup completed!"
echo ""
echo "📋 Database Configuration:"
echo "   Database: $DB_NAME"
echo "   User: $DB_USER"
echo "   Schema: $SCHEMA_NAME"
echo ""
echo "🔗 Update your DATABASE_URL to:"
echo "   postgresql+asyncpg://$DB_USER:$DB_PASSWORD@localhost/$DB_NAME"
echo ""
echo "🚀 Next steps:"
echo "   1. Update your .env file with the DATABASE_URL above"
echo "   2. Run: alembic revision --autogenerate -m 'Initial migration'"
echo "   3. Run: alembic upgrade head"
