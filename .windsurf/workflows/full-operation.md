---
description: Ejecutar operación de seguridad completa - La IA toma control total y ejecuta todo automáticamente
---

# 🛡️ FULL OPERATION - Operación de Seguridad Automatizada

Este workflow permite que la IA tome **control total** de una operación de seguridad, ejecutando todas las fases automáticamente y tomando decisiones en tiempo real.

## Activación

El usuario simplemente dice:
- "Full operation contra example.com"
- "Pentest completo de 192.168.1.0/24"
- "Operación de seguridad full auto"
- "Ataca y protege example.com"

## Fases de Ejecución Automática

### FASE 1: 🔴 RedTeam - Reconocimiento
// turbo
```bash
secteam new "$(echo $TARGET | tr '.' '-')-$(date +%Y%m%d)"
```

La IA ejecutará automáticamente:
1. **Reconocimiento pasivo**: whois, DNS, subdominios, certificados
2. **Reconocimiento activo**: nmap, masscan, puertos y servicios
3. **Enumeración web**: ffuf, gobuster, directorios y archivos
4. **Fingerprinting**: tecnologías, versiones, WAF detection

### FASE 2: 🔴 RedTeam - Análisis de Vulnerabilidades
La IA ejecutará:
1. **Escaneo automatizado**: nuclei, nikto, wapiti
2. **Análisis manual**: endpoints interesantes, parámetros
3. **Identificación de CVEs**: searchsploit, vulners
4. **Priorización**: ordenar por criticidad y explotabilidad

### FASE 3: 🔴 RedTeam - Explotación
La IA decidirá y ejecutará:
1. **Selección de exploits**: basado en vulnerabilidades encontradas
2. **Preparación de payloads**: adaptar al objetivo
3. **Ejecución controlada**: intentar explotación
4. **Documentación**: capturar evidencia de cada intento

### FASE 4: 🔴 RedTeam - Post-Explotación (si hay acceso)
1. **Enumeración interna**: usuarios, permisos, red
2. **Escalación de privilegios**: buscar vías
3. **Movimiento lateral**: identificar otros sistemas
4. **Persistencia**: documentar métodos (no implementar sin autorización)

### FASE 5: 🔵 BlueTeam - Análisis de Detecciones
La IA analizará:
1. **Logs generados**: qué se detectó del ataque
2. **Alertas SIEM**: correlación de eventos
3. **Gaps de detección**: qué NO se detectó
4. **IOCs**: indicadores de compromiso identificados

### FASE 6: 🟣 PurpleTeam - Validación
La IA mapeará:
1. **MITRE ATT&CK**: técnicas utilizadas
2. **Detecciones vs Ataques**: matriz de cobertura
3. **Gaps identificados**: brechas de seguridad
4. **Recomendaciones**: mejoras de detección

### FASE 7: 🟢 GreenTeam - Análisis de Código (si aplica)
1. **SAST**: análisis estático del código
2. **Secrets**: búsqueda de credenciales hardcodeadas
3. **Dependencias**: vulnerabilidades en librerías
4. **IaC**: misconfigurations en infraestructura

### FASE 8: 📊 Generación de Mega Reporte
// turbo
```bash
secteam report "$PROJECT_NAME" --full
```

## Decisiones Autónomas de la IA

La IA tomará decisiones basándose en:

| Situación | Decisión |
|-----------|----------|
| Puerto 80/443 abierto | Ejecutar escaneo web completo |
| Puerto 22 abierto | Intentar enumeración SSH, buscar credenciales |
| Puerto 3306/5432 abierto | Probar credenciales por defecto |
| Vulnerabilidad crítica encontrada | Intentar explotación inmediata |
| WAF detectado | Aplicar técnicas de bypass |
| Acceso obtenido | Proceder con post-explotación |
| Sin vulnerabilidades web | Pivotar a otros vectores |

## Ejemplo de Ejecución

```
Usuario: "Full operation contra testsite.com"

IA: 🛡️ Iniciando FULL OPERATION contra testsite.com
    
    📁 Creando proyecto: testsite-com-20240504
    
    ═══ FASE 1: RECONOCIMIENTO ═══
    🔴 [RedTeam] Ejecutando reconocimiento pasivo...
    > whois testsite.com
    > dig testsite.com ANY
    > subfinder -d testsite.com
    
    🔴 [RedTeam] Ejecutando reconocimiento activo...
    > nmap -sV -sC -p- testsite.com
    [+] Puertos encontrados: 22, 80, 443, 3306
    
    ═══ FASE 2: ANÁLISIS DE VULNERABILIDADES ═══
    🔴 [RedTeam] Escaneando vulnerabilidades...
    > nuclei -u https://testsite.com -t cves/
    [CRITICAL] CVE-2024-XXXX detectado en /api/upload
    
    ═══ FASE 3: EXPLOTACIÓN ═══
    🔴 [RedTeam] Intentando explotar CVE-2024-XXXX...
    > [payload ejecutado]
    [+] ¡Acceso obtenido! Shell como www-data
    
    ═══ FASE 4: POST-EXPLOTACIÓN ═══
    🔴 [RedTeam] Enumerando sistema...
    > id && whoami && uname -a
    > cat /etc/passwd
    [+] Usuario mysql encontrado con acceso a DB
    
    ═══ FASE 5: ANÁLISIS DEFENSIVO ═══
    🔵 [BlueTeam] Analizando detecciones...
    [!] El WAF no bloqueó el payload
    [!] No hay alertas en SIEM para este ataque
    
    ═══ FASE 6: VALIDACIÓN ═══
    🟣 [PurpleTeam] Mapeando a MITRE ATT&CK...
    - T1190: Exploit Public-Facing Application
    - T1059: Command and Scripting Interpreter
    - T1083: File and Directory Discovery
    
    ═══ FASE 7: REPORTE ═══
    📊 Generando mega reporte...
    [+] Reporte guardado en: reports/testsite-com-20240504/
    
    ✅ FULL OPERATION COMPLETADA
    
    Resumen:
    - Vulnerabilidades críticas: 1
    - Accesos obtenidos: 1 (www-data)
    - Gaps de detección: 3
    - Recomendaciones: 5
```

## Comandos que la IA Puede Ejecutar

### Reconocimiento
```bash
nmap -sV -sC -p- $TARGET
masscan -p1-65535 $TARGET --rate=1000
subfinder -d $TARGET
amass enum -d $TARGET
whatweb $TARGET
wafw00f $TARGET
```

### Escaneo de Vulnerabilidades
```bash
nuclei -u $TARGET -t cves/ -t vulnerabilities/
nikto -h $TARGET
wapiti -u $TARGET
sqlmap -u "$TARGET/page?id=1" --batch
```

### Explotación
```bash
msfconsole -q -x "use exploit/...; set RHOSTS $TARGET; run"
searchsploit $SERVICE $VERSION
```

### Análisis Defensivo
```bash
grep -r "attack_pattern" /var/log/
suricata -r capture.pcap
yara -r rules/ samples/
```

## Notas Importantes

1. **Autorización**: Este workflow asume autorización total
2. **Scope**: La IA respetará el alcance definido
3. **Documentación**: Todo se documenta automáticamente
4. **Reversibilidad**: No se realizan cambios destructivos sin confirmación
