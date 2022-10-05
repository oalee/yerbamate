from yerbamate.mate_config import MateConfig
from .package import Package
from .package_repository import PackageRepository
from .metadata.generator import MetadataGenerator
from typing import Optional
import ipdb


"""
should install packages, update packages, remove packages, list packages, etc
"""


class PackageManager:
    def __init__(self, config: MateConfig):
        self.repository = PackageRepository(config)
        self.metadata_generator = MetadataGenerator(
            config.project, config.metadata, self.repository.local
        )

    def list(self, module: str, query: Optional[str] = None):
        return self.repository.list(module, query)

    """
    def query_models(self, query: Optional[str] = None):
        return self.remote.get_models(query)

    def query_trainers(self, query: str = None):
        return self.remote.get_trainers(query)

    def query_datasets(self, query: str = None):
        return self.remote.get_data_loaders(query)

    def install_model(self, model: Package):
        self.local.add_model(model)
    """
