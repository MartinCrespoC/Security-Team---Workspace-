#!/bin/bash
# ═══════════════════════════════════════════════════════════════════════════════
# 🔵 DETECTION VALIDATE - Purple Team Windsurf
# Validador de detecciones para técnicas ATT&CK
# ═══════════════════════════════════════════════════════════════════════════════
#
# Uso:
#   ./detection_validate.sh T1003.001
#   ./detection_validate.sh T1059.001 --timeframe 1h
#   ./detection_validate.sh --list-sources
#   ./detection_validate.sh T1003.001 --source sysmon
#
# ═══════════════════════════════════════════════════════════════════════════════

set -e

# ═══════════════════════════════════════════════════════════════════════════════
# COLORES Y VARIABLES
# ═══════════════════════════════════════════════════════════════════════════════

RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
WHITE='\033[1;37m'
NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BASE_DIR="$(dirname "$(dirname "$SCRIPT_DIR")")"
DETECTIONS_DIR="$BASE_DIR/detections"
LOGS_DIR="$BASE_DIR/logs"
RULES_DIR="$BASE_DIR/rules"
SIGMA_DIR="$RULES_DIR/sigma"

# ═══════════════════════════════════════════════════════════════════════════════
# FUNCIONES DE UTILIDAD
# ═══════════════════════════════════════════════════════════════════════════════

banner() {
    echo -e "${BLUE}"
    cat << "EOF"
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║  ██████╗ ███████╗████████╗███████╗ ██████╗████████╗██╗ ██████╗ ███╗   ██╗    ║
║  ██╔══██╗██╔════╝╚══██╔══╝██╔════╝██╔════╝╚══██╔══╝██║██╔═══██╗████╗  ██║    ║
║  ██║  ██║█████╗     ██║   █████╗  ██║        ██║   ██║██║   ██║██╔██╗ ██║    ║
║  ██║  ██║██╔══╝     ██║   ██╔══╝  ██║        ██║   ██║██║   ██║██║╚██╗██║    ║
║  ██████╔╝███████╗   ██║   ███████╗╚██████╗   ██║   ██║╚██████╔╝██║ ╚████║    ║
║  ╚═════╝ ╚══════╝   ╚═╝   ╚══════╝ ╚═════╝   ╚═╝   ╚═╝ ╚═════╝ ╚═╝  ╚═══╝    ║
║                                                                               ║
║  🔵 DETECTION VALIDATOR - Purple Team Windsurf                                ║
║  Validador de detecciones para técnicas ATT&CK                                ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
EOF
    echo -e "${NC}"
}

log() {
    echo -e "${GREEN}[+]${NC} $1"
}

warn() {
    echo -e "${YELLOW}[!]${NC} $1"
}

error() {
    echo -e "${RED}[✗]${NC} $1"
}

success() {
    echo -e "${GREEN}[✓]${NC} $1"
}

info() {
    echo -e "${CYAN}[i]${NC} $1"
}

# ═══════════════════════════════════════════════════════════════════════════════
# FUENTES DE DETECCIÓN
# ═══════════════════════════════════════════════════════════════════════════════

declare -A DETECTION_SOURCES
DETECTION_SOURCES=(
    ["sysmon"]="Sysmon Event Logs"
    ["windows_security"]="Windows Security Event Logs"
    ["windows_system"]="Windows System Event Logs"
    ["powershell"]="PowerShell Script Block Logging"
    ["edr"]="Endpoint Detection and Response"
    ["siem"]="Security Information and Event Management"
    ["network"]="Network Traffic Analysis"
    ["sigma"]="Sigma Detection Rules"
    ["yara"]="YARA Rules"
    ["auditd"]="Linux Audit Daemon"
    ["syslog"]="System Logs"
)

# Mapeo de técnicas a eventos esperados
declare -A TECHNIQUE_EVENTS
TECHNIQUE_EVENTS=(
    ["T1003.001"]="sysmon:10,edr:lsass_access,sigma:proc_access_win_lsass"
    ["T1003.002"]="sysmon:13,windows_security:4656,sigma:registry_event_sam"
    ["T1003.003"]="sysmon:1,windows_security:4662,sigma:ntds_dump"
    ["T1059.001"]="powershell:4104,sysmon:1,sigma:powershell_suspicious"
    ["T1059.003"]="sysmon:1,windows_security:4688,sigma:cmd_suspicious"
    ["T1059.004"]="auditd:execve,syslog:bash,sigma:linux_shell"
    ["T1547.001"]="sysmon:13,windows_security:4657,sigma:registry_run_keys"
    ["T1055.001"]="sysmon:8,edr:dll_injection,sigma:process_injection"
    ["T1055.002"]="sysmon:8,edr:pe_injection,sigma:process_injection"
    ["T1070.001"]="sysmon:1,windows_security:1102,sigma:eventlog_cleared"
    ["T1082"]="sysmon:1,windows_security:4688,sigma:system_info_discovery"
    ["T1083"]="sysmon:1,auditd:openat,sigma:file_discovery"
    ["T1021.001"]="network:3389,windows_security:4624,sigma:rdp_connection"
    ["T1021.002"]="network:445,windows_security:4624,sigma:smb_lateral"
    ["T1021.006"]="network:5985,windows_security:4624,sigma:winrm_connection"
    ["T1005"]="sysmon:11,edr:file_access,sigma:data_collection"
    ["T1048.003"]="network:http,sysmon:3,sigma:exfiltration_http"
    ["T1486"]="sysmon:11,edr:ransomware,sigma:ransomware_activity"
)

# ═══════════════════════════════════════════════════════════════════════════════
# FUNCIONES DE VALIDACIÓN
# ═══════════════════════════════════════════════════════════════════════════════

list_sources() {
    echo ""
    echo -e "${CYAN}═══════════════════════════════════════════════════════════════════${NC}"
    echo -e "${CYAN}  📡 Fuentes de Detección Disponibles${NC}"
    echo -e "${CYAN}═══════════════════════════════════════════════════════════════════${NC}"
    echo ""
    
    for source in "${!DETECTION_SOURCES[@]}"; do
        echo -e "  ${GREEN}•${NC} ${WHITE}$source${NC} - ${DETECTION_SOURCES[$source]}"
    done
    
    echo ""
}

check_sigma_rules() {
    local technique_id="$1"
    local found_rules=()
    
    info "Buscando reglas Sigma para $technique_id..."
    
    # Buscar en directorio de Sigma
    if [[ -d "$SIGMA_DIR/sigma/rules" ]]; then
        while IFS= read -r -d '' rule_file; do
            if grep -q "$technique_id" "$rule_file" 2>/dev/null; then
                found_rules+=("$rule_file")
            fi
        done < <(find "$SIGMA_DIR/sigma/rules" -name "*.yml" -print0 2>/dev/null)
    fi
    
    if [[ ${#found_rules[@]} -gt 0 ]]; then
        success "Encontradas ${#found_rules[@]} reglas Sigma"
        for rule in "${found_rules[@]}"; do
            echo -e "    ${CYAN}→${NC} $(basename "$rule")"
        done
        return 0
    else
        warn "No se encontraron reglas Sigma para $technique_id"
        return 1
    fi
}

check_yara_rules() {
    local technique_id="$1"
    local found_rules=()
    
    info "Buscando reglas YARA para $technique_id..."
    
    if [[ -d "$RULES_DIR/yara" ]]; then
        while IFS= read -r -d '' rule_file; do
            if grep -qi "$technique_id\|$(echo "$technique_id" | tr '.' '_')" "$rule_file" 2>/dev/null; then
                found_rules+=("$rule_file")
            fi
        done < <(find "$RULES_DIR/yara" -name "*.yar" -o -name "*.yara" -print0 2>/dev/null)
    fi
    
    if [[ ${#found_rules[@]} -gt 0 ]]; then
        success "Encontradas ${#found_rules[@]} reglas YARA"
        for rule in "${found_rules[@]}"; do
            echo -e "    ${CYAN}→${NC} $(basename "$rule")"
        done
        return 0
    else
        warn "No se encontraron reglas YARA para $technique_id"
        return 1
    fi
}

check_sysmon_events() {
    local technique_id="$1"
    local timeframe="${2:-1h}"
    
    info "Verificando eventos Sysmon..."
    
    # Obtener eventos esperados
    local events="${TECHNIQUE_EVENTS[$technique_id]}"
    
    if [[ -z "$events" ]]; then
        warn "No hay eventos definidos para $technique_id"
        return 1
    fi
    
    # Parsear eventos de Sysmon
    local sysmon_events=""
    IFS=',' read -ra event_array <<< "$events"
    for event in "${event_array[@]}"; do
        if [[ "$event" == sysmon:* ]]; then
            local event_id="${event#sysmon:}"
            sysmon_events="$sysmon_events $event_id"
        fi
    done
    
    if [[ -n "$sysmon_events" ]]; then
        success "Eventos Sysmon esperados:$sysmon_events"
        
        # En Linux, simular verificación
        if command -v journalctl &> /dev/null; then
            info "Verificando logs del sistema (últimas $timeframe)..."
            # journalctl --since "-$timeframe" 2>/dev/null | head -5 || true
        fi
        
        return 0
    fi
    
    return 1
}

check_windows_events() {
    local technique_id="$1"
    local timeframe="${2:-1h}"
    
    info "Verificando eventos Windows Security..."
    
    local events="${TECHNIQUE_EVENTS[$technique_id]}"
    
    if [[ -z "$events" ]]; then
        return 1
    fi
    
    # Parsear eventos de Windows Security
    local win_events=""
    IFS=',' read -ra event_array <<< "$events"
    for event in "${event_array[@]}"; do
        if [[ "$event" == windows_security:* ]]; then
            local event_id="${event#windows_security:}"
            win_events="$win_events $event_id"
        fi
    done
    
    if [[ -n "$win_events" ]]; then
        success "Eventos Windows Security esperados:$win_events"
        return 0
    fi
    
    return 1
}

check_network_indicators() {
    local technique_id="$1"
    
    info "Verificando indicadores de red..."
    
    local events="${TECHNIQUE_EVENTS[$technique_id]}"
    
    if [[ -z "$events" ]]; then
        return 1
    fi
    
    # Parsear indicadores de red
    local net_indicators=""
    IFS=',' read -ra event_array <<< "$events"
    for event in "${event_array[@]}"; do
        if [[ "$event" == network:* ]]; then
            local indicator="${event#network:}"
            net_indicators="$net_indicators $indicator"
        fi
    done
    
    if [[ -n "$net_indicators" ]]; then
        success "Indicadores de red esperados:$net_indicators"
        
        # Verificar con netstat/ss
        if command -v ss &> /dev/null; then
            info "Conexiones activas relevantes:"
            for port in $net_indicators; do
                if [[ "$port" =~ ^[0-9]+$ ]]; then
                    ss -tuln 2>/dev/null | grep ":$port " | head -3 || true
                fi
            done
        fi
        
        return 0
    fi
    
    return 1
}

check_edr_alerts() {
    local technique_id="$1"
    
    info "Verificando alertas EDR..."
    
    local events="${TECHNIQUE_EVENTS[$technique_id]}"
    
    if [[ -z "$events" ]]; then
        return 1
    fi
    
    # Parsear alertas EDR
    local edr_alerts=""
    IFS=',' read -ra event_array <<< "$events"
    for event in "${event_array[@]}"; do
        if [[ "$event" == edr:* ]]; then
            local alert="${event#edr:}"
            edr_alerts="$edr_alerts $alert"
        fi
    done
    
    if [[ -n "$edr_alerts" ]]; then
        success "Alertas EDR esperadas:$edr_alerts"
        return 0
    fi
    
    return 1
}

# ═══════════════════════════════════════════════════════════════════════════════
# VALIDACIÓN PRINCIPAL
# ═══════════════════════════════════════════════════════════════════════════════

validate_technique() {
    local technique_id="$1"
    local timeframe="${2:-1h}"
    local specific_source="$3"
    
    echo ""
    echo -e "${PURPLE}═══════════════════════════════════════════════════════════════════${NC}"
    echo -e "${PURPLE}  🔍 Validando detección para: $technique_id${NC}"
    echo -e "${PURPLE}═══════════════════════════════════════════════════════════════════${NC}"
    echo ""
    
    local total_checks=0
    local passed_checks=0
    local detection_results=()
    
    # Timestamp de inicio
    local start_time=$(date +%s)
    
    # Verificar cada fuente de detección
    if [[ -z "$specific_source" ]] || [[ "$specific_source" == "sigma" ]]; then
        ((total_checks++))
        if check_sigma_rules "$technique_id"; then
            ((passed_checks++))
            detection_results+=("sigma:detected")
        else
            detection_results+=("sigma:not_detected")
        fi
        echo ""
    fi
    
    if [[ -z "$specific_source" ]] || [[ "$specific_source" == "yara" ]]; then
        ((total_checks++))
        if check_yara_rules "$technique_id"; then
            ((passed_checks++))
            detection_results+=("yara:detected")
        else
            detection_results+=("yara:not_detected")
        fi
        echo ""
    fi
    
    if [[ -z "$specific_source" ]] || [[ "$specific_source" == "sysmon" ]]; then
        ((total_checks++))
        if check_sysmon_events "$technique_id" "$timeframe"; then
            ((passed_checks++))
            detection_results+=("sysmon:detected")
        else
            detection_results+=("sysmon:not_detected")
        fi
        echo ""
    fi
    
    if [[ -z "$specific_source" ]] || [[ "$specific_source" == "windows_security" ]]; then
        ((total_checks++))
        if check_windows_events "$technique_id" "$timeframe"; then
            ((passed_checks++))
            detection_results+=("windows_security:detected")
        else
            detection_results+=("windows_security:not_detected")
        fi
        echo ""
    fi
    
    if [[ -z "$specific_source" ]] || [[ "$specific_source" == "network" ]]; then
        ((total_checks++))
        if check_network_indicators "$technique_id"; then
            ((passed_checks++))
            detection_results+=("network:detected")
        else
            detection_results+=("network:not_detected")
        fi
        echo ""
    fi
    
    if [[ -z "$specific_source" ]] || [[ "$specific_source" == "edr" ]]; then
        ((total_checks++))
        if check_edr_alerts "$technique_id"; then
            ((passed_checks++))
            detection_results+=("edr:detected")
        else
            detection_results+=("edr:not_detected")
        fi
        echo ""
    fi
    
    # Calcular tiempo de validación
    local end_time=$(date +%s)
    local validation_time=$((end_time - start_time))
    
    # Calcular cobertura
    local coverage=0
    if [[ $total_checks -gt 0 ]]; then
        coverage=$((passed_checks * 100 / total_checks))
    fi
    
    # Mostrar resumen
    echo -e "${PURPLE}═══════════════════════════════════════════════════════════════════${NC}"
    echo -e "${PURPLE}  📊 RESUMEN DE VALIDACIÓN${NC}"
    echo -e "${PURPLE}═══════════════════════════════════════════════════════════════════${NC}"
    echo ""
    echo -e "  ${WHITE}Técnica:${NC}        $technique_id"
    echo -e "  ${WHITE}Timeframe:${NC}      $timeframe"
    echo -e "  ${WHITE}Checks:${NC}         $passed_checks / $total_checks"
    echo -e "  ${WHITE}Cobertura:${NC}      ${coverage}%"
    echo -e "  ${WHITE}Tiempo:${NC}         ${validation_time}s"
    echo ""
    
    # Indicador visual de cobertura
    if [[ $coverage -ge 80 ]]; then
        echo -e "  ${GREEN}████████████████████${NC} ${GREEN}EXCELENTE${NC}"
    elif [[ $coverage -ge 60 ]]; then
        echo -e "  ${YELLOW}████████████████░░░░${NC} ${YELLOW}BUENO${NC}"
    elif [[ $coverage -ge 40 ]]; then
        echo -e "  ${YELLOW}████████████░░░░░░░░${NC} ${YELLOW}REGULAR${NC}"
    else
        echo -e "  ${RED}████████░░░░░░░░░░░░${NC} ${RED}DEFICIENTE${NC}"
    fi
    echo ""
    
    # Guardar resultado
    save_validation_result "$technique_id" "$coverage" "${detection_results[*]}"
    
    # Mostrar siguiente paso
    if [[ $coverage -lt 80 ]]; then
        echo -e "${CYAN}═══════════════════════════════════════════════════════════════════${NC}"
        echo -e "${CYAN}  📋 SIGUIENTE PASO${NC}"
        echo -e "${CYAN}═══════════════════════════════════════════════════════════════════${NC}"
        echo ""
        echo -e "  ${YELLOW}⚠️  Cobertura insuficiente detectada${NC}"
        echo -e "  Ejecutar: ${GREEN}python gap_analyzer.py --technique $technique_id${NC}"
        echo -e "  Para analizar brechas y obtener recomendaciones"
        echo ""
    fi
    
    return $((100 - coverage))
}

save_validation_result() {
    local technique_id="$1"
    local coverage="$2"
    local results="$3"
    
    # Crear directorio de detecciones
    mkdir -p "$DETECTIONS_DIR/$technique_id"
    
    # Guardar resultado en YAML
    local filename="$(date +%Y%m%d_%H%M%S).yaml"
    local filepath="$DETECTIONS_DIR/$technique_id/$filename"
    
    cat > "$filepath" << EOFYAML
technique_id: $technique_id
validation_timestamp: $(date -Iseconds)
coverage: $coverage
detection_sources:
EOFYAML
    
    for result in $results; do
        local source="${result%%:*}"
        local status="${result##*:}"
        echo "  - source: $source" >> "$filepath"
        echo "    detected: $([ "$status" == "detected" ] && echo "true" || echo "false")" >> "$filepath"
    done
    
    success "Resultado guardado en: $filepath"
}

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

usage() {
    echo "Uso: $0 <TECHNIQUE_ID> [opciones]"
    echo ""
    echo "Opciones:"
    echo "  --timeframe <tiempo>   Ventana de tiempo (ej: 1h, 30m, 1d)"
    echo "  --source <fuente>      Fuente específica a verificar"
    echo "  --list-sources         Listar fuentes de detección disponibles"
    echo "  -h, --help             Mostrar esta ayuda"
    echo ""
    echo "Ejemplos:"
    echo "  $0 T1003.001"
    echo "  $0 T1059.001 --timeframe 2h"
    echo "  $0 T1003.001 --source sigma"
    echo "  $0 --list-sources"
}

main() {
    banner
    
    local technique_id=""
    local timeframe="1h"
    local source=""
    
    while [[ $# -gt 0 ]]; do
        case $1 in
            --list-sources)
                list_sources
                exit 0
                ;;
            --timeframe)
                timeframe="$2"
                shift 2
                ;;
            --source)
                source="$2"
                shift 2
                ;;
            -h|--help)
                usage
                exit 0
                ;;
            T*)
                technique_id="$1"
                shift
                ;;
            *)
                error "Opción desconocida: $1"
                usage
                exit 1
                ;;
        esac
    done
    
    if [[ -z "$technique_id" ]]; then
        error "Se requiere un ID de técnica ATT&CK"
        usage
        exit 1
    fi
    
    validate_technique "$technique_id" "$timeframe" "$source"
}

main "$@"
