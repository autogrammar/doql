"""Regression tests for generated authentication models."""
from __future__ import annotations

from doql.generators.api_gen.auth import gen_auth
from doql.parsers.models import DoqlSpec, Entity, EntityField


def _field(name: str) -> EntityField:
    return EntityField(name=name, type="string")


def test_domain_user_without_credentials_gets_separate_auth_model() -> None:
    spec = DoqlSpec(
        entities=[Entity(name="User", fields=[_field("name"), _field("email"), _field("role")])]
    )

    generated = gen_auth(spec)

    assert "class AuthUser(Base):" in generated
    assert '__tablename__ = "auth_users"' in generated
    assert "db.query(AuthUser)" in generated


def test_compatible_domain_user_is_reused_for_authentication() -> None:
    spec = DoqlSpec(
        entities=[
            Entity(
                name="User",
                fields=[
                    _field("username"),
                    _field("email"),
                    _field("hashed_password"),
                    _field("role"),
                ],
            )
        ]
    )

    generated = gen_auth(spec)

    assert "from models import User as AuthUser" in generated
    assert "class AuthUser(Base):" not in generated
