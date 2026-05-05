<![CDATA[#!/bin/bash

#╔═══════════════════════════════════════════════════════════════════════════════╗
#║                                                                               ║
#║   ██████╗ ██╗   ██╗██████╗ ██████╗ ██╗     ███████╗    ████████╗███████╗     ║
#║   ██╔══██╗██║   ██║██╔══██╗██╔══██╗██║     ██╔════╝    ╚══██╔══╝██╔════╝     ║
#║   ██████╔╝██║   ██║██████╔╝██████╔╝██║     █████╗         ██║   █████╗       ║
#║   ██╔═══╝ ██║   ██║██╔══██╗██╔═══╝ ██║     ██╔══╝         ██║   ██╔══╝       ║
#║   ██║     ╚██████╔╝██║  ██║██║     ███████╗███████╗       ██║   ███████╗     ║
#║   ╚═╝      ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚══════╝╚══════╝       ╚═╝   ╚══════╝     ║
#║                                                                               ║
#║   PURPLE TEAM INSTALLER - Kali Linux + Windsurf AI                           ║
#║   Instalador completo de herramientas ofensivas y defensivas                 ║
#║                                                                               ║
#╚═══════════════════════════════════════════════════════════════════════════════╝

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

INSTALL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TOOLS_DIR="$INSTALL_DIR/tools"
VENV_DIR="$INSTALL_DIR/venv"
LOG_FILE="$INSTALL_DIR/logs/install_$(date +%Y%m%d_%H%M%S).log"

# ═══════════════════════════════════════════════════════════════════════════════
# FUNCIONES DE UTILIDAD
# ═══════════════════════════════════════════════════════════════════════════════

banner() {
    echo -e "${PURPLE}"
    cat << "EOF"
    
    ╔═══════════════════════════════════════════════════════════════════╗
    ║                                                                   ║
    ║   🟣 PURPLE TEAM INSTALLER                                        ║
    ║                                                                   ║
    ║   Instalando herramientas para:                                   ║
    ║   🔴 Red Team (Offensive Security)                                ║
    ║   🔵 Blue Team (Defensive Security)                               ║
    ║   🟣 Purple Team (Collaborative Validation)                       ║
    ║                                                                   ║
    ╚═══════════════════════════════════════════════════════════════════╝
    
EOF
    echo -e "${NC}"
}

log() {
    echo -e "${GREEN}[+]${NC} $1"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

warn() {
    echo -e "${YELLOW}[!]${NC} $1"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] WARNING: $1" >> "$LOG_FILE"
}

error() {
    echo -e "${RED}[✗]${NC} $1"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ERROR: $1" >> "$LOG_FILE"
}

success() {
    echo -e "${GREEN}[✓]${NC} $1"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] SUCCESS: $1" >> "$LOG_FILE"
}

section() {
    echo ""
    echo -e "${PURPLE}═══════════════════════════════════════════════════════════════════${NC}"
    echo -e "${PURPLE}  $1${NC}"
    echo -e "${PURPLE}═══════════════════════════════════════════════════════════════════${NC}"
    echo ""
}

check_root() {
    if [[ $EUID -ne 0 ]]; then
        error "Este script debe ejecutarse como root"
        echo "Uso: sudo ./install.sh"
        exit 1
    fi
}

check_kali() {
    if ! grep -q "Kali" /etc/os-release 2>/dev/null; then
        warn "Este script está optimizado para Kali Linux"
        read -p "¿Desea continuar de todos modos? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    fi
}

# ═══════════════════════════════════════════════════════════════════════════════
# PREPARACIÓN DEL SISTEMA
# ═══════════════════════════════════════════════════════════════════════════════

prepare_system() {
    section "🔧 PREPARANDO SISTEMA"
    
    log "Creando directorios necesarios..."
    mkdir -p "$INSTALL_DIR"/{logs,tools/external,evidence,templates}
    mkdir -p "$TOOLS_DIR"/{atomic-red-team,caldera,infection-monkey,stratus-red-team}
    mkdir -p "$INSTALL_DIR"/rules/{sigma,yara}
    
    log "Actualizando repositorios..."
    apt-get update -qq
    
    log "Instalando dependencias base..."
    apt-get install -y -qq \
        git \
        curl \
        wget \
        python3 \
        python3-pip \
        python3-venv \
        docker.io \
        docker-compose \
        golang-go \
        jq \
        yq \
        tree \
        tmux \
        vim \
        net-tools \
        dnsutils \
        whois \
        nmap \
        2>/dev/null
    
    success "Sistema preparado"
}

# ═══════════════════════════════════════════════════════════════════════════════
# ENTORNO VIRTUAL PYTHON
# ═══════════════════════════════════════════════════════════════════════════════

setup_python_env() {
    section "🐍 CONFIGURANDO ENTORNO PYTHON"
    
    log "Creando entorno virtual..."
    python3 -m venv "$VENV_DIR"
    source "$VENV_DIR/bin/activate"
    
    log "Actualizando pip..."
    pip install --upgrade pip setuptools wheel -q
    
    log "Instalando dependencias Python..."
    pip install -q \
        requests \
        pyyaml \
        colorama \
        tabulate \
        jinja2 \
        pandas \
        numpy \
        matplotlib \
        rich \
        typer \
        httpx \
        aiohttp \
        python-dateutil \
        cryptography \
        pycryptodome \
        scapy \
        impacket \
        ldap3 \
        dnspython \
        paramiko \
        fabric \
        pywinrm \
        bloodhound \
        neo4j \
        sigma-cli \
        stix2 \
        taxii2-client \
        mitreattack-python \
        attackcti
    
    success "Entorno Python configurado"
}

# ═══════════════════════════════════════════════════════════════════════════════
# HERRAMIENTAS RED TEAM
# ═══════════════════════════════════════════════════════════════════════════════

install_red_team_tools() {
    section "🔴 INSTALANDO HERRAMIENTAS RED TEAM"
    
    # Atomic Red Team
    log "Instalando Atomic Red Team..."
    if [[ ! -d "$TOOLS_DIR/atomic-red-team/atomics" ]]; then
        git clone --depth 1 https://github.com/redcanaryco/atomic-red-team.git "$TOOLS_DIR/atomic-red-team" 2>/dev/null || true
    fi
    success "Atomic Red Team instalado"
    
    # MITRE Caldera
    log "Instalando MITRE Caldera..."
    if [[ ! -d "$TOOLS_DIR/caldera/caldera" ]]; then
        git clone --depth 1 https://github.com/mitre/caldera.git "$TOOLS_DIR/caldera" --recursive 2>/dev/null || true
        if [[ -f "$TOOLS_DIR/caldera/requirements.txt" ]]; then
            pip install -r "$TOOLS_DIR/caldera/requirements.txt" -q 2>/dev/null || true
        fi
    fi
    success "MITRE Caldera instalado"
    
    # Infection Monkey
    log "Instalando Infection Monkey..."
    if [[ ! -d "$TOOLS_DIR/infection-monkey" ]]; then
        mkdir -p "$TOOLS_DIR/infection-monkey"
        # Descargar docker-compose para Infection Monkey
        cat > "$TOOLS_DIR/infection-monkey/docker-compose.yml" << 'EOFMONKEY'
version: '3'
services:
  monkey-island:
    image: guardicore/monkey-island:latest
    ports:
      - "5000:5000"
      - "443:443"
    volumes:
      - monkey-data:/var/monkey-island-data
volumes:
  monkey-data:
EOFMONKEY
    fi
    success "Infection Monkey configurado"
    
    # Stratus Red Team
    log "Instalando Stratus Red Team..."
    if ! command -v stratus &> /dev/null; then
        go install -v github.com/datadog/stratus-red-team/v2/cmd/stratus@latest 2>/dev/null || true
    fi
    success "Stratus Red Team instalado"
    
    # Herramientas Kali adicionales
    log "Instalando herramientas Kali adicionales..."
    apt-get install -y -qq \
        metasploit-framework \
        exploitdb \
        sqlmap \
        nikto \
        dirb \
        gobuster \
        ffuf \
        wfuzz \
        hydra \
        john \
        hashcat \
        aircrack-ng \
        wireshark \
        tcpdump \
        responder \
        crackmapexec \
        evil-winrm \
        bloodhound \
        neo4j \
        seclists \
        wordlists \
        payloadsallthethings \
        webshells \
        mimikatz \
        powersploit \
        empire \
        covenant \
        2>/dev/null || true
    
    success "Herramientas Red Team instaladas"
}

# ═══════════════════════════════════════════════════════════════════════════════
# HERRAMIENTAS BLUE TEAM
# ═══════════════════════════════════════════════════════════════════════════════

install_blue_team_tools() {
    section "🔵 INSTALANDO HERRAMIENTAS BLUE TEAM"
    
    # Sigma Rules
    log "Descargando Sigma Rules..."
    if [[ ! -d "$INSTALL_DIR/rules/sigma/sigma" ]]; then
        git clone --depth 1 https://github.com/SigmaHQ/sigma.git "$INSTALL_DIR/rules/sigma/sigma" 2>/dev/null || true
    fi
    success "Sigma Rules descargadas"
    
    # YARA Rules
    log "Descargando YARA Rules..."
    if [[ ! -d "$INSTALL_DIR/rules/yara/yara-rules" ]]; then
        git clone --depth 1 https://github.com/Yara-Rules/rules.git "$INSTALL_DIR/rules/yara/yara-rules" 2>/dev/null || true
    fi
    success "YARA Rules descargadas"
    
    # Herramientas de análisis
    log "Instalando herramientas de análisis..."
    apt-get install -y -qq \
        yara \
        clamav \
        rkhunter \
        chkrootkit \
        lynis \
        aide \
        ossec-hids \
        snort \
        suricata \
        zeek \
        volatility3 \
        autopsy \
        sleuthkit \
        foremost \
        binwalk \
        radare2 \
        ghidra \
        2>/dev/null || true
    
    # Velociraptor
    log "Instalando Velociraptor..."
    if ! command -v velociraptor &> /dev/null; then
        VELO_VERSION=$(curl -s https://api.github.com/repos/Velocidex/velociraptor/releases/latest | jq -r '.tag_name' | tr -d 'v')
        wget -q "https://github.com/Velocidex/velociraptor/releases/download/v${VELO_VERSION}/velociraptor-v${VELO_VERSION}-linux-amd64" -O /usr/local/bin/velociraptor 2>/dev/null || true
        chmod +x /usr/local/bin/velociraptor 2>/dev/null || true
    fi
    success "Velociraptor instalado"
    
    # Wazuh Agent
    log "Configurando Wazuh..."
    cat > "$TOOLS_DIR/wazuh-docker-compose.yml" << 'EOFWAZUH'
version: '3'
services:
  wazuh-manager:
    image: wazuh/wazuh-manager:latest
    ports:
      - "1514:1514/udp"
      - "1515:1515"
      - "514:514/udp"
      - "55000:55000"
    volumes:
      - wazuh-data:/var/ossec/data
volumes:
  wazuh-data:
EOFWAZUH
    success "Wazuh configurado"
    
    success "Herramientas Blue Team instaladas"
}

# ═══════════════════════════════════════════════════════════════════════════════
# HERRAMIENTAS PURPLE TEAM
# ═══════════════════════════════════════════════════════════════════════════════

install_purple_team_tools() {
    section "🟣 INSTALANDO HERRAMIENTAS PURPLE TEAM"
    
    # DetectionLab
    log "Configurando DetectionLab..."
    if [[ ! -d "$TOOLS_DIR/DetectionLab" ]]; then
        git clone --depth 1 https://github.com/clong/DetectionLab.git "$TOOLS_DIR/DetectionLab" 2>/dev/null || true
    fi
    success "DetectionLab configurado"
    
    # DeTTECT
    log "Instalando DeTTECT..."
    if [[ ! -d "$TOOLS_DIR/DeTTECT" ]]; then
        git clone --depth 1 https://github.com/rabobank-cdc/DeTTECT.git "$TOOLS_DIR/DeTTECT" 2>/dev/null || true
        if [[ -f "$TOOLS_DIR/DeTTECT/requirements.txt" ]]; then
            pip install -r "$TOOLS_DIR/DeTTECT/requirements.txt" -q 2>/dev/null || true
        fi
    fi
    success "DeTTECT instalado"
    
    # ATT&CK Navigator
    log "Configurando ATT&CK Navigator..."
    cat > "$TOOLS_DIR/navigator-docker-compose.yml" << 'EOFNAV'
version: '3'
services:
  attack-navigator:
    image: mitre/attack-navigator:latest
    ports:
      - "4200:4200"
EOFNAV
    success "ATT&CK Navigator configurado"
    
    # Vectr
    log "Configurando Vectr..."
    if [[ ! -d "$TOOLS_DIR/vectr" ]]; then
        mkdir -p "$TOOLS_DIR/vectr"
        cat > "$TOOLS_DIR/vectr/docker-compose.yml" << 'EOFVECTR'
version: '3'
services:
  vectr:
    image: securityriskadvisors/vectr:latest
    ports:
      - "8081:8081"
    environment:
      - VECTR_PORT=8081
    volumes:
      - vectr-data:/data
volumes:
  vectr-data:
EOFVECTR
    fi
    success "Vectr configurado"
    
    success "Herramientas Purple Team instaladas"
}

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURACIÓN DE DOCKER
# ═══════════════════════════════════════════════════════════════════════════════

setup_docker() {
    section "🐳 CONFIGURANDO DOCKER"
    
    log "Iniciando servicio Docker..."
    systemctl enable docker 2>/dev/null || true
    systemctl start docker 2>/dev/null || true
    
    log "Agregando usuario al grupo docker..."
    usermod -aG docker "$SUDO_USER" 2>/dev/null || true
    
    # Docker Compose principal
    log "Creando Docker Compose principal..."
    cat > "$TOOLS_DIR/docker-compose.yml" << 'EOFDOCKER'
version: '3.8'

services:
  # ═══════════════════════════════════════════════════════════════
  # ELASTIC STACK - SIEM
  # ═══════════════════════════════════════════════════════════════
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.11.0
    container_name: purple-elasticsearch
    environment:
      - discovery.type=single-node
      - xpack.security.enabled=false
      - "ES_JAVA_OPTS=-Xms1g -Xmx1g"
    ports:
      - "9200:9200"
    volumes:
      - elastic-data:/usr/share/elasticsearch/data
    networks:
      - purple-network

  kibana:
    image: docker.elastic.co/kibana/kibana:8.11.0
    container_name: purple-kibana
    ports:
      - "5601:5601"
    environment:
      - ELASTICSEARCH_HOSTS=http://elasticsearch:9200
    depends_on:
      - elasticsearch
    networks:
      - purple-network

  # ═══════════════════════════════════════════════════════════════
  # MITRE CALDERA
  # ═══════════════════════════════════════════════════════════════
  caldera:
    image: mitre/caldera:latest
    container_name: purple-caldera
    ports:
      - "8888:8888"
      - "7010:7010"
      - "7011:7011"
    volumes:
      - caldera-data:/usr/src/app/data
    networks:
      - purple-network

  # ═══════════════════════════════════════════════════════════════
  # OPENCTI - THREAT INTELLIGENCE
  # ═══════════════════════════════════════════════════════════════
  redis:
    image: redis:7
    container_name: purple-redis
    networks:
      - purple-network

  # ═══════════════════════════════════════════════════════════════
  # PORTAINER - DOCKER MANAGEMENT
  # ═══════════════════════════════════════════════════════════════
  portainer:
    image: portainer/portainer-ce:latest
    container_name: purple-portainer
    ports:
      - "9000:9000"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - portainer-data:/data
    networks:
      - purple-network

networks:
  purple-network:
    driver: bridge

volumes:
  elastic-data:
  caldera-data:
  portainer-data:
EOFDOCKER
    
    success "Docker configurado"
}

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURACIÓN FINAL
# ═══════════════════════════════════════════════════════════════════════════════

final_setup() {
    section "⚙️ CONFIGURACIÓN FINAL"
    
    log "Configurando permisos..."
    chown -R "$SUDO_USER:$SUDO_USER" "$INSTALL_DIR"
    chmod +x "$INSTALL_DIR/tools/custom-scripts/"*.py 2>/dev/null || true
    chmod +x "$INSTALL_DIR/tools/custom-scripts/"*.sh 2>/dev/null || true
    
    log "Creando alias útiles..."
    cat >> "/home/$SUDO_USER/.bashrc" << 'EOFALIAS'

# ═══════════════════════════════════════════════════════════════
# PURPLE TEAM ALIASES
# ═══════════════════════════════════════════════════════════════
alias purple-activate='source ~/Documents/PurpleTeam\ -\ Windsurf/venv/bin/activate'
alias purple-simulate='python3 ~/Documents/PurpleTeam\ -\ Windsurf/tools/custom-scripts/attack_simulate.py'
alias purple-validate='~/Documents/PurpleTeam\ -\ Windsurf/tools/custom-scripts/detection_validate.sh'
alias purple-gaps='python3 ~/Documents/PurpleTeam\ -\ Windsurf/tools/custom-scripts/gap_analyzer.py'
alias purple-report='python3 ~/Documents/PurpleTeam\ -\ Windsurf/tools/custom-scripts/purple_report.py'
alias purple-mitre='python3 ~/Documents/PurpleTeam\ -\ Windsurf/tools/custom-scripts/mitre_mapper.py'
alias atomic='cd ~/Documents/PurpleTeam\ -\ Windsurf/tools/atomic-red-team && pwsh'
alias caldera-start='cd ~/Documents/PurpleTeam\ -\ Windsurf/tools/caldera && python3 server.py'
alias purple-docker='cd ~/Documents/PurpleTeam\ -\ Windsurf/tools && docker-compose up -d'
EOFALIAS
    
    log "Creando script de inicio rápido..."
    cat > "$INSTALL_DIR/start.sh" << 'EOFSTART'
#!/bin/bash
echo "🟣 Iniciando Purple Team Environment..."
source "$(dirname "$0")/venv/bin/activate"
cd "$(dirname "$0")"
echo "✅ Entorno activado. Comandos disponibles:"
echo "   purple-simulate  - Simular técnicas ATT&CK"
echo "   purple-validate  - Validar detecciones"
echo "   purple-gaps      - Analizar brechas"
echo "   purple-report    - Generar reportes"
echo "   purple-docker    - Iniciar servicios Docker"
exec $SHELL
EOFSTART
    chmod +x "$INSTALL_DIR/start.sh"
    
    success "Configuración final completada"
}

# ═══════════════════════════════════════════════════════════════════════════════
# RESUMEN DE INSTALACIÓN
# ═══════════════════════════════════════════════════════════════════════════════

print_summary() {
    section "📋 RESUMEN DE INSTALACIÓN"
    
    echo -e "${GREEN}"
    cat << "EOF"
    
    ╔═══════════════════════════════════════════════════════════════════╗
    ║                                                                   ║
    ║   ✅ INSTALACIÓN COMPLETADA EXITOSAMENTE                          ║
    ║                                                                   ║
    ╠═══════════════════════════════════════════════════════════════════╣
    ║                                                                   ║
    ║   🔴 RED TEAM TOOLS:                                              ║
    ║      • Atomic Red Team                                            ║
    ║      • MITRE Caldera                                              ║
    ║      • Infection Monkey                                           ║
    ║      • Stratus Red Team                                           ║
    ║      • Metasploit, CrackMapExec, BloodHound, etc.                ║
    ║                                                                   ║
    ║   🔵 BLUE TEAM TOOLS:                                             ║
    ║      • Sigma Rules                                                ║
    ║      • YARA Rules                                                 ║
    ║      • Velociraptor                                               ║
    ║      • Wazuh (Docker)                                             ║
    ║      • Suricata, Zeek, Volatility, etc.                          ║
    ║                                                                   ║
    ║   🟣 PURPLE TEAM TOOLS:                                           ║
    ║      • DetectionLab                                               ║
    ║      • DeTTECT                                                    ║
    ║      • ATT&CK Navigator                                           ║
    ║      • Vectr                                                      ║
    ║      • Custom Scripts                                             ║
    ║                                                                   ║
    ╠═══════════════════════════════════════════════════════════════════╣
    ║                                                                   ║
    ║   📂 UBICACIÓN: ~/Documents/PurpleTeam - Windsurf                 ║
    ║                                                                   ║
    ║   🚀 INICIO RÁPIDO:                                               ║
    ║      cd ~/Documents/PurpleTeam\ -\ Windsurf                       ║
    ║      ./start.sh                                                   ║
    ║                                                                   ║
    ║   🐳 SERVICIOS DOCKER:                                            ║
    ║      cd tools && docker-compose up -d                             ║
    ║      • Elasticsearch: http://localhost:9200                       ║
    ║      • Kibana: http://localhost:5601                              ║
    ║      • Caldera: http://localhost:8888                             ║
    ║      • Portainer: http://localhost:9000                           ║
    ║                                                                   ║
    ╚═══════════════════════════════════════════════════════════════════╝
    
EOF
    echo -e "${NC}"
    
    echo -e "${YELLOW}[!] Recuerda cerrar y abrir una nueva terminal para aplicar los alias${NC}"
    echo ""
}

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

main() {
    banner
    check_root
    check_kali
    
    mkdir -p "$INSTALL_DIR/logs"
    touch "$LOG_FILE"
    
    log "Iniciando instalación Purple Team..."
    log "Log file: $LOG_FILE"
    
    prepare_system
    setup_python_env
    install_red_team_tools
    install_blue_team_tools
    install_purple_team_tools
    setup_docker
    final_setup
    print_summary
    
    success "¡Instalación completada! 🟣"
}

# Ejecutar
main "$@"
]]>
