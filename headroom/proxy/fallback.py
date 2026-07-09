import os
from typing import Tuple


def apply_global_fallback(request_headers: dict, body: dict, request_id: str) -> Tuple[dict, bool, str]:
    """
    Apply a global fallback rewrite to the request body when no upstream API key/header
    is present and a fallback provider is configured.

    Returns: (new_body, applied_flag, debug_msg)
    """
    hdrs = {k.lower(): v for k, v in (request_headers or {}).items()}

    # If user configured global fallback, prefer that. Backward compat with ANTHROPIC-specific env.
    fallback_provider = os.environ.get("HEADROOM_GLOBAL_FALLBACK") or os.environ.get(
        "HEADROOM_ANTHROPIC_FALLBACK", ""
    )
    fallback_model = os.environ.get("HEADROOM_GLOBAL_FALLBACK_MODEL") or os.environ.get(
        "HEADROOM_ANTHROPIC_FALLBACK_MODEL", ""
    )

    if not fallback_provider:
        return body, False, "no_fallback_configured"

    # Detect presence of auth headers. If any auth present, do not rewrite.
    auth_present = False
    if "authorization" in hdrs and hdrs["authorization"].strip():
        auth_present = True
    if "x-api-key" in hdrs and hdrs["x-api-key"].strip():
        auth_present = True

    if auth_present:
        return body, False, "auth_present"

    # No auth and fallback configured -> rewrite model
    model_name = body.get("model", "") or ""
    if "claude" in model_name.lower() and not fallback_model:
        # sensible default if user didn't set fallback_model
        mapped = f"{fallback_provider}/qwen2.5-coder:3b"
    elif fallback_model:
        mapped = fallback_model
    elif "/" in model_name:
        mapped = model_name
    else:
        mapped = f"{fallback_provider}/{model_name or 'qwen2.5-coder:3b'}"

    new_body = dict(body)
    new_body["model"] = mapped
    debug = f"rewrote model->{mapped} provider={fallback_provider}"
    return new_body, True, debug

