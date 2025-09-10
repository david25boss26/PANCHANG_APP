#main.py

from fastapi import FastAPI
from panchang import get_panchang
from festivals import get_festivals

app = FastAPI()

@app.get("/panchang")
def daily_panchang(date: str):
    try:
        p = get_panchang(date)
        if not isinstance(p, dict):
            return {"error": "get_panchang did not return a dict", "value": str(p)}
        p["festivals"] = get_festivals(date, p)
        return p
    except Exception as e:
        return {"error": str(e)}


@app.get("/month")
def monthly_panchang(year: int, month: int):
    from calendar import monthrange
    days = monthrange(year, month)[1]

    results = []
    for d in range(1, days+1):
        date = f"{year}-{month:02d}-{d:02d}"
        p = get_panchang(date)
        p["festivals"] = get_festivals(date, p)
        results.append(p)
    return results
