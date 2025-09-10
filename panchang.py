# panchang.py

from typing import Union
from skyfield.api import load, Topos
from skyfield import almanac
import datetime as _dt

# Load ephemeris & timescale once
_eph = load('de421.bsp')
_ts = load.timescale()

# Default location (Delhi). You can change these or pass per-call.
DEFAULT_LAT = 28.61
DEFAULT_LON = 77.23

# ---- Name tables ----
_TITHI_SHUKLA = [
    "Pratipada", "Dvitiya", "Tritiya", "Chaturthi", "Panchami",
    "Shashthi", "Saptami", "Ashtami", "Navami", "Dashami",
    "Ekadashi", "Dvadashi", "Trayodashi", "Chaturdashi", "Purnima"
]
_TITHI_KRISHNA = [
    "Pratipada", "Dvitiya", "Tritiya", "Chaturthi", "Panchami",
    "Shashthi", "Saptami", "Ashtami", "Navami", "Dashami",
    "Ekadashi", "Dvadashi", "Trayodashi", "Chaturdashi", "Amavasya"
]
_NAKSHATRA = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira",
    "Ardra", "Punarvasu", "Pushya", "Ashlesha", "Magha",
    "Purva Phalguni", "Uttara Phalguni", "Hasta", "Chitra", "Swati",
    "Vishakha", "Anuradha", "Jyeshtha", "Mula", "Purva Ashadha",
    "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha", "Purva Bhadrapada",
    "Uttara Bhadrapada", "Revati"
]
_YOGA = [
    "Vishkambha","Priti","Ayushman","Saubhagya","Shobhana",
    "Atiganda","Sukarma","Dhriti","Shoola","Ganda",
    "Vriddhi","Dhruva","Vyaghata","Harshana","Vajra",
    "Siddhi","Vyatipata","Variyana","Parigha","Shiva",
    "Siddha","Sadhya","Shubha","Shukla","Brahma","Indra","Vaidhriti"
]
# Karana sequence is more complex in reality; using repeating set as a placeholder
_KARANA = ["Bava","Balava","Kaulava","Taitila","Garaja","Vanija","Vishti (Bhadra)","Shakuni","Chatushpada","Naga","Kimstughna"]

_NAKSHATRA_SPAN = 360.0 / 27.0  # 13°20'
_YOGA_SPAN = 360.0 / 27.0       # 13°20'

def _parse_date(d: Union[str, _dt.date, _dt.datetime]) -> _dt.date:
    if isinstance(d, _dt.datetime):
        return d.date()
    if isinstance(d, _dt.date):
        return d
    if isinstance(d, str):
        try:
            return _dt.datetime.strptime(d, "%Y-%m-%d").date()
        except ValueError as e:
            raise ValueError("date must be 'YYYY-MM-DD'") from e
    raise TypeError("date must be a str 'YYYY-MM-DD', datetime.date, or datetime.datetime")

def _sunrise_time(dt: _dt.date, lat: float, lon: float):
    """Return Skyfield Time at sunrise for given date and location.
       If not found (extreme latitudes), fall back to 06:00 UTC."""
    topos = Topos(latitude_degrees=lat, longitude_degrees=lon)
    t0 = _ts.utc(dt.year, dt.month, dt.day, 0, 0)
    t1 = _ts.utc(dt.year, dt.month, dt.day, 23, 59)
    f = almanac.sunrise_sunset(_eph, topos)
    times, events = almanac.find_discrete(t0, t1, f)
    for t, e in zip(times, events):
        if e:  # True => sunrise
            return t
    # Fallback: 06:00 UTC if a discrete sunrise wasn't returned
    return _ts.utc(dt.year, dt.month, dt.day, 6, 0)

def get_panchang(date: Union[str, _dt.date, _dt.datetime],
                 lat: float = DEFAULT_LAT,
                 lon: float = DEFAULT_LON):
    """Compute Panchang at sunrise for the given date and location."""
    dt = _parse_date(date)
    t = _sunrise_time(dt, lat, lon)

    earth = _eph['earth']
    sun = _eph['sun']
    moon = _eph['moon']
    observer = earth + Topos(latitude_degrees=lat, longitude_degrees=lon)

    sun_app = observer.at(t).observe(sun).apparent()
    moon_app = observer.at(t).observe(moon).apparent()

    sun_lon = sun_app.ecliptic_latlon()[1].degrees % 360.0
    moon_lon = moon_app.ecliptic_latlon()[1].degrees % 360.0

    # ---- Tithi (12° each) ----
    diff = (moon_lon - sun_lon) % 360.0
    tithi_num = int(diff // 12.0) + 1  # 1..30
    if tithi_num <= 15:
        tithi_name_base = _TITHI_SHUKLA[tithi_num - 1]
        tithi_name = f"{tithi_name_base} (Shukla)"
    else:
        tithi_name_base = _TITHI_KRISHNA[tithi_num - 16]
        tithi_name = f"{tithi_name_base} (Krishna)"

    # ---- Nakshatra (Moon lon) ----
    nakshatra_num = int(moon_lon // _NAKSHATRA_SPAN) + 1  # 1..27
    nakshatra_name = _NAKSHATRA[(nakshatra_num - 1) % 27]

    # ---- Yoga (Sun+Moon lon) ----
    yoga_val = (sun_lon + moon_lon) % 360.0
    yoga_num = int(yoga_val // _YOGA_SPAN) + 1  # 1..27
    yoga_name = _YOGA[(yoga_num - 1) % 27]

    # ---- Karana (6° each: placeholder repeating names) ----
    karana_num = int(diff // 6.0) + 1  # 1..60 in full system
    karana_name = _KARANA[(karana_num - 1) % len(_KARANA)]

    # ---- Vara (weekday) ----
    weekday = dt.strftime("%A")

    return {
        "date": dt.isoformat(),
        "tithi": tithi_name,
        "nakshatra": nakshatra_name,
        "yoga": yoga_name,
        "karana": karana_name,
        "var": weekday
    }

# Manual check:
if __name__ == "__main__":
    print(get_panchang("2025-08-26"))
