class PanchangModel {
  final String date;
  final String tithi;
  final String paksha;
  final String nakshatra;
  final int? nakshatraPada;
  final String yoga;
  final String karana;
  final String vara;
  final String? moonRashi;
  final String? sunRashi;
  final String? lunarMonthAmanta;
  final String? lunarMonthPurnimanta;
  final String? lunarMonthChosen;
  final String sunrise;
  final String sunset;
  final List<String> festivals;
  final Map<String, dynamic>? debug;

  PanchangModel({
    required this.date,
    required this.tithi,
    required this.paksha,
    required this.nakshatra,
    this.nakshatraPada,
    required this.yoga,
    required this.karana,
    required this.vara,
    this.moonRashi,
    this.sunRashi,
    this.lunarMonthAmanta,
    this.lunarMonthPurnimanta,
    this.lunarMonthChosen,
    required this.sunrise,
    required this.sunset,
    required this.festivals,
    this.debug,
  });

  factory PanchangModel.fromJson(Map<String, dynamic> json) {
    // Handle nested tithi object
    String tithiName = '';
    String pakshaName = '';
    if (json['tithi'] is Map<String, dynamic>) {
      tithiName = json['tithi']['name'] ?? '';
      pakshaName = json['tithi']['paksha'] ?? '';
    } else {
      tithiName = json['tithi'] ?? '';
      pakshaName = json['paksha'] ?? '';
    }

    // Handle nested nakshatra object
    String nakshatraName = '';
    int? nakshatraPada;
    if (json['nakshatra'] is Map<String, dynamic>) {
      nakshatraName = json['nakshatra']['name'] ?? '';
      nakshatraPada = json['nakshatra']['number'];
    } else {
      nakshatraName = json['nakshatra'] ?? '';
      nakshatraPada = json['nakshatra_pada'];
    }

    // Handle nested yoga object
    String yogaName = '';
    if (json['yoga'] is Map<String, dynamic>) {
      yogaName = json['yoga']['name'] ?? '';
    } else {
      yogaName = json['yoga'] ?? '';
    }

    // Handle nested karana object
    String karanaName = '';
    if (json['karana'] is Map<String, dynamic>) {
      karanaName = json['karana']['name'] ?? '';
    } else {
      karanaName = json['karana'] ?? '';
    }

    return PanchangModel(
      date: json['date'] ?? '',
      tithi: tithiName,
      paksha: pakshaName,
      nakshatra: nakshatraName,
      nakshatraPada: nakshatraPada,
      yoga: yogaName,
      karana: karanaName,
      vara: json['var'] ?? json['vara'] ?? '',
      moonRashi: json['moon_rashi'],
      sunRashi: json['sun_rashi'],
      lunarMonthAmanta: json['lunar_month_amanta'],
      lunarMonthPurnimanta: json['lunar_month_purnimanta'],
      lunarMonthChosen: json['lunar_month_chosen'],
      sunrise: json['sunrise'] ?? '',
      sunset: json['sunset'] ?? '',
      festivals: _parseFestivals(json['festivals']),
      debug: json['_debug'],
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'date': date,
      'tithi': tithi,
      'paksha': paksha,
      'nakshatra': nakshatra,
      'nakshatra_pada': nakshatraPada,
      'yoga': yoga,
      'karana': karana,
      'var': vara,
      'moon_rashi': moonRashi,
      'sun_rashi': sunRashi,
      'lunar_month_amanta': lunarMonthAmanta,
      'lunar_month_purnimanta': lunarMonthPurnimanta,
      'lunar_month_chosen': lunarMonthChosen,
      'sunrise': sunrise,
      'sunset': sunset,
      'festivals': festivals,
      '_debug': debug,
    };
  }

  // Helper method to safely parse festivals
  static List<String> _parseFestivals(dynamic festivals) {
    if (festivals == null) return [];
    if (festivals is List) {
      return festivals.map((f) => f.toString()).toList();
    }
    return [];
  }
}

class FestivalModel {
  final String name;
  final String date;
  final String description;
  final String emoji;

  FestivalModel({
    required this.name,
    required this.date,
    required this.description,
    required this.emoji,
  });

  static Map<String, FestivalModel> festivalData = {
    'Diwali': FestivalModel(
      name: 'Diwali',
      date: 'Kartika Amavasya',
      description: 'Festival of Lights - Victory of good over evil',
      emoji: '🪔',
    ),
    'Krishna Janmashtami': FestivalModel(
      name: 'Krishna Janmashtami',
      date: 'Bhadrapada Krishna Ashtami',
      description: 'Birth anniversary of Lord Krishna',
      emoji: '🌌',
    ),
    'Holi': FestivalModel(
      name: 'Holi',
      date: 'Phalguna Purnima',
      description: 'Festival of Colors - Spring celebration',
      emoji: '🌈',
    ),
    'Karva Chauth': FestivalModel(
      name: 'Karva Chauth',
      date: 'Kartika Krishna Chaturthi',
      description: 'Hindu festival for married women',
      emoji: '🪔',
    ),
    'Raksha Bandhan': FestivalModel(
      name: 'Raksha Bandhan',
      date: 'Shravana Purnima',
      description: 'Sacred bond between brothers and sisters',
      emoji: '🎇',
    ),
    'Ganesh Chaturthi': FestivalModel(
      name: 'Ganesh Chaturthi',
      date: 'Bhadrapada Shukla Chaturthi',
      description: 'Birth anniversary of Lord Ganesha',
      emoji: '🙏',
    ),
    'Maha Shivratri': FestivalModel(
      name: 'Maha Shivratri',
      date: 'Phalguna Krishna Chaturdashi',
      description: 'Great night of Lord Shiva',
      emoji: '🕉️',
    ),
    'Sharadiya Navratri Begins': FestivalModel(
      name: 'Sharadiya Navratri',
      date: 'Ashwin Shukla Pratipada',
      description: 'Nine nights of Goddess Durga',
      emoji: '🪔',
    ),
    'Dussehra / Vijayadashami': FestivalModel(
      name: 'Dussehra',
      date: 'Ashwin Shukla Dashami',
      description: 'Victory of good over evil',
      emoji: '🌺',
    ),
    'Makar Sankranti': FestivalModel(
      name: 'Makar Sankranti',
      date: 'January 14-15',
      description: 'Sun enters Capricorn - Harvest festival',
      emoji: '🎆',
    ),
    'Ram Navami': FestivalModel(
      name: 'Ram Navami',
      date: 'Chaitra Shukla Navami',
      description: 'Birth anniversary of Lord Rama',
      emoji: '🌼',
    ),
    'Chhath Puja': FestivalModel(
      name: 'Chhath Puja',
      date: 'Kartika Shukla Shashthi',
      description: 'Sun worship festival',
      emoji: '🪔',
    ),
  };
}
