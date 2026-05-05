#!/usr/bin/env python3
"""
BlueTeam-Windsurf - Incident Response System
Automated incident response and management
"""

import os
import sys
import json
import hashlib
import argparse
import subprocess
import socket
import datetime
import shutil
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field, asdict
from enum import Enum
import re

# Colors for terminal output
class Colors:
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    CYAN = '\033[0;36m'
    PURPLE = '\033[0;35m'
    NC = '\033[0m'

def log(msg: str) -> None:
    print(f"{Colors.GREEN}[+]{Colors.NC} {msg}")

def warn(msg: str) -> None:
    print(f"{Colors.YELLOW}[!]{Colors.NC} {msg}")

def error(msg: str) -> None:
    print(f"{Colors.RED}[✗]{Colors.NC} {msg}")

def alert(msg: str) -> None:
    print(f"{Colors.RED}[🚨]{Colors.NC} {msg}")

def info(msg: str) -> None:
    print(f"{Colors.BLUE}[i]{Colors.NC} {msg}")

# Paths
SCRIPT_DIR = Path(__file__).parent.resolve()
BASE_DIR = SCRIPT_DIR.parent.parent
INCIDENTS_DIR = BASE_DIR / "incidents"
ALERTS_DIR = BASE_DIR / "alerts"
FORENSICS_DIR = BASE_DIR / "forensics"
REPORTS_DIR = BASE_DIR / "reports"
IOCS_DIR = BASE_DIR / "iocs"

class Severity(Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"

class IncidentStatus(Enum):
    NEW = "new"
    INVESTIGATING = "investigating"
    CONTAINING = "containing"
    ERADICATING = "eradicating"
    RECOVERING = "recovering"
    CLOSED = "closed"

class IncidentType(Enum):
    MALWARE = "malware"
    RANSOMWARE = "ransomware"
    PHISHING = "phishing"
    DATA_BREACH = "data_breach"
    DDOS = "ddos"
    INTRUSION = "intrusion"
    INSIDER_THREAT = "insider_threat"
    APT = "apt"
    CRYPTOMINING = "cryptomining"
    UNKNOWN = "unknown"

@dataclass
class IOC:
    type: str  # ip, domain, hash, url, file
    value: str
    description: str = ""
    source: str = ""
    timestamp: str = field(default_factory=lambda: datetime.datetime.now().isoformat())

@dataclass
class TimelineEvent:
    timestamp: str
    event: str
    source: str
    details: str = ""

@dataclass
class Incident:
    id: str
    title: str
    description: str
    severity: str
    status: str
    type: str
    affected_hosts: List[str] = field(default_factory=list)
    affected_users: List[str] = field(default_factory=list)
    iocs: List[Dict] = field(default_factory=list)
    timeline: List[Dict] = field(default_factory=list)
    actions_taken: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.datetime.now().isoformat())
    closed_at: Optional[str] = None
    analyst: str = field(default_factory=lambda: os.getenv("USER", "unknown"))
    mitre_techniques: List[str] = field(default_factory=list)

class IncidentResponseSystem:
    def __init__(self):
        self.ensure_directories()
        
    def ensure_directories(self):
        """Create necessary directories"""
        for d in [INCIDENTS_DIR / "active", INCIDENTS_DIR / "resolved", 
                  INCIDENTS_DIR / "templates", REPORTS_DIR / "incident"]:
            d.mkdir(parents=True, exist_ok=True)
    
    def generate_incident_id(self) -> str:
        """Generate unique incident ID"""
        year = datetime.datetime.now().year
        existing = list((INCIDENTS_DIR / "active").glob(f"INC-{year}-*"))
        existing += list((INCIDENTS_DIR / "resolved").glob(f"INC-{year}-*"))
        num = len(existing) + 1
        return f"INC-{year}-{num:04d}"
    
    def create_incident(self, title: str, description: str, 
                       severity: str = "high", incident_type: str = "unknown") -> Incident:
        """Create a new incident"""
        incident_id = self.generate_incident_id()
        
        incident = Incident(
            id=incident_id,
            title=title,
            description=description,
            severity=severity,
            status=IncidentStatus.NEW.value,
            type=incident_type
        )
        
        # Add initial timeline event
        incident.timeline.append(asdict(TimelineEvent(
            timestamp=datetime.datetime.now().isoformat(),
            event="Incident created",
            source="incident_response.py",
            details=f"Severity: {severity}, Type: {incident_type}"
        )))
        
        # Save incident
        incident_dir = INCIDENTS_DIR / "active" / incident_id
        incident_dir.mkdir(parents=True, exist_ok=True)
        
        with open(incident_dir / "incident.json", "w") as f:
            json.dump(asdict(incident), f, indent=2)
        
        log(f"Created incident: {incident_id}")
        log(f"Incident directory: {incident_dir}")
        
        return incident
    
    def load_incident(self, incident_id: str) -> Optional[Incident]:
        """Load an existing incident"""
        for status_dir in ["active", "resolved"]:
            incident_file = INCIDENTS_DIR / status_dir / incident_id / "incident.json"
            if incident_file.exists():
                with open(incident_file) as f:
                    data = json.load(f)
                return Incident(**data)
        return None
    
    def save_incident(self, incident: Incident):
        """Save incident to disk"""
        status_dir = "resolved" if incident.status == IncidentStatus.CLOSED.value else "active"
        incident_dir = INCIDENTS_DIR / status_dir / incident.id
        incident_dir.mkdir(parents=True, exist_ok=True)
        
        incident.updated_at = datetime.datetime.now().isoformat()
        
        with open(incident_dir / "incident.json", "w") as f:
            json.dump(asdict(incident), f, indent=2)
    
    def add_timeline_event(self, incident: Incident, event: str, 
                          source: str, details: str = ""):
        """Add event to incident timeline"""
        incident.timeline.append(asdict(TimelineEvent(
            timestamp=datetime.datetime.now().isoformat(),
            event=event,
            source=source,
            details=details
        )))
        self.save_incident(incident)
    
    def add_ioc(self, incident: Incident, ioc_type: str, value: str, 
                description: str = "", source: str = ""):
        """Add IOC to incident"""
        ioc = IOC(
            type=ioc_type,
            value=value,
            description=description,
            source=source
        )
        incident.iocs.append(asdict(ioc))
        self.save_incident(incident)
        
        # Also save to IOC directory
        ioc_file = IOCS_DIR / f"{ioc_type}s" / f"incident_{incident.id}.txt"
        ioc_file.parent.mkdir(parents=True, exist_ok=True)
        with open(ioc_file, "a") as f:
            f.write(f"{value}\t{description}\t{source}\n")
        
        log(f"Added IOC: {ioc_type} = {value}")
    
    def update_status(self, incident: Incident, new_status: str):
        """Update incident status"""
        old_status = incident.status
        incident.status = new_status
        
        if new_status == IncidentStatus.CLOSED.value:
            incident.closed_at = datetime.datetime.now().isoformat()
            # Move to resolved
            old_dir = INCIDENTS_DIR / "active" / incident.id
            new_dir = INCIDENTS_DIR / "resolved" / incident.id
            if old_dir.exists():
                shutil.move(str(old_dir), str(new_dir))
        
        self.add_timeline_event(incident, f"Status changed: {old_status} -> {new_status}",
                               "incident_response.py")
        log(f"Status updated: {old_status} -> {new_status}")
    
    #===========================================================================
    # CONTAINMENT ACTIONS
    #===========================================================================
    
    def contain_ip(self, ip: str, incident: Optional[Incident] = None) -> bool:
        """Block an IP address using iptables"""
        alert(f"Containing IP: {ip}")
        
        try:
            # Add iptables rule
            cmd = f"iptables -A INPUT -s {ip} -j DROP"
            result = subprocess.run(cmd.split(), capture_output=True, text=True)
            
            if result.returncode == 0:
                log(f"Successfully blocked IP: {ip}")
                if incident:
                    self.add_timeline_event(incident, f"Blocked IP: {ip}",
                                           "containment", "iptables rule added")
                    incident.actions_taken.append(f"Blocked IP {ip} via iptables")
                    self.save_incident(incident)
                return True
            else:
                error(f"Failed to block IP: {result.stderr}")
                return False
        except Exception as e:
            error(f"Error blocking IP: {e}")
            return False
    
    def contain_process(self, pid: int, incident: Optional[Incident] = None) -> bool:
        """Kill a malicious process"""
        alert(f"Killing process: {pid}")
        
        try:
            # Get process info first
            proc_info = subprocess.run(["ps", "-p", str(pid), "-o", "comm="],
                                       capture_output=True, text=True)
            proc_name = proc_info.stdout.strip()
            
            # Kill process
            os.kill(pid, 9)
            log(f"Successfully killed process {pid} ({proc_name})")
            
            if incident:
                self.add_timeline_event(incident, f"Killed process: {pid} ({proc_name})",
                                       "containment")
                incident.actions_taken.append(f"Killed process {pid} ({proc_name})")
                self.save_incident(incident)
            return True
        except ProcessLookupError:
            warn(f"Process {pid} not found")
            return False
        except PermissionError:
            error(f"Permission denied to kill process {pid}")
            return False
        except Exception as e:
            error(f"Error killing process: {e}")
            return False
    
    def contain_user(self, username: str, incident: Optional[Incident] = None) -> bool:
        """Disable a user account"""
        alert(f"Disabling user: {username}")
        
        try:
            # Lock account
            result = subprocess.run(["usermod", "-L", username],
                                   capture_output=True, text=True)
            
            if result.returncode == 0:
                log(f"Successfully disabled user: {username}")
                
                # Also expire password
                subprocess.run(["chage", "-E", "0", username], capture_output=True)
                
                if incident:
                    self.add_timeline_event(incident, f"Disabled user: {username}",
                                           "containment", "Account locked and expired")
                    incident.actions_taken.append(f"Disabled user account: {username}")
                    self.save_incident(incident)
                return True
            else:
                error(f"Failed to disable user: {result.stderr}")
                return False
        except Exception as e:
            error(f"Error disabling user: {e}")
            return False
    
    def contain_domain(self, domain: str, incident: Optional[Incident] = None) -> bool:
        """Block a domain via /etc/hosts"""
        alert(f"Blocking domain: {domain}")
        
        try:
            # Add to /etc/hosts
            with open("/etc/hosts", "a") as f:
                f.write(f"\n127.0.0.1 {domain}\n")
                f.write(f"::1 {domain}\n")
            
            log(f"Successfully blocked domain: {domain}")
            
            if incident:
                self.add_timeline_event(incident, f"Blocked domain: {domain}",
                                       "containment", "Added to /etc/hosts")
                incident.actions_taken.append(f"Blocked domain: {domain}")
                self.save_incident(incident)
            return True
        except Exception as e:
            error(f"Error blocking domain: {e}")
            return False
    
    def isolate_host(self, interface: str = "eth0", 
                     incident: Optional[Incident] = None) -> bool:
        """Isolate host by dropping all network traffic except SSH"""
        alert(f"Isolating host (keeping SSH access)")
        
        try:
            commands = [
                "iptables -F",
                "iptables -A INPUT -p tcp --dport 22 -j ACCEPT",
                "iptables -A OUTPUT -p tcp --sport 22 -j ACCEPT",
                "iptables -A INPUT -i lo -j ACCEPT",
                "iptables -A OUTPUT -o lo -j ACCEPT",
                "iptables -A INPUT -j DROP",
                "iptables -A OUTPUT -j DROP"
            ]
            
            for cmd in commands:
                subprocess.run(cmd.split(), capture_output=True)
            
            log("Host isolated - only SSH traffic allowed")
            
            if incident:
                self.add_timeline_event(incident, "Host isolated",
                                       "containment", "All traffic blocked except SSH")
                incident.actions_taken.append("Isolated host network")
                self.save_incident(incident)
            return True
        except Exception as e:
            error(f"Error isolating host: {e}")
            return False
    
    #===========================================================================
    # EVIDENCE COLLECTION
    #===========================================================================
    
    def collect_evidence(self, incident: Incident) -> Path:
        """Collect forensic evidence for an incident"""
        log("Collecting forensic evidence...")
        
        evidence_dir = FORENSICS_DIR / "artifacts" / incident.id
        evidence_dir.mkdir(parents=True, exist_ok=True)
        
        # Collect various artifacts
        artifacts = {
            "processes.txt": "ps auxf",
            "network_connections.txt": "ss -tunapl",
            "network_stats.txt": "netstat -s",
            "open_files.txt": "lsof -n",
            "users_logged.txt": "who -a",
            "last_logins.txt": "last -50",
            "crontabs.txt": "cat /etc/crontab",
            "services.txt": "systemctl list-units --type=service",
            "modules.txt": "lsmod",
            "mounts.txt": "mount",
            "env_vars.txt": "env",
            "iptables.txt": "iptables -L -n -v",
            "hosts.txt": "cat /etc/hosts",
            "passwd.txt": "cat /etc/passwd",
            "shadow_perms.txt": "ls -la /etc/shadow",
            "sudoers.txt": "cat /etc/sudoers",
            "ssh_config.txt": "cat /etc/ssh/sshd_config",
            "history_root.txt": "cat /root/.bash_history",
            "suid_files.txt": "find / -perm -4000 -type f 2>/dev/null",
            "world_writable.txt": "find / -perm -002 -type f 2>/dev/null | head -100",
            "recent_files.txt": "find / -mtime -1 -type f 2>/dev/null | head -200",
        }
        
        for filename, cmd in artifacts.items():
            try:
                result = subprocess.run(cmd, shell=True, capture_output=True, 
                                        text=True, timeout=60)
                with open(evidence_dir / filename, "w") as f:
                    f.write(f"# Command: {cmd}\n")
                    f.write(f"# Timestamp: {datetime.datetime.now().isoformat()}\n\n")
                    f.write(result.stdout)
                    if result.stderr:
                        f.write(f"\n# STDERR:\n{result.stderr}")
            except Exception as e:
                warn(f"Failed to collect {filename}: {e}")
        
        # Copy important logs
        log_files = [
            "/var/log/auth.log",
            "/var/log/syslog",
            "/var/log/kern.log",
            "/var/log/messages",
            "/var/log/secure",
            "/var/log/audit/audit.log"
        ]
        
        logs_dir = evidence_dir / "logs"
        logs_dir.mkdir(exist_ok=True)
        
        for log_file in log_files:
            if os.path.exists(log_file):
                try:
                    shutil.copy2(log_file, logs_dir / os.path.basename(log_file))
                except Exception as e:
                    warn(f"Failed to copy {log_file}: {e}")
        
        # Create evidence manifest
        manifest = {
            "incident_id": incident.id,
            "collection_time": datetime.datetime.now().isoformat(),
            "hostname": socket.gethostname(),
            "collector": os.getenv("USER", "unknown"),
            "artifacts": list(artifacts.keys()),
            "logs_collected": [os.path.basename(f) for f in log_files if os.path.exists(f)]
        }
        
        with open(evidence_dir / "manifest.json", "w") as f:
            json.dump(manifest, f, indent=2)
        
        # Calculate hashes
        hash_file = evidence_dir / "hashes.txt"
        with open(hash_file, "w") as f:
            for file in evidence_dir.rglob("*"):
                if file.is_file() and file.name != "hashes.txt":
                    try:
                        sha256 = hashlib.sha256(file.read_bytes()).hexdigest()
                        f.write(f"{sha256}  {file.relative_to(evidence_dir)}\n")
                    except Exception:
                        pass
        
        self.add_timeline_event(incident, "Evidence collected",
                               "forensics", f"Saved to {evidence_dir}")
        incident.actions_taken.append(f"Collected forensic evidence to {evidence_dir}")
        self.save_incident(incident)
        
        log(f"Evidence collected to: {evidence_dir}")
        return evidence_dir
    
    #===========================================================================
    # REPORTING
    #===========================================================================
    
    def generate_report(self, incident: Incident) -> Path:
        """Generate incident report"""
        log(f"Generating report for incident: {incident.id}")
        
        report_file = REPORTS_DIR / "incident" / f"{incident.id}_report.md"
        report_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Build report
        report = f"""# Incident Report: {incident.id}

## Executive Summary

| Field | Value |
|-------|-------|
| **Incident ID** | {incident.id} |
| **Title** | {incident.title} |
| **Severity** | {incident.severity.upper()} |
| **Status** | {incident.status} |
| **Type** | {incident.type} |
| **Created** | {incident.created_at} |
| **Last Updated** | {incident.updated_at} |
| **Analyst** | {incident.analyst} |

## Description

{incident.description}

## Affected Assets

### Hosts
{chr(10).join(f"- {h}" for h in incident.affected_hosts) if incident.affected_hosts else "- None identified"}

### Users
{chr(10).join(f"- {u}" for u in incident.affected_users) if incident.affected_users else "- None identified"}

## Timeline of Events

| Timestamp | Event | Source | Details |
|-----------|-------|--------|---------|
"""
        for event in incident.timeline:
            report += f"| {event.get('timestamp', 'N/A')} | {event.get('event', 'N/A')} | {event.get('source', 'N/A')} | {event.get('details', '')} |\n"

        report += f"""

## Indicators of Compromise (IOCs)

| Type | Value | Description | Source |
|------|-------|-------------|--------|
"""
        for ioc in incident.iocs:
            report += f"| {ioc.get('type', 'N/A')} | `{ioc.get('value', 'N/A')}` | {ioc.get('description', '')} | {ioc.get('source', '')} |\n"

        report += f"""

## MITRE ATT&CK Mapping

{chr(10).join(f"- {t}" for t in incident.mitre_techniques) if incident.mitre_techniques else "- Not yet mapped"}

## Actions Taken

{chr(10).join(f"1. {a}" for i, a in enumerate(incident.actions_taken)) if incident.actions_taken else "- No actions taken yet"}

## Recommendations

{chr(10).join(f"1. {r}" for i, r in enumerate(incident.recommendations)) if incident.recommendations else "- No recommendations yet"}

## Lessons Learned

*To be completed after incident closure*

---

**Report Generated:** {datetime.datetime.now().isoformat()}
**Generated By:** BlueTeam-Windsurf Incident Response System
"""
        
        with open(report_file, "w") as f:
            f.write(report)
        
        log(f"Report generated: {report_file}")
        return report_file
    
    def list_incidents(self, status: str = "all"):
        """List all incidents"""
        print(f"\n{'='*80}")
        print(f"{'ID':<20} {'Title':<30} {'Severity':<10} {'Status':<15}")
        print(f"{'='*80}")
        
        for status_dir in ["active", "resolved"]:
            if status != "all" and status != status_dir:
                continue
                
            incidents_path = INCIDENTS_DIR / status_dir
            if incidents_path.exists():
                for incident_dir in sorted(incidents_path.iterdir()):
                    incident_file = incident_dir / "incident.json"
                    if incident_file.exists():
                        with open(incident_file) as f:
                            inc = json.load(f)
                        
                        severity_color = {
                            "critical": Colors.RED,
                            "high": Colors.YELLOW,
                            "medium": Colors.BLUE,
                            "low": Colors.GREEN
                        }.get(inc.get("severity", ""), Colors.NC)
                        
                        print(f"{inc.get('id', 'N/A'):<20} "
                              f"{inc.get('title', 'N/A')[:28]:<30} "
                              f"{severity_color}{inc.get('severity', 'N/A'):<10}{Colors.NC} "
                              f"{inc.get('status', 'N/A'):<15}")
        
        print(f"{'='*80}\n")

def show_banner():
    print(f"""{Colors.CYAN}
╔══════════════════════════════════════════════════════════════════════╗
║     🚨 BlueTeam Incident Response System                             ║
║        Powered by Windsurf AI                                        ║
╚══════════════════════════════════════════════════════════════════════╝
{Colors.NC}""")

def main():
    parser = argparse.ArgumentParser(
        description="BlueTeam-Windsurf Incident Response System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --new-incident                    Create new incident interactively
  %(prog)s --new "Malware detected" -s high  Create incident with title
  %(prog)s --list                            List all incidents
  %(prog)s --list active                     List active incidents
  %(prog)s --contain --ip 192.168.1.100      Block an IP address
  %(prog)s --contain --pid 1234              Kill a process
  %(prog)s --contain --user baduser          Disable a user
  %(prog)s --contain --domain evil.com       Block a domain
  %(prog)s --isolate                         Isolate the host
  %(prog)s --collect INC-2024-0001           Collect evidence for incident
  %(prog)s --report INC-2024-0001            Generate incident report
        """
    )
    
    parser.add_argument("--new-incident", action="store_true",
                       help="Create new incident interactively")
    parser.add_argument("--new", type=str, metavar="TITLE",
                       help="Create new incident with title")
    parser.add_argument("-s", "--severity", type=str, 
                       choices=["critical", "high", "medium", "low"],
                       default="high", help="Incident severity")
    parser.add_argument("-t", "--type", type=str,
                       choices=["malware", "ransomware", "phishing", "data_breach",
                               "ddos", "intrusion", "insider_threat", "apt", 
                               "cryptomining", "unknown"],
                       default="unknown", help="Incident type")
    parser.add_argument("-d", "--description", type=str, default="",
                       help="Incident description")
    
    parser.add_argument("--list", nargs="?", const="all", metavar="STATUS",
                       help="List incidents (all, active, resolved)")
    
    parser.add_argument("--contain", action="store_true",
                       help="Execute containment action")
    parser.add_argument("--ip", type=str, help="IP to block")
    parser.add_argument("--pid", type=int, help="Process ID to kill")
    parser.add_argument("--user", type=str, help="User to disable")
    parser.add_argument("--domain", type=str, help="Domain to block")
    parser.add_argument("--isolate", action="store_true",
                       help="Isolate host (block all traffic except SSH)")
    
    parser.add_argument("--collect", type=str, metavar="INCIDENT_ID",
                       help="Collect evidence for incident")
    parser.add_argument("--report", type=str, metavar="INCIDENT_ID",
                       help="Generate report for incident")
    
    parser.add_argument("--incident", type=str, metavar="INCIDENT_ID",
                       help="Associate action with incident")
    
    args = parser.parse_args()
    
    show_banner()
    irs = IncidentResponseSystem()
    
    # Load incident if specified
    incident = None
    if args.incident:
        incident = irs.load_incident(args.incident)
        if not incident:
            error(f"Incident not found: {args.incident}")
            sys.exit(1)
    
    # Handle commands
    if args.new_incident or args.new:
        title = args.new if args.new else input("Incident title: ")
        description = args.description if args.description else input("Description: ")
        incident = irs.create_incident(title, description, args.severity, args.type)
        print(f"\n{Colors.GREEN}✓ Incident created: {incident.id}{Colors.NC}\n")
    
    elif args.list is not None:
        irs.list_incidents(args.list)
    
    elif args.contain:
        if args.ip:
            irs.contain_ip(args.ip, incident)
        elif args.pid:
            irs.contain_process(args.pid, incident)
        elif args.user:
            irs.contain_user(args.user, incident)
        elif args.domain:
            irs.contain_domain(args.domain, incident)
        else:
            error("Specify target: --ip, --pid, --user, or --domain")
    
    elif args.isolate:
        irs.isolate_host(incident=incident)
    
    elif args.collect:
        incident = irs.load_incident(args.collect)
        if incident:
            irs.collect_evidence(incident)
        else:
            error(f"Incident not found: {args.collect}")
    
    elif args.report:
        incident = irs.load_incident(args.report)
        if incident:
            report_path = irs.generate_report(incident)
            print(f"\n{Colors.GREEN}✓ Report generated: {report_path}{Colors.NC}\n")
        else:
            error(f"Incident not found: {args.report}")
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
