#!/bin/bash
#═══════════════════════════════════════════════════════════════════════════════
#  🛡️ SECURITY TEAM UNIFIED INSTALLER
#  Red • Blue • Purple • Green • White • Yellow • Orange
#═══════════════════════════════════════════════════════════════════════════════
#  Un solo script para instalar y configurar todos los equipos de seguridad
#  con contextos aislados que pueden comunicarse entre sí.
#═══════════════════════════════════════════════════════════════════════════════

set -e

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
ORANGE='\033[0;33m'
NC='\033[0m'

# Variables globales
WORKSPACE_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_FILE="$WORKSPACE_ROOT/install.log"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

# Banner principal
print_banner() {
    clear
    echo -e "${PURPLE}"
    cat << "EOF"
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║   ███████╗███████╗ ██████╗██╗   ██╗██████╗ ██╗████████╗██╗   ██╗             ║
║   ██╔════╝██╔════╝██╔════╝██║   ██║██╔══██╗██║╚══██╔══╝╚██╗ ██╔╝             ║
║   ███████╗█████╗  ██║     ██║   ██║██████╔╝██║   ██║    ╚████╔╝              ║
║   ╚════██║██╔══╝  ██║     ██║   ██║██╔══██╗██║   ██║     ╚██╔╝               ║
║   ███████║███████╗╚██████╗╚██████╔╝██║  ██║██║   ██║      ██║                ║
║   ╚══════╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝   ╚═╝      ╚═╝                ║
║                                                                               ║
║   ████████╗███████╗ █████╗ ███╗   ███╗    ██╗   ██╗███╗   ██╗██╗███████╗    ║
║   ╚══██╔══╝██╔════╝██╔══██╗████╗ ████║    ██║   ██║████╗  ██║██║██╔════╝    ║
║      ██║   █████╗  ███████║██╔████╔██║    ██║   ██║██╔██╗ ██║██║█████╗      ║
║      ██║   ██╔══╝  ██╔══██║██║╚██╔╝██║    ██║   ██║██║╚██╗██║██║██╔══╝      ║
║      ██║   ███████╗██║  ██║██║ ╚═╝ ██║    ╚██████╔╝██║ ╚████║██║██║         ║
║      ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝     ╚═════╝ ╚═╝  ╚═══╝╚═╝╚═╝         ║
║                                                                               ║
║   🔴 Red   🔵 Blue   🟣 Purple   🟢 Green   ⚪ White   🟡 Yellow   🟠 Orange  ║
║                                                                               ║
║                    UNIFIED CYBERSECURITY WORKSPACE                            ║
║                       Powered by Windsurf AI                                  ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
EOF
    echo -e "${NC}"
}

# Funciones de logging
log() { echo -e "${CYAN}[*]${NC} $1" | tee -a "$LOG_FILE"; }
success() { echo -e "${GREEN}[✓]${NC} $1" | tee -a "$LOG_FILE"; }
warning() { echo -e "${YELLOW}[!]${NC} $1" | tee -a "$LOG_FILE"; }
error() { echo -e "${RED}[✗]${NC} $1" | tee -a "$LOG_FILE"; }

section() {
    echo "" | tee -a "$LOG_FILE"
    echo -e "${PURPLE}═══════════════════════════════════════════════════════════════════${NC}" | tee -a "$LOG_FILE"
    echo -e "${WHITE}  $1${NC}" | tee -a "$LOG_FILE"
    echo -e "${PURPLE}═══════════════════════════════════════════════════════════════════${NC}" | tee -a "$LOG_FILE"
    echo "" | tee -a "$LOG_FILE"
}

# Verificar root
check_root() {
    if [[ $EUID -ne 0 ]]; then
        error "Este script debe ejecutarse como root"
        echo -e "Ejecuta: ${CYAN}sudo $0${NC}"
        exit 1
    fi
}

# Detectar OS
detect_os() {
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        OS=$NAME
        log "Sistema detectado: $OS"
    fi
}

#═══════════════════════════════════════════════════════════════════════════════
# FASE 1: ACTUALIZACIÓN DEL SISTEMA
#═══════════════════════════════════════════════════════════════════════════════
update_system() {
    section "📦 FASE 1: ACTUALIZACIÓN DEL SISTEMA"
    log "Actualizando repositorios..."
    apt-get update -qq
    apt-get upgrade -y -qq
    success "Sistema actualizado"
}

#═══════════════════════════════════════════════════════════════════════════════
# FASE 2: DEPENDENCIAS BASE
#═══════════════════════════════════════════════════════════════════════════════
install_base_deps() {
    section "🔧 FASE 2: DEPENDENCIAS BASE"
    
    log "Instalando dependencias esenciales..."
    apt-get install -y -qq \
        curl wget git vim nano htop tmux screen \
        jq yq tree unzip p7zip-full \
        build-essential cmake pkg-config \
        libssl-dev libffi-dev \
        python3 python3-pip python3-venv python3-dev \
        golang-go ruby ruby-dev \
        nodejs npm \
        default-jdk \
        docker.io docker-compose \
        apt-transport-https ca-certificates gnupg lsb-release \
        software-properties-common \
        2>/dev/null || warning "Algunas dependencias no se pudieron instalar"
    
    # Habilitar Docker
    systemctl enable docker 2>/dev/null || true
    systemctl start docker 2>/dev/null || true
    
    success "Dependencias base instaladas"
}

#═══════════════════════════════════════════════════════════════════════════════
# FASE 3: INSTALAR EQUIPOS INDIVIDUALES
#═══════════════════════════════════════════════════════════════════════════════
install_team() {
    local team=$1
    local color=$2
    local team_dir="$WORKSPACE_ROOT/$team"
    
    echo -e "\n${color}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${color}  Instalando: $team${NC}"
    echo -e "${color}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    
    if [[ -d "$team_dir" ]]; then
        cd "$team_dir"
        
        # Crear entorno virtual Python para cada equipo
        if [[ ! -d "venv" ]]; then
            log "Creando entorno virtual para $team..."
            python3 -m venv venv
        fi
        
        # Instalar requirements si existe
        if [[ -f "requirements.txt" ]]; then
            log "Instalando dependencias Python de $team..."
            source venv/bin/activate
            pip install --upgrade pip -q
            pip install -r requirements.txt -q 2>/dev/null || true
            deactivate
        fi
        
        # Crear directorios de contexto
        mkdir -p contexts projects logs
        
        success "$team configurado"
        cd "$WORKSPACE_ROOT"
    else
        warning "Directorio $team no encontrado"
    fi
}

install_all_teams() {
    section "🛡️ FASE 3: INSTALANDO TODOS LOS EQUIPOS"
    
    install_team "RedTeam" "$RED"
    install_team "BlueTeam" "$BLUE"
    install_team "PurpleTeam" "$PURPLE"
    install_team "GreenTeam" "$GREEN"
    install_team "WhiteTeam" "$WHITE"
    install_team "YellowTeam" "$YELLOW"
    install_team "OrangeTeam" "$ORANGE"
    
    success "Todos los equipos instalados"
}

#═══════════════════════════════════════════════════════════════════════════════
# FASE 4: SISTEMA DE CONTEXTOS AISLADOS
#═══════════════════════════════════════════════════════════════════════════════
create_context_system() {
    section "🔐 FASE 4: SISTEMA DE CONTEXTOS AISLADOS"
    
    local contexts_dir="$WORKSPACE_ROOT/.contexts"
    mkdir -p "$contexts_dir"
    
    log "Creando sistema de gestión de contextos..."
    
    # Crear archivo de configuración de contextos
    cat > "$contexts_dir/config.json" << 'CTXCONFIG'
{
    "version": "1.0.0",
    "workspace_root": "/home/xroot/Documents/SecurityTeam Workspace",
    "teams": {
        "RedTeam": {
            "color": "red",
            "emoji": "🔴",
            "role": "Offensive Security",
            "capabilities": ["exploitation", "reconnaissance", "post-exploitation", "social-engineering"],
            "can_communicate_with": ["PurpleTeam", "BlueTeam"]
        },
        "BlueTeam": {
            "color": "blue",
            "emoji": "🔵",
            "role": "Defensive Security",
            "capabilities": ["detection", "response", "forensics", "monitoring", "threat-intel"],
            "can_communicate_with": ["PurpleTeam", "RedTeam", "GreenTeam"]
        },
        "PurpleTeam": {
            "color": "purple",
            "emoji": "🟣",
            "role": "Security Validation",
            "capabilities": ["attack-simulation", "detection-validation", "gap-analysis"],
            "can_communicate_with": ["RedTeam", "BlueTeam", "WhiteTeam"]
        },
        "GreenTeam": {
            "color": "green",
            "emoji": "🟢",
            "role": "DevSecOps",
            "capabilities": ["sast", "dast", "sca", "container-security", "iac-security"],
            "can_communicate_with": ["BlueTeam", "YellowTeam"]
        },
        "WhiteTeam": {
            "color": "white",
            "emoji": "⚪",
            "role": "GRC",
            "capabilities": ["governance", "risk-management", "compliance", "audit"],
            "can_communicate_with": ["PurpleTeam", "YellowTeam", "OrangeTeam"]
        },
        "YellowTeam": {
            "color": "yellow",
            "emoji": "🟡",
            "role": "Security Architecture",
            "capabilities": ["threat-modeling", "architecture-review", "security-requirements"],
            "can_communicate_with": ["GreenTeam", "WhiteTeam"]
        },
        "OrangeTeam": {
            "color": "orange",
            "emoji": "🟠",
            "role": "Security Awareness",
            "capabilities": ["phishing-simulation", "training", "metrics", "awareness-campaigns"],
            "can_communicate_with": ["WhiteTeam", "BlueTeam"]
        }
    },
    "isolation": {
        "enabled": true,
        "share_findings": true,
        "audit_communications": true
    }
}
CTXCONFIG

    success "Configuración de contextos creada"
    
    # Crear script de gestión de contextos
    cat > "$WORKSPACE_ROOT/secteam" << 'SECTEAM'
#!/bin/bash
#═══════════════════════════════════════════════════════════════════════════════
#  🛡️ SECURITY TEAM ORCHESTRATOR
#  Gestiona contextos aislados y comunicación entre equipos
#═══════════════════════════════════════════════════════════════════════════════

WORKSPACE_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONTEXTS_DIR="$WORKSPACE_ROOT/.contexts"
PROJECTS_DIR="$WORKSPACE_ROOT/.projects"
CURRENT_CONTEXT=""

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
ORANGE='\033[0;33m'
NC='\033[0m'

# Mostrar ayuda
show_help() {
    echo -e "${PURPLE}"
    cat << "BANNER"
╔═══════════════════════════════════════════════════════════════════════════════╗
║   🛡️ SECURITY TEAM ORCHESTRATOR - Comandos Disponibles                       ║
╚═══════════════════════════════════════════════════════════════════════════════╝
BANNER
    echo -e "${NC}"
    echo -e "${CYAN}Gestión de Proyectos:${NC}"
    echo -e "  ${GREEN}secteam new <nombre>${NC}     - Crear nuevo proyecto con contextos aislados"
    echo -e "  ${GREEN}secteam list${NC}             - Listar todos los proyectos"
    echo -e "  ${GREEN}secteam use <proyecto>${NC}   - Activar contexto de un proyecto"
    echo -e "  ${GREEN}secteam status${NC}           - Ver estado actual"
    echo ""
    echo -e "${CYAN}Activar Equipos:${NC}"
    echo -e "  ${RED}secteam red${NC}              - Activar contexto Red Team"
    echo -e "  ${BLUE}secteam blue${NC}             - Activar contexto Blue Team"
    echo -e "  ${PURPLE}secteam purple${NC}           - Activar contexto Purple Team"
    echo -e "  ${GREEN}secteam green${NC}            - Activar contexto Green Team"
    echo -e "  ${WHITE}secteam white${NC}            - Activar contexto White Team"
    echo -e "  ${YELLOW}secteam yellow${NC}           - Activar contexto Yellow Team"
    echo -e "  ${ORANGE}secteam orange${NC}           - Activar contexto Orange Team"
    echo ""
    echo -e "${CYAN}Comunicación:${NC}"
    echo -e "  ${GREEN}secteam share <team> <file>${NC}  - Compartir hallazgo con otro equipo"
    echo -e "  ${GREEN}secteam call <team> <action>${NC} - Invocar acción de otro equipo"
    echo -e "  ${GREEN}secteam sync${NC}                 - Sincronizar contextos"
    echo ""
    echo -e "${CYAN}Workflows:${NC}"
    echo -e "  ${GREEN}secteam workflow <name>${NC}  - Ejecutar workflow predefinido"
    echo -e "  ${GREEN}secteam workflows${NC}        - Listar workflows disponibles"
}

# Crear nuevo proyecto
new_project() {
    local project_name=$1
    if [[ -z "$project_name" ]]; then
        echo -e "${RED}Error: Especifica un nombre de proyecto${NC}"
        return 1
    fi
    
    local project_dir="$PROJECTS_DIR/$project_name"
    mkdir -p "$project_dir"
    
    echo -e "${CYAN}[*]${NC} Creando proyecto: $project_name"
    
    # Crear contextos aislados para cada equipo
    for team in RedTeam BlueTeam PurpleTeam GreenTeam WhiteTeam YellowTeam OrangeTeam; do
        local team_ctx="$project_dir/$team"
        mkdir -p "$team_ctx"/{findings,logs,evidence,reports,notes}
        
        # Crear archivo de contexto
        cat > "$team_ctx/context.json" << EOF
{
    "project": "$project_name",
    "team": "$team",
    "created": "$(date -Iseconds)",
    "status": "active",
    "findings": [],
    "communications": []
}
EOF
    done
    
    # Crear archivo de proyecto
    cat > "$project_dir/project.json" << EOF
{
    "name": "$project_name",
    "created": "$(date -Iseconds)",
    "status": "active",
    "teams_involved": ["RedTeam", "BlueTeam", "PurpleTeam", "GreenTeam", "WhiteTeam", "YellowTeam", "OrangeTeam"],
    "current_phase": "initialization"
}
EOF
    
    echo -e "${GREEN}[✓]${NC} Proyecto '$project_name' creado con contextos aislados"
    echo -e "${CYAN}[*]${NC} Usa: ${GREEN}secteam use $project_name${NC} para activarlo"
}

# Listar proyectos
list_projects() {
    echo -e "${PURPLE}═══════════════════════════════════════════════════════════════════${NC}"
    echo -e "${WHITE}  📁 PROYECTOS DISPONIBLES${NC}"
    echo -e "${PURPLE}═══════════════════════════════════════════════════════════════════${NC}"
    
    if [[ -d "$PROJECTS_DIR" ]]; then
        for project in "$PROJECTS_DIR"/*/; do
            if [[ -d "$project" ]]; then
                local name=$(basename "$project")
                local status=$(jq -r '.status' "$project/project.json" 2>/dev/null || echo "unknown")
                echo -e "  ${GREEN}●${NC} $name (${CYAN}$status${NC})"
            fi
        done
    else
        echo -e "  ${YELLOW}No hay proyectos creados${NC}"
    fi
    echo ""
}

# Activar contexto de equipo
activate_team() {
    local team=$1
    local team_dir="$WORKSPACE_ROOT/$team"
    
    if [[ ! -d "$team_dir" ]]; then
        echo -e "${RED}Error: Equipo $team no encontrado${NC}"
        return 1
    fi
    
    # Activar entorno virtual si existe
    if [[ -f "$team_dir/venv/bin/activate" ]]; then
        source "$team_dir/venv/bin/activate"
    fi
    
    # Exportar variables de contexto
    export SECURITY_TEAM="$team"
    export SECURITY_TEAM_DIR="$team_dir"
    export SECURITY_WORKSPACE="$WORKSPACE_ROOT"
    
    # Cambiar al directorio del equipo
    cd "$team_dir"
    
    echo -e "${GREEN}[✓]${NC} Contexto activado: $team"
    echo -e "${CYAN}[*]${NC} Directorio: $team_dir"
}

# Compartir hallazgo
share_finding() {
    local target_team=$1
    local file=$2
    
    if [[ -z "$target_team" || -z "$file" ]]; then
        echo -e "${RED}Error: Uso: secteam share <team> <file>${NC}"
        return 1
    fi
    
    local source_team="${SECURITY_TEAM:-unknown}"
    local shared_dir="$WORKSPACE_ROOT/.shared"
    mkdir -p "$shared_dir"
    
    local timestamp=$(date +%Y%m%d_%H%M%S)
    local shared_file="$shared_dir/${source_team}_to_${target_team}_${timestamp}_$(basename "$file")"
    
    cp "$file" "$shared_file"
    
    echo -e "${GREEN}[✓]${NC} Hallazgo compartido con $target_team"
    echo -e "${CYAN}[*]${NC} Archivo: $shared_file"
    
    # Log de comunicación
    echo "[$(date -Iseconds)] $source_team -> $target_team: $(basename "$file")" >> "$shared_dir/communications.log"
}

# Invocar acción de otro equipo
call_team() {
    local target_team=$1
    local action=$2
    shift 2
    local args="$@"
    
    echo -e "${CYAN}[*]${NC} Invocando $action en $target_team..."
    
    local team_dir="$WORKSPACE_ROOT/$target_team"
    if [[ -d "$team_dir" ]]; then
        # Buscar script de acción
        if [[ -f "$team_dir/actions/$action.sh" ]]; then
            bash "$team_dir/actions/$action.sh" $args
        else
            echo -e "${YELLOW}[!]${NC} Acción '$action' no encontrada en $target_team"
        fi
    fi
}

# Estado actual
show_status() {
    echo -e "${PURPLE}═══════════════════════════════════════════════════════════════════${NC}"
    echo -e "${WHITE}  🛡️ ESTADO DEL SECURITY TEAM WORKSPACE${NC}"
    echo -e "${PURPLE}═══════════════════════════════════════════════════════════════════${NC}"
    echo ""
    echo -e "  ${CYAN}Workspace:${NC} $WORKSPACE_ROOT"
    echo -e "  ${CYAN}Equipo Activo:${NC} ${SECURITY_TEAM:-ninguno}"
    echo -e "  ${CYAN}Proyecto Activo:${NC} ${SECURITY_PROJECT:-ninguno}"
    echo ""
    echo -e "${WHITE}  Equipos Disponibles:${NC}"
    echo -e "    ${RED}🔴 RedTeam${NC}    - Offensive Security"
    echo -e "    ${BLUE}🔵 BlueTeam${NC}   - Defensive Security"
    echo -e "    ${PURPLE}🟣 PurpleTeam${NC} - Security Validation"
    echo -e "    ${GREEN}🟢 GreenTeam${NC}  - DevSecOps"
    echo -e "    ${WHITE}⚪ WhiteTeam${NC}  - GRC"
    echo -e "    ${YELLOW}🟡 YellowTeam${NC} - Security Architecture"
    echo -e "    ${ORANGE}🟠 OrangeTeam${NC} - Security Awareness"
    echo ""
}

# Main
case "$1" in
    new)
        new_project "$2"
        ;;
    list)
        list_projects
        ;;
    use)
        export SECURITY_PROJECT="$2"
        echo -e "${GREEN}[✓]${NC} Proyecto activo: $2"
        ;;
    status)
        show_status
        ;;
    red)
        activate_team "RedTeam"
        ;;
    blue)
        activate_team "BlueTeam"
        ;;
    purple)
        activate_team "PurpleTeam"
        ;;
    green)
        activate_team "GreenTeam"
        ;;
    white)
        activate_team "WhiteTeam"
        ;;
    yellow)
        activate_team "YellowTeam"
        ;;
    orange)
        activate_team "OrangeTeam"
        ;;
    share)
        share_finding "$2" "$3"
        ;;
    call)
        call_team "$2" "$3" "${@:4}"
        ;;
    help|--help|-h|"")
        show_help
        ;;
    *)
        echo -e "${RED}Comando desconocido: $1${NC}"
        show_help
        ;;
esac
SECTEAM

    chmod +x "$WORKSPACE_ROOT/secteam"
    
    # Crear enlace simbólico global
    ln -sf "$WORKSPACE_ROOT/secteam" /usr/local/bin/secteam 2>/dev/null || true
    
    success "Script de orquestación creado: secteam"
}

#═══════════════════════════════════════════════════════════════════════════════
# FASE 5: CONFIGURAR WINDSURF WORKFLOWS
#═══════════════════════════════════════════════════════════════════════════════
setup_windsurf_workflows() {
    section "🌊 FASE 5: CONFIGURANDO WINDSURF WORKFLOWS"
    
    local workflows_dir="$WORKSPACE_ROOT/.windsurf/workflows"
    mkdir -p "$workflows_dir"
    
    # Workflow: Activar equipo
    cat > "$workflows_dir/team.md" << 'WORKFLOW'
---
description: Activar contexto de un equipo de seguridad específico
---

# Activar Equipo de Seguridad

1. Identificar el equipo solicitado (Red, Blue, Purple, Green, White, Yellow, Orange)
2. Cargar el contexto del equipo desde `.contexts/config.json`
3. Activar las herramientas y capacidades del equipo
4. Informar al usuario las capacidades disponibles

## Equipos Disponibles:
- **RedTeam**: Seguridad ofensiva, pentesting, explotación
- **BlueTeam**: Seguridad defensiva, detección, respuesta a incidentes
- **PurpleTeam**: Validación de seguridad, simulación de ataques
- **GreenTeam**: DevSecOps, SAST, DAST, seguridad de contenedores
- **WhiteTeam**: GRC, cumplimiento, auditoría
- **YellowTeam**: Arquitectura de seguridad, threat modeling
- **OrangeTeam**: Awareness, phishing simulation, training
WORKFLOW

    # Workflow: Nuevo proyecto
    cat > "$workflows_dir/project.md" << 'WORKFLOW'
---
description: Crear un nuevo proyecto con contextos aislados para todos los equipos
---

# Crear Nuevo Proyecto de Seguridad

1. Solicitar nombre del proyecto al usuario
2. Crear estructura de directorios en `.projects/<nombre>/`
3. Inicializar contextos aislados para cada equipo
4. Crear archivos de configuración del proyecto
5. Informar al usuario cómo activar el proyecto

// turbo
```bash
secteam new <nombre_proyecto>
```
WORKFLOW

    # Workflow: Comunicación entre equipos
    cat > "$workflows_dir/communicate.md" << 'WORKFLOW'
---
description: Facilitar comunicación y compartir hallazgos entre equipos
---

# Comunicación Entre Equipos

1. Identificar equipo origen y destino
2. Verificar permisos de comunicación en config.json
3. Preparar el hallazgo o información a compartir
4. Registrar la comunicación en el log
5. Notificar al equipo destino

## Comandos:
```bash
secteam share <equipo_destino> <archivo>
secteam call <equipo> <accion>
```
WORKFLOW

    success "Workflows de Windsurf configurados"
}

#═══════════════════════════════════════════════════════════════════════════════
# FASE 6: CREAR ESTRUCTURA COMPARTIDA
#═══════════════════════════════════════════════════════════════════════════════
create_shared_structure() {
    section "📂 FASE 6: ESTRUCTURA COMPARTIDA"
    
    mkdir -p "$WORKSPACE_ROOT/.shared"/{findings,evidence,reports,communications}
    mkdir -p "$WORKSPACE_ROOT/.projects"
    mkdir -p "$WORKSPACE_ROOT/.contexts"
    
    # Crear README principal
    cat > "$WORKSPACE_ROOT/README.md" << 'README'
# 🛡️ Security Team Unified Workspace

Workspace unificado para equipos de ciberseguridad con contextos aislados.

## Equipos

| Equipo | Rol | Descripción |
|--------|-----|-------------|
| 🔴 RedTeam | Offensive | Pentesting, explotación, reconocimiento |
| 🔵 BlueTeam | Defensive | Detección, respuesta, forense |
| 🟣 PurpleTeam | Validation | Simulación de ataques, validación |
| 🟢 GreenTeam | DevSecOps | SAST, DAST, seguridad de código |
| ⚪ WhiteTeam | GRC | Governance, Risk, Compliance |
| 🟡 YellowTeam | Architecture | Threat modeling, arquitectura |
| 🟠 OrangeTeam | Awareness | Training, phishing simulation |

## Uso Rápido

```bash
# Ver estado
secteam status

# Crear nuevo proyecto
secteam new mi-proyecto

# Activar equipo
secteam red    # Red Team
secteam blue   # Blue Team
secteam purple # Purple Team

# Compartir hallazgos
secteam share BlueTeam finding.txt

# Ver ayuda
secteam help
```

## Estructura

```
SecurityTeam Workspace/
├── RedTeam/           # Herramientas ofensivas
├── BlueTeam/          # Herramientas defensivas
├── PurpleTeam/        # Validación de seguridad
├── GreenTeam/         # DevSecOps
├── WhiteTeam/         # GRC
├── YellowTeam/        # Arquitectura
├── OrangeTeam/        # Awareness
├── .contexts/         # Configuración de contextos
├── .projects/         # Proyectos con contextos aislados
├── .shared/           # Hallazgos compartidos
└── .windsurf/         # Workflows de Windsurf
```

## Windsurf AI Integration

Este workspace está diseñado para trabajar con Windsurf AI. Usa los workflows:
- `/team` - Activar contexto de equipo
- `/project` - Crear nuevo proyecto
- `/communicate` - Compartir entre equipos
README

    success "Estructura compartida creada"
}

#═══════════════════════════════════════════════════════════════════════════════
# FASE 7: FINALIZACIÓN
#═══════════════════════════════════════════════════════════════════════════════
finalize_installation() {
    section "✅ FASE 7: FINALIZACIÓN"
    
    # Install secteam globally
    echo -e "${CYAN}[*] Installing secteam command globally...${NC}"
    chmod +x "$WORKSPACE_ROOT/secteam"
    
    # Create symlink in /usr/local/bin (requires sudo)
    if [ -w /usr/local/bin ] || [ "$EUID" -eq 0 ]; then
        ln -sf "$WORKSPACE_ROOT/secteam" /usr/local/bin/secteam
        echo -e "${GREEN}[✓] secteam installed globally - use 'secteam' from anywhere${NC}"
    else
        # Try with sudo
        if sudo ln -sf "$WORKSPACE_ROOT/secteam" /usr/local/bin/secteam 2>/dev/null; then
            echo -e "${GREEN}[✓] secteam installed globally - use 'secteam' from anywhere${NC}"
        else
            echo -e "${YELLOW}[!] Could not install globally. Use: sudo ln -sf $WORKSPACE_ROOT/secteam /usr/local/bin/secteam${NC}"
        fi
    fi
    
    # Crear archivo de estado
    cat > "$WORKSPACE_ROOT/.installed" << EOF
{
    "version": "1.0.0",
    "installed_at": "$(date -Iseconds)",
    "teams": ["RedTeam", "BlueTeam", "PurpleTeam", "GreenTeam", "WhiteTeam", "YellowTeam", "OrangeTeam"],
    "status": "complete"
}
EOF
    
    echo ""
    echo -e "${GREEN}═══════════════════════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}  ✅ INSTALACIÓN COMPLETADA EXITOSAMENTE${NC}"
    echo -e "${GREEN}═══════════════════════════════════════════════════════════════════${NC}"
    echo ""
    echo -e "${CYAN}Comandos disponibles:${NC}"
    echo -e "  ${GREEN}secteam status${NC}    - Ver estado del workspace"
    echo -e "  ${GREEN}secteam new${NC}       - Crear nuevo proyecto"
    echo -e "  ${GREEN}secteam red${NC}       - Activar Red Team"
    echo -e "  ${GREEN}secteam blue${NC}      - Activar Blue Team"
    echo -e "  ${GREEN}secteam report${NC}    - Generar mega reporte"
    echo -e "  ${GREEN}secteam help${NC}      - Ver todos los comandos"
    echo ""
    echo -e "${YELLOW}═══════════════════════════════════════════════════════════════════${NC}"
    echo -e "${YELLOW}  ⚠️  CONFIGURACIÓN REQUERIDA - ARCHIVOS .env${NC}"
    echo -e "${YELLOW}═══════════════════════════════════════════════════════════════════${NC}"
    echo ""
    echo -e "${CYAN}Algunos equipos requieren configuración de API keys y secrets:${NC}"
    echo ""
    echo -e "  ${RED}RedTeam:${NC}"
    echo -e "    cp RedTeam/.env.example RedTeam/.env"
    echo -e "    # Configurar: SHODAN_API_KEY, CENSYS_API_KEY"
    echo ""
    echo -e "  ${BLUE}BlueTeam:${NC}"
    echo -e "    cp BlueTeam/.env.example BlueTeam/.env"
    echo -e "    # Configurar: VIRUSTOTAL_API_KEY, MISP_API_KEY"
    echo ""
    echo -e "  ${ORANGE}OrangeTeam:${NC}"
    echo -e "    cp OrangeTeam/.env.example OrangeTeam/.env"
    echo -e "    # Configurar: SMTP_SERVER, SMTP_USER, SMTP_PASS"
    echo ""
    echo -e "${PURPLE}Consulta el README.md para más detalles sobre configuración.${NC}"
    echo ""
    echo -e "${PURPLE}Log de instalación: $LOG_FILE${NC}"
    echo ""
}

#═══════════════════════════════════════════════════════════════════════════════
# MENÚ PRINCIPAL
#═══════════════════════════════════════════════════════════════════════════════
show_menu() {
    echo ""
    echo -e "${CYAN}Selecciona una opción:${NC}"
    echo -e "  ${GREEN}1)${NC} Instalación completa (todos los equipos)"
    echo -e "  ${GREEN}2)${NC} Solo actualizar sistema y dependencias"
    echo -e "  ${GREEN}3)${NC} Solo configurar contextos y orquestador"
    echo -e "  ${GREEN}4)${NC} Instalar equipo específico"
    echo -e "  ${GREEN}5)${NC} Salir"
    echo ""
    read -p "Opción [1-5]: " choice
    
    case $choice in
        1) full_install ;;
        2) update_system && install_base_deps ;;
        3) create_context_system && setup_windsurf_workflows && create_shared_structure ;;
        4) select_team ;;
        5) exit 0 ;;
        *) echo -e "${RED}Opción inválida${NC}"; show_menu ;;
    esac
}

select_team() {
    echo ""
    echo -e "${CYAN}Selecciona el equipo a instalar:${NC}"
    echo -e "  ${RED}1)${NC} RedTeam"
    echo -e "  ${BLUE}2)${NC} BlueTeam"
    echo -e "  ${PURPLE}3)${NC} PurpleTeam"
    echo -e "  ${GREEN}4)${NC} GreenTeam"
    echo -e "  ${WHITE}5)${NC} WhiteTeam"
    echo -e "  ${YELLOW}6)${NC} YellowTeam"
    echo -e "  ${ORANGE}7)${NC} OrangeTeam"
    echo ""
    read -p "Opción [1-7]: " team_choice
    
    case $team_choice in
        1) install_team "RedTeam" "$RED" ;;
        2) install_team "BlueTeam" "$BLUE" ;;
        3) install_team "PurpleTeam" "$PURPLE" ;;
        4) install_team "GreenTeam" "$GREEN" ;;
        5) install_team "WhiteTeam" "$WHITE" ;;
        6) install_team "YellowTeam" "$YELLOW" ;;
        7) install_team "OrangeTeam" "$ORANGE" ;;
        *) echo -e "${RED}Opción inválida${NC}" ;;
    esac
}

full_install() {
    update_system
    install_base_deps
    install_all_teams
    create_context_system
    setup_windsurf_workflows
    create_shared_structure
    finalize_installation
}

#═══════════════════════════════════════════════════════════════════════════════
# MAIN
#═══════════════════════════════════════════════════════════════════════════════
main() {
    print_banner
    check_root
    detect_os
    
    # Si se pasa --full como argumento, instalar todo sin menú
    if [[ "$1" == "--full" || "$1" == "-f" ]]; then
        full_install
    else
        show_menu
    fi
}

main "$@"
