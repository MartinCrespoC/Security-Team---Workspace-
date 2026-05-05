#!/usr/bin/env python3
"""
🟠 ORANGE TEAM - Awareness Metrics Analyzer
Análisis y visualización de métricas de concientización
"""

import os
import sys
import json
import argparse
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any, Tuple
from dataclasses import dataclass, asdict, field
from enum import Enum
import logging

# Third-party imports
try:
    import requests
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
    from rich.layout import Layout
    from rich.live import Live
    from rich import print as rprint
except ImportError:
    print("Installing required packages...")
    os.system("pip install requests rich")
    import requests
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
    from rich.layout import Layout
    from rich.live import Live
    from rich import print as rprint

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

console = Console()


@dataclass
class MetricThreshold:
    """Threshold configuration for a metric"""
    target: float
    warning: float
    critical: float
    unit: str = "percent"


@dataclass
class KPI:
    """Key Performance Indicator"""
    name: str
    value: float
    target: float
    unit: str
    trend: float = 0.0  # Positive = improving, negative = worsening
    status: str = "normal"  # normal, warning, critical


@dataclass
class DepartmentMetrics:
    """Metrics for a specific department"""
    name: str
    click_rate: float
    report_rate: float
    training_completion: float
    risk_score: int
    user_count: int


@dataclass
class MetricsReport:
    """Complete metrics report"""
    generated_at: datetime
    period_start: datetime
    period_end: datetime
    kpis: List[KPI]
    department_metrics: List[DepartmentMetrics]
    high_risk_users: List[Dict]
    recommendations: List[str]


class MetricStatus(Enum):
    GOOD = "good"
    WARNING = "warning"
    CRITICAL = "critical"


class AwarenessMetricsAnalyzer:
    """Analyzer for security awareness metrics"""
    
    THRESHOLDS = {
        "click_rate": MetricThreshold(target=5, warning=10, critical=15),
        "report_rate": MetricThreshold(target=80, warning=60, critical=40),
        "credential_submit": MetricThreshold(target=2, warning=5, critical=10),
        "training_completion": MetricThreshold(target=95, warning=85, critical=75),
        "time_to_report": MetricThreshold(target=5, warning=15, critical=30, unit="minutes"),
        "repeat_offenders": MetricThreshold(target=3, warning=5, critical=10),
    }
    
    def __init__(self):
        self.gophish_url = os.getenv("GOPHISH_URL", "https://localhost:3333")
        self.gophish_api_key = os.getenv("GOPHISH_API_KEY", "")
        self.data_dir = "metrics/data"
        os.makedirs(self.data_dir, exist_ok=True)
    
    def _get_status(self, metric_name: str, value: float) -> Tuple[str, str]:
        """Get status and color for a metric value"""
        threshold = self.THRESHOLDS.get(metric_name)
        if not threshold:
            return "normal", "white"
        
        # For metrics where lower is better (click_rate, credential_submit, etc.)
        if metric_name in ["click_rate", "credential_submit", "time_to_report", "repeat_offenders"]:
            if value <= threshold.target:
                return "good", "green"
            elif value <= threshold.warning:
                return "warning", "yellow"
            else:
                return "critical", "red"
        # For metrics where higher is better (report_rate, training_completion)
        else:
            if value >= threshold.target:
                return "good", "green"
            elif value >= threshold.warning:
                return "warning", "yellow"
            else:
                return "critical", "red"
    
    def collect_metrics(self) -> Dict[str, Any]:
        """Collect metrics from all sources"""
        console.print("[bold orange1]📊 Collecting Metrics...[/bold orange1]\n")
        
        metrics = {
            "timestamp": datetime.now().isoformat(),
            "campaigns": self._collect_campaign_metrics(),
            "training": self._collect_training_metrics(),
            "users": self._collect_user_metrics(),
        }
        
        # Save metrics
        self._save_metrics(metrics)
        
        return metrics
    
    def _collect_campaign_metrics(self) -> Dict:
        """Collect metrics from phishing campaigns"""
        # In production, this would call GoPhish API
        # For demo, using sample data
        return {
            "total_campaigns": 12,
            "active_campaigns": 2,
            "total_emails_sent": 15000,
            "total_opened": 10500,
            "total_clicked": 1875,
            "total_submitted": 450,
            "total_reported": 8250,
            "click_rate": 12.5,
            "report_rate": 55.0,
            "credential_submit_rate": 3.0,
        }
    
    def _collect_training_metrics(self) -> Dict:
        """Collect metrics from training platform"""
        return {
            "total_modules": 8,
            "total_assigned": 5000,
            "total_completed": 4460,
            "completion_rate": 89.2,
            "average_score": 82.5,
            "modules_by_completion": {
                "phishing_101": 95.2,
                "social_engineering": 88.4,
                "password_security": 92.1,
                "data_protection": 85.3,
                "incident_response": 78.9,
            }
        }
    
    def _collect_user_metrics(self) -> Dict:
        """Collect user-related metrics"""
        return {
            "total_users": 1250,
            "active_users": 1180,
            "high_risk_users": 45,
            "repeat_offenders": 12,
            "champions": 125,
            "average_risk_score": 42,
        }
    
    def _save_metrics(self, metrics: Dict):
        """Save metrics to file"""
        filename = f"{self.data_dir}/metrics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, "w") as f:
            json.dump(metrics, f, indent=2)
        logger.info(f"Metrics saved to {filename}")
    
    def generate_dashboard(self):
        """Generate and display metrics dashboard"""
        metrics = self.collect_metrics()
        
        # Header
        console.print(Panel.fit(
            "[bold orange1]🟠 ORANGE TEAM - Security Awareness Dashboard[/bold orange1]",
            subtitle=f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        ))
        
        # KPI Cards
        self._display_kpi_cards(metrics)
        
        # Trend Chart (ASCII)
        self._display_trend_chart()
        
        # Department Breakdown
        self._display_department_metrics()
        
        # High Risk Users
        self._display_high_risk_users()
        
        # Recommendations
        self._display_recommendations(metrics)
    
    def _display_kpi_cards(self, metrics: Dict):
        """Display KPI cards"""
        campaign = metrics.get("campaigns", {})
        training = metrics.get("training", {})
        users = metrics.get("users", {})
        
        kpis = [
            ("Click Rate", campaign.get("click_rate", 0), "%", "click_rate"),
            ("Report Rate", campaign.get("report_rate", 0), "%", "report_rate"),
            ("Training Completion", training.get("completion_rate", 0), "%", "training_completion"),
            ("High Risk Users", users.get("high_risk_users", 0), "", None),
        ]
        
        table = Table(show_header=False, box=None, padding=(0, 2))
        for _ in range(4):
            table.add_column()
        
        row = []
        for name, value, unit, metric_name in kpis:
            status, color = self._get_status(metric_name, value) if metric_name else ("normal", "cyan")
            
            # Create mini panel for each KPI
            panel_content = f"[bold]{name}[/bold]\n[{color}]{value}{unit}[/{color}]"
            row.append(Panel(panel_content, border_style=color))
        
        table.add_row(*row)
        console.print(table)
        console.print()
    
    def _display_trend_chart(self):
        """Display ASCII trend chart"""
        console.print("[bold]📈 Click Rate Trend (Last 12 Months)[/bold]\n")
        
        # Sample data
        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", 
                  "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        values = [22, 19, 17, 16, 15, 14, 13, 12, 11, 12, 12, 12.5]
        
        max_val = max(values)
        chart_height = 10
        
        for row in range(chart_height, 0, -1):
            threshold = (row / chart_height) * max_val
            line = f"{threshold:5.1f}% │"
            for val in values:
                if val >= threshold:
                    line += " ██"
                else:
                    line += "   "
            console.print(line)
        
        console.print("       └" + "───" * len(months))
        console.print("        " + "  ".join(months))
        console.print()
    
    def _display_department_metrics(self):
        """Display metrics by department"""
        console.print("[bold]📊 Department Performance[/bold]\n")
        
        departments = [
            DepartmentMetrics("Sales", 18.2, 45.0, 82.5, 65, 150),
            DepartmentMetrics("Marketing", 14.1, 52.0, 85.0, 58, 80),
            DepartmentMetrics("Finance", 11.3, 68.0, 91.2, 45, 120),
            DepartmentMetrics("Engineering", 7.2, 72.0, 88.5, 35, 200),
            DepartmentMetrics("IT", 4.1, 85.0, 95.0, 22, 50),
            DepartmentMetrics("Security", 1.2, 98.0, 100.0, 8, 25),
        ]
        
        table = Table(title="")
        table.add_column("Department", style="white")
        table.add_column("Click Rate", justify="right")
        table.add_column("Report Rate", justify="right")
        table.add_column("Training", justify="right")
        table.add_column("Risk Score", justify="right")
        table.add_column("Users", justify="right")
        
        for dept in departments:
            click_status, click_color = self._get_status("click_rate", dept.click_rate)
            report_status, report_color = self._get_status("report_rate", dept.report_rate)
            
            table.add_row(
                dept.name,
                f"[{click_color}]{dept.click_rate}%[/{click_color}]",
                f"[{report_color}]{dept.report_rate}%[/{report_color}]",
                f"{dept.training_completion}%",
                str(dept.risk_score),
                str(dept.user_count)
            )
        
        console.print(table)
        console.print()
    
    def _display_high_risk_users(self):
        """Display high risk users"""
        console.print("[bold]⚠️ High Risk Users (Top 5)[/bold]\n")
        
        high_risk = [
            {"email": "john.doe@company.com", "clicks": 5, "risk_score": 92, "dept": "Sales"},
            {"email": "jane.smith@company.com", "clicks": 4, "risk_score": 85, "dept": "Marketing"},
            {"email": "bob.wilson@company.com", "clicks": 4, "risk_score": 82, "dept": "Sales"},
            {"email": "alice.jones@company.com", "clicks": 3, "risk_score": 78, "dept": "Finance"},
            {"email": "charlie.brown@company.com", "clicks": 3, "risk_score": 75, "dept": "Marketing"},
        ]
        
        table = Table()
        table.add_column("Email", style="red")
        table.add_column("Clicks", justify="center")
        table.add_column("Risk Score", justify="center")
        table.add_column("Department")
        table.add_column("Action")
        
        for user in high_risk:
            table.add_row(
                user["email"],
                str(user["clicks"]),
                f"[red]{user['risk_score']}[/red]",
                user["dept"],
                "[yellow]Training Assigned[/yellow]"
            )
        
        console.print(table)
        console.print()
    
    def _display_recommendations(self, metrics: Dict):
        """Display AI-generated recommendations"""
        console.print("[bold]💡 Recommendations[/bold]\n")
        
        recommendations = self._generate_recommendations(metrics)
        
        for i, rec in enumerate(recommendations, 1):
            console.print(f"  {i}. {rec}")
        
        console.print()
    
    def _generate_recommendations(self, metrics: Dict) -> List[str]:
        """Generate recommendations based on metrics"""
        recommendations = []
        
        campaign = metrics.get("campaigns", {})
        training = metrics.get("training", {})
        
        # Click rate recommendations
        click_rate = campaign.get("click_rate", 0)
        if click_rate > 10:
            recommendations.append(
                f"[red]Click rate ({click_rate}%) is above target. "
                "Consider increasing training frequency for high-risk departments.[/red]"
            )
        
        # Report rate recommendations
        report_rate = campaign.get("report_rate", 0)
        if report_rate < 60:
            recommendations.append(
                f"[yellow]Report rate ({report_rate}%) is below target. "
                "Launch a campaign to promote the phishing report button.[/yellow]"
            )
        
        # Training recommendations
        completion_rate = training.get("completion_rate", 0)
        if completion_rate < 90:
            recommendations.append(
                f"[yellow]Training completion ({completion_rate}%) needs improvement. "
                "Send reminders to users with overdue training.[/yellow]"
            )
        
        # Department-specific
        recommendations.append(
            "[cyan]Sales department shows highest click rate. "
            "Consider targeted spear-phishing awareness training.[/cyan]"
        )
        
        # Positive reinforcement
        recommendations.append(
            "[green]Security team maintains excellent metrics. "
            "Consider them as mentors for other departments.[/green]"
        )
        
        return recommendations
    
    def generate_report(self, format: str = "console", output: str = None) -> str:
        """Generate metrics report"""
        metrics = self.collect_metrics()
        
        if format == "console":
            self.generate_dashboard()
            return "Dashboard displayed"
        
        elif format == "json":
            report = {
                "generated_at": datetime.now().isoformat(),
                "metrics": metrics,
                "recommendations": self._generate_recommendations(metrics)
            }
            
            if output:
                with open(output, "w") as f:
                    json.dump(report, f, indent=2)
                return f"Report saved to {output}"
            else:
                return json.dumps(report, indent=2)
        
        elif format == "markdown":
            report = self._generate_markdown_report(metrics)
            
            if output:
                with open(output, "w") as f:
                    f.write(report)
                return f"Report saved to {output}"
            else:
                return report
        
        return "Unknown format"
    
    def _generate_markdown_report(self, metrics: Dict) -> str:
        """Generate markdown report"""
        campaign = metrics.get("campaigns", {})
        training = metrics.get("training", {})
        users = metrics.get("users", {})
        
        report = f"""# 🟠 Orange Team - Security Awareness Report

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 📊 Executive Summary

| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| Click Rate | {campaign.get('click_rate', 0)}% | <5% | {'🟢' if campaign.get('click_rate', 0) < 5 else '🔴'} |
| Report Rate | {campaign.get('report_rate', 0)}% | >80% | {'🟢' if campaign.get('report_rate', 0) > 80 else '🔴'} |
| Training Completion | {training.get('completion_rate', 0)}% | >95% | {'🟢' if training.get('completion_rate', 0) > 95 else '🔴'} |
| High Risk Users | {users.get('high_risk_users', 0)} | <20 | {'🟢' if users.get('high_risk_users', 0) < 20 else '🔴'} |

## 📈 Campaign Statistics

- **Total Campaigns:** {campaign.get('total_campaigns', 0)}
- **Emails Sent:** {campaign.get('total_emails_sent', 0):,}
- **Emails Opened:** {campaign.get('total_opened', 0):,}
- **Links Clicked:** {campaign.get('total_clicked', 0):,}
- **Credentials Submitted:** {campaign.get('total_submitted', 0):,}
- **Phishing Reported:** {campaign.get('total_reported', 0):,}

## 📚 Training Statistics

- **Total Modules:** {training.get('total_modules', 0)}
- **Assigned:** {training.get('total_assigned', 0):,}
- **Completed:** {training.get('total_completed', 0):,}
- **Average Score:** {training.get('average_score', 0)}%

## 💡 Recommendations

"""
        for rec in self._generate_recommendations(metrics):
            # Strip rich formatting
            clean_rec = rec.replace("[red]", "").replace("[/red]", "")
            clean_rec = clean_rec.replace("[yellow]", "").replace("[/yellow]", "")
            clean_rec = clean_rec.replace("[green]", "").replace("[/green]", "")
            clean_rec = clean_rec.replace("[cyan]", "").replace("[/cyan]", "")
            report += f"- {clean_rec}\n"
        
        report += "\n---\n*Report generated by Orange Team Security Awareness Platform*"
        
        return report
    
    def calculate_risk_score(self, user_email: str) -> int:
        """Calculate risk score for a user"""
        # In production, this would query actual user data
        # For demo, returning sample calculation
        
        base_score = 50
        
        # Factors that increase risk
        # - Number of phishing clicks
        # - Time since last training
        # - Failed quiz attempts
        # - Department risk level
        
        # Factors that decrease risk
        # - Phishing reports
        # - Training completions
        # - Quiz scores
        # - Time without incidents
        
        return min(100, max(0, base_score))


def main():
    parser = argparse.ArgumentParser(
        description="🟠 Orange Team - Awareness Metrics Analyzer"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # Dashboard
    subparsers.add_parser("dashboard", help="Display metrics dashboard")
    
    # Report
    report_parser = subparsers.add_parser("report", help="Generate metrics report")
    report_parser.add_argument("--format", "-f", default="console",
                              choices=["console", "json", "markdown"])
    report_parser.add_argument("--output", "-o", help="Output file path")
    
    # Collect
    subparsers.add_parser("collect", help="Collect and save metrics")
    
    # Risk score
    risk_parser = subparsers.add_parser("risk", help="Calculate user risk score")
    risk_parser.add_argument("--email", "-e", required=True, help="User email")
    
    args = parser.parse_args()
    
    analyzer = AwarenessMetricsAnalyzer()
    
    if args.command == "dashboard":
        analyzer.generate_dashboard()
    
    elif args.command == "report":
        result = analyzer.generate_report(format=args.format, output=args.output)
        if args.format != "console":
            console.print(result)
    
    elif args.command == "collect":
        metrics = analyzer.collect_metrics()
        console.print("[green]✅ Metrics collected and saved[/green]")
    
    elif args.command == "risk":
        score = analyzer.calculate_risk_score(args.email)
        console.print(f"Risk score for {args.email}: {score}")
    
    else:
        # Default: show dashboard
        analyzer.generate_dashboard()


if __name__ == "__main__":
    main()
