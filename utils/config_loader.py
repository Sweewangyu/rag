import yaml
from typing import Dict, Any


class ConfigLoader:
    def __init__(self, config_path: str):
        """
        Initialize config loader

        Args:
            config_path (str): Path to the config file
        """
        self.config_path = config_path
        self.config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """
        Load configuration from YAML file

        Returns:
            Dict[str, Any]: Configuration dictionary
        """
        with open(self.config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)

    def get_retriever_config(self, retriever_type: str) -> Dict[str, Any]:
        """
        Get configuration for specific retriever

        Args:
            retriever_type (str): Type of retriever (e.g., "faiss", "elasticsearch")

        Returns:
            Dict[str, Any]: Retriever configuration
        """
        if retriever_type not in self.config['retrievers']:
            raise ValueError(f"Retriever type {retriever_type} not found in config")
        return self.config['retrievers'][retriever_type]