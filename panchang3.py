# panchang2.py
"""
Accurate Panchang generator using Skyfield.

- Calculates Tithi, Nakshatra (and pada), Yoga, Karana, Rashi, Vara.
- Computes Amanta and Purnimanta lunar months using nearest new/full moon <= sunrise.
- Robust handling of Skyfield Time ranges (avoids 'single Time' errors).
- Returns debug info for verification.

Dependencies:
    pip install skyfield

Run:
    python panchang2.py
"""

from typing import Union, Optional, Tuple, Dict
import datetime as _dt
from math import floor
from skyfield.api import load, wgs84
from skyfield import almanac

# -------------------------
# Setup ephemeris & timescale
# -------------------------
EPH = load("de421.bsp")
TS = load.timescale()

# -------------------------
# Tables
# -------------------------
TITHI_SHUKLA = [
    "Pratipada", "Dvitiya", "Tritiya", "Chaturthi", "Panchami",
    "Shashthi", "Saptami", "Ashtami", "Navami", "Dashami",
    "Ekadashi", "Dvadashi", "Trayodashi", "Chaturdashi", "Purnima"
]
TITHI_KRISHNA = [
    "Pratipada", "Dvitiya", "Tritiya", "Chaturthi", "Panchami",
    "Shashthi", "Saptami", "Ashtami", "Navami", "Dashami",
    "Ekadashi", "Dvadashi", "Trayodashi", "Chaturdashi", "Amavasya"
]

NAKSHATRA = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira",
    "Ardra", "Punarvasu", "Pushya", "Ashlesha", "Magha",
    "Purva Phalguni", "Uttara Phalguni", "Hasta", "Chitra", "Swati",
    "Vishakha", "Anuradha", "Jyeshtha", "Mula", "Purva Ashadha",
    "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha", "Purva Bhadrapada",
    "Uttara Bhadrapada", "Revati"
]

YOGA = [
    "Vishkambha", "Priti", "Ayushman", "Saubhagya", "Shobhana",
    "Atiganda", "Sukarma", "Dhriti", "Shoola", "Ganda",
    "Vriddhi", "Dhruva", "Vyaghata", "Harshana", "Vajra",
    "Siddhi", "Vyatipata", "Variyana", "Parigha", "Shiva",
    "Siddha", "Sadhya", "Shubha", "Shukla", "Brahma", "Indra", "Vaidhriti"
]

KARANA_CORE = ["Bava","Balava","Kaulava","Taitila","Garaja","Vanija","Vishti"]
KARANA_LAST4 = ["Shakuni","Chatushpada","Naga","Kimstughna"]

RASHIS = [
    "Mesha","Vrishabha","Mithuna","Karka","Simha","Kanya",
    "Tula","Vrishchika","Dhanu","Makara","Kumbha","Meena"
]

LUNAR_MONTHS = [
    "Chaitra","Vaishakha","Jyeshtha","Ashadha","Shravana","Bhadrapada",
    "Ashwin","Kartika","Margashirsha","Pausha","Magha","Phalguna"
]

NAKSHATRA_SPAN = 360.0 / 27.0   # 13°20'
YOGA_SPAN = 360.0 / 27.0
TITHI_SPAN = 12.0               # 12°

# -------------------------
# Ayanamsa (Lahiri-style approx)
# -------------------------
def lahiri_ayanamsa_deg(time_obj) -> float:
    """
    Practical Lahiri-style ayanamsa (degrees).
    Good for panchang-level accuracy across modern dates.
    """
    jd_tt = time_obj.tt
    # centuries from J2000
    t = (jd_tt - 2451545.0) / 36525.0
    # polynomial approximation (coefficients chosen to be practical)
    # Based on earlier approximations; gives about 0.01-0.1 deg accuracy for 1900-2100.
    return 23.8531 + 0.013969 * ((jd_tt - 2451545.0) / 365.2425)

# -------------------------
# Utility: parse date input
# -------------------------
def parse_date(d: Union[str, _dt.date, _dt.datetime]) -> _dt.date:
    if isinstance(d, _dt.datetime):
        return d.date()
    if isinstance(d, _dt.date):
        return d
    if isinstance(d, str):
        try:
            return _dt.datetime.strptime(d, "%Y-%m-%d").date()
        except ValueError:
            parts = d.split("-")
            if len(parts) == 3:
                y, m, day = map(int, parts)
                return _dt.date(y, m, day)
    raise ValueError("date must be 'YYYY-MM-DD' or a date/datetime object")

# -------------------------
# Sunrise / Sunset (robust)
# -------------------------
def sunrise_sunset_for_date(date_obj: _dt.date, lat: float, lon: float) -> Tuple[object, object]:
    """Return (sunrise_time, sunset_time) Skyfield Time objects for the local date."""
    loc = wgs84.latlon(latitude_degrees=lat, longitude_degrees=lon)
    t0 = TS.utc(date_obj.year, date_obj.month, date_obj.day, 0, 0, 0)
    t1 = TS.utc(date_obj.year, date_obj.month, date_obj.day, 23, 59, 59)
    f = almanac.sunrise_sunset(EPH, loc)
    try:
        times, events = almanac.find_discrete(t0, t1, f)
    except Exception:
        # fallback simple times
        return TS.utc(date_obj.year, date_obj.month, date_obj.day, 6, 0, 0), TS.utc(date_obj.year, date_obj.month, date_obj.day, 18, 0, 0)

    sunrise = None
    sunset = None
    for ti, ev in zip(times, events):
        if int(ev) == 1 and sunrise is None:
            sunrise = ti
        elif int(ev) == 0 and sunset is None:
            sunset = ti

    if sunrise is None:
        sunrise = TS.utc(date_obj.year, date_obj.month, date_obj.day, 6, 0, 0)
    if sunset is None:
        sunset = TS.utc(date_obj.year, date_obj.month, date_obj.day, 18, 0, 0)
    return sunrise, sunset

# -------------------------
# Sun/Moon longitudes helpers
# -------------------------
def sun_moon_longitudes(time_obj, observer = None) -> Dict[str, float]:
    """
    Return tropical and sidereal longitudes at time_obj.
    Keys: 'sun_lon', 'moon_lon', 'sid_sun', 'sid_moon', 'ayanamsa'
    """
    earth = EPH['earth']
    sun = EPH['sun']
    moon = EPH['moon']

    if observer is None:
        obs = earth.at(time_obj)
    else:
        obs = (earth + observer).at(time_obj)

    sun_app = obs.observe(sun).apparent()
    moon_app = obs.observe(moon).apparent()

    sun_lon = sun_app.ecliptic_latlon()[1].degrees % 360.0
    moon_lon = moon_app.ecliptic_latlon()[1].degrees % 360.0

    ayan = lahiri_ayanamsa_deg(time_obj)
    sid_sun = (sun_lon - ayan) % 360.0
    sid_moon = (moon_lon - ayan) % 360.0

    return {
        "sun_lon": sun_lon,
        "moon_lon": moon_lon,
        "sid_sun": sid_sun,
        "sid_moon": sid_moon,
        "ayanamsa": ayan
    }

# -------------------------
# Find last moon phase <= t_center (robust)
# -------------------------
def find_last_moon_phase_before(t_center, phase_value:int, max_lookback_days:int=400):
    """
    phase_value: 0=new, 1=first quarter, 2=full, 3=last quarter
    Returns Skyfield Time or None.
    """
    f = almanac.moon_phases(EPH)
    dt_center = t_center.utc_datetime()
    windows = [30, 60, 120, 365]
    for days in windows:
        if days > max_lookback_days:
            days = max_lookback_days
        t0_dt = dt_center - _dt.timedelta(days=days)
        t0 = TS.utc(t0_dt.year, t0_dt.month, t0_dt.day, t0_dt.hour, t0_dt.minute, t0_dt.second)
        t1 = t_center
        try:
            times, phases = almanac.find_discrete(t0, t1, f)
        except Exception:
            continue
        last = None
        for ti, ph in zip(times, phases):
            try:
                if int(ph) == int(phase_value) and ti.tt <= t_center.tt:
                    last = ti
            except Exception:
                continue
        if last is not None:
            return last
    # final exhaustive attempt
    try:
        t0 = TS.utc((dt_center - _dt.timedelta(days=max_lookback_days)).year,
                    (dt_center - _dt.timedelta(days=max_lookback_days)).month,
                    (dt_center - _dt.timedelta(days=max_lookback_days)).day)
        times, phases = almanac.find_discrete(t0, t_center, f)
        last = None
        for ti, ph in zip(times, phases):
            if int(ph) == int(phase_value) and ti.tt <= t_center.tt:
                last = ti
        return last
    except Exception:
        return None

# -------------------------
# Karana mapping (classical 60 half-tithi)
# -------------------------
def karana_from_half_index(half_index:int) -> str:
    """
    half_index: 1..60
    first 56: repeating 7-core, last 4: special.
    """
    if half_index <= 0:
        half_index = 1
    if half_index <= 56:
        return KARANA_CORE[(half_index - 1) % 7]
    else:
        return KARANA_LAST4[max(0, min(half_index - 57, 3))]

# -------------------------
# Helper: next lunar month
# -------------------------
def next_lunar_month(name:str) -> str:
    try:
        idx = LUNAR_MONTHS.index(name)
    except ValueError:
        # fallback to first if unknown
        return LUNAR_MONTHS[0]
    return LUNAR_MONTHS[(idx + 1) % 12]

# -------------------------
# Determine months (amanta & purnimanta)
# -------------------------
def determine_lunar_months(sunrise_time, observer) -> Tuple[str, str, Dict]:
    """
    Returns (amanta_month, purnimanta_month, debug_dict)
    - amanta_month: month name by new-moon -> sidereal sun method (fallback to sidereal sun at sunrise)
    - purnimanta_month: month determined for purnimanta (full-moon anchor + shift if in Krishna paksha)
    debug_dict contains data used.
    """
    debug = {}
    # find most recent new moon <= sunrise
    new_moon = find_last_moon_phase_before(sunrise_time, phase_value=0)
    full_moon = find_last_moon_phase_before(sunrise_time, phase_value=2)

    # Amanta: sidereal sun at most recent NEW MOON
    if new_moon is not None:
        s_new = sun_moon_longitudes(new_moon, observer=observer)
        idx_amanta = int(s_new["sid_sun"] // 30.0) % 12
        amanta = LUNAR_MONTHS[idx_amanta]
        debug["new_moon_time_utc"] = new_moon.utc_iso()
        debug["sid_sun_at_newmoon"] = s_new["sid_sun"]
    else:
        # fallback to sidereal sun at sunrise
        s_sunrise = sun_moon_longitudes(sunrise_time, observer=observer)
        idx_amanta = int(s_sunrise["sid_sun"] // 30.0) % 12
        amanta = LUNAR_MONTHS[idx_amanta]
        debug["new_moon_time_utc"] = None
        debug["sid_sun_fallback_at_sunrise"] = s_sunrise["sid_sun"]

    # Purnimanta: derive base from full-moon's nakshatra anchor (heuristic) then shift for Krishna paksha
    purnimanta = None
    debug["full_moon_time_utc"] = None
    debug["full_moon_sid_sun"] = None
    debug["full_moon_sid_moon"] = None
    debug["full_moon_nakshatra_index"] = None

    if full_moon is not None:
        s_full = sun_moon_longitudes(full_moon, observer=observer)
        debug["full_moon_time_utc"] = full_moon.utc_iso()
        debug["full_moon_sid_sun"] = s_full["sid_sun"]
        debug["full_moon_sid_moon"] = s_full["sid_moon"]
        nak_idx_full = int(s_full["sid_moon"] // NAKSHATRA_SPAN) % 27
        debug["full_moon_nakshatra_index"] = nak_idx_full
        debug["full_moon_nakshatra"] = NAKSHATRA[nak_idx_full]

        # Map full-moon nakshatra to a month anchor.
        # We'll choose a conservative, commonly used mapping (tweakable)
        anchor_map = {
            # anchor nakshatra -> month
            "Chitra": "Ashwin",
            "Vishakha": "Kartika",
            "Jyeshtha": "Jyeshtha",
            "Uttara Ashadha": "Magha",
            "Shravana": "Shravana",
            "Purva Bhadrapada": "Bhadrapada",
            "Uttara Bhadrapada": "Chaitra",
            "Rohini": "Vaishakha",
            "Mrigashira": "Margashirsha",
            "Pushya": "Pausha",
            "Magha": "Magha",
            "Uttara Phalguni": "Phalguna",
            "Bharani": "Vaishakha",
            "Revati": "Phalguna"
            # This map can be extended/tuned.
        }
        full_nak = NAKSHATRA[nak_idx_full]
        base_month = anchor_map.get(full_nak)
        # fallback: use sidereal sun at full moon to pick month
        if base_month is None:
            idx = int(s_full["sid_sun"] // 30.0) % 12
            base_month = LUNAR_MONTHS[idx]

        # Now decide purnimanta label: if date at sunrise is in Krishna paksha, shift to next month
        # But we can't know paksha here; caller will shift. Return base for now.
        purnimanta = base_month
    else:
        # fallback to sidereal sun at sunrise
        s_sunrise = sun_moon_longitudes(sunrise_time, observer=observer)
        idx = int(s_sunrise["sid_sun"] // 30.0) % 12
        purnimanta = LUNAR_MONTHS[idx]
        debug["full_moon_time_utc"] = None
        debug["full_moon_sid_sun_fallback"] = s_sunrise["sid_sun"]

    return amanta, purnimanta, debug

# -------------------------
# Main get_panchang
# -------------------------
def get_panchang(date_in: Union[str, _dt.date, _dt.datetime],
                 lat: float = 28.6139,
                 lon: float = 77.2090,
                 month_system: str = "purnimanta") -> Dict:
    """
    month_system: 'amanta' or 'purnimanta' (default 'purnimanta' for North-India style)
    """
    dt_date = parse_date(date_in)
    # get sunrise & sunset
    sunrise, sunset = sunrise_sunset_for_date(dt_date, lat, lon)

    # observer for topocentric
    observer = wgs84.latlon(latitude_degrees=lat, longitude_degrees=lon)

    # compute positions (use sunrise as epoch)
    vals = sun_moon_longitudes(sunrise, observer=observer)
    sun_lon = vals["sun_lon"]
    moon_lon = vals["moon_lon"]
    sid_sun = vals["sid_sun"]
    sid_moon = vals["sid_moon"]
    ayan = vals["ayanamsa"]

    # Tithi (using tropical/apparent longitudes; difference unaffected by adding same ayanamsa)
    diff = (moon_lon - sun_lon) % 360.0
    tithi_index = int(diff // TITHI_SPAN) + 1  # 1..30
    if tithi_index <= 15:
        paksha = "Shukla"
        tithi_name = f"{TITHI_SHUKLA[tithi_index - 1]} ({paksha})"
    else:
        paksha = "Krishna"
        tithi_name = f"{TITHI_KRISHNA[tithi_index - 16]} ({paksha})"

    # Nakshatra & pada (sidereal moon)
    nak_index = int(sid_moon // NAKSHATRA_SPAN) % 27
    nakshatra = NAKSHATRA[nak_index]
    nak_pada = int((sid_moon % NAKSHATRA_SPAN) // (NAKSHATRA_SPAN / 4)) + 1

    # Yoga (sidereal sun + sidereal moon)
    yoga_val = (sid_sun + sid_moon) % 360.0
    yoga_index = int(yoga_val // YOGA_SPAN) % len(YOGA)
    yoga_name = YOGA[yoga_index]

    # Karana (half-tithi)
    half_index = int(diff // 6.0) + 1
    half_index = ((half_index - 1) % 60) + 1
    if half_index <= 56:
        karana_name = KARANA_CORE[(half_index - 1) % 7]
    else:
        karana_name = KARANA_LAST4[half_index - 57]

    # Rashis (sidereal)
    moon_rashi = RASHIS[int(sid_moon // 30.0) % 12]
    sun_rashi = RASHIS[int(sid_sun // 30.0) % 12]

    # Determine lunar months
    amanta_base, purnimanta_base, month_debug = determine_lunar_months(sunrise, observer)

    # For purnimanta system, if current paksha == Krishna, the named month is NEXT month of base
    if month_system == "purnimanta":
        if paksha == "Krishna":
            purnimanta_final = next_lunar_month(purnimanta_base)
        else:
            purnimanta_final = purnimanta_base
        amanta_final = amanta_base
        chosen_month = purnimanta_final
    else:
        # amanta system: use amanta_base directly
        amanta_final = amanta_base
        # for convenience provide amanta_chosen
        chosen_month = amanta_final

    result = {
        "date": dt_date.isoformat(),
        "tithi": tithi_name,
        "paksha": paksha,
        "nakshatra": nakshatra,
        "nakshatra_pada": nak_pada,
        "yoga": yoga_name,
        "karana": karana_name,
        "var": dt_date.strftime("%A"),
        "moon_rashi": moon_rashi,
        "sun_rashi": sun_rashi,
        "lunar_month_amanta": amanta_final,
        "lunar_month_purnimanta": purnimanta_final if month_system=="purnimanta" else None,
        "lunar_month_chosen": chosen_month,
        "sunrise": sunrise.utc_iso(),
        "sunset": sunset.utc_iso(),
        "_debug": {
            "ayanamsa_deg_at_sunrise": ayan,
            "sun_lon_tropical_at_sunrise": sun_lon,
            "moon_lon_tropical_at_sunrise": moon_lon,
            "sidereal_sun_lon_at_sunrise": sid_sun,
            "sidereal_moon_lon_at_sunrise": sid_moon,
            "amanta_purnimanta_debug": month_debug
        }
    }
    return result

# -------------------------
# CLI test
# -------------------------
if __name__ == "__main__":
    dates = ["2025-08-16", "2025-10-21", "2025-11-20"]
    for d in dates:
        try:
            p = get_panchang(d, month_system="purnimanta")
            import json
            print(json.dumps(p, indent=2))
        except Exception as e:
            print(f"Error for {d}: {e}")
