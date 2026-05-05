#!/usr/bin/env python3
"""
⚪ WHITE TEAM GRC - Policy Generator Tool
Genera políticas de seguridad basadas en templates y frameworks
"""

import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass
import re

try:
    import click
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.prompt import Prompt, Confirm
    from jinja2 import Template
except ImportError:
    print("Installing required packages...")
    os.system("pip install click rich jinja2")
    import click
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.prompt import Prompt, Confirm
    from jinja2 import Template

console = Console()

# ══════════════════════════════════════════════════════════════════════════════
# POLICY TEMPLATES
# ══════════════════════════════════════════════════════════════════════════════

POLICY_TYPES = {
    "information_security": {
        "name": "Information Security Policy",
        "code": "SEC",
        "frameworks": ["ISO27001:A.5.1", "SOC2:CC1.1", "NIST:GV.PO"],
        "description": "Establece el marco general de seguridad de la información"
    },
    "access_control": {
        "name": "Access Control Policy",
        "code": "ACC",
        "frameworks": ["ISO27001:A.5.15", "SOC2:CC6.1", "PCI-DSS:7", "HIPAA:164.312(a)"],
        "description": "Define los controles de acceso a sistemas e información"
    },
    "data_classification": {
        "name": "Data Classification Policy",
        "code": "CLS",
        "frameworks": ["ISO27001:A.5.12", "SOC2:CC6.1", "GDPR:Art.5"],
        "description": "Establece los niveles de clasificación de información"
    },
    "acceptable_use": {
        "name": "Acceptable Use Policy",
        "code": "AUP",
        "frameworks": ["ISO27001:A.5.10", "SOC2:CC1.4"],
        "description": "Define el uso aceptable de recursos tecnológicos"
    },
    "incident_response": {
        "name": "Incident Response Policy",
        "code": "INC",
        "frameworks": ["ISO27001:A.5.24", "SOC2:CC7.4", "PCI-DSS:12.10", "HIPAA:164.308(a)(6)"],
        "description": "Establece el proceso de respuesta a incidentes"
    },
    "business_continuity": {
        "name": "Business Continuity Policy",
        "code": "BCP",
        "frameworks": ["ISO27001:A.5.29", "SOC2:A1.2"],
        "description": "Define la continuidad del negocio y recuperación"
    },
    "data_privacy": {
        "name": "Data Privacy Policy",
        "code": "PRV",
        "frameworks": ["GDPR:Art.5", "HIPAA:164.502", "ISO27001:A.5.34"],
        "description": "Establece la protección de datos personales"
    },
    "vendor_management": {
        "name": "Vendor Management Policy",
        "code": "VND",
        "frameworks": ["ISO27001:A.5.19", "SOC2:CC9.2", "PCI-DSS:12.8"],
        "description": "Define la gestión de proveedores y terceros"
    },
    "change_management": {
        "name": "Change Management Policy",
        "code": "CHG",
        "frameworks": ["ISO27001:A.8.32", "SOC2:CC8.1", "PCI-DSS:6.4"],
        "description": "Establece el proceso de gestión de cambios"
    },
    "secure_development": {
        "name": "Secure Development Policy",
        "code": "DEV",
        "frameworks": ["ISO27001:A.8.25", "SOC2:CC8.1", "PCI-DSS:6"],
        "description": "Define las prácticas de desarrollo seguro"
    },
    "remote_work": {
        "name": "Remote Work Policy",
        "code": "RMT",
        "frameworks": ["ISO27001:A.6.7", "SOC2:CC6.6"],
        "description": "Establece las políticas de trabajo remoto"
    },
    "password": {
        "name": "Password Policy",
        "code": "PWD",
        "frameworks": ["ISO27001:A.5.17", "SOC2:CC6.1", "PCI-DSS:8.3", "HIPAA:164.312(d)"],
        "description": "Define los requisitos de contraseñas"
    }
}

POLICY_TEMPLATE = """# {{ policy_name }}

**Código:** {{ policy_code }}
**Versión:** {{ version }}
**Fecha de Vigencia:** {{ effective_date }}
**Última Revisión:** {{ review_date }}
**Próxima Revisión:** {{ next_review }}
**Propietario:** {{ owner }}
**Aprobado por:** {{ approved_by }}
**Clasificación:** {{ classification }}

---

## 1. Propósito

{{ purpose }}

## 2. Alcance

{{ scope }}

## 3. Definiciones

{% for term, definition in definitions.items() %}
- **{{ term }}**: {{ definition }}
{% endfor %}

## 4. Declaraciones de Política

{% for statement in policy_statements %}
### 4.{{ loop.index }}. {{ statement.title }}

{{ statement.content }}

{% endfor %}

## 5. Roles y Responsabilidades

| Rol | Responsabilidad |
|-----|-----------------|
{% for role in roles %}
| {{ role.name }} | {{ role.responsibility }} |
{% endfor %}

## 6. Cumplimiento

### 6.1. Medición del Cumplimiento

{{ compliance_measurement }}

### 6.2. Excepciones

{{ exceptions }}

### 6.3. Incumplimiento

{{ non_compliance }}

## 7. Documentos Relacionados

{% for doc in related_documents %}
- {{ doc }}
{% endfor %}

## 8. Mapeo a Frameworks

| Framework | Referencia |
|-----------|------------|
{% for framework in frameworks %}
| {{ framework.name }} | {{ framework.reference }} |
{% endfor %}

## 9. Historial de Revisiones

| Versión | Fecha | Autor | Descripción |
|---------|-------|-------|-------------|
{% for revision in revision_history %}
| {{ revision.version }} | {{ revision.date }} | {{ revision.author }} | {{ revision.description }} |
{% endfor %}

---

**Aprobación:**

| Nombre | Cargo | Firma | Fecha |
|--------|-------|-------|-------|
| {{ approved_by }} | {{ approver_title }} | _____________ | {{ approval_date }} |

---

*Este documento es propiedad de {{ organization }}. Su distribución está restringida según su clasificación.*
"""

# ══════════════════════════════════════════════════════════════════════════════
# POLICY GENERATOR CLASS
# ══════════════════════════════════════════════════════════════════════════════

@dataclass
class PolicyStatement:
    title: str
    content: str

@dataclass
class Role:
    name: str
    responsibility: str

@dataclass
class Framework:
    name: str
    reference: str

@dataclass
class Revision:
    version: str
    date: str
    author: str
    description: str

class PolicyGenerator:
    def __init__(self, workspace_path: str = "."):
        self.workspace = Path(workspace_path)
        self.policies_path = self.workspace / "policies"
        self.templates_path = self.workspace / "templates" / "policies"
        
    def list_policy_types(self) -> None:
        """List available policy types"""
        console.print(Panel.fit(
            "[bold white]⚪ AVAILABLE POLICY TYPES[/bold white]",
            border_style="white"
        ))
        
        table = Table(show_header=True, header_style="bold cyan")
        table.add_column("Type", width=20)
        table.add_column("Name", width=30)
        table.add_column("Code", width=8)
        table.add_column("Frameworks", width=40)
        
        for type_id, info in POLICY_TYPES.items():
            table.add_row(
                type_id,
                info["name"],
                info["code"],
                ", ".join(info["frameworks"][:3]) + ("..." if len(info["frameworks"]) > 3 else "")
            )
        
        console.print(table)
    
    def generate_policy(self, policy_type: str, interactive: bool = True) -> str:
        """Generate a new policy"""
        if policy_type not in POLICY_TYPES:
            console.print(f"[red]Unknown policy type: {policy_type}[/red]")
            self.list_policy_types()
            return ""
        
        policy_info = POLICY_TYPES[policy_type]
        
        console.print(Panel.fit(
            f"[bold white]⚪ GENERATING: {policy_info['name']}[/bold white]",
            border_style="white"
        ))
        
        if interactive:
            data = self._interactive_policy_data(policy_info)
        else:
            data = self._default_policy_data(policy_info)
        
        # Render template
        template = Template(POLICY_TEMPLATE)
        content = template.render(**data)
        
        # Save policy
        return self._save_policy(policy_info["code"], data["version"], content)
    
    def _interactive_policy_data(self, policy_info: Dict) -> Dict:
        """Gather policy data interactively"""
        console.print("\n[cyan]Policy Information[/cyan]\n")
        
        organization = Prompt.ask("Organization Name", default="Organization")
        owner = Prompt.ask("Policy Owner", default="CISO")
        approved_by = Prompt.ask("Approved By", default="CEO")
        approver_title = Prompt.ask("Approver Title", default="Chief Executive Officer")
        classification = Prompt.ask("Classification", 
                                    choices=["Public", "Internal", "Confidential", "Restricted"],
                                    default="Internal")
        
        version = Prompt.ask("Version", default="1.0")
        
        console.print("\n[cyan]Policy Content[/cyan]\n")
        
        purpose = Prompt.ask("Purpose (or press Enter for default)",
                            default=f"Establecer las directrices y requisitos para {policy_info['description'].lower()}.")
        
        scope = Prompt.ask("Scope (or press Enter for default)",
                          default="Esta política aplica a todos los empleados, contratistas y terceros que tengan acceso a los sistemas e información de la organización.")
        
        # Generate default statements based on policy type
        statements = self._get_default_statements(policy_info)
        
        # Frameworks
        frameworks = [
            Framework(name=f.split(":")[0], reference=f.split(":")[1] if ":" in f else f)
            for f in policy_info["frameworks"]
        ]
        
        today = datetime.now()
        
        return {
            "policy_name": policy_info["name"],
            "policy_code": f"POL-{policy_info['code']}-001",
            "version": version,
            "effective_date": today.strftime("%Y-%m-%d"),
            "review_date": today.strftime("%Y-%m-%d"),
            "next_review": (today.replace(year=today.year + 1)).strftime("%Y-%m-%d"),
            "owner": owner,
            "approved_by": approved_by,
            "approver_title": approver_title,
            "classification": classification,
            "organization": organization,
            "purpose": purpose,
            "scope": scope,
            "definitions": self._get_default_definitions(policy_info),
            "policy_statements": statements,
            "roles": self._get_default_roles(),
            "compliance_measurement": "El cumplimiento de esta política será medido mediante auditorías periódicas, revisiones de acceso y monitoreo continuo.",
            "exceptions": "Las excepciones a esta política deben ser documentadas, aprobadas por el propietario de la política y revisadas periódicamente.",
            "non_compliance": "El incumplimiento de esta política puede resultar en acciones disciplinarias, incluyendo la terminación del empleo o contrato.",
            "related_documents": self._get_related_documents(policy_info),
            "frameworks": [{"name": f.name, "reference": f.reference} for f in frameworks],
            "revision_history": [
                {"version": version, "date": today.strftime("%Y-%m-%d"), "author": owner, "description": "Versión inicial"}
            ],
            "approval_date": today.strftime("%Y-%m-%d")
        }
    
    def _default_policy_data(self, policy_info: Dict) -> Dict:
        """Generate default policy data"""
        today = datetime.now()
        frameworks = [
            Framework(name=f.split(":")[0], reference=f.split(":")[1] if ":" in f else f)
            for f in policy_info["frameworks"]
        ]
        
        return {
            "policy_name": policy_info["name"],
            "policy_code": f"POL-{policy_info['code']}-001",
            "version": "1.0",
            "effective_date": today.strftime("%Y-%m-%d"),
            "review_date": today.strftime("%Y-%m-%d"),
            "next_review": (today.replace(year=today.year + 1)).strftime("%Y-%m-%d"),
            "owner": "CISO",
            "approved_by": "CEO",
            "approver_title": "Chief Executive Officer",
            "classification": "Internal",
            "organization": "Organization",
            "purpose": f"Establecer las directrices y requisitos para {policy_info['description'].lower()}.",
            "scope": "Esta política aplica a todos los empleados, contratistas y terceros.",
            "definitions": self._get_default_definitions(policy_info),
            "policy_statements": self._get_default_statements(policy_info),
            "roles": self._get_default_roles(),
            "compliance_measurement": "El cumplimiento será medido mediante auditorías periódicas.",
            "exceptions": "Las excepciones deben ser documentadas y aprobadas.",
            "non_compliance": "El incumplimiento puede resultar en acciones disciplinarias.",
            "related_documents": self._get_related_documents(policy_info),
            "frameworks": [{"name": f.name, "reference": f.reference} for f in frameworks],
            "revision_history": [
                {"version": "1.0", "date": today.strftime("%Y-%m-%d"), "author": "CISO", "description": "Versión inicial"}
            ],
            "approval_date": today.strftime("%Y-%m-%d")
        }
    
    def _get_default_statements(self, policy_info: Dict) -> List[Dict]:
        """Get default policy statements based on type"""
        statements_map = {
            "access_control": [
                {"title": "Principio de Mínimo Privilegio", "content": "Los usuarios deben tener únicamente los permisos mínimos necesarios para realizar sus funciones laborales."},
                {"title": "Segregación de Funciones", "content": "Las funciones críticas deben estar segregadas para prevenir fraude y errores."},
                {"title": "Revisión de Accesos", "content": "Los accesos deben ser revisados periódicamente, al menos trimestralmente."},
                {"title": "Gestión de Cuentas", "content": "Las cuentas de usuario deben ser gestionadas según el ciclo de vida del empleado."},
            ],
            "password": [
                {"title": "Complejidad de Contraseñas", "content": "Las contraseñas deben tener mínimo 12 caracteres, incluyendo mayúsculas, minúsculas, números y caracteres especiales."},
                {"title": "Rotación de Contraseñas", "content": "Las contraseñas deben cambiarse cada 90 días para cuentas estándar y cada 60 días para cuentas privilegiadas."},
                {"title": "Historial de Contraseñas", "content": "No se permite reutilizar las últimas 12 contraseñas."},
                {"title": "Autenticación Multifactor", "content": "MFA es obligatorio para acceso remoto y sistemas críticos."},
            ],
            "incident_response": [
                {"title": "Detección y Reporte", "content": "Todos los incidentes de seguridad deben ser reportados inmediatamente al equipo de seguridad."},
                {"title": "Clasificación", "content": "Los incidentes deben ser clasificados según su severidad: Crítico, Alto, Medio, Bajo."},
                {"title": "Respuesta", "content": "El equipo de respuesta debe actuar según los tiempos de SLA establecidos para cada nivel de severidad."},
                {"title": "Documentación", "content": "Todos los incidentes deben ser documentados completamente, incluyendo lecciones aprendidas."},
            ],
            "data_classification": [
                {"title": "Niveles de Clasificación", "content": "La información se clasifica en: Pública, Interna, Confidencial, Restringida."},
                {"title": "Etiquetado", "content": "Toda información debe ser etiquetada según su nivel de clasificación."},
                {"title": "Manejo", "content": "La información debe ser manejada según los controles definidos para cada nivel."},
                {"title": "Retención y Destrucción", "content": "La información debe ser retenida y destruida según los períodos establecidos."},
            ],
        }
        
        # Get specific statements or default
        code = policy_info["code"].lower()
        for key, statements in statements_map.items():
            if key in code or code in key:
                return statements
        
        # Default statements
        return [
            {"title": "Requisitos Generales", "content": "Se deben cumplir todos los requisitos establecidos en esta política."},
            {"title": "Controles", "content": "Se deben implementar los controles necesarios para asegurar el cumplimiento."},
            {"title": "Monitoreo", "content": "El cumplimiento debe ser monitoreado de forma continua."},
            {"title": "Mejora Continua", "content": "La política debe ser revisada y mejorada periódicamente."},
        ]
    
    def _get_default_definitions(self, policy_info: Dict) -> Dict:
        """Get default definitions"""
        return {
            "Activo de Información": "Cualquier dato, sistema o recurso que tenga valor para la organización.",
            "Control": "Medida que modifica el riesgo, incluyendo políticas, procedimientos y mecanismos técnicos.",
            "Incidente de Seguridad": "Evento que compromete la confidencialidad, integridad o disponibilidad de la información.",
            "Usuario": "Cualquier persona que accede a los sistemas o información de la organización.",
            "Propietario de Datos": "Persona responsable de la clasificación y protección de un conjunto de datos.",
        }
    
    def _get_default_roles(self) -> List[Dict]:
        """Get default roles"""
        return [
            {"name": "CISO", "responsibility": "Propietario de la política, responsable de su mantenimiento y cumplimiento."},
            {"name": "Gerentes de Área", "responsibility": "Asegurar el cumplimiento de la política en sus equipos."},
            {"name": "Empleados", "responsibility": "Cumplir con los requisitos establecidos en la política."},
            {"name": "TI", "responsibility": "Implementar los controles técnicos necesarios."},
            {"name": "Auditoría", "responsibility": "Verificar el cumplimiento de la política."},
        ]
    
    def _get_related_documents(self, policy_info: Dict) -> List[str]:
        """Get related documents"""
        return [
            "POL-SEC-001 - Política de Seguridad de la Información",
            "PRO-INC-001 - Procedimiento de Respuesta a Incidentes",
            "STD-PWD-001 - Estándar de Contraseñas",
            "Manual de Seguridad de la Información",
        ]
    
    def _save_policy(self, code: str, version: str, content: str) -> str:
        """Save policy to file"""
        # Determine subdirectory
        subdir_map = {
            "SEC": "security",
            "ACC": "access",
            "CLS": "security",
            "AUP": "security",
            "INC": "security",
            "BCP": "security",
            "PRV": "privacy",
            "VND": "security",
            "CHG": "security",
            "DEV": "security",
            "RMT": "security",
            "PWD": "access",
        }
        
        subdir = subdir_map.get(code, "security")
        policy_dir = self.policies_path / subdir
        policy_dir.mkdir(parents=True, exist_ok=True)
        
        filename = f"POL-{code}-001-v{version}.md"
        filepath = policy_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        console.print(f"\n[green]✓ Policy saved to: {filepath}[/green]")
        return str(filepath)

# ══════════════════════════════════════════════════════════════════════════════
# CLI INTERFACE
# ══════════════════════════════════════════════════════════════════════════════

@click.command()
@click.option('--type', '-t', 'policy_type', type=str, help='Policy type to generate')
@click.option('--list', '-l', 'list_types', is_flag=True, help='List available policy types')
@click.option('--workspace', '-w', type=click.Path(exists=True), default='.', help='Workspace path')
@click.option('--interactive/--no-interactive', '-i', default=True, help='Interactive mode')
@click.version_option(version='1.0.0', prog_name='WHITE TEAM GRC - Policy Generator')
def main(policy_type: str, list_types: bool, workspace: str, interactive: bool):
    """
    ⚪ WHITE TEAM GRC - Policy Generator Tool
    
    Genera políticas de seguridad basadas en templates y frameworks.
    """
    generator = PolicyGenerator(workspace)
    
    if list_types:
        generator.list_policy_types()
    elif policy_type:
        generator.generate_policy(policy_type, interactive=interactive)
    else:
        console.print(Panel.fit(
            "[bold white]⚪ WHITE TEAM GRC - Policy Generator[/bold white]",
            border_style="white"
        ))
        generator.list_policy_types()
        console.print("\n[cyan]Usage:[/cyan]")
        console.print("  --type TYPE      Generate specific policy type")
        console.print("  --list           List available policy types")
        console.print("  --help           Show all options")
        console.print("\n[dim]Example: python policy_generator.py --type access_control[/dim]")

if __name__ == '__main__':
    main()
