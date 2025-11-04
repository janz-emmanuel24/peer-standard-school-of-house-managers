#!/bin/bash
# Deployment script for Peer Standard School Django Application

set -e

echo "=========================================="
echo "Peer Standard School - Docker Deployment"
echo "=========================================="

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found!"
    echo "📋 Creating .env from env.production.example..."
    if [ -f env.production.example ]; then
        cp env.production.example .env
        echo "✅ Created .env file. Please edit it with your production values!"
        echo "   Run: nano .env"
        exit 1
    else
        echo "❌ env.production.example not found. Please create .env manually."
        exit 1
    fi
fi

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Function to check if docker-compose or docker compose should be used
docker_compose() {
    if command -v docker-compose &> /dev/null; then
        docker-compose "$@"
    else
        docker compose "$@"
    fi
}

# Parse command line arguments
case "${1:-}" in
    build)
        echo "🔨 Building Docker images..."
        docker_compose build
        echo "✅ Build complete!"
        ;;
    up|start)
        echo "🚀 Starting services..."
        docker_compose up -d
        echo "✅ Services started!"
        echo ""
        echo "📊 View logs: docker-compose logs -f"
        echo "🌐 Application should be available at: http://localhost"
        ;;
    down|stop)
        echo "🛑 Stopping services..."
        docker_compose down
        echo "✅ Services stopped!"
        ;;
    restart)
        echo "🔄 Restarting services..."
        docker_compose restart
        echo "✅ Services restarted!"
        ;;
    logs)
        echo "📋 Showing logs..."
        docker_compose logs -f "${2:-}"
        ;;
    migrate)
        echo "🔄 Running migrations..."
        docker_compose exec web python manage.py migrate
        echo "✅ Migrations complete!"
        ;;
    createsuperuser)
        echo "👤 Creating superuser..."
        docker_compose exec web python manage.py createsuperuser
        ;;
    collectstatic)
        echo "📦 Collecting static files..."
        docker_compose exec web python manage.py collectstatic --noinput
        echo "✅ Static files collected!"
        ;;
    shell)
        echo "🐚 Opening Django shell..."
        docker_compose exec web python manage.py shell
        ;;
    backup)
        echo "💾 Creating database backup..."
        BACKUP_FILE="backup_$(date +%Y%m%d_%H%M%S).sql"
        docker_compose exec -T db pg_dump -U peer_school_user peer_school_db > "$BACKUP_FILE"
        echo "✅ Backup created: $BACKUP_FILE"
        ;;
    update)
        echo "🔄 Updating application..."
        echo "1️⃣  Pulling latest code..."
        git pull origin main || echo "⚠️  Git pull failed or not a git repository"
        echo "2️⃣  Rebuilding images..."
        docker_compose build
        echo "3️⃣  Restarting services..."
        docker_compose up -d
        echo "4️⃣  Running migrations..."
        docker_compose exec web python manage.py migrate
        echo "5️⃣  Collecting static files..."
        docker_compose exec web python manage.py collectstatic --noinput
        echo "✅ Update complete!"
        ;;
    status)
        echo "📊 Service status:"
        docker_compose ps
        ;;
    *)
        echo "Usage: $0 {build|up|start|down|stop|restart|logs|migrate|createsuperuser|collectstatic|shell|backup|update|status}"
        echo ""
        echo "Commands:"
        echo "  build            - Build Docker images"
        echo "  up, start        - Start all services"
        echo "  down, stop       - Stop all services"
        echo "  restart          - Restart all services"
        echo "  logs [service]   - Show logs (optionally for specific service)"
        echo "  migrate          - Run database migrations"
        echo "  createsuperuser  - Create Django superuser"
        echo "  collectstatic    - Collect static files"
        echo "  shell            - Open Django shell"
        echo "  backup           - Backup database"
        echo "  update           - Update application (git pull + rebuild + restart)"
        echo "  status           - Show service status"
        echo ""
        echo "Examples:"
        echo "  $0 build            # Build images"
        echo "  $0 up               # Start services"
        echo "  $0 logs web         # Show web service logs"
        echo "  $0 update           # Full update process"
        exit 1
        ;;
esac

