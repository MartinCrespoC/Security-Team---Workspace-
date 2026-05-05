#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║   🟢 GREEN TEAM - Dependency Security Checker                               ║
║   Verificación de vulnerabilidades en dependencias                          ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import os
import sys
import json
import subprocess
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum

class Severity(Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"

@dataclass
class Vulnerability:
    package: str
    version: str
    severity: Severity
    cve: Optional[str]
    description: str
    fix_version: Optional[str] = None
    
@dataclass
class ScanResult:
    tool: str
    ecosystem: str
    vulnerabilities: List[Vulnerability] = field(default_factory=list)
    error: Optional[str] = None

class Colors:
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    CYAN = '\033[0;36m'
    PURPLE = '\033[0;35m'
    NC = '\033[0m'
    BOLD = '\033[1m'

def print_banner():
    print(f"{Colors.GREEN}")
    print("╔═══════════════════════════════════════════════════════════════╗")
    print("║       📦 GREEN TEAM - Dependency Security Checker            ║")
    print("╚═══════════════════════════════════════════════════════════════╝")
    print(f"{Colors.NC}")

def log_info(msg: str):
    print(f"{Colors.BLUE}[INFO]{Colors.NC} {msg}")

def log_success(msg: str):
    print(f"{Colors.GREEN}[✓]{Colors.NC} {msg}")

def log_warning(msg: str):
    print(f"{Colors.YELLOW}[!]{Colors.NC} {msg}")

def log_error(msg: str):
    print(f"{Colors.RED}[✗]{Colors.NC} {msg}")

def check_tool(tool: str) -> bool:
    """Verificar si una herramienta está instalada."""
    try:
        subprocess.run([tool, "--version"], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def detect_ecosystems(target_dir: Path) -> Dict[str, List[Path]]:
    """Detectar ecosistemas de dependencias en el proyecto."""
    ecosystems = {
        "python": [],
        "nodejs": [],
        "ruby": [],
        "go": [],
        "java": [],
        "rust": [],
        "php": []
    }
    
    # Python
    for pattern in ["requirements*.txt", "Pipfile", "pyproject.toml", "setup.py"]:
        ecosystems["python"].extend(target_dir.glob(f"**/{pattern}"))
    
    # Node.js
    for pattern in ["package.json", "package-lock.json", "yarn.lock"]:
        ecosystems["nodejs"].extend(target_dir.glob(f"**/{pattern}"))
    
    # Ruby
    for pattern in ["Gemfile", "Gemfile.lock"]:
        ecosystems["ruby"].extend(target_dir.glob(f"**/{pattern}"))
    
    # Go
    for pattern in ["go.mod", "go.sum"]:
        ecosystems["go"].extend(target_dir.glob(f"**/{pattern}"))
    
    # Java
    for pattern in ["pom.xml", "build.gradle", "build.gradle.kts"]:
        ecosystems["java"].extend(target_dir.glob(f"**/{pattern}"))
    
    # Rust
    ecosystems["rust"].extend(target_dir.glob("**/Cargo.toml"))
    
    # PHP
    ecosystems["php"].extend(target_dir.glob("**/composer.json"))
    
    return {k: v for k, v in ecosystems.items() if v}

def run_safety(target_dir: Path) -> ScanResult:
    """Ejecutar Safety para Python."""
    result = ScanResult(tool="safety", ecosystem="python")
    
    if not check_tool("safety"):
        result.error = "Safety no instalado"
        return result
    
    try:
        # Buscar requirements.txt
        req_files = list(target_dir.glob("**/requirements*.txt"))
        
        for req_file in req_files:
            cmd = ["safety", "check", "-r", str(req_file), "--json"]
            proc = subprocess.run(cmd, capture_output=True, text=True)
            
            if proc.stdout:
                try:
                    data = json.loads(proc.stdout)
                    for vuln in data.get("vulnerabilities", []):
                        result.vulnerabilities.append(Vulnerability(
                            package=vuln.get("package_name", "unknown"),
                            version=vuln.get("analyzed_version", "unknown"),
                            severity=Severity.HIGH,
                            cve=vuln.get("CVE"),
                            description=vuln.get("advisory", ""),
                            fix_version=vuln.get("fixed_versions", [None])[0] if vuln.get("fixed_versions") else None
                        ))
                except json.JSONDecodeError:
                    pass
                    
    except Exception as e:
        result.error = str(e)
    
    return result

def run_pip_audit(target_dir: Path) -> ScanResult:
    """Ejecutar pip-audit para Python."""
    result = ScanResult(tool="pip-audit", ecosystem="python")
    
    if not check_tool("pip-audit"):
        result.error = "pip-audit no instalado"
        return result
    
    try:
        req_files = list(target_dir.glob("**/requirements*.txt"))
        
        for req_file in req_files:
            cmd = ["pip-audit", "-r", str(req_file), "--format", "json"]
            proc = subprocess.run(cmd, capture_output=True, text=True)
            
            if proc.stdout:
                try:
                    data = json.loads(proc.stdout)
                    for vuln in data:
                        for v in vuln.get("vulns", []):
                            severity = Severity.HIGH
                            if "critical" in v.get("id", "").lower():
                                severity = Severity.CRITICAL
                            
                            result.vulnerabilities.append(Vulnerability(
                                package=vuln.get("name", "unknown"),
                                version=vuln.get("version", "unknown"),
                                severity=severity,
                                cve=v.get("id"),
                                description=v.get("description", ""),
                                fix_version=v.get("fix_versions", [None])[0] if v.get("fix_versions") else None
                            ))
                except json.JSONDecodeError:
                    pass
                    
    except Exception as e:
        result.error = str(e)
    
    return result

def run_npm_audit(target_dir: Path) -> ScanResult:
    """Ejecutar npm audit para Node.js."""
    result = ScanResult(tool="npm-audit", ecosystem="nodejs")
    
    if not check_tool("npm"):
        result.error = "npm no instalado"
        return result
    
    try:
        package_dirs = [f.parent for f in target_dir.glob("**/package.json")]
        
        for pkg_dir in package_dirs:
            cmd = ["npm", "audit", "--json"]
            proc = subprocess.run(cmd, capture_output=True, text=True, cwd=str(pkg_dir))
            
            if proc.stdout:
                try:
                    data = json.loads(proc.stdout)
                    vulns = data.get("vulnerabilities", {})
                    
                    for name, info in vulns.items():
                        severity_map = {
                            "critical": Severity.CRITICAL,
                            "high": Severity.HIGH,
                            "moderate": Severity.MEDIUM,
                            "low": Severity.LOW
                        }
                        
                        result.vulnerabilities.append(Vulnerability(
                            package=name,
                            version=info.get("range", "unknown"),
                            severity=severity_map.get(info.get("severity", "low"), Severity.LOW),
                            cve=info.get("via", [{}])[0].get("cve") if isinstance(info.get("via", [{}])[0], dict) else None,
                            description=info.get("via", [{}])[0].get("title", "") if isinstance(info.get("via", [{}])[0], dict) else str(info.get("via", "")),
                            fix_version=info.get("fixAvailable", {}).get("version") if isinstance(info.get("fixAvailable"), dict) else None
                        ))
                except json.JSONDecodeError:
                    pass
                    
    except Exception as e:
        result.error = str(e)
    
    return result

def run_snyk(target_dir: Path) -> ScanResult:
    """Ejecutar Snyk para múltiples ecosistemas."""
    result = ScanResult(tool="snyk", ecosystem="multi")
    
    if not check_tool("snyk"):
        result.error = "Snyk no instalado"
        return result
    
    try:
        cmd = ["snyk", "test", "--json", str(target_dir)]
        proc = subprocess.run(cmd, capture_output=True, text=True)
        
        if proc.stdout:
            try:
                data = json.loads(proc.stdout)
                
                for vuln in data.get("vulnerabilities", []):
                    severity_map = {
                        "critical": Severity.CRITICAL,
                        "high": Severity.HIGH,
                        "medium": Severity.MEDIUM,
                        "low": Severity.LOW
                    }
                    
                    result.vulnerabilities.append(Vulnerability(
                        package=vuln.get("packageName", "unknown"),
                        version=vuln.get("version", "unknown"),
                        severity=severity_map.get(vuln.get("severity", "low"), Severity.LOW),
                        cve=vuln.get("identifiers", {}).get("CVE", [None])[0],
                        description=vuln.get("title", ""),
                        fix_version=vuln.get("fixedIn", [None])[0] if vuln.get("fixedIn") else None
                    ))
            except json.JSONDecodeError:
                pass
                
    except Exception as e:
        result.error = str(e)
    
    return result

def generate_report(results: List[ScanResult], output_dir: Path) -> Path:
    """Generar reporte de vulnerabilidades."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_dir = output_dir / "sca" / timestamp
    report_dir.mkdir(parents=True, exist_ok=True)
    
    # Reporte JSON
    json_report = {
        "timestamp": datetime.now().isoformat(),
        "results": []
    }
    
    for result in results:
        json_report["results"].append({
            "tool": result.tool,
            "ecosystem": result.ecosystem,
            "error": result.error,
            "vulnerabilities": [
                {
                    "package": v.package,
                    "version": v.version,
                    "severity": v.severity.value,
                    "cve": v.cve,
                    "description": v.description,
                    "fix_version": v.fix_version
                }
                for v in result.vulnerabilities
            ]
        })
    
    json_path = report_dir / "dependency_check.json"
    with open(json_path, "w") as f:
        json.dump(json_report, f, indent=2)
    
    # Reporte Markdown
    md_path = report_dir / "dependency_check.md"
    with open(md_path, "w") as f:
        f.write("# 📦 Dependency Security Report\n\n")
        f.write(f"**Fecha:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        # Resumen
        total_vulns = sum(len(r.vulnerabilities) for r in results)
        critical = sum(1 for r in results for v in r.vulnerabilities if v.severity == Severity.CRITICAL)
        high = sum(1 for r in results for v in r.vulnerabilities if v.severity == Severity.HIGH)
        medium = sum(1 for r in results for v in r.vulnerabilities if v.severity == Severity.MEDIUM)
        low = sum(1 for r in results for v in r.vulnerabilities if v.severity == Severity.LOW)
        
        f.write("## 📊 Resumen\n\n")
        f.write("| Severidad | Cantidad |\n")
        f.write("|-----------|----------|\n")
        f.write(f"| 🔴 Crítica | {critical} |\n")
        f.write(f"| 🟠 Alta | {high} |\n")
        f.write(f"| 🟡 Media | {medium} |\n")
        f.write(f"| 🔵 Baja | {low} |\n")
        f.write(f"| **Total** | **{total_vulns}** |\n\n")
        
        # Detalles por herramienta
        for result in results:
            f.write(f"## {result.tool.upper()} ({result.ecosystem})\n\n")
            
            if result.error:
                f.write(f"⚠️ Error: {result.error}\n\n")
                continue
            
            if not result.vulnerabilities:
                f.write("✅ No se encontraron vulnerabilidades\n\n")
                continue
            
            f.write("| Package | Version | Severity | CVE | Fix Version |\n")
            f.write("|---------|---------|----------|-----|-------------|\n")
            
            for v in sorted(result.vulnerabilities, key=lambda x: ["critical", "high", "medium", "low"].index(x.severity.value)):
                severity_icon = {"critical": "🔴", "high": "🟠", "medium": "🟡", "low": "🔵"}.get(v.severity.value, "⚪")
                f.write(f"| {v.package} | {v.version} | {severity_icon} {v.severity.value} | {v.cve or 'N/A'} | {v.fix_version or 'N/A'} |\n")
            
            f.write("\n")
    
    return report_dir

def print_summary(results: List[ScanResult]):
    """Imprimir resumen en consola."""
    print(f"\n{Colors.CYAN}{'═' * 65}{Colors.NC}")
    print(f"{Colors.BOLD}📊 RESUMEN DE VULNERABILIDADES{Colors.NC}")
    print(f"{Colors.CYAN}{'═' * 65}{Colors.NC}\n")
    
    total_vulns = sum(len(r.vulnerabilities) for r in results)
    critical = sum(1 for r in results for v in r.vulnerabilities if v.severity == Severity.CRITICAL)
    high = sum(1 for r in results for v in r.vulnerabilities if v.severity == Severity.HIGH)
    medium = sum(1 for r in results for v in r.vulnerabilities if v.severity == Severity.MEDIUM)
    low = sum(1 for r in results for v in r.vulnerabilities if v.severity == Severity.LOW)
    
    print(f"  {Colors.RED}🔴 Críticas:{Colors.NC}  {critical}")
    print(f"  {Colors.YELLOW}🟠 Altas:{Colors.NC}      {high}")
    print(f"  {Colors.BLUE}🟡 Medias:{Colors.NC}     {medium}")
    print(f"  {Colors.CYAN}🔵 Bajas:{Colors.NC}      {low}")
    print(f"  {Colors.BOLD}📦 Total:{Colors.NC}      {total_vulns}")
    
    # Estado del gate de seguridad
    print(f"\n{Colors.CYAN}{'─' * 65}{Colors.NC}")
    if critical > 0:
        print(f"{Colors.RED}❌ SECURITY GATE: FAILED (Critical vulnerabilities found){Colors.NC}")
    elif high > 5:
        print(f"{Colors.YELLOW}⚠️ SECURITY GATE: WARNING (Too many high vulnerabilities){Colors.NC}")
    else:
        print(f"{Colors.GREEN}✅ SECURITY GATE: PASSED{Colors.NC}")
    print(f"{Colors.CYAN}{'─' * 65}{Colors.NC}\n")

def main():
    parser = argparse.ArgumentParser(description="GREEN TEAM Dependency Security Checker")
    parser.add_argument("target", nargs="?", default=".", help="Directorio a escanear")
    parser.add_argument("-o", "--output", default=None, help="Directorio de salida para reportes")
    parser.add_argument("--json", action="store_true", help="Salida en formato JSON")
    args = parser.parse_args()
    
    print_banner()
    
    target_dir = Path(args.target).resolve()
    output_dir = Path(args.output) if args.output else target_dir / "scans"
    
    log_info(f"Target: {target_dir}")
    
    # Detectar ecosistemas
    ecosystems = detect_ecosystems(target_dir)
    log_info(f"Ecosistemas detectados: {', '.join(ecosystems.keys())}")
    
    results: List[ScanResult] = []
    
    # Ejecutar scanners según ecosistemas detectados
    print(f"\n{Colors.CYAN}{'═' * 65}{Colors.NC}")
    print(f"{Colors.BOLD}Ejecutando análisis de dependencias...{Colors.NC}")
    print(f"{Colors.CYAN}{'═' * 65}{Colors.NC}\n")
    
    if "python" in ecosystems:
        log_info("Escaneando dependencias Python...")
        results.append(run_safety(target_dir))
        results.append(run_pip_audit(target_dir))
    
    if "nodejs" in ecosystems:
        log_info("Escaneando dependencias Node.js...")
        results.append(run_npm_audit(target_dir))
    
    # Snyk para todos los ecosistemas
    log_info("Ejecutando Snyk (multi-ecosistema)...")
    results.append(run_snyk(target_dir))
    
    # Generar reporte
    report_dir = generate_report(results, output_dir)
    
    # Mostrar resumen
    print_summary(results)
    
    log_success(f"Reportes generados en: {report_dir}")
    
    # Código de salida basado en vulnerabilidades críticas
    critical_count = sum(1 for r in results for v in r.vulnerabilities if v.severity == Severity.CRITICAL)
    sys.exit(1 if critical_count > 0 else 0)

if __name__ == "__main__":
    main()
