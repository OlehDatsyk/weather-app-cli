# Weather App CLI

A clean, well-structured command-line weather application built with Python 3.12+.
It fetches live weather data from the [OpenWeatherMap](https://openweathermap.org/api)
API and displays it in a nicely formatted terminal report using [Rich](https://github.com/Textualize/rich).

![Tech](https://img.shields.io/badge/Python-3.9+-blue) ![Tech](https://img.shields.io/badge/Flask-3.0-black) ![Tech](https://img.shields.io/badge/JavaScript-ES6-yellow)

---

## Project Structure

```
weather-app-cli/
│
├── main.py              # CLI entry point / user interaction loop
├── weather_service.py   # API client + WeatherReport data model
├── config.py            # Environment-based configuration (Settings)
├── utils.py             # Validation & formatting helpers
├── requirements.txt     # Python dependencies
├── .env.example          # Template for required environment variables
├── .gitignore
└── README.md
```

## Features

- Prompts for a city name and validates the input
- Fetches current weather conditions from OpenWeatherMap
- Displays: city, country, temperature, feels-like, min/max temperature,
  humidity, pressure, wind speed & direction, weather description,
  sunrise, sunset, and last-updated time
- Robust exception handling for invalid cities, bad API keys, rate limits,
  and network failures
- Formatted terminal output using Rich panels and tables

---

## 1. Installation Steps

**Prerequisites:** Python 3.12 or later installed on your machine.

```bash
# 1. Clone or copy the project, then move into it
cd weather-app-cli

# 2. (Recommended) Create and activate a virtual environment
python3 -m venv venv

# macOS / Linux
source venv/bin/activate

# Windows (PowerShell)
venv\Scripts\Activate.ps1

# 3. Copy the environment template and add your API key
cp .env.example .env
```

Then open `.env` and paste in your API key:

```
OPENWEATHER_API_KEY=your_actual_api_key_here
```

## 2. Required pip Commands

```bash
pip install -r requirements.txt
```

This installs:

| Package        | Purpose                                    |
|----------------|--------------------------------------------|
| `requests`     | HTTP calls to the weather API              |
| `python-dotenv`| Loads variables from `.env`                |
| `rich`         | Formatted terminal output (tables/panels)  |

## 3. How to Obtain an API Key

1. Go to [https://openweathermap.org/api](https://openweathermap.org/api)
2. Click **Sign Up** and create a free account (or **Sign In** if you have one)
3. Once logged in, go to your account menu → **My API Keys**
4. Copy the default key (or generate a new one)
5. Paste it into your `.env` file as `OPENWEATHER_API_KEY`

> **Note:** New API keys can take a few minutes up to a couple of hours to
> activate. If you get an authentication error immediately after creating
> a key, wait a bit and try again.

## 4. How to Run the Application

Once dependencies are installed and `.env` is configured:

```bash
python main.py
```

You'll be prompted to enter a city name. After each lookup, you can search
again or exit.

### Opening in Visual Studio Code

1. Open the `weather-app-cli` folder in VS Code (`File → Open Folder`)
2. Select the virtual environment's Python interpreter
   (`Ctrl+Shift+P` → **Python: Select Interpreter** → choose `venv`)
3. Open a terminal in VS Code (`` Ctrl+` ``) and run `python main.py`

## 5. Example Terminal Output

```
╭────────────────────────────────────────╮
│ Weather App CLI                        │
│ Powered by OpenWeatherMap              │
╰────────────────────────────────────────╯
Enter a city name: London

╭─── Weather Report — London, GB ─────────────────╮
│ City                  London                    │
│ Country               GB                        │
│ Temperature           15.2°C                    │
│ Feels Like            14.1°C                    │
│ Min Temperature       13.0°C                    │
│ Max Temperature       17.0°C                    │
│ Humidity              70%                       │
│ Pressure              1012 hPa                  │
│ Wind Speed            4.5 m/s                   │
│ Wind Direction        WSW                       │
│ Weather Description   Light rain                │
│ Sunrise               06:13:20                  │
│ Sunset                17:20:00                  │
│ Last Updated          2026-07-08 12:28:49       │
╰─────────────────────────────────────────────────╯

Look up another city? (y/n): n
Goodbye!
```

An invalid city produces a clear, friendly error instead of a stack trace:

```
Enter a city name: Xyzqqqq123

╭─────────────────────────────────────────╮
│ Not found: City not found. Please check │
│ the spelling and try again.             │
╰─────────────────────────────────────────╯
```

---

## Error Handling Summary

| Scenario                   | Behavior                                             |
|----------------------------|------------------------------------------------------|
| Empty / invalid city name  | Re-prompts the user with a validation message        |
| City not found (404)       | Friendly "not found" message, loop continues         |
| Invalid API key (401)      | Clear auth error, application exits                  |
| Rate limit exceeded (429)  | Friendly rate-limit message, loop continues          |
| Network / timeout errors   | Friendly network error message, loop continues       |
| Malformed API response     | Friendly parsing error message, loop continues       |

---

## Quick reference: Windows / PowerShell / VS Code

If you're on Windows and just want the exact command sequence to copy and
paste, use this section.

### First-time setup

```powershell
cd "path\to\weather-app-cli"

python -m venv venv
venv\Scripts\Activate.ps1
```

If activation fails with an execution-policy error, run this once, then
repeat the activate command:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
venv\Scripts\Activate.ps1
```

Your prompt should now start with `(venv)`. Then:

```powershell
pip install -r requirements.txt
pip show rich
copy .env.example .env
code .env
```

In the `.env` file that opens, fill in and **save**:

```
OPENWEATHER_API_KEY=<your real OpenWeatherMap key>
```

Make sure there is only **one** `OPENWEATHER_API_KEY=` line, and it is not
still the placeholder text `your_actual_api_key_here`.

Then run the app:

```powershell
python main.py
```

You'll be prompted to enter a city name in the terminal.

### Every time you come back later

```powershell
cd "path\to\weather-app-cli"
venv\Scripts\Activate.ps1
python main.py
```

### If you ever edit `.env`

`.env` is only read at startup, so changes won't apply automatically:

1. Click into the terminal.
2. If the app is running, press `Ctrl+C` to stop it (or let it exit
   naturally after answering `n` at the "Look up another city?" prompt).
3. Run `python main.py` again.

### Troubleshooting

**`source venv/bin/activate` not recognized**
That's macOS/Linux syntax. On Windows PowerShell use `venv\Scripts\Activate.ps1` instead.

**`No module named 'rich'` or similar import errors**
Confirm `(venv)` is shown in your prompt, then run `pip install -r requirements.txt` again — this error usually means `pip install` ran against a different Python than the one running `main.py`.

**Invalid auth error / 401 on lookup**
Your `.env` still has the placeholder text, has a duplicate `OPENWEATHER_API_KEY` line, or the key hasn't finished activating yet (can take up to a couple of hours after creating it). Double-check the key, save `.env`, and rerun `python main.py`.

**"City not found" (404)**
Check spelling. This is expected, friendly behavior, not a bug — the loop continues and re-prompts you.

**Rate limit exceeded (429)**
You've hit OpenWeatherMap's free-tier request limit. Wait a short while before searching again.

**Network / timeout errors**
Check your internet connection. The app shows a friendly message and lets you try again rather than crashing.

## License

This project is provided as-is for personal and educational use.
