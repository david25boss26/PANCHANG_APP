#festivals.py

def get_festivals(date, panchang):
    festivals = []

    tithi = panchang["tithi"]
    nakshatra = panchang["nakshatra"]
    weekday = panchang["var"]
    month = int(date.split("-")[1])  # crude month check

    # 🪔 Diwali → Amavasya in Kartika (Oct/Nov)
    if tithi == "Amavasya" and month in (10, 11):
        festivals.append("Diwali")

    # 🌌 Janmashtami → Krishna Ashtami + Rohini
    if "Ashtami" in tithi and "Krishna" in tithi and nakshatra == "Rohini":
        festivals.append("Janmashtami")

    # 🌈 Holi → Phalguna Purnima (Feb/Mar)
    if "Purnima" in tithi and month in (2, 3):
        festivals.append("Holi")

    # 🪔 Karva Chauth → Krishna Chaturthi (Oct)
    if "Chaturthi" in tithi and "Krishna" in tithi and month == 10:
        festivals.append("Karva Chauth")

    # 🎇 Raksha Bandhan → Shravana Purnima (Aug)
    if "Purnima" in tithi and month == 8:
        festivals.append("Raksha Bandhan")

    # 🙏 Ganesh Chaturthi → Shukla Chaturthi (Aug/Sep)
    if "Chaturthi" in tithi and "Krishna" not in tithi and month in (8, 9):
        festivals.append("Ganesh Chaturthi")

    # 🕉️ Maha Shivratri → Krishna Chaturdashi (Feb/Mar)
    if "Chaturdashi" in tithi and "Krishna" in tithi and month in (2, 3):
        festivals.append("Maha Shivratri")

    # 🪔 Navratri start → Shukla Pratipada (Sep/Oct)
    if "Pratipada" in tithi and "Krishna" not in tithi and month in (9, 10):
        festivals.append("Sharadiya Navratri Begins")

    # 🌺 Dussehra → Shukla Dashami (Oct)
    if "Dashami" in tithi and "Krishna" not in tithi and month == 10:
        festivals.append("Dussehra / Vijayadashami")

    # 🎆 Makar Sankranti → fixed Jan 14
    if date.endswith("01-14"):
        festivals.append("Makar Sankranti")

    # 🌼 Ram Navami → Shukla Navami (Mar/Apr)
    if "Navami" in tithi and "Krishna" not in tithi and month in (3, 4):
        festivals.append("Ram Navami")

    return festivals
