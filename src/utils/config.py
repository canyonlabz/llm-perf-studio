import yaml
import os
import platform

def load_config():
    # Compute the repository root directory.
    # Assuming this file is at 'repo/src/utils/config.py', we go up two levels.
    # Compute the repository root directory.
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    
    # Platform-specific config mapping
    config_map = {
        'Darwin': 'config.mac.yaml',
        'Windows': 'config.windows.yaml'
    }

    system = platform.system()
    platform_config = config_map.get(system)
    
    # Use platform-specific config if it exists, otherwise fall back to config.yaml
    candidate_files = [platform_config, 'config.yaml'] if platform_config else ['config.yaml']
    
    for filename in candidate_files:
        config_path = os.path.join(repo_root, filename)
        if os.path.exists(config_path):
            with open(config_path, 'r') as file:
                try:
                    return yaml.safe_load(file)
                except yaml.YAMLError as e:
                    raise Exception(f"Error parsing '{filename}': {e}")
    
    raise FileNotFoundError("No valid configuration file found (checked platform-specific and default).")

# Uncomment the following lines if you want to use a specific config file
#def load_config():
#    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
#    config_file = os.path.join(repo_root, 'config.yaml')
#
#    if not os.path.exists(config_file):
#        raise FileNotFoundError(f"Configuration file '{config_file}' not found.")
#    
#    with open(config_file, 'r') as file:
#        try:
#            config = yaml.safe_load(file)
#        except yaml.YAMLError as e:
#            raise Exception(f"Error parsing the configuration file: {e}")
#    
#    return config

def load_jmeter_config():
    """
    Loads the JMeter configuration from 'jmeter_config.yaml' located at the root of the repository.
    Returns:
      - A dictionary with the JMeter configuration.
    """
    # Compute the repository root directory.
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    jmeter_config_file = os.path.join(repo_root, 'jmeter_config.yaml')

    if not os.path.exists(jmeter_config_file):
        raise FileNotFoundError(f"JMeter configuration file '{jmeter_config_file}' not found.")
    
    with open(jmeter_config_file, 'r') as file:
        try:
            jmeter_config = yaml.safe_load(file)
        except yaml.YAMLError as e:
            raise Exception(f"Error parsing the JMeter configuration file: {e}")
    
    return jmeter_config

if __name__ == '__main__':
    # For testing purposes, print both configurations.
    config = load_config()
    print("Loaded general configuration:")
    print(config)

    jmeter_config = load_jmeter_config()
    print("Loaded JMeter configuration:")
    print(jmeter_config)
