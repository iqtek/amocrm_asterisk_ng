import yaml

from amocrm_asterisk_ng.main import main


if __name__ == "__main__":
    with open('config.yml') as config_file:
        settings = yaml.safe_load(config_file)

    main(settings=settings)
