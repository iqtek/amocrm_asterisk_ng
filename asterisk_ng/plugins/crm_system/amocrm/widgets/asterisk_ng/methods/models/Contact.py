from pydantic import BaseModel


__all__ = ["Contact"]


class Contact(BaseModel):
    uuid: str
    name: str
    phone: str
