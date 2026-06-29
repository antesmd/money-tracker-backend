from __future__ import annotations

import secrets
import string
from dataclasses import dataclass, field
from typing import Any

import httpx


@dataclass
class AuthSession:
    email: str
    password: str
    username: str
    cookies: httpx.Cookies = field(default_factory=httpx.Cookies)
    account_id: str = "00000000-0000-0000-0000-000000000001"
    category_id: str = "00000000-0000-0000-0000-000000000002"
    transaction_id: str = "00000000-0000-0000-0000-000000000003"
    budget_id: str = "00000000-0000-0000-0000-000000000004"


def _random_suffix(length: int = 8) -> str:
    alphabet = string.ascii_lowercase + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(length))


class AuthClient:
    def __init__(self, client: httpx.Client, base_url: str, password: str, username_prefix: str) -> None:
        self._client = client
        self._base_url = base_url.rstrip("/")
        self._password = password
        self._username_prefix = username_prefix

    def create_session(self, *, email: str = "", password: str = "") -> AuthSession:
        suffix = _random_suffix()
        resolved_email = email or f"{self._username_prefix}_{suffix}@fuzz.test"
        resolved_password = password or self._password
        username = f"{self._username_prefix}_{suffix}"

        register_response = self._client.post(
            f"{self._base_url}/identity/users",
            json={
                "email": resolved_email,
                "username": username,
                "password": resolved_password,
            },
        )
        if register_response.status_code not in {204, 409}:
            register_response.raise_for_status()

        login_response = self._client.post(
            f"{self._base_url}/identity/auth",
            json={"email": resolved_email, "password": resolved_password},
        )
        login_response.raise_for_status()

        session = AuthSession(
            email=resolved_email,
            password=resolved_password,
            username=username,
            cookies=login_response.cookies,
        )
        self._seed_resources(session)
        return session

    def login_existing(self, email: str, password: str) -> AuthSession:
        login_response = self._client.post(
            f"{self._base_url}/identity/auth",
            json={"email": email, "password": password},
        )
        login_response.raise_for_status()
        session = AuthSession(email=email, password=password, username="", cookies=login_response.cookies)
        self._seed_resources(session)
        return session

    def _seed_resources(self, session: AuthSession) -> None:
        account = self._client.post(
            f"{self._base_url}/accounts/accounts",
            cookies=session.cookies,
            json={"name": "Fuzz Seed Account", "account_type": "cash", "initial_balance": "100.00"},
        )
        if account.status_code == 201:
            session.account_id = account.json()["account_id"]

        category = self._client.post(
            f"{self._base_url}/categories/categories",
            cookies=session.cookies,
            json={"name": "Fuzz Seed Category"},
        )
        if category.status_code == 201:
            session.category_id = category.json()["category_id"]

        transaction = self._client.post(
            f"{self._base_url}/transactions/transactions",
            cookies=session.cookies,
            json={
                "account_id": session.account_id,
                "category_id": session.category_id,
                "transaction_type": "expense",
                "amount": "10.00",
                "description": "Seed transaction",
                "date": "2025-01-01T12:00:00",
            },
        )
        if transaction.status_code == 201:
            session.transaction_id = transaction.json()["transaction_id"]

        budget = self._client.post(
            f"{self._base_url}/budgets/budgets",
            cookies=session.cookies,
            json={
                "category_id": session.category_id,
                "amount": "500.00",
                "period_start": "2025-01-01T00:00:00",
                "period_end": "2025-12-31T23:59:59",
            },
        )
        if budget.status_code == 201:
            session.budget_id = budget.json()["budget_id"]

    def template_context(self, session: AuthSession) -> dict[str, str]:
        return {
            "email": session.email,
            "password": session.password,
            "username": session.username,
            "account_id": session.account_id,
            "category_id": session.category_id,
            "transaction_id": session.transaction_id,
            "budget_id": session.budget_id,
        }

    def cookies_for(self, auth_mode: str, session: AuthSession) -> httpx.Cookies | None:
        if auth_mode == "none":
            return None
        if auth_mode == "access":
            return session.cookies
        if auth_mode == "refresh":
            refresh = session.cookies.get("refresh_token")
            if refresh is None:
                return None
            cookies = httpx.Cookies()
            cookies.set("refresh_token", refresh)
            return cookies
        return None

    def resolve_placeholders(self, value: Any, context: dict[str, str]) -> Any:
        if isinstance(value, str):
            result = value
            for key, replacement in context.items():
                result = result.replace(f"{{{{{key}}}}}", replacement)
            return result
        if isinstance(value, dict):
            return {key: self.resolve_placeholders(item, context) for key, item in value.items()}
        if isinstance(value, list):
            return [self.resolve_placeholders(item, context) for item in value]
        return value
