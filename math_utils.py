from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from vli.config import load_config
from vli.open_meteo import OpenMeteoRequest, fetch_forecast
from vli.report import render_markdown
from vli.scoring import compute_index
from vli.store import save_json, save_text


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="config/locations.json")
    parser.add_argument("--date", default=None, help="Target date YYYY-MM-DD. Default: today in local runtime timezone.")
    args = parser.parse_args()

    cfg = load_config(args.config)
    target_date = datetime.fromisoformat(args.date).date() if args.date else datetime.now().date()

    open_meteo_cfg = cfg.raw.get("data_sources", {}).get("open_meteo", {})
    include_pressure = bool(open_meteo_cfg.get("include_pressure_levels", False))

    for location in cfg.locations:
        req = OpenMeteoRequest(
            latitude=location.latitude,
            longitude=location.longitude,
            timezone=cfg.timezone,
            include_pressure_levels=include_pressure,
        )
        forecast = fetch_forecast(req)
        result = compute_index(
            forecast_data=forecast,
            location=location,
            target_date=target_date,
            window=cfg.forecast_window,
            settings=cfg.sector_settings,
        )

        base = f"{target_date.isoformat()}_{location.id}"
        out_json = PROJECT_ROOT / "data" / "forecasts" / f"{base}.json"
        out_md = PROJECT_ROOT / "data" / "forecasts" / f"{base}.md"

        save_json(out_json, result)
        save_text(out_md, render_markdown(result))

        print(f"Saved {out_json}")
        print(f"Saved {out_md}")


if __name__ == "__main__":
    main()
