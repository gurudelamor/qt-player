from pathlib import Path
import yaml


class ReadConfigs:
    def __init__(self, file_config:str=None):
        self.__cnf_ReadConfigs()
        self.DEFAULT_PATH = file_config \
            if file_config else 'sin_orden/config_sinergia.yml'
        self._load_config(self.DEFAULT_PATH)

    def __cnf_ReadConfigs(self):
        self.configs = None
        self.state = None

    def _load_config(self, path:str):
        """carga las configuraciones"""
        try:
            config_file = Path(path)
            self.state = '[ReadConfig]: config loaded.'
            if not config_file.exists():
                raise FileNotFoundError('[ReadConfig]: file no found.')
            with open(config_file, 'r', encoding='utf-8') as f:
                self.configs = yaml.safe_load(f)
        except FileNotFoundError as e:
            self.state = f'ERROR {e}'
        except yaml.YAMLError as e:
            self.state = f'ERROR[YML]: {e}'

    def get(self, key:str, default=None) -> str:
        """retorna valor de key"""
        current = self.configs
        for key in key.split('.'):
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                return default
        return current


if __name__ == "__main__":
    rc = ReadConfigs()
    print(rc.state)
    print(rc.get('formats'))
    print(rc.get('formats.video'))