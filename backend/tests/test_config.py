"""Tests for application settings."""

from app.core.config import Settings, get_settings


def test_get_settings_default() -> None:
    """Test loading default configuration."""
    settings = get_settings()
    assert isinstance(settings, Settings)
    assert settings.app_env in ("development", "test", "production")
    assert settings.log_level in ("INFO", "DEBUG", "WARNING", "ERROR")
    assert "postgresql://" in settings.database_url


def test_get_settings_cached() -> None:
    """Test that get_settings() returns the cached singleton."""
    s1 = get_settings()
    s2 = get_settings()
    assert s1 is s2
