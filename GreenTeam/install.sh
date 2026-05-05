#!/bin/bash

#╔══════════════════════════════════════════════════════════════════════════════╗
#║                                                                              ║
#║   🟢 GREEN TEAM - DevSecOps Environment Installer                           ║
#║   ═══════════════════════════════════════════════════════════════════════   ║
#║                                                                              ║
#║   Este script instala todas las herramientas necesarias para un entorno     ║
#║   completo de DevSecOps con integración Windsurf AI.                        ║
#║                                                                              ║
#║   Categorías:                                                                ║
#║   • SAST: Semgrep, SonarQube, Bandit, ESLint Security                       ║
#║   • DAST: OWASP ZAP, Nuclei, Nikto                                          ║
#║   • SCA: Snyk, OWASP Dependency-Check                                       ║
#║   • Secrets: Gitleaks, TruffleHog, detect-secrets                           ║
#║   • Container: Trivy, Grype, Clair, Falco                                   ║
#║   • IaC: Checkov, tfsec, KICS                                               ║
#║   • API: Postman CLI, Insomnia                                              ║
#║                                                                              ║
#╚══════════════════════════════════════════════════════════════════════════════╝

set -e

# ═══════════════════════════════════════════════════════════════════════════════
# COLORES Y ESTILOS
# ═══════════════════════════════════════════════════════════════════════════════
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
NC='\033[0m' # No Color
BOLD='\033[1m'

# ═══════════════════════════════════════════════════════════════════════════════
# VARIABLES GLOBALES
# ═══════════════════════════════════════════════════════════════════════════════
INSTALL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_FILE="${INSTALL_DIR}/install.log"
TOOLS_INSTALLED=0
TOOLS_FAILED=0
TOOLS_SKIPPED=0

# ═══════════════════════════════════════════════════════════════════════════════
# FUNCIONES DE UTILIDAD
# ═══════════════════════════════════════════════════════════════════════════════

print_banner() {
    echo -e "${GREEN}"
    cat << 'EOF'
    
    ╔═══════════════════════════════════════════════════════════════════════════╗
    ║                                                                           ║
    ║   ██████╗ ██████╗ ███████╗███████╗███╗   ██╗    ████████╗███████╗ █████╗  ║
    ║  ██╔════╝ ██╔══██╗██╔════╝██╔════╝████╗  ██║    ╚══██╔══╝██╔════╝██╔══██╗ ║
    ║  ██║  ███╗██████╔╝█████╗  █████╗  ██╔██╗ ██║       ██║   █████╗  ███████║ ║
    ║  ██║   ██║██╔══██╗██╔══╝  ██╔══╝  ██║╚██╗██║       ██║   ██╔══╝  ██╔══██║ ║
    ║  ╚██████╔╝██║  ██║███████╗███████╗██║ ╚████║       ██║   ███████╗██║  ██║ ║
    ║   ╚═════╝ ╚═╝  ╚═╝╚══════╝╚══════╝╚═╝  ╚═══╝       ╚═╝   ╚══════╝╚═╝  ╚═╝ ║
    ║                                                                           ║
    ║                    🛡️  DevSecOps Environment Installer  🛡️                ║
    ║                                                                           ║
    ╚═══════════════════════════════════════════════════════════════════════════╝

EOF
    echo -e "${NC}"
}

print_section() {
    echo -e "\n${CYAN}╔══════════════════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${CYAN}║${NC} ${BOLD}${WHITE}$1${NC}"
    echo -e "${CYAN}╚══════════════════════════════════════════════════════════════════════════════╝${NC}\n"
}

print_subsection() {
    echo -e "\n${PURPLE}┌──────────────────────────────────────────────────────────────────────────────┐${NC}"
    echo -e "${PURPLE}│${NC} ${BOLD}$1${NC}"
    echo -e "${PURPLE}└──────────────────────────────────────────────────────────────────────────────┘${NC}"
}

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
    echo "[INFO] $(date '+%Y-%m-%d %H:%M:%S') $1" >> "$LOG_FILE"
}

log_success() {
    echo -e "${GREEN}[✓]${NC} $1"
    echo "[SUCCESS] $(date '+%Y-%m-%d %H:%M:%S') $1" >> "$LOG_FILE"
    ((TOOLS_INSTALLED++))
}

log_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
    echo "[WARNING] $(date '+%Y-%m-%d %H:%M:%S') $1" >> "$LOG_FILE"
}

log_error() {
    echo -e "${RED}[✗]${NC} $1"
    echo "[ERROR] $(date '+%Y-%m-%d %H:%M:%S') $1" >> "$LOG_FILE"
    ((TOOLS_FAILED++))
}

log_skip() {
    echo -e "${YELLOW}[→]${NC} $1 (ya instalado)"
    echo "[SKIP] $(date '+%Y-%m-%d %H:%M:%S') $1 already installed" >> "$LOG_FILE"
    ((TOOLS_SKIPPED++))
}

check_command() {
    command -v "$1" &> /dev/null
}

check_root() {
    if [[ $EUID -eq 0 ]]; then
        log_warning "Ejecutando como root. Algunas herramientas se instalarán globalmente."
        SUDO=""
    else
        SUDO="sudo"
    fi
}

detect_os() {
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        if check_command apt-get; then
            OS="debian"
            PKG_MANAGER="apt-get"
        elif check_command yum; then
            OS="rhel"
            PKG_MANAGER="yum"
        elif check_command dnf; then
            OS="fedora"
            PKG_MANAGER="dnf"
        elif check_command pacman; then
            OS="arch"
            PKG_MANAGER="pacman"
        else
            OS="linux"
            PKG_MANAGER="unknown"
        fi
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        OS="macos"
        PKG_MANAGER="brew"
    else
        OS="unknown"
        PKG_MANAGER="unknown"
    fi
    log_info "Sistema operativo detectado: $OS ($PKG_MANAGER)"
}

# ═══════════════════════════════════════════════════════════════════════════════
# INSTALACIÓN DE DEPENDENCIAS BASE
# ═══════════════════════════════════════════════════════════════════════════════

install_base_dependencies() {
    print_section "📦 Instalando Dependencias Base"
    
    case $OS in
        debian)
            log_info "Actualizando repositorios..."
            $SUDO apt-get update -qq
            
            log_info "Instalando dependencias base..."
            $SUDO apt-get install -y -qq \
                curl wget git jq unzip \
                python3 python3-pip python3-venv \
                nodejs npm \
                golang-go \
                docker.io docker-compose \
                ruby ruby-dev \
                openjdk-17-jdk \
                build-essential \
                2>/dev/null || log_warning "Algunas dependencias no se pudieron instalar"
            ;;
        rhel|fedora)
            log_info "Instalando dependencias base..."
            $SUDO $PKG_MANAGER install -y -q \
                curl wget git jq unzip \
                python3 python3-pip \
                nodejs npm \
                golang \
                docker docker-compose \
                ruby ruby-devel \
                java-17-openjdk \
                gcc gcc-c++ make \
                2>/dev/null || log_warning "Algunas dependencias no se pudieron instalar"
            ;;
        arch)
            log_info "Instalando dependencias base..."
            $SUDO pacman -Sy --noconfirm --quiet \
                curl wget git jq unzip \
                python python-pip \
                nodejs npm \
                go \
                docker docker-compose \
                ruby \
                jdk17-openjdk \
                base-devel \
                2>/dev/null || log_warning "Algunas dependencias no se pudieron instalar"
            ;;
        macos)
            if ! check_command brew; then
                log_info "Instalando Homebrew..."
                /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
            fi
            
            log_info "Instalando dependencias base..."
            brew install -q \
                curl wget git jq unzip \
                python3 \
                node \
                go \
                docker docker-compose \
                ruby \
                openjdk@17 \
                2>/dev/null || log_warning "Algunas dependencias no se pudieron instalar"
            ;;
        *)
            log_warning "Sistema operativo no soportado para instalación automática de dependencias"
            ;;
    esac
    
    log_success "Dependencias base instaladas"
}

# ═══════════════════════════════════════════════════════════════════════════════
# SAST - STATIC APPLICATION SECURITY TESTING
# ═══════════════════════════════════════════════════════════════════════════════

install_sast_tools() {
    print_section "📊 SAST - Static Application Security Testing"
    
    # Semgrep
    print_subsection "Semgrep - Multi-language SAST"
    if check_command semgrep; then
        log_skip "Semgrep"
    else
        log_info "Instalando Semgrep..."
        pip3 install semgrep --quiet 2>/dev/null && log_success "Semgrep instalado" || log_error "Error instalando Semgrep"
    fi
    
    # Bandit (Python)
    print_subsection "Bandit - Python Security Linter"
    if check_command bandit; then
        log_skip "Bandit"
    else
        log_info "Instalando Bandit..."
        pip3 install bandit --quiet 2>/dev/null && log_success "Bandit instalado" || log_error "Error instalando Bandit"
    fi
    
    # ESLint Security
    print_subsection "ESLint Security - JavaScript/TypeScript Security"
    if npm list -g eslint-plugin-security &>/dev/null; then
        log_skip "ESLint Security"
    else
        log_info "Instalando ESLint y plugins de seguridad..."
        npm install -g eslint eslint-plugin-security eslint-plugin-no-secrets --quiet 2>/dev/null && \
            log_success "ESLint Security instalado" || log_error "Error instalando ESLint Security"
    fi
    
    # Brakeman (Ruby)
    print_subsection "Brakeman - Ruby on Rails Security Scanner"
    if check_command brakeman; then
        log_skip "Brakeman"
    else
        log_info "Instalando Brakeman..."
        gem install brakeman --quiet 2>/dev/null && log_success "Brakeman instalado" || log_error "Error instalando Brakeman"
    fi
    
    # Gosec (Go)
    print_subsection "Gosec - Go Security Checker"
    if check_command gosec; then
        log_skip "Gosec"
    else
        log_info "Instalando Gosec..."
        go install github.com/securego/gosec/v2/cmd/gosec@latest 2>/dev/null && \
            log_success "Gosec instalado" || log_error "Error instalando Gosec"
    fi
    
    # SpotBugs (Java) - Descarga JAR
    print_subsection "SpotBugs - Java Static Analysis"
    if [[ -f "${INSTALL_DIR}/tools/spotbugs/lib/spotbugs.jar" ]]; then
        log_skip "SpotBugs"
    else
        log_info "Descargando SpotBugs..."
        mkdir -p "${INSTALL_DIR}/tools/spotbugs"
        SPOTBUGS_VERSION="4.8.3"
        curl -sL "https://github.com/spotbugs/spotbugs/releases/download/${SPOTBUGS_VERSION}/spotbugs-${SPOTBUGS_VERSION}.tgz" | \
            tar -xz -C "${INSTALL_DIR}/tools/spotbugs" --strip-components=1 2>/dev/null && \
            log_success "SpotBugs instalado" || log_error "Error instalando SpotBugs"
    fi
    
    # SonarScanner
    print_subsection "SonarScanner - SonarQube CLI"
    if check_command sonar-scanner; then
        log_skip "SonarScanner"
    else
        log_info "Instalando SonarScanner..."
        SONAR_VERSION="5.0.1.3006"
        mkdir -p "${INSTALL_DIR}/tools/sonar-scanner"
        curl -sL "https://binaries.sonarsource.com/Distribution/sonar-scanner-cli/sonar-scanner-cli-${SONAR_VERSION}-linux.zip" \
            -o /tmp/sonar-scanner.zip 2>/dev/null
        unzip -q /tmp/sonar-scanner.zip -d "${INSTALL_DIR}/tools/" 2>/dev/null && \
            mv "${INSTALL_DIR}/tools/sonar-scanner-${SONAR_VERSION}-linux" "${INSTALL_DIR}/tools/sonar-scanner" 2>/dev/null && \
            log_success "SonarScanner instalado" || log_error "Error instalando SonarScanner"
        rm -f /tmp/sonar-scanner.zip
    fi
}

# ═══════════════════════════════════════════════════════════════════════════════
# DAST - DYNAMIC APPLICATION SECURITY TESTING
# ═══════════════════════════════════════════════════════════════════════════════

install_dast_tools() {
    print_section "🌐 DAST - Dynamic Application Security Testing"
    
    # OWASP ZAP
    print_subsection "OWASP ZAP - Web Application Scanner"
    if check_command zap.sh || check_command zaproxy; then
        log_skip "OWASP ZAP"
    else
        log_info "Instalando OWASP ZAP..."
        case $OS in
            debian)
                $SUDO apt-get install -y -qq zaproxy 2>/dev/null && \
                    log_success "OWASP ZAP instalado" || log_error "Error instalando OWASP ZAP"
                ;;
            macos)
                brew install --cask owasp-zap 2>/dev/null && \
                    log_success "OWASP ZAP instalado" || log_error "Error instalando OWASP ZAP"
                ;;
            *)
                log_warning "Instalar OWASP ZAP manualmente: https://www.zaproxy.org/download/"
                ;;
        esac
    fi
    
    # Nuclei
    print_subsection "Nuclei - Fast Vulnerability Scanner"
    if check_command nuclei; then
        log_skip "Nuclei"
    else
        log_info "Instalando Nuclei..."
        go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest 2>/dev/null && \
            log_success "Nuclei instalado" || log_error "Error instalando Nuclei"
    fi
    
    # Nikto
    print_subsection "Nikto - Web Server Scanner"
    if check_command nikto; then
        log_skip "Nikto"
    else
        log_info "Instalando Nikto..."
        case $OS in
            debian)
                $SUDO apt-get install -y -qq nikto 2>/dev/null && \
                    log_success "Nikto instalado" || log_error "Error instalando Nikto"
                ;;
            macos)
                brew install nikto 2>/dev/null && \
                    log_success "Nikto instalado" || log_error "Error instalando Nikto"
                ;;
            *)
                git clone https://github.com/sullo/nikto.git "${INSTALL_DIR}/tools/nikto" 2>/dev/null && \
                    log_success "Nikto instalado" || log_error "Error instalando Nikto"
                ;;
        esac
    fi
    
    # httpx
    print_subsection "httpx - HTTP Toolkit"
    if check_command httpx; then
        log_skip "httpx"
    else
        log_info "Instalando httpx..."
        go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest 2>/dev/null && \
            log_success "httpx instalado" || log_error "Error instalando httpx"
    fi
    
    # ffuf
    print_subsection "ffuf - Fast Web Fuzzer"
    if check_command ffuf; then
        log_skip "ffuf"
    else
        log_info "Instalando ffuf..."
        go install github.com/ffuf/ffuf/v2@latest 2>/dev/null && \
            log_success "ffuf instalado" || log_error "Error instalando ffuf"
    fi
}

# ═══════════════════════════════════════════════════════════════════════════════
# SCA - SOFTWARE COMPOSITION ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════════

install_sca_tools() {
    print_section "📦 SCA - Software Composition Analysis"
    
    # Snyk
    print_subsection "Snyk - Dependency Vulnerability Scanner"
    if check_command snyk; then
        log_skip "Snyk"
    else
        log_info "Instalando Snyk..."
        npm install -g snyk --quiet 2>/dev/null && \
            log_success "Snyk instalado" || log_error "Error instalando Snyk"
    fi
    
    # OWASP Dependency-Check
    print_subsection "OWASP Dependency-Check"
    if [[ -f "${INSTALL_DIR}/tools/dependency-check/bin/dependency-check.sh" ]]; then
        log_skip "OWASP Dependency-Check"
    else
        log_info "Descargando OWASP Dependency-Check..."
        DC_VERSION="9.0.9"
        mkdir -p "${INSTALL_DIR}/tools/dependency-check"
        curl -sL "https://github.com/jeremylong/DependencyCheck/releases/download/v${DC_VERSION}/dependency-check-${DC_VERSION}-release.zip" \
            -o /tmp/dependency-check.zip 2>/dev/null
        unzip -q /tmp/dependency-check.zip -d "${INSTALL_DIR}/tools/" 2>/dev/null && \
            log_success "OWASP Dependency-Check instalado" || log_error "Error instalando Dependency-Check"
        rm -f /tmp/dependency-check.zip
    fi
    
    # Safety (Python)
    print_subsection "Safety - Python Dependency Checker"
    if check_command safety; then
        log_skip "Safety"
    else
        log_info "Instalando Safety..."
        pip3 install safety --quiet 2>/dev/null && \
            log_success "Safety instalado" || log_error "Error instalando Safety"
    fi
    
    # npm audit (viene con npm)
    print_subsection "npm audit - Node.js Dependency Checker"
    if check_command npm; then
        log_success "npm audit disponible (incluido con npm)"
    fi
    
    # pip-audit
    print_subsection "pip-audit - Python Pip Auditor"
    if check_command pip-audit; then
        log_skip "pip-audit"
    else
        log_info "Instalando pip-audit..."
        pip3 install pip-audit --quiet 2>/dev/null && \
            log_success "pip-audit instalado" || log_error "Error instalando pip-audit"
    fi
    
    # RetireJS
    print_subsection "RetireJS - JavaScript Library Scanner"
    if check_command retire; then
        log_skip "RetireJS"
    else
        log_info "Instalando RetireJS..."
        npm install -g retire --quiet 2>/dev/null && \
            log_success "RetireJS instalado" || log_error "Error instalando RetireJS"
    fi
}

# ═══════════════════════════════════════════════════════════════════════════════
# SECRET DETECTION
# ═══════════════════════════════════════════════════════════════════════════════

install_secret_tools() {
    print_section "🔑 Secret Detection Tools"
    
    # Gitleaks
    print_subsection "Gitleaks - Git Secret Scanner"
    if check_command gitleaks; then
        log_skip "Gitleaks"
    else
        log_info "Instalando Gitleaks..."
        case $OS in
            macos)
                brew install gitleaks 2>/dev/null && \
                    log_success "Gitleaks instalado" || log_error "Error instalando Gitleaks"
                ;;
            *)
                GITLEAKS_VERSION="8.18.2"
                curl -sL "https://github.com/gitleaks/gitleaks/releases/download/v${GITLEAKS_VERSION}/gitleaks_${GITLEAKS_VERSION}_linux_x64.tar.gz" | \
                    tar -xz -C /usr/local/bin gitleaks 2>/dev/null && \
                    log_success "Gitleaks instalado" || {
                        go install github.com/gitleaks/gitleaks/v8@latest 2>/dev/null && \
                            log_success "Gitleaks instalado (via go)" || log_error "Error instalando Gitleaks"
                    }
                ;;
        esac
    fi
    
    # TruffleHog
    print_subsection "TruffleHog - Credential Scanner"
    if check_command trufflehog; then
        log_skip "TruffleHog"
    else
        log_info "Instalando TruffleHog..."
        case $OS in
            macos)
                brew install trufflehog 2>/dev/null && \
                    log_success "TruffleHog instalado" || log_error "Error instalando TruffleHog"
                ;;
            *)
                curl -sSfL https://raw.githubusercontent.com/trufflesecurity/trufflehog/main/scripts/install.sh | sh -s -- -b /usr/local/bin 2>/dev/null && \
                    log_success "TruffleHog instalado" || log_error "Error instalando TruffleHog"
                ;;
        esac
    fi
    
    # detect-secrets
    print_subsection "detect-secrets - Yelp Secret Scanner"
    if check_command detect-secrets; then
        log_skip "detect-secrets"
    else
        log_info "Instalando detect-secrets..."
        pip3 install detect-secrets --quiet 2>/dev/null && \
            log_success "detect-secrets instalado" || log_error "Error instalando detect-secrets"
    fi
    
    # git-secrets
    print_subsection "git-secrets - AWS Secret Prevention"
    if check_command git-secrets; then
        log_skip "git-secrets"
    else
        log_info "Instalando git-secrets..."
        case $OS in
            macos)
                brew install git-secrets 2>/dev/null && \
                    log_success "git-secrets instalado" || log_error "Error instalando git-secrets"
                ;;
            debian)
                git clone https://github.com/awslabs/git-secrets.git /tmp/git-secrets 2>/dev/null
                (cd /tmp/git-secrets && $SUDO make install) 2>/dev/null && \
                    log_success "git-secrets instalado" || log_error "Error instalando git-secrets"
                rm -rf /tmp/git-secrets
                ;;
            *)
                log_warning "Instalar git-secrets manualmente"
                ;;
        esac
    fi
}

# ═══════════════════════════════════════════════════════════════════════════════
# CONTAINER SECURITY
# ═══════════════════════════════════════════════════════════════════════════════

install_container_tools() {
    print_section "🐳 Container Security Tools"
    
    # Trivy
    print_subsection "Trivy - Container Vulnerability Scanner"
    if check_command trivy; then
        log_skip "Trivy"
    else
        log_info "Instalando Trivy..."
        case $OS in
            debian)
                $SUDO apt-get install -y -qq wget apt-transport-https gnupg lsb-release 2>/dev/null
                wget -qO - https://aquasecurity.github.io/trivy-repo/deb/public.key | gpg --dearmor | $SUDO tee /usr/share/keyrings/trivy.gpg > /dev/null
                echo "deb [signed-by=/usr/share/keyrings/trivy.gpg] https://aquasecurity.github.io/trivy-repo/deb $(lsb_release -sc) main" | $SUDO tee -a /etc/apt/sources.list.d/trivy.list
                $SUDO apt-get update -qq && $SUDO apt-get install -y -qq trivy 2>/dev/null && \
                    log_success "Trivy instalado" || log_error "Error instalando Trivy"
                ;;
            macos)
                brew install trivy 2>/dev/null && \
                    log_success "Trivy instalado" || log_error "Error instalando Trivy"
                ;;
            *)
                curl -sfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh | sh -s -- -b /usr/local/bin 2>/dev/null && \
                    log_success "Trivy instalado" || log_error "Error instalando Trivy"
                ;;
        esac
    fi
    
    # Grype
    print_subsection "Grype - Container Image Vulnerability Scanner"
    if check_command grype; then
        log_skip "Grype"
    else
        log_info "Instalando Grype..."
        curl -sSfL https://raw.githubusercontent.com/anchore/grype/main/install.sh | sh -s -- -b /usr/local/bin 2>/dev/null && \
            log_success "Grype instalado" || log_error "Error instalando Grype"
    fi
    
    # Syft
    print_subsection "Syft - SBOM Generator"
    if check_command syft; then
        log_skip "Syft"
    else
        log_info "Instalando Syft..."
        curl -sSfL https://raw.githubusercontent.com/anchore/syft/main/install.sh | sh -s -- -b /usr/local/bin 2>/dev/null && \
            log_success "Syft instalado" || log_error "Error instalando Syft"
    fi
    
    # Hadolint
    print_subsection "Hadolint - Dockerfile Linter"
    if check_command hadolint; then
        log_skip "Hadolint"
    else
        log_info "Instalando Hadolint..."
        case $OS in
            macos)
                brew install hadolint 2>/dev/null && \
                    log_success "Hadolint instalado" || log_error "Error instalando Hadolint"
                ;;
            *)
                HADOLINT_VERSION="2.12.0"
                curl -sL "https://github.com/hadolint/hadolint/releases/download/v${HADOLINT_VERSION}/hadolint-Linux-x86_64" \
                    -o /usr/local/bin/hadolint 2>/dev/null
                chmod +x /usr/local/bin/hadolint && \
                    log_success "Hadolint instalado" || log_error "Error instalando Hadolint"
                ;;
        esac
    fi
    
    # Dockle
    print_subsection "Dockle - Container Image Linter"
    if check_command dockle; then
        log_skip "Dockle"
    else
        log_info "Instalando Dockle..."
        case $OS in
            macos)
                brew install goodwithtech/r/dockle 2>/dev/null && \
                    log_success "Dockle instalado" || log_error "Error instalando Dockle"
                ;;
            debian)
                DOCKLE_VERSION="0.4.14"
                curl -sL "https://github.com/goodwithtech/dockle/releases/download/v${DOCKLE_VERSION}/dockle_${DOCKLE_VERSION}_Linux-64bit.deb" \
                    -o /tmp/dockle.deb 2>/dev/null
                $SUDO dpkg -i /tmp/dockle.deb 2>/dev/null && \
                    log_success "Dockle instalado" || log_error "Error instalando Dockle"
                rm -f /tmp/dockle.deb
                ;;
            *)
                log_warning "Instalar Dockle manualmente"
                ;;
        esac
    fi
}

# ═══════════════════════════════════════════════════════════════════════════════
# IaC SECURITY
# ═══════════════════════════════════════════════════════════════════════════════

install_iac_tools() {
    print_section "🏗️ Infrastructure as Code Security"
    
    # Checkov
    print_subsection "Checkov - IaC Scanner"
    if check_command checkov; then
        log_skip "Checkov"
    else
        log_info "Instalando Checkov..."
        pip3 install checkov --quiet 2>/dev/null && \
            log_success "Checkov instalado" || log_error "Error instalando Checkov"
    fi
    
    # tfsec
    print_subsection "tfsec - Terraform Security Scanner"
    if check_command tfsec; then
        log_skip "tfsec"
    else
        log_info "Instalando tfsec..."
        case $OS in
            macos)
                brew install tfsec 2>/dev/null && \
                    log_success "tfsec instalado" || log_error "Error instalando tfsec"
                ;;
            *)
                go install github.com/aquasecurity/tfsec/cmd/tfsec@latest 2>/dev/null && \
                    log_success "tfsec instalado" || log_error "Error instalando tfsec"
                ;;
        esac
    fi
    
    # KICS
    print_subsection "KICS - Keeping Infrastructure as Code Secure"
    if check_command kics; then
        log_skip "KICS"
    else
        log_info "Instalando KICS..."
        case $OS in
            macos)
                brew install kics 2>/dev/null && \
                    log_success "KICS instalado" || log_error "Error instalando KICS"
                ;;
            *)
                KICS_VERSION="2.0.0"
                curl -sL "https://github.com/Checkmarx/kics/releases/download/v${KICS_VERSION}/kics_${KICS_VERSION}_linux_x64.tar.gz" | \
                    tar -xz -C /usr/local/bin kics 2>/dev/null && \
                    log_success "KICS instalado" || log_error "Error instalando KICS"
                ;;
        esac
    fi
    
    # Terrascan
    print_subsection "Terrascan - Compliance as Code"
    if check_command terrascan; then
        log_skip "Terrascan"
    else
        log_info "Instalando Terrascan..."
        curl -L "$(curl -s https://api.github.com/repos/tenable/terrascan/releases/latest | grep -o -E "https://.+?_Linux_x86_64.tar.gz")" | \
            tar -xz -C /usr/local/bin terrascan 2>/dev/null && \
            log_success "Terrascan instalado" || log_error "Error instalando Terrascan"
    fi
    
    # Terraform
    print_subsection "Terraform - IaC Tool"
    if check_command terraform; then
        log_skip "Terraform"
    else
        log_info "Instalando Terraform..."
        case $OS in
            macos)
                brew install terraform 2>/dev/null && \
                    log_success "Terraform instalado" || log_error "Error instalando Terraform"
                ;;
            debian)
                wget -O- https://apt.releases.hashicorp.com/gpg | gpg --dearmor | $SUDO tee /usr/share/keyrings/hashicorp-archive-keyring.gpg > /dev/null
                echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | $SUDO tee /etc/apt/sources.list.d/hashicorp.list
                $SUDO apt-get update -qq && $SUDO apt-get install -y -qq terraform 2>/dev/null && \
                    log_success "Terraform instalado" || log_error "Error instalando Terraform"
                ;;
            *)
                log_warning "Instalar Terraform manualmente"
                ;;
        esac
    fi
}

# ═══════════════════════════════════════════════════════════════════════════════
# API SECURITY TOOLS
# ═══════════════════════════════════════════════════════════════════════════════

install_api_tools() {
    print_section "🔌 API Security Tools"
    
    # Postman CLI (Newman)
    print_subsection "Newman - Postman CLI"
    if check_command newman; then
        log_skip "Newman"
    else
        log_info "Instalando Newman..."
        npm install -g newman --quiet 2>/dev/null && \
            log_success "Newman instalado" || log_error "Error instalando Newman"
    fi
    
    # HTTPie
    print_subsection "HTTPie - HTTP Client"
    if check_command http; then
        log_skip "HTTPie"
    else
        log_info "Instalando HTTPie..."
        pip3 install httpie --quiet 2>/dev/null && \
            log_success "HTTPie instalado" || log_error "Error instalando HTTPie"
    fi
    
    # jwt-cli
    print_subsection "jwt-cli - JWT Decoder"
    if check_command jwt; then
        log_skip "jwt-cli"
    else
        log_info "Instalando jwt-cli..."
        npm install -g jwt-cli --quiet 2>/dev/null && \
            log_success "jwt-cli instalado" || log_error "Error instalando jwt-cli"
    fi
    
    # Insomnia CLI (Inso)
    print_subsection "Inso - Insomnia CLI"
    if check_command inso; then
        log_skip "Inso"
    else
        log_info "Instalando Inso..."
        npm install -g insomnia-inso --quiet 2>/dev/null && \
            log_success "Inso instalado" || log_error "Error instalando Inso"
    fi
}

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURACIÓN POST-INSTALACIÓN
# ═══════════════════════════════════════════════════════════════════════════════

post_install_config() {
    print_section "⚙️ Configuración Post-Instalación"
    
    # Actualizar PATH
    log_info "Configurando PATH..."
    
    GOPATH="${HOME}/go"
    GOBIN="${GOPATH}/bin"
    
    # Agregar al PATH si no existe
    if [[ ":$PATH:" != *":${GOBIN}:"* ]]; then
        echo "export PATH=\"\$PATH:${GOBIN}\"" >> ~/.bashrc
        echo "export PATH=\"\$PATH:${GOBIN}\"" >> ~/.zshrc 2>/dev/null || true
        export PATH="$PATH:${GOBIN}"
    fi
    
    # Agregar tools locales al PATH
    if [[ ":$PATH:" != *":${INSTALL_DIR}/tools:"* ]]; then
        echo "export PATH=\"\$PATH:${INSTALL_DIR}/tools/sonar-scanner/bin\"" >> ~/.bashrc
        echo "export PATH=\"\$PATH:${INSTALL_DIR}/tools/dependency-check/bin\"" >> ~/.bashrc
    fi
    
    log_success "PATH configurado"
    
    # Crear archivos de configuración
    log_info "Creando archivos de configuración..."
    
    # Gitleaks config
    cat > "${INSTALL_DIR}/secrets/.gitleaks.toml" << 'EOF'
title = "Gitleaks Configuration"

[extend]
useDefault = true

[[rules]]
id = "custom-api-key"
description = "Custom API Key Detection"
regex = '''(?i)(api[_-]?key|apikey)['":\s]*[=:]\s*['"]?([a-zA-Z0-9_-]{20,})['"]?'''
tags = ["key", "api"]

[[rules]]
id = "custom-password"
description = "Custom Password Detection"
regex = '''(?i)(password|passwd|pwd)['":\s]*[=:]\s*['"]?([^\s'"]{8,})['"]?'''
tags = ["password"]

[allowlist]
paths = [
    '''\.git/''',
    '''node_modules/''',
    '''vendor/''',
    '''\.env\.example''',
]
EOF
    
    # detect-secrets baseline
    if check_command detect-secrets; then
        (cd "${INSTALL_DIR}" && detect-secrets scan > secrets/.secrets.baseline 2>/dev/null) || true
    fi
    
    log_success "Archivos de configuración creados"
    
    # Descargar templates de Nuclei
    log_info "Descargando templates de Nuclei..."
    if check_command nuclei; then
        nuclei -update-templates -silent 2>/dev/null && \
            log_success "Templates de Nuclei actualizados" || log_warning "No se pudieron actualizar templates de Nuclei"
    fi
    
    # Actualizar base de datos de Trivy
    log_info "Actualizando base de datos de Trivy..."
    if check_command trivy; then
        trivy image --download-db-only 2>/dev/null && \
            log_success "Base de datos de Trivy actualizada" || log_warning "No se pudo actualizar base de datos de Trivy"
    fi
}

# ═══════════════════════════════════════════════════════════════════════════════
# VERIFICACIÓN DE INSTALACIÓN
# ═══════════════════════════════════════════════════════════════════════════════

verify_installation() {
    print_section "✅ Verificación de Instalación"
    
    echo -e "\n${BOLD}Herramientas SAST:${NC}"
    check_command semgrep && echo -e "  ${GREEN}✓${NC} Semgrep" || echo -e "  ${RED}✗${NC} Semgrep"
    check_command bandit && echo -e "  ${GREEN}✓${NC} Bandit" || echo -e "  ${RED}✗${NC} Bandit"
    check_command eslint && echo -e "  ${GREEN}✓${NC} ESLint" || echo -e "  ${RED}✗${NC} ESLint"
    check_command gosec && echo -e "  ${GREEN}✓${NC} Gosec" || echo -e "  ${RED}✗${NC} Gosec"
    
    echo -e "\n${BOLD}Herramientas DAST:${NC}"
    (check_command zap.sh || check_command zaproxy) && echo -e "  ${GREEN}✓${NC} OWASP ZAP" || echo -e "  ${RED}✗${NC} OWASP ZAP"
    check_command nuclei && echo -e "  ${GREEN}✓${NC} Nuclei" || echo -e "  ${RED}✗${NC} Nuclei"
    check_command nikto && echo -e "  ${GREEN}✓${NC} Nikto" || echo -e "  ${RED}✗${NC} Nikto"
    
    echo -e "\n${BOLD}Herramientas SCA:${NC}"
    check_command snyk && echo -e "  ${GREEN}✓${NC} Snyk" || echo -e "  ${RED}✗${NC} Snyk"
    check_command safety && echo -e "  ${GREEN}✓${NC} Safety" || echo -e "  ${RED}✗${NC} Safety"
    check_command retire && echo -e "  ${GREEN}✓${NC} RetireJS" || echo -e "  ${RED}✗${NC} RetireJS"
    
    echo -e "\n${BOLD}Detección de Secrets:${NC}"
    check_command gitleaks && echo -e "  ${GREEN}✓${NC} Gitleaks" || echo -e "  ${RED}✗${NC} Gitleaks"
    check_command trufflehog && echo -e "  ${GREEN}✓${NC} TruffleHog" || echo -e "  ${RED}✗${NC} TruffleHog"
    check_command detect-secrets && echo -e "  ${GREEN}✓${NC} detect-secrets" || echo -e "  ${RED}✗${NC} detect-secrets"
    
    echo -e "\n${BOLD}Seguridad de Containers:${NC}"
    check_command trivy && echo -e "  ${GREEN}✓${NC} Trivy" || echo -e "  ${RED}✗${NC} Trivy"
    check_command grype && echo -e "  ${GREEN}✓${NC} Grype" || echo -e "  ${RED}✗${NC} Grype"
    check_command hadolint && echo -e "  ${GREEN}✓${NC} Hadolint" || echo -e "  ${RED}✗${NC} Hadolint"
    
    echo -e "\n${BOLD}Seguridad IaC:${NC}"
    check_command checkov && echo -e "  ${GREEN}✓${NC} Checkov" || echo -e "  ${RED}✗${NC} Checkov"
    check_command tfsec && echo -e "  ${GREEN}✓${NC} tfsec" || echo -e "  ${RED}✗${NC} tfsec"
    check_command terrascan && echo -e "  ${GREEN}✓${NC} Terrascan" || echo -e "  ${RED}✗${NC} Terrascan"
}

# ═══════════════════════════════════════════════════════════════════════════════
# RESUMEN FINAL
# ═══════════════════════════════════════════════════════════════════════════════

print_summary() {
    print_section "📊 Resumen de Instalación"
    
    echo -e "${GREEN}╔══════════════════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║${NC}                          ${BOLD}INSTALACIÓN COMPLETADA${NC}                             ${GREEN}║${NC}"
    echo -e "${GREEN}╠══════════════════════════════════════════════════════════════════════════════╣${NC}"
    echo -e "${GREEN}║${NC}                                                                              ${GREEN}║${NC}"
    echo -e "${GREEN}║${NC}   ${GREEN}✓ Herramientas instaladas:${NC}  ${TOOLS_INSTALLED}                                         ${GREEN}║${NC}"
    echo -e "${GREEN}║${NC}   ${YELLOW}→ Herramientas omitidas:${NC}    ${TOOLS_SKIPPED}                                         ${GREEN}║${NC}"
    echo -e "${GREEN}║${NC}   ${RED}✗ Herramientas fallidas:${NC}    ${TOOLS_FAILED}                                         ${GREEN}║${NC}"
    echo -e "${GREEN}║${NC}                                                                              ${GREEN}║${NC}"
    echo -e "${GREEN}║${NC}   📁 Directorio de instalación: ${INSTALL_DIR}                ${GREEN}║${NC}"
    echo -e "${GREEN}║${NC}   📄 Log de instalación: ${LOG_FILE}                          ${GREEN}║${NC}"
    echo -e "${GREEN}║${NC}                                                                              ${GREEN}║${NC}"
    echo -e "${GREEN}╠══════════════════════════════════════════════════════════════════════════════╣${NC}"
    echo -e "${GREEN}║${NC}                           ${BOLD}PRÓXIMOS PASOS${NC}                                     ${GREEN}║${NC}"
    echo -e "${GREEN}╠══════════════════════════════════════════════════════════════════════════════╣${NC}"
    echo -e "${GREEN}║${NC}                                                                              ${GREEN}║${NC}"
    echo -e "${GREEN}║${NC}   1. Reiniciar terminal o ejecutar: source ~/.bashrc                        ${GREEN}║${NC}"
    echo -e "${GREEN}║${NC}   2. Configurar Snyk: snyk auth                                              ${GREEN}║${NC}"
    echo -e "${GREEN}║${NC}   3. Configurar SonarQube (opcional): Editar sonar-project.properties        ${GREEN}║${NC}"
    echo -e "${GREEN}║${NC}   4. Ejecutar escaneo de prueba: ./tools/custom-scripts/secure_scan.sh .     ${GREEN}║${NC}"
    echo -e "${GREEN}║${NC}                                                                              ${GREEN}║${NC}"
    echo -e "${GREEN}╚══════════════════════════════════════════════════════════════════════════════╝${NC}"
    echo ""
}

# ═══════════════════════════════════════════════════════════════════════════════
# MENÚ PRINCIPAL
# ═══════════════════════════════════════════════════════════════════════════════

show_menu() {
    echo -e "\n${CYAN}Seleccione una opción:${NC}\n"
    echo -e "  ${WHITE}1)${NC} Instalación completa (todas las herramientas)"
    echo -e "  ${WHITE}2)${NC} Solo SAST"
    echo -e "  ${WHITE}3)${NC} Solo DAST"
    echo -e "  ${WHITE}4)${NC} Solo SCA"
    echo -e "  ${WHITE}5)${NC} Solo Secret Detection"
    echo -e "  ${WHITE}6)${NC} Solo Container Security"
    echo -e "  ${WHITE}7)${NC} Solo IaC Security"
    echo -e "  ${WHITE}8)${NC} Solo API Tools"
    echo -e "  ${WHITE}9)${NC} Verificar instalación"
    echo -e "  ${WHITE}0)${NC} Salir"
    echo ""
    read -p "Opción: " choice
    
    case $choice in
        1) full_install ;;
        2) install_sast_tools && post_install_config ;;
        3) install_dast_tools && post_install_config ;;
        4) install_sca_tools && post_install_config ;;
        5) install_secret_tools && post_install_config ;;
        6) install_container_tools && post_install_config ;;
        7) install_iac_tools && post_install_config ;;
        8) install_api_tools && post_install_config ;;
        9) verify_installation ;;
        0) exit 0 ;;
        *) log_error "Opción inválida" && show_menu ;;
    esac
}

full_install() {
    install_base_dependencies
    install_sast_tools
    install_dast_tools
    install_sca_tools
    install_secret_tools
    install_container_tools
    install_iac_tools
    install_api_tools
    post_install_config
    verify_installation
    print_summary
}

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

main() {
    print_banner
    
    # Inicializar log
    echo "=== GREEN TEAM DevSecOps Installer ===" > "$LOG_FILE"
    echo "Fecha: $(date)" >> "$LOG_FILE"
    echo "=======================================" >> "$LOG_FILE"
    
    check_root
    detect_os
    
    # Verificar argumentos
    if [[ $# -eq 0 ]]; then
        show_menu
    else
        case "$1" in
            --full|-f)
                full_install
                ;;
            --sast)
                install_sast_tools
                ;;
            --dast)
                install_dast_tools
                ;;
            --sca)
                install_sca_tools
                ;;
            --secrets)
                install_secret_tools
                ;;
            --containers)
                install_container_tools
                ;;
            --iac)
                install_iac_tools
                ;;
            --api)
                install_api_tools
                ;;
            --verify|-v)
                verify_installation
                ;;
            --help|-h)
                echo "Uso: $0 [opción]"
                echo ""
                echo "Opciones:"
                echo "  --full, -f      Instalación completa"
                echo "  --sast          Solo herramientas SAST"
                echo "  --dast          Solo herramientas DAST"
                echo "  --sca           Solo herramientas SCA"
                echo "  --secrets       Solo detección de secrets"
                echo "  --containers    Solo seguridad de containers"
                echo "  --iac           Solo seguridad IaC"
                echo "  --api           Solo herramientas API"
                echo "  --verify, -v    Verificar instalación"
                echo "  --help, -h      Mostrar esta ayuda"
                ;;
            *)
                log_error "Opción desconocida: $1"
                echo "Use --help para ver las opciones disponibles"
                exit 1
                ;;
        esac
    fi
}

main "$@"
