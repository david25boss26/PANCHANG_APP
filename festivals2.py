# festivals.py

from datetime import datetime, timedelta
from panchang2 import get_panchang, get_sun_moon_longitudes, _ts, _eph
from skyfield import almanac
from skyfield.almanac import find_discrete
from skyfield.api import Topos

'''def _get_hindu_month(date, lat, lon):
    """Hindu month calculation with seasonal adjustment"""
    dt_date = datetime.strptime(date, "%Y-%m-%d").date()
    t = get_sunrise_time(dt_date, lat, lon)
    sun_lon, _ = get_sun_moon_longitudes(t, lat, lon)
    
    sun_lon_normalized = sun_lon % 360
    zodiac_sign = int(sun_lon_normalized // 30)
    
    # Check if we're in the first or second half of the solar year
    # (approximately April-September vs October-March)
    is_second_half = (dt_date.month <3 or dt_date.month >= 9)
    
    if is_second_half:
        # Use mapping for second half of year (matches your second mapping)
        hindu_months = [
            "Vaisakha", "Jyeshtha", "Ashadha", "Shravana", 
            "Bhadrapada", "Ashwin", "Kartika", "Margashirsha",
            "Pausha", "Magha", "Phalguna", "Chaitra"
        ]
    else:
        # Use mapping for first half of year (matches your first mapping)  
        hindu_months = [
            "Chaitra", "Vaisakha", "Jyeshtha", "Ashadha",
            "Shravana", "Bhadrapada", "Ashwin", "Kartika",
            "Margashirsha", "Pausha", "Magha", "Phalguna"
        ]
    
    return hindu_months[zodiac_sign]'''

def _find_previous_new_moon(t, lat, lon):
    """Find the time of the previous New Moon (Amavasya) using astronomical calculations"""
    from skyfield.almanac import find_discrete
    
    earth = _eph['earth']
    sun = _eph['sun']
    moon = _eph['moon']
    observer = earth + Topos(latitude_degrees=lat, longitude_degrees=lon)
    
    # Search backwards 35 days to find the last New Moon
    search_start = t.utc_datetime() - timedelta(days=35)
    t_start = _ts.utc(search_start.year, search_start.month, search_start.day)
    
    # Function to detect New Moon (Sun and Moon conjunction)
    def is_new_moon(t):
        sun_app = observer.at(t).observe(sun).apparent()
        moon_app = observer.at(t).observe(moon).apparent()
        sun_lon = sun_app.ecliptic_latlon()[1].degrees
        moon_lon = moon_app.ecliptic_latlon()[1].degrees
        separation = abs((moon_lon - sun_lon) % 360)
        return separation < 1.0  # Consider it New Moon if within 1 degree
    
    try:
        # Find all New Moons in the search period
        times, events = find_discrete(t_start, t, is_new_moon)
        
        if len(times) > 0:
            return times[-1]  # Return the most recent New Moon
        else:
            # Fallback: use Skyfield's built-in lunar phase calculation
            return _find_new_moon_fallback(t)
            
    except Exception as e:
        return _find_new_moon_fallback(t)

def _find_new_moon_fallback(t):
    """Fallback method to find New Moon using lunar phases"""
    from skyfield.almanac import lunar_phases
    
    # Search backwards for the last New Moon
    search_start = t.utc_datetime() - timedelta(days=35)
    t_start = _ts.utc(search_start.year, search_start.month, search_start.day)
    
    # Find lunar phase changes (0 = New Moon)
    phases = lunar_phases(_eph)
    times, phase_values = find_discrete(t_start, t, phases)
    
    # Find the most recent New Moon (phase = 0)
    for i in range(len(times)-1, -1, -1):
        if phase_values[i] == 0:  # New Moon
            return times[i]
    
    # Ultimate fallback: approximate 29.5 days cycle
    return _ts.utc(t.utc_datetime() - timedelta(days=15))
    
def _get_hindu_month(date, lat, lon):
    """Simplified but more reliable Hindu month calculation"""
    dt_date = datetime.strptime(date, "%Y-%m-%d").date()
    t = get_sunrise_time(dt_date, lat, lon)
    sun_lon, _ = get_sun_moon_longitudes(t, lat, lon)
    
    # Use the traditional mapping that actually works
    # Based on your testing, this mapping gives correct results:
    zodiac_sign = int((sun_lon % 360) // 30)
    
    hindu_months = [
        "Chaitra",    # Aries (0°)
        "Vaisakha",   # Taurus (30°)
        "Jyeshtha",   # Gemini (60°)
        "Ashadha",    # Cancer (90°)
        "Shravana",   # Leo (120°)
        "Bhadrapada", # Virgo (150°)
        "Ashwin",     # Libra (180°)
        "Kartika",    # Scorpio (210°)
        "Margashirsha", # Sagittarius (240°)
        "Pausha",     # Capricorn (270°)
        "Magha",      # Aquarius (300°)
        "Phalguna"    # Pisces (330°)
    ]
    
    return hindu_months[zodiac_sign]

def _is_amsavsya(tithi_data):
    """Check if it's Amavasya (new moon)"""
    return tithi_data["name"] == "Amavasya"

def _is_purnima(tithi_data):
    """Check if it's Purnima (full moon)"""
    return tithi_data["name"] == "Purnima"

def _is_krishna_ashtami(tithi_data):
    """Check if it's Krishna Paksha Ashtami"""
    return (tithi_data["name"] == "Ashtami" and 
            tithi_data["paksha"] == "Krishna")

def _is_shukla_chaturthi(tithi_data):
    """Check if it's Shukla Paksha Chaturthi"""
    return (tithi_data["name"] == "Chaturthi" and 
            tithi_data["paksha"] == "Shukla")

def get_festivals(date, panchang, lat=28.61, lon=77.23):
    """Get Hindu festivals for the given date and panchang data"""
    festivals = []
    
    tithi = panchang["tithi"]
    nakshatra = panchang["nakshatra"]["name"]
    hindu_month = _get_hindu_month(date, lat, lon)
    
    # DEBUG: Print all values
    print(f"DEBUG: Date={date}, Tithi={tithi['name']} {tithi['paksha']}, "
          f"Nakshatra={nakshatra}, HinduMonth={hindu_month}")
    
    # Janmashtami condition
    '''if (tithi["name"] == "Ashtami" and 
        tithi["paksha"] == "Krishna" and 
        hindu_month == "Bhadrapada" and 
        nakshatra == "Rohini"):
        print("DEBUG: Janmashtami condition MET")
        festivals.append("Krishna Janmashtami")
    else:
        print("DEBUG: Janmashtami condition NOT MET")'''
    
    # 🪔 Diwali - Amavasya in Kartika month
    if (_is_amsavsya(tithi) and hindu_month == "Kartika"):
        festivals.append("Diwali")
    
    # 🌌 Janmashtami - Krishna Ashtami in Bhadrapada with Rohini nakshatra
    if (_is_krishna_ashtami(tithi) and hindu_month == "Bhadrapada" and 
       nakshatra == "Rohini"):
       festivals.append("Krishna Janmashtami")
    
    # 🌈 Holi - Phalguna Purnima
    if (_is_purnima(tithi) and hindu_month == "Phalguna"):
        festivals.append("Holi")
    
    # 🪔 Karva Chauth - Krishna Chaturthi in Kartika
    if (tithi["name"] == "Chaturthi" and tithi["paksha"] == "Krishna" and 
        hindu_month == "Kartika"):
        festivals.append("Karva Chauth")
    
    # 🎇 Raksha Bandhan - Shravana Purnima
    if (_is_purnima(tithi) and hindu_month == "Shravana"):
        festivals.append("Raksha Bandhan")
    
    # 🙏 Ganesh Chaturthi - Shukla Chaturthi in Bhadrapada
    if (_is_shukla_chaturthi(tithi) and hindu_month == "Bhadrapada"):
        festivals.append("Ganesh Chaturthi")
    
    # 🕉️ Maha Shivratri - Krishna Chaturdashi in Phalguna
    if (tithi["name"] == "Chaturdashi" and tithi["paksha"] == "Krishna" and 
        hindu_month == "Phalguna"):
        festivals.append("Maha Shivratri")
    
    # 🪔 Navratri start - Shukla Pratipada in Ashwin
    if (tithi["name"] == "Pratipada" and tithi["paksha"] == "Shukla" and 
        hindu_month == "Ashwin"):
        festivals.append("Sharadiya Navratri Begins")
    
    # 🌺 Dussehra - Shukla Dashami in Ashwin
    if (tithi["name"] == "Dashami" and tithi["paksha"] == "Shukla" and 
        hindu_month == "Ashwin"):
        festivals.append("Dussehra / Vijayadashami")
    
    # 🎆 Makar Sankranti - Sun enters Capricorn (approx Jan 14-15)
    dt_date = datetime.strptime(date, "%Y-%m-%d").date()
    if (dt_date.month == 1 and dt_date.day in [14, 15]):
        festivals.append("Makar Sankranti")
    
    # 🌼 Ram Navami - Shukla Navami in Chaitra
    if (tithi["name"] == "Navami" and tithi["paksha"] == "Shukla" and 
        hindu_month == "Chaitra"):
        festivals.append("Ram Navami")
    
    # 🪔 Chhath Puja - Shukla Shashthi in Kartika
    if (tithi["name"] == "Shashthi" and tithi["paksha"] == "Shukla" and 
        hindu_month == "Kartika"):
        festivals.append("Chhath Puja")
    
    return festivals

# Helper function to get sunrise time (needed for Hindu month calculation)
def get_sunrise_time(dt_date, lat, lon):
    """Get sunrise time for a date"""
    from skyfield.api import Topos
    
    topos = Topos(latitude_degrees=lat, longitude_degrees=lon)
    t0 = _ts.utc(dt_date.year, dt_date.month, dt_date.day, 0, 0)
    t1 = _ts.utc(dt_date.year, dt_date.month, dt_date.day, 23, 59)
    
    f = almanac.sunrise_sunset(_eph, topos)
    times, events = find_discrete(t0, t1, f)
    
    for t, e in zip(times, events):
        if e:  # True indicates sunrise
            return t
    
    # Fallback for polar regions
    return _ts.utc(dt_date.year, dt_date.month, dt_date.day, 6, 0)