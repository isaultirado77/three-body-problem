import json
import yaml


def load_config(filepath: str):
    """Carga configuración desde archivo JSON o YAML."""
    if filepath.endswith('.json'): 
        with open(filepath, 'r') as f: 
            return json.load(f)
    elif filepath.endswith('.yaml'):
        with open(filepath, 'r') as f: 
            return yaml.safe_load(f)
    else: 
        raise ValueError("Formato de archivo no soportado. Use .json o .yaml")
    

def validate_config(config) -> dict:
    """Valida la estructura del archivo de configuración."""
    required_keys = ['masses', 'initial_positions', 'initial_velocities']
    for key in required_keys: 
        if key not in config: 
            raise ValueError(f"Falta clave requerida en la configuración: {key}")
    if len(config['masses']) != 3 or len(config['initial_positions']) != 3 or len(config['initial_velocities']) != 3:
        raise ValueError("Todos los arrays deben contener exactamente 3 elementos (3 cuerpos)")
    
    return {
        'masses': config['masses'],
        'initial_positions': config['initial_positions'],
        'initial_velocities': config['initial_velocities'],
        'dt': config.get('dt', 0.001),
        't_max': config.get('t_max', 10.0),
        'filename': config.get('filename', 'three_body_simulation'),
        'G': config.get('G', 6.67430e-11)
    }
