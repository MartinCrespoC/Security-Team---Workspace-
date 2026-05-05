#!/bin/bash
# Quick Recon Script - Reconocimiento rápido de un target
# Uso: ./quick_recon.sh <TARGET_IP>

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

if [ -z "$1" ]; then
    echo -e "${RED}[!] Uso: $0 <TARGET_IP>${NC}"
    exit 1
fi

TARGET=$1
OUTPUT_DIR="../recon/active/$(date +%Y%m%d)_${TARGET}"
mkdir -p "$OUTPUT_DIR"

echo -e "${BLUE}[*] Iniciando reconocimiento de: ${TARGET}${NC}"
echo -e "${BLUE}[*] Output: ${OUTPUT_DIR}${NC}"
echo ""

# Ping check
echo -e "${YELLOW}[+] Verificando conectividad...${NC}"
if ping -c 1 "$TARGET" &> /dev/null; then
    echo -e "${GREEN}[✓] Host activo${NC}"
else
    echo -e "${RED}[!] Host no responde a ping (puede tener firewall)${NC}"
fi

# Quick port scan
echo -e "${YELLOW}[+] Escaneo rápido de puertos (top 1000)...${NC}"
nmap -sT -T4 --top-ports 1000 -oN "$OUTPUT_DIR/quick_scan.txt" "$TARGET"

# Service version detection on open ports
echo -e "${YELLOW}[+] Detectando versiones de servicios...${NC}"
nmap -sV -sC -oN "$OUTPUT_DIR/service_scan.txt" "$TARGET"

# Check for common web ports
if nmap -p 80,443,8080,8443 "$TARGET" | grep -q "open"; then
    echo -e "${YELLOW}[+] Puertos web detectados, ejecutando whatweb...${NC}"
    whatweb "http://$TARGET" 2>/dev/null | tee "$OUTPUT_DIR/whatweb_http.txt"
    whatweb "https://$TARGET" 2>/dev/null | tee "$OUTPUT_DIR/whatweb_https.txt"
fi

# Summary
echo ""
echo -e "${GREEN}[✓] Reconocimiento completado${NC}"
echo -e "${BLUE}[*] Resultados guardados en: ${OUTPUT_DIR}${NC}"
echo ""
echo -e "${YELLOW}Archivos generados:${NC}"
ls -la "$OUTPUT_DIR"
