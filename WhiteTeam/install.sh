#!/bin/bash

#══════════════════════════════════════════════════════════════════════════════
#  ⚪ WHITE TEAM - GRC INSTALLER
#  Governance • Risk • Compliance
#══════════════════════════════════════════════════════════════════════════════

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
NC='\033[0m'

# Banner
print_banner() {
    echo -e "${WHITE}"
    echo "╔══════════════════════════════════════════════════════════════════════════════╗"
    echo "║                                                                              ║"
    echo "║   ██╗    ██╗██╗  ██╗██╗████████╗███████╗    ████████╗███████╗ █████╗ ███╗   ███╗   ║"
    echo "║   ██║    ██║██║  ██║██║╚══██╔══╝██╔════╝    ╚══██╔══╝██╔════╝██╔══██╗████╗ ████║   ║"
    echo "║   ██║ █╗ ██║███████║██║   ██║   █████╗         ██║   █████╗  ███████║██╔████╔██║   ║"
    echo "║   ██║███╗██║██╔══██║██║   ██║   ██╔══╝         ██║   ██╔══╝  ██╔══██║██║╚██╔╝██║   ║"
    echo "║   ╚███╔███╔╝██║  ██║██║   ██║   ███████╗       ██║   ███████╗██║  ██║██║ ╚═╝ ██║   ║"
    echo "║    ╚══╝╚══╝ ╚═╝  ╚═╝╚═╝   ╚═╝   ╚══════╝       ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝   ║"
    echo "║                                                                              ║"
    echo "║                    G R C   I N S T A L L E R   v1.0                          ║"
    echo "║                                                                              ║"
    echo "╚══════════════════════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[✓]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

log_error() {
    echo -e "${RED}[✗]${NC} $1"
}

log_step() {
    echo -e "\n${PURPLE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${CYAN}  $1${NC}"
    echo -e "${PURPLE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}\n"
}

# Check if running as root
check_root() {
    if [[ $EUID -eq 0 ]]; then
        log_warning "Running as root. Some operations will be adjusted."
        SUDO=""
    else
        SUDO="sudo"
    fi
}

# Detect OS
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
    log_info "Detected OS: $OS"
}

# Check prerequisites
check_prerequisites() {
    log_step "Checking Prerequisites"
    
    local missing=()
    
    # Check Python
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2)
        log_success "Python $PYTHON_VERSION found"
    else
        missing+=("python3")
        log_error "Python 3 not found"
    fi
    
    # Check pip
    if command -v pip3 &> /dev/null; then
        log_success "pip3 found"
    else
        missing+=("pip3")
        log_error "pip3 not found"
    fi
    
    # Check git
    if command -v git &> /dev/null; then
        log_success "Git found"
    else
        missing+=("git")
        log_error "Git not found"
    fi
    
    # Check curl
    if command -v curl &> /dev/null; then
        log_success "curl found"
    else
        missing+=("curl")
        log_warning "curl not found (optional)"
    fi
    
    if [[ ${#missing[@]} -gt 0 ]]; then
        log_error "Missing required tools: ${missing[*]}"
        log_info "Installing missing dependencies..."
        install_system_deps "${missing[@]}"
    fi
}

# Install system dependencies
install_system_deps() {
    local deps=("$@")
    
    case $OS in
        ubuntu|debian)
            $SUDO apt-get update
            $SUDO apt-get install -y "${deps[@]}"
            ;;
        fedora)
            $SUDO dnf install -y "${deps[@]}"
            ;;
        centos|rhel)
            $SUDO yum install -y "${deps[@]}"
            ;;
        arch)
            $SUDO pacman -S --noconfirm "${deps[@]}"
            ;;
        macos)
            if command -v brew &> /dev/null; then
                brew install "${deps[@]}"
            else
                log_error "Homebrew not found. Please install: https://brew.sh"
                exit 1
            fi
            ;;
        *)
            log_error "Unsupported OS. Please install manually: ${deps[*]}"
            exit 1
            ;;
    esac
}

# Create virtual environment
setup_venv() {
    log_step "Setting up Python Virtual Environment"
    
    VENV_DIR="venv"
    
    if [[ -d "$VENV_DIR" ]]; then
        log_warning "Virtual environment already exists"
        read -p "Recreate? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            rm -rf "$VENV_DIR"
            python3 -m venv "$VENV_DIR"
            log_success "Virtual environment recreated"
        fi
    else
        python3 -m venv "$VENV_DIR"
        log_success "Virtual environment created"
    fi
    
    # Activate venv
    source "$VENV_DIR/bin/activate"
    log_success "Virtual environment activated"
    
    # Upgrade pip
    pip install --upgrade pip setuptools wheel
    log_success "pip upgraded"
}

# Install Python dependencies
install_python_deps() {
    log_step "Installing Python Dependencies"
    
    # Create requirements.txt if not exists
    if [[ ! -f "requirements.txt" ]]; then
        cat > requirements.txt << 'EOF'
# WHITE TEAM GRC - Python Dependencies
# =====================================

# Core
pyyaml>=6.0.1
jinja2>=3.1.2
click>=8.1.7
pydantic>=2.5.0
python-dotenv>=1.0.0

# Data Processing
pandas>=2.1.0
numpy>=1.26.0
openpyxl>=3.1.2

# Document Generation
python-docx>=1.1.0
reportlab>=4.0.0
markdown>=3.5.0
weasyprint>=60.0

# CLI & Formatting
rich>=13.7.0
tabulate>=0.9.0
colorama>=0.4.6
tqdm>=4.66.0

# Database
sqlalchemy>=2.0.23
sqlite-utils>=3.35

# Security
cryptography>=41.0.0
python-jose>=3.3.0

# HTTP & API
requests>=2.31.0
httpx>=0.25.0
fastapi>=0.104.0
uvicorn>=0.24.0

# Testing
pytest>=7.4.0
pytest-cov>=4.1.0

# Linting & Formatting
black>=23.11.0
pylint>=3.0.0
mypy>=1.7.0

# GRC Specific
oscal-pydantic>=1.0.0
compliance-checker>=0.1.0
EOF
        log_success "requirements.txt created"
    fi
    
    pip install -r requirements.txt
    log_success "Python dependencies installed"
}

# Setup directory structure
setup_directories() {
    log_step "Setting up Directory Structure"
    
    directories=(
        "policies/security"
        "policies/privacy"
        "policies/access"
        "policies/templates"
        "procedures/incident-response"
        "procedures/change-management"
        "procedures/access-management"
        "procedures/backup-recovery"
        "audits/internal"
        "audits/external"
        "audits/checklists"
        "audits/reports"
        "risks/assessments"
        "risks/register"
        "risks/treatments"
        "risks/monitoring"
        "compliance/iso27001"
        "compliance/soc2"
        "compliance/pci-dss"
        "compliance/gdpr"
        "compliance/hipaa"
        "compliance/nist-csf"
        "frameworks/iso27001"
        "frameworks/soc2"
        "frameworks/pci-dss"
        "frameworks/gdpr"
        "frameworks/hipaa"
        "frameworks/nist-csf"
        "controls/technical"
        "controls/administrative"
        "controls/physical"
        "controls/mappings"
        "tools/custom-scripts"
        "templates/policies"
        "templates/procedures"
        "templates/audits"
        "templates/reports"
        "reports/executive"
        "reports/technical"
        "reports/compliance"
        "evidence/screenshots"
        "evidence/logs"
        "evidence/configs"
        "evidence/documents"
        ".windsurf/workflows"
        ".windsurf/skills"
        "schemas"
        "data"
        "logs"
    )
    
    for dir in "${directories[@]}"; do
        mkdir -p "$dir"
        log_info "Created: $dir"
    done
    
    log_success "Directory structure created"
}

# Create .gitignore
create_gitignore() {
    log_step "Creating .gitignore"
    
    cat > .gitignore << 'EOF'
# WHITE TEAM GRC - Git Ignore
# ===========================

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
ENV/
.venv/
pip-log.txt
pip-delete-this-directory.txt

# IDE
.idea/
.vscode/
*.swp
*.swo
*~
.project
.pydevproject
.settings/

# OS
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# Logs
logs/
*.log

# Sensitive Data
.env
.env.local
.env.*.local
secrets/
credentials/
*.key
*.pem
*.crt

# Evidence (large files)
evidence/screenshots/*.png
evidence/screenshots/*.jpg
evidence/logs/*.log
evidence/configs/*.bak

# Reports (generated)
reports/**/*.pdf
reports/**/*.docx
reports/**/*.xlsx

# Database
*.db
*.sqlite
*.sqlite3

# Temporary
tmp/
temp/
*.tmp
*.temp
*.bak
*.backup

# Build
build/
dist/
*.egg-info/

# Coverage
.coverage
htmlcov/
.pytest_cache/

# MyPy
.mypy_cache/
EOF
    
    log_success ".gitignore created"
}

# Create environment file template
create_env_template() {
    log_step "Creating Environment Template"
    
    cat > .env.example << 'EOF'
# WHITE TEAM GRC - Environment Configuration
# ==========================================
# Copy this file to .env and fill in your values

# Organization
ORG_NAME="Your Organization"
ORG_DOMAIN="example.com"

# Database
DATABASE_URL="sqlite:///data/grc.db"

# API Keys (if using external services)
# OPENRMF_API_KEY=""
# ERAMBA_API_KEY=""

# Email Notifications
# SMTP_HOST=""
# SMTP_PORT=587
# SMTP_USER=""
# SMTP_PASSWORD=""

# Logging
LOG_LEVEL="INFO"
LOG_FILE="logs/grc.log"

# Security
SECRET_KEY="change-this-to-a-secure-random-string"
ENCRYPTION_KEY=""

# Frameworks Enabled
FRAMEWORKS_ENABLED="ISO27001,SOC2,PCI-DSS,GDPR,HIPAA,NIST-CSF"

# Compliance Settings
COMPLIANCE_CHECK_INTERVAL="daily"
RISK_ASSESSMENT_INTERVAL="weekly"
AUDIT_REMINDER_DAYS=30
EOF
    
    log_success ".env.example created"
}

# Initialize Git repository
init_git() {
    log_step "Initializing Git Repository"
    
    if [[ -d ".git" ]]; then
        log_warning "Git repository already initialized"
    else
        git init
        log_success "Git repository initialized"
    fi
    
    # Create initial commit
    git add .
    git commit -m "Initial commit: WHITE TEAM GRC workspace setup" 2>/dev/null || true
    log_success "Initial commit created"
}

# Create placeholder files
create_placeholders() {
    log_step "Creating Placeholder Files"
    
    # Create .gitkeep files for empty directories
    find . -type d -empty -not -path "./.git/*" -exec touch {}/.gitkeep \;
    
    # Create README files for main directories
    directories=("policies" "procedures" "audits" "risks" "compliance" "frameworks" "controls" "templates" "reports" "evidence")
    
    for dir in "${directories[@]}"; do
        if [[ ! -f "$dir/README.md" ]]; then
            echo "# ${dir^}" > "$dir/README.md"
            echo "" >> "$dir/README.md"
            echo "This directory contains ${dir} for the WHITE TEAM GRC system." >> "$dir/README.md"
        fi
    done
    
    log_success "Placeholder files created"
}

# Verify installation
verify_installation() {
    log_step "Verifying Installation"
    
    local errors=0
    
    # Check Python scripts
    if [[ -f "tools/custom-scripts/compliance_check.py" ]]; then
        log_success "compliance_check.py exists"
    else
        log_warning "compliance_check.py not found"
        ((errors++))
    fi
    
    # Check virtual environment
    if [[ -d "venv" ]]; then
        log_success "Virtual environment exists"
    else
        log_error "Virtual environment not found"
        ((errors++))
    fi
    
    # Check key directories
    key_dirs=("policies" "procedures" "audits" "risks" "compliance" "frameworks" "controls" "tools")
    for dir in "${key_dirs[@]}"; do
        if [[ -d "$dir" ]]; then
            log_success "Directory $dir exists"
        else
            log_error "Directory $dir not found"
            ((errors++))
        fi
    done
    
    if [[ $errors -eq 0 ]]; then
        log_success "All verifications passed!"
    else
        log_warning "$errors verification(s) failed"
    fi
}

# Print completion message
print_completion() {
    echo -e "\n${GREEN}"
    echo "╔══════════════════════════════════════════════════════════════════════════════╗"
    echo "║                                                                              ║"
    echo "║                    ✓ INSTALLATION COMPLETED SUCCESSFULLY                     ║"
    echo "║                                                                              ║"
    echo "╚══════════════════════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
    
    echo -e "${CYAN}Next Steps:${NC}"
    echo ""
    echo "  1. Activate the virtual environment:"
    echo -e "     ${WHITE}source venv/bin/activate${NC}"
    echo ""
    echo "  2. Configure your environment:"
    echo -e "     ${WHITE}cp .env.example .env${NC}"
    echo -e "     ${WHITE}nano .env${NC}"
    echo ""
    echo "  3. Open the workspace in VS Code/Windsurf:"
    echo -e "     ${WHITE}code WhiteTeam-GRC.code-workspace${NC}"
    echo ""
    echo "  4. Run a compliance check:"
    echo -e "     ${WHITE}python tools/custom-scripts/compliance_check.py --help${NC}"
    echo ""
    echo -e "${PURPLE}Available Commands:${NC}"
    echo "  • /audit      - Run an audit"
    echo "  • /risk       - Assess a risk"
    echo "  • /compliance - Check compliance status"
    echo "  • /policy     - Generate a policy"
    echo "  • /gap        - Run gap analysis"
    echo ""
    echo -e "${WHITE}⚪ WHITE TEAM GRC - Ready for Governance, Risk & Compliance${NC}"
    echo ""
}

# Main installation function
main() {
    print_banner
    
    # Get script directory
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    cd "$SCRIPT_DIR"
    
    check_root
    detect_os
    check_prerequisites
    setup_venv
    install_python_deps
    setup_directories
    create_gitignore
    create_env_template
    create_placeholders
    init_git
    verify_installation
    print_completion
}

# Run main function
main "$@"
