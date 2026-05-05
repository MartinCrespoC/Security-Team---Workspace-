#!/bin/bash

#═══════════════════════════════════════════════════════════════════════════════
#  🟠 ORANGE TEAM - Security Awareness Platform
#  Instalador Automatizado v2.0
#═══════════════════════════════════════════════════════════════════════════════

set -e

# Colores
ORANGE='\033[0;33m'
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
NC='\033[0m'

# Banner
print_banner() {
    echo -e "${ORANGE}"
    cat << "EOF"
    
 ██████╗ ██████╗  █████╗ ███╗   ██╗ ██████╗ ███████╗    ████████╗███████╗ █████╗ ███╗   ███╗
██╔═══██╗██╔══██╗██╔══██╗████╗  ██║██╔════╝ ██╔════╝    ╚══██╔══╝██╔════╝██╔══██╗████╗ ████║
██║   ██║██████╔╝███████║██╔██╗ ██║██║  ███╗█████╗         ██║   █████╗  ███████║██╔████╔██║
██║   ██║██╔══██╗██╔══██║██║╚██╗██║██║   ██║██╔══╝         ██║   ██╔══╝  ██╔══██║██║╚██╔╝██║
╚██████╔╝██║  ██║██║  ██║██║ ╚████║╚██████╔╝███████╗       ██║   ███████╗██║  ██║██║ ╚═╝ ██║
 ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚══════╝       ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝
                                                                                            
    ███████╗███████╗ ██████╗██╗   ██╗██████╗ ██╗████████╗██╗   ██╗                          
    ██╔════╝██╔════╝██╔════╝██║   ██║██╔══██╗██║╚══██╔══╝╚██╗ ██╔╝                          
    ███████╗█████╗  ██║     ██║   ██║██████╔╝██║   ██║    ╚████╔╝                           
    ╚════██║██╔══╝  ██║     ██║   ██║██╔══██╗██║   ██║     ╚██╔╝                            
    ███████║███████╗╚██████╗╚██████╔╝██║  ██║██║   ██║      ██║                             
    ╚══════╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝   ╚═╝      ╚═╝                             
                                                                                            
     █████╗ ██╗    ██╗ █████╗ ██████╗ ███████╗███╗   ██╗███████╗███████╗███████╗            
    ██╔══██╗██║    ██║██╔══██╗██╔══██╗██╔════╝████╗  ██║██╔════╝██╔════╝██╔════╝            
    ███████║██║ █╗ ██║███████║██████╔╝█████╗  ██╔██╗ ██║█████╗  ███████╗███████╗            
    ██╔══██║██║███╗██║██╔══██║██╔══██╗██╔══╝  ██║╚██╗██║██╔══╝  ╚════██║╚════██║            
    ██║  ██║╚███╔███╔╝██║  ██║██║  ██║███████╗██║ ╚████║███████╗███████║███████║            
    ╚═╝  ╚═╝ ╚══╝╚══╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═══╝╚══════╝╚══════╝╚══════╝            

                    🛡️ Security Awareness Platform Installer 🛡️
                              Powered by Windsurf AI
EOF
    echo -e "${NC}"
}

# Funciones de logging
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[✓]${NC} $1"
}

log_warning() {
    echo -e "${ORANGE}[!]${NC} $1"
}

log_error() {
    echo -e "${RED}[✗]${NC} $1"
}

log_step() {
    echo -e "\n${PURPLE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${WHITE}  $1${NC}"
    echo -e "${PURPLE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}\n"
}

# Verificar si se ejecuta como root
check_root() {
    if [[ $EUID -eq 0 ]]; then
        log_warning "Se recomienda NO ejecutar como root. Continuando de todos modos..."
    fi
}

# Detectar sistema operativo
detect_os() {
    if [[ -f /etc/os-release ]]; then
        . /etc/os-release
        OS=$ID
        VERSION=$VERSION_ID
    elif [[ -f /etc/debian_version ]]; then
        OS="debian"
    elif [[ -f /etc/redhat-release ]]; then
        OS="rhel"
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        OS="macos"
    else
        OS="unknown"
    fi
    log_info "Sistema operativo detectado: $OS"
}

# Verificar dependencias del sistema
check_dependencies() {
    log_step "🔍 Verificando Dependencias del Sistema"
    
    local deps=("git" "curl" "wget" "python3" "pip3" "docker" "docker-compose")
    local missing=()
    
    for dep in "${deps[@]}"; do
        if command -v "$dep" &> /dev/null; then
            log_success "$dep instalado"
        else
            log_warning "$dep no encontrado"
            missing+=("$dep")
        fi
    done
    
    if [[ ${#missing[@]} -gt 0 ]]; then
        log_warning "Dependencias faltantes: ${missing[*]}"
        read -p "¿Desea instalar las dependencias faltantes? (y/n): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            install_dependencies "${missing[@]}"
        else
            log_error "Instalación cancelada. Por favor instale las dependencias manualmente."
            exit 1
        fi
    fi
}

# Instalar dependencias faltantes
install_dependencies() {
    local deps=("$@")
    
    case $OS in
        ubuntu|debian|kali)
            sudo apt-get update
            for dep in "${deps[@]}"; do
                case $dep in
                    pip3)
                        sudo apt-get install -y python3-pip
                        ;;
                    docker)
                        curl -fsSL https://get.docker.com | sh
                        sudo usermod -aG docker $USER
                        ;;
                    docker-compose)
                        sudo apt-get install -y docker-compose
                        ;;
                    *)
                        sudo apt-get install -y "$dep"
                        ;;
                esac
            done
            ;;
        fedora|rhel|centos)
            for dep in "${deps[@]}"; do
                case $dep in
                    pip3)
                        sudo dnf install -y python3-pip
                        ;;
                    docker)
                        sudo dnf install -y docker
                        sudo systemctl start docker
                        sudo systemctl enable docker
                        ;;
                    *)
                        sudo dnf install -y "$dep"
                        ;;
                esac
            done
            ;;
        arch)
            for dep in "${deps[@]}"; do
                sudo pacman -S --noconfirm "$dep"
            done
            ;;
        macos)
            if ! command -v brew &> /dev/null; then
                /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
            fi
            for dep in "${deps[@]}"; do
                brew install "$dep"
            done
            ;;
    esac
}

# Crear estructura de directorios
create_directory_structure() {
    log_step "📁 Creando Estructura de Directorios"
    
    local dirs=(
        "campaigns/active"
        "campaigns/completed"
        "campaigns/scheduled"
        "training/modules"
        "training/videos"
        "training/slides"
        "training/interactive"
        "metrics/dashboard"
        "metrics/reports"
        "metrics/data"
        "templates/email/credential"
        "templates/email/malware"
        "templates/email/bec"
        "templates/email/awareness"
        "templates/landing"
        "templates/sms"
        "templates/qr"
        "quizzes/questions"
        "quizzes/assessments"
        "tools/custom-scripts"
        "tools/integrations"
        "docker/gophish"
        "docker/kingphisher"
        "docker/beef"
        "docker/elk"
        ".windsurf/workflows"
        ".windsurf/skills"
        "docs"
        "logs"
        "backups"
    )
    
    for dir in "${dirs[@]}"; do
        mkdir -p "$dir"
        log_success "Creado: $dir"
    done
}

# Crear entorno virtual de Python
setup_python_env() {
    log_step "🐍 Configurando Entorno Python"
    
    if [[ ! -d "venv" ]]; then
        python3 -m venv venv
        log_success "Entorno virtual creado"
    fi
    
    source venv/bin/activate
    
    pip install --upgrade pip
    pip install -r requirements.txt
    
    log_success "Dependencias Python instaladas"
}

# Instalar herramientas de phishing
install_phishing_tools() {
    log_step "🎣 Instalando Herramientas de Phishing"
    
    # GoPhish
    log_info "Instalando GoPhish..."
    if [[ ! -d "tools/gophish" ]]; then
        mkdir -p tools/gophish
        cd tools/gophish
        
        GOPHISH_VERSION="0.12.1"
        ARCH=$(uname -m)
        
        case $ARCH in
            x86_64)
                GOPHISH_ARCH="linux-64bit"
                ;;
            aarch64)
                GOPHISH_ARCH="linux-arm64"
                ;;
            *)
                GOPHISH_ARCH="linux-64bit"
                ;;
        esac
        
        wget -q "https://github.com/gophish/gophish/releases/download/v${GOPHISH_VERSION}/gophish-v${GOPHISH_VERSION}-${GOPHISH_ARCH}.zip" -O gophish.zip
        unzip -q gophish.zip
        rm gophish.zip
        chmod +x gophish
        
        cd ../..
        log_success "GoPhish instalado"
    else
        log_info "GoPhish ya está instalado"
    fi
    
    # King Phisher (via Docker)
    log_info "Configurando King Phisher (Docker)..."
    cat > docker/kingphisher/docker-compose.yml << 'KINGPHISHER_DOCKER'
version: '3.8'
services:
  kingphisher:
    image: securecodebox/king-phisher
    container_name: orange_kingphisher
    ports:
      - "8443:443"
      - "8080:80"
    volumes:
      - ./data:/var/lib/king-phisher
      - ./config:/etc/king-phisher
    environment:
      - KP_SERVER_ADDRESS=0.0.0.0
    restart: unless-stopped
    networks:
      - orange_network

networks:
  orange_network:
    driver: bridge
KINGPHISHER_DOCKER
    log_success "King Phisher configurado"
    
    # Evilginx2
    log_info "Instalando Evilginx2..."
    if [[ ! -d "tools/evilginx2" ]]; then
        git clone https://github.com/kgretzky/evilginx2.git tools/evilginx2 2>/dev/null || true
        log_success "Evilginx2 clonado"
    else
        log_info "Evilginx2 ya está instalado"
    fi
}

# Instalar herramientas de Social Engineering
install_social_engineering_tools() {
    log_step "🎭 Instalando Herramientas de Social Engineering"
    
    # Social Engineering Toolkit (SET)
    log_info "Instalando SET..."
    if [[ ! -d "tools/set" ]]; then
        git clone https://github.com/trustedsec/social-engineer-toolkit.git tools/set 2>/dev/null || true
        if [[ -d "tools/set" ]]; then
            cd tools/set
            pip3 install -r requirements.txt 2>/dev/null || true
            cd ../..
        fi
        log_success "SET instalado"
    else
        log_info "SET ya está instalado"
    fi
    
    # BeEF (Browser Exploitation Framework)
    log_info "Configurando BeEF (Docker)..."
    cat > docker/beef/docker-compose.yml << 'BEEF_DOCKER'
version: '3.8'
services:
  beef:
    image: beefproject/beef
    container_name: orange_beef
    ports:
      - "3000:3000"
      - "6789:6789"
      - "61985:61985"
      - "61986:61986"
    volumes:
      - ./config:/beef/config
    restart: unless-stopped
    networks:
      - orange_network

networks:
  orange_network:
    external: true
BEEF_DOCKER
    log_success "BeEF configurado"
}

# Configurar GoPhish Docker
setup_gophish_docker() {
    log_step "🐳 Configurando GoPhish Docker"
    
    cat > docker/gophish/docker-compose.yml << 'GOPHISH_DOCKER'
version: '3.8'
services:
  gophish:
    image: gophish/gophish:latest
    container_name: orange_gophish
    ports:
      - "3333:3333"
      - "8888:80"
    volumes:
      - ./data:/opt/gophish/data
      - ./config.json:/opt/gophish/config.json
    restart: unless-stopped
    networks:
      - orange_network

networks:
  orange_network:
    driver: bridge
GOPHISH_DOCKER

    cat > docker/gophish/config.json << 'GOPHISH_CONFIG'
{
    "admin_server": {
        "listen_url": "0.0.0.0:3333",
        "use_tls": true,
        "cert_path": "gophish_admin.crt",
        "key_path": "gophish_admin.key"
    },
    "phish_server": {
        "listen_url": "0.0.0.0:80",
        "use_tls": false,
        "cert_path": "example.crt",
        "key_path": "example.key"
    },
    "db_name": "sqlite3",
    "db_path": "gophish.db",
    "migrations_prefix": "db/db_",
    "contact_address": "",
    "logging": {
        "filename": "",
        "level": ""
    }
}
GOPHISH_CONFIG
    
    log_success "GoPhish Docker configurado"
}

# Configurar ELK Stack para métricas
setup_elk_stack() {
    log_step "📊 Configurando ELK Stack para Métricas"
    
    cat > docker/elk/docker-compose.yml << 'ELK_DOCKER'
version: '3.8'
services:
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.11.0
    container_name: orange_elasticsearch
    environment:
      - discovery.type=single-node
      - xpack.security.enabled=false
      - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
    ports:
      - "9200:9200"
    volumes:
      - elasticsearch_data:/usr/share/elasticsearch/data
    networks:
      - orange_network

  kibana:
    image: docker.elastic.co/kibana/kibana:8.11.0
    container_name: orange_kibana
    ports:
      - "5601:5601"
    environment:
      - ELASTICSEARCH_HOSTS=http://elasticsearch:9200
    depends_on:
      - elasticsearch
    networks:
      - orange_network

  grafana:
    image: grafana/grafana:latest
    container_name: orange_grafana
    ports:
      - "3001:3000"
    volumes:
      - grafana_data:/var/lib/grafana
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=orangeteam
    networks:
      - orange_network

volumes:
  elasticsearch_data:
  grafana_data:

networks:
  orange_network:
    external: true
ELK_DOCKER
    
    log_success "ELK Stack configurado"
}

# Crear archivo de requirements
create_requirements() {
    log_step "📦 Creando Requirements"
    
    cat > requirements.txt << 'REQUIREMENTS'
# Orange Team - Security Awareness Platform
# Python Dependencies

# Core
flask>=2.3.0
fastapi>=0.104.0
uvicorn>=0.24.0
pydantic>=2.5.0
python-dotenv>=1.0.0

# Database
sqlalchemy>=2.0.0
psycopg2-binary>=2.9.0
redis>=5.0.0
elasticsearch>=8.11.0

# HTTP & API
requests>=2.31.0
httpx>=0.25.0
aiohttp>=3.9.0
beautifulsoup4>=4.12.0

# Email
python-emails>=0.6
aiosmtplib>=3.0.0

# Security
cryptography>=41.0.0
pyjwt>=2.8.0
passlib>=1.7.0
bcrypt>=4.1.0

# Data Processing
pandas>=2.1.0
numpy>=1.26.0
jinja2>=3.1.0
pyyaml>=6.0.0

# Reporting
reportlab>=4.0.0
matplotlib>=3.8.0
plotly>=5.18.0

# CLI
click>=8.1.0
rich>=13.7.0
typer>=0.9.0

# Testing
pytest>=7.4.0
pytest-asyncio>=0.21.0
pytest-cov>=4.1.0

# Utilities
python-dateutil>=2.8.0
pytz>=2023.3
tqdm>=4.66.0
colorama>=0.4.6

# GoPhish API
gophish>=0.5.0

# Logging
loguru>=0.7.0
structlog>=23.2.0

# Task Queue
celery>=5.3.0
flower>=2.0.0

# Metrics
prometheus-client>=0.19.0
statsd>=4.0.0
REQUIREMENTS
    
    log_success "requirements.txt creado"
}

# Crear docker-compose principal
create_main_docker_compose() {
    log_step "🐳 Creando Docker Compose Principal"
    
    cat > docker-compose.yml << 'MAIN_DOCKER'
version: '3.8'

services:
  # PostgreSQL Database
  postgres:
    image: postgres:16-alpine
    container_name: orange_postgres
    environment:
      POSTGRES_DB: orangeteam
      POSTGRES_USER: orange
      POSTGRES_PASSWORD: ${DB_PASSWORD:-orangeteam_secure_2024}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    networks:
      - orange_network
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U orange -d orangeteam"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Redis Cache
  redis:
    image: redis:7-alpine
    container_name: orange_redis
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    networks:
      - orange_network
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

  # GoPhish
  gophish:
    image: gophish/gophish:latest
    container_name: orange_gophish
    ports:
      - "3333:3333"
      - "8888:80"
    volumes:
      - gophish_data:/opt/gophish/data
    networks:
      - orange_network
    restart: unless-stopped

  # Metrics Dashboard
  dashboard:
    build:
      context: ./metrics/dashboard
      dockerfile: Dockerfile
    container_name: orange_dashboard
    ports:
      - "8080:8080"
    environment:
      - DATABASE_URL=postgresql://orange:${DB_PASSWORD:-orangeteam_secure_2024}@postgres:5432/orangeteam
      - REDIS_URL=redis://redis:6379
    depends_on:
      - postgres
      - redis
    networks:
      - orange_network
    restart: unless-stopped

  # API Server
  api:
    build:
      context: .
      dockerfile: Dockerfile.api
    container_name: orange_api
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://orange:${DB_PASSWORD:-orangeteam_secure_2024}@postgres:5432/orangeteam
      - REDIS_URL=redis://redis:6379
      - GOPHISH_URL=https://gophish:3333
    depends_on:
      - postgres
      - redis
      - gophish
    networks:
      - orange_network
    restart: unless-stopped

  # Celery Worker
  celery:
    build:
      context: .
      dockerfile: Dockerfile.api
    container_name: orange_celery
    command: celery -A app.celery worker --loglevel=info
    environment:
      - DATABASE_URL=postgresql://orange:${DB_PASSWORD:-orangeteam_secure_2024}@postgres:5432/orangeteam
      - REDIS_URL=redis://redis:6379
    depends_on:
      - postgres
      - redis
    networks:
      - orange_network
    restart: unless-stopped

volumes:
  postgres_data:
  redis_data:
  gophish_data:

networks:
  orange_network:
    driver: bridge
MAIN_DOCKER
    
    log_success "docker-compose.yml creado"
}

# Crear archivos de configuración
create_config_files() {
    log_step "⚙️ Creando Archivos de Configuración"
    
    # .env
    cat > .env << 'ENV_FILE'
# Orange Team Environment Configuration

# Database
DB_PASSWORD=orangeteam_secure_2024
DATABASE_URL=postgresql://orange:orangeteam_secure_2024@localhost:5432/orangeteam

# Redis
REDIS_URL=redis://localhost:6379

# GoPhish
GOPHISH_URL=https://localhost:3333
GOPHISH_API_KEY=your_api_key_here

# SMTP
SMTP_HOST=localhost
SMTP_PORT=25
SMTP_USER=
SMTP_PASSWORD=

# Security
SECRET_KEY=your_secret_key_here_change_in_production
JWT_SECRET=your_jwt_secret_here

# Logging
LOG_LEVEL=INFO

# Features
ENABLE_GAMIFICATION=true
ENABLE_AUTO_TRAINING=true
ENABLE_PURPLE_TEAM_INTEGRATION=true
ENV_FILE
    
    # .gitignore
    cat > .gitignore << 'GITIGNORE'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
ENV/
.venv/

# IDE
.idea/
.vscode/
*.swp
*.swo

# Environment
.env
.env.local
*.env

# Logs
logs/
*.log

# Data
*.db
*.sqlite
data/

# Docker
docker/*/data/

# Secrets
*.pem
*.key
*.crt
secrets/

# OS
.DS_Store
Thumbs.db

# Backups
backups/
*.bak

# Reports (sensitive)
metrics/reports/*.pdf
campaigns/*/results.json
GITIGNORE
    
    log_success "Archivos de configuración creados"
}

# Crear dashboard de métricas básico
create_metrics_dashboard() {
    log_step "📊 Creando Dashboard de Métricas"
    
    cat > metrics/dashboard/index.html << 'DASHBOARD_HTML'
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🟠 Orange Team - Metrics Dashboard</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        :root {
            --orange-primary: #FF6B00;
            --orange-secondary: #FF8C00;
            --orange-light: #FFA500;
        }
        .bg-orange-primary { background-color: var(--orange-primary); }
        .text-orange-primary { color: var(--orange-primary); }
        .border-orange-primary { border-color: var(--orange-primary); }
    </style>
</head>
<body class="bg-gray-900 text-white min-h-screen">
    <!-- Header -->
    <header class="bg-orange-primary p-4 shadow-lg">
        <div class="container mx-auto flex justify-between items-center">
            <h1 class="text-2xl font-bold">🟠 Orange Team - Security Awareness</h1>
            <nav>
                <a href="#overview" class="mx-2 hover:underline">Overview</a>
                <a href="#campaigns" class="mx-2 hover:underline">Campaigns</a>
                <a href="#training" class="mx-2 hover:underline">Training</a>
                <a href="#leaderboard" class="mx-2 hover:underline">Leaderboard</a>
            </nav>
        </div>
    </header>

    <!-- Main Content -->
    <main class="container mx-auto p-6">
        <!-- KPI Cards -->
        <section id="overview" class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
            <div class="bg-gray-800 rounded-lg p-6 border-l-4 border-green-500">
                <h3 class="text-gray-400 text-sm">Click Rate</h3>
                <p class="text-3xl font-bold text-green-500">12.5%</p>
                <p class="text-sm text-gray-500">↓ 3.2% vs last month</p>
            </div>
            <div class="bg-gray-800 rounded-lg p-6 border-l-4 border-blue-500">
                <h3 class="text-gray-400 text-sm">Report Rate</h3>
                <p class="text-3xl font-bold text-blue-500">67.3%</p>
                <p class="text-sm text-gray-500">↑ 8.1% vs last month</p>
            </div>
            <div class="bg-gray-800 rounded-lg p-6 border-l-4 border-purple-500">
                <h3 class="text-gray-400 text-sm">Training Completion</h3>
                <p class="text-3xl font-bold text-purple-500">89.2%</p>
                <p class="text-sm text-gray-500">↑ 2.4% vs last month</p>
            </div>
            <div class="bg-gray-800 rounded-lg p-6 border-l-4 border-orange-500">
                <h3 class="text-gray-400 text-sm">Security Score</h3>
                <p class="text-3xl font-bold text-orange-500">78/100</p>
                <p class="text-sm text-gray-500">↑ 5 points vs last month</p>
            </div>
        </section>

        <!-- Charts -->
        <section class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
            <div class="bg-gray-800 rounded-lg p-6">
                <h3 class="text-xl font-bold mb-4">📈 Click Rate Trend</h3>
                <canvas id="clickRateChart"></canvas>
            </div>
            <div class="bg-gray-800 rounded-lg p-6">
                <h3 class="text-xl font-bold mb-4">📊 Department Performance</h3>
                <canvas id="departmentChart"></canvas>
            </div>
        </section>

        <!-- Active Campaigns -->
        <section id="campaigns" class="bg-gray-800 rounded-lg p-6 mb-8">
            <h3 class="text-xl font-bold mb-4">🎣 Active Campaigns</h3>
            <table class="w-full">
                <thead>
                    <tr class="text-left text-gray-400 border-b border-gray-700">
                        <th class="pb-2">Campaign</th>
                        <th class="pb-2">Status</th>
                        <th class="pb-2">Sent</th>
                        <th class="pb-2">Opened</th>
                        <th class="pb-2">Clicked</th>
                        <th class="pb-2">Reported</th>
                    </tr>
                </thead>
                <tbody>
                    <tr class="border-b border-gray-700">
                        <td class="py-3">Q1 Credential Phishing</td>
                        <td><span class="bg-green-500 px-2 py-1 rounded text-xs">Active</span></td>
                        <td>1,250</td>
                        <td>892 (71%)</td>
                        <td>156 (12%)</td>
                        <td>423 (34%)</td>
                    </tr>
                    <tr class="border-b border-gray-700">
                        <td class="py-3">Executive Whaling Test</td>
                        <td><span class="bg-yellow-500 px-2 py-1 rounded text-xs">Scheduled</span></td>
                        <td>50</td>
                        <td>-</td>
                        <td>-</td>
                        <td>-</td>
                    </tr>
                </tbody>
            </table>
        </section>

        <!-- Leaderboard -->
        <section id="leaderboard" class="bg-gray-800 rounded-lg p-6">
            <h3 class="text-xl font-bold mb-4">🏆 Security Champions</h3>
            <div class="space-y-3">
                <div class="flex items-center justify-between bg-gray-700 p-3 rounded">
                    <div class="flex items-center">
                        <span class="text-2xl mr-3">🥇</span>
                        <span>Alice Johnson</span>
                    </div>
                    <div class="flex items-center">
                        <span class="mr-4">4,250 pts</span>
                        <span>🛡️🔍🎓🏅</span>
                    </div>
                </div>
                <div class="flex items-center justify-between bg-gray-700 p-3 rounded">
                    <div class="flex items-center">
                        <span class="text-2xl mr-3">🥈</span>
                        <span>Bob Smith</span>
                    </div>
                    <div class="flex items-center">
                        <span class="mr-4">3,890 pts</span>
                        <span>🛡️🔍🎓</span>
                    </div>
                </div>
                <div class="flex items-center justify-between bg-gray-700 p-3 rounded">
                    <div class="flex items-center">
                        <span class="text-2xl mr-3">🥉</span>
                        <span>Carol Williams</span>
                    </div>
                    <div class="flex items-center">
                        <span class="mr-4">3,650 pts</span>
                        <span>🛡️🔍⚡</span>
                    </div>
                </div>
            </div>
        </section>
    </main>

    <!-- Footer -->
    <footer class="bg-gray-800 p-4 mt-8">
        <div class="container mx-auto text-center text-gray-400">
            <p>🟠 Orange Team - Security Awareness Platform | Powered by Windsurf AI</p>
        </div>
    </footer>

    <script>
        // Click Rate Chart
        const clickCtx = document.getElementById('clickRateChart').getContext('2d');
        new Chart(clickCtx, {
            type: 'line',
            data: {
                labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
                datasets: [{
                    label: 'Click Rate %',
                    data: [22, 19, 17, 16, 15, 14, 13, 12, 11, 12, 12, 12.5],
                    borderColor: '#FF6B00',
                    backgroundColor: 'rgba(255, 107, 0, 0.1)',
                    fill: true,
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { labels: { color: 'white' } }
                },
                scales: {
                    y: { ticks: { color: 'white' }, grid: { color: 'rgba(255,255,255,0.1)' } },
                    x: { ticks: { color: 'white' }, grid: { color: 'rgba(255,255,255,0.1)' } }
                }
            }
        });

        // Department Chart
        const deptCtx = document.getElementById('departmentChart').getContext('2d');
        new Chart(deptCtx, {
            type: 'bar',
            data: {
                labels: ['Sales', 'Marketing', 'Finance', 'Engineering', 'IT', 'Security'],
                datasets: [{
                    label: 'Click Rate %',
                    data: [18.2, 14.1, 11.3, 7.2, 4.1, 1.2],
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.8)',
                        'rgba(255, 159, 64, 0.8)',
                        'rgba(255, 205, 86, 0.8)',
                        'rgba(75, 192, 192, 0.8)',
                        'rgba(54, 162, 235, 0.8)',
                        'rgba(153, 102, 255, 0.8)'
                    ]
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { labels: { color: 'white' } }
                },
                scales: {
                    y: { ticks: { color: 'white' }, grid: { color: 'rgba(255,255,255,0.1)' } },
                    x: { ticks: { color: 'white' }, grid: { color: 'rgba(255,255,255,0.1)' } }
                }
            }
        });
    </script>
</body>
</html>
DASHBOARD_HTML
    
    log_success "Dashboard de métricas creado"
}

# Iniciar servicios Docker
start_docker_services() {
    log_step "🚀 Iniciando Servicios Docker"
    
    # Crear red si no existe
    docker network create orange_network 2>/dev/null || true
    
    read -p "¿Desea iniciar los servicios Docker ahora? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        docker-compose up -d
        log_success "Servicios Docker iniciados"
        
        echo -e "\n${CYAN}Servicios disponibles:${NC}"
        echo -e "  • GoPhish Admin:    ${GREEN}https://localhost:3333${NC}"
        echo -e "  • GoPhish Phishing: ${GREEN}http://localhost:8888${NC}"
        echo -e "  • Dashboard:        ${GREEN}http://localhost:8080${NC}"
        echo -e "  • API:              ${GREEN}http://localhost:8000${NC}"
    else
        log_info "Puede iniciar los servicios más tarde con: docker-compose up -d"
    fi
}

# Mostrar resumen final
show_summary() {
    echo -e "\n${ORANGE}"
    echo "═══════════════════════════════════════════════════════════════════════════════"
    echo "                    🟠 INSTALACIÓN COMPLETADA EXITOSAMENTE 🟠                  "
    echo "═══════════════════════════════════════════════════════════════════════════════"
    echo -e "${NC}"
    
    echo -e "${WHITE}📁 Estructura creada:${NC}"
    echo "   campaigns/  - Campañas de phishing"
    echo "   training/   - Material de capacitación"
    echo "   metrics/    - Métricas y reportes"
    echo "   templates/  - Templates de phishing"
    echo "   quizzes/    - Evaluaciones"
    echo "   tools/      - Scripts y herramientas"
    
    echo -e "\n${WHITE}🔧 Herramientas instaladas:${NC}"
    echo "   • GoPhish      - Plataforma de phishing"
    echo "   • King Phisher - Campañas avanzadas"
    echo "   • Evilginx2    - Proxy MitM"
    echo "   • SET          - Social Engineering Toolkit"
    echo "   • BeEF         - Browser Exploitation"
    
    echo -e "\n${WHITE}🚀 Próximos pasos:${NC}"
    echo "   1. Activar entorno: source venv/bin/activate"
    echo "   2. Iniciar servicios: docker-compose up -d"
    echo "   3. Acceder a GoPhish: https://localhost:3333"
    echo "   4. Ver dashboard: http://localhost:8080"
    
    echo -e "\n${WHITE}💬 Comandos Windsurf:${NC}"
    echo "   /phishing  - Crear campaña de phishing"
    echo "   /training  - Generar material de training"
    echo "   /metrics   - Ver métricas de awareness"
    
    echo -e "\n${ORANGE}═══════════════════════════════════════════════════════════════════════════════${NC}"
    echo -e "${WHITE}                    ¡Gracias por usar Orange Team! 🛡️${NC}"
    echo -e "${ORANGE}═══════════════════════════════════════════════════════════════════════════════${NC}\n"
}

# Función principal
main() {
    print_banner
    
    check_root
    detect_os
    check_dependencies
    create_directory_structure
    create_requirements
    setup_python_env
    install_phishing_tools
    install_social_engineering_tools
    setup_gophish_docker
    setup_elk_stack
    create_main_docker_compose
    create_config_files
    create_metrics_dashboard
    start_docker_services
    
    show_summary
}

# Ejecutar
main "$@"
