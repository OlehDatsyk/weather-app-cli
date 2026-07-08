"""
utils.py

Small, reusable helper functions used across the application:
input validation and value formatting (timestamps, wind direction, etc.).
"""

from __future__ import annotations

from datetime import datetime, timezone


class InvalidCityNameError(ValueError):
    """Raised when the user-provided city name fails validation."""


def validate_city_name(raw_input: str) -> str:
    """
    Validate and normalize a city name entered by the user.

    Args:
        raw_input: The raw string typed by the user.

    Returns:
        A cleaned, whitespace-trimmed city name.

    Raises:
        InvalidCityNameError: If the input is empty or contains no
            alphabetic characters (e.g. only digits or symbols).
    """
    city = raw_input.strip()

    if not city:
        raise InvalidCityNameError("City name cannot be empty.")

    if len(city) < 2:
        raise InvalidCityNameError("City name is too short to be valid.")

    if not any(char.isalpha() for char in city):
        raise InvalidCityNameError(
            "City name must contain at least one letter."
        )

    allowed_extra = {" ", "-", "'", ".", ","}
    if not all(char.isalpha() or char in allowed_extra for char in city):
        raise InvalidCityNameError(
            "City name contains unsupported characters."
        )

    return city


def unix_to_local_time(timestamp: int, tz_offset_seconds: int) -> str:
    """
    Convert a UNIX timestamp (UTC) into a human-readable local time string,
    using the location's UTC offset returned by the weather API.

    Args:
        timestamp: UNIX timestamp in seconds (UTC).
        tz_offset_seconds: Offset from UTC, in seconds, for the target location.

    Returns:
        A formatted string, e.g. "06:12:45".
    """
    local_dt = datetime.fromtimestamp(
        timestamp + tz_offset_seconds, tz=timezone.utc
    )
    return local_dt.strftime("%H:%M:%S")


def degrees_to_compass(degrees: float) -> str:
    """
    Convert a wind direction in degrees to a 16-point compass direction.

    Args:
        degrees: Wind direction in degrees (0-360).

    Returns:
        A compass direction string, e.g. "NNE".
    """
    directions = [
        "N", "NNE", "NE", "ENE",
        "E", "ESE", "SE", "SSE",
        "S", "SSW", "SW", "WSW",
        "W", "WNW", "NW", "NNW",
    ]
    index = round(degrees / 22.5) % 16
    return directions[index]


def format_last_updated(tz_offset_seconds: int) -> str:
    """
    Produce a formatted "now" timestamp adjusted to the location's UTC offset,
    representing when the data was fetched/displayed.

    Args:
        tz_offset_seconds: Offset from UTC, in seconds, for the target location.

    Returns:
        A formatted string, e.g. "2025-01-15 06:12:45".
    """
    now_timestamp = int(datetime.now(tz=timezone.utc).timestamp())
    local_dt = datetime.fromtimestamp(
        now_timestamp + tz_offset_seconds, tz=timezone.utc
    )
    return local_dt.strftime("%Y-%m-%d %H:%M:%S")
