---
name: Training Designer
description: AI skill for designing security awareness training
triggers:
  - crear training
  - generate training
  - new module
  - design course
---

# 📚 Training Designer Skill

## Capabilities

This skill creates comprehensive security awareness training:

1. **Module Generation**: Create complete training modules
2. **Quiz Creation**: Generate assessment questions
3. **Learning Paths**: Design personalized training paths
4. **Content Adaptation**: Adjust difficulty and focus

## Available Topics

| Topic | Duration | Level |
|-------|----------|-------|
| Phishing | 30 min | Basic |
| Social Engineering | 45 min | Intermediate |
| Password Security | 20 min | Basic |
| Data Protection | 40 min | Intermediate |
| Incident Response | 60 min | Advanced |
| Ransomware | 35 min | Intermediate |
| Mobile Security | 25 min | Basic |
| Remote Work | 35 min | Intermediate |

## Module Structure

```
Module
├── Overview
├── Learning Objectives
├── Content Sections
│   ├── Theory
│   ├── Examples
│   ├── Interactive Exercises
│   └── Real-world Scenarios
├── Quiz
└── Summary
```

## Usage

```python
from tools.custom_scripts.training_generator import TrainingContentGenerator

generator = TrainingContentGenerator()
module = generator.generate_module(
    topic="phishing",
    include_quiz=True
)
```

## Response Format

```
📚 **Módulo de Training Generado**

- **Nombre:** {name}
- **Duración:** {duration} minutos
- **Dificultad:** {difficulty}
- **Preguntas de Quiz:** {quiz_count}

✅ Contenido generado
✅ Quiz incluido
✅ Guardado en training/modules/
```

## Personalization

- Role-based content
- Department-specific examples
- Difficulty adaptation
- Language localization
