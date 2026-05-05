#!/bin/bash

#╔══════════════════════════════════════════════════════════════════════════════╗
#║   🟢 GREEN TEAM - Secret Scanner                                            ║
#║   Detección de secrets y credenciales expuestas                             ║
#╚══════════════════════════════════════════════════════════════════════════════╝

set -e

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
PURPLE='\033[0;35m'
NC='\033[0m'
BOLD='\033[1m'

# Variables
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"
SCANS_DIR="${PROJECT_ROOT}/scans"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
REPORT_DIR="${SCANS_DIR}/secrets/${TIMESTAMP}"

# Contadores
GITLEAKS_FINDINGS=0
TRUFFLEHOG_FINDINGS=0
DETECT_SECRETS_FINDINGS=0
TOTAL_FINDINGS=0

# Crear directorio de reportes
mkdir -p "${REPORT_DIR}"

print_banner() {
    echo -e "${PURPLE}"
    echo "╔═══════════════════════════════════════════════════════════════╗"
    echo "║            🔑 GREEN TEAM - Secret Scanner                     ║"
    echo "╚═══════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

log_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[✓]${NC} $1"; }
log_warning() { echo -e "${YELLOW}[!]${NC} $1"; }
log_error() { echo -e "${RED}[✗]${NC} $1"; }
log_critical() { echo -e "${RED}${BOLD}[🚨]${NC} $1"; }

check_tool() {
    command -v "$1" &> /dev/null
}

run_gitleaks() {
    local target="$1"
    
    echo -e "\n${CYAN}┌──────────────────────────────────────────────────────────────────┐${NC}"
    echo -e "${CYAN}│${NC} ${BOLD}Gitleaks - Git Secret Scanner${NC}"
    echo -e "${CYAN}└──────────────────────────────────────────────────────────────────┘${NC}"
    
    if ! check_tool gitleaks; then
        log_warning "Gitleaks no instalado. Saltando..."
        return
    fi
    
    log_info "Ejecutando Gitleaks..."
    
    # Ejecutar gitleaks
    if gitleaks detect --source "$target" --report-format json --report-path "${REPORT_DIR}/gitleaks.json" --no-git 2>/dev/null; then
        log_success "No se encontraron secrets con Gitleaks"
    else
        # Contar findings
        if [[ -f "${REPORT_DIR}/gitleaks.json" ]]; then
            GITLEAKS_FINDINGS=$(jq 'length' "${REPORT_DIR}/gitleaks.json" 2>/dev/null || echo "0")
            if [[ "$GITLEAKS_FINDINGS" -gt 0 ]]; then
                log_critical "Gitleaks encontró ${GITLEAKS_FINDINGS} secrets!"
                
                # Mostrar resumen
                echo -e "\n${YELLOW}Secrets encontrados:${NC}"
                jq -r '.[] | "  - \(.RuleID): \(.File):\(.StartLine)"' "${REPORT_DIR}/gitleaks.json" 2>/dev/null | head -10
                
                if [[ "$GITLEAKS_FINDINGS" -gt 10 ]]; then
                    echo -e "  ${YELLOW}... y $((GITLEAKS_FINDINGS - 10)) más${NC}"
                fi
            fi
        fi
    fi
    
    # Generar reporte legible
    if [[ -f "${REPORT_DIR}/gitleaks.json" ]] && [[ "$GITLEAKS_FINDINGS" -gt 0 ]]; then
        {
            echo "# Gitleaks Report"
            echo ""
            echo "## Findings: ${GITLEAKS_FINDINGS}"
            echo ""
            jq -r '.[] | "### \(.RuleID)\n- **File:** \(.File)\n- **Line:** \(.StartLine)\n- **Secret:** \(.Secret | .[0:20])...\n"' "${REPORT_DIR}/gitleaks.json" 2>/dev/null
        } > "${REPORT_DIR}/gitleaks.md"
    fi
}

run_trufflehog() {
    local target="$1"
    
    echo -e "\n${CYAN}┌──────────────────────────────────────────────────────────────────┐${NC}"
    echo -e "${CYAN}│${NC} ${BOLD}TruffleHog - Credential Scanner${NC}"
    echo -e "${CYAN}└──────────────────────────────────────────────────────────────────┘${NC}"
    
    if ! check_tool trufflehog; then
        log_warning "TruffleHog no instalado. Saltando..."
        return
    fi
    
    log_info "Ejecutando TruffleHog..."
    
    # Ejecutar trufflehog
    trufflehog filesystem "$target" --json 2>/dev/null > "${REPORT_DIR}/trufflehog.json" || true
    
    # Contar findings
    if [[ -f "${REPORT_DIR}/trufflehog.json" ]] && [[ -s "${REPORT_DIR}/trufflehog.json" ]]; then
        TRUFFLEHOG_FINDINGS=$(wc -l < "${REPORT_DIR}/trufflehog.json" | tr -d ' ')
        
        if [[ "$TRUFFLEHOG_FINDINGS" -gt 0 ]]; then
            log_critical "TruffleHog encontró ${TRUFFLEHOG_FINDINGS} credenciales!"
            
            echo -e "\n${YELLOW}Credenciales encontradas:${NC}"
            head -5 "${REPORT_DIR}/trufflehog.json" | jq -r '"  - \(.DetectorName): \(.SourceMetadata.Data.Filesystem.file)"' 2>/dev/null || true
        else
            log_success "No se encontraron credenciales con TruffleHog"
        fi
    else
        log_success "No se encontraron credenciales con TruffleHog"
        TRUFFLEHOG_FINDINGS=0
    fi
}

run_detect_secrets() {
    local target="$1"
    
    echo -e "\n${CYAN}┌──────────────────────────────────────────────────────────────────┐${NC}"
    echo -e "${CYAN}│${NC} ${BOLD}detect-secrets - Yelp Secret Scanner${NC}"
    echo -e "${CYAN}└──────────────────────────────────────────────────────────────────┘${NC}"
    
    if ! check_tool detect-secrets; then
        log_warning "detect-secrets no instalado. Saltando..."
        return
    fi
    
    log_info "Ejecutando detect-secrets..."
    
    # Ejecutar detect-secrets
    detect-secrets scan "$target" > "${REPORT_DIR}/detect-secrets.json" 2>/dev/null || true
    
    # Contar findings
    if [[ -f "${REPORT_DIR}/detect-secrets.json" ]]; then
        DETECT_SECRETS_FINDINGS=$(jq '[.results | to_entries[] | .value | length] | add // 0' "${REPORT_DIR}/detect-secrets.json" 2>/dev/null || echo "0")
        
        if [[ "$DETECT_SECRETS_FINDINGS" -gt 0 ]]; then
            log_critical "detect-secrets encontró ${DETECT_SECRETS_FINDINGS} posibles secrets!"
            
            echo -e "\n${YELLOW}Posibles secrets:${NC}"
            jq -r '.results | to_entries[] | "  - \(.key): \(.value | length) secrets"' "${REPORT_DIR}/detect-secrets.json" 2>/dev/null | head -10
        else
            log_success "No se encontraron secrets con detect-secrets"
        fi
    fi
}

run_custom_patterns() {
    local target="$1"
    
    echo -e "\n${CYAN}┌──────────────────────────────────────────────────────────────────┐${NC}"
    echo -e "${CYAN}│${NC} ${BOLD}Custom Pattern Scanner${NC}"
    echo -e "${CYAN}└──────────────────────────────────────────────────────────────────┘${NC}"
    
    log_info "Buscando patrones personalizados..."
    
    local patterns=(
        "password\s*=\s*['\"][^'\"]+['\"]"
        "api[_-]?key\s*=\s*['\"][^'\"]+['\"]"
        "secret\s*=\s*['\"][^'\"]+['\"]"
        "token\s*=\s*['\"][^'\"]+['\"]"
        "AWS_SECRET_ACCESS_KEY"
        "PRIVATE[_-]KEY"
        "BEGIN RSA PRIVATE KEY"
        "BEGIN OPENSSH PRIVATE KEY"
        "jdbc:.*password="
        "mongodb://.*:.*@"
        "postgres://.*:.*@"
        "mysql://.*:.*@"
    )
    
    local custom_findings=0
    local custom_report="${REPORT_DIR}/custom_patterns.txt"
    
    echo "# Custom Pattern Scan Results" > "$custom_report"
    echo "# Date: $(date)" >> "$custom_report"
    echo "" >> "$custom_report"
    
    for pattern in "${patterns[@]}"; do
        local matches
        matches=$(grep -rniE "$pattern" "$target" --include="*.py" --include="*.js" --include="*.ts" --include="*.java" --include="*.go" --include="*.rb" --include="*.php" --include="*.yml" --include="*.yaml" --include="*.json" --include="*.xml" --include="*.properties" --include="*.env*" --include="*.config" 2>/dev/null | grep -v "node_modules" | grep -v ".git" || true)
        
        if [[ -n "$matches" ]]; then
            echo "## Pattern: $pattern" >> "$custom_report"
            echo "$matches" >> "$custom_report"
            echo "" >> "$custom_report"
            
            local count
            count=$(echo "$matches" | wc -l)
            custom_findings=$((custom_findings + count))
        fi
    done
    
    if [[ "$custom_findings" -gt 0 ]]; then
        log_warning "Patrones personalizados encontraron ${custom_findings} coincidencias"
    else
        log_success "No se encontraron patrones sospechosos"
    fi
}

generate_summary() {
    local target="$1"
    
    TOTAL_FINDINGS=$((GITLEAKS_FINDINGS + TRUFFLEHOG_FINDINGS + DETECT_SECRETS_FINDINGS))
    
    local summary_file="${REPORT_DIR}/summary.md"
    
    cat > "$summary_file" << EOF
# 🔑 Secret Scan Report

**Fecha:** $(date)
**Target:** ${target}
**Directorio de reportes:** ${REPORT_DIR}

## 📊 Resumen

| Herramienta | Findings |
|-------------|----------|
| Gitleaks | ${GITLEAKS_FINDINGS} |
| TruffleHog | ${TRUFFLEHOG_FINDINGS} |
| detect-secrets | ${DETECT_SECRETS_FINDINGS} |
| **Total** | **${TOTAL_FINDINGS}** |

## 🚨 Estado

EOF

    if [[ "$TOTAL_FINDINGS" -gt 0 ]]; then
        echo "**❌ SECURITY GATE: FAILED**" >> "$summary_file"
        echo "" >> "$summary_file"
        echo "Se encontraron secrets expuestos. Acción inmediata requerida:" >> "$summary_file"
        echo "" >> "$summary_file"
        echo "1. Rotar todas las credenciales comprometidas" >> "$summary_file"
        echo "2. Remover secrets del código" >> "$summary_file"
        echo "3. Usar variables de entorno o secret managers" >> "$summary_file"
        echo "4. Revisar historial de git para exposición previa" >> "$summary_file"
    else
        echo "**✅ SECURITY GATE: PASSED**" >> "$summary_file"
        echo "" >> "$summary_file"
        echo "No se encontraron secrets expuestos." >> "$summary_file"
    fi
    
    echo "" >> "$summary_file"
    echo "## 📁 Reportes Detallados" >> "$summary_file"
    echo "" >> "$summary_file"
    
    [[ -f "${REPORT_DIR}/gitleaks.json" ]] && echo "- [Gitleaks](gitleaks.json)" >> "$summary_file"
    [[ -f "${REPORT_DIR}/trufflehog.json" ]] && echo "- [TruffleHog](trufflehog.json)" >> "$summary_file"
    [[ -f "${REPORT_DIR}/detect-secrets.json" ]] && echo "- [detect-secrets](detect-secrets.json)" >> "$summary_file"
    [[ -f "${REPORT_DIR}/custom_patterns.txt" ]] && echo "- [Custom Patterns](custom_patterns.txt)" >> "$summary_file"
}

print_final_summary() {
    echo ""
    echo -e "${CYAN}═══════════════════════════════════════════════════════════════${NC}"
    echo -e "${BOLD}📊 RESUMEN FINAL${NC}"
    echo -e "${CYAN}═══════════════════════════════════════════════════════════════${NC}"
    echo ""
    echo -e "  ${PURPLE}Gitleaks:${NC}        ${GITLEAKS_FINDINGS} findings"
    echo -e "  ${PURPLE}TruffleHog:${NC}      ${TRUFFLEHOG_FINDINGS} findings"
    echo -e "  ${PURPLE}detect-secrets:${NC}  ${DETECT_SECRETS_FINDINGS} findings"
    echo -e "  ${BOLD}Total:${NC}           ${TOTAL_FINDINGS} findings"
    echo ""
    echo -e "${CYAN}───────────────────────────────────────────────────────────────${NC}"
    
    if [[ "$TOTAL_FINDINGS" -gt 0 ]]; then
        echo -e "${RED}${BOLD}❌ SECURITY GATE: FAILED${NC}"
        echo -e "${RED}   Secrets expuestos detectados. Acción inmediata requerida.${NC}"
    else
        echo -e "${GREEN}${BOLD}✅ SECURITY GATE: PASSED${NC}"
        echo -e "${GREEN}   No se encontraron secrets expuestos.${NC}"
    fi
    
    echo -e "${CYAN}───────────────────────────────────────────────────────────────${NC}"
    echo ""
    echo -e "Reportes disponibles en: ${CYAN}${REPORT_DIR}${NC}"
    echo ""
}

main() {
    print_banner
    
    local target="${1:-.}"
    target=$(realpath "$target")
    
    log_info "Target: $target"
    log_info "Reportes: ${REPORT_DIR}"
    
    # Ejecutar scanners
    run_gitleaks "$target"
    run_trufflehog "$target"
    run_detect_secrets "$target"
    run_custom_patterns "$target"
    
    # Generar resumen
    generate_summary "$target"
    
    # Mostrar resumen final
    print_final_summary
    
    # Exit code basado en findings
    if [[ "$TOTAL_FINDINGS" -gt 0 ]]; then
        exit 1
    else
        exit 0
    fi
}

main "$@"
