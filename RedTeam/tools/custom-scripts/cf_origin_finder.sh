#!/bin/bash
# Cloudflare Origin IP Finder
# Busca la IP real detrás de Cloudflare

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

if [ -z "$1" ]; then
    echo "Uso: $0 <dominio>"
    echo "Ejemplo: $0 example.com"
    exit 1
fi

DOMAIN=$1
OUTPUT_DIR="/home/xroot/Documents/Proyectos_Kali/recon/active/cf_bypass"
mkdir -p $OUTPUT_DIR

echo -e "${BLUE}[*] Buscando IP origen para: ${DOMAIN}${NC}"
echo "=============================================="

# 1. Verificar si está en Cloudflare
echo -e "\n${YELLOW}[1] Verificando Cloudflare...${NC}"
CF_CHECK=$(curl -sI "https://$DOMAIN" 2>/dev/null | grep -i "cf-ray\|cloudflare")
if [ -n "$CF_CHECK" ]; then
    echo -e "${RED}[!] Cloudflare DETECTADO${NC}"
    echo "$CF_CHECK"
else
    echo -e "${GREEN}[+] No parece estar en Cloudflare${NC}"
fi

# 2. Buscar subdominios que podrían exponer IP real
echo -e "\n${YELLOW}[2] Buscando subdominios sin CF...${NC}"
SUBS_TO_CHECK=(
    "direct" "origin" "server" "backend" "api" "mail" "ftp" 
    "cpanel" "webmail" "admin" "dev" "staging" "test" "old"
    "www2" "secure" "portal" "internal" "intranet" "vpn"
    "mx" "smtp" "pop" "imap" "ns1" "ns2" "dns"
)

for sub in "${SUBS_TO_CHECK[@]}"; do
    FULL="${sub}.${DOMAIN}"
    IP=$(dig +short $FULL 2>/dev/null | head -1)
    if [ -n "$IP" ]; then
        # Verificar si es IP de Cloudflare
        if [[ ! $IP =~ ^104\. ]] && [[ ! $IP =~ ^172\.6[4-9]\. ]] && [[ ! $IP =~ ^172\.[7-9][0-9]\. ]] && [[ ! $IP =~ ^103\.21\. ]] && [[ ! $IP =~ ^103\.22\. ]] && [[ ! $IP =~ ^103\.31\. ]] && [[ ! $IP =~ ^141\.101\. ]] && [[ ! $IP =~ ^108\.162\. ]] && [[ ! $IP =~ ^190\.93\. ]] && [[ ! $IP =~ ^188\.114\. ]] && [[ ! $IP =~ ^197\.234\. ]] && [[ ! $IP =~ ^198\.41\. ]] && [[ ! $IP =~ ^162\.158\. ]] && [[ ! $IP =~ ^173\.245\. ]]; then
            echo -e "${GREEN}[+] $FULL -> $IP (POSIBLE ORIGEN)${NC}"
            echo "$FULL,$IP" >> "$OUTPUT_DIR/${DOMAIN}_origins.txt"
        else
            echo -e "    $FULL -> $IP (Cloudflare)"
        fi
    fi
done

# 3. Buscar en registros MX (mail servers suelen exponer IP real)
echo -e "\n${YELLOW}[3] Verificando registros MX...${NC}"
MX_RECORDS=$(dig +short MX $DOMAIN 2>/dev/null)
if [ -n "$MX_RECORDS" ]; then
    echo "$MX_RECORDS" | while read priority mx; do
        MX_IP=$(dig +short $mx 2>/dev/null | head -1)
        if [ -n "$MX_IP" ]; then
            echo -e "${GREEN}[+] MX: $mx -> $MX_IP${NC}"
            echo "MX,$mx,$MX_IP" >> "$OUTPUT_DIR/${DOMAIN}_origins.txt"
        fi
    done
fi

# 4. Buscar en SPF (puede contener IPs del servidor)
echo -e "\n${YELLOW}[4] Analizando SPF...${NC}"
SPF=$(dig +short TXT $DOMAIN 2>/dev/null | grep "v=spf1")
if [ -n "$SPF" ]; then
    echo "$SPF"
    # Extraer IPs del SPF
    echo "$SPF" | grep -oE "ip4:[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+" | while read ip; do
        IP_CLEAN=$(echo $ip | cut -d: -f2)
        echo -e "${GREEN}[+] SPF IP: $IP_CLEAN${NC}"
        echo "SPF,$IP_CLEAN" >> "$OUTPUT_DIR/${DOMAIN}_origins.txt"
    done
fi

# 5. Buscar en histórico de DNS (SecurityTrails, etc.)
echo -e "\n${YELLOW}[5] Buscando en fuentes OSINT...${NC}"

# Usar subfinder para más subdominios
echo "[*] Ejecutando subfinder..."
subfinder -d $DOMAIN -silent 2>/dev/null | head -50 | while read sub; do
    IP=$(dig +short $sub 2>/dev/null | head -1)
    if [ -n "$IP" ]; then
        if [[ ! $IP =~ ^104\. ]] && [[ ! $IP =~ ^172\.6 ]] && [[ ! $IP =~ ^103\. ]] && [[ ! $IP =~ ^141\.101\. ]]; then
            echo -e "${GREEN}[+] $sub -> $IP${NC}"
            echo "$sub,$IP" >> "$OUTPUT_DIR/${DOMAIN}_origins.txt"
        fi
    fi
done

# 6. Buscar en Shodan/Censys por el dominio
echo -e "\n${YELLOW}[6] Buscando en certificados SSL...${NC}"
# Usar crt.sh para buscar certificados
curl -s "https://crt.sh/?q=%25.${DOMAIN}&output=json" 2>/dev/null | \
    jq -r '.[].common_name' 2>/dev/null | sort -u | head -20 | while read cn; do
    IP=$(dig +short $cn 2>/dev/null | head -1)
    if [ -n "$IP" ] && [[ ! $IP =~ ^104\. ]] && [[ ! $IP =~ ^172\.6 ]]; then
        echo -e "${GREEN}[+] Cert: $cn -> $IP${NC}"
    fi
done

# Resumen
echo -e "\n${BLUE}=============================================="
echo -e "[*] RESUMEN${NC}"
if [ -f "$OUTPUT_DIR/${DOMAIN}_origins.txt" ]; then
    echo -e "${GREEN}[+] Posibles IPs origen encontradas:${NC}"
    cat "$OUTPUT_DIR/${DOMAIN}_origins.txt" | sort -u
    echo -e "\n${YELLOW}[!] Verificar manualmente estas IPs${NC}"
    echo -e "${YELLOW}[!] Probar: curl -H 'Host: $DOMAIN' http://<IP>${NC}"
else
    echo -e "${RED}[-] No se encontraron IPs origen${NC}"
fi

echo -e "\n${BLUE}[*] Resultados guardados en: $OUTPUT_DIR/${DOMAIN}_origins.txt${NC}"
