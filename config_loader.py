import json
import yaml


def load_config(filepath: str):
    """Carga configuración desde archivo JSON o YAML."""
    if filepath.endswith('.json'): 
        with open(filepath, 'r') as f: 
            return json.load(f)
    elif filepath.endswith('.yaml'):
        with open(filepath, 'r') as f: 
            return yaml.load(f, Loader=yaml.Loader)
    else: 
        raise ValueError("Formato de archivo no soportado. Use .json o .yaml")
    

def validate_config(config):
    """Valida la estructura del archivo de configuración y convierte tipos."""
    required_keys = ['masses', 'initial_positions', 'initial_velocities']
    for key in required_keys:
        if key not in config:
            raise ValueError(f"Falta clave requerida en configuración: {key}")
    
    # Conversión de tipos
    validated = {
        'masses': [float(m) for m in config['masses']],
        'initial_positions': [[float(x), float(y), float(z)] for x, y, z in config['initial_positions']],
        'initial_velocities': [[float(vx), float(vy), float(vz)] for vx, vy, vz in config['initial_velocities']],
        'dt': float(config.get('dt', 0.001)),
        't_max': float(config.get('t_max', 10.0)),
        'filename': str(config.get('filename', 'three_body_simulation')),
        'G': float(config.get('G', 6.67430e-11))
    }
    
    # Validación de dimensiones
    if len(validated['masses']) != 3 or len(validated['initial_positions']) != 3 or len(validated['initial_velocities']) != 3:
        raise ValueError("Todos los arrays deben contener exactamente 3 elementos (3 cuerpos)")
    
    return validated
