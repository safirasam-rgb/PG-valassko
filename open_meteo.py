from __future__ import annotations

import argparse
from datetime import datetime, timedelta
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from vli.config import load_config
from vli.open_meteo import OpenMeteoRequest, fetch_historical_actual
from vli.store import load_json, save_json, save_text
from vli.validation import compare_forecast_to_actual, render_validation_markdown, summarize_actual


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="config/locations.json")
    parser.add_argument("--date", default=None, help="Date to validate YYYY-MM-DD. Default: yesterday.")
    args = parser.parse_args()

    cfg = load_config(args.config)
    target_date = (
        datetime.fromisoformat(args.date).date()
        if args.date
        else (datetime.now().date() - timedelta(days=1))
    )

    for location in cfg.locations:
        base = f"{target_date.isoformat()}_{location.id}"
        forecast_path = PROJECT_ROOT / "data" / "forecasts" / f"{base}.json"

        if not forecast_path.exists():
            print(f"Forecast file not found, skipping: {forecast_path}")
            continue

        forecast = load_json(forecast_path)

        req = OpenMeteoRequest(
            latitude=location.latitude,
            longitude=location.longitude,
            timezone=cfg.timezone,
        )
        actual_data = fetch_historical_actual(req, target_date)
        actual_summary = summarize_actual(actual_data, target_date, cfg.forecast_window)

        validation = compare_forecast_to_actual(forecast, actual_summary)

        out_json = PROJECT_ROOT / "data" / "validation" / f"{base}_validation.json"
        out_md = PROJECT_ROOT / "data" / "validation" / f"{base}_validation.md"

        save_json(out_json, validation)
        save_text(out_md, render_validation_markdown(validation))

        print(f"Saved {out_json}")
        print(f"Saved {out_md}")


if __name__ == "__main__":
    main()
