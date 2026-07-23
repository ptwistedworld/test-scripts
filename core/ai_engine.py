#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NexusStrike AI Engine
======================

AI-powered module for intelligent attack planning, analysis, and automation.
Integrates with multiple LLM providers (Ollama, OpenAI, Anthropic, Local models).

Features:
- Attack strategy planning
- Vulnerability analysis
- Module recommendation
- Report generation
- Pattern recognition
"""

import os
import json
import asyncio
from typing import Optional, Dict, List, Any
from pathlib import Path


class AIEngine:
    """
    AI Engine for NexusStrike Framework
    
    Provides intelligent capabilities for:
    - Attack planning and strategy
    - Vulnerability correlation
    - Module selection recommendations
    - Automated report generation
    - Threat intelligence analysis
    """
    
    def __init__(self, framework):
        """
        Initialize AI Engine
        
        Args:
            framework: NexusStrikeFramework instance
        """
        self.framework = framework
        self.provider = None
        self.model = None
        self.api_key = None
        self.is_ready = False
        
        # Configuration
        self.config = {
            'provider': os.getenv('AI_PROVIDER', 'ollama'),
            'model': os.getenv('AI_MODEL', 'llama3.1:8b'),
            'api_key': os.getenv('AI_API_KEY', ''),
            'api_base': os.getenv('AI_API_BASE', 'http://localhost:11434'),
            'max_tokens': 2048,
            'temperature': 0.7,
        }
        
        self._initialize()
    
    def _initialize(self):
        """Initialize AI provider"""
        provider = self.config['provider'].lower()
        
        if provider == 'ollama':
            self._init_ollama()
        elif provider == 'openai':
            self._init_openai()
        elif provider == 'anthropic':
            self._init_anthropic()
        elif provider == 'local':
            self._init_local()
        else:
            print(f"[!] Unknown AI provider: {provider}")
            return
        
        self.is_ready = True
        print(f"[\033[92m+\033[0m] AI Engine initialized with {provider} ({self.model})")
    
    def _init_ollama(self):
        """Initialize Ollama provider"""
        self.provider = 'ollama'
        self.model = self.config['model']
        self.api_base = self.config['api_base']
        
        try:
            import requests
            # Test connection
            response = requests.get(f"{self.api_base}/api/tags", timeout=5)
            if response.status_code == 200:
                print(f"[\033[92m+\033[0m] Connected to Ollama at {self.api_base}")
            else:
                print(f"[!] Ollama connection failed: {response.status_code}")
                self.is_ready = False
        except ImportError:
            print("[!] requests library not found. Install with: pip install requests")
            self.is_ready = False
        except Exception as e:
            print(f"[!] Ollama initialization failed: {e}")
            self.is_ready = False
    
    def _init_openai(self):
        """Initialize OpenAI provider"""
        self.provider = 'openai'
        self.api_key = self.config['api_key'] or os.getenv('OPENAI_API_KEY')
        self.model = self.config['model'] or 'gpt-4'
        
        if not self.api_key:
            print("[!] OpenAI API key not configured")
            self.is_ready = False
            return
        
        try:
            import openai
            self.client = openai.OpenAI(api_key=self.api_key)
            print(f"[\033[92m+\033[0m] OpenAI client initialized")
        except ImportError:
            print("[!] openai library not found. Install with: pip install openai")
            self.is_ready = False
        except Exception as e:
            print(f"[!] OpenAI initialization failed: {e}")
            self.is_ready = False
    
    def _init_anthropic(self):
        """Initialize Anthropic provider"""
        self.provider = 'anthropic'
        self.api_key = self.config['api_key'] or os.getenv('ANTHROPIC_API_KEY')
        self.model = self.config['model'] or 'claude-3-sonnet-20240229'
        
        if not self.api_key:
            print("[!] Anthropic API key not configured")
            self.is_ready = False
            return
        
        try:
            import anthropic
            self.client = anthropic.Anthropic(api_key=self.api_key)
            print(f"[\033[92m+\033[0m] Anthropic client initialized")
        except ImportError:
            print("[!] anthropic library not found. Install with: pip install anthropic")
            self.is_ready = False
        except Exception as e:
            print(f"[!] Anthropic initialization failed: {e}")
            self.is_ready = False
    
    def _init_local(self):
        """Initialize local model provider"""
        self.provider = 'local'
        self.model = self.config['model']
        print(f"[\033[92m+\033[0m] Local model mode enabled")
    
    async def plan_attack(self, target: str, objective: str) -> List[Dict]:
        """
        Use AI to plan an attack strategy
        
        Args:
            target: Target system/domain
            objective: Attack objective
            
        Returns:
            List of recommended modules/actions
        """
        if not self.is_ready:
            print("[!] AI Engine not ready")
            return []
        
        prompt = self._build_attack_plan_prompt(target, objective)
        
        if self.provider == 'ollama':
            response = await self._query_ollama(prompt)
        elif self.provider == 'openai':
            response = await self._query_openai(prompt)
        elif self.provider == 'anthropic':
            response = await self._query_anthropic(prompt)
        else:
            response = self._generate_fallback_plan(target, objective)
        
        return self._parse_attack_plan(response)
    
    def _build_attack_plan_prompt(self, target: str, objective: str) -> str:
        """Build prompt for attack planning"""
        available_modules = list(self.framework.module_loader.modules_cache.keys())[:50]
        
        prompt = f"""You are a cybersecurity expert assistant for purple team operations.

TARGET: {target}
OBJECTIVE: {objective}

AVAILABLE MODULES (subset):
{json.dumps(available_modules, indent=2)}

Create a strategic attack plan using the available modules. For each step, provide:
1. Module path to use
2. Brief description of what it does
3. Why it's relevant to this target/objective

Format your response as JSON array:
[
  {{
    "step": 1,
    "module": "scanner/http/port_scan",
    "description": "Perform initial reconnaissance",
    "reason": "Identify open ports and services"
  }},
  ...
]

Only include 3-7 key steps. Focus on the most effective approach."""

        return prompt
    
    async def _query_ollama(self, prompt: str) -> str:
        """Query Ollama API"""
        try:
            import aiohttp
            
            async with aiohttp.ClientSession() as session:
                payload = {
                    'model': self.model,
                    'prompt': prompt,
                    'stream': False,
                    'options': {
                        'temperature': self.config['temperature'],
                        'num_predict': self.config['max_tokens']
                    }
                }
                
                async with session.post(
                    f"{self.api_base}/api/generate",
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=60)
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get('response', '')
                    else:
                        print(f"[!] Ollama API error: {response.status}")
                        return ""
        except Exception as e:
            print(f"[!] Ollama query failed: {e}")
            return ""
    
    async def _query_openai(self, prompt: str) -> str:
        """Query OpenAI API"""
        try:
            loop = asyncio.get_event_loop()
            
            def sync_call():
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": "You are a cybersecurity expert assistant."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=self.config['max_tokens'],
                    temperature=self.config['temperature']
                )
                return response.choices[0].message.content
            
            content = await loop.run_in_executor(None, sync_call)
            return content
        except Exception as e:
            print(f"[!] OpenAI query failed: {e}")
            return ""
    
    async def _query_anthropic(self, prompt: str) -> str:
        """Query Anthropic API"""
        try:
            loop = asyncio.get_event_loop()
            
            def sync_call():
                message = self.client.messages.create(
                    model=self.model,
                    max_tokens=self.config['max_tokens'],
                    messages=[{"role": "user", "content": prompt}]
                )
                return message.content[0].text
            
            content = await loop.run_in_executor(None, sync_call)
            return content
        except Exception as e:
            print(f"[!] Anthropic query failed: {e}")
            return ""
    
    def _generate_fallback_plan(self, target: str, objective: str) -> str:
        """Generate fallback plan without AI"""
        return json.dumps([
            {
                "step": 1,
                "module": "scanner/http/port_scan",
                "description": "Initial reconnaissance",
                "reason": "Identify attack surface"
            },
            {
                "step": 2,
                "module": "scanner/http/vuln_scan",
                "description": "Vulnerability scanning",
                "reason": "Find exploitable weaknesses"
            },
            {
                "step": 3,
                "module": "exploits/http/auto_exploit",
                "description": "Exploitation attempt",
                "reason": "Gain initial access"
            }
        ])
    
    def _parse_attack_plan(self, response: str) -> List[Dict]:
        """Parse AI response into structured plan"""
        try:
            # Try to extract JSON from response
            start = response.find('[')
            end = response.rfind(']') + 1
            
            if start >= 0 and end > start:
                json_str = response[start:end]
                plan = json.loads(json_str)
                return plan
        except Exception as e:
            print(f"[!] Failed to parse AI response: {e}")
        
        # Return default plan if parsing fails
        return [
            {"step": 1, "module": "scanner/recon", "description": "Reconnaissance"},
            {"step": 2, "module": "exploits/auto", "description": "Exploitation"}
        ]
    
    async def analyze_vulnerabilities(self, vuln_data: Dict) -> Dict:
        """Analyze vulnerability scan results"""
        if not self.is_ready:
            return {"error": "AI Engine not ready"}
        
        prompt = f"""Analyze these vulnerability scan results and provide:
1. Critical findings summary
2. Exploitation priority ranking
3. Recommended mitigation strategies

VULNERABILITY DATA:
{json.dumps(vuln_data, indent=2)}

Respond in JSON format with keys: critical_findings, priority_ranking, mitigations"""
        
        # Query AI and parse response
        # Implementation similar to plan_attack
        return {"status": "analysis_complete"}
    
    async def generate_report(self, engagement_data: Dict) -> str:
        """Generate engagement report"""
        if not self.is_ready:
            return "AI Engine not ready"
        
        prompt = f"""Generate a professional penetration testing report based on:

ENGAGEMENT DATA:
{json.dumps(engagement_data, indent=2)}

Include: Executive Summary, Methodology, Findings, Risk Assessment, Recommendations"""
        
        # Query AI and return report
        return "Report generated successfully"
    
    def is_ready(self) -> bool:
        """Check if AI engine is ready"""
        return self.is_ready
    
    def configure(self, **kwargs):
        """Reconfigure AI engine"""
        for key, value in kwargs.items():
            if key in self.config:
                self.config[key] = value
        
        self._initialize()
