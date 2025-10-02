#!/usr/bin/env python3
"""
Test script to verify database connection and configuration.
Run this after setting up the database to ensure everything is working.
"""

import asyncio
import os
import sys
from pathlib import Path

# Add the app directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

async def test_connection():
    """Test database connection and basic operations."""
    try:
        print("🔍 Testing database connection...")
        
        # Import after adding to path
        from app.db import engine, Base, get_db
        from app.models import Item
        
        # Test engine connection
        async with engine.begin() as conn:
            print("✅ Database engine connection successful!")
            
            # Create tables
            await conn.run_sync(Base.metadata.create_all)
            print("✅ Database tables created successfully!")
        
        # Test session
        async for session in get_db():
            print("✅ Database session created successfully!")
            
            # Test basic query
            from sqlalchemy import text
            result = await session.execute(text("SELECT version()"))
            version = result.scalar()
            print(f"✅ PostgreSQL version: {version}")
            
            break  # Exit after first iteration
        
        print("\n🎉 All database tests passed!")
        print("✅ Your database is ready for Alembic migrations!")
        
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        print("\n🔧 Troubleshooting:")
        print("1. Make sure PostgreSQL is running: sudo systemctl status postgresql")
        print("2. Check your .env file has the correct DATABASE_URL")
        print("3. Verify database user has proper permissions")
        print("4. Run the setup_database.sh script if you haven't already")
        sys.exit(1)

if __name__ == "__main__":
    # Load environment variables from .env file
    env_file = Path(__file__).parent / ".env"
    if env_file.exists():
        print(f"📄 Loading environment from: {env_file}")
        with open(env_file) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key] = value
    else:
        print("⚠️  No .env file found. Make sure to set DATABASE_URL environment variable.")
    
    # Show current DATABASE_URL (masked for security)
    db_url = os.getenv("DATABASE_URL", "Not set")
    if db_url != "Not set":
        # Mask password in URL for display
        import re
        masked_url = re.sub(r'://([^:]+):([^@]+)@', r'://\1:***@', db_url)
        print(f"🔗 Using DATABASE_URL: {masked_url}")
    else:
        print("❌ DATABASE_URL not set!")
        sys.exit(1)
    
    # Run the test
    asyncio.run(test_connection())
