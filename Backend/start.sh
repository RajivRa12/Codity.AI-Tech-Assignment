#!/bin/bash

# Color codes
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}  Distributed Job Scheduler - Quick Start${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo ""

# Check if venv exists
if [ ! -d ".venv" ]; then
    echo -e "${YELLOW}Virtual environment not found. Creating...${NC}"
    python3 -m venv .venv
fi

# Activate venv
source .venv/bin/activate

# Set SQLite environment
export USE_SQLITE=True

echo -e "${GREEN}✓${NC} Virtual environment activated"
echo ""

# Run migrations if needed
if [ ! -f "db.sqlite3" ]; then
    echo -e "${YELLOW}Setting up database...${NC}"
    python manage.py migrate --noinput
    echo -e "${GREEN}✓${NC} Database initialized"
else
    echo -e "${GREEN}✓${NC} Database already exists"
fi

echo ""
echo -e "${YELLOW}Creating admin user if doesn't exist...${NC}"
python manage.py shell << 'PYEOF'
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print("✓ Admin user created: admin / admin123")
else:
    print("✓ Admin user already exists")
PYEOF

echo ""
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}🚀 Server Starting...${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "${YELLOW}📍 Local URLs:${NC}"
echo -e "   API Documentation: ${GREEN}http://localhost:8000/api/docs/${NC}"
echo -e "   Admin Panel:       ${GREEN}http://localhost:8000/admin/${NC}"
echo -e "   API Base:          ${GREEN}http://localhost:8000/api/${NC}"
echo ""
echo -e "${YELLOW}🔐 Admin Credentials:${NC}"
echo -e "   Username: ${GREEN}admin${NC}"
echo -e "   Password: ${GREEN}admin123${NC}"
echo ""
echo -e "${YELLOW}📚 Documentation:${NC}"
echo -e "   See ${GREEN}GETTING_STARTED.md${NC} for usage examples and API endpoints"
echo ""
echo -e "${YELLOW}⚡ Press Ctrl+C to stop the server${NC}"
echo ""

# Start the development server
python manage.py runserver 0.0.0.0:8000
