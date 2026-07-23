#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NexusStrike Playbook Manager
=============================

Manages playbook execution for automated purple team operations.
Playbooks are YAML-defined sequences of modules for common tasks.

Features:
- YAML playbook definitions
- Conditional execution
- Variable substitution
- Error handling and rollback
- Progress tracking
"""

import os
import yaml
import json
from pathlib import Path
from typing import Optional, Dict, List, Any
from dataclasses import dataclass


@dataclass
class PlaybookStep:
    """Represents a single step in a playbook"""
    id: str
    module: str
    description: str
    options: Dict = None
    condition: str = None
    on_success: str = None
    on_failure: str = None


@dataclass
class Playbook:
    """Represents a complete playbook"""
    id: str
    name: str
    version: str
    description: str
    steps: List[PlaybookStep]
    prerequisites: Dict = None
    tags: List[str] = None
    references: List[str] = None


class PlaybookManager:
    """
    Manages playbook loading, validation, and execution
    
    Features:
    - Load playbooks from YAML files
    - Validate playbook structure
    - Execute playbooks with error handling
    - Track execution progress
    - Support conditional steps
    """
    
    def __init__(self, framework):
        """
        Initialize Playbook Manager
        
        Args:
            framework: NexusStrikeFramework instance
        """
        self.framework = framework
        self.playbooks: Dict[str, Playbook] = {}
        self.library_path = Path('playbooks/library')
        self.execution_history = []
        
        # Ensure library directory exists
        self.library_path.mkdir(parents=True, exist_ok=True)
    
    def load_playbooks(self):
        """Load all playbooks from library"""
        if not self.library_path.exists():
            return
        
        for yaml_file in self.library_path.glob('*.yaml'):
            try:
                playbook = self._load_playbook(yaml_file)
                if playbook:
                    self.playbooks[playbook.id] = playbook
            except Exception as e:
                print(f"[!] Failed to load playbook {yaml_file}: {e}")
    
    def _load_playbook(self, yaml_path: Path) -> Optional[Playbook]:
        """Load a single playbook from YAML file"""
        try:
            with open(yaml_path, 'r') as f:
                data = yaml.safe_load(f)
            
            if not data:
                return None
            
            # Parse steps
            steps = []
            for step_data in data.get('chain', []):
                step = PlaybookStep(
                    id=step_data.get('id', ''),
                    module=step_data.get('module', ''),
                    description=step_data.get('description', ''),
                    options=step_data.get('options', {}),
                    condition=step_data.get('condition'),
                    on_success=step_data.get('on_success'),
                    on_failure=step_data.get('on_failure')
                )
                steps.append(step)
            
            playbook = Playbook(
                id=data.get('id', ''),
                name=data.get('name', ''),
                version=data.get('version', '1.0'),
                description=data.get('description', ''),
                steps=steps,
                prerequisites=data.get('prerequisites', {}),
                tags=data.get('tags', []),
                references=data.get('references', [])
            )
            
            return playbook
            
        except Exception as e:
            print(f"[!] Error loading playbook {yaml_path}: {e}")
            return None
    
    def execute(self, playbook_id: str, target: str = None, **kwargs) -> bool:
        """
        Execute a playbook
        
        Args:
            playbook_id: ID of playbook to execute
            target: Target for the playbook
            **kwargs: Additional parameters
            
        Returns:
            bool: Success status
        """
        if playbook_id not in self.playbooks:
            print(f"[!] Playbook not found: {playbook_id}")
            return False
        
        playbook = self.playbooks[playbook_id]
        print(f"[\033[94m*\033[0m] Executing playbook: {playbook.name}")
        print(f"     Description: {playbook.description}")
        
        execution_context = {
            'target': target,
            'results': {},
            'variables': kwargs,
            'current_step': 0,
            'failed_steps': []
        }
        
        success = True
        for i, step in enumerate(playbook.steps):
            print(f"\n[\033[94m*\033[0m] Step {i+1}/{len(playbook.steps)}: {step.description}")
            print(f"     Module: {step.module}")
            
            # Check condition if present
            if step.condition and not self._evaluate_condition(step.condition, execution_context):
                print(f"     [!] Condition not met, skipping step")
                continue
            
            # Prepare module options
            options = step.options or {}
            if target:
                options['TARGET'] = target
            
            # Inject context variables
            options = self._substitute_variables(options, execution_context)
            
            # Execute module
            try:
                result = self.framework.execute_module(step.module, options)
                execution_context['results'][step.id] = result
                
                if result:
                    print(f"     [\033[92m+\033[0m] Step completed successfully")
                else:
                    print(f"     [!] Step failed")
                    execution_context['failed_steps'].append(step.id)
                    
                    if step.on_failure:
                        print(f"     Handling failure: {step.on_failure}")
                        # Handle failure logic
                    else:
                        success = False
                        
            except Exception as e:
                print(f"     [!] Step execution error: {e}")
                execution_context['failed_steps'].append(step.id)
                success = False
            
            execution_context['current_step'] = i + 1
        
        # Store execution history
        self.execution_history.append({
            'playbook_id': playbook_id,
            'success': success,
            'context': execution_context
        })
        
        return success
    
    def _evaluate_condition(self, condition: str, context: Dict) -> bool:
        """Evaluate a condition string"""
        # Simple condition evaluation (can be extended)
        if condition.startswith('result.'):
            step_id = condition.split('.')[1].split('=')[0]
            expected = condition.split('=')[1] if '=' in condition else None
            
            result = context['results'].get(step_id)
            if expected:
                return str(result) == expected
            return bool(result)
        
        return True
    
    def _substitute_variables(self, options: Dict, context: Dict) -> Dict:
        """Substitute variables in options"""
        result = {}
        for key, value in options.items():
            if isinstance(value, str):
                # Replace {{variable}} with actual values
                for var_name, var_value in context['variables'].items():
                    value = value.replace(f'{{{{{var_name}}}}}', str(var_value))
                
                # Replace {{result.step_id}} with previous results
                for step_id, step_result in context['results'].items():
                    value = value.replace(f'{{{{result.{step_id}}}}}', str(step_result))
            
            result[key] = value
        
        return result
    
    def list_playbooks(self) -> List[Dict]:
        """List all available playbooks"""
        return [
            {
                'id': pb.id,
                'name': pb.name,
                'version': pb.version,
                'description': pb.description,
                'steps': len(pb.steps),
                'tags': pb.tags
            }
            for pb in self.playbooks.values()
        ]
    
    def get_playbook(self, playbook_id: str) -> Optional[Playbook]:
        """Get a specific playbook"""
        return self.playbooks.get(playbook_id)
    
    def create_playbook(self, playbook_data: Dict) -> bool:
        """Create a new playbook"""
        try:
            playbook_id = playbook_data.get('id')
            if not playbook_id:
                print("[!] Playbook must have an ID")
                return False
            
            yaml_path = self.library_path / f"{playbook_id}.yaml"
            
            with open(yaml_path, 'w') as f:
                yaml.dump(playbook_data, f, default_flow_style=False)
            
            # Reload playbooks
            self._load_playbook(yaml_path)
            
            print(f"[\033[92m+\033[0m] Playbook created: {playbook_id}")
            return True
            
        except Exception as e:
            print(f"[!] Failed to create playbook: {e}")
            return False
    
    def validate_playbook(self, playbook_id: str) -> Dict:
        """Validate a playbook structure"""
        playbook = self.get_playbook(playbook_id)
        
        if not playbook:
            return {'valid': False, 'errors': ['Playbook not found']}
        
        errors = []
        
        # Check required fields
        if not playbook.id:
            errors.append("Missing playbook ID")
        if not playbook.name:
            errors.append("Missing playbook name")
        if not playbook.steps:
            errors.append("No steps defined")
        
        # Validate each step
        for i, step in enumerate(playbook.steps):
            if not step.id:
                errors.append(f"Step {i+1} missing ID")
            if not step.module:
                errors.append(f"Step {i+1} missing module")
            
            # Check if module exists
            if step.module and step.module not in self.framework.module_loader.modules_cache:
                errors.append(f"Step {i+1}: Module '{step.module}' not found")
        
        return {
            'valid': len(errors) == 0,
            'errors': errors
        }


# Example playbook templates
PLAYBOOK_TEMPLATES = {
    'web-recon': {
        'id': 'web-recon',
        'name': 'Web Application Reconnaissance',
        'version': '1.0',
        'description': 'Comprehensive web application reconnaissance',
        'tags': ['recon', 'web', 'discovery'],
        'chain': [
            {
                'id': 'port_scan',
                'module': 'scanner/port/tcp_scan',
                'description': 'Scan for open ports',
                'options': {'PORTS': '80,443,8080,8443'}
            },
            {
                'id': 'http_enum',
                'module': 'scanner/http/enum',
                'description': 'Enumerate web directories',
                'options': {}
            },
            {
                'id': 'tech_detect',
                'module': 'scanner/http/tech_detect',
                'description': 'Detect technologies',
                'options': {}
            },
            {
                'id': 'vuln_scan',
                'module': 'scanner/http/vuln_scan',
                'description': 'Vulnerability scanning',
                'options': {}
            }
        ]
    },
    
    'ad-assessment': {
        'id': 'ad-assessment',
        'name': 'Active Directory Security Assessment',
        'version': '1.0',
        'description': 'Comprehensive AD security assessment',
        'tags': ['active-directory', 'windows', 'assessment'],
        'chain': [
            {
                'id': 'ldap_enum',
                'module': 'scanner/ldap/enum',
                'description': 'LDAP enumeration',
                'options': {}
            },
            {
                'id': 'smb_scan',
                'module': 'scanner/smb/scan',
                'description': 'SMB share scanning',
                'options': {}
            },
            {
                'id': 'kerberoast',
                'module': 'auxiliary/kerberos/kerberoast',
                'description': 'Kerberoasting attack',
                'options': {}
            }
        ]
    }
}
