from pydantic import BaseModel


__all__ = ["ConfiguratorConfig"]


class ConfiguratorConfig(BaseModel):
    config_path: str = "./config.yml"
    enable_saving: bool = False
    saved_config_path: str = "./saved_config.yml"
