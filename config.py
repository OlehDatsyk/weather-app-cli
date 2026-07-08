"""
config.py

Centralized application configuration.
Loads and validates environment variables required to run the application.
"""

from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv

# Load variables from a .env file into the process environment, if present.
load_dotenv()


class ConfigError(Exception):
    """Raised when required configuration is missing or invalid."""


@dataclass(frozen=True, slots=True)
class Settings:
    """Immutable application settings."""

    api_key: str
    base_url: str = "https://api.openweathermap.org/data/2.5/weather"
    request_timeout: float = 10.0
    units: str = "metric"  # metric -> Celsius, m/s

    @staticmethod
    def load() -> "Settings":
        """
        Build a Settings instance from environment variables.

        Raises:
            ConfigError: If the required OPENWEATHER_API_KEY variable is missing.
        """
        api_key = os.getenv("OPENWEATHER_API_KEY", "").strip()
        if not api_key:
            raise ConfigError(
                "Missing OPENWEATHER_API_KEY. "
                "Create a .env file (see .env.example) and set your API key."
            )

        timeout_raw = os.getenv("REQUEST_TIMEOUT", "10")
        try:
            timeout = float(timeout_raw)
        except ValueError as exc:
            raise ConfigError(
                f"REQUEST_TIMEOUT must be a number, got: {timeout_raw!r}"
            ) from exc

        units = os.getenv("WEATHER_UNITS", "metric").strip().lower()
        if units not in {"metric", "imperial", "standard"}:
            raise ConfigError(
                "WEATHER_UNITS must be one of: metric, imperial, standard "
                f"(got: {units!r})"
            )

        return Settings(api_key=api_key, request_timeout=timeout, units=units)
