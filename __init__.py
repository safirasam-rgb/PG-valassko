{
  "timezone": "Europe/Prague",
  "forecast_window": {
    "start_hour": 10,
    "end_hour": 17
  },
  "locations": [
    {
      "id": "valassko-vsetin",
      "name": "Valašsko / Vsetín",
      "latitude": 49.3387,
      "longitude": 17.9962,
      "elevation_m": 342,
      "notes": "Globální regionální bod. Pro pozdější verzi lze přidat více bodů: Javorníky, Beskydy, okolí Vsetína."
    }
  ],
  "sector_settings": {
    "allowed_spread_deg": 60,
    "ideal_spread_deg": 25,
    "ideal_wind_min_ms": 2.0,
    "ideal_wind_max_ms": 5.0,
    "strong_wind_ms": 8.0
  },
  "data_sources": {
    "open_meteo": {
      "enabled": true,
      "include_pressure_levels": false
    },
    "flymet": {
      "enabled": false,
      "mode": "stub",
      "notes": "Zapnout až po ověření, zda má Flymet legální a stabilní strojové rozhraní."
    }
  }
}