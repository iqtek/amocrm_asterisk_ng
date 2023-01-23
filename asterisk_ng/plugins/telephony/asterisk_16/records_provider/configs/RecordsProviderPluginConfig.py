from pydantic import BaseModel

from .MySqlConfig import MySqlConfig


__all__ = ["RecordsProviderPluginConfig"]


class RecordsProviderPluginConfig(BaseModel):
    mysql: MySqlConfig
    media_root: str = "/var/spool/asterisk/monitor/%Y/%m/%d/"
    cdr_table: str = "cdr"
    calldate_column: str = "calldate"
    recordingfile_column: str = "recordingfile"
