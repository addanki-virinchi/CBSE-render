#!/usr/bin/env python3
"""
Render.com Configuration Handler
Handles configuration and credentials for deployment on Render.com
Supports both local development and Render deployment environments
"""

import os
import json
import logging

logger = logging.getLogger(__name__)

class RenderConfigHandler:
    """Handles configuration for both local and Render.com environments"""
    
    def __init__(self):
        self.is_render_deployment = self._detect_render_environment()
        self.config = self._load_config()
        self.credentials = self._load_credentials()
    
    def _detect_render_environment(self):
        """Detect if running on Render.com"""
        # Render.com sets specific environment variables
        render_indicators = [
            'RENDER',
            'RENDER_SERVICE_ID',
            'RENDER_SERVICE_NAME',
            'RENDER_EXTERNAL_URL'
        ]
        
        for indicator in render_indicators:
            if os.getenv(indicator):
                logger.info("🚀 Detected Render.com deployment environment")
                return True
        
        logger.info("🏠 Detected local development environment")
        return False
    
    def _load_config(self):
        """Load configuration from environment variables or local config.py"""
        config = {}
        
        if self.is_render_deployment:
            # Load from environment variables on Render
            config = {
                'MAX_STATES': self._get_env_int('MAX_STATES', None),
                'MAX_DISTRICTS_PER_STATE': self._get_env_int('MAX_DISTRICTS_PER_STATE', None),
                'WAIT_BETWEEN_STATES': self._get_env_int('WAIT_BETWEEN_STATES', 3),
                'WAIT_BETWEEN_DISTRICTS': self._get_env_int('WAIT_BETWEEN_DISTRICTS', 2),
                'WAIT_AFTER_SEARCH': self._get_env_int('WAIT_AFTER_SEARCH', 5),
                'WAIT_FOR_PAGE_LOAD': self._get_env_int('WAIT_FOR_PAGE_LOAD', 3),
                'OUTPUT_DIRECTORY': os.getenv('OUTPUT_DIRECTORY', 'output'),
                'BACKUP_FREQUENCY': self._get_env_int('BACKUP_FREQUENCY', 100),
                'IMPLICIT_WAIT': self._get_env_int('IMPLICIT_WAIT', 10),
                'EXPLICIT_WAIT': self._get_env_int('EXPLICIT_WAIT', 10),
                'PAGE_LOAD_TIMEOUT': self._get_env_int('PAGE_LOAD_TIMEOUT', 30),
                'BASE_URL': os.getenv('BASE_URL', 'https://udiseplus.gov.in/#/en/home'),
                'LOG_LEVEL': os.getenv('LOG_LEVEL', 'INFO'),
                'LOG_FORMAT': os.getenv('LOG_FORMAT', '%(asctime)s - %(levelname)s - %(message)s'),
                'MAX_RETRIES': self._get_env_int('MAX_RETRIES', 3),
                'RETRY_DELAY': self._get_env_int('RETRY_DELAY', 5),
                'HEADLESS': self._get_env_bool('HEADLESS', True),  # Always True on Render
                'WINDOW_SIZE': os.getenv('WINDOW_SIZE', '1920,1080'),
                'RENDER_DEPLOYMENT': True
            }
            logger.info("✅ Loaded configuration from environment variables")
        else:
            # Load from local config.py file
            try:
                import config as local_config
                config = {
                    'MAX_STATES': getattr(local_config, 'MAX_STATES', None),
                    'MAX_DISTRICTS_PER_STATE': getattr(local_config, 'MAX_DISTRICTS_PER_STATE', None),
                    'WAIT_BETWEEN_STATES': getattr(local_config, 'WAIT_BETWEEN_STATES', 3),
                    'WAIT_BETWEEN_DISTRICTS': getattr(local_config, 'WAIT_BETWEEN_DISTRICTS', 2),
                    'WAIT_AFTER_SEARCH': getattr(local_config, 'WAIT_AFTER_SEARCH', 5),
                    'WAIT_FOR_PAGE_LOAD': getattr(local_config, 'WAIT_FOR_PAGE_LOAD', 3),
                    'OUTPUT_DIRECTORY': getattr(local_config, 'OUTPUT_DIRECTORY', 'output'),
                    'BACKUP_FREQUENCY': getattr(local_config, 'BACKUP_FREQUENCY', 100),
                    'IMPLICIT_WAIT': getattr(local_config, 'IMPLICIT_WAIT', 10),
                    'EXPLICIT_WAIT': getattr(local_config, 'EXPLICIT_WAIT', 10),
                    'PAGE_LOAD_TIMEOUT': getattr(local_config, 'PAGE_LOAD_TIMEOUT', 30),
                    'BASE_URL': getattr(local_config, 'BASE_URL', 'https://udiseplus.gov.in/#/en/home'),
                    'LOG_LEVEL': getattr(local_config, 'LOG_LEVEL', 'INFO'),
                    'LOG_FORMAT': getattr(local_config, 'LOG_FORMAT', '%(asctime)s - %(levelname)s - %(message)s'),
                    'MAX_RETRIES': getattr(local_config, 'MAX_RETRIES', 3),
                    'RETRY_DELAY': getattr(local_config, 'RETRY_DELAY', 5),
                    'HEADLESS': getattr(local_config, 'HEADLESS', False),
                    'WINDOW_SIZE': getattr(local_config, 'WINDOW_SIZE', '1920,1080'),
                    'RENDER_DEPLOYMENT': getattr(local_config, 'RENDER_DEPLOYMENT', False)
                }
                logger.info("✅ Loaded configuration from local config.py")
            except ImportError:
                # Fallback configuration
                config = self._get_fallback_config()
                logger.warning("⚠️ Using fallback configuration")
        
        return config
    
    def _load_credentials(self):
        """Load Google Sheets credentials from environment or local file"""
        credentials = None
        
        if self.is_render_deployment:
            # Load from environment variable on Render
            creds_json = os.getenv('GOOGLE_CREDENTIALS_JSON')
            if creds_json:
                try:
                    credentials = json.loads(creds_json)
                    logger.info("✅ Loaded Google credentials from environment variable")
                except json.JSONDecodeError as e:
                    logger.error(f"❌ Failed to parse Google credentials JSON: {e}")
            else:
                logger.warning("⚠️ GOOGLE_CREDENTIALS_JSON environment variable not found")
        else:
            # Load from local credentials.json file
            try:
                with open('credentials.json', 'r') as f:
                    credentials = json.load(f)
                logger.info("✅ Loaded Google credentials from local credentials.json")
            except FileNotFoundError:
                logger.warning("⚠️ Local credentials.json file not found")
            except json.JSONDecodeError as e:
                logger.error(f"❌ Failed to parse local credentials.json: {e}")
        
        return credentials
    
    def _get_env_int(self, key, default):
        """Get integer value from environment variable"""
        value = os.getenv(key)
        if value is None:
            return default
        try:
            return int(value)
        except ValueError:
            logger.warning(f"⚠️ Invalid integer value for {key}: {value}, using default: {default}")
            return default
    
    def _get_env_bool(self, key, default):
        """Get boolean value from environment variable"""
        value = os.getenv(key)
        if value is None:
            return default
        return value.lower() in ('true', '1', 'yes', 'on')
    
    def _get_fallback_config(self):
        """Fallback configuration when no config file is available"""
        return {
            'MAX_STATES': None,
            'MAX_DISTRICTS_PER_STATE': None,
            'WAIT_BETWEEN_STATES': 3,
            'WAIT_BETWEEN_DISTRICTS': 2,
            'WAIT_AFTER_SEARCH': 5,
            'WAIT_FOR_PAGE_LOAD': 3,
            'OUTPUT_DIRECTORY': 'output',
            'BACKUP_FREQUENCY': 100,
            'IMPLICIT_WAIT': 10,
            'EXPLICIT_WAIT': 10,
            'PAGE_LOAD_TIMEOUT': 30,
            'BASE_URL': 'https://udiseplus.gov.in/#/en/home',
            'LOG_LEVEL': 'INFO',
            'LOG_FORMAT': '%(asctime)s - %(levelname)s - %(message)s',
            'MAX_RETRIES': 3,
            'RETRY_DELAY': 5,
            'HEADLESS': True,
            'WINDOW_SIZE': '1920,1080',
            'RENDER_DEPLOYMENT': True
        }
    
    def get_config(self, key, default=None):
        """Get configuration value"""
        return self.config.get(key, default)
    
    def get_credentials(self):
        """Get Google Sheets credentials"""
        return self.credentials
    
    def save_credentials_to_temp_file(self):
        """Save credentials to temporary file for Google Sheets API"""
        if not self.credentials:
            return None
        
        import tempfile
        temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
        json.dump(self.credentials, temp_file, indent=2)
        temp_file.close()
        
        logger.info(f"✅ Saved credentials to temporary file: {temp_file.name}")
        return temp_file.name

# Global instance
render_config = RenderConfigHandler()

# Backward compatibility - expose config values as module attributes
MAX_STATES = render_config.get_config('MAX_STATES')
MAX_DISTRICTS_PER_STATE = render_config.get_config('MAX_DISTRICTS_PER_STATE')
WAIT_BETWEEN_STATES = render_config.get_config('WAIT_BETWEEN_STATES')
WAIT_BETWEEN_DISTRICTS = render_config.get_config('WAIT_BETWEEN_DISTRICTS')
WAIT_AFTER_SEARCH = render_config.get_config('WAIT_AFTER_SEARCH')
WAIT_FOR_PAGE_LOAD = render_config.get_config('WAIT_FOR_PAGE_LOAD')
OUTPUT_DIRECTORY = render_config.get_config('OUTPUT_DIRECTORY')
BACKUP_FREQUENCY = render_config.get_config('BACKUP_FREQUENCY')
IMPLICIT_WAIT = render_config.get_config('IMPLICIT_WAIT')
EXPLICIT_WAIT = render_config.get_config('EXPLICIT_WAIT')
PAGE_LOAD_TIMEOUT = render_config.get_config('PAGE_LOAD_TIMEOUT')
BASE_URL = render_config.get_config('BASE_URL')
LOG_LEVEL = render_config.get_config('LOG_LEVEL')
LOG_FORMAT = render_config.get_config('LOG_FORMAT')
MAX_RETRIES = render_config.get_config('MAX_RETRIES')
RETRY_DELAY = render_config.get_config('RETRY_DELAY')
HEADLESS = render_config.get_config('HEADLESS')
WINDOW_SIZE = render_config.get_config('WINDOW_SIZE')
RENDER_DEPLOYMENT = render_config.get_config('RENDER_DEPLOYMENT')
