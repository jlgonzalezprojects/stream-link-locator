
from dynaconf import Dynaconf

settings = Dynaconf(
    envvar_prefix="STREAM",
    settings_files=['settings.yaml', '.secrets.yaml'],
)
