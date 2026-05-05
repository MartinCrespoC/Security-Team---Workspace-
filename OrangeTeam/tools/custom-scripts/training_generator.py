#!/usr/bin/env python3
"""
🟠 ORANGE TEAM - Training Content Generator
Generación automática de material de capacitación en seguridad
"""

import os
import json
import argparse
from datetime import datetime
from typing import List, Dict
from dataclasses import dataclass, field
from enum import Enum
import logging

try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.progress import Progress, SpinnerColumn, TextColumn
except ImportError:
    os.system("pip install rich")
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.progress import Progress, SpinnerColumn, TextColumn

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
console = Console()


class Difficulty(Enum):
    BASIC = "basic"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


@dataclass
class QuizQuestion:
    question: str
    options: List[str]
    correct_answer: int
    explanation: str


@dataclass
class TrainingModule:
    id: str
    name: str
    description: str
    duration_minutes: int
    difficulty: Difficulty
    topics: List[str]
    learning_objectives: List[str]
    quiz_questions: List[QuizQuestion]
    passing_score: int = 80
    created_at: datetime = field(default_factory=datetime.now)


class TrainingContentGenerator:
    TOPICS = {
        "phishing": {"name": "Phishing Awareness", "duration": 30, "difficulty": Difficulty.BASIC},
        "social_engineering": {"name": "Social Engineering", "duration": 45, "difficulty": Difficulty.INTERMEDIATE},
        "password_security": {"name": "Password Security", "duration": 20, "difficulty": Difficulty.BASIC},
        "incident_response": {"name": "Incident Response", "duration": 60, "difficulty": Difficulty.ADVANCED},
        "ransomware": {"name": "Ransomware Prevention", "duration": 35, "difficulty": Difficulty.INTERMEDIATE},
    }
    
    def __init__(self):
        self.training_dir = "training/modules"
        os.makedirs(self.training_dir, exist_ok=True)
    
    def generate_module(self, topic: str, include_quiz: bool = True) -> TrainingModule:
        console.print(Panel.fit(f"[bold orange1]📚 Generating: {topic}[/bold orange1]"))
        
        template = self.TOPICS.get(topic.lower())
        if not template:
            console.print(f"[red]Unknown topic. Available: {list(self.TOPICS.keys())}[/red]")
            return None
        
        module = TrainingModule(
            id=f"{topic}_{datetime.now().strftime('%Y%m%d')}",
            name=template["name"],
            description=f"Training module for {template['name']}",
            duration_minutes=template["duration"],
            difficulty=template["difficulty"],
            topics=[f"Topic {i}" for i in range(1, 6)],
            learning_objectives=[f"Objective {i}" for i in range(1, 5)],
            quiz_questions=self._generate_quiz(topic) if include_quiz else []
        )
        
        self._save_module(module)
        self._display_summary(module)
        return module
    
    def _generate_quiz(self, topic: str) -> List[QuizQuestion]:
        return [QuizQuestion(
            question=f"Sample question about {topic}?",
            options=["Option A", "Option B", "Option C", "Option D"],
            correct_answer=1,
            explanation="This is the correct answer because..."
        )]
    
    def _save_module(self, module: TrainingModule):
        module_dir = f"{self.training_dir}/{module.id}"
        os.makedirs(module_dir, exist_ok=True)
        
        config = {"id": module.id, "name": module.name, "duration": module.duration_minutes}
        with open(f"{module_dir}/config.json", "w") as f:
            json.dump(config, f, indent=2)
        
        console.print(f"[green]✅ Saved to {module_dir}[/green]")
    
    def _display_summary(self, module: TrainingModule):
        console.print(Panel.fit(
            f"[bold green]✅ Module Generated[/bold green]\n\n"
            f"Name: {module.name}\n"
            f"Duration: {module.duration_minutes} min\n"
            f"Difficulty: {module.difficulty.value}\n"
            f"Quiz Questions: {len(module.quiz_questions)}"
        ))
    
    def list_modules(self):
        table = Table(title="📚 Available Training Modules")
        table.add_column("Topic", style="cyan")
        table.add_column("Name", style="white")
        table.add_column("Duration", style="yellow")
        table.add_column("Difficulty", style="green")
        
        for topic, info in self.TOPICS.items():
            table.add_row(topic, info["name"], f"{info['duration']} min", info["difficulty"].value)
        
        console.print(table)


def main():
    parser = argparse.ArgumentParser(description="🟠 Training Generator")
    subparsers = parser.add_subparsers(dest="command")
    
    gen_parser = subparsers.add_parser("generate", help="Generate module")
    gen_parser.add_argument("--topic", "-t", required=True)
    gen_parser.add_argument("--no-quiz", action="store_true")
    
    subparsers.add_parser("list", help="List available topics")
    
    args = parser.parse_args()
    generator = TrainingContentGenerator()
    
    if args.command == "generate":
        generator.generate_module(args.topic, not args.no_quiz)
    elif args.command == "list":
        generator.list_modules()
    else:
        generator.list_modules()


if __name__ == "__main__":
    main()
