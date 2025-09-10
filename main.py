# main.py (updated)

from fastapi import FastAPI
from panchang2 import get_panchang
from festivals2 import get_festivals

app = FastAPI()

@app.get("/panchang")
def daily_panchang(date: str, lat: float = 28.61, lon: float = 77.23):
    try:
        p = get_panchang(date, lat, lon)
        if not isinstance(p, dict):
            return {"error": "get_panchang did not return a dict", "value": str(p)}
        p["festivals"] = get_festivals(date, p, lat, lon)
        return p
    except Exception as e:
        return {"error": str(e)}
    
@app.get("/debug/hindu_month")
def debug_hindu_month(date: str, lat: float = 28.61, lon: float = 77.23):
    from festivals import _get_hindu_month
    return {"date": date, "hindu_month": _get_hindu_month(date, lat, lon)}

@app.get("/debug/sun_position")
def debug_sun_position(date: str, lat: float = 28.61, lon: float = 77.23):
    from panchang import get_sun_moon_longitudes, _ts, _eph
    from skyfield.api import Topos
    from datetime import datetime
    
    try:
        dt_date = datetime.strptime(date, "%Y-%m-%d").date()
        
        # Get sunrise time
        topos = Topos(latitude_degrees=lat, longitude_degrees=lon)
        t0 = _ts.utc(dt_date.year, dt_date.month, dt_date.day, 0, 0)
        t1 = _ts.utc(dt_date.year, dt_date.month, dt_date.day, 23, 59)
        
        from skyfield import almanac
        from skyfield.almanac import find_discrete
        f = almanac.sunrise_sunset(_eph, topos)
        times, events = find_discrete(t0, t1, f)
        
        sunrise_time = None
        for t, e in zip(times, events):
            if e:  # True indicates sunrise
                sunrise_time = t
                break
        
        if sunrise_time is None:
            sunrise_time = _ts.utc(dt_date.year, dt_date.month, dt_date.day, 6, 0)
        
        # Get sun longitude
        sun_lon, moon_lon = get_sun_moon_longitudes(sunrise_time, lat, lon)
        
        zodiac_sign = int(sun_lon // 30)
        zodiac_names = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", 
                       "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
        
        # Simple Hindu month calculation for debugging
        hindu_month_index = (zodiac_sign + 9) % 12
        hindu_months = [
            "Chaitra", "Vaisakha", "Jyeshtha", "Ashadha",
            "Shravana", "Bhadrapada", "Ashwin", "Kartika",
            "Margashirsha", "Pausha", "Magha", "Phalguna"
        ]
        
        return {
            "date": date,
            "sun_longitude": sun_lon,
            "zodiac_sign": zodiac_sign,
            "zodiac_name": zodiac_names[zodiac_sign],
            "hindu_month": hindu_months[hindu_month_index]
        }
    except Exception as e:
        return {"error": str(e)}

@app.get("/month")
def monthly_panchang(year: int, month: int, lat: float = 28.61, lon: float = 77.23):
    from calendar import monthrange
    days = monthrange(year, month)[1]

    results = []
    for d in range(1, days+1):
        date_str = f"{year}-{month:02d}-{d:02d}"
        p = get_panchang(date_str, lat, lon)
        p["festivals"] = get_festivals(date_str, p, lat, lon)
        results.append(p)
    return results