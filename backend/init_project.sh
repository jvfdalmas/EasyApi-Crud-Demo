#!/bin/bash

# Complete project initialization script
# This script sets up the database, creates migrations, and prepares the project for deployment

set -e

echo "🚀 Initializing EasyAPI CRUD Demo Project..."
echo "============================================="

# Step 1: Setup database
echo ""
echo "📝 Step 1: Setting up PostgreSQL database..."
./setup_database.sh

# Step 2: Test database connection
echo ""
echo "🔍 Step 2: Testing database connection..."
python test_db_connection.py

# Step 3: Create initial migration
echo ""
echo "📦 Step 3: Creating initial migration..."
./run_alembic.sh revision --autogenerate -m "Initial migration"

# Step 4: Apply migration
echo ""
echo "⬆️  Step 4: Applying migration..."
./run_alembic.sh upgrade head

# Step 5: Verify everything is working
echo ""
echo "✅ Step 5: Final verification..."
python -c "
import asyncio
import sys
sys.path.insert(0, '.')

async def verify():
    from app.db import get_db
    from app.models import Item
    from sqlalchemy import select
    
    async for session in get_db():
        # Test creating an item
        item = Item(name='Test Item')
        session.add(item)
        await session.commit()
        await session.refresh(item)
        print(f'✅ Created test item with ID: {item.id}')
        
        # Test querying items
        result = await session.execute(select(Item))
        items = result.scalars().all()
        print(f'✅ Found {len(items)} items in database')
        
        # Clean up test item
        await session.delete(item)
        await session.commit()
        print('✅ Cleaned up test item')
        
        break

asyncio.run(verify())
print('✅ Database operations working correctly!')
"

echo ""
echo "🎉 Project initialization completed successfully!"
echo "============================================="
echo ""
echo "📋 Summary:"
echo "   ✅ Database created and configured"
echo "   ✅ Database connection tested"
echo "   ✅ Initial migration created and applied"
echo "   ✅ Database operations verified"
echo ""
echo "🚀 Next steps:"
echo "   1. Start the backend: gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 127.0.0.1:8000"
echo "   2. Build the frontend: cd ../frontend && npm run build"
echo "   3. Deploy with Nginx using the provided configuration"
echo ""
echo "🔧 Useful commands:"
echo "   - Test backend: curl http://localhost:8000/api/health"
echo "   - View logs: journalctl -u backend.service -f"
echo "   - Database migrations: ./run_alembic.sh [command]"
