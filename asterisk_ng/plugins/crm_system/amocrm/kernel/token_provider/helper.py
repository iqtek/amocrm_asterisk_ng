import typing as t
from uuid import UUID
from urllib.parse import urljoin, urlencode, urlparse, urlunparse


__all__ = [
    "generate_auth_url_for_connector",
    "generate_auth_url_for_authorizer",
]


def generate_auth_url_for_connector(
    state: str,
    mode: t.Literal['popup', 'post_message'],
    name: str,
    description: str,
    redirect_uri: str,
    secrets_uri: str,
    logo: str,
    scopes: t.List[str],
) -> str:
    query_params = {
        "state": state,
        "mode": mode,
        "name": name,
        "description": description,
        "redirect_uri": redirect_uri,
        "secrets_uri": secrets_uri,
        "logo": logo,
        "scopes": scopes,
    }
    return urlunparse(("https", "www.amocrm.ru", "/oauth", "", urlencode(query_params), ""))


def generate_auth_url_for_authorizer(
    integration_id: UUID,
    state: str,
    mode: t.Literal['popup', 'post_message'],
) -> str:
    query_params = {
        "client_id": str(integration_id),
        "state": state,
        "mode": mode,
    }
    return urlunparse(("https", "www.amocrm.ru", "/oauth", "", urlencode(query_params), ""))

# print(generate_auth_url_for_authorizer(UUID("fe0924a3-615e-4e15-b033-d7a92256cbb0"), "state", "popup", "origin"))
