#!/bin/bash
#############################################################################
#  ██████╗ ███████╗██████╗     ████████╗███████╗ █████╗ ███╗   ███╗
#  ██╔══██╗██╔════╝██╔══██╗    ╚══██╔══╝██╔════╝██╔══██╗████╗ ████║
#  ██████╔╝█████╗  ██║  ██║       ██║   █████╗  ███████║██╔████╔██║
#  ██╔══██╗██╔══╝  ██║  ██║       ██║   ██╔══╝  ██╔══██╗██║╚██╔╝██║
#  ██║  ██║███████╗██████╔╝       ██║   ███████╗██║  ██║██║ ╚═╝ ██║
#  ╚═╝  ╚═╝╚══════╝╚═════╝        ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝
#                    KALI LINUX - ZERO DAY HUNTER
#############################################################################
# Instalador completo del Red Team Workspace
# Ejecutar: chmod +x install.sh && sudo ./install.sh
#############################################################################

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m'

WORKSPACE="/home/xroot/Documents/Proyectos_Kali"

log() { echo -e "${CYAN}[*]${NC} $1"; }
success() { echo -e "${GREEN}[✓]${NC} $1"; }
warning() { echo -e "${YELLOW}[!]${NC} $1"; }
error() { echo -e "${RED}[✗]${NC} $1"; }

echo -e "${RED}"
cat << "EOF"
  ██████╗ ███████╗██████╗     ████████╗███████╗ █████╗ ███╗   ███╗
  ██╔══██╗██╔════╝██╔══██╗    ╚══██╔══╝██╔════╝██╔══██╗████╗ ████║
  ██████╔╝█████╗  ██║  ██║       ██║   █████╗  ███████║██╔████╔██║
  ██╔══██╗██╔══╝  ██║  ██║       ██║   ██╔══╝  ██╔══██╗██║╚██╔╝██║
  ██║  ██║███████╗██████╔╝       ██║   ███████╗██║  ██║██║ ╚═╝ ██║
  ╚═╝  ╚═╝╚══════╝╚═════╝        ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝
              ZERO DAY HUNTER - FULL INSTALLATION
EOF
echo -e "${NC}"

#############################################################################
# FASE 1: ACTUALIZACIÓN DEL SISTEMA
#############################################################################
echo -e "\n${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}[FASE 1/8] ACTUALIZACIÓN DEL SISTEMA${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"

log "Actualizando repositorios..."
apt update -y
apt upgrade -y
success "Sistema actualizado"

#############################################################################
# FASE 2: HERRAMIENTAS DE RECONOCIMIENTO
#############################################################################
echo -e "\n${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}[FASE 2/8] HERRAMIENTAS DE RECONOCIMIENTO${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"

RECON_TOOLS=(
    "nmap"
    "masscan"
    "rustscan"
    "nuclei"
    "subfinder"
    "amass"
    "httpx-toolkit"
    "dnsx"
    "dnsrecon"
    "fierce"
    "theharvester"
    "recon-ng"
    "maltego"
    "spiderfoot"
    "shodan"
    "censys"
)

for tool in "${RECON_TOOLS[@]}"; do
    log "Instalando $tool..."
    apt install -y "$tool" 2>/dev/null || warning "$tool no disponible en apt"
done
success "Herramientas de reconocimiento instaladas"

#############################################################################
# FASE 3: HERRAMIENTAS WEB
#############################################################################
echo -e "\n${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}[FASE 3/8] HERRAMIENTAS WEB${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"

WEB_TOOLS=(
    "gobuster"
    "ffuf"
    "feroxbuster"
    "dirb"
    "dirbuster"
    "nikto"
    "sqlmap"
    "whatweb"
    "wpscan"
    "joomscan"
    "droopescan"
    "commix"
    "xsser"
    "wafw00f"
    "arjun"
    "paramspider"
    "burpsuite"
    "zaproxy"
)

for tool in "${WEB_TOOLS[@]}"; do
    log "Instalando $tool..."
    apt install -y "$tool" 2>/dev/null || warning "$tool no disponible en apt"
done
success "Herramientas web instaladas"

#############################################################################
# FASE 4: FRAMEWORKS DE EXPLOTACIÓN
#############################################################################
echo -e "\n${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}[FASE 4/8] FRAMEWORKS DE EXPLOTACIÓN${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"

EXPLOIT_TOOLS=(
    "metasploit-framework"
    "exploitdb"
    "searchsploit"
    "beef-xss"
    "set"
    "sliver"
    "havoc"
    "covenant"
    "empire"
    "starkiller"
    "crackmapexec"
    "impacket-scripts"
    "evil-winrm"
    "bloodhound"
    "neo4j"
    "responder"
    "mitm6"
    "bettercap"
)

for tool in "${EXPLOIT_TOOLS[@]}"; do
    log "Instalando $tool..."
    apt install -y "$tool" 2>/dev/null || warning "$tool no disponible en apt"
done
success "Frameworks de explotación instalados"

#############################################################################
# FASE 5: HERRAMIENTAS DE PASSWORDS
#############################################################################
echo -e "\n${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}[FASE 5/8] HERRAMIENTAS DE PASSWORDS${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"

PASS_TOOLS=(
    "hydra"
    "john"
    "hashcat"
    "hashid"
    "hash-identifier"
    "crunch"
    "cewl"
    "medusa"
    "ncrack"
    "patator"
    "thc-pptp-bruter"
    "wordlists"
    "seclists"
    "rockyou"
)

for tool in "${PASS_TOOLS[@]}"; do
    log "Instalando $tool..."
    apt install -y "$tool" 2>/dev/null || warning "$tool no disponible en apt"
done

# Descomprimir rockyou si existe
if [ -f /usr/share/wordlists/rockyou.txt.gz ]; then
    log "Descomprimiendo rockyou.txt..."
    gunzip -k /usr/share/wordlists/rockyou.txt.gz 2>/dev/null || true
fi
success "Herramientas de passwords instaladas"

#############################################################################
# FASE 6: HERRAMIENTAS DE RED Y PIVOTING
#############################################################################
echo -e "\n${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}[FASE 6/8] HERRAMIENTAS DE RED Y PIVOTING${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"

NET_TOOLS=(
    "wireshark"
    "tcpdump"
    "tshark"
    "ettercap-graphical"
    "arpspoof"
    "dsniff"
    "mitmproxy"
    "proxychains4"
    "tor"
    "chisel"
    "ligolo-ng"
    "sshuttle"
    "socat"
    "netcat-openbsd"
    "ncat"
    "pwncat"
)

for tool in "${NET_TOOLS[@]}"; do
    log "Instalando $tool..."
    apt install -y "$tool" 2>/dev/null || warning "$tool no disponible en apt"
done
success "Herramientas de red instaladas"

#############################################################################
# FASE 7: GOLANG Y HERRAMIENTAS GO
#############################################################################
echo -e "\n${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}[FASE 7/8] GOLANG Y HERRAMIENTAS GO${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"

log "Instalando Go..."
apt install -y golang-go

export PATH=$PATH:/root/go/bin:/home/xroot/go/bin
echo 'export PATH=$PATH:$HOME/go/bin' >> /home/xroot/.zshrc

GO_TOOLS=(
    "github.com/hahwul/dalfox/v2@latest"
    "github.com/projectdiscovery/katana/cmd/katana@latest"
    "github.com/projectdiscovery/chaos-client/cmd/chaos@latest"
    "github.com/tomnomnom/gf@latest"
    "github.com/tomnomnom/waybackurls@latest"
    "github.com/tomnomnom/assetfinder@latest"
    "github.com/tomnomnom/httprobe@latest"
    "github.com/lc/gau/v2/cmd/gau@latest"
    "github.com/hakluke/hakrawler@latest"
    "github.com/jaeles-project/gospider@latest"
    "github.com/dwisiswant0/crlfuzz/cmd/crlfuzz@latest"
    "github.com/sensepost/gowitness@latest"
)

for tool in "${GO_TOOLS[@]}"; do
    log "Instalando $tool..."
    go install "$tool" 2>/dev/null || warning "Error instalando $tool"
done
success "Herramientas Go instaladas"

#############################################################################
# FASE 8: PYTHON Y LIBRERÍAS
#############################################################################
echo -e "\n${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}[FASE 8/8] PYTHON Y LIBRERÍAS${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"

log "Instalando librerías Python..."
pip3 install --break-system-packages \
    cloudscraper \
    curl_cffi \
    httpx[http2] \
    aiohttp \
    requests \
    beautifulsoup4 \
    lxml \
    pwntools \
    paramiko \
    impacket \
    ldap3 \
    pycryptodome \
    scapy \
    python-nmap \
    shodan \
    censys \
    GitPython \
    PyGithub

success "Librerías Python instaladas"

#############################################################################
# CONFIGURACIÓN DE MCP SERVERS
#############################################################################
echo -e "\n${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}[EXTRA] CONFIGURACIÓN DE MCP SERVERS${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"

log "Instalando Node.js y npm..."
apt install -y nodejs npm

log "Instalando MCP servers..."
npm install -g osint-mcp-server cve-mcp 2>/dev/null || warning "Error con npm global"

log "Habilitando Kali MCP Server..."
apt install -y mcp-kali-server 2>/dev/null || warning "mcp-kali-server no disponible"
systemctl enable kali-server-mcp 2>/dev/null || true
systemctl start kali-server-mcp 2>/dev/null || true

success "MCP Servers configurados"

#############################################################################
# CREAR ESTRUCTURA DE DIRECTORIOS
#############################################################################
echo -e "\n${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}[ESTRUCTURA] CREANDO DIRECTORIOS${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"

mkdir -p "$WORKSPACE"/{recon/{active,passive,osint,apk_analysis},exploitation/{exploits,payloads,shells},post-exploitation/{exfiltration,lateral-movement,persistence},network/{mitm,scanning,sniffing},web/{sqli,xss,lfi-rfi,auth-bypass},wireless/{wifi,bluetooth},social-engineering/{phishing,pretexting},tools/{custom-scripts,configs,wordlists},reports/{findings,templates},credentials,loot,logs,notes}

success "Estructura de directorios creada"

#############################################################################
# INSTALAR COMANDO PWN
#############################################################################
echo -e "\n${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}[PWN] INSTALANDO COMANDO PWN${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"

cat > /usr/local/bin/pwn << 'PWNEOF'
#!/bin/bash
# PWN - DESTRUCCIÓN TOTAL EN UN COMANDO
TARGET="$1"
[[ -z "$TARGET" ]] && echo "Uso: pwn <target>" && exit 1

DOMAIN=$(echo "$TARGET" | sed -E 's|https?://||' | cut -d'/' -f1)
URL="https://$DOMAIN"
RESULTS="/home/xroot/Documents/Proyectos_Kali/recon/active/${DOMAIN}_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$RESULTS" && cd "$RESULTS" || exit

echo -e "\033[0;31m[PWN] Target: $TARGET\033[0m"
echo -e "\033[0;34m[PWN] Output: $RESULTS\033[0m"

# FASE 1: RECON
echo -e "\n\033[0;32m[1/6] RECONOCIMIENTO\033[0m"
subfinder -d "$DOMAIN" -silent > subdomains.txt 2>/dev/null &
nmap -sV -sC -T4 "$DOMAIN" -oN nmap.txt 2>/dev/null &
wait

# FASE 2: HOSTS VIVOS
echo -e "\033[0;32m[2/6] HOSTS VIVOS\033[0m"
cat subdomains.txt 2>/dev/null | httpx -silent | tee live.txt

# FASE 3: NUCLEI
echo -e "\033[0;32m[3/6] VULNERABILITY SCAN\033[0m"
nuclei -u "$URL" -severity critical,high -silent -o nuclei.txt 2>/dev/null &
nikto -h "$URL" -o nikto.txt 2>/dev/null &
wait

# FASE 4: FUZZING
echo -e "\033[0;32m[4/6] FUZZING\033[0m"
ffuf -u "${URL}/FUZZ" -w /usr/share/seclists/Discovery/Web-Content/common.txt -mc 200,301,302,403 -o dirs.json 2>/dev/null

# FASE 5: INJECTION
echo -e "\033[0;32m[5/6] INJECTION TESTS\033[0m"
paramspider -d "$DOMAIN" -o params.txt 2>/dev/null
[[ -f params.txt ]] && head -10 params.txt | xargs -I{} sqlmap -u "{}" --batch --level=2 --dbs 2>/dev/null | tee sqlmap.txt

# FASE 6: EXPLOITS
echo -e "\033[0;32m[6/6] EXPLOIT SEARCH\033[0m"
grep -oP 'CVE-\d{4}-\d+' nuclei.txt 2>/dev/null | while read cve; do
    searchsploit "$cve" 2>/dev/null | head -5
done | tee exploits.txt

echo -e "\n\033[0;31m════════════════════════════════════════\033[0m"
echo -e "\033[0;31m[PWN] COMPLETADO - $DOMAIN\033[0m"
echo -e "Subdominios: $(wc -l < subdomains.txt 2>/dev/null || echo 0)"
echo -e "Vulns: $(wc -l < nuclei.txt 2>/dev/null || echo 0)"
echo -e "Resultados: $RESULTS"
PWNEOF

chmod +x /usr/local/bin/pwn
success "Comando 'pwn' instalado"

#############################################################################
# RESUMEN FINAL
#############################################################################
echo -e "\n${GREEN}"
cat << "EOF"
╔═══════════════════════════════════════════════════════════════════════════╗
║                    ✓ INSTALACIÓN COMPLETADA                               ║
╠═══════════════════════════════════════════════════════════════════════════╣
║  RED TEAM WORKSPACE - ZERO DAY HUNTER                                     ║
║                                                                           ║
║  Herramientas instaladas:                                                 ║
║  • Reconocimiento: nmap, nuclei, subfinder, amass, httpx, shodan         ║
║  • Web: sqlmap, ffuf, burpsuite, nikto, wpscan, dalfox                   ║
║  • Explotación: metasploit, sliver, havoc, beef-xss, searchsploit        ║
║  • Passwords: hydra, john, hashcat, crackmapexec                         ║
║  • Red: wireshark, responder, chisel, proxychains, tor                   ║
║  • MCP: osint-mcp, cve-mcp, kali-mcp-server                              ║
║                                                                           ║
║  Comando rápido: pwn <target>                                             ║
║                                                                           ║
║  Workspace: /home/xroot/Documents/Proyectos_Kali                          ║
╚═══════════════════════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

echo -e "${YELLOW}[!] Reinicia la terminal para aplicar cambios de PATH${NC}"
echo -e "${GREEN}[✓] ¡Listo para cazar zero-days!${NC}"
