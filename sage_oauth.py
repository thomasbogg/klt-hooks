"""Sage One (Portugal) OAuth2 token exchange - the klt-hooks half of the connection klt-web's
staff/views.py::StaffSageConnectView and finance/services.py rely on (2026-09-09, per Thomas).

Deliberately just the initial code->token exchange, nothing else. The actual signed API client
(contact/invoice calls) and the ongoing token-refresh logic both live in klt-web
(libraries/accounting/sage.py) - that's a Django app with real test coverage, and this module
can't import that code anyway (separate deployables, same constraint postgres_bookings.py's own
docstring already documents for the rest of this file's imports). klt-hooks' only job here is
being a publicly-reachable HTTPS redirect target: klt-web only ever runs as 127.0.0.1 on someone's
own machine (see CLAUDE.md), so it can't itself be where Sage's OAuth server redirects back to.
"""
import requests

TOKEN_URL = 'https://api.sageone.com/oauth2/token'


def exchange_code_for_tokens(client_id: str, client_secret: str, code: str, redirect_uri: str) -> dict | None:
    """Returns Sage's raw token response dict (access_token/refresh_token/expires_in/...), or None
    on failure. redirect_uri must exactly match the one used in the original authorize request
    (klt-web's StaffSageConnectView) - Sage validates that, same as any standard OAuth2
    implementation. The code itself expires in 60 seconds per Sage's own docs - there's no retry
    window if this is called too late."""
    response = requests.post(TOKEN_URL, data={
        'client_id': client_id, 'client_secret': client_secret,
        'code': code, 'grant_type': 'authorization_code', 'redirect_uri': redirect_uri,
    })
    if response.status_code == 200:
        return response.json()
    return None
