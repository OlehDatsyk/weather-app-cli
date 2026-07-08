"""
main.py

Entry point for the Weather App CLI.
Prompts the user for a city, fetches current weather data, and renders
a formatted report to the terminal using Rich.
"""

from __future__ import annotations

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from config import ConfigError, Settings
from utils import InvalidCityNameError, validate_city_name
from weather_service import (
    ApiResponseError,
    AuthenticationError,
    CityNotFoundError,
    NetworkError,
    RateLimitError,
    WeatherReport,
    WeatherService,
    WeatherServiceError,
)

console = Console()


def prompt_for_city() -> str:
    """Prompt the user for a city name and validate it."""
    while True:
        raw_input_value = console.input("[bold cyan]Enter a city name: [/bold cyan]")
        try:
            return validate_city_name(raw_input_value)
        except InvalidCityNameError as exc:
            console.print(f"[bold red]Invalid input:[/bold red] {exc}")


def render_weather_report(report: WeatherReport, wind_unit: str) -> None:
    """Render a WeatherReport as a formatted Rich table inside a panel."""
    table = Table(show_header=False, box=None, padding=(0, 1))
    table.add_column("Field", style="bold cyan", no_wrap=True)
    table.add_column("Value", style="white")

    rows = [
        ("City", report.city),
        ("Country", report.country),
        ("Temperature", f"{report.temperature:.1f}{report.units_symbol}"),
        ("Feels Like", f"{report.feels_like:.1f}{report.units_symbol}"),
        ("Min Temperature", f"{report.temp_min:.1f}{report.units_symbol}"),
        ("Max Temperature", f"{report.temp_max:.1f}{report.units_symbol}"),
        ("Humidity", f"{report.humidity}%"),
        ("Pressure", f"{report.pressure} hPa"),
        ("Wind Speed", f"{report.wind_speed} {wind_unit}"),
        ("Wind Direction", report.wind_direction),
        ("Weather Description", report.description),
        ("Sunrise", report.sunrise),
        ("Sunset", report.sunset),
        ("Last Updated", report.last_updated),
    ]

    for field, value in rows:
        table.add_row(field, str(value))

    panel = Panel(
        table,
        title=f"[bold green]Weather Report — {report.city}, {report.country}[/bold green]",
        border_style="green",
        expand=False,
    )
    console.print(panel)


def run() -> None:
    """Application main loop."""
    console.print(
        Panel(
            "[bold]Weather App CLI[/bold]\nPowered by OpenWeatherMap",
            border_style="blue",
            expand=False,
        )
    )

    try:
        settings = Settings.load()
    except ConfigError as exc:
        console.print(f"[bold red]Configuration error:[/bold red] {exc}")
        return

    service = WeatherService(settings)

    while True:
        city = prompt_for_city()

        try:
            with console.status("[bold cyan]Fetching weather data...[/bold cyan]"):
                report = service.get_weather(city)
            render_weather_report(report, service.speed_symbol)

        except CityNotFoundError as exc:
            console.print(f"[bold yellow]Not found:[/bold yellow] {exc}")
        except AuthenticationError as exc:
            console.print(f"[bold red]Authentication error:[/bold red] {exc}")
            break
        except RateLimitError as exc:
            console.print(f"[bold yellow]Rate limited:[/bold yellow] {exc}")
        except NetworkError as exc:
            console.print(f"[bold red]Network error:[/bold red] {exc}")
        except ApiResponseError as exc:
            console.print(f"[bold red]API error:[/bold red] {exc}")
        except WeatherServiceError as exc:
            console.print(f"[bold red]Unexpected error:[/bold red] {exc}")

        again = console.input(
            "\n[bold cyan]Look up another city? (y/n): [/bold cyan]"
        ).strip().lower()
        if again != "y":
            console.print("[bold blue]Goodbye![/bold blue]")
            break


if __name__ == "__main__":
    try:
        run()
    except KeyboardInterrupt:
        console.print("\n[bold blue]Interrupted. Goodbye![/bold blue]")
