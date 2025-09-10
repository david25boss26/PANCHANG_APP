# panchang.py

from typing import Union, Dict, List, Tuple
from skyfield.api import load, Topos
from skyfield import almanac
from skyfield.almanac import find_discrete
import datetime as dt
import math

# Load ephemeris & timescale once
_eph = load('de421.bsp')
_ts = load.timescale()

# Default location (Delhi)
DEFAULT_LAT = 28.61
DEFAULT_LON = 77.23

# ---- Name tables ----
_TITHI_NAMES = {
    1: "Pratipada", 2: "Dvitiya", 3: "Tritiya", 4: "Chaturthi", 
    5: "Panchami", 6: "Shashthi", 7: "Saptami", 8: "Ashtami", 
    9: "Navami", 10: "Dashami", 11: "Ekadashi", 12: "Dvadashi", 
    13: "Trayodashi", 14: "Chaturdashi", 15: "Purnima", 30: "Amavasya"
}

_NAKSHATRA_NAMES = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira",
    "Ardra", "Punarvasu", "Pushya", "Ashlesha", "Magha",
    "Purva Phalguni", "Uttara Phalguni", "Hasta", "Chitra", "Swati",
    "Vishakha", "Anuradha", "Jyeshtha", "Mula", "Purva Ashadha",
    "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha", 
    "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"
]

_YOGA_NAMES = [
    "Vishkambha", "Priti", "Ayushman", "Saubhagya", "Shobhana",
    "Atiganda", "Sukarma", "Dhriti", "Shoola", "Ganda",
    "Vriddhi", "Dhruva", "Vyaghata", "Harshana", "Vajra",
    "Siddhi", "Vyatipata", "Variyana", "Parigha", "Shiva",
    "Siddha", "Sadhya", "Shubha", "Shukla", "Brahma", 
    "Indra", "Vaidhriti"
]

_KARANA_NAMES = [
    "Bava", "Balava", "Kaulava", "Taitila", "Garaja", 
    "Vanija", "Vishti (Bhadra)", "Shakuni", "Chatushpada", 
    "Naga", "Kimstughna"
]

_WEEKDAYS = [
    "Sunday", "Monday", "Tuesday", "Wednesday", 
    "Thursday", "Friday", "Saturday"
]

def _parse_date(d: Union[str, dt.date, dt.datetime]) -> dt.date:
    """Parse various date formats to datetime.date"""
    if isinstance(d, dt.datetime):
        return d.date()
    if isinstance(d, dt.date):
        return d
    if isinstance(d, str):
        try:
            return dt.datetime.strptime(d, "%Y-%m-%d").date()
        except ValueError:
            raise ValueError("Date must be in 'YYYY-MM-DD' format")
    raise TypeError("Date must be string, datetime.date, or datetime.datetime")

def _get_sun_moon_longitudes(t, lat: float, lon: float) -> Tuple[float, float]:
    """Get apparent longitudes of Sun and Moon"""
    earth = _eph['earth']
    sun = _eph['sun']
    moon = _eph['moon']
    observer = earth + Topos(latitude_degrees=lat, longitude_degrees=lon)
    
    sun_app = observer.at(t).observe(sun).apparent()
    moon_app = observer.at(t).observe(moon).apparent()
    
    sun_lon = sun_app.ecliptic_latlon()[1].degrees % 360.0
    moon_lon = moon_app.ecliptic_latlon()[1].degrees % 360.0
    
    return sun_lon, moon_lon

def _calculate_tithi(sun_lon: float, moon_lon: float) -> Tuple[int, str, str]:
    """Calculate tithi with proper paksha determination"""
    diff = (moon_lon - sun_lon) % 360.0
    tithi_num = int(diff // 12.0) + 1
    
    if tithi_num > 30:
        tithi_num = 30
    
    paksha = "Shukla" if tithi_num <= 15 else "Krishna"
    
    if tithi_num == 15:
        tithi_name = "Purnima"
    elif tithi_num == 30:
        tithi_name = "Amavasya"
    else:
        tithi_num_in_paksha = tithi_num if tithi_num <= 15 else tithi_num - 15
        tithi_name = _TITHI_NAMES.get(tithi_num_in_paksha, f"Tithi {tithi_num_in_paksha}")
    
    return tithi_num, tithi_name, paksha

def _calculate_nakshatra(moon_lon: float) -> Tuple[int, str]:
    """Calculate nakshatra"""
    nakshatra_span = 360.0 / 27.0
    nakshatra_num = int(moon_lon // nakshatra_span) + 1
    if nakshatra_num > 27:
        nakshatra_num = 27
    nakshatra_name = _NAKSHATRA_NAMES[nakshatra_num - 1]
    return nakshatra_num, nakshatra_name

def _calculate_yoga(sun_lon: float, moon_lon: float) -> Tuple[int, str]:
    """Calculate yoga"""
    yoga_span = 360.0 / 27.0
    yoga_val = (sun_lon + moon_lon) % 360.0
    yoga_num = int(yoga_val // yoga_span) + 1
    if yoga_num > 27:
        yoga_num = 27
    yoga_name = _YOGA_NAMES[yoga_num - 1]
    return yoga_num, yoga_name

def _calculate_karana(sun_lon: float, moon_lon: float) -> Tuple[int, str]:
    """Calculate karana with proper sequence"""
    diff = (moon_lon - sun_lon) % 360.0
    karana_num = int(diff // 6.0) + 1
    
    # Handle the complex karana sequence
    if karana_num <= 7:
        karana_name = _KARANA_NAMES[karana_num - 1]
    elif karana_num <= 56:
        # For karanas 8-56, they follow a repeating pattern
        cycle_num = (karana_num - 8) % 7
        karana_name = _KARANA_NAMES[cycle_num]
    else:
        # Last 4 karanas are fixed
        karana_name = _KARANA_NAMES[karana_num - 57 + 7]
    
    return karana_num, karana_name

def get_sunrise_time(date: dt.date, lat: float, lon: float):
    """Get precise sunrise time for given date and location"""
    topos = Topos(latitude_degrees=lat, longitude_degrees=lon)
    t0 = _ts.utc(date.year, date.month, date.day, 0, 0)
    t1 = _ts.utc(date.year, date.month, date.day, 23, 59)
    
    f = almanac.sunrise_sunset(_eph, topos)
    times, events = find_discrete(t0, t1, f)
    
    for t, e in zip(times, events):
        if e:  # True indicates sunrise
            return t
    
    # Fallback for polar regions
    return _ts.utc(date.year, date.month, date.day, 6, 0)

def get_panchang(date: Union[str, dt.date, dt.datetime],
                 lat: float = DEFAULT_LAT,
                 lon: float = DEFAULT_LON) -> Dict:
    """Compute complete Panchang for the given date and location"""
    dt_date = _parse_date(date)
    sunrise_time = get_sunrise_time(dt_date, lat, lon)
    
    sun_lon, moon_lon = _get_sun_moon_longitudes(sunrise_time, lat, lon)
    
    # Calculate all components
    tithi_num, tithi_name, paksha = _calculate_tithi(sun_lon, moon_lon)
    nakshatra_num, nakshatra_name = _calculate_nakshatra(moon_lon)
    yoga_num, yoga_name = _calculate_yoga(sun_lon, moon_lon)
    karana_num, karana_name = _calculate_karana(sun_lon, moon_lon)
    
    # Get weekday
    weekday_num = dt_date.weekday()
    weekday_name = _WEEKDAYS[weekday_num]
    
    return {
        "date": dt_date.isoformat(),
        "sunrise": sunrise_time.utc_datetime().strftime("%Y-%m-%d %H:%M:%S UTC"),
        "tithi": {
            "number": tithi_num,
            "name": tithi_name,
            "paksha": paksha
        },
        "nakshatra": {
            "number": nakshatra_num,
            "name": nakshatra_name
        },
        "yoga": {
            "number": yoga_num,
            "name": yoga_name
        },
        "karana": {
            "number": karana_num,
            "name": karana_name
        },
        "vara": weekday_name,
        "longitudes": {
            "sun": round(sun_lon, 4),
            "moon": round(moon_lon, 4)
        }
    }

def get_tithi_start_end(date: dt.date, tithi_number: int, lat: float, lon: float) -> Tuple[dt.datetime, dt.datetime]:
    """Calculate when a specific tithi starts and ends"""
    # This is complex and requires finding when moon_lon - sun_lon crosses multiples of 12°
    # Implementation would involve scanning through the day to find exact transition times
    pass

# For festival detection, you'll need additional logic:
def detect_festivals(panchang_data: Dict, date: dt.date) -> List[str]:
    """Detect festivals based on panchang data"""
    festivals = []
    
    tithi = panchang_data["tithi"]
    nakshatra = panchang_data["nakshatra"]
    paksha = tithi["paksha"]
    tithi_num = tithi["number"]
    
    # Example festival logic (simplified)
    if tithi_num == 8 and paksha == "Krishna":
        festivals.append("Krishna Janmashtami")
    
    if tithi_num == 15 and paksha == "Shukla":
        festivals.append("Guru Purnima")
    
    # Diwali is more complex - it spans multiple days with specific conditions
    # This requires more sophisticated logic
    
    return festivals

# Make these functions available for festivals.py
def get_sun_moon_longitudes(t, lat, lon):
    """Get apparent longitudes of Sun and Moon"""
    earth = _eph['earth']
    sun = _eph['sun']
    moon = _eph['moon']
    observer = earth + Topos(latitude_degrees=lat, longitude_degrees=lon)
    
    sun_app = observer.at(t).observe(sun).apparent()
    moon_app = observer.at(t).observe(moon).apparent()
    
    sun_lon = sun_app.ecliptic_latlon()[1].degrees % 360.0
    moon_lon = moon_app.ecliptic_latlon()[1].degrees % 360.0
    
    return sun_lon, moon_lon

# Make the ephemeris available
def get_eph():
    return _eph

if __name__ == "__main__":
    # Test with known dates
    test_dates = [
        "2025-08-26",  # Regular day
        "2025-10-31",  # Diwali (check your calculations)
        "2025-09-22",  # Navratri start
        "2025-10-22"   # Another important date
    ]
    
    for test_date in test_dates:
        result = get_panchang(test_date)
        print(f"\n{test_date}:")
        print(f"Tithi: {result['tithi']['name']} ({result['tithi']['paksha']})")
        print(f"Nakshatra: {result['nakshatra']['name']}")
        print(f"Yoga: {result['yoga']['name']}")
        print(f"Karana: {result['karana']['name']}")