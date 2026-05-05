#!/bin/bash

#╔══════════════════════════════════════════════════════════════════════════════╗
#║   🟢 GREEN TEAM - Container Security Scanner                                ║
#║   Escaneo de seguridad para imágenes Docker y configuraciones              ║
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
REPORT_DIR="${SCANS_DIR}/containers/${TIMESTAMP}"

# Contadores de vulnerabilidades
CRITICAL=0
HIGH=0
MEDIUM=0
LOW=0

# Crear directorio de reportes
mkdir -p "${REPORT_DIR}"

print_banner() {
    echo -e "${CYAN}"
    echo "╔═══════════════════════════════════════════════════════════════╗"
    echo "║         🐳 GREEN TEAM - Container Security Scanner            ║"
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

run_trivy_image() {
    local image="$1"
    
    echo -e "\n${CYAN}┌──────────────────────────────────────────────────────────────────┐${NC}"
    echo -e "${CYAN}│${NC} ${BOLD}Trivy - Container Image Vulnerability Scanner${NC}"
    echo -e "${CYAN}└──────────────────────────────────────────────────────────────────┘${NC}"
    
    if ! check_tool trivy; then
        log_warning "Trivy no instalado. Saltando..."
        return
    fi
    
    log_info "Escaneando imagen: $image"
    
    # Escaneo JSON
    trivy image "$image" --format json --output "${REPORT_DIR}/trivy.json" 2>/dev/null || {
        log_error "Error escaneando imagen con Trivy"
        return
    }
    
    # Escaneo tabla
    trivy image "$image" --format table --output "${REPORT_DIR}/trivy.txt" 2>/dev/null || true
    
    # Extraer contadores
    if [[ -f "${REPORT_DIR}/trivy.json" ]]; then
        local trivy_critical trivy_high trivy_medium trivy_low
        trivy_critical=$(jq '[.Results[]?.Vulnerabilities[]? | select(.Severity=="CRITICAL")] | length' "${REPORT_DIR}/trivy.json" 2>/dev/null || echo 0)
        trivy_high=$(jq '[.Results[]?.Vulnerabilities[]? | select(.Severity=="HIGH")] | length' "${REPORT_DIR}/trivy.json" 2>/dev/null || echo 0)
        trivy_medium=$(jq '[.Results[]?.Vulnerabilities[]? | select(.Severity=="MEDIUM")] | length' "${REPORT_DIR}/trivy.json" 2>/dev/null || echo 0)
        trivy_low=$(jq '[.Results[]?.Vulnerabilities[]? | select(.Severity=="LOW")] | length' "${REPORT_DIR}/trivy.json" 2>/dev/null || echo 0)
        
        CRITICAL=$((CRITICAL + trivy_critical))
        HIGH=$((HIGH + trivy_high))
        MEDIUM=$((MEDIUM + trivy_medium))
        LOW=$((LOW + trivy_low))
        
        log_success "Trivy completado"
        echo -e "  ${RED}Críticas:${NC} $trivy_critical | ${YELLOW}Altas:${NC} $trivy_high | ${BLUE}Medias:${NC} $trivy_medium | ${CYAN}Bajas:${NC} $trivy_low"
    fi
}

run_grype() {
    local image="$1"
    
    echo -e "\n${CYAN}┌──────────────────────────────────────────────────────────────────┐${NC}"
    echo -e "${CYAN}│${NC} ${BOLD}Grype - Container Vulnerability Scanner${NC}"
    echo -e "${CYAN}└──────────────────────────────────────────────────────────────────┘${NC}"
    
    if ! check_tool grype; then
        log_warning "Grype no instalado. Saltando..."
        return
    fi
    
    log_info "Escaneando imagen: $image"
    
    # Escaneo JSON
    grype "$image" -o json > "${REPORT_DIR}/grype.json" 2>/dev/null || {
        log_error "Error escaneando imagen con Grype"
        return
    }
    
    # Escaneo tabla
    grype "$image" -o table > "${REPORT_DIR}/grype.txt" 2>/dev/null || true
    
    # Extraer contadores
    if [[ -f "${REPORT_DIR}/grype.json" ]]; then
        local grype_critical grype_high grype_medium grype_low
        grype_critical=$(jq '[.matches[]? | select(.vulnerability.severity=="Critical")] | length' "${REPORT_DIR}/grype.json" 2>/dev/null || echo 0)
        grype_high=$(jq '[.matches[]? | select(.vulnerability.severity=="High")] | length' "${REPORT_DIR}/grype.json" 2>/dev/null || echo 0)
        grype_medium=$(jq '[.matches[]? | select(.vulnerability.severity=="Medium")] | length' "${REPORT_DIR}/grype.json" 2>/dev/null || echo 0)
        grype_low=$(jq '[.matches[]? | select(.vulnerability.severity=="Low")] | length' "${REPORT_DIR}/grype.json" 2>/dev/null || echo 0)
        
        log_success "Grype completado"
        echo -e "  ${RED}Críticas:${NC} $grype_critical | ${YELLOW}Altas:${NC} $grype_high | ${BLUE}Medias:${NC} $grype_medium | ${CYAN}Bajas:${NC} $grype_low"
    fi
}

run_hadolint() {
    local dockerfile="$1"
    
    echo -e "\n${CYAN}┌──────────────────────────────────────────────────────────────────┐${NC}"
    echo -e "${CYAN}│${NC} ${BOLD}Hadolint - Dockerfile Linter${NC}"
    echo -e "${CYAN}└──────────────────────────────────────────────────────────────────┘${NC}"
    
    if ! check_tool hadolint; then
        log_warning "Hadolint no instalado. Saltando..."
        return
    fi
    
    if [[ ! -f "$dockerfile" ]]; then
        log_warning "Dockerfile no encontrado: $dockerfile"
        return
    fi
    
    log_info "Analizando Dockerfile: $dockerfile"
    
    # Escaneo JSON
    hadolint "$dockerfile" --format json > "${REPORT_DIR}/hadolint.json" 2>/dev/null || true
    
    # Escaneo texto
    hadolint "$dockerfile" > "${REPORT_DIR}/hadolint.txt" 2>/dev/null || true
    
    # Contar issues
    if [[ -f "${REPORT_DIR}/hadolint.json" ]]; then
        local hadolint_errors hadolint_warnings hadolint_info
        hadolint_errors=$(jq '[.[] | select(.level=="error")] | length' "${REPORT_DIR}/hadolint.json" 2>/dev/null || echo 0)
        hadolint_warnings=$(jq '[.[] | select(.level=="warning")] | length' "${REPORT_DIR}/hadolint.json" 2>/dev/null || echo 0)
        hadolint_info=$(jq '[.[] | select(.level=="info")] | length' "${REPORT_DIR}/hadolint.json" 2>/dev/null || echo 0)
        
        log_success "Hadolint completado"
        echo -e "  ${RED}Errores:${NC} $hadolint_errors | ${YELLOW}Warnings:${NC} $hadolint_warnings | ${BLUE}Info:${NC} $hadolint_info"
        
        # Mostrar issues principales
        if [[ "$hadolint_errors" -gt 0 ]] || [[ "$hadolint_warnings" -gt 0 ]]; then
            echo -e "\n${YELLOW}Issues encontrados:${NC}"
            jq -r '.[] | select(.level=="error" or .level=="warning") | "  - [\(.code)] \(.message)"' "${REPORT_DIR}/hadolint.json" 2>/dev/null | head -10
        fi
    fi
}

run_dockle() {
    local image="$1"
    
    echo -e "\n${CYAN}┌──────────────────────────────────────────────────────────────────┐${NC}"
    echo -e "${CYAN}│${NC} ${BOLD}Dockle - Container Image Linter${NC}"
    echo -e "${CYAN}└──────────────────────────────────────────────────────────────────┘${NC}"
    
    if ! check_tool dockle; then
        log_warning "Dockle no instalado. Saltando..."
        return
    fi
    
    log_info "Analizando imagen: $image"
    
    # Escaneo JSON
    dockle "$image" -f json -o "${REPORT_DIR}/dockle.json" 2>/dev/null || true
    
    if [[ -f "${REPORT_DIR}/dockle.json" ]]; then
        local dockle_fatal dockle_warn dockle_info
        dockle_fatal=$(jq '[.details[]? | select(.level=="FATAL")] | length' "${REPORT_DIR}/dockle.json" 2>/dev/null || echo 0)
        dockle_warn=$(jq '[.details[]? | select(.level=="WARN")] | length' "${REPORT_DIR}/dockle.json" 2>/dev/null || echo 0)
        dockle_info=$(jq '[.details[]? | select(.level=="INFO")] | length' "${REPORT_DIR}/dockle.json" 2>/dev/null || echo 0)
        
        log_success "Dockle completado"
        echo -e "  ${RED}Fatal:${NC} $dockle_fatal | ${YELLOW}Warn:${NC} $dockle_warn | ${BLUE}Info:${NC} $dockle_info"
    fi
}

run_syft() {
    local image="$1"
    
    echo -e "\n${CYAN}┌──────────────────────────────────────────────────────────────────┐${NC}"
    echo -e "${CYAN}│${NC} ${BOLD}Syft - SBOM Generator${NC}"
    echo -e "${CYAN}└──────────────────────────────────────────────────────────────────┘${NC}"
    
    if ! check_tool syft; then
        log_warning "Syft no instalado. Saltando..."
        return
    fi
    
    log_info "Generando SBOM para: $image"
    
    # Generar SBOM en diferentes formatos
    syft "$image" -o json > "${REPORT_DIR}/sbom.json" 2>/dev/null || true
    syft "$image" -o cyclonedx-json > "${REPORT_DIR}/sbom-cyclonedx.json" 2>/dev/null || true
    syft "$image" -o spdx-json > "${REPORT_DIR}/sbom-spdx.json" 2>/dev/null || true
    
    if [[ -f "${REPORT_DIR}/sbom.json" ]]; then
        local package_count
        package_count=$(jq '.artifacts | length' "${REPORT_DIR}/sbom.json" 2>/dev/null || echo 0)
        log_success "SBOM generado: $package_count paquetes identificados"
    fi
}

scan_dockerfile_dir() {
    local dir="$1"
    
    echo -e "\n${CYAN}┌──────────────────────────────────────────────────────────────────┐${NC}"
    echo -e "${CYAN}│${NC} ${BOLD}Escaneando Dockerfiles en directorio${NC}"
    echo -e "${CYAN}└──────────────────────────────────────────────────────────────────┘${NC}"
    
    local dockerfiles
    dockerfiles=$(find "$dir" -name "Dockerfile*" -o -name "*.dockerfile" 2>/dev/null)
    
    if [[ -z "$dockerfiles" ]]; then
        log_warning "No se encontraron Dockerfiles en: $dir"
        return
    fi
    
    while IFS= read -r dockerfile; do
        run_hadolint "$dockerfile"
    done <<< "$dockerfiles"
}

generate_summary() {
    local target="$1"
    local summary_file="${REPORT_DIR}/summary.md"
    
    local total=$((CRITICAL + HIGH + MEDIUM + LOW))
    
    cat > "$summary_file" << EOF
# 🐳 Container Security Scan Report

**Fecha:** $(date)
**Target:** ${target}
**Directorio de reportes:** ${REPORT_DIR}

## 📊 Resumen de Vulnerabilidades

| Severidad | Cantidad |
|-----------|----------|
| 🔴 Crítica | ${CRITICAL} |
| 🟠 Alta | ${HIGH} |
| 🟡 Media | ${MEDIUM} |
| 🔵 Baja | ${LOW} |
| **Total** | **${total}** |

## 🚨 Estado del Security Gate

EOF

    if [[ "$CRITICAL" -gt 0 ]]; then
        echo "**❌ FAILED** - Vulnerabilidades críticas encontradas" >> "$summary_file"
    elif [[ "$HIGH" -gt 5 ]]; then
        echo "**⚠️ WARNING** - Demasiadas vulnerabilidades altas" >> "$summary_file"
    else
        echo "**✅ PASSED**" >> "$summary_file"
    fi
    
    cat >> "$summary_file" << EOF

## 📁 Reportes Generados

| Herramienta | Archivo |
|-------------|---------|
EOF

    [[ -f "${REPORT_DIR}/trivy.json" ]] && echo "| Trivy | trivy.json |" >> "$summary_file"
    [[ -f "${REPORT_DIR}/grype.json" ]] && echo "| Grype | grype.json |" >> "$summary_file"
    [[ -f "${REPORT_DIR}/hadolint.json" ]] && echo "| Hadolint | hadolint.json |" >> "$summary_file"
    [[ -f "${REPORT_DIR}/dockle.json" ]] && echo "| Dockle | dockle.json |" >> "$summary_file"
    [[ -f "${REPORT_DIR}/sbom.json" ]] && echo "| Syft SBOM | sbom.json |" >> "$summary_file"
    
    cat >> "$summary_file" << EOF

## 🛠️ Recomendaciones

1. **Actualizar imagen base** a la última versión con parches de seguridad
2. **Usar imágenes distroless** o alpine para reducir superficie de ataque
3. **No ejecutar como root** - usar USER en Dockerfile
4. **Escanear regularmente** en CI/CD pipeline
5. **Mantener SBOM actualizado** para trazabilidad

EOF
}

print_final_summary() {
    local total=$((CRITICAL + HIGH + MEDIUM + LOW))
    
    echo ""
    echo -e "${CYAN}═══════════════════════════════════════════════════════════════${NC}"
    echo -e "${BOLD}📊 RESUMEN FINAL${NC}"
    echo -e "${CYAN}═══════════════════════════════════════════════════════════════${NC}"
    echo ""
    echo -e "  ${RED}🔴 Críticas:${NC}  ${CRITICAL}"
    echo -e "  ${YELLOW}🟠 Altas:${NC}     ${HIGH}"
    echo -e "  ${BLUE}🟡 Medias:${NC}    ${MEDIUM}"
    echo -e "  ${CYAN}🔵 Bajas:${NC}     ${LOW}"
    echo -e "  ${BOLD}📦 Total:${NC}     ${total}"
    echo ""
    echo -e "${CYAN}───────────────────────────────────────────────────────────────${NC}"
    
    if [[ "$CRITICAL" -gt 0 ]]; then
        echo -e "${RED}${BOLD}❌ SECURITY GATE: FAILED${NC}"
        echo -e "${RED}   Vulnerabilidades críticas encontradas.${NC}"
    elif [[ "$HIGH" -gt 5 ]]; then
        echo -e "${YELLOW}${BOLD}⚠️ SECURITY GATE: WARNING${NC}"
        echo -e "${YELLOW}   Demasiadas vulnerabilidades altas.${NC}"
    else
        echo -e "${GREEN}${BOLD}✅ SECURITY GATE: PASSED${NC}"
    fi
    
    echo -e "${CYAN}───────────────────────────────────────────────────────────────${NC}"
    echo ""
    echo -e "Reportes disponibles en: ${CYAN}${REPORT_DIR}${NC}"
    echo ""
}

usage() {
    echo "Uso: $0 [opciones] <imagen|directorio>"
    echo ""
    echo "Opciones:"
    echo "  -i, --image <nombre>     Escanear imagen Docker"
    echo "  -d, --dir <directorio>   Escanear Dockerfiles en directorio"
    echo "  -f, --dockerfile <path>  Escanear Dockerfile específico"
    echo "  -s, --sbom               Generar SBOM"
    echo "  -h, --help               Mostrar esta ayuda"
    echo ""
    echo "Ejemplos:"
    echo "  $0 -i nginx:latest"
    echo "  $0 -d ./docker"
    echo "  $0 -f Dockerfile"
}

main() {
    print_banner
    
    local image=""
    local dir=""
    local dockerfile=""
    local generate_sbom=false
    
    # Parsear argumentos
    while [[ $# -gt 0 ]]; do
        case "$1" in
            -i|--image)
                image="$2"
                shift 2
                ;;
            -d|--dir)
                dir="$2"
                shift 2
                ;;
            -f|--dockerfile)
                dockerfile="$2"
                shift 2
                ;;
            -s|--sbom)
                generate_sbom=true
                shift
                ;;
            -h|--help)
                usage
                exit 0
                ;;
            *)
                # Si no hay flag, asumir que es una imagen
                if [[ -z "$image" ]]; then
                    image="$1"
                fi
                shift
                ;;
        esac
    done
    
    # Validar entrada
    if [[ -z "$image" ]] && [[ -z "$dir" ]] && [[ -z "$dockerfile" ]]; then
        log_error "Debe especificar una imagen, directorio o Dockerfile"
        usage
        exit 1
    fi
    
    log_info "Reportes: ${REPORT_DIR}"
    
    # Ejecutar escaneos según entrada
    if [[ -n "$image" ]]; then
        log_info "Escaneando imagen: $image"
        run_trivy_image "$image"
        run_grype "$image"
        run_dockle "$image"
        
        if [[ "$generate_sbom" == true ]]; then
            run_syft "$image"
        fi
    fi
    
    if [[ -n "$dir" ]]; then
        scan_dockerfile_dir "$dir"
    fi
    
    if [[ -n "$dockerfile" ]]; then
        run_hadolint "$dockerfile"
    fi
    
    # Generar resumen
    generate_summary "${image:-${dir:-$dockerfile}}"
    
    # Mostrar resumen final
    print_final_summary
    
    # Exit code basado en vulnerabilidades críticas
    if [[ "$CRITICAL" -gt 0 ]]; then
        exit 1
    else
        exit 0
    fi
}

main "$@"
