from dataclasses import dataclass
from typing import Any


@dataclass
class TradingCredentialOverrides:
    private_key: str | None = None
    deposit_wallet_address: str | None = None
    poly_api_key: str | None = None
    poly_api_secret: str | None = None
    poly_passphrase: str | None = None
    poly_builder_code: str | None = None
    clob_signature_type: int | None = None


def credentials_from_kwargs(**kwargs: Any) -> TradingCredentialOverrides | None:
    fields = {
        "private_key": kwargs.get("private_key"),
        "deposit_wallet_address": kwargs.get("deposit_wallet_address"),
        "poly_api_key": kwargs.get("poly_api_key"),
        "poly_api_secret": kwargs.get("poly_api_secret"),
        "poly_passphrase": kwargs.get("poly_passphrase"),
        "poly_builder_code": kwargs.get("poly_builder_code"),
        "clob_signature_type": kwargs.get("clob_signature_type"),
    }
    if not any(value is not None for value in fields.values()):
        return None
    return TradingCredentialOverrides(**fields)


def credential_headers(credentials: TradingCredentialOverrides | None) -> dict[str, str]:
    if credentials is None:
        return {}
    headers: dict[str, str] = {}
    mapping = {
        "private_key": "X-Poly-Private-Key",
        "deposit_wallet_address": "X-Poly-Deposit-Wallet-Address",
        "poly_api_key": "X-Poly-Api-Key",
        "poly_api_secret": "X-Poly-Api-Secret",
        "poly_passphrase": "X-Poly-Api-Passphrase",
        "poly_builder_code": "X-Poly-Builder-Code",
    }
    for field, header in mapping.items():
        value = getattr(credentials, field)
        if value:
            headers[header] = str(value)
    if credentials.clob_signature_type is not None:
        headers["X-Poly-Signature-Type"] = str(credentials.clob_signature_type)
    return headers
