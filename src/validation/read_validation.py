import yaml
import logging

from pathlib import Path
from typing import Dict, Any

from .validation_env import validation_env
from .validation import validation

logging.basicConfig(level=logging.INFO, format='%(levelname)s-%(asctime)s-%(message)s')
logger= logging.getLogger(__name__)

def read_yaml() -> Dict[str, Any]: 
    file= Path(__file__).resolve().parent.parent.parent / 'config' / 'config.yaml'
    
    try: 
        with open(file, 'r') as c: 
            readed= yaml.safe_load(c)
            logging.info('The YAML file was read correctly')
        
        config= validation(
            config_val=readed, 
            env_val=validation_env()
        )
        logger.info('Configuration validation was successful')
    except Exception as e: 
        logger.error(f'An error occurred in the YAML file: {e}')
        raise ValueError(f'An error occurred in the YAML file: {e}')
    
    return config

