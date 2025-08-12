import json
from typing import Any, Callable, List
from ..constants import MASK_PLACEHOLDER

MAX_DEPTH = 8

sensitive_fields = [
    "password", "pass", "passwd", "pwd", "token", "access_token", "accessToken",
    "refresh_token", "refreshToken", "secret", "api_key", "apiKey", "authorization",
    "auth_token", "authToken", "jwt", "session_id", "sessionId", "sessionToken",
    "client_secret", "clientSecret", "private_key", "privateKey", "public_key", "publicKey",
    "key", "encryption_key", "encryptionKey", "credit_card", "creditCard", "card_number",
    "cardNumber", "cvv", "cvc", "ssn", "sin", "pin", "security_code", "securityCode",
    "bank_account", "bankAccount", "iban", "swift", "bic", "routing_number", "routingNumber",
    "license_key", "licenseKey", "otp", "mfa_code", "mfaCode", "phone_number", "phoneNumber",
    "email", "address", "dob", "tax_id", "taxId", "passport_number", "passportNumber",
    "driver_license", "driverLicense", "set-cookie", "cookie", "proxyAuthorization"
]

sensitive_headers = [
    "set-cookie", "cookie", "authorization", "proxyAuthorization"
]

def mask_all(value: Any, depth: int = 0) -> Any:
    if depth > MAX_DEPTH:
        return None

    if isinstance(value, list):
        return [mask_all(item, depth + 1) for item in value]

    if isinstance(value, dict):
        return {k: mask_all(v, depth + 1) for k, v in value.items()}

    if isinstance(value, str):
        return MASK_PLACEHOLDER

    return value

def mask_selected(value: Any, keys_to_mask: List[str]) -> Any:
    if isinstance(value, list):
        return [mask_selected(item, keys_to_mask) for item in value]

    if isinstance(value, dict):
        masked = {}
        keys_set = set(k.lower() for k in keys_to_mask)
        for k, v in value.items():
            if k.lower() in keys_set:
                masked[k] = MASK_PLACEHOLDER
            else:
                masked[k] = mask_selected(v, keys_to_mask)
        return masked

    return value

# --- Final masking function ---
def mask(keys_to_mask: List[str] = []) -> Callable[[Any, Any], str]:
    def apply_mask(value: Any, span: Any = None) -> str:
        try:
            parsed = json.loads(value) if isinstance(value, str) else value
        except Exception:
            parsed = value

        if keys_to_mask:
            masked = mask_selected(parsed, keys_to_mask)
        else:
            masked = mask_all(parsed)

        if not isinstance(masked, str):
            try:
                masked = json.dumps(masked)
            except Exception:
                masked = str(masked)

        return masked

    return apply_mask
