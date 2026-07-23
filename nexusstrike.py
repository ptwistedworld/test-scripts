#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NexusStrike Framework - Advanced Purple Teaming Operations Platform
=====================================================================

A next-generation cybersecurity framework for purple team operations,
combining offensive capabilities with defensive intelligence.

Author: Security Team
License: MIT
Version: 1.0.0
"""

import os
import sys
import asyncio
import logging
from pathlib import Path
from typing import Optional, Dict, List, Any

# Add core to path
sys.path.insert(0, str(Path(__file__).parent))

# Import from stub managers first (will be replaced by KittySploit if available)
from core.stub_managers import WorkspaceManager, DatabaseManager, SessionManager
from core.interactive_shell import NexusStrikeShell
from core.module_loader import ModuleLoader
from core.playbook_manager import PlaybookManager
from core.ai_engine import AIEngine


class NexusStrikeFramework:
    """
    Main NexusStrike Framework Class
    
    Orchestrates all components for purple team operations including:
    - Module management and execution
    - AI-powered attack planning
    - Playbook orchestration
    - Session handling
    - Collaborative operations
    """
    
    version = "1.0.0"
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the NexusStrike Framework
        
        Args:
            config_path: Path to configuration file
        """
        self.name = "NexusStrike"
        self.config_path = config_path or self._default_config_path()
        
        # Setup logging
        self._setup_logging()
        self.logger = logging.getLogger('NexusStrike')
        self.logger.info(f"Initializing {self.name} Framework v{self.version}")
        
        # Initialize core components
        self.workspace_manager = WorkspaceManager()
        self.db_manager = DatabaseManager()
        self.module_loader = ModuleLoader()
        self.playbook_manager = PlaybookManager(self)
        self.ai_engine = AIEngine(self)
        self.session_manager = SessionManager(self)
        
        # State
        self.current_module = None
        self.active_sessions = []
        self.loaded_modules = {}
        
        # Initialize components
        self._initialize_components()
        
        self.logger.info(f"{self.name} Framework initialized successfully")
    
    def _default_config_path(self) -> str:
        """Get default configuration path"""
        return os.path.join(os.path.expanduser('~'), '.nexusstrike', 'config.yaml')
    
    def _setup_logging(self):
        """Configure logging"""
        log_dir = Path('logs')
        log_dir.mkdir(exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_dir / 'nexusstrike.log'),
                logging.StreamHandler(sys.stdout)
            ]
        )
    
    def _initialize_components(self):
        """Initialize all framework components"""
        try:
            # Load modules
            self.logger.info("Loading modules...")
            self.module_loader.discover_modules()
            
            # Initialize database
            self.db_manager.initialize()
            
            # Load playbooks
            self.playbook_manager.load_playbooks()
            
            self.logger.info(f"Loaded {len(self.loaded_modules)} modules")
            self.logger.info(f"Loaded {len(self.playbook_manager.playbooks)} playbooks")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize components: {e}")
            raise
    
    def load_module(self, module_path: str) -> bool:
        """
        Load a module by path
        
        Args:
            module_path: Path to the module
            
        Returns:
            bool: Success status
        """
        try:
            module = self.module_loader.load(module_path)
            if module:
                self.loaded_modules[module_path] = module
                self.current_module = module
                self.logger.info(f"Loaded module: {module_path}")
                return True
            return False
        except Exception as e:
            self.logger.error(f"Failed to load module {module_path}: {e}")
            return False
    
    def execute_module(self, module_path: str, options: Optional[Dict] = None) -> Any:
        """
        Execute a module
        
        Args:
            module_path: Path to the module
            options: Module options/parameters
            
        Returns:
            Execution results
        """
        if not self.load_module(module_path):
            return None
        
        module = self.loaded_modules[module_path]
        if options:
            module.set_options(options)
        
        return module.execute()
    
    def run_playbook(self, playbook_id: str, target: str = None) -> bool:
        """
        Execute a playbook
        
        Args:
            playbook_id: ID of the playbook to run
            target: Target for the playbook
            
        Returns:
            bool: Success status
        """
        return self.playbook_manager.execute(playbook_id, target=target)
    
    async def ai_plan_attack(self, target: str, objective: str) -> List[Dict]:
        """
        Use AI to plan an attack strategy
        
        Args:
            target: Target system/domain
            objective: Attack objective
            
        Returns:
            List of recommended modules/actions
        """
        return await self.ai_engine.plan_attack(target, objective)
    
    def start_console(self):
        """Start the interactive console"""
        shell = NexusStrikeShell(self)
        shell.run()
    
    def start_api_server(self, host: str = '0.0.0.0', port: int = 8080):
        """Start the REST API server"""
        from interfaces.api_server import APIServer
        api = APIServer(self, host, port)
        api.start()
    
    def get_status(self) -> Dict:
        """Get framework status"""
        return {
            'name': self.name,
            'version': self.version,
            'loaded_modules': len(self.loaded_modules),
            'active_sessions': len(self.active_sessions),
            'playbooks_available': len(self.playbook_manager.playbooks),
            'ai_engine_ready': self.ai_engine.is_ready(),
            'workspace': self.workspace_manager.get_current_workspace()
        }


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='NexusStrike - Advanced Purple Teaming Framework',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  nexusstrike                    Start interactive console
  nexusstrike --api              Start API server only
  nexusstrike --module exploits/http/rce_scanner --target example.com
  nexusstrike --playbook web-recon --target example.com
        """
    )
    
    parser.add_argument('--version', action='version', version=f'NexusStrike v{NexusStrikeFramework.version}')
    parser.add_argument('--config', help='Configuration file path')
    parser.add_argument('--api', action='store_true', help='Start API server')
    parser.add_argument('--api-host', default='0.0.0.0', help='API server host')
    parser.add_argument('--api-port', type=int, default=8080, help='API server port')
    parser.add_argument('--module', help='Module to execute')
    parser.add_argument('--playbook', help='Playbook to execute')
    parser.add_argument('--target', '-t', help='Target for module/playbook')
    parser.add_argument('--options', '-o', nargs='+', help='Module options (key=value)')
    parser.add_argument('--ai-plan', action='store_true', help='Use AI to plan attack')
    parser.add_argument('--objective', help='Attack objective for AI planning')
    
    args = parser.parse_args()
    
    # Initialize framework
    try:
        framework = NexusStrikeFramework(config_path=args.config)
        
        # Handle different modes
        if args.api:
            framework.start_api_server(host=args.api_host, port=args.api_port)
        elif args.module:
            options = {}
            if args.options:
                for opt in args.options:
                    if '=' in opt:
                        key, value = opt.split('=', 1)
                        options[key] = value
            
            if args.target:
                options['TARGET'] = args.target
            
            result = framework.execute_module(args.module, options)
            print(result)
        elif args.playbook:
            success = framework.run_playbook(args.playbook, target=args.target)
            sys.exit(0 if success else 1)
        elif args.ai_plan and args.target and args.objective:
            plan = asyncio.run(framework.ai_plan_attack(args.target, args.objective))
            print(plan)
        else:
            # Default: start interactive console
            framework.start_console()
            
    except KeyboardInterrupt:
        print("\n[!] Interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"[!] Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
