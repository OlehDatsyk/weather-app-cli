"""
weather_service.py

Encapsulates all communication with the OpenWeatherMap API and defines
the data model used to represent a weather report.
"""

from __future__ import annotations

from dataclasses import dataclass

import requests

from config import Settings
from utils import degrees_to_compass, format_last_updated, unix_to_local_time


class WeatherServiceError(Exception):
    """Base exception for all weather-service-related failures."""


class CityNotFoundError(WeatherServiceError):
    """Raised when the API cannot find the requested city."""


class AuthenticationError(WeatherServiceError):
    """Raised when the API rejects the configured API key."""


class RateLimitError(WeatherServiceError):
    """Raised when the API reports that the rate limit has been exceeded."""


class NetworkError(WeatherServiceError):
    """Raised when a network-level failure prevents reaching the API."""


class ApiResponseError(WeatherServiceError):
    """Raised when the API returns an unexpected or malformed response."""


@dataclass(frozen=True, slots=True)
class WeatherReport:
    """A structured, display-ready weather report for a single city."""

    city: str
    country: str
    temperature: float
    feels_like: float
    temp_min: float
    temp_max: float
    humidity: int
    pressure: int
    wind_speed: float
    wind_direction: str
    description: str
    sunrise: str
    sunset: str
    last_updated: str
    units_symbol: str


class WeatherService:
    """Client responsible for fetching and parsing weather data."""

    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._temp_symbol = "°C" if settings.units == "metric" else (
            "°F" if settings.units == "imperial" else "K"
        )
        self._speed_symbol = "m/s" if settings.units != "imperial" else "mph"

    def get_weather(self, city: str) -> WeatherReport:
        """
        Fetch and parse current weather data for the given city.

        Args:
            city: A validated city name.

        Returns:
            A populated WeatherReport instance.

        Raises:
            CityNotFoundError: If the API cannot find the city.
            AuthenticationError: If the API key is invalid.
            RateLimitError: If the API rate limit has been exceeded.
            NetworkError: If a connection/timeout error occurs.
            ApiResponseError: If the response cannot be parsed as expected.
        """
        payload = self._fetch_raw_data(city)
        return self._parse_response(payload)

    def _fetch_raw_data(self, city: str) -> dict:
        """Perform the HTTP request and translate transport errors."""
        params = {
            "q": city,
            "appid": self._settings.api_key,
            "units": self._settings.units,
        }

        try:
            response = requests.get(
                self._settings.base_url,
                params=params,
                timeout=self._settings.request_timeout,
            )
        except requests.exceptions.Timeout as exc:
            raise NetworkError(
                "The request timed out while contacting the weather service."
            ) from exc
        except requests.exceptions.ConnectionError as exc:
            raise NetworkError(
                "Could not connect to the weather service. "
                "Check your internet connection."
            ) from exc
        except requests.exceptions.RequestException as exc:
            raise NetworkError(f"An unexpected network error occurred: {exc}") from exc

        return self._handle_status_code(response)

    def _handle_status_code(self, response: requests.Response) -> dict:
        """Map HTTP status codes to domain-specific exceptions."""
        if response.status_code == 200:
            try:
                return response.json()
            except ValueError as exc:
                raise ApiResponseError(
                    "The weather service returned an unreadable response."
                ) from exc

        if response.status_code == 404:
            raise CityNotFoundError(
                "City not found. Please check the spelling and try again."
            )

        if response.status_code == 401:
            raise AuthenticationError(
                "Invalid API key. Verify OPENWEATHER_API_KEY in your .env file."
            )

        if response.status_code == 429:
            raise RateLimitError(
                "API rate limit exceeded. Please wait before trying again."
            )

        raise ApiResponseError(
            f"Weather service returned an unexpected status code: "
            f"{response.status_code}"
        )

    def _parse_response(self, data: dict) -> WeatherReport:
        """Convert a raw JSON payload into a WeatherReport."""
        try:
            main = data["main"]
            wind = data.get("wind", {})
            sys_info = data["sys"]
            weather_list = data["weather"]
            tz_offset = data.get("timezone", 0)

            if not weather_list:
                raise ApiResponseError("Weather description missing from response.")

            description = weather_list[0].get("description", "unknown").capitalize()

            return WeatherReport(
                city=data.get("name", "Unknown"),
                country=sys_info.get("country", "N/A"),
                temperature=main["temp"],
                feels_like=main["feels_like"],
                temp_min=main["temp_min"],
                temp_max=main["temp_max"],
                humidity=main["humidity"],
                pressure=main["pressure"],
                wind_speed=wind.get("speed", 0.0),
                wind_direction=degrees_to_compass(wind.get("deg", 0)),
                description=description,
                sunrise=unix_to_local_time(sys_info["sunrise"], tz_offset),
                sunset=unix_to_local_time(sys_info["sunset"], tz_offset),
                last_updated=format_last_updated(tz_offset),
                units_symbol=self._temp_symbol,
            )
        except KeyError as exc:
            raise ApiResponseError(
                f"Missing expected field in API response: {exc}"
            ) from exc

    @property
    def speed_symbol(self) -> str:
        """Unit symbol used for wind speed (depends on configured units)."""
        return self._speed_symbol
