#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NexusStrike Interactive Shell
==============================

Advanced interactive console for purple team operations with:
- Intelligent command completion
- Module management
- AI-assisted operations
- Real-time session handling
- Playbook execution
"""

import cmd
import json
import sys
import asyncio
from typing import Optional, Dict, List
from pathlib import Path

try:
    from prompt_toolkit import PromptSession
    from prompt_toolkit.completion import Completer, Completion
    from prompt_toolkit.history import FileHistory
    from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
    from prompt_toolkit.styles import Style
    from prompt_toolkit.key_binding import KeyBindings
    PROMPT_TOOLKIT_AVAILABLE = True
except ImportError:
    PROMPT_TOOLKIT_AVAILABLE = False


class NexusStrikeCompleter:
    """Intelligent command completer for NexusStrike shell"""
    
    def __init__(self, framework):
        self.framework = framework
        self.commands = [
            'use', 'run', 'execute', 'search', 'info', 'show',
            'set', 'unset', 'options', 'back', 'exit', 'quit',
            'playbook', 'list', 'load', 'unload', 'sessions',
            'ai', 'plan', 'analyze', 'report', 'workspace',
            'help', 'history', 'clear', 'version', 'status'
        ]
        self.module_cache = []
        self.playbook_cache = []
        self._update_cache()
    
    def _update_cache(self):
        """Update module and playbook caches"""
        if hasattr(self.framework, 'module_loader'):
            self.module_cache = list(self.framework.module_loader.modules_cache.keys())
        if hasattr(self.framework, 'playbook_manager'):
            self.playbook_cache = list(self.framework.playbook_manager.playbooks.keys())
    
    def get_completions(self, text, cursor_position):
        """Get completions for current input"""
        words = text.split()
        if not words:
            for cmd in self.commands:
                yield Completion(cmd, start_position=-len(text))
            return
        
        current_word = words[-1] if cursor_position > len(text) - len(words[-1]) else ''
        
        # Command completion
        if len(words) == 1:
            for cmd in self.commands:
                if cmd.startswith(current_word):
                    yield Completion(cmd, start_position=-len(current_word))
        
        # Module completion after 'use' or 'run'
        elif words[0] in ['use', 'run', 'execute']:
            for module in self.module_cache:
                if module.startswith(current_word):
                    yield Completion(module, start_position=-len(current_word))
        
        # Playbook completion after 'playbook'
        elif words[0] == 'playbook':
            for playbook in self.playbook_cache:
                if playbook.startswith(current_word):
                    yield Completion(playbook, start_position=-len(current_word))


class NexusStrikeShell:
    """
    Interactive shell for NexusStrike Framework
    
    Provides a rich CLI interface for:
    - Module selection and execution
    - Playbook management
    - AI-powered planning
    - Session management
    - Workspace operations
    """
    
    BANNER = r"""
  _   _                     ____                  _   
 | \ | |_   _ _ __ ___     / ___|_      _____  ___| |_ 
 |  \| | | | | '__/ _ \    \___ \ \ /\ / / _ \/ __| __|
 | |\  | |_| | | | (_) |    ___) \ V  V /  __/\__ \ |_ 
 |_| \_|\__,_|_|  \___/    |____/ \_/\_/ \___||___/\__|
                                                       
         Advanced Purple Teaming Framework v1.0.0
          Type 'help' for available commands
    """
    
    def __init__(self, framework):
        """
        Initialize the interactive shell
        
        Args:
            framework: NexusStrikeFramework instance
        """
        self.framework = framework
        self.current_module = None
        self.module_options = {}
        self.prompt_style = 'classic'  # 'classic' or 'prompt_toolkit'
        
        # Setup prompt toolkit if available
        if PROMPT_TOOLKIT_AVAILABLE:
            self.style = Style.from_dict({
                'prompt': 'ansired bold',
                'command': 'ansicyan',
                'module': 'ansigreen',
            })
            
            self.session = PromptSession(
                completer=NexusStrikeCompleter(framework),
                history=FileHistory('.nexusstrike_history'),
                auto_suggest=AutoSuggestFromHistory(),
                style=self.style,
                enable_history_search=True,
            )
        
        print(self.BANNER)
    
    def _get_prompt(self) -> str:
        """Generate dynamic prompt based on current state"""
        if self.current_module:
            return f"\033[91mnexusstrike\033[0m:\033[92m{self.current_module}\033[0m$ "
        return "\033[91mnexusstrike\033[0m$ "
    
    def run(self):
        """Main shell loop"""
        if PROMPT_TOOLKIT_AVAILABLE:
            self._run_prompt_toolkit()
        else:
            self._run_classic()
    
    def _run_prompt_toolkit(self):
        """Run shell using prompt_toolkit for enhanced UX"""
        while True:
            try:
                text = self.session.prompt(self._get_prompt())
                if text.strip():
                    self._process_command(text.strip())
            except KeyboardInterrupt:
                continue
            except EOFError:
                break
        
        print("\n[!] Goodbye!")
    
    def _run_classic(self):
        """Fallback classic shell without prompt_toolkit"""
        while True:
            try:
                text = input(self._get_prompt())
                if text.strip():
                    self._process_command(text.strip())
            except KeyboardInterrupt:
                continue
            except EOFError:
                break
        
        print("\n[!] Goodbye!")
    
    def _process_command(self, command: str):
        """Process user command"""
        parts = command.split(maxsplit=1)
        if not parts:
            return
        
        cmd = parts[0].lower()
        args = parts[1] if len(parts) > 1 else ''
        
        # Command dispatch
        commands = {
            'help': self._cmd_help,
            'use': self._cmd_use,
            'run': self._cmd_run,
            'execute': self._cmd_run,
            'info': self._cmd_info,
            'show': self._cmd_show,
            'set': self._cmd_set,
            'options': self._cmd_options,
            'back': self._cmd_back,
            'exit': self._cmd_exit,
            'quit': self._cmd_exit,
            'search': self._cmd_search,
            'list': self._cmd_list,
            'playbook': self._cmd_playbook,
            'sessions': self._cmd_sessions,
            'ai': self._cmd_ai,
            'plan': self._cmd_plan,
            'workspace': self._cmd_workspace,
            'status': self._cmd_status,
            'version': self._cmd_version,
            'clear': self._cmd_clear,
            'history': self._cmd_history,
        }
        
        handler = commands.get(cmd)
        if handler:
            handler(args)
        else:
            print(f"[!] Unknown command: {cmd}. Type 'help' for assistance.")
    
    def _cmd_help(self, args):
        """Display help information"""
        help_text = """
Available Commands:
-------------------
  use <module>           Load a module
  run                    Execute current module
  execute <module>       Load and execute a module in one step
  info                   Show information about current module
  show options           Display module options
  set <option> <value>   Set module option
  back                   Unload current module
  
  search <keyword>       Search for modules
  list [modules|playbooks]  List available modules or playbooks
  
  playbook <id> [target] Execute a playbook
  sessions               List active sessions
  
  ai plan <target> <objective>  Use AI to plan attack strategy
  ai analyze <data>      Analyze data with AI
  
  workspace <name>       Switch workspace
  status                 Show framework status
  version                Show version information
  clear                  Clear screen
  history                Show command history
  help                   Show this help message
  exit/quit              Exit the framework
        """
        print(help_text)
    
    def _cmd_use(self, args):
        """Load a module"""
        if not args:
            print("[!] Usage: use <module_path>")
            return
        
        module_path = args.strip()
        success = self.framework.load_module(module_path)
        
        if success:
            self.current_module = module_path
            print(f"[\033[92m+\033[0m] Module loaded: {module_path}")
            print(f"[\033[92m+\033[0m] Type 'options' to view available options")
            print(f"[\033[92m+\033[0m] Type 'run' to execute the module")
        else:
            print(f"[!] Failed to load module: {module_path}")
    
    def _cmd_run(self, args):
        """Execute current module"""
        if not self.current_module:
            print("[!] No module loaded. Use 'use <module>' first.")
            return
        
        print(f"[\033[94m*\033[0m] Executing module: {self.current_module}")
        result = self.framework.execute_module(self.current_module, self.module_options)
        
        if result:
            print(f"[\033[92m+\033[0m] Execution completed successfully")
            if isinstance(result, dict):
                print(json.dumps(result, indent=2))
            else:
                print(result)
        else:
            print("[!] Module execution failed")
    
    def _cmd_info(self, args):
        """Show module information"""
        if not self.current_module:
            print("[!] No module loaded")
            return
        
        module = self.framework.loaded_modules.get(self.current_module)
        if module:
            print(f"\nModule: {self.current_module}")
            print(f"Name: {getattr(module, 'name', 'N/A')}")
            print(f"Description: {getattr(module, 'description', 'N/A')}")
            print(f"Author: {getattr(module, 'author', 'N/A')}")
            print(f"References: {getattr(module, 'references', [])}")
        else:
            print("[!] Module information not available")
    
    def _cmd_show(self, args):
        """Show module details"""
        if args.lower() == 'options':
            self._cmd_options('')
        else:
            print("[!] Usage: show options")
    
    def _cmd_set(self, args):
        """Set module option"""
        if not self.current_module:
            print("[!] No module loaded")
            return
        
        parts = args.split(maxsplit=1)
        if len(parts) != 2:
            print("[!] Usage: set <option> <value>")
            return
        
        option, value = parts
        self.module_options[option.upper()] = value
        print(f"[\033[92m+\033[0m] {option.upper()} => {value}")
    
    def _cmd_options(self, args):
        """Display module options"""
        if not self.current_module:
            print("[!] No module loaded")
            return
        
        module = self.framework.loaded_modules.get(self.current_module)
        if not module:
            print("[!] Module not found")
            return
        
        print(f"\nModule Options ({self.current_module}):")
        print("-" * 50)
        
        # Get module options if available
        options = getattr(module, 'options', {})
        if options:
            for opt_name, opt_value in options.items():
                current = self.module_options.get(opt_name.upper(), opt_value)
                print(f"  {opt_name:20} => {current}")
        else:
            print("  No specific options defined")
        
        if self.module_options:
            print("\nUser-set Options:")
            for opt_name, opt_value in self.module_options.items():
                print(f"  {opt_name:20} => {opt_value}")
    
    def _cmd_back(self, args):
        """Unload current module"""
        self.current_module = None
        self.module_options = {}
        print("[\033[92m+\033[0m] Module unloaded")
    
    def _cmd_exit(self, args):
        """Exit the shell"""
        raise EOFError()
    
    def _cmd_search(self, args):
        """Search for modules"""
        if not args:
            print("[!] Usage: search <keyword>")
            return
        
        keyword = args.lower()
        results = []
        
        for module_path in self.framework.module_loader.modules_cache.keys():
            if keyword in module_path.lower():
                results.append(module_path)
        
        if results:
            print(f"\nFound {len(results)} matching modules:")
            for module in results[:20]:  # Limit to 20 results
                print(f"  - {module}")
            if len(results) > 20:
                print(f"  ... and {len(results) - 20} more")
        else:
            print("[!] No matching modules found")
    
    def _cmd_list(self, args):
        """List modules or playbooks"""
        list_type = args.lower() if args else 'modules'
        
        if list_type == 'modules':
            print(f"\nAvailable Modules ({len(self.framework.module_loader.modules_cache)} total):")
            categories = {}
            for module_path in self.framework.module_loader.modules_cache.keys():
                category = module_path.split('/')[0] if '/' in module_path else 'other'
                if category not in categories:
                    categories[category] = []
                categories[category].append(module_path)
            
            for category, modules in sorted(categories.items()):
                print(f"\n  {category.upper()} ({len(modules)}):")
                for module in modules[:5]:
                    print(f"    - {module}")
                if len(modules) > 5:
                    print(f"    ... and {len(modules) - 5} more")
        
        elif list_type == 'playbooks':
            playbooks = self.framework.playbook_manager.playbooks
            print(f"\nAvailable Playbooks ({len(playbooks)} total):")
            for pb_id, pb_info in list(playbooks.items())[:10]:
                name = pb_info.get('name', pb_id) if isinstance(pb_info, dict) else pb_id
                print(f"  - {pb_id}: {name}")
            if len(playbooks) > 10:
                print(f"  ... and {len(playbooks) - 10} more")
        else:
            print("[!] Usage: list [modules|playbooks]")
    
    def _cmd_playbook(self, args):
        """Execute a playbook"""
        if not args:
            print("[!] Usage: playbook <playbook_id> [target]")
            return
        
        parts = args.split(maxsplit=1)
        playbook_id = parts[0]
        target = parts[1] if len(parts) > 1 else None
        
        print(f"[\033[94m*\033[0m] Executing playbook: {playbook_id}")
        if target:
            print(f"[\033[94m*\033[0m] Target: {target}")
        
        success = self.framework.run_playbook(playbook_id, target=target)
        
        if success:
            print(f"[\033[92m+\033[0m] Playbook execution completed")
        else:
            print(f"[!] Playbook execution failed")
    
    def _cmd_sessions(self, args):
        """List active sessions"""
        sessions = self.framework.session_manager.get_all_sessions()
        
        if sessions:
            print(f"\nActive Sessions ({len(sessions)}):")
            for i, session in enumerate(sessions, 1):
                print(f"  {i}. ID: {session.get('id', 'N/A')}")
                print(f"     Type: {session.get('type', 'N/A')}")
                print(f"     Target: {session.get('target', 'N/A')}")
                print(f"     Status: {session.get('status', 'N/A')}")
                print()
        else:
            print("[!] No active sessions")
    
    def _cmd_ai(self, args):
        """AI-assisted operations"""
        sub_args = args.split(maxsplit=2)
        if not sub_args:
            print("[!] Usage: ai <plan|analyze> <args>")
            return
        
        action = sub_args[0].lower()
        
        if action == 'plan':
            if len(sub_args) < 3:
                print("[!] Usage: ai plan <target> <objective>")
                return
            
            target = sub_args[1]
            objective = sub_args[2]
            
            print(f"[\033[94m*\033[0m] AI is planning attack strategy...")
            print(f"     Target: {target}")
            print(f"     Objective: {objective}")
            
            try:
                plan = asyncio.run(self.framework.ai_engine.plan_attack(target, objective))
                print(f"\n[\033[92m+\033[0m] AI Attack Plan:")
                for i, step in enumerate(plan, 1):
                    print(f"  {i}. {step.get('module', 'N/A')} - {step.get('description', 'N/A')}")
            except Exception as e:
                print(f"[!] AI planning failed: {e}")
        
        elif action == 'analyze':
            if len(sub_args) < 2:
                print("[!] Usage: ai analyze <data>")
                return
            
            data = sub_args[1]
            print(f"[\033[94m*\033[0m] Analyzing data with AI...")
            # Implement AI analysis
            print("[!] AI analysis not yet implemented")
        
        else:
            print("[!] Usage: ai <plan|analyze> <args>")
    
    def _cmd_plan(self, args):
        """Quick access to AI planning"""
        self._cmd_ai(f"plan {args}")
    
    def _cmd_workspace(self, args):
        """Manage workspaces"""
        if not args:
            current = self.framework.workspace_manager.get_current_workspace()
            print(f"Current workspace: {current}")
            return
        
        # Switch workspace
        success = self.framework.workspace_manager.switch_workspace(args)
        if success:
            print(f"[\033[92m+\033[0m] Switched to workspace: {args}")
        else:
            print(f"[!] Failed to switch workspace")
    
    def _cmd_status(self, args):
        """Show framework status"""
        status = self.framework.get_status()
        
        print("\n=== NexusStrike Framework Status ===")
        print(f"Name:           {status['name']}")
        print(f"Version:        {status['version']}")
        print(f"Loaded Modules: {status['loaded_modules']}")
        print(f"Active Sessions: {status['active_sessions']}")
        print(f"Playbooks:      {status['playbooks_available']}")
        print(f"AI Engine:      {'Ready' if status['ai_engine_ready'] else 'Not Ready'}")
        print(f"Workspace:      {status['workspace']}")
        print("=" * 40)
    
    def _cmd_version(self, args):
        """Show version information"""
        print(f"NexusStrike Framework v{self.framework.version}")
        print("Advanced Purple Teaming Operations Platform")
    
    def _cmd_clear(self, args):
        """Clear screen"""
        import os
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def _cmd_history(self, args):
        """Show command history"""
        if PROMPT_TOOLKIT_AVAILABLE and hasattr(self.session, 'history'):
            history_items = list(self.session.history.get_strings())
            if history_items:
                print("\nCommand History:")
                for i, item in enumerate(history_items[-20:], 1):  # Last 20 commands
                    print(f"  {i}. {item}")
            else:
                print("[!] No command history")
        else:
            print("[!] Command history not available")
