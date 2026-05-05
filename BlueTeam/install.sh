#!/bin/bash

#===============================================================================
#
#   ██████╗ ██╗     ██╗   ██╗███████╗████████╗███████╗ █████╗ ███╗   ███╗
#   ██╔══██╗██║     ██║   ██║██╔════╝╚══██╔══╝██╔════╝██╔══██╗████╗ ████║
#   ██████╔╝██║     ██║   ██║█████╗     ██║   █████╗  ███████║██╔████╔██║
#   ██╔══██╗██║     ██║   ██║██╔══╝     ██║   ██╔══╝  ██╔══██║██║╚██╔╝██║
#   ██████╔╝███████╗╚██████╔╝███████╗   ██║   ███████╗██║  ██║██║ ╚═╝ ██║
#   ╚═════╝ ╚══════╝ ╚═════╝ ╚══════╝   ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝
#
#   BlueTeam-Windsurf Installer v2.0
#   Powered by Cascade AI
#
#===============================================================================

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

# Variables
INSTALL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_FILE="$INSTALL_DIR/install.log"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

# Banner
show_banner() {
    clear
    echo -e "${CYAN}"
    echo "╔══════════════════════════════════════════════════════════════════════╗"
    echo "║                                                                      ║"
    echo "║   ██████╗ ██╗     ██╗   ██╗███████╗████████╗███████╗ █████╗ ███╗   ███╗║"
    echo "║   ██╔══██╗██║     ██║   ██║██╔════╝╚══██╔══╝██╔════╝██╔══██╗████╗ ████║║"
    echo "║   ██████╔╝██║     ██║   ██║█████╗     ██║   █████╗  ███████║██╔████╔██║║"
    echo "║   ██╔══██╗██║     ██║   ██║██╔══╝     ██║   ██╔══╝  ██╔══██║██║╚██╔╝██║║"
    echo "║   ██████╔╝███████╗╚██████╔╝███████╗   ██║   ███████╗██║  ██║██║ ╚═╝ ██║║"
    echo "║   ╚═════╝ ╚══════╝ ╚═════╝ ╚══════╝   ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝║"
    echo "║                                                                      ║"
    echo "║              ⚡ Security Operations Center Installer ⚡              ║"
    echo "║                     Powered by Windsurf AI                           ║"
    echo "║                                                                      ║"
    echo "╚══════════════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

# Logging
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

info() {
    echo -e "${BLUE}[i]${NC} $1"
}

# Check root
check_root() {
    if [[ $EUID -ne 0 ]]; then
        error "Este script debe ejecutarse como root"
        echo -e "Ejecuta: ${CYAN}sudo $0${NC}"
        exit 1
    fi
}

# Check OS
check_os() {
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        OS=$NAME
        VER=$VERSION_ID
    fi
    
    log "Sistema detectado: $OS $VER"
    
    if [[ "$OS" != *"Kali"* ]] && [[ "$OS" != *"Debian"* ]] && [[ "$OS" != *"Ubuntu"* ]]; then
        warn "Este script está optimizado para Kali Linux/Debian/Ubuntu"
        read -p "¿Deseas continuar de todos modos? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    fi
}

# Create directory structure
create_directories() {
    log "Creando estructura de directorios..."
    
    directories=(
        "alerts/critical"
        "alerts/high"
        "alerts/medium"
        "alerts/low"
        "forensics/memory"
        "forensics/disk"
        "forensics/network"
        "forensics/artifacts"
        "incidents/active"
        "incidents/resolved"
        "incidents/templates"
        "iocs/hashes"
        "iocs/ips"
        "iocs/domains"
        "iocs/urls"
        "iocs/yara"
        "logs/system"
        "logs/network"
        "logs/application"
        "logs/security"
        "malware/samples"
        "malware/analysis"
        "malware/signatures"
        "playbooks/ransomware"
        "playbooks/phishing"
        "playbooks/malware"
        "playbooks/ddos"
        "playbooks/data-breach"
        "reports/daily"
        "reports/weekly"
        "reports/monthly"
        "reports/incident"
        "rules/yara"
        "rules/sigma"
        "rules/snort"
        "rules/suricata"
        "rules/ossec"
        "threat-intel/feeds"
        "threat-intel/reports"
        "threat-intel/actors"
        "tools/custom-scripts"
        "config/wazuh"
        "config/suricata"
        "config/snort"
        "config/ossec"
        ".windsurf/workflows"
    )
    
    for dir in "${directories[@]}"; do
        mkdir -p "$INSTALL_DIR/$dir"
    done
    
    success "Estructura de directorios creada"
}

# Update system
update_system() {
    log "Actualizando sistema..."
    apt-get update -qq
    apt-get upgrade -y -qq
    success "Sistema actualizado"
}

# Install dependencies
install_dependencies() {
    log "Instalando dependencias base..."
    
    apt-get install -y -qq \
        curl \
        wget \
        git \
        vim \
        nano \
        htop \
        tmux \
        screen \
        jq \
        yq \
        tree \
        unzip \
        p7zip-full \
        build-essential \
        cmake \
        pkg-config \
        libssl-dev \
        libffi-dev \
        python3 \
        python3-pip \
        python3-venv \
        python3-dev \
        golang \
        ruby \
        ruby-dev \
        nodejs \
        npm \
        default-jdk \
        docker.io \
        docker-compose \
        apt-transport-https \
        ca-certificates \
        gnupg \
        lsb-release \
        software-properties-common
    
    # Enable Docker
    systemctl enable docker 2>/dev/null || true
    systemctl start docker 2>/dev/null || true
    
    success "Dependencias base instaladas"
}

# Install Python packages
install_python_packages() {
    log "Instalando paquetes Python..."
    
    pip3 install --upgrade pip --quiet
    
    pip3 install --quiet \
        requests \
        beautifulsoup4 \
        lxml \
        pandas \
        numpy \
        scikit-learn \
        matplotlib \
        seaborn \
        plotly \
        yara-python \
        pefile \
        oletools \
        python-magic \
        ssdeep \
        pymisp \
        thehive4py \
        cortex4py \
        stix2 \
        taxii2-client \
        sigma-cli \
        volatility3 \
        scapy \
        dpkt \
        pyshark \
        impacket \
        ldap3 \
        paramiko \
        fabric \
        ansible \
        rich \
        typer \
        click \
        colorama \
        tqdm \
        python-dateutil \
        pytz \
        croniter \
        schedule \
        watchdog \
        psutil \
        netifaces \
        dnspython \
        ipwhois \
        geoip2 \
        maxminddb \
        elasticsearch \
        redis \
        pymongo \
        sqlalchemy \
        flask \
        fastapi \
        uvicorn \
        celery \
        pyyaml \
        toml \
        configparser \
        python-dotenv \
        cryptography \
        pycryptodome \
        hashlib \
        virustotal-api \
        OTXv2 \
        shodan \
        censys
    
    success "Paquetes Python instalados"
}

#===============================================================================
# SIEM & LOG MANAGEMENT
#===============================================================================

install_wazuh() {
    log "Instalando Wazuh SIEM..."
    
    # Add Wazuh repository
    curl -s https://packages.wazuh.com/key/GPG-KEY-WAZUH | gpg --dearmor -o /usr/share/keyrings/wazuh.gpg
    echo "deb [signed-by=/usr/share/keyrings/wazuh.gpg] https://packages.wazuh.com/4.x/apt/ stable main" | tee /etc/apt/sources.list.d/wazuh.list
    
    apt-get update -qq
    apt-get install -y -qq wazuh-manager wazuh-agent 2>/dev/null || warn "Wazuh requiere configuración adicional"
    
    success "Wazuh instalado"
}

install_ossec() {
    log "Instalando OSSEC HIDS..."
    
    apt-get install -y -qq ossec-hids ossec-hids-server 2>/dev/null || {
        # Manual installation
        cd /tmp
        wget -q https://github.com/ossec/ossec-hids/archive/3.7.0.tar.gz -O ossec.tar.gz
        tar -xzf ossec.tar.gz
        cd ossec-hids-3.7.0
        ./install.sh local <<< $'en\n\n\n\n\n\n' 2>/dev/null || warn "OSSEC requiere instalación manual"
        cd "$INSTALL_DIR"
    }
    
    success "OSSEC instalado"
}

install_elastic_stack() {
    log "Instalando Elastic Stack (ELK)..."
    
    # Add Elastic repository
    wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | gpg --dearmor -o /usr/share/keyrings/elastic.gpg
    echo "deb [signed-by=/usr/share/keyrings/elastic.gpg] https://artifacts.elastic.co/packages/8.x/apt stable main" | tee /etc/apt/sources.list.d/elastic-8.x.list
    
    apt-get update -qq
    apt-get install -y -qq elasticsearch kibana logstash filebeat metricbeat auditbeat packetbeat 2>/dev/null || warn "ELK requiere configuración adicional"
    
    success "Elastic Stack instalado"
}

install_graylog() {
    log "Instalando Graylog..."
    
    # MongoDB
    apt-get install -y -qq mongodb-org 2>/dev/null || apt-get install -y -qq mongodb
    
    # Graylog
    wget -q https://packages.graylog2.org/repo/packages/graylog-5.2-repository_latest.deb
    dpkg -i graylog-5.2-repository_latest.deb 2>/dev/null || true
    apt-get update -qq
    apt-get install -y -qq graylog-server 2>/dev/null || warn "Graylog requiere configuración adicional"
    rm -f graylog-5.2-repository_latest.deb
    
    success "Graylog instalado"
}

install_splunk() {
    log "Instalando Splunk Free..."
    
    # Splunk requires manual download due to license
    info "Splunk requiere descarga manual desde: https://www.splunk.com/en_us/download/splunk-enterprise.html"
    info "Después de descargar, ejecuta: dpkg -i splunk-*.deb && /opt/splunk/bin/splunk start --accept-license"
    
    success "Instrucciones de Splunk proporcionadas"
}

#===============================================================================
# IDS/IPS
#===============================================================================

install_snort() {
    log "Instalando Snort IDS..."
    
    apt-get install -y -qq snort 2>/dev/null || {
        # Build from source
        apt-get install -y -qq libpcap-dev libpcre3-dev libdumbnet-dev bison flex zlib1g-dev liblzma-dev openssl libssl-dev libnghttp2-dev
        cd /tmp
        wget -q https://www.snort.org/downloads/snort/snort-2.9.20.tar.gz -O snort.tar.gz
        tar -xzf snort.tar.gz
        cd snort-2.9.20
        ./configure --enable-sourcefire && make && make install
        ldconfig
        cd "$INSTALL_DIR"
    }
    
    # Download community rules
    mkdir -p /etc/snort/rules
    wget -q https://www.snort.org/downloads/community/community-rules.tar.gz -O /tmp/community-rules.tar.gz
    tar -xzf /tmp/community-rules.tar.gz -C /etc/snort/rules/ 2>/dev/null || true
    
    success "Snort instalado"
}

install_suricata() {
    log "Instalando Suricata IDS/IPS..."
    
    add-apt-repository -y ppa:oisf/suricata-stable 2>/dev/null || true
    apt-get update -qq
    apt-get install -y -qq suricata suricata-update
    
    # Update rules
    suricata-update 2>/dev/null || true
    
    # Copy config
    cp /etc/suricata/suricata.yaml "$INSTALL_DIR/config/suricata/" 2>/dev/null || true
    
    success "Suricata instalado"
}

install_zeek() {
    log "Instalando Zeek (Bro) Network Monitor..."
    
    echo 'deb http://download.opensuse.org/repositories/security:/zeek/xUbuntu_22.04/ /' | tee /etc/apt/sources.list.d/zeek.list
    curl -fsSL https://download.opensuse.org/repositories/security:zeek/xUbuntu_22.04/Release.key | gpg --dearmor | tee /etc/apt/trusted.gpg.d/zeek.gpg > /dev/null
    apt-get update -qq
    apt-get install -y -qq zeek 2>/dev/null || apt-get install -y -qq bro
    
    # Add to PATH
    echo 'export PATH=$PATH:/opt/zeek/bin' >> /etc/profile.d/zeek.sh
    
    success "Zeek instalado"
}

install_fail2ban() {
    log "Instalando Fail2Ban..."
    
    apt-get install -y -qq fail2ban
    
    # Configure
    cat > /etc/fail2ban/jail.local << 'EOF'
[DEFAULT]
bantime = 3600
findtime = 600
maxretry = 3
backend = systemd

[sshd]
enabled = true
port = ssh
filter = sshd
logpath = /var/log/auth.log
maxretry = 3

[apache-auth]
enabled = true

[nginx-http-auth]
enabled = true
EOF
    
    systemctl enable fail2ban
    systemctl restart fail2ban
    
    success "Fail2Ban instalado y configurado"
}

#===============================================================================
# FORENSICS
#===============================================================================

install_autopsy() {
    log "Instalando Autopsy Digital Forensics..."
    
    apt-get install -y -qq autopsy sleuthkit 2>/dev/null || {
        # Install Sleuth Kit first
        apt-get install -y -qq sleuthkit
        
        # Download Autopsy
        cd /tmp
        wget -q https://github.com/sleuthkit/autopsy/releases/download/autopsy-4.21.0/autopsy-4.21.0.zip -O autopsy.zip
        unzip -q autopsy.zip -d /opt/
        chmod +x /opt/autopsy-4.21.0/bin/autopsy
        ln -sf /opt/autopsy-4.21.0/bin/autopsy /usr/local/bin/autopsy
        cd "$INSTALL_DIR"
    }
    
    success "Autopsy instalado"
}

install_volatility() {
    log "Instalando Volatility Memory Forensics..."
    
    # Volatility 3
    pip3 install volatility3 --quiet
    
    # Volatility 2 (legacy)
    cd /tmp
    git clone --quiet https://github.com/volatilityfoundation/volatility.git /opt/volatility2 2>/dev/null || true
    
    # Download symbols
    mkdir -p /opt/volatility3/symbols
    cd /opt/volatility3/symbols
    wget -q https://downloads.volatilityfoundation.org/volatility3/symbols/windows.zip 2>/dev/null || true
    wget -q https://downloads.volatilityfoundation.org/volatility3/symbols/linux.zip 2>/dev/null || true
    wget -q https://downloads.volatilityfoundation.org/volatility3/symbols/mac.zip 2>/dev/null || true
    
    cd "$INSTALL_DIR"
    success "Volatility instalado"
}

install_forensic_tools() {
    log "Instalando herramientas forenses adicionales..."
    
    apt-get install -y -qq \
        foremost \
        scalpel \
        binwalk \
        bulk-extractor \
        dc3dd \
        dcfldd \
        guymager \
        ewf-tools \
        afflib-tools \
        libewf-dev \
        plaso \
        log2timeline \
        pff-tools \
        libesedb-utils \
        libvshadow-utils \
        regripper \
        yara \
        ssdeep \
        hashdeep \
        md5deep \
        exiftool \
        pdfid \
        pdf-parser \
        oletools \
        olevba \
        xxd \
        hexedit \
        radare2 \
        ghidra 2>/dev/null || true
    
    success "Herramientas forenses instaladas"
}

#===============================================================================
# NETWORK ANALYSIS
#===============================================================================

install_network_tools() {
    log "Instalando herramientas de análisis de red..."
    
    apt-get install -y -qq \
        wireshark \
        tshark \
        tcpdump \
        ngrep \
        tcpflow \
        tcpreplay \
        tcpick \
        tcptrack \
        iftop \
        nethogs \
        bmon \
        iptraf-ng \
        darkstat \
        ntopng \
        nmap \
        masscan \
        zmap \
        netcat-openbsd \
        socat \
        hping3 \
        arping \
        arpwatch \
        arp-scan \
        fping \
        mtr \
        traceroute \
        whois \
        dnsutils \
        dnsenum \
        dnsrecon \
        fierce \
        p0f \
        ettercap-text-only \
        bettercap \
        responder \
        mitmproxy 2>/dev/null || true
    
    # NetworkMiner
    cd /tmp
    wget -q https://www.netresec.com/?download=NetworkMiner -O networkminer.zip 2>/dev/null || true
    unzip -q networkminer.zip -d /opt/ 2>/dev/null || true
    
    cd "$INSTALL_DIR"
    success "Herramientas de red instaladas"
}

#===============================================================================
# MALWARE ANALYSIS
#===============================================================================

install_malware_tools() {
    log "Instalando herramientas de análisis de malware..."
    
    apt-get install -y -qq \
        yara \
        clamav \
        clamav-daemon \
        clamav-freshclam \
        radare2 \
        python3-pefile \
        upx-ucl \
        strace \
        ltrace \
        gdb \
        edb-debugger 2>/dev/null || true
    
    # Update ClamAV
    freshclam 2>/dev/null || true
    
    # YARA rules
    cd "$INSTALL_DIR/rules/yara"
    git clone --quiet https://github.com/Yara-Rules/rules.git yara-rules 2>/dev/null || true
    git clone --quiet https://github.com/Neo23x0/signature-base.git signature-base 2>/dev/null || true
    
    # Ghidra
    if ! command -v ghidra &> /dev/null; then
        cd /tmp
        wget -q https://github.com/NationalSecurityAgency/ghidra/releases/download/Ghidra_11.0.1_build/ghidra_11.0.1_PUBLIC_20240130.zip -O ghidra.zip 2>/dev/null || true
        unzip -q ghidra.zip -d /opt/ 2>/dev/null || true
        ln -sf /opt/ghidra_*/ghidraRun /usr/local/bin/ghidra 2>/dev/null || true
    fi
    
    # Cuckoo Sandbox (Docker)
    docker pull cuckoo/cuckoo 2>/dev/null || true
    
    cd "$INSTALL_DIR"
    success "Herramientas de malware instaladas"
}

#===============================================================================
# THREAT INTELLIGENCE
#===============================================================================

install_threat_intel() {
    log "Instalando plataformas de Threat Intelligence..."
    
    # MISP (Docker)
    cd /tmp
    git clone --quiet https://github.com/MISP/misp-docker.git 2>/dev/null || true
    
    # TheHive (Docker)
    docker pull strangebee/thehive:5 2>/dev/null || true
    
    # Cortex (Docker)
    docker pull thehiveproject/cortex:3.1.7 2>/dev/null || true
    
    # OpenCTI (Docker)
    git clone --quiet https://github.com/OpenCTI-Platform/docker.git /opt/opencti-docker 2>/dev/null || true
    
    # YETI
    pip3 install yeti --quiet 2>/dev/null || true
    
    # SpiderFoot
    pip3 install spiderfoot --quiet 2>/dev/null || true
    
    # Shodan CLI
    pip3 install shodan --quiet
    
    # Maltego
    apt-get install -y -qq maltego 2>/dev/null || true
    
    cd "$INSTALL_DIR"
    success "Plataformas de Threat Intel instaladas"
}

#===============================================================================
# EDR & ENDPOINT
#===============================================================================

install_edr_tools() {
    log "Instalando herramientas EDR..."
    
    # OSQuery
    curl -L https://pkg.osquery.io/deb/osquery.gpg | apt-key add -
    echo "deb [arch=amd64] https://pkg.osquery.io/deb deb main" | tee /etc/apt/sources.list.d/osquery.list
    apt-get update -qq
    apt-get install -y -qq osquery 2>/dev/null || true
    
    # Velociraptor
    cd /tmp
    wget -q https://github.com/Velocidex/velociraptor/releases/download/v0.7.0/velociraptor-v0.7.0-linux-amd64 -O /usr/local/bin/velociraptor 2>/dev/null || true
    chmod +x /usr/local/bin/velociraptor 2>/dev/null || true
    
    # Sysdig
    curl -s https://s3.amazonaws.com/download.draios.com/stable/install-sysdig | bash 2>/dev/null || true
    
    # Falco
    curl -fsSL https://falco.org/repo/falcosecurity-packages.asc | gpg --dearmor -o /usr/share/keyrings/falco-archive-keyring.gpg
    echo "deb [signed-by=/usr/share/keyrings/falco-archive-keyring.gpg] https://download.falco.org/packages/deb stable main" | tee /etc/apt/sources.list.d/falcosecurity.list
    apt-get update -qq
    apt-get install -y -qq falco 2>/dev/null || true
    
    # Auditd
    apt-get install -y -qq auditd audispd-plugins
    
    cd "$INSTALL_DIR"
    success "Herramientas EDR instaladas"
}

#===============================================================================
# HONEYPOTS
#===============================================================================

install_honeypots() {
    log "Instalando Honeypots..."
    
    # Cowrie SSH Honeypot
    cd /opt
    git clone --quiet https://github.com/cowrie/cowrie.git 2>/dev/null || true
    
    # Dionaea
    apt-get install -y -qq dionaea 2>/dev/null || {
        docker pull dinotools/dionaea 2>/dev/null || true
    }
    
    # T-Pot (All-in-one)
    git clone --quiet https://github.com/telekom-security/tpotce.git /opt/tpot 2>/dev/null || true
    
    # HoneyPy
    pip3 install honeypy --quiet 2>/dev/null || true
    
    cd "$INSTALL_DIR"
    success "Honeypots instalados"
}

#===============================================================================
# VISUALIZATION
#===============================================================================

install_visualization() {
    log "Instalando herramientas de visualización..."
    
    # Grafana
    wget -q -O /usr/share/keyrings/grafana.key https://apt.grafana.com/gpg.key
    echo "deb [signed-by=/usr/share/keyrings/grafana.key] https://apt.grafana.com stable main" | tee /etc/apt/sources.list.d/grafana.list
    apt-get update -qq
    apt-get install -y -qq grafana
    
    # Prometheus
    apt-get install -y -qq prometheus prometheus-node-exporter 2>/dev/null || true
    
    success "Herramientas de visualización instaladas"
}

#===============================================================================
# VULNERABILITY SCANNING
#===============================================================================

install_vuln_scanners() {
    log "Instalando escáneres de vulnerabilidades..."
    
    apt-get install -y -qq \
        nikto \
        wapiti \
        skipfish \
        sqlmap \
        commix \
        xsser \
        lynis \
        chkrootkit \
        rkhunter 2>/dev/null || true
    
    # Nuclei
    go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest 2>/dev/null || true
    
    # Trivy
    wget -qO - https://aquasecurity.github.io/trivy-repo/deb/public.key | gpg --dearmor | tee /usr/share/keyrings/trivy.gpg > /dev/null
    echo "deb [signed-by=/usr/share/keyrings/trivy.gpg] https://aquasecurity.github.io/trivy-repo/deb generic main" | tee /etc/apt/sources.list.d/trivy.list
    apt-get update -qq
    apt-get install -y -qq trivy 2>/dev/null || true
    
    # OpenVAS
    apt-get install -y -qq openvas gvm 2>/dev/null || true
    
    success "Escáneres de vulnerabilidades instalados"
}

#===============================================================================
# SIGMA RULES
#===============================================================================

install_sigma_rules() {
    log "Instalando reglas Sigma..."
    
    cd "$INSTALL_DIR/rules/sigma"
    git clone --quiet https://github.com/SigmaHQ/sigma.git 2>/dev/null || true
    
    pip3 install sigma-cli pySigma --quiet
    
    success "Reglas Sigma instaladas"
}

#===============================================================================
# DOWNLOAD IOC FEEDS
#===============================================================================

download_ioc_feeds() {
    log "Descargando feeds de IOCs..."
    
    cd "$INSTALL_DIR/iocs"
    
    # IP Blacklists
    wget -q https://raw.githubusercontent.com/stamparm/ipsum/master/ipsum.txt -O ips/ipsum.txt 2>/dev/null || true
    wget -q https://rules.emergingthreats.net/blockrules/compromised-ips.txt -O ips/et-compromised.txt 2>/dev/null || true
    wget -q https://www.spamhaus.org/drop/drop.txt -O ips/spamhaus-drop.txt 2>/dev/null || true
    
    # Domain Blacklists
    wget -q https://urlhaus.abuse.ch/downloads/text/ -O domains/urlhaus.txt 2>/dev/null || true
    wget -q https://openphish.com/feed.txt -O domains/openphish.txt 2>/dev/null || true
    
    # Hash Lists
    wget -q https://bazaar.abuse.ch/export/txt/sha256/recent/ -O hashes/malwarebazaar.txt 2>/dev/null || true
    
    cd "$INSTALL_DIR"
    success "Feeds de IOCs descargados"
}

#===============================================================================
# CONFIGURE SERVICES
#===============================================================================

configure_services() {
    log "Configurando servicios..."
    
    # Enable services
    systemctl enable elasticsearch 2>/dev/null || true
    systemctl enable kibana 2>/dev/null || true
    systemctl enable logstash 2>/dev/null || true
    systemctl enable grafana-server 2>/dev/null || true
    systemctl enable prometheus 2>/dev/null || true
    systemctl enable suricata 2>/dev/null || true
    systemctl enable fail2ban 2>/dev/null || true
    systemctl enable auditd 2>/dev/null || true
    systemctl enable osqueryd 2>/dev/null || true
    
    success "Servicios configurados"
}

#===============================================================================
# CREATE ALIASES
#===============================================================================

create_aliases() {
    log "Creando aliases útiles..."
    
    cat >> ~/.bashrc << 'EOF'

# BlueTeam Aliases
alias bt-detect='$HOME/Documents/BlueTeam-Windsurf/tools/custom-scripts/detect.sh'
alias bt-respond='python3 $HOME/Documents/BlueTeam-Windsurf/tools/custom-scripts/incident_response.py'
alias bt-analyze='python3 $HOME/Documents/BlueTeam-Windsurf/tools/custom-scripts/log_analyzer.py'
alias bt-hunt='$HOME/Documents/BlueTeam-Windsurf/tools/custom-scripts/threat_hunter.sh'
alias bt-forensics='$HOME/Documents/BlueTeam-Windsurf/tools/custom-scripts/forensic_collector.sh'

# Quick commands
alias logs='tail -f /var/log/syslog'
alias authlog='tail -f /var/log/auth.log'
alias netstat-listen='netstat -tlnp'
alias ps-tree='ps auxf'
alias connections='ss -tunapl'
alias firewall='iptables -L -n -v'

# Suricata
alias suricata-logs='tail -f /var/log/suricata/fast.log'
alias suricata-alerts='tail -f /var/log/suricata/eve.json | jq'

# Zeek
alias zeek-logs='tail -f /opt/zeek/logs/current/conn.log'

EOF
    
    success "Aliases creados"
}

#===============================================================================
# PRINT SUMMARY
#===============================================================================

print_summary() {
    echo ""
    echo -e "${GREEN}╔══════════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║                    INSTALACIÓN COMPLETADA                            ║${NC}"
    echo -e "${GREEN}╚══════════════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "${CYAN}📁 Directorio de instalación:${NC} $INSTALL_DIR"
    echo -e "${CYAN}📋 Log de instalación:${NC} $LOG_FILE"
    echo ""
    echo -e "${YELLOW}🔧 Servicios instalados:${NC}"
    echo "   • SIEM: Wazuh, OSSEC, Elastic Stack, Graylog"
    echo "   • IDS/IPS: Snort, Suricata, Zeek, Fail2Ban"
    echo "   • Forensics: Autopsy, Volatility, Sleuth Kit"
    echo "   • Network: Wireshark, tcpdump, NetworkMiner"
    echo "   • Malware: YARA, ClamAV, Ghidra, Radare2"
    echo "   • Threat Intel: MISP, TheHive, Cortex (Docker)"
    echo "   • EDR: Velociraptor, OSQuery, Falco, Sysdig"
    echo "   • Honeypots: Cowrie, Dionaea, T-Pot"
    echo "   • Visualization: Grafana, Kibana, Prometheus"
    echo ""
    echo -e "${YELLOW}🚀 Comandos rápidos:${NC}"
    echo "   bt-detect    - Detectar amenazas"
    echo "   bt-respond   - Responder a incidentes"
    echo "   bt-analyze   - Analizar logs"
    echo "   bt-hunt      - Threat hunting"
    echo "   bt-forensics - Recolección forense"
    echo ""
    echo -e "${YELLOW}📖 Workflows de Cascade AI:${NC}"
    echo "   /detect      - Detectar amenazas en logs"
    echo "   /investigate - Investigar incidente"
    echo "   /respond     - Responder a incidente"
    echo "   /hunt        - Threat hunting proactivo"
    echo "   /forensics   - Análisis forense"
    echo ""
    echo -e "${GREEN}✅ BlueTeam-Windsurf está listo para defender!${NC}"
    echo ""
}

#===============================================================================
# MAIN
#===============================================================================

main() {
    show_banner
    check_root
    check_os
    
    echo ""
    echo -e "${CYAN}Selecciona el tipo de instalación:${NC}"
    echo ""
    echo "  1) Full        - Instalación completa (todas las herramientas)"
    echo "  2) Minimal     - Solo herramientas esenciales"
    echo "  3) SIEM        - Solo SIEM y log management"
    echo "  4) IDS         - Solo IDS/IPS"
    echo "  5) Forensics   - Solo herramientas forenses"
    echo "  6) Network     - Solo análisis de red"
    echo "  7) Malware     - Solo análisis de malware"
    echo "  8) Threat-Intel- Solo threat intelligence"
    echo "  9) Custom      - Selección personalizada"
    echo ""
    
    # Check for command line arguments
    case "$1" in
        --full)
            INSTALL_TYPE=1
            ;;
        --minimal)
            INSTALL_TYPE=2
            ;;
        --siem)
            INSTALL_TYPE=3
            ;;
        --ids)
            INSTALL_TYPE=4
            ;;
        --forensics)
            INSTALL_TYPE=5
            ;;
        --network)
            INSTALL_TYPE=6
            ;;
        --malware)
            INSTALL_TYPE=7
            ;;
        --threat-intel)
            INSTALL_TYPE=8
            ;;
        *)
            read -p "Selección [1-9]: " INSTALL_TYPE
            ;;
    esac
    
    echo ""
    log "Iniciando instalación tipo $INSTALL_TYPE..."
    echo ""
    
    # Always create directories and install dependencies
    create_directories
    update_system
    install_dependencies
    install_python_packages
    
    case $INSTALL_TYPE in
        1) # Full
            install_wazuh
            install_ossec
            install_elastic_stack
            install_graylog
            install_splunk
            install_snort
            install_suricata
            install_zeek
            install_fail2ban
            install_autopsy
            install_volatility
            install_forensic_tools
            install_network_tools
            install_malware_tools
            install_threat_intel
            install_edr_tools
            install_honeypots
            install_visualization
            install_vuln_scanners
            install_sigma_rules
            download_ioc_feeds
            ;;
        2) # Minimal
            install_suricata
            install_fail2ban
            install_network_tools
            install_forensic_tools
            install_sigma_rules
            ;;
        3) # SIEM
            install_wazuh
            install_ossec
            install_elastic_stack
            install_graylog
            ;;
        4) # IDS
            install_snort
            install_suricata
            install_zeek
            install_fail2ban
            ;;
        5) # Forensics
            install_autopsy
            install_volatility
            install_forensic_tools
            ;;
        6) # Network
            install_network_tools
            install_zeek
            ;;
        7) # Malware
            install_malware_tools
            ;;
        8) # Threat Intel
            install_threat_intel
            download_ioc_feeds
            ;;
        9) # Custom
            echo "Selecciona los componentes a instalar (s/n):"
            read -p "SIEM (Wazuh, OSSEC, ELK)? " -n 1 -r; echo
            [[ $REPLY =~ ^[Yy]$ ]] && { install_wazuh; install_ossec; install_elastic_stack; }
            
            read -p "IDS/IPS (Snort, Suricata, Zeek)? " -n 1 -r; echo
            [[ $REPLY =~ ^[Yy]$ ]] && { install_snort; install_suricata; install_zeek; }
            
            read -p "Forensics (Autopsy, Volatility)? " -n 1 -r; echo
            [[ $REPLY =~ ^[Yy]$ ]] && { install_autopsy; install_volatility; install_forensic_tools; }
            
            read -p "Network Analysis? " -n 1 -r; echo
            [[ $REPLY =~ ^[Yy]$ ]] && install_network_tools
            
            read -p "Malware Analysis? " -n 1 -r; echo
            [[ $REPLY =~ ^[Yy]$ ]] && install_malware_tools
            
            read -p "Threat Intelligence? " -n 1 -r; echo
            [[ $REPLY =~ ^[Yy]$ ]] && install_threat_intel
            
            read -p "EDR Tools? " -n 1 -r; echo
            [[ $REPLY =~ ^[Yy]$ ]] && install_edr_tools
            
            read -p "Honeypots? " -n 1 -r; echo
            [[ $REPLY =~ ^[Yy]$ ]] && install_honeypots
            
            read -p "Visualization (Grafana, Kibana)? " -n 1 -r; echo
            [[ $REPLY =~ ^[Yy]$ ]] && install_visualization
            ;;
    esac
    
    configure_services
    create_aliases
    print_summary
}

# Run
main "$@"
