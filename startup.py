import yaml
from asterisk_amocrm.main import Integration


if __name__ == "__main__":

    with open('config.yml') as config_file:
        settings = yaml.safe_load(config_file)

    integration = Integration(settings=settings)
    integration.startup()
