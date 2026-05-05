#!/bin/bash

#╔══════════════════════════════════════════════════════════════════════════════╗
#║   🟢 GREEN TEAM - Secure Code Scanner                                       ║
#║   Escaneo completo de seguridad de código fuente                            ║
#╚══════════════════════════════════════════════════════════════════════════════╝

set -e

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'
BOLD='\033[1m'

# Variables
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"
SCANS_DIR="${PROJECT_ROOT}/scans"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
REPORT_DIR="${SCANS_DIR}/sast/${TIMESTAMP}"

# Crear directorio de reportes
mkdir -p "${REPORT_DIR}"

print_banner() {
    echo -e "${GREEN}"
    echo "╔═══════════════════════════════════════════════════════════════╗"
    echo "║          🔍 GREEN TEAM - Secure Code Scanner                  ║"
    echo "╚═══════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

log_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[✓]${NC} $1"; }
log_warning() { echo -e "${YELLOW}[!]${NC} $1"; }
log_error() { echo -e "${RED}[✗]${NC} $1"; }

check_tool() {
    command -v "$1" &> /dev/null
}

detect_languages() {
    local target="$1"
    local languages=()
    
    [[ -n $(find "$target" -name "*.py" 2>/dev/null | head -1) ]] && languages+=("python")
    [[ -n $(find "$target" -name "*.js" -o -name "*.ts" 2>/dev/null | head -1) ]] && languages+=("javascript")
    [[ -n $(find "$target" -name "*.java" 2>/dev/null | head -1) ]] && languages+=("java")
    [[ -n $(find "$target" -name "*.go" 2>/dev/null | head -1) ]] && languages+=("go")
    [[ -n $(find "$target" -name "*.rb" 2>/dev/null | head -1) ]] && languages+=("ruby")
    [[ -n $(find "$target" -name "*.php" 2>/dev/null | head -1) ]] && languages+=("php")
    
    echo "${languages[@]}"
}

run_semgrep() {
    local target="$1"
    log_info "Ejecutando Semgrep..."
    
    if check_tool semgrep; then
        semgrep scan --config auto "$target" --json > "${REPORT_DIR}/semgrep.json" 2>/dev/null || true
        semgrep scan --config auto "$target" > "${REPORT_DIR}/semgrep.txt" 2>/dev/null || true
        log_success "Semgrep completado"
    else
        log_warning "Semgrep no instalado"
    fi
}

run_bandit() {
    local target="$1"
    log_info "Ejecutando Bandit (Python)..."
    
    if check_tool bandit; then
        bandit -r "$target" -f json -o "${REPORT_DIR}/bandit.json" 2>/dev/null || true
        bandit -r "$target" -f txt -o "${REPORT_DIR}/bandit.txt" 2>/dev/null || true
        log_success "Bandit completado"
    else
        log_warning "Bandit no instalado"
    fi
}

run_eslint() {
    local target="$1"
    log_info "Ejecutando ESLint Security..."
    
    if check_tool eslint; then
        eslint "$target" --ext .js,.ts,.jsx,.tsx -f json > "${REPORT_DIR}/eslint.json" 2>/dev/null || true
        log_success "ESLint completado"
    else
        log_warning "ESLint no instalado"
    fi
}

run_gosec() {
    local target="$1"
    log_info "Ejecutando Gosec (Go)..."
    
    if check_tool gosec; then
        gosec -fmt=json -out="${REPORT_DIR}/gosec.json" "$target/..." 2>/dev/null || true
        log_success "Gosec completado"
    else
        log_warning "Gosec no instalado"
    fi
}

generate_summary() {
    local report_file="${REPORT_DIR}/summary.md"
    
    cat > "$report_file" << EOF
# 🔍 Security Scan Report

**Fecha:** $(date)
**Target:** $1
**Directorio de reportes:** ${REPORT_DIR}

## Herramientas Ejecutadas

| Herramienta | Estado | Reporte |
|-------------|--------|---------|
EOF

    [[ -f "${REPORT_DIR}/semgrep.json" ]] && echo "| Semgrep | ✅ | semgrep.json |" >> "$report_file"
    [[ -f "${REPORT_DIR}/bandit.json" ]] && echo "| Bandit | ✅ | bandit.json |" >> "$report_file"
    [[ -f "${REPORT_DIR}/eslint.json" ]] && echo "| ESLint | ✅ | eslint.json |" >> "$report_file"
    [[ -f "${REPORT_DIR}/gosec.json" ]] && echo "| Gosec | ✅ | gosec.json |" >> "$report_file"

    echo "" >> "$report_file"
    echo "## Próximos Pasos" >> "$report_file"
    echo "1. Revisar vulnerabilidades críticas" >> "$report_file"
    echo "2. Aplicar fixes sugeridos" >> "$report_file"
    echo "3. Re-escanear después de correcciones" >> "$report_file"
    
    log_success "Resumen generado: $report_file"
}

main() {
    print_banner
    
    local target="${1:-.}"
    target=$(realpath "$target")
    
    log_info "Target: $target"
    log_info "Reportes: ${REPORT_DIR}"
    
    # Detectar lenguajes
    local languages=$(detect_languages "$target")
    log_info "Lenguajes detectados: $languages"
    
    echo ""
    echo -e "${CYAN}═══════════════════════════════════════════════════════════════${NC}"
    echo -e "${BOLD}Ejecutando escaneos de seguridad...${NC}"
    echo -e "${CYAN}═══════════════════════════════════════════════════════════════${NC}"
    echo ""
    
    # Ejecutar scanners
    run_semgrep "$target"
    
    [[ "$languages" == *"python"* ]] && run_bandit "$target"
    [[ "$languages" == *"javascript"* ]] && run_eslint "$target"
    [[ "$languages" == *"go"* ]] && run_gosec "$target"
    
    echo ""
    generate_summary "$target"
    
    echo ""
    echo -e "${GREEN}╔═══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║              ✅ Escaneo completado                            ║${NC}"
    echo -e "${GREEN}╚═══════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "Reportes disponibles en: ${CYAN}${REPORT_DIR}${NC}"
}

main "$@"
