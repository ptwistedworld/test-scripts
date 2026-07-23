# NexusStrike Framework Documentation

## Advanced Purple Teaming Operations Platform

**Version:** 1.0.0  
**License:** MIT  
**Author:** Security Team

---

## Table of Contents

1. [Introduction](#introduction)
2. [Architecture](#architecture)
3. [Installation](#installation)
4. [Quick Start](#quick-start)
5. [Core Components](#core-components)
6. [Modules](#modules)
7. [Playbooks](#playbooks)
8. [AI Engine](#ai-engine)
9. [Interactive Shell](#interactive-shell)
10. [API Reference](#api-reference)
11. [Module Development](#module-development)
12. [Best Practices](#best-practices)
13. [Troubleshooting](#troubleshooting)

---

## Introduction

### What is NexusStrike?

NexusStrike is a next-generation cybersecurity framework designed for **purple team operations**. It combines offensive security capabilities with defensive intelligence, powered by AI-driven automation and intelligent orchestration.

Built upon the foundation of KittySploit and enhanced with modern features, NexusStrike provides:

- **Modular Architecture**: Easy-to-extend module system
- **AI-Powered Operations**: Intelligent attack planning and analysis
- **Playbook Automation**: Curated sequences for routine tasks
- **Interactive Shell**: Rich CLI with intelligent completion
- **Purple Team Focus**: Both offensive and defensive capabilities

### Key Features

| Feature | Description |
|---------|-------------|
| **AI Integration** | Connect to Ollama, OpenAI, Anthropic, or local models for intelligent planning |
| **Playbook System** | YAML-defined automated attack sequences |
| **Module Ecosystem** | Hundreds of pre-built modules from KittySploit |
| **Interactive Console** | Enhanced shell with auto-completion and history |
| **Workspace Management** | Organize engagements by workspace |
| **Session Handling** | Manage multiple active sessions |
| **REST API** | Programmatic access to all framework features |

### Use Cases

- **Red Team Operations**: Simulate advanced adversaries
- **Penetration Testing**: Comprehensive security assessments
- **Purple Team Exercises**: Collaborative offensive/defensive training
- **Security Research**: Vulnerability discovery and exploitation
- **Training & Education**: Learn offensive security techniques

---

## Architecture

### High-Level Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    NexusStrike Framework                     │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │ Interactive  │  │   REST API   │  │   CLI Tools  │       │
│  │    Shell     │  │   Server     │  │              │       │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘       │
│         │                 │                 │                │
│         └─────────────────┼─────────────────┘                │
│                           │                                  │
│                  ┌────────▼────────┐                         │
│                  │  Framework Core │                         │
│                  │   (Orchestrator)│                         │
│                  └────────┬────────┘                         │
│                           │                                  │
│     ┌─────────────────────┼─────────────────────┐           │
│     │                     │                     │            │
│     ▼                     ▼                     ▼            │
│ ┌─────────┐        ┌─────────────┐       ┌──────────┐       │
│ │ Module  │        │  Playbook   │       │    AI    │       │
│ │ Loader  │        │  Manager    │       │  Engine  │       │
│ └────┬────┘        └──────┬──────┘       └────┬─────┘       │
│      │                   │                    │              │
│      ▼                   ▼                    ▼              │
│ ┌─────────┐        ┌─────────────┐       ┌──────────┐       │
│ │ Kitty-  │        │   YAML      │       │  LLM     │       │
│ Sploit    │        │  Playbooks  │       │Providers │       │
│ Modules   │        │             │       │          │       │
│ └─────────┘        └─────────────┘       └──────────┘       │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Component Breakdown

#### Core Components

1. **Framework Orchestrator** (`nexusstrike.py`)
   - Main entry point
   - Component initialization
   - Lifecycle management

2. **Module Loader** (`core/module_loader.py`)
   - Dynamic module discovery
   - Module loading and execution
   - Dependency management

3. **Playbook Manager** (`core/playbook_manager.py`)
   - YAML playbook parsing
   - Sequential execution
   - Conditional logic

4. **AI Engine** (`core/ai_engine.py`)
   - Multi-provider LLM support
   - Attack planning
   - Analysis and reporting

5. **Interactive Shell** (`core/interactive_shell.py`)
   - Rich CLI interface
   - Command completion
   - Session management

#### Supporting Components

- **Workspace Manager**: Organize engagements
- **Session Manager**: Track active sessions
- **Database Manager**: Persistent storage
- **API Server**: RESTful interface

---

## Installation

### Prerequisites

- Python 3.9 or higher
- pip package manager
- Git (for cloning repositories)

### Quick Installation

```bash
# Clone the repository
git clone https://github.com/your-org/nexusstrike-framework.git
cd nexusstrike-framework

# Install dependencies
pip install -r requirements.txt

# Verify installation
python nexusstrike.py --version
```

### Dependencies

Create a `requirements.txt` file:

```txt
prompt_toolkit>=3.0.0
pyyaml>=6.0
requests>=2.28.0
aiohttp>=3.8.0
openai>=1.0.0
anthropic>=0.18.0
```

### Optional: AI Provider Setup

#### Ollama (Local LLM)

```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Pull a model
ollama pull llama3.1:8b

# Configure NexusStrike
export AI_PROVIDER=ollama
export AI_MODEL=llama3.1:8b
export AI_API_BASE=http://localhost:11434
```

#### OpenAI

```bash
export AI_PROVIDER=openai
export AI_API_KEY=your-openai-api-key
export AI_MODEL=gpt-4
```

#### Anthropic

```bash
export AI_PROVIDER=anthropic
export AI_API_KEY=your-anthropic-api-key
export AI_MODEL=claude-3-sonnet-20240229
```

---

## Quick Start

### Launch the Interactive Shell

```bash
python nexusstrike.py
```

You'll see the NexusStrike banner and prompt:

```
  _   _                     ____                  _   
 | \ | |_   _ _ __ ___     / ___|_      _____  ___| |_ 
 |  \| | | | | '__/ _ \    \___ \ \ /\ / / _ \/ __| __|
 | |\  | |_| | | | (_) |    ___) \ V  V /  __/\__ \ |_ 
 |_| \_|\__,_|_|  \___/    |____/ \_/\_/ \___||___/\__|
                                                       
         Advanced Purple Teaming Framework v1.0.0
          Type 'help' for available commands
    
nexusstrike$ 
```

### Basic Commands

```bash
# List available modules
nexusstrike$ list modules

# Search for modules
nexusstrike$ search http

# Load a module
nexusstrike$ use scanner/http/port_scan

# View module options
nexusstrike$ show options

# Set options
nexusstrike$ set TARGET example.com
nexusstrike$ set PORTS 80,443,8080

# Execute the module
nexusstrike$ run

# Unload module
nexusstrike$ back

# Run a playbook
nexusstrike$ playbook web-recon example.com

# AI attack planning
nexusstrike$ ai plan example.com "gain initial access"

# Exit
nexusstrike$ exit
```

### Command-Line Usage

```bash
# Run a single module
python nexusstrike.py --module scanner/http/port_scan -t example.com

# Execute a playbook
python nexusstrike.py --playbook web-recon -t example.com

# AI planning
python nexusstrike.py --ai-plan -t example.com --objective "find vulnerabilities"

# Start API server
python nexusstrike.py --api --api-port 8080
```

---

## Core Components

### Framework Class

The main `NexusStrikeFramework` class orchestrates all operations:

```python
from nexusstrike import NexusStrikeFramework

# Initialize
framework = NexusStrikeFramework()

# Get status
status = framework.get_status()
print(status)

# Load and execute a module
framework.load_module('scanner/http/port_scan')
result = framework.execute_module('scanner/http/port_scan', {'TARGET': 'example.com'})

# Run a playbook
success = framework.run_playbook('web-recon', target='example.com')

# AI planning
import asyncio
plan = asyncio.run(framework.ai_plan_attack('example.com', 'find vulnerabilities'))
```

### Module Loader

Discovers and loads modules dynamically:

```python
from core.module_loader import ModuleLoader

loader = ModuleLoader()
loader.discover_modules()

# Load specific module
module = loader.load('exploits/http/rce_scanner')

# Access module cache
modules = loader.modules_cache
```

### Playbook Manager

Manages playbook execution:

```python
from core.playbook_manager import PlaybookManager

manager = PlaybookManager(framework)
manager.load_playbooks()

# List playbooks
playbooks = manager.list_playbooks()

# Validate playbook
validation = manager.validate_playbook('web-recon')

# Execute playbook
success = manager.execute('web-recon', target='example.com')
```

### AI Engine

Provides AI-powered capabilities:

```python
from core.ai_engine import AIEngine

ai = AIEngine(framework)

# Plan attack
import asyncio
plan = asyncio.run(ai.plan_attack('example.com', 'gain shell access'))

# Analyze vulnerabilities
analysis = asyncio.run(ai.analyze_vulnerabilities(vuln_data))

# Generate report
report = asyncio.run(ai.generate_report(engagement_data))
```

---

## Modules

### Module Structure

Modules are organized in categories:

```
modules/
├── scanner/
│   ├── http/
│   │   ├── port_scan.py
│   │   ├── vuln_scan.py
│   │   └── tech_detect.py
│   ├── network/
│   └── ldap/
├── exploits/
│   ├── http/
│   ├── linux/
│   └── windows/
├── auxiliary/
├── post/
└── payloads/
```

### Using Modules

```bash
# List all modules
nexusstrike$ list modules

# Search modules
nexusstrike$ search sqli

# Use a module
nexusstrike$ use exploits/http/sqli_injection

# View information
nexusstrike$ info

# Set options
nexusstrike$ set TARGET example.com
nexusstrike$ set PARAMETER id
nexusstrike$ set PAYLOAD 'UNION SELECT'

# Execute
nexusstrike$ run
```

### Module Categories

| Category | Description | Example Modules |
|----------|-------------|-----------------|
| **scanner** | Reconnaissance and discovery | port_scan, vuln_scan, tech_detect |
| **exploits** | Exploitation modules | rce_scanner, sqli_injection |
| **auxiliary** | Support tools | fuzzers, bruteforce |
| **post** | Post-exploitation | privilege_escalation, lateral_movement |
| **payloads** | Payload generation | reverse_shell, bind_shell |

---

## Playbooks

### What are Playbooks?

Playbooks are YAML-defined sequences of modules that automate common workflows. They enable:

- Automated reconnaissance
- Standardized testing procedures
- Repeatable engagement workflows
- Knowledge capture and sharing

### Example Playbook

```yaml
id: web-recon
version: "1.0"
name: Web Application Reconnaissance
description: Comprehensive web application reconnaissance
tags: [recon, web, discovery]

prerequisites:
  signals_any:
    - web_application
  tech_any:
    - http

chain:
  - id: port_scan
    module: scanner/port/tcp_scan
    description: Scan for open ports
    options:
      PORTS: "80,443,8080,8443"
  
  - id: http_enum
    module: scanner/http/enum
    description: Enumerate web directories
    options: {}
  
  - id: tech_detect
    module: scanner/http/tech_detect
    description: Detect technologies
    options: {}
  
  - id: vuln_scan
    module: scanner/http/vuln_scan
    description: Vulnerability scanning
    options: {}

blockers:
  - WAF blocking scans
  - Rate limiting

references:
  - "OWASP Testing Guide"
```

### Creating Playbooks

1. Create a YAML file in `playbooks/library/`
2. Define the structure (id, name, description, chain)
3. Add module steps with options
4. Test with `playbook validate <id>`

### Running Playbooks

```bash
# From interactive shell
nexusstrike$ playbook web-recon example.com

# From command line
python nexusstrike.py --playbook web-recon -t example.com

# With custom variables
python nexusstrike.py --playbook ad-assessment -o DC_IP=192.168.1.10
```

### Built-in Playbooks

| Playbook | Description | Use Case |
|----------|-------------|----------|
| `web-recon` | Web reconnaissance | Initial web app assessment |
| `ad-assessment` | Active Directory assessment | Internal network engagements |
| `web-sqli-to-shell` | SQLi exploitation chain | Bug bounty hunting |
| `linux-privesc` | Linux privilege escalation | Post-exploitation |

---

## AI Engine

### Overview

The AI Engine integrates with multiple LLM providers to enable:

- Intelligent attack planning
- Vulnerability correlation
- Module recommendations
- Automated reporting

### Configuration

Set environment variables:

```bash
# Choose provider
export AI_PROVIDER=ollama  # or openai, anthropic, local

# Model configuration
export AI_MODEL=llama3.1:8b
export AI_API_BASE=http://localhost:11434
export AI_API_KEY=your-api-key  # For cloud providers
```

### AI Planning

Request an AI-generated attack plan:

```bash
nexusstrike$ ai plan example.com "gain initial access"
```

Example output:

```
[*] AI is planning attack strategy...
     Target: example.com
     Objective: gain initial access

[+] AI Attack Plan:
  1. scanner/http/port_scan - Identify open ports and services
  2. scanner/http/tech_detect - Detect web technologies
  3. scanner/http/vuln_scan - Find known vulnerabilities
  4. exploits/http/auto_exploit - Attempt automated exploitation
  5. post/shell/reverse_tcp - Establish persistence
```

### Supported Providers

| Provider | Models | Setup |
|----------|--------|-------|
| **Ollama** | Local models (Llama, Mistral, etc.) | Install Ollama, pull model |
| **OpenAI** | GPT-3.5, GPT-4 | API key required |
| **Anthropic** | Claude 3 family | API key required |
| **Local** | Custom models | Configure manually |

### AI Capabilities

1. **Attack Planning**: Generate strategic attack sequences
2. **Vulnerability Analysis**: Correlate and prioritize findings
3. **Module Selection**: Recommend appropriate modules
4. **Report Generation**: Create professional reports
5. **Pattern Recognition**: Identify attack patterns

---

## Interactive Shell

### Commands Reference

| Command | Description | Example |
|---------|-------------|---------|
| `use` | Load a module | `use scanner/http/port_scan` |
| `run` | Execute current module | `run` |
| `execute` | Load and execute | `execute exploits/http/rce` |
| `info` | Module information | `info` |
| `show options` | Display options | `show options` |
| `set` | Set option | `set TARGET example.com` |
| `back` | Unload module | `back` |
| `search` | Search modules | `search http` |
| `list` | List modules/playbooks | `list modules` |
| `playbook` | Execute playbook | `playbook web-recon target.com` |
| `sessions` | List sessions | `sessions` |
| `ai` | AI operations | `ai plan target.com objective` |
| `workspace` | Switch workspace | `workspace engagement1` |
| `status` | Framework status | `status` |
| `help` | Show help | `help` |
| `exit` | Exit shell | `exit` |

### Features

- **Tab Completion**: Auto-complete commands, modules, options
- **Command History**: Navigate previous commands with up/down arrows
- **Dynamic Prompt**: Shows current module when loaded
- **Color Output**: Syntax highlighting for better readability
- **Auto-Suggest**: Context-aware suggestions

### Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Tab` | Auto-complete |
| `Ctrl+R` | Reverse search history |
| `Ctrl+C` | Cancel current command |
| `Ctrl+D` | Exit shell |
| `Up/Down` | Navigate history |

---

## API Reference

### REST API

Start the API server:

```bash
python nexusstrike.py --api --api-port 8080
```

### Endpoints

#### GET /status

Get framework status.

```bash
curl http://localhost:8080/status
```

Response:
```json
{
  "name": "NexusStrike",
  "version": "1.0.0",
  "loaded_modules": 150,
  "active_sessions": 0,
  "playbooks_available": 10,
  "ai_engine_ready": true
}
```

#### GET /modules

List all modules.

```bash
curl http://localhost:8080/modules
```

#### POST /modules/:path/run

Execute a module.

```bash
curl -X POST http://localhost:8080/modules/scanner/http/port_scan/run \
  -H "Content-Type: application/json" \
  -d '{"TARGET": "example.com", "PORTS": "80,443"}'
```

#### GET /playbooks

List playbooks.

```bash
curl http://localhost:8080/playbooks
```

#### POST /playbooks/:id/run

Execute a playbook.

```bash
curl -X POST http://localhost:8080/playbooks/web-recon/run \
  -H "Content-Type: application/json" \
  -d '{"target": "example.com"}'
```

#### POST /ai/plan

Request AI attack plan.

```bash
curl -X POST http://localhost:8080/ai/plan \
  -H "Content-Type: application/json" \
  -d '{"target": "example.com", "objective": "find vulnerabilities"}'
```

---

## Module Development

### Creating a New Module

1. Create a Python file in the appropriate category directory
2. Inherit from `BaseModule`
3. Implement required methods

### Module Template

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from core.framework.base_module import BaseModule


class MyModule(BaseModule):
    """
    Module description here
    """
    
    def __init__(self):
        super().__init__()
        
        # Module metadata
        self.name = "My Module"
        self.description = "Description of what the module does"
        self.author = "Your Name"
        self.version = "1.0"
        
        # Module options
        self.options = {
            'TARGET': {
                'value': '',
                'required': True,
                'description': 'Target host'
            },
            'PORT': {
                'value': '80',
                'required': False,
                'description': 'Target port'
            }
        }
    
    def check(self) -> bool:
        """Validate options before execution"""
        if not self.options['TARGET']['value']:
            return False
        return True
    
    def execute(self):
        """Main execution logic"""
        target = self.options['TARGET']['value']
        port = self.options['PORT']['value']
        
        # Your code here
        result = self.perform_action(target, port)
        
        return result
    
    def perform_action(self, target, port):
        """Implement your logic"""
        # Implementation
        return {"status": "success"}
```

### Module Best Practices

1. **Validate Input**: Always check options in `check()` method
2. **Error Handling**: Use try/except blocks
3. **Logging**: Use framework logging
4. **Documentation**: Add clear docstrings
5. **Testing**: Test thoroughly before sharing

### Registering Modules

Modules are auto-discovered from the `modules/` directory. No manual registration needed.

---

## Best Practices

### Operational Security

1. **Authorization**: Only test systems you own or have explicit permission to test
2. **Scope**: Define and adhere to engagement scope
3. **Logging**: Maintain detailed logs of all activities
4. **Data Handling**: Securely store and dispose of sensitive data

### Framework Usage

1. **Workspaces**: Use separate workspaces for different engagements
2. **Playbooks**: Leverage playbooks for consistency
3. **AI Planning**: Review AI suggestions before execution
4. **Module Selection**: Understand modules before running them

### Performance

1. **Rate Limiting**: Respect rate limits on targets
2. **Parallel Execution**: Use async features where available
3. **Resource Management**: Monitor memory and CPU usage
4. **Caching**: Utilize module caching for repeated operations

---

## Troubleshooting

### Common Issues

#### Module Not Found

```
[!] Failed to load module: scanner/http/nonexistent
```

**Solution**: Check module path spelling. Use `list modules` to see available modules.

#### AI Engine Not Ready

```
[!] AI Engine not ready
```

**Solution**: 
1. Verify AI provider is installed and running
2. Check environment variables
3. Test connection manually

#### Playbook Execution Fails

```
[!] Step execution error: Module not found
```

**Solution**: Ensure all modules referenced in playbook exist. Run `playbook validate <id>`.

#### Import Errors

```
ImportError: No module named 'prompt_toolkit'
```

**Solution**: Install missing dependencies: `pip install -r requirements.txt`

### Getting Help

1. **Documentation**: Check this documentation
2. **Help Command**: Use `help` in interactive shell
3. **Logs**: Review `logs/nexusstrike.log`
4. **Issues**: Report bugs on GitHub

---

## Appendix

### A. Module Reference

Complete list of available modules (auto-generated from KittySploit).

### B. Playbook Templates

Pre-built playbook templates for common scenarios.

### C. Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `AI_PROVIDER` | AI provider (ollama, openai, anthropic) | ollama |
| `AI_MODEL` | Model name | llama3.1:8b |
| `AI_API_KEY` | API key for cloud providers | - |
| `AI_API_BASE` | API base URL | http://localhost:11434 |

### D. Changelog

**v1.0.0** - Initial Release
- Core framework implementation
- AI engine integration
- Playbook system
- Interactive shell
- KittySploit module integration

---

## License

MIT License - See LICENSE file for details.

## Credits

Built upon the excellent [KittySploit Framework](https://github.com/SIA-IOTechnology/Kittysploit-framework).

---

*Documentation generated for NexusStrike Framework v1.0.0*
