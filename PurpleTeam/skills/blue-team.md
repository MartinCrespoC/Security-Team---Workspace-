# 🔵 BLUE TEAM SKILLS

## Descripción
Skills para operaciones defensivas, detección y respuesta a incidentes.

---

## Monitoreo y Logging

### Sysmon Configuration
```xml
<!-- Sysmon config para detección avanzada -->
<Sysmon schemaversion="4.90">
  <EventFiltering>
    <!-- Process Creation -->
    <ProcessCreate onmatch="include">
      <Image condition="contains">powershell</Image>
      <Image condition="contains">cmd.exe</Image>
      <CommandLine condition="contains">-enc</CommandLine>
    </ProcessCreate>
    
    <!-- Process Access (LSASS) -->
    <ProcessAccess onmatch="include">
      <TargetImage condition="is">C:\Windows\System32\lsass.exe</TargetImage>
    </ProcessAccess>
    
    <!-- Registry Events -->
    <RegistryEvent onmatch="include">
      <TargetObject condition="contains">CurrentVersion\Run</TargetObject>
    </RegistryEvent>
  </EventFiltering>
</Sysmon>
```

### Windows Event Logging
```powershell
# Habilitar PowerShell Script Block Logging
Set-ItemProperty -Path "HKLM:\SOFTWARE\Policies\Microsoft\Windows\PowerShell\ScriptBlockLogging" -Name "EnableScriptBlockLogging" -Value 1

# Habilitar Module Logging
Set-ItemProperty -Path "HKLM:\SOFTWARE\Policies\Microsoft\Windows\PowerShell\ModuleLogging" -Name "EnableModuleLogging" -Value 1

# Verificar configuración de auditoría
auditpol /get /category:*
```

### Linux Auditd
```bash
# Configuración de auditd
cat >> /etc/audit/rules.d/audit.rules << EOF
# Monitorear ejecución de comandos
-a always,exit -F arch=b64 -S execve -k exec_commands

# Monitorear acceso a archivos sensibles
-w /etc/passwd -p wa -k passwd_changes
-w /etc/shadow -p wa -k shadow_changes
-w /etc/sudoers -p wa -k sudoers_changes

# Monitorear conexiones de red
-a always,exit -F arch=b64 -S connect -k network_connect
EOF

# Recargar reglas
auditctl -R /etc/audit/rules.d/audit.rules
```

---

## Reglas de Detección

### Sigma Rules

#### LSASS Access Detection
```yaml
title: LSASS Memory Access
id: 0d894093-71bc-43c3-8c4d-ecfc28dcf5d9
status: experimental
description: Detects suspicious access to LSASS process
logsource:
    category: process_access
    product: windows
detection:
    selection:
        TargetImage|endswith: '\lsass.exe'
        GrantedAccess|contains:
            - '0x1010'
            - '0x1038'
            - '0x1438'
    filter:
        SourceImage|endswith:
            - '\wmiprvse.exe'
            - '\taskmgr.exe'
            - '\MsMpEng.exe'
    condition: selection and not filter
falsepositives:
    - Legitimate administrative tools
level: high
tags:
    - attack.credential_access
    - attack.t1003.001
```

#### PowerShell Suspicious Execution
```yaml
title: Suspicious PowerShell Execution
id: f4bbd493-b796-416e-bbf2-121235348529
status: experimental
description: Detects suspicious PowerShell command patterns
logsource:
    product: windows
    category: ps_script
detection:
    selection:
        ScriptBlockText|contains:
            - 'IEX'
            - 'Invoke-Expression'
            - 'DownloadString'
            - 'Net.WebClient'
            - '-enc'
            - 'FromBase64String'
    condition: selection
falsepositives:
    - Legitimate administrative scripts
level: medium
tags:
    - attack.execution
    - attack.t1059.001
```

#### Registry Run Key Modification
```yaml
title: Registry Run Key Modification
id: 17f878b8-9968-4f3f-9c7f-4e7b8d4c4f8a
status: experimental
description: Detects modification of registry run keys
logsource:
    category: registry_set
    product: windows
detection:
    selection:
        TargetObject|contains:
            - '\SOFTWARE\Microsoft\Windows\CurrentVersion\Run'
            - '\SOFTWARE\Microsoft\Windows\CurrentVersion\RunOnce'
    condition: selection
falsepositives:
    - Legitimate software installation
level: medium
tags:
    - attack.persistence
    - attack.t1547.001
```

### YARA Rules

#### Mimikatz Detection
```yara
rule Mimikatz_Strings
{
    meta:
        description = "Detects Mimikatz strings"
        author = "Purple Team"
        reference = "T1003"
        
    strings:
        $s1 = "sekurlsa::logonpasswords" ascii wide
        $s2 = "lsadump::sam" ascii wide
        $s3 = "kerberos::list" ascii wide
        $s4 = "privilege::debug" ascii wide
        $s5 = "mimikatz" ascii wide nocase
        
    condition:
        2 of them
}
```

#### PowerShell Empire Detection
```yara
rule PowerShell_Empire
{
    meta:
        description = "Detects PowerShell Empire artifacts"
        author = "Purple Team"
        
    strings:
        $s1 = "Invoke-Empire" ascii wide
        $s2 = "Get-Keystrokes" ascii wide
        $s3 = "Invoke-Mimikatz" ascii wide
        $s4 = "Invoke-Shellcode" ascii wide
        
    condition:
        any of them
}
```

---

## Análisis de Logs

### Splunk Queries

```spl
# Detectar acceso a LSASS
index=windows EventCode=10 TargetImage="*lsass.exe"
| stats count by SourceImage, SourceProcessId, GrantedAccess

# Detectar PowerShell sospechoso
index=windows EventCode=4104
| search ScriptBlockText="*IEX*" OR ScriptBlockText="*DownloadString*"
| table _time, ComputerName, ScriptBlockText

# Detectar modificación de registry run keys
index=windows EventCode=13 TargetObject="*CurrentVersion\\Run*"
| table _time, ComputerName, Image, TargetObject, Details

# Detectar movimiento lateral
index=windows EventCode=4624 LogonType=3
| stats count by TargetUserName, IpAddress, WorkstationName
| where count > 5
```

### Elastic Queries

```json
// Detectar acceso a LSASS
{
  "query": {
    "bool": {
      "must": [
        { "match": { "event.code": "10" }},
        { "wildcard": { "winlog.event_data.TargetImage": "*lsass.exe" }}
      ]
    }
  }
}

// Detectar PowerShell sospechoso
{
  "query": {
    "bool": {
      "must": [
        { "match": { "event.code": "4104" }},
        {
          "bool": {
            "should": [
              { "match_phrase": { "powershell.scriptblock.text": "IEX" }},
              { "match_phrase": { "powershell.scriptblock.text": "DownloadString" }}
            ]
          }
        }
      ]
    }
  }
}
```

---

## Respuesta a Incidentes

### Contención

```bash
# Aislar host de la red
netsh advfirewall set allprofiles state on
netsh advfirewall firewall add rule name="Block All" dir=in action=block
netsh advfirewall firewall add rule name="Block All Out" dir=out action=block

# Deshabilitar cuenta comprometida
net user <username> /active:no

# Terminar proceso malicioso
taskkill /F /PID <pid>
wmic process where processid=<pid> delete
```

### Recolección de Evidencia

```bash
# Memoria
winpmem_mini_x64.exe memory.raw

# Procesos
tasklist /v > processes.txt
wmic process list full > processes_wmic.txt

# Conexiones de red
netstat -anob > netstat.txt

# Usuarios logueados
query user > users.txt
net session > sessions.txt

# Tareas programadas
schtasks /query /fo csv > tasks.csv

# Servicios
sc query > services.txt

# Registry run keys
reg query "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run" > run_keys.txt
reg query "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Run" >> run_keys.txt
```

### Análisis Forense

```bash
# Volatility - Análisis de memoria
volatility3 -f memory.raw windows.pslist
volatility3 -f memory.raw windows.pstree
volatility3 -f memory.raw windows.netscan
volatility3 -f memory.raw windows.malfind
volatility3 -f memory.raw windows.cmdline

# Timeline
volatility3 -f memory.raw windows.timeliner

# Strings
strings -a memory.raw | grep -i "password\|credential\|secret"
```

---

## Threat Hunting

### Hipótesis de Hunting

```markdown
## Hipótesis 1: Credential Dumping
**Descripción**: Adversarios pueden estar extrayendo credenciales de LSASS
**Indicadores**:
- Acceso a lsass.exe desde procesos no autorizados
- Creación de archivos .dmp en ubicaciones inusuales
- Uso de herramientas como procdump, mimikatz

**Query**:
```spl
index=windows (EventCode=10 TargetImage="*lsass.exe") OR 
(EventCode=11 TargetFilename="*.dmp")
| stats count by SourceImage, TargetImage, TargetFilename
```

## Hipótesis 2: Lateral Movement via SMB
**Descripción**: Adversarios pueden estar moviéndose lateralmente usando SMB
**Indicadores**:
- Múltiples conexiones SMB desde un solo host
- Acceso a admin shares (C$, ADMIN$)
- Autenticación tipo 3 desde hosts inusuales

**Query**:
```spl
index=windows EventCode=5140 ShareName IN ("\\*\C$", "\\*\ADMIN$")
| stats count by SubjectUserName, IpAddress, ShareName
| where count > 3
```
```

### Hunting Playbooks

```yaml
name: Hunt for Credential Access
description: Buscar indicadores de robo de credenciales
techniques:
  - T1003.001
  - T1003.002
  - T1003.003

steps:
  - name: Check LSASS access
    query: |
      index=windows EventCode=10 TargetImage="*lsass.exe"
      | stats count by SourceImage
      | where count > 1
    
  - name: Check for credential dumping tools
    query: |
      index=windows EventCode=1
      | search Image="*mimikatz*" OR Image="*procdump*" OR 
        CommandLine="*sekurlsa*" OR CommandLine="*lsadump*"
    
  - name: Check for SAM access
    query: |
      index=windows EventCode=4656 ObjectName="*\\SAM"
      | stats count by SubjectUserName, ProcessName
```

---

## Herramientas Defensivas

| Herramienta | Propósito | Uso |
|-------------|-----------|-----|
| Sysmon | System monitoring | Logging avanzado |
| Velociraptor | Endpoint visibility | Hunting, IR |
| Wazuh | SIEM/XDR | Detección, alertas |
| YARA | Malware detection | Scanning |
| Sigma | Detection rules | Reglas genéricas |
| Zeek | Network monitoring | Análisis de tráfico |
| Suricata | IDS/IPS | Detección de red |
| Volatility | Memory forensics | Análisis de memoria |

---

## Comandos Rápidos

```bash
# Verificar conexiones sospechosas
netstat -anob | findstr ESTABLISHED
ss -tuln

# Buscar archivos modificados recientemente
find / -mtime -1 -type f 2>/dev/null
forfiles /P C:\ /S /D +0 /C "cmd /c echo @path"

# Verificar procesos sospechosos
ps aux | grep -E "nc|ncat|python|perl|ruby"
wmic process where "name like '%powershell%'" get commandline

# Verificar tareas programadas
crontab -l
schtasks /query /fo list /v

# Verificar usuarios
cat /etc/passwd | grep -v nologin
net user

# Verificar servicios
systemctl list-units --type=service --state=running
sc query state= all
```
