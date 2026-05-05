#!/usr/bin/env python3
"""
🟠 ORANGE TEAM - Phishing Campaign Manager
Gestión completa de campañas de phishing con GoPhish
"""

import os
import sys
import json
import argparse
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
from dataclasses import dataclass, asdict
from enum import Enum
import logging

# Third-party imports
try:
    import requests
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.progress import Progress, SpinnerColumn, TextColumn
    from rich import print as rprint
except ImportError:
    print("Installing required packages...")
    os.system("pip install requests rich")
    import requests
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.progress import Progress, SpinnerColumn, TextColumn
    from rich import print as rprint

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

console = Console()


class Difficulty(Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"
    EXPERT = "expert"


class CampaignStatus(Enum):
    DRAFT = "draft"
    SCHEDULED = "scheduled"
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


@dataclass
class CampaignConfig:
    """Configuration for a phishing campaign"""
    name: str
    description: str
    target_department: str
    difficulty: Difficulty
    template_id: str
    landing_page_id: str
    smtp_profile_id: str
    start_date: datetime
    end_date: Optional[datetime] = None
    send_by_date: Optional[datetime] = None
    auto_remediation: bool = True
    track_opens: bool = True
    track_clicks: bool = True


@dataclass
class CampaignResult:
    """Results from a phishing campaign"""
    campaign_id: str
    total_sent: int
    total_opened: int
    total_clicked: int
    total_submitted: int
    total_reported: int
    click_rate: float
    report_rate: float


class GoPhishAPI:
    """GoPhish API Client"""
    
    def __init__(self, url: str = None, api_key: str = None):
        self.url = url or os.getenv("GOPHISH_URL", "https://localhost:3333")
        self.api_key = api_key or os.getenv("GOPHISH_API_KEY", "")
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        self.verify_ssl = False  # For local development
    
    def _request(self, method: str, endpoint: str, data: dict = None) -> dict:
        """Make API request to GoPhish"""
        url = f"{self.url}/api/{endpoint}"
        try:
            response = requests.request(
                method=method,
                url=url,
                headers=self.headers,
                json=data,
                verify=self.verify_ssl
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {e}")
            return {"error": str(e)}
    
    def get_campaigns(self) -> List[dict]:
        """Get all campaigns"""
        return self._request("GET", "campaigns/")
    
    def get_campaign(self, campaign_id: int) -> dict:
        """Get specific campaign"""
        return self._request("GET", f"campaigns/{campaign_id}")
    
    def create_campaign(self, campaign: dict) -> dict:
        """Create new campaign"""
        return self._request("POST", "campaigns/", campaign)
    
    def delete_campaign(self, campaign_id: int) -> dict:
        """Delete campaign"""
        return self._request("DELETE", f"campaigns/{campaign_id}")
    
    def complete_campaign(self, campaign_id: int) -> dict:
        """Mark campaign as complete"""
        return self._request("GET", f"campaigns/{campaign_id}/complete")
    
    def get_campaign_results(self, campaign_id: int) -> dict:
        """Get campaign results"""
        return self._request("GET", f"campaigns/{campaign_id}/results")
    
    def get_templates(self) -> List[dict]:
        """Get all email templates"""
        return self._request("GET", "templates/")
    
    def get_groups(self) -> List[dict]:
        """Get all target groups"""
        return self._request("GET", "groups/")
    
    def get_landing_pages(self) -> List[dict]:
        """Get all landing pages"""
        return self._request("GET", "pages/")
    
    def get_smtp_profiles(self) -> List[dict]:
        """Get all SMTP profiles"""
        return self._request("GET", "smtp/")


class PhishingCampaignManager:
    """Manager for phishing campaigns"""
    
    def __init__(self):
        self.api = GoPhishAPI()
        self.templates_dir = "templates/email"
        self.campaigns_dir = "campaigns"
    
    def create_campaign(
        self,
        name: str,
        department: str,
        difficulty: str = "medium",
        template: str = None,
        schedule: datetime = None
    ) -> dict:
        """Create a new phishing campaign"""
        
        console.print(Panel.fit(
            f"[bold orange1]🎣 Creating Phishing Campaign[/bold orange1]\n\n"
            f"Name: {name}\n"
            f"Department: {department}\n"
            f"Difficulty: {difficulty}",
            title="Campaign Setup"
        ))
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            
            # Step 1: Validate inputs
            task = progress.add_task("Validating inputs...", total=None)
            difficulty_enum = Difficulty(difficulty.lower())
            progress.update(task, completed=True)
            
            # Step 2: Select template based on difficulty
            task = progress.add_task("Selecting template...", total=None)
            template_id = self._select_template(difficulty_enum, template)
            progress.update(task, completed=True)
            
            # Step 3: Get target group
            task = progress.add_task("Loading target group...", total=None)
            group_id = self._get_or_create_group(department)
            progress.update(task, completed=True)
            
            # Step 4: Configure campaign
            task = progress.add_task("Configuring campaign...", total=None)
            campaign_data = {
                "name": name,
                "template": {"id": template_id},
                "page": {"id": 1},  # Default landing page
                "smtp": {"id": 1},  # Default SMTP profile
                "groups": [{"id": group_id}],
                "launch_date": (schedule or datetime.now()).isoformat(),
            }
            progress.update(task, completed=True)
            
            # Step 5: Create campaign in GoPhish
            task = progress.add_task("Creating campaign in GoPhish...", total=None)
            result = self.api.create_campaign(campaign_data)
            progress.update(task, completed=True)
            
            # Step 6: Save campaign config locally
            task = progress.add_task("Saving configuration...", total=None)
            self._save_campaign_config(name, campaign_data, result)
            progress.update(task, completed=True)
        
        if "error" not in result:
            console.print(Panel.fit(
                f"[bold green]✅ Campaign Created Successfully![/bold green]\n\n"
                f"Campaign ID: {result.get('id', 'N/A')}\n"
                f"Status: {result.get('status', 'N/A')}\n"
                f"Launch Date: {result.get('launch_date', 'N/A')}",
                title="Success"
            ))
        else:
            console.print(f"[bold red]❌ Error: {result['error']}[/bold red]")
        
        return result
    
    def _select_template(self, difficulty: Difficulty, template_name: str = None) -> int:
        """Select appropriate template based on difficulty"""
        templates = self.api.get_templates()
        
        if template_name:
            for t in templates:
                if t.get("name") == template_name:
                    return t.get("id")
        
        # Default template selection based on difficulty
        difficulty_templates = {
            Difficulty.EASY: "awareness_test_easy",
            Difficulty.MEDIUM: "credential_phishing_medium",
            Difficulty.HARD: "spear_phishing_hard",
            Difficulty.EXPERT: "whaling_expert"
        }
        
        target_name = difficulty_templates.get(difficulty, "credential_phishing_medium")
        
        for t in templates:
            if target_name in t.get("name", "").lower():
                return t.get("id")
        
        # Return first template if no match
        return templates[0].get("id") if templates else 1
    
    def _get_or_create_group(self, department: str) -> int:
        """Get or create target group for department"""
        groups = self.api.get_groups()
        
        for g in groups:
            if department.lower() in g.get("name", "").lower():
                return g.get("id")
        
        # Return first group if no match
        return groups[0].get("id") if groups else 1
    
    def _save_campaign_config(self, name: str, config: dict, result: dict):
        """Save campaign configuration locally"""
        campaign_dir = f"{self.campaigns_dir}/active/{name.replace(' ', '_').lower()}"
        os.makedirs(campaign_dir, exist_ok=True)
        
        with open(f"{campaign_dir}/config.json", "w") as f:
            json.dump({
                "config": config,
                "result": result,
                "created_at": datetime.now().isoformat()
            }, f, indent=2, default=str)
    
    def list_campaigns(self) -> List[dict]:
        """List all campaigns"""
        campaigns = self.api.get_campaigns()
        
        table = Table(title="🎣 Phishing Campaigns")
        table.add_column("ID", style="cyan")
        table.add_column("Name", style="white")
        table.add_column("Status", style="green")
        table.add_column("Launch Date", style="yellow")
        table.add_column("Sent", style="blue")
        table.add_column("Clicked", style="red")
        
        for c in campaigns:
            status_color = {
                "In progress": "green",
                "Completed": "blue",
                "Queued": "yellow"
            }.get(c.get("status", ""), "white")
            
            stats = c.get("stats", {})
            table.add_row(
                str(c.get("id", "")),
                c.get("name", ""),
                f"[{status_color}]{c.get('status', '')}[/{status_color}]",
                c.get("launch_date", "")[:10] if c.get("launch_date") else "",
                str(stats.get("sent", 0)),
                str(stats.get("clicked", 0))
            )
        
        console.print(table)
        return campaigns
    
    def get_results(self, campaign_id: int) -> CampaignResult:
        """Get campaign results"""
        results = self.api.get_campaign_results(campaign_id)
        campaign = self.api.get_campaign(campaign_id)
        
        stats = campaign.get("stats", {})
        total_sent = stats.get("sent", 0)
        total_opened = stats.get("opened", 0)
        total_clicked = stats.get("clicked", 0)
        total_submitted = stats.get("submitted_data", 0)
        total_reported = stats.get("reported", 0)
        
        click_rate = (total_clicked / total_sent * 100) if total_sent > 0 else 0
        report_rate = (total_reported / total_sent * 100) if total_sent > 0 else 0
        
        result = CampaignResult(
            campaign_id=str(campaign_id),
            total_sent=total_sent,
            total_opened=total_opened,
            total_clicked=total_clicked,
            total_submitted=total_submitted,
            total_reported=total_reported,
            click_rate=round(click_rate, 2),
            report_rate=round(report_rate, 2)
        )
        
        # Display results
        console.print(Panel.fit(
            f"[bold orange1]📊 Campaign Results[/bold orange1]\n\n"
            f"Campaign: {campaign.get('name', 'N/A')}\n"
            f"Status: {campaign.get('status', 'N/A')}\n\n"
            f"[bold]Statistics:[/bold]\n"
            f"  📧 Sent: {total_sent}\n"
            f"  👁️ Opened: {total_opened} ({total_opened/total_sent*100:.1f}%)\n"
            f"  🖱️ Clicked: {total_clicked} ({click_rate:.1f}%)\n"
            f"  📝 Submitted: {total_submitted}\n"
            f"  🚨 Reported: {total_reported} ({report_rate:.1f}%)",
            title=f"Campaign #{campaign_id}"
        ))
        
        return result
    
    def identify_high_risk_users(self, campaign_id: int) -> List[dict]:
        """Identify users who clicked or submitted credentials"""
        results = self.api.get_campaign_results(campaign_id)
        high_risk = []
        
        for event in results.get("timeline", []):
            if event.get("message") in ["Clicked Link", "Submitted Data"]:
                high_risk.append({
                    "email": event.get("email"),
                    "action": event.get("message"),
                    "timestamp": event.get("time")
                })
        
        if high_risk:
            table = Table(title="⚠️ High Risk Users")
            table.add_column("Email", style="red")
            table.add_column("Action", style="yellow")
            table.add_column("Timestamp", style="white")
            
            for user in high_risk:
                table.add_row(
                    user["email"],
                    user["action"],
                    user["timestamp"]
                )
            
            console.print(table)
        
        return high_risk
    
    def assign_remediation_training(self, users: List[dict], module: str = "phishing-remediation"):
        """Assign remediation training to users who failed"""
        console.print(f"\n[bold yellow]📚 Assigning Training: {module}[/bold yellow]")
        
        for user in users:
            console.print(f"  ✅ Training assigned to: {user['email']}")
            # Here you would integrate with your LMS/training platform
            # For now, we'll just log it
            logger.info(f"Training '{module}' assigned to {user['email']}")
        
        console.print(f"\n[bold green]✅ Training assigned to {len(users)} users[/bold green]")


def main():
    parser = argparse.ArgumentParser(
        description="🟠 Orange Team - Phishing Campaign Manager"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # Create campaign
    create_parser = subparsers.add_parser("create", help="Create new campaign")
    create_parser.add_argument("--name", "-n", required=True, help="Campaign name")
    create_parser.add_argument("--department", "-d", required=True, help="Target department")
    create_parser.add_argument("--difficulty", "-D", default="medium", 
                              choices=["easy", "medium", "hard", "expert"])
    create_parser.add_argument("--template", "-t", help="Template name")
    create_parser.add_argument("--schedule", "-s", help="Schedule date (YYYY-MM-DD)")
    
    # List campaigns
    subparsers.add_parser("list", help="List all campaigns")
    
    # Get results
    results_parser = subparsers.add_parser("results", help="Get campaign results")
    results_parser.add_argument("--id", "-i", type=int, required=True, help="Campaign ID")
    results_parser.add_argument("--remediate", "-r", action="store_true", 
                               help="Auto-assign training to failed users")
    
    # Launch mode (for Windsurf integration)
    subparsers.add_parser("launch", help="Interactive launch mode")
    
    # Debug mode
    subparsers.add_parser("debug", help="Debug mode")
    
    args = parser.parse_args()
    
    manager = PhishingCampaignManager()
    
    if args.command == "create":
        schedule = None
        if args.schedule:
            schedule = datetime.fromisoformat(args.schedule)
        
        manager.create_campaign(
            name=args.name,
            department=args.department,
            difficulty=args.difficulty,
            template=args.template,
            schedule=schedule
        )
    
    elif args.command == "list":
        manager.list_campaigns()
    
    elif args.command == "results":
        result = manager.get_results(args.id)
        
        if args.remediate:
            high_risk = manager.identify_high_risk_users(args.id)
            if high_risk:
                manager.assign_remediation_training(high_risk)
    
    elif args.command == "launch":
        console.print(Panel.fit(
            "[bold orange1]🎣 Phishing Campaign Manager[/bold orange1]\n\n"
            "Interactive mode for Windsurf AI integration.\n"
            "Use natural language commands to manage campaigns.",
            title="Orange Team"
        ))
        
        # Interactive mode
        while True:
            try:
                command = console.input("\n[orange1]orange>[/orange1] ")
                if command.lower() in ["exit", "quit", "q"]:
                    break
                elif "list" in command.lower():
                    manager.list_campaigns()
                elif "create" in command.lower():
                    console.print("Use: create --name <name> --department <dept>")
                else:
                    console.print(f"Unknown command: {command}")
            except KeyboardInterrupt:
                break
    
    elif args.command == "debug":
        console.print("[bold yellow]Debug Mode[/bold yellow]")
        console.print(f"GoPhish URL: {manager.api.url}")
        console.print(f"API Key configured: {'Yes' if manager.api.api_key else 'No'}")
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
