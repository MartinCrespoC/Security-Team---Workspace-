# 🟠 ORANGE TEAM - Memoria de Construcción

## 📋 Documento de Arquitectura y Construcción Detallada

---

## 🎯 Resumen Ejecutivo

Este documento detalla la construcción completa del workspace **ORANGE TEAM - Security Awareness Platform**, una solución integral para capacitación y concientización en seguridad informática, integrada con Windsurf AI para automatización inteligente.

---

## 📐 Arquitectura del Sistema

### 🏗️ Diagrama de Alto Nivel

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                           ORANGE TEAM ARCHITECTURE v2.0                             │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                     │
│  ┌─────────────────────────────────────────────────────────────────────────────┐   │
│  │                            PRESENTATION LAYER                               │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │   │
│  │  │   Windsurf   │  │   Web UI     │  │   CLI        │  │   API        │    │   │
│  │  │   Interface  │  │   Dashboard  │  │   Tools      │  │   Gateway    │    │   │
│  │  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘    │   │
│  └─────────────────────────────────────────────────────────────────────────────┘   │
│                                        │                                            │
│  ┌─────────────────────────────────────▼───────────────────────────────────────┐   │
│  │                            ORCHESTRATION LAYER                              │   │
│  │                                                                             │   │
│  │  ┌─────────────────────────────────────────────────────────────────────┐   │   │
│  │  │                      🤖 WINDSURF AI ENGINE                          │   │   │
│  │  │                                                                     │   │   │
│  │  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌───────────┐  │   │   │
│  │  │  │ NLP Parser  │  │ Campaign    │  │ Training    │  │ Analytics │  │   │   │
│  │  │  │             │  │ Generator   │  │ Generator   │  │ Engine    │  │   │   │
│  │  │  └─────────────┘  └─────────────┘  └─────────────┘  └───────────┘  │   │   │
│  │  │                                                                     │   │   │
│  │  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌───────────┐  │   │   │
│  │  │  │ Workflow    │  │ Skill       │  │ Memory      │  │ Decision  │  │   │   │
│  │  │  │ Engine      │  │ Executor    │  │ Manager     │  │ Engine    │  │   │   │
│  │  │  └─────────────┘  └─────────────┘  └─────────────┘  └───────────┘  │   │   │
│  │  └─────────────────────────────────────────────────────────────────────┘   │   │
│  │                                                                             │   │
│  └─────────────────────────────────────────────────────────────────────────────┘   │
│                                        │                                            │
│  ┌─────────────────────────────────────▼───────────────────────────────────────┐   │
│  │                              SERVICE LAYER                                  │   │
│  │                                                                             │   │
│  │  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐  ┌─────────────┐  │   │
│  │  │   PHISHING    │  │   TRAINING    │  │   METRICS     │  │  GAMIFY     │  │   │
│  │  │   SERVICE     │  │   SERVICE     │  │   SERVICE     │  │  SERVICE    │  │   │
│  │  │               │  │               │  │               │  │             │  │   │
│  │  │ • Campaigns   │  │ • Modules     │  │ • Collection  │  │ • Points    │  │   │
│  │  │ • Templates   │  │ • Quizzes     │  │ • Analysis    │  │ • Badges    │  │   │
│  │  │ • Tracking    │  │ • Paths       │  │ • Reporting   │  │ • Rewards   │  │   │
│  │  │ • Results     │  │ • Certs       │  │ • Alerts      │  │ • Leaders   │  │   │
│  │  └───────────────┘  └───────────────┘  └───────────────┘  └─────────────┘  │   │
│  │                                                                             │   │
│  └─────────────────────────────────────────────────────────────────────────────┘   │
│                                        │                                            │
│  ┌─────────────────────────────────────▼───────────────────────────────────────┐   │
│  │                            INTEGRATION LAYER                                │   │
│  │                                                                             │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────────┐    │   │
│  │  │   GoPhish   │  │ King Phisher│  │  Evilginx2  │  │      SET        │    │   │
│  │  │   Engine    │  │   Engine    │  │    Proxy    │  │    Toolkit      │    │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────────┘    │   │
│  │                                                                             │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────────┐    │   │
│  │  │    BeEF     │  │   SMTP      │  │   LDAP/AD   │  │    SIEM         │    │   │
│  │  │  Framework  │  │   Relay     │  │   Connector │  │   Connector     │    │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────────┘    │   │
│  │                                                                             │   │
│  └─────────────────────────────────────────────────────────────────────────────┘   │
│                                        │                                            │
│  ┌─────────────────────────────────────▼───────────────────────────────────────┐   │
│  │                               DATA LAYER                                    │   │
│  │                                                                             │   │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────────────────┐ │   │
│  │  │   PostgreSQL    │  │  Elasticsearch  │  │        Redis Cache          │ │   │
│  │  │   (Primary DB)  │  │  (Metrics/Logs) │  │     (Session/Queue)         │ │   │
│  │  └─────────────────┘  └─────────────────┘  └─────────────────────────────┘ │   │
│  │                                                                             │   │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────────────────┐ │   │
│  │  │   File Storage  │  │   S3/MinIO      │  │      Backup Storage         │ │   │
│  │  │   (Templates)   │  │   (Media)       │  │       (Archives)            │ │   │
│  │  └─────────────────┘  └─────────────────┘  └─────────────────────────────┘ │   │
│  │                                                                             │   │
│  └─────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                     │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 🔧 Componentes Detallados

### 1. 📁 Estructura de Directorios

```
OrangeTeam-Windsurf/
│
├── 📄 ARCHIVOS RAÍZ
│   ├── OrangeTeam.code-workspace     # Configuración VS Code/Windsurf
│   │   ├── Colores: Orange theme (#FF6B00)
│   │   ├── Extensiones recomendadas
│   │   ├── Tasks predefinidas
│   │   └── Launch configurations
│   │
│   ├── README.md                      # Documentación principal
│   │   ├── ASCII Art banner
│   │   ├── Badges de estado
│   │   ├── Diagramas Mermaid
│   │   └── Guías de uso
│   │
│   ├── memoria.md                     # Este documento
│   │
│   ├── install.sh                     # Instalador automatizado
│   │   ├── Verificación de dependencias
│   │   ├── Instalación de herramientas
│   │   ├── Configuración de Docker
│   │   └── Setup inicial
│   │
│   ├── .windsurfrules                 # Reglas de automatización AI
│   │   ├── Triggers automáticos
│   │   ├── Respuestas predefinidas
│   │   └── Workflows integrados
│   │
│   ├── requirements.txt               # Dependencias Python
│   └── docker-compose.yml             # Orquestación de servicios
│
├── 📁 campaigns/                      # GESTIÓN DE CAMPAÑAS
│   │
│   ├── active/                        # Campañas en ejecución
│   │   └── {campaign_id}/
│   │       ├── config.yaml            # Configuración
│   │       ├── targets.csv            # Lista de objetivos
│   │       ├── template.html          # Template usado
│   │       ├── results.json           # Resultados en tiempo real
│   │       └── logs/                  # Logs de la campaña
│   │
│   ├── completed/                     # Campañas finalizadas
│   │   └── {campaign_id}/
│   │       ├── final_report.pdf       # Reporte final
│   │       ├── metrics.json           # Métricas finales
│   │       └── archive/               # Datos archivados
│   │
│   ├── scheduled/                     # Campañas programadas
│   │   └── {campaign_id}/
│   │       ├── schedule.yaml          # Programación
│   │       └── config.yaml            # Configuración
│   │
│   └── campaign_config.yaml           # Configuración global
│       ├── default_settings
│       ├── smtp_profiles
│       ├── landing_pages
│       └── tracking_options
│
├── 📁 training/                       # MATERIAL DE CAPACITACIÓN
│   │
│   ├── modules/                       # Módulos de entrenamiento
│   │   ├── phishing-101/
│   │   │   ├── content.md             # Contenido del módulo
│   │   │   ├── slides.pptx            # Presentación
│   │   │   ├── quiz.yaml              # Evaluación
│   │   │   └── resources/             # Recursos adicionales
│   │   │
│   │   ├── social-engineering/
│   │   ├── password-security/
│   │   ├── data-protection/
│   │   ├── incident-response/
│   │   ├── mobile-security/
│   │   ├── remote-work/
│   │   └── insider-threats/
│   │
│   ├── videos/                        # Videos educativos
│   │   ├── awareness/
│   │   ├── tutorials/
│   │   └── simulations/
│   │
│   ├── slides/                        # Presentaciones
│   │   ├── executive/
│   │   ├── technical/
│   │   └── general/
│   │
│   └── interactive/                   # Contenido interactivo
│       ├── simulations/
│       ├── games/
│       └── scenarios/
│
├── 📁 metrics/                        # MÉTRICAS Y REPORTES
│   │
│   ├── dashboard/                     # Dashboard web
│   │   ├── index.html                 # Página principal
│   │   ├── css/                       # Estilos
│   │   ├── js/                        # Scripts
│   │   └── components/                # Componentes
│   │
│   ├── reports/                       # Reportes generados
│   │   ├── daily/
│   │   ├── weekly/
│   │   ├── monthly/
│   │   └── quarterly/
│   │
│   ├── data/                          # Datos históricos
│   │   ├── campaigns/
│   │   ├── users/
│   │   └── trends/
│   │
│   └── metrics_config.yaml            # Configuración
│       ├── kpis
│       ├── thresholds
│       ├── alerts
│       └── reporting_schedule
│
├── 📁 templates/                      # TEMPLATES DE PHISHING
│   │
│   ├── email/                         # Templates de correo
│   │   ├── credential/                # Robo de credenciales
│   │   │   ├── office365.html
│   │   │   ├── google.html
│   │   │   ├── linkedin.html
│   │   │   └── custom/
│   │   │
│   │   ├── malware/                   # Entrega de malware
│   │   │   ├── invoice.html
│   │   │   ├── document.html
│   │   │   └── update.html
│   │   │
│   │   ├── bec/                       # Business Email Compromise
│   │   │   ├── ceo_fraud.html
│   │   │   ├── wire_transfer.html
│   │   │   └── vendor_change.html
│   │   │
│   │   └── awareness/                 # Templates de awareness
│   │       ├── test_easy.html
│   │       ├── test_medium.html
│   │       └── test_hard.html
│   │
│   ├── landing/                       # Landing pages
│   │   ├── login_pages/
│   │   ├── download_pages/
│   │   └── awareness_pages/
│   │
│   ├── sms/                           # Templates SMS
│   │   ├── delivery.txt
│   │   ├── bank_alert.txt
│   │   └── verification.txt
│   │
│   └── qr/                            # Templates QR
│       ├── wifi.json
│       ├── payment.json
│       └── survey.json
│
├── 📁 quizzes/                        # EVALUACIONES
│   │
│   ├── questions/                     # Banco de preguntas
│   │   ├── phishing.yaml
│   │   ├── social_engineering.yaml
│   │   ├── passwords.yaml
│   │   ├── data_protection.yaml
│   │   └── incident_response.yaml
│   │
│   ├── assessments/                   # Evaluaciones completas
│   │   ├── baseline.yaml              # Evaluación inicial
│   │   ├── quarterly.yaml             # Evaluación trimestral
│   │   ├── annual.yaml                # Evaluación anual
│   │   └── remediation.yaml           # Post-incidente
│   │
│   └── quiz_config.yaml               # Configuración
│       ├── passing_score
│       ├── time_limits
│       ├── retry_policy
│       └── certificate_settings
│
├── 📁 tools/                          # HERRAMIENTAS
│   │
│   ├── custom-scripts/                # Scripts personalizados
│   │   │
│   │   ├── phishing_campaign.py       # Gestión de campañas
│   │   │   ├── create_campaign()
│   │   │   ├── launch_campaign()
│   │   │   ├── track_results()
│   │   │   ├── generate_report()
│   │   │   └── auto_remediate()
│   │   │
│   │   ├── awareness_metrics.py       # Métricas y analytics
│   │   │   ├── collect_metrics()
│   │   │   ├── analyze_trends()
│   │   │   ├── generate_dashboard()
│   │   │   ├── risk_scoring()
│   │   │   └── export_report()
│   │   │
│   │   ├── training_generator.py      # Generador de training
│   │   │   ├── generate_module()
│   │   │   ├── create_quiz()
│   │   │   ├── personalize_path()
│   │   │   ├── assign_training()
│   │   │   └── track_completion()
│   │   │
│   │   └── social_eng_test.sh         # Tests de ingeniería social
│   │       ├── vishing_test()
│   │       ├── pretexting_test()
│   │       ├── tailgating_test()
│   │       └── report_results()
│   │
│   └── integrations/                  # Integraciones externas
│       ├── gophish_api.py
│       ├── ldap_connector.py
│       ├── siem_connector.py
│       └── slack_notifier.py
│
├── 📁 docker/                         # CONFIGURACIONES DOCKER
│   │
│   ├── gophish/
│   │   ├── Dockerfile
│   │   ├── docker-compose.yml
│   │   └── config.json
│   │
│   ├── kingphisher/
│   │   ├── Dockerfile
│   │   └── docker-compose.yml
│   │
│   ├── beef/
│   │   ├── Dockerfile
│   │   └── docker-compose.yml
│   │
│   └── elk/                           # Elasticsearch + Kibana
│       └── docker-compose.yml
│
├── 📁 .windsurf/                      # CONFIGURACIÓN WINDSURF
│   │
│   ├── workflows/                     # Workflows automatizados
│   │   ├── phishing.md                # /phishing
│   │   ├── training.md                # /training
│   │   ├── metrics.md                 # /metrics
│   │   ├── campaign.md                # /campaign
│   │   └── quiz.md                    # /quiz
│   │
│   └── skills/                        # Skills de AI
│       ├── campaign_creator.md
│       ├── metrics_analyzer.md
│       ├── training_designer.md
│       ├── report_generator.md
│       └── purple_team_integrator.md
│
└── 📁 docs/                           # DOCUMENTACIÓN
    ├── API.md                         # Documentación de API
    ├── CONTRIBUTING.md                # Guía de contribución
    ├── SECURITY.md                    # Políticas de seguridad
    └── CHANGELOG.md                   # Historial de cambios
```

---

## 🔄 Flujos de Trabajo

### 1. 🎣 Flujo de Campaña de Phishing

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        PHISHING CAMPAIGN WORKFLOW                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐  │
│  │  PLAN   │───▶│ CREATE  │───▶│ LAUNCH  │───▶│ TRACK   │───▶│ REPORT  │  │
│  └────┬────┘    └────┬────┘    └────┬────┘    └────┬────┘    └────┬────┘  │
│       │              │              │              │              │        │
│       ▼              ▼              ▼              ▼              ▼        │
│  ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐  │
│  │• Target │    │• Select │    │• Send   │    │• Opens  │    │• Stats  │  │
│  │  groups │    │  template│    │  emails │    │• Clicks │    │• Trends │  │
│  │• Goals  │    │• Config │    │• Track  │    │• Submits│    │• Risks  │  │
│  │• Timeline│   │  SMTP   │    │  pixels │    │• Reports│    │• Actions│  │
│  └─────────┘    └─────────┘    └─────────┘    └─────────┘    └─────────┘  │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                         AUTO-REMEDIATION                            │   │
│  │                                                                     │   │
│  │   User Clicked? ──▶ Assign Training ──▶ Track Completion ──▶ Retest │   │
│  │                                                                     │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2. 📚 Flujo de Training

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          TRAINING WORKFLOW                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌───────────────────────────────────────────────────────────────────────┐ │
│  │                        TRAINING PATH                                  │ │
│  │                                                                       │ │
│  │  ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐           │ │
│  │  │ ASSESS  │───▶│ ASSIGN  │───▶│ LEARN   │───▶│ VERIFY  │           │ │
│  │  │ Baseline│    │ Modules │    │ Content │    │ Quiz    │           │ │
│  │  └─────────┘    └─────────┘    └─────────┘    └─────────┘           │ │
│  │       │              │              │              │                 │ │
│  │       │              │              │              ▼                 │ │
│  │       │              │              │         ┌─────────┐           │ │
│  │       │              │              │         │ PASSED? │           │ │
│  │       │              │              │         └────┬────┘           │ │
│  │       │              │              │              │                 │ │
│  │       │              │              │    ┌─────────┴─────────┐      │ │
│  │       │              │              │    │                   │      │ │
│  │       │              │              │    ▼                   ▼      │ │
│  │       │              │              │ ┌─────┐           ┌─────────┐ │ │
│  │       │              │              │ │ YES │           │   NO    │ │ │
│  │       │              │              │ └──┬──┘           └────┬────┘ │ │
│  │       │              │              │    │                   │      │ │
│  │       │              │              │    ▼                   ▼      │ │
│  │       │              │              │ ┌─────────┐     ┌───────────┐ │ │
│  │       │              │              │ │CERTIFY  │     │ REMEDIATE │ │ │
│  │       │              │              │ │+ Points │     │ + Retry   │ │ │
│  │       │              │              │ └─────────┘     └───────────┘ │ │
│  │                                                                       │ │
│  └───────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 3. 📊 Flujo de Métricas

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          METRICS WORKFLOW                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  DATA SOURCES                    PROCESSING                    OUTPUT       │
│  ┌─────────────┐                ┌─────────────┐            ┌─────────────┐ │
│  │  Campaigns  │───┐            │             │            │  Dashboard  │ │
│  └─────────────┘   │            │             │        ┌──▶│  Real-time  │ │
│  ┌─────────────┐   │            │   METRICS   │        │   └─────────────┘ │
│  │  Training   │───┼───────────▶│   ENGINE    │────────┤   ┌─────────────┐ │
│  └─────────────┘   │            │             │        ├──▶│   Reports   │ │
│  ┌─────────────┐   │            │  • Collect  │        │   │   PDF/CSV   │ │
│  │   Quizzes   │───┤            │  • Analyze  │        │   └─────────────┘ │
│  └─────────────┘   │            │  • Score    │        │   ┌─────────────┐ │
│  ┌─────────────┐   │            │  • Alert    │        └──▶│   Alerts    │ │
│  │   Reports   │───┘            │             │            │  Slack/Email│ │
│  └─────────────┘                └─────────────┘            └─────────────┘ │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                         KEY METRICS                                 │   │
│  │                                                                     │   │
│  │  • Click Rate (target: <5%)        • Training Completion (>95%)    │   │
│  │  • Report Rate (target: >80%)      • Quiz Pass Rate (>85%)         │   │
│  │  • Credential Submit (<2%)         • Time to Report (<5 min)       │   │
│  │  • Repeat Offenders (<3%)          • Security Score (>85)          │   │
│  │                                                                     │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 🤖 Integración Windsurf AI

### Configuración de .windsurfrules

```yaml
# Reglas de automatización para Orange Team

triggers:
  # Trigger: Crear campaña de phishing
  - pattern: "crear campaña|new campaign|phishing campaign"
    action: execute_workflow
    workflow: phishing
    auto_execute: true
    
  # Trigger: Resultados de campaña
  - pattern: "resultados|results|métricas de campaña"
    action: generate_metrics
    auto_report: true
    
  # Trigger: Usuario cayó en phishing
  - pattern: "usuario cayó|user clicked|failed phishing"
    action: assign_training
    training_module: phishing-remediation
    notify: true
    
  # Trigger: Generar training
  - pattern: "generar training|create training|nuevo módulo"
    action: execute_workflow
    workflow: training
    
responses:
  campaign_created:
    message: "🎣 Campaña creada exitosamente"
    actions:
      - log_event
      - notify_admin
      - schedule_tracking
      
  user_failed:
    message: "⚠️ Usuario requiere training"
    actions:
      - assign_training
      - update_risk_score
      - notify_manager
      
  training_completed:
    message: "✅ Training completado"
    actions:
      - award_points
      - update_metrics
      - schedule_retest

integrations:
  gophish:
    enabled: true
    auto_sync: true
    
  purple_team:
    enabled: true
    share_intelligence: true
```

### Skills Disponibles

| Skill | Descripción | Trigger |
|-------|-------------|---------|
| **campaign_creator** | Crea campañas de phishing | "crear campaña" |
| **metrics_analyzer** | Analiza métricas | "analizar métricas" |
| **training_designer** | Diseña módulos de training | "crear training" |
| **report_generator** | Genera reportes | "generar reporte" |
| **purple_team_integrator** | Integra con Purple Team | "integrar con red/blue" |

---

## 💜 Integración Purple Team

### Matriz de Integración

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    PURPLE TEAM INTEGRATION MATRIX                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  FROM/TO        │ 🔴 RED    │ 🔵 BLUE   │ 🟡 YELLOW │ 🟢 GREEN  │ ⚪ WHITE │
│  ───────────────┼───────────┼───────────┼───────────┼───────────┼──────────│
│  🟠 ORANGE      │           │           │           │           │          │
│  ───────────────┼───────────┼───────────┼───────────┼───────────┼──────────│
│  Phishing       │ Attack    │ Detection │ Secure    │ Alert     │ Policy   │
│  Results        │ Vectors   │ Rules     │ Code      │ Rules     │ Updates  │
│  ───────────────┼───────────┼───────────┼───────────┼───────────┼──────────│
│  User Behavior  │ Target    │ Baseline  │ Training  │ Anomaly   │ Awareness│
│  Patterns       │ Profiles  │ Behavior  │ Needs     │ Detection │ Metrics  │
│  ───────────────┼───────────┼───────────┼───────────┼───────────┼──────────│
│  Training       │ Social    │ Response  │ DevSec    │ Incident  │ Compliance│
│  Gaps           │ Eng Tests │ Training  │ Training  │ Playbooks │ Training │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### APIs de Integración

```python
# Ejemplo de integración bidireccional

class PurpleTeamIntegration:
    """Integración con otros equipos del Purple Team"""
    
    def share_with_red_team(self, data):
        """Compartir datos con Red Team para mejorar ataques"""
        # Usuarios más susceptibles
        # Horarios de mayor vulnerabilidad
        # Tipos de phishing más efectivos
        pass
    
    def receive_from_red_team(self, attack_vector):
        """Recibir nuevos vectores de ataque para awareness"""
        # Crear campaña basada en nuevo vector
        # Generar training específico
        pass
    
    def share_with_blue_team(self, data):
        """Compartir datos con Blue Team para detección"""
        # Patrones de comportamiento
        # Indicadores de compromiso humano
        pass
    
    def receive_from_blue_team(self, incident):
        """Recibir incidentes para training"""
        # Crear caso de estudio
        # Actualizar módulos de training
        pass
```

---

## 📊 Modelo de Datos

### Esquema de Base de Datos

```sql
-- Campañas de Phishing
CREATE TABLE campaigns (
    id UUID PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    status ENUM('draft', 'scheduled', 'active', 'completed', 'cancelled'),
    difficulty ENUM('easy', 'medium', 'hard', 'expert'),
    template_id UUID REFERENCES templates(id),
    start_date TIMESTAMP,
    end_date TIMESTAMP,
    created_by UUID REFERENCES users(id),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Resultados de Campaña
CREATE TABLE campaign_results (
    id UUID PRIMARY KEY,
    campaign_id UUID REFERENCES campaigns(id),
    user_id UUID REFERENCES users(id),
    email_sent_at TIMESTAMP,
    email_opened_at TIMESTAMP,
    link_clicked_at TIMESTAMP,
    credentials_submitted_at TIMESTAMP,
    reported_at TIMESTAMP,
    training_assigned_at TIMESTAMP,
    training_completed_at TIMESTAMP
);

-- Usuarios
CREATE TABLE users (
    id UUID PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255),
    department VARCHAR(100),
    risk_score INTEGER DEFAULT 50,
    total_points INTEGER DEFAULT 0,
    badges JSONB DEFAULT '[]',
    created_at TIMESTAMP DEFAULT NOW()
);

-- Módulos de Training
CREATE TABLE training_modules (
    id UUID PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    duration_minutes INTEGER,
    difficulty ENUM('basic', 'intermediate', 'advanced'),
    content JSONB,
    quiz_id UUID REFERENCES quizzes(id),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Métricas
CREATE TABLE metrics (
    id UUID PRIMARY KEY,
    metric_type VARCHAR(50),
    value DECIMAL,
    metadata JSONB,
    recorded_at TIMESTAMP DEFAULT NOW()
);
```

---

## 🔐 Consideraciones de Seguridad

### Políticas de Seguridad

```yaml
security_policies:
  data_protection:
    - Encriptar datos en reposo (AES-256)
    - Encriptar datos en tránsito (TLS 1.3)
    - Anonimizar datos en reportes externos
    - Retención de datos: 2 años
    
  access_control:
    - RBAC implementado
    - MFA requerido para admins
    - Audit logging habilitado
    - Session timeout: 30 minutos
    
  campaign_ethics:
    - No usar datos reales de empleados sin consentimiento
    - Notificar a HR antes de campañas
    - No penalizar laboralmente por fallar
    - Enfoque educativo, no punitivo
    
  compliance:
    - GDPR compliant
    - SOC 2 Type II
    - ISO 27001
    - NIST CSF
```

---

## 📈 Roadmap

### Q1 2024
- [x] Setup inicial del workspace
- [x] Integración con GoPhish
- [x] Dashboard básico de métricas
- [ ] Primeras campañas piloto

### Q2 2024
- [ ] Sistema de gamification completo
- [ ] Integración con SIEM
- [ ] Mobile app para training
- [ ] AI-powered template generation

### Q3 2024
- [ ] Integración completa Purple Team
- [ ] Vishing automation
- [ ] Advanced analytics
- [ ] Custom LMS

### Q4 2024
- [ ] Machine learning para risk scoring
- [ ] Automated remediation workflows
- [ ] Multi-tenant support
- [ ] Enterprise features

---

## 📞 Contacto y Soporte

| Recurso | Enlace |
|---------|--------|
| **Documentación** | `/docs/` |
| **Issues** | GitHub Issues |
| **Slack** | #orange-team |
| **Email** | orange-team@company.com |

---

<div align="center">

**🟠 ORANGE TEAM - Security Awareness Platform**

*Construido con ❤️ para fortalecer el factor humano*

</div>
