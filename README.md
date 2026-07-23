# NexusStrike Framework

## Advanced Purple Teaming Operations Platform

<div align="center">

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg?style=for-the-badge&logo=python)
![License](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)
![Version](https://img.shields.io/badge/Version-1.0.0-orange.svg?style=for-the-badge)

**[Documentation](docs/README.md)** • **[Installation](#installation)** • **[Usage](#usage)**

</div>

---

## Overview

NexusStrike is a next-generation cybersecurity framework designed for **purple team operations**. It combines offensive security capabilities with defensive intelligence, powered by AI-driven automation and intelligent orchestration.

Built upon the foundation of [KittySploit](https://github.com/SIA-IOTechnology/Kittysploit-framework) and enhanced with modern features, NexusStrike provides a comprehensive platform for security professionals.

## Key Features

| Feature | Description |
|---------|-------------|
| 🤖 **AI Integration** | Connect to Ollama, OpenAI, Anthropic, or local models for intelligent attack planning |
| 📚 **Playbook System** | YAML-defined automated attack sequences for routine tasks |
| 🔌 **Module Ecosystem** | Hundreds of pre-built modules from KittySploit |
| 💻 **Interactive Shell** | Enhanced CLI with auto-completion and history |
| 🗂️ **Workspace Management** | Organize engagements by workspace |
| 🔗 **Session Handling** | Manage multiple active sessions |
| 🌐 **REST API** | Programmatic access to all framework features |

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/your-org/nexusstrike-framework.git
cd nexusstrike-framework

# Install dependencies
pip install -r requirements.txt

# Launch the interactive shell
python nexusstrike.py
```

### Basic Usage

```bash
# Start interactive console
python nexusstrike.py

# Run a single module
python nexusstrike.py --module scanner/http/port_scan -t example.com

# Execute a playbook
python nexusstrike.py --playbook web-recon -t example.com

# AI-powered attack planning
python nexusstrike.py --ai-plan -t example.com --objective "find vulnerabilities"

# Start API server
python nexusstrike.py --api --api-port 8080
```

## Interactive Shell Commands

```
nexusstrike$ help          # Show available commands
nexusstrike$ list modules  # List all modules
nexusstrike$ search http   # Search for modules
nexusstrike$ use <module>  # Load a module
nexusstrike$ set TARGET example.com
nexusstrike$ run           # Execute module
nexusstrike$ playbook web-recon example.com
nexusstrike$ ai plan example.com "gain access"
nexusstrike$ exit
```

## Architecture

```
┌─────────────────────────────────────────┐
│         NexusStrike Framework            │
├─────────────────────────────────────────┤
│  ┌─────────┐  ┌─────────┐  ┌─────────┐ │
│  │  Shell  │  │   API   │  │   CLI   │ │
│  └────┬────┘  └────┬────┘  └────┬────┘ │
│       └─────────────┼─────────────┘     │
│                     ▼                   │
│           ┌─────────────────┐           │
│           │  Core Framework │           │
│           └────────┬────────┘           │
│     ┌──────────────┼──────────────┐     │
│     ▼              ▼              ▼     │
│  ┌──────┐    ┌──────────┐    ┌──────┐  │
│  │Module│    │ Playbook │    │  AI  │  │
│  │Loader│    │ Manager  │    │Engine│  │
│  └──┬───┘    └────┬─────┘    └──┬───┘  │
│     │             │              │      │
│     ▼             ▼              ▼      │
│  KittySploit   YAML Plans    LLM APIs   │
│   Modules                              │
└─────────────────────────────────────────┘
```

## Core Components

### 1. Module Loader
Dynamic discovery and execution of security modules from KittySploit.

### 2. Playbook Manager  
YAML-based automation for multi-step operations.

### 3. AI Engine
Intelligent attack planning with support for:
- Ollama (local models)
- OpenAI (GPT-4, GPT-3.5)
- Anthropic (Claude 3)

### 4. Interactive Shell
Rich CLI with tab completion, history, and dynamic prompts.

## Example Playbook

```yaml
id: web-recon
name: Web Application Reconnaissance
description: Comprehensive web reconnaissance

chain:
  - id: port_scan
    module: scanner/port/tcp_scan
    description: Scan for open ports
    options:
      PORTS: "80,443,8080"
  
  - id: tech_detect
    module: scanner/http/tech_detect
    description: Detect technologies
  
  - id: vuln_scan
    module: scanner/http/vuln_scan
    description: Vulnerability scanning
```

## AI Integration

Configure your preferred AI provider:

```bash
# Using Ollama (local)
export AI_PROVIDER=ollama
export AI_MODEL=llama3.1:8b

# Using OpenAI
export AI_PROVIDER=openai
export AI_API_KEY=your-api-key
export AI_MODEL=gpt-4

# Using Anthropic
export AI_PROVIDER=anthropic
export AI_API_KEY=your-api-key
export AI_MODEL=claude-3-sonnet-20240229
```

## Documentation

See [docs/README.md](docs/README.md) for complete documentation including:
- Installation guide
- Architecture details
- Module development
- API reference
- Best practices
- Troubleshooting

## License

MIT License - See LICENSE file for details.

## Credits

Built upon the excellent [KittySploit Framework](https://github.com/SIA-IOTechnology/Kittysploit-framework).

---

<div align="center">

**NexusStrike Framework v1.0.0**

*Advanced Purple Teaming Operations Platform*

</div>
