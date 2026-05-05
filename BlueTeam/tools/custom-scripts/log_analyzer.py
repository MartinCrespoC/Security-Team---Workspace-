#!/usr/bin/env python3
"""
BlueTeam-Windsurf - AI-Powered Log Analyzer
Intelligent log analysis with pattern detection and threat correlation
"""

import os
import sys
import re
import json
import argparse
import hashlib
import gzip
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from collections import defaultdict, Counter
from dataclasses import dataclass, field, asdict
import ipaddress

# Colors
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
ALERTS_DIR = BASE_DIR / "alerts"
IOCS_DIR = BASE_DIR / "iocs"
REPORTS_DIR = BASE_DIR / "reports"

@dataclass
class LogEvent:
    timestamp: str
    source: str
    message: str
    severity: str = "info"
    category: str = "general"
    raw: str = ""
    parsed: Dict = field(default_factory=dict)

@dataclass
class SecurityFinding:
    title: str
    description: str
    severity: str
    category: str
    count: int = 1
    samples: List[str] = field(default_factory=list)
    iocs: List[str] = field(default_factory=list)
    mitre: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)

class LogAnalyzer:
    """AI-powered log analyzer for security events"""
    
    # Attack patterns with MITRE ATT&CK mapping
    ATTACK_PATTERNS = {
        # Authentication attacks
        "brute_force": {
            "patterns": [
                r"Failed password for .* from (\d+\.\d+\.\d+\.\d+)",
                r"authentication failure.*rhost=(\d+\.\d+\.\d+\.\d+)",
                r"Invalid user .* from (\d+\.\d+\.\d+\.\d+)",
                r"Failed login attempt from (\d+\.\d+\.\d+\.\d+)",
            ],
            "threshold": 5,
            "severity": "high",
            "mitre": ["T1110 - Brute Force"],
            "category": "authentication"
        },
        "successful_login": {
            "patterns": [
                r"Accepted password for (\w+) from (\d+\.\d+\.\d+\.\d+)",
                r"Accepted publickey for (\w+) from (\d+\.\d+\.\d+\.\d+)",
                r"session opened for user (\w+)",
            ],
            "threshold": 1,
            "severity": "info",
            "mitre": ["T1078 - Valid Accounts"],
            "category": "authentication"
        },
        "privilege_escalation": {
            "patterns": [
                r"sudo:.*COMMAND=(.+)",
                r"su\[\d+\]: .* to root",
                r"pkexec.*COMMAND=(.+)",
                r"Successful su for root",
            ],
            "threshold": 1,
            "severity": "medium",
            "mitre": ["T1548 - Abuse Elevation Control Mechanism"],
            "category": "privilege_escalation"
        },
        
        # Web attacks
        "sql_injection": {
            "patterns": [
                r"(?:union\s+select|select\s+.*\s+from|insert\s+into|update\s+.*\s+set|delete\s+from)",
                r"(?:or\s+1\s*=\s*1|and\s+1\s*=\s*1|'\s*or\s*'|;\s*drop\s+table)",
                r"(?:--\s*$|/\*.*\*/|#.*$)",
                r"(?:benchmark\s*\(|sleep\s*\(|waitfor\s+delay)",
            ],
            "threshold": 1,
            "severity": "critical",
            "mitre": ["T1190 - Exploit Public-Facing Application"],
            "category": "web_attack"
        },
        "xss": {
            "patterns": [
                r"<script[^>]*>",
                r"javascript\s*:",
                r"on(?:error|load|click|mouseover)\s*=",
                r"<img[^>]+onerror\s*=",
            ],
            "threshold": 1,
            "severity": "high",
            "mitre": ["T1059.007 - JavaScript"],
            "category": "web_attack"
        },
        "path_traversal": {
            "patterns": [
                r"\.\.\/",
                r"\.\.\\",
                r"%2e%2e%2f",
                r"%2e%2e/",
                r"\.\.%2f",
            ],
            "threshold": 1,
            "severity": "high",
            "mitre": ["T1083 - File and Directory Discovery"],
            "category": "web_attack"
        },
        "command_injection": {
            "patterns": [
                r";\s*(?:cat|ls|id|whoami|uname|pwd|wget|curl|nc|bash|sh)\s",
                r"\|\s*(?:cat|ls|id|whoami|uname|pwd|wget|curl|nc|bash|sh)\s",
                r"`[^`]+`",
                r"\$\([^)]+\)",
            ],
            "threshold": 1,
            "severity": "critical",
            "mitre": ["T1059 - Command and Scripting Interpreter"],
            "category": "web_attack"
        },
        
        # Reconnaissance
        "port_scan": {
            "patterns": [
                r"Connection from (\d+\.\d+\.\d+\.\d+) port \d+",
                r"SYN flood",
                r"port scan detected from (\d+\.\d+\.\d+\.\d+)",
            ],
            "threshold": 20,
            "severity": "medium",
            "mitre": ["T1046 - Network Service Discovery"],
            "category": "reconnaissance"
        },
        "directory_enumeration": {
            "patterns": [
                r"(?:GET|POST)\s+/(?:admin|wp-admin|phpmyadmin|manager|console)",
                r"(?:GET|POST)\s+.*(?:\.bak|\.old|\.backup|\.sql|\.zip)",
                r"(?:nikto|dirbuster|gobuster|wfuzz|dirb)",
            ],
            "threshold": 10,
            "severity": "medium",
            "mitre": ["T1083 - File and Directory Discovery"],
            "category": "reconnaissance"
        },
        
        # Malware indicators
        "c2_communication": {
            "patterns": [
                r"(?:POST|GET)\s+/[a-zA-Z0-9]{32,}",
                r"User-Agent:.*(?:curl|wget|python|powershell)",
                r"beacon",
                r"callback",
            ],
            "threshold": 3,
            "severity": "critical",
            "mitre": ["T1071 - Application Layer Protocol"],
            "category": "malware"
        },
        "suspicious_process": {
            "patterns": [
                r"(?:nc|ncat|netcat)\s+-[el]",
                r"bash\s+-i\s+>&",
                r"python\s+-c\s+['\"]import",
                r"perl\s+-e\s+['\"]",
                r"powershell.*-enc",
                r"certutil.*-urlcache",
            ],
            "threshold": 1,
            "severity": "critical",
            "mitre": ["T1059 - Command and Scripting Interpreter"],
            "category": "malware"
        },
        
        # Data exfiltration
        "data_exfiltration": {
            "patterns": [
                r"(?:scp|rsync|ftp|sftp).*(?:external|remote)",
                r"curl.*-d.*@",
                r"wget.*--post-file",
                r"base64.*\|.*curl",
            ],
            "threshold": 1,
            "severity": "critical",
            "mitre": ["T1041 - Exfiltration Over C2 Channel"],
            "category": "exfiltration"
        },
        
        # System events
        "service_failure": {
            "patterns": [
                r"(?:failed|error|crash|segfault|killed)",
                r"service .* (?:failed|stopped|crashed)",
                r"Out of memory",
                r"kernel panic",
            ],
            "threshold": 5,
            "severity": "medium",
            "mitre": ["T1499 - Endpoint Denial of Service"],
            "category": "system"
        },
        "file_modification": {
            "patterns": [
                r"(?:modified|changed|deleted|created)\s+(?:/etc/passwd|/etc/shadow|/etc/sudoers)",
                r"chmod\s+(?:777|666|4755)",
                r"chown\s+root",
            ],
            "threshold": 1,
            "severity": "high",
            "mitre": ["T1222 - File and Directory Permissions Modification"],
            "category": "persistence"
        },
    }
    
    # Log format parsers
    LOG_PARSERS = {
        "syslog": r"^(\w{3}\s+\d+\s+\d+:\d+:\d+)\s+(\S+)\s+(\S+?)(?:\[\d+\])?:\s+(.+)$",
        "apache_access": r'^(\S+)\s+\S+\s+\S+\s+\[([^\]]+)\]\s+"([^"]+)"\s+(\d+)\s+(\d+)',
        "apache_error": r"^\[([^\]]+)\]\s+\[(\w+)\]\s+\[([^\]]+)\]\s+(.+)$",
        "nginx_access": r'^(\S+)\s+-\s+-\s+\[([^\]]+)\]\s+"([^"]+)"\s+(\d+)\s+(\d+)',
        "auth": r"^(\w{3}\s+\d+\s+\d+:\d+:\d+)\s+(\S+)\s+(\S+?)(?:\[\d+\])?:\s+(.+)$",
        "json": r"^\{.*\}$",
    }
    
    def __init__(self):
        self.findings: List[SecurityFinding] = []
        self.events: List[LogEvent] = []
        self.stats = defaultdict(int)
        self.ip_activity = defaultdict(list)
        self.user_activity = defaultdict(list)
        self.timeline = []
        
    def detect_log_format(self, line: str) -> str:
        """Detect the format of a log line"""
        for format_name, pattern in self.LOG_PARSERS.items():
            if re.match(pattern, line):
                return format_name
        return "unknown"
    
    def parse_line(self, line: str, log_format: str = "auto") -> Optional[LogEvent]:
        """Parse a single log line"""
        line = line.strip()
        if not line:
            return None
            
        if log_format == "auto":
            log_format = self.detect_log_format(line)
        
        event = LogEvent(
            timestamp=datetime.now().isoformat(),
            source="unknown",
            message=line,
            raw=line
        )
        
        try:
            if log_format == "syslog" or log_format == "auth":
                match = re.match(self.LOG_PARSERS["syslog"], line)
                if match:
                    event.timestamp = match.group(1)
                    event.source = match.group(3)
                    event.message = match.group(4)
                    event.parsed = {
                        "host": match.group(2),
                        "program": match.group(3)
                    }
                    
            elif log_format == "apache_access" or log_format == "nginx_access":
                match = re.match(self.LOG_PARSERS[log_format], line)
                if match:
                    event.timestamp = match.group(2)
                    event.source = "webserver"
                    event.message = match.group(3)
                    event.parsed = {
                        "client_ip": match.group(1),
                        "request": match.group(3),
                        "status": match.group(4),
                        "bytes": match.group(5)
                    }
                    
            elif log_format == "json":
                try:
                    data = json.loads(line)
                    event.timestamp = data.get("timestamp", data.get("@timestamp", ""))
                    event.source = data.get("source", data.get("program", "unknown"))
                    event.message = data.get("message", str(data))
                    event.parsed = data
                except json.JSONDecodeError:
                    pass
                    
        except Exception as e:
            warn(f"Parse error: {e}")
            
        return event
    
    def extract_ips(self, text: str) -> List[str]:
        """Extract IP addresses from text"""
        ip_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
        ips = re.findall(ip_pattern, text)
        valid_ips = []
        for ip in ips:
            try:
                ipaddress.ip_address(ip)
                if not ip.startswith("127.") and not ip.startswith("0."):
                    valid_ips.append(ip)
            except ValueError:
                pass
        return valid_ips
    
    def extract_users(self, text: str) -> List[str]:
        """Extract usernames from text"""
        patterns = [
            r"user[=:\s]+(\w+)",
            r"for\s+(?:user\s+)?(\w+)\s+from",
            r"session opened for user (\w+)",
            r"Accepted \w+ for (\w+)",
        ]
        users = []
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            users.extend(matches)
        return list(set(users))
    
    def analyze_event(self, event: LogEvent) -> List[SecurityFinding]:
        """Analyze a single event for security issues"""
        findings = []
        
        for attack_name, config in self.ATTACK_PATTERNS.items():
            for pattern in config["patterns"]:
                if re.search(pattern, event.message, re.IGNORECASE):
                    # Extract IOCs
                    iocs = self.extract_ips(event.message)
                    
                    finding = SecurityFinding(
                        title=attack_name.replace("_", " ").title(),
                        description=f"Detected {attack_name} pattern in logs",
                        severity=config["severity"],
                        category=config["category"],
                        samples=[event.message[:200]],
                        iocs=iocs,
                        mitre=config["mitre"]
                    )
                    findings.append(finding)
                    
                    # Track IP activity
                    for ip in iocs:
                        self.ip_activity[ip].append({
                            "attack": attack_name,
                            "timestamp": event.timestamp,
                            "message": event.message[:100]
                        })
                    
                    # Track user activity
                    for user in self.extract_users(event.message):
                        self.user_activity[user].append({
                            "attack": attack_name,
                            "timestamp": event.timestamp,
                            "message": event.message[:100]
                        })
                    
                    break  # One finding per pattern group
                    
        return findings
    
    def analyze_file(self, filepath: str, max_lines: int = 100000) -> Dict[str, Any]:
        """Analyze a log file"""
        log(f"Analyzing: {filepath}")
        
        path = Path(filepath)
        if not path.exists():
            error(f"File not found: {filepath}")
            return {}
        
        # Handle gzipped files
        opener = gzip.open if filepath.endswith('.gz') else open
        
        line_count = 0
        finding_counts = defaultdict(int)
        
        try:
            with opener(filepath, 'rt', errors='ignore') as f:
                for line in f:
                    if line_count >= max_lines:
                        warn(f"Reached max lines limit ({max_lines})")
                        break
                        
                    line_count += 1
                    event = self.parse_line(line)
                    
                    if event:
                        self.events.append(event)
                        findings = self.analyze_event(event)
                        
                        for finding in findings:
                            finding_counts[finding.title] += 1
                            
                            # Aggregate findings
                            existing = next((f for f in self.findings 
                                           if f.title == finding.title), None)
                            if existing:
                                existing.count += 1
                                if len(existing.samples) < 5:
                                    existing.samples.extend(finding.samples)
                                existing.iocs = list(set(existing.iocs + finding.iocs))
                            else:
                                self.findings.append(finding)
                                
        except Exception as e:
            error(f"Error reading file: {e}")
            return {}
        
        self.stats["lines_analyzed"] = line_count
        self.stats["findings_count"] = len(self.findings)
        self.stats["unique_ips"] = len(self.ip_activity)
        self.stats["unique_users"] = len(self.user_activity)
        
        log(f"Analyzed {line_count} lines")
        log(f"Found {len(self.findings)} unique security findings")
        
        return {
            "stats": dict(self.stats),
            "findings": [asdict(f) for f in self.findings],
            "ip_activity": dict(self.ip_activity),
            "user_activity": dict(self.user_activity)
        }
    
    def analyze_directory(self, dirpath: str, pattern: str = "*.log") -> Dict[str, Any]:
        """Analyze all log files in a directory"""
        log(f"Analyzing directory: {dirpath}")
        
        path = Path(dirpath)
        if not path.exists():
            error(f"Directory not found: {dirpath}")
            return {}
        
        results = {}
        for log_file in path.rglob(pattern):
            results[str(log_file)] = self.analyze_file(str(log_file))
        
        # Also check for .gz files
        for log_file in path.rglob(f"{pattern}.gz"):
            results[str(log_file)] = self.analyze_file(str(log_file))
            
        return results
    
    def correlate_events(self) -> List[Dict]:
        """Correlate events to identify attack chains"""
        correlations = []
        
        # Find IPs with multiple attack types
        for ip, activities in self.ip_activity.items():
            attack_types = set(a["attack"] for a in activities)
            if len(attack_types) > 1:
                correlations.append({
                    "type": "multi_stage_attack",
                    "ip": ip,
                    "attack_types": list(attack_types),
                    "event_count": len(activities),
                    "severity": "critical" if len(attack_types) > 2 else "high",
                    "description": f"IP {ip} involved in multiple attack types: {', '.join(attack_types)}"
                })
        
        # Find users with suspicious activity
        for user, activities in self.user_activity.items():
            attack_types = set(a["attack"] for a in activities)
            suspicious_attacks = {"privilege_escalation", "suspicious_process", 
                                "data_exfiltration", "file_modification"}
            if attack_types & suspicious_attacks:
                correlations.append({
                    "type": "compromised_account",
                    "user": user,
                    "attack_types": list(attack_types),
                    "event_count": len(activities),
                    "severity": "critical",
                    "description": f"User {user} shows signs of compromise: {', '.join(attack_types)}"
                })
        
        # Detect brute force followed by successful login
        for ip, activities in self.ip_activity.items():
            brute_force = [a for a in activities if a["attack"] == "brute_force"]
            success = [a for a in activities if a["attack"] == "successful_login"]
            if brute_force and success:
                correlations.append({
                    "type": "successful_brute_force",
                    "ip": ip,
                    "failed_attempts": len(brute_force),
                    "successful_logins": len(success),
                    "severity": "critical",
                    "description": f"IP {ip} had {len(brute_force)} failed attempts followed by successful login"
                })
        
        return correlations
    
    def generate_report(self, output_path: Optional[str] = None) -> str:
        """Generate analysis report"""
        correlations = self.correlate_events()
        
        report = f"""# Log Analysis Report

**Generated:** {datetime.now().isoformat()}
**Analyzer:** BlueTeam-Windsurf AI Log Analyzer

---

## Executive Summary

| Metric | Value |
|--------|-------|
| Lines Analyzed | {self.stats.get('lines_analyzed', 0):,} |
| Security Findings | {len(self.findings)} |
| Unique IPs | {len(self.ip_activity)} |
| Unique Users | {len(self.user_activity)} |
| Correlations | {len(correlations)} |

---

## Critical Findings

"""
        # Sort findings by severity
        severity_order = {"critical": 0, "high": 1, "medium": 2, "low": 3, "info": 4}
        sorted_findings = sorted(self.findings, 
                                key=lambda x: severity_order.get(x.severity, 5))
        
        for finding in sorted_findings:
            severity_emoji = {
                "critical": "🔴",
                "high": "🟠", 
                "medium": "🟡",
                "low": "🟢",
                "info": "🔵"
            }.get(finding.severity, "⚪")
            
            report += f"""### {severity_emoji} {finding.title}

- **Severity:** {finding.severity.upper()}
- **Category:** {finding.category}
- **Count:** {finding.count}
- **MITRE ATT&CK:** {', '.join(finding.mitre)}

**IOCs:**
"""
            for ioc in finding.iocs[:10]:
                report += f"- `{ioc}`\n"
            
            report += "\n**Sample Events:**\n```\n"
            for sample in finding.samples[:3]:
                report += f"{sample}\n"
            report += "```\n\n---\n\n"
        
        # Correlations
        if correlations:
            report += "## Attack Correlations\n\n"
            for corr in correlations:
                report += f"""### {corr['type'].replace('_', ' ').title()}

- **Severity:** {corr['severity'].upper()}
- **Description:** {corr['description']}

"""
        
        # Top IPs
        report += "## Top Suspicious IPs\n\n"
        report += "| IP Address | Events | Attack Types |\n"
        report += "|------------|--------|-------------|\n"
        
        sorted_ips = sorted(self.ip_activity.items(), 
                           key=lambda x: len(x[1]), reverse=True)[:20]
        for ip, activities in sorted_ips:
            attack_types = set(a["attack"] for a in activities)
            report += f"| `{ip}` | {len(activities)} | {', '.join(attack_types)} |\n"
        
        # Recommendations
        report += """

## Recommendations

1. **Immediate Actions:**
   - Block IPs showing malicious activity
   - Reset credentials for potentially compromised accounts
   - Isolate affected systems if necessary

2. **Investigation:**
   - Review all critical and high severity findings
   - Correlate with other log sources
   - Check for lateral movement

3. **Hardening:**
   - Implement rate limiting for authentication
   - Enable Web Application Firewall (WAF)
   - Review and update firewall rules

4. **Monitoring:**
   - Set up alerts for detected patterns
   - Increase logging verbosity if needed
   - Consider deploying additional sensors

---

*Report generated by BlueTeam-Windsurf AI Log Analyzer*
"""
        
        if output_path:
            with open(output_path, 'w') as f:
                f.write(report)
            log(f"Report saved to: {output_path}")
        
        return report
    
    def export_iocs(self, output_dir: Optional[str] = None) -> Dict[str, List[str]]:
        """Export discovered IOCs"""
        if output_dir is None:
            output_dir = str(IOCS_DIR)
        
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Collect all IOCs
        all_ips = set()
        for finding in self.findings:
            all_ips.update(finding.iocs)
        
        # Save IPs
        if all_ips:
            ip_file = output_path / "ips" / f"analyzed_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            ip_file.parent.mkdir(exist_ok=True)
            with open(ip_file, 'w') as f:
                f.write(f"# IOCs extracted from log analysis\n")
                f.write(f"# Generated: {datetime.now().isoformat()}\n\n")
                for ip in sorted(all_ips):
                    f.write(f"{ip}\n")
            log(f"Exported {len(all_ips)} IPs to {ip_file}")
        
        return {"ips": list(all_ips)}
    
    def print_summary(self):
        """Print analysis summary to console"""
        print(f"\n{'='*70}")
        print(f"{Colors.CYAN}📊 LOG ANALYSIS SUMMARY{Colors.NC}")
        print(f"{'='*70}\n")
        
        print(f"📈 Statistics:")
        print(f"   • Lines analyzed: {self.stats.get('lines_analyzed', 0):,}")
        print(f"   • Security findings: {len(self.findings)}")
        print(f"   • Unique IPs: {len(self.ip_activity)}")
        print(f"   • Unique users: {len(self.user_activity)}")
        
        if self.findings:
            print(f"\n🚨 Findings by Severity:")
            severity_counts = Counter(f.severity for f in self.findings)
            for sev in ["critical", "high", "medium", "low", "info"]:
                if sev in severity_counts:
                    emoji = {"critical": "🔴", "high": "🟠", "medium": "🟡", 
                            "low": "🟢", "info": "🔵"}[sev]
                    print(f"   {emoji} {sev.upper()}: {severity_counts[sev]}")
            
            print(f"\n🎯 Top Findings:")
            for finding in sorted(self.findings, 
                                 key=lambda x: x.count, reverse=True)[:5]:
                print(f"   • {finding.title}: {finding.count} occurrences")
        
        if self.ip_activity:
            print(f"\n🌐 Top Suspicious IPs:")
            for ip, activities in sorted(self.ip_activity.items(),
                                        key=lambda x: len(x[1]), 
                                        reverse=True)[:5]:
                print(f"   • {ip}: {len(activities)} events")
        
        print(f"\n{'='*70}\n")


def show_banner():
    print(f"""{Colors.CYAN}
╔══════════════════════════════════════════════════════════════════════╗
║     📊 BlueTeam AI Log Analyzer                                      ║
║        Powered by Windsurf AI                                        ║
╚══════════════════════════════════════════════════════════════════════╝
{Colors.NC}""")


def main():
    parser = argparse.ArgumentParser(
        description="BlueTeam-Windsurf AI-Powered Log Analyzer",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --analyze /var/log/auth.log
  %(prog)s --analyze /var/log/apache2/access.log --report report.md
  %(prog)s --directory /var/log --pattern "*.log"
  %(prog)s --analyze /var/log/syslog --export-iocs
        """
    )
    
    parser.add_argument("--analyze", "-a", type=str, metavar="FILE",
                       help="Analyze a single log file")
    parser.add_argument("--directory", "-d", type=str, metavar="DIR",
                       help="Analyze all logs in directory")
    parser.add_argument("--pattern", "-p", type=str, default="*.log",
                       help="File pattern for directory analysis (default: *.log)")
    parser.add_argument("--report", "-r", type=str, metavar="FILE",
                       help="Generate report to file")
    parser.add_argument("--export-iocs", action="store_true",
                       help="Export discovered IOCs")
    parser.add_argument("--json", "-j", type=str, metavar="FILE",
                       help="Export results as JSON")
    parser.add_argument("--max-lines", type=int, default=100000,
                       help="Maximum lines to analyze (default: 100000)")
    parser.add_argument("--quiet", "-q", action="store_true",
                       help="Suppress output")
    
    args = parser.parse_args()
    
    if not args.quiet:
        show_banner()
    
    analyzer = LogAnalyzer()
    
    if args.analyze:
        results = analyzer.analyze_file(args.analyze, args.max_lines)
    elif args.directory:
        results = analyzer.analyze_directory(args.directory, args.pattern)
    else:
        parser.print_help()
        return
    
    if not args.quiet:
        analyzer.print_summary()
    
    if args.report:
        analyzer.generate_report(args.report)
    
    if args.export_iocs:
        analyzer.export_iocs()
    
    if args.json:
        with open(args.json, 'w') as f:
            json.dump({
                "stats": dict(analyzer.stats),
                "findings": [asdict(f) for f in analyzer.findings],
                "correlations": analyzer.correlate_events(),
                "ip_activity": {k: v for k, v in list(analyzer.ip_activity.items())[:100]},
                "user_activity": dict(analyzer.user_activity)
            }, f, indent=2)
        log(f"Results exported to: {args.json}")


if __name__ == "__main__":
    main()
