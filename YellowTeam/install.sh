#!/bin/bash

#═══════════════════════════════════════════════════════════════════════════════
#  🟡 YELLOW TEAM - Security Architecture Installer
#═══════════════════════════════════════════════════════════════════════════════
#  Instala todas las herramientas necesarias para el workspace de Yellow Team
#  Threat Modeling, Diagramming, Documentation, Analysis Tools
#═══════════════════════════════════════════════════════════════════════════════

set -e

# Colors
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color
BOLD='\033[1m'

# Banner
print_banner() {
    echo -e "${YELLOW}"
    cat << "EOF"
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║   ██╗   ██╗███████╗██╗     ██╗      ██████╗ ██╗    ██╗                       ║
║   ╚██╗ ██╔╝██╔════╝██║     ██║     ██╔═══██╗██║    ██║                       ║
║    ╚████╔╝ █████╗  ██║     ██║     ██║   ██║██║ █╗ ██║                       ║
║     ╚██╔╝  ██╔══╝  ██║     ██║     ██║   ██║██║███╗██║                       ║
║      ██║   ███████╗███████╗███████╗╚██████╔╝╚███╔███╔╝                       ║
║      ╚═╝   ╚══════╝╚══════╝╚══════╝ ╚═════╝  ╚══╝╚══╝                        ║
║                                                                               ║
║              ████████╗███████╗ █████╗ ███╗   ███╗                             ║
║              ╚══██╔══╝██╔════╝██╔══██╗████╗ ████║                             ║
║                 ██║   █████╗  ███████║██╔████╔██║                             ║
║                 ██║   ██╔══╝  ██╔══██║██║╚██╔╝██║                             ║
║                 ██║   ███████╗██║  ██║██║ ╚═╝ ██║                             ║
║                 ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝                             ║
║                                                                               ║
║          🏗️  SECURITY ARCHITECTURE INSTALLER  🛡️                              ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
EOF
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

log_section() {
    echo ""
    echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${YELLOW}  $1${NC}"
    echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
}

# Check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Detect package manager
detect_package_manager() {
    if command_exists apt-get; then
        PKG_MANAGER="apt"
        PKG_INSTALL="sudo apt-get install -y"
        PKG_UPDATE="sudo apt-get update"
    elif command_exists dnf; then
        PKG_MANAGER="dnf"
        PKG_INSTALL="sudo dnf install -y"
        PKG_UPDATE="sudo dnf check-update || true"
    elif command_exists yum; then
        PKG_MANAGER="yum"
        PKG_INSTALL="sudo yum install -y"
        PKG_UPDATE="sudo yum check-update || true"
    elif command_exists pacman; then
        PKG_MANAGER="pacman"
        PKG_INSTALL="sudo pacman -S --noconfirm"
        PKG_UPDATE="sudo pacman -Sy"
    elif command_exists brew; then
        PKG_MANAGER="brew"
        PKG_INSTALL="brew install"
        PKG_UPDATE="brew update"
    else
        log_error "No supported package manager found"
        exit 1
    fi
    log_info "Detected package manager: ${PKG_MANAGER}"
}

# Install system dependencies
install_system_deps() {
    log_section "📦 Installing System Dependencies"

    $PKG_UPDATE

    # Common packages
    local packages=(
        "git"
        "curl"
        "wget"
        "jq"
        "graphviz"
        "plantuml"
    )

    for pkg in "${packages[@]}"; do
        if ! command_exists "$pkg"; then
            log_info "Installing $pkg..."
            $PKG_INSTALL "$pkg" || log_warning "Could not install $pkg"
        else
            log_success "$pkg already installed"
        fi
    done

    # Java for PlantUML
    if ! command_exists java; then
        log_info "Installing Java (required for PlantUML)..."
        case $PKG_MANAGER in
            apt)
                $PKG_INSTALL default-jre
                ;;
            dnf|yum)
                $PKG_INSTALL java-11-openjdk
                ;;
            pacman)
                $PKG_INSTALL jre-openjdk
                ;;
            brew)
                $PKG_INSTALL openjdk
                ;;
        esac
    else
        log_success "Java already installed"
    fi
}

# Install Python and create virtual environment
setup_python_env() {
    log_section "🐍 Setting up Python Environment"

    # Check Python
    if ! command_exists python3; then
        log_info "Installing Python3..."
        $PKG_INSTALL python3 python3-pip python3-venv
    else
        log_success "Python3 already installed: $(python3 --version)"
    fi

    # Create virtual environment
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    VENV_DIR="$SCRIPT_DIR/venv"

    if [ ! -d "$VENV_DIR" ]; then
        log_info "Creating virtual environment..."
        python3 -m venv "$VENV_DIR"
        log_success "Virtual environment created at $VENV_DIR"
    else
        log_success "Virtual environment already exists"
    fi

    # Activate and install packages
    source "$VENV_DIR/bin/activate"

    log_info "Installing Python packages..."
    pip install --upgrade pip

    # Create requirements.txt
    cat > "$SCRIPT_DIR/requirements.txt" << 'EOF'
# Yellow Team - Security Architecture Dependencies

# Core
pyyaml>=6.0
jinja2>=3.1.0
click>=8.1.0
rich>=13.0.0
typer>=0.9.0

# Threat Modeling
pytm>=1.3.0

# Diagramming
diagrams>=0.23.0
plantuml>=0.3.0

# Documentation
mkdocs>=1.5.0
mkdocs-material>=9.0.0
mkdocs-mermaid2-plugin>=1.0.0

# Analysis & Reporting
pandas>=2.0.0
openpyxl>=3.1.0
python-docx>=0.8.11
reportlab>=4.0.0

# Security Analysis
bandit>=1.7.0
safety>=2.3.0

# JSON/YAML processing
jsonschema>=4.17.0
ruamel.yaml>=0.17.0

# HTTP client (for API integrations)
requests>=2.31.0
httpx>=0.24.0

# Testing
pytest>=7.4.0
pytest-cov>=4.1.0

# Code quality
black>=23.0.0
flake8>=6.1.0
mypy>=1.5.0
EOF

    pip install -r "$SCRIPT_DIR/requirements.txt"
    log_success "Python packages installed"
}

# Install Node.js tools
install_node_tools() {
    log_section "📦 Installing Node.js Tools"

    # Check Node.js
    if ! command_exists node; then
        log_info "Installing Node.js..."
        if command_exists curl; then
            curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
            $PKG_INSTALL nodejs
        else
            $PKG_INSTALL nodejs npm
        fi
    else
        log_success "Node.js already installed: $(node --version)"
    fi

    # Install global npm packages
    log_info "Installing npm packages..."
    npm install -g @mermaid-js/mermaid-cli || log_warning "Could not install mermaid-cli"
    npm install -g markdownlint-cli || log_warning "Could not install markdownlint-cli"

    log_success "Node.js tools installed"
}

# Install Threat Modeling Tools
install_threat_modeling_tools() {
    log_section "🔍 Installing Threat Modeling Tools"

    # OWASP Threat Dragon (Desktop App)
    log_info "OWASP Threat Dragon can be downloaded from:"
    echo -e "${CYAN}  https://github.com/OWASP/threat-dragon/releases${NC}"

    # Microsoft Threat Modeling Tool (Windows only, note for reference)
    log_info "Microsoft TMT (Windows only) available at:"
    echo -e "${CYAN}  https://aka.ms/threatmodelingtool${NC}"

    # PyTM (Python Threat Modeling)
    log_info "PyTM installed via Python packages"

    log_success "Threat modeling tools information provided"
}

# Install Diagramming Tools
install_diagramming_tools() {
    log_section "📊 Installing Diagramming Tools"

    # Draw.io Desktop
    if ! command_exists drawio; then
        log_info "Draw.io Desktop can be downloaded from:"
        echo -e "${CYAN}  https://github.com/jgraph/drawio-desktop/releases${NC}"

        # Try to install via snap if available
        if command_exists snap; then
            log_info "Attempting to install Draw.io via snap..."
            sudo snap install drawio || log_warning "Could not install Draw.io via snap"
        fi
    else
        log_success "Draw.io already installed"
    fi

    # PlantUML (already installed via system deps)
    log_success "PlantUML installed"

    # Mermaid CLI (already installed via npm)
    log_success "Mermaid CLI installed"

    # Graphviz (already installed via system deps)
    log_success "Graphviz installed"
}

# Install Documentation Tools
install_documentation_tools() {
    log_section "📚 Installing Documentation Tools"

    # MkDocs (already installed via pip)
    log_success "MkDocs installed via Python"

    # Initialize MkDocs if not exists
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    if [ ! -f "$SCRIPT_DIR/mkdocs.yml" ]; then
        log_info "Creating MkDocs configuration..."
        cat > "$SCRIPT_DIR/mkdocs.yml" << 'EOF'
site_name: Yellow Team - Security Architecture
site_description: Security Architecture & Threat Modeling Documentation
site_author: Yellow Team

theme:
  name: material
  palette:
    primary: amber
    accent: amber
  features:
    - navigation.tabs
    - navigation.sections
    - toc.integrate
    - search.suggest
    - content.code.copy

plugins:
  - search
  - mermaid2

markdown_extensions:
  - pymdownx.highlight
  - pymdownx.superfences:
      custom_fences:
        - name: mermaid
          class: mermaid
          format: !!python/name:pymdownx.superfences.fence_code_format
  - pymdownx.tabbed
  - admonition
  - tables
  - toc:
      permalink: true

nav:
  - Home: index.md
  - Threat Modeling:
    - STRIDE: threat-modeling/stride.md
    - PASTA: threat-modeling/pasta.md
    - Attack Trees: threat-modeling/attack-trees.md
  - Frameworks:
    - SABSA: frameworks/sabsa.md
    - TOGAF: frameworks/togaf.md
    - NIST CSF: frameworks/nist-csf.md
  - Zero Trust:
    - Principles: zero-trust/principles.md
    - Architecture: zero-trust/architecture.md
  - Tools:
    - Scripts: tools/scripts.md
    - Templates: tools/templates.md
EOF
        log_success "MkDocs configuration created"
    fi
}

# Create directory structure
create_directory_structure() {
    log_section "📁 Creating Directory Structure"

    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

    # Main directories
    directories=(
        "architectures/templates"
        "architectures/examples"
        "threat-models/templates"
        "threat-models/completed"
        "requirements/templates"
        "requirements/projects"
        "patterns/authentication"
        "patterns/authorization"
        "patterns/encryption"
        "patterns/network"
        "frameworks/sabsa"
        "frameworks/togaf"
        "frameworks/nist"
        "frameworks/zero-trust"
        "reviews/templates"
        "reviews/completed"
        "tools/custom-scripts"
        "templates/threat-models"
        "templates/architectures"
        "templates/requirements"
        "reports"
        ".windsurf/workflows"
        ".windsurf/skills"
        "docs"
    )

    for dir in "${directories[@]}"; do
        mkdir -p "$SCRIPT_DIR/$dir"
        log_success "Created: $dir"
    done
}

# Create template files
create_templates() {
    log_section "📝 Creating Template Files"

    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

    # STRIDE Template
    cat > "$SCRIPT_DIR/templates/threat-models/stride-template.md" << 'EOF'
# STRIDE Threat Model

## System Information
- **System Name:**
- **Version:**
- **Date:**
- **Author:**

## System Description


## Data Flow Diagram

```mermaid
flowchart LR
    subgraph External
        User[User]
    end

    subgraph TrustBoundary[Trust Boundary]
        WebApp[Web Application]
        API[API Server]
        DB[(Database)]
    end

    User -->|HTTPS| WebApp
    WebApp -->|REST| API
    API -->|SQL| DB
```

## Threat Analysis

### Spoofing
| ID | Threat | Impact | Likelihood | Mitigation |
|----|--------|--------|------------|------------|
| S1 |        |        |            |            |

### Tampering
| ID | Threat | Impact | Likelihood | Mitigation |
|----|--------|--------|------------|------------|
| T1 |        |        |            |            |

### Repudiation
| ID | Threat | Impact | Likelihood | Mitigation |
|----|--------|--------|------------|------------|
| R1 |        |        |            |            |

### Information Disclosure
| ID | Threat | Impact | Likelihood | Mitigation |
|----|--------|--------|------------|------------|
| I1 |        |        |            |            |

### Denial of Service
| ID | Threat | Impact | Likelihood | Mitigation |
|----|--------|--------|------------|------------|
| D1 |        |        |            |            |

### Elevation of Privilege
| ID | Threat | Impact | Likelihood | Mitigation |
|----|--------|--------|------------|------------|
| E1 |        |        |            |            |

## Risk Summary

## Recommendations
EOF

    # Architecture Review Template
    cat > "$SCRIPT_DIR/templates/architectures/review-template.md" << 'EOF'
# Architecture Security Review

## System Information
- **System Name:**
- **Review Date:**
- **Reviewer:**
- **Version:**

## Executive Summary


## Architecture Overview

### Components
| Component | Description | Technology | Security Controls |
|-----------|-------------|------------|-------------------|
|           |             |            |                   |

### Data Flows
| Source | Destination | Data Type | Protection |
|--------|-------------|-----------|------------|
|        |             |           |            |

## Security Assessment

### Authentication
- [ ] MFA implemented
- [ ] Session management
- [ ] Password policy

### Authorization
- [ ] RBAC/ABAC
- [ ] Least privilege
- [ ] Separation of duties

### Data Protection
- [ ] Encryption at rest
- [ ] Encryption in transit
- [ ] Key management

### Network Security
- [ ] Segmentation
- [ ] Firewall rules
- [ ] WAF/IDS/IPS

### Logging & Monitoring
- [ ] Audit logging
- [ ] SIEM integration
- [ ] Alerting

## Findings

### Critical
| ID | Finding | Risk | Recommendation |
|----|---------|------|----------------|
|    |         |      |                |

### High
| ID | Finding | Risk | Recommendation |
|----|---------|------|----------------|
|    |         |      |                |

### Medium
| ID | Finding | Risk | Recommendation |
|----|---------|------|----------------|
|    |         |      |                |

### Low
| ID | Finding | Risk | Recommendation |
|----|---------|------|----------------|
|    |         |      |                |

## Recommendations


## Appendix
EOF

    # Security Requirements Template
    cat > "$SCRIPT_DIR/templates/requirements/security-requirements-template.md" << 'EOF'
# Security Requirements Specification

## Document Information
- **Project:**
- **Version:**
- **Date:**
- **Author:**

## 1. Authentication Requirements

| ID | Requirement | Priority | Status |
|----|-------------|----------|--------|
| AUTH-001 | System SHALL implement MFA | High | |
| AUTH-002 | System SHALL enforce password complexity | High | |
| AUTH-003 | System SHALL implement account lockout | Medium | |

## 2. Authorization Requirements

| ID | Requirement | Priority | Status |
|----|-------------|----------|--------|
| AUTHZ-001 | System SHALL implement RBAC | High | |
| AUTHZ-002 | System SHALL enforce least privilege | High | |

## 3. Data Protection Requirements

| ID | Requirement | Priority | Status |
|----|-------------|----------|--------|
| DATA-001 | System SHALL encrypt data at rest | High | |
| DATA-002 | System SHALL encrypt data in transit | High | |
| DATA-003 | System SHALL implement key rotation | Medium | |

## 4. Logging & Monitoring Requirements

| ID | Requirement | Priority | Status |
|----|-------------|----------|--------|
| LOG-001 | System SHALL log all authentication events | High | |
| LOG-002 | System SHALL log all authorization failures | High | |
| LOG-003 | System SHALL retain logs for 90 days | Medium | |

## 5. Network Security Requirements

| ID | Requirement | Priority | Status |
|----|-------------|----------|--------|
| NET-001 | System SHALL implement network segmentation | High | |
| NET-002 | System SHALL use TLS 1.3 | High | |

## 6. Compliance Requirements

| ID | Requirement | Standard | Status |
|----|-------------|----------|--------|
| COMP-001 | | | |

## Traceability Matrix

| Requirement | Threat | Control | Test |
|-------------|--------|---------|------|
|             |        |         |      |
EOF

    log_success "Templates created"
}

# Create .gitignore
create_gitignore() {
    log_section "📄 Creating .gitignore"

    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

    cat > "$SCRIPT_DIR/.gitignore" << 'EOF'
# Virtual Environment
venv/
.venv/
env/

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
*.egg-info/
.eggs/
dist/
build/

# IDE
.idea/
.vscode/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Logs
*.log
logs/

# Temp files
*.tmp
*.temp
.cache/

# Reports (optional - uncomment if you want to ignore)
# reports/

# Secrets (NEVER commit these)
*.pem
*.key
*.crt
.env
.env.local
secrets/
credentials/

# Node
node_modules/

# MkDocs
site/
EOF

    log_success ".gitignore created"
}

# Make scripts executable
make_scripts_executable() {
    log_section "🔧 Setting Script Permissions"

    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

    if [ -d "$SCRIPT_DIR/tools/custom-scripts" ]; then
        chmod +x "$SCRIPT_DIR/tools/custom-scripts/"*.sh 2>/dev/null || true
        chmod +x "$SCRIPT_DIR/tools/custom-scripts/"*.py 2>/dev/null || true
        log_success "Script permissions set"
    fi
}

# Print completion message
print_completion() {
    echo ""
    echo -e "${GREEN}"
    cat << "EOF"
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║   ✅ INSTALLATION COMPLETE!                                                   ║
║                                                                               ║
║   🟡 Yellow Team Security Architecture Workspace is ready!                    ║
║                                                                               ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║   Next Steps:                                                                 ║
║                                                                               ║
║   1. Activate virtual environment:                                            ║
║      source venv/bin/activate                                                 ║
║                                                                               ║
║   2. Open workspace in Windsurf:                                              ║
║      windsurf YellowTeam.code-workspace                                       ║
║                                                                               ║
║   3. Use Windsurf AI commands:                                                ║
║      /threat-model  - Create threat model                                     ║
║      /review-arch   - Review architecture                                     ║
║      /zero-trust    - Validate Zero Trust                                     ║
║                                                                               ║
║   4. Run custom scripts:                                                      ║
║      python tools/custom-scripts/threat_model.py                              ║
║      python tools/custom-scripts/architecture_review.py                       ║
║      bash tools/custom-scripts/zero_trust_check.sh                            ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
EOF
    echo -e "${NC}"
}

# Main installation
main() {
    print_banner

    log_info "Starting Yellow Team Security Architecture installation..."
    log_info "This may take several minutes..."

    detect_package_manager
    install_system_deps
    setup_python_env
    install_node_tools
    install_threat_modeling_tools
    install_diagramming_tools
    install_documentation_tools
    create_directory_structure
    create_templates
    create_gitignore
    make_scripts_executable

    print_completion
}

# Run main
main "$@"
