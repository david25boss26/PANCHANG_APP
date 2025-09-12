

```markdown
# 🕉️ Hindu Panchang & Festival Calculator

A comprehensive **Hindu Panchang and Festival Calculator** application with both a Python FastAPI backend and a Flutter mobile frontend. This application provides accurate astronomical calculations for Hindu calendar elements and festival detection.

## 🌟 Features

### 📱 **Mobile App (Flutter)**
- **Beautiful Dark Theme** with modern UI/UX
- **Cross-Platform Support** - Android, iOS, and Web
- **Interactive Panchang Cards** with detailed information
- **Festival Detection** with emojis and descriptions
- **Date Picker** for any date selection
- **Sunrise/Sunset Times** with astronomical accuracy
- **Responsive Design** for all screen sizes

### 🔧 **Backend API (Python/FastAPI)**
- **Accurate Astronomical Calculations** using Skyfield library
- **Comprehensive Panchang Data** - Tithi, Nakshatra, Yoga, Karana, Vara
- **Festival Detection** for major Hindu festivals
- **Multiple Calculation Methods** with debug endpoints
- **RESTful API** with automatic documentation

## 🏗️ Architecture

```
├── Backend (Python/FastAPI)
│   ├── main.py - API server
│   ├── panchang2.py - Panchang calculations
│   ├── festivals2.py - Festival detection
│   └── requirements.txt - Dependencies
│
├── Frontend (Flutter)
│   ├── lib/
│   │   ├── main.dart - App entry point
│   │   ├── models/ - Data models
│   │   ├── providers/ - State management
│   │   ├── services/ - API communication
│   │   └── screens/ - UI screens
│   └── pubspec.yaml - Flutter dependencies
│
└── README.md - This file
```

## 🚀 Quick Start

### **Prerequisites**
- Python 3.8+
- Flutter 3.8+
- Git

### **1. Clone the Repository**
```bash
git clone <your-repository-url>
cd major1
```

### **2. Backend Setup**
```bash
# Install Python dependencies
pip install -r requirements.txt

# Start the FastAPI server
python run.py
```

The backend will be available at `http://localhost:8000`

### **3. Frontend Setup**
```bash
# Navigate to Flutter app
cd panchang_app

# Install Flutter dependencies
flutter pub get

# Update API URL (see Configuration section)
# Run the app
flutter run
```

## ⚙️ Configuration

### **Backend Configuration**
- **Default Location**: Delhi (28.61°N, 77.23°E)
- **Port**: 8000
- **Ephemeris**: de421.bsp (downloaded automatically)

### **Frontend Configuration**
Update the API URL in `panchang_app/lib/services/api_service.dart`:

```dart
// For Android Emulator
static const String baseUrl = 'http://10.0.2.2:8000';

// For Physical Device (replace with your computer's IP)
static const String baseUrl = 'http://192.168.1.100:8000';

// For Web
static const String baseUrl = 'http://localhost:8000';
```

## �� API Endpoints

### **Main Endpoints**
- `GET /panchang?date=YYYY-MM-DD&lat=28.61&lon=77.23` - Get daily panchang
- `GET /month?year=2025&month=8&lat=28.61&lon=77.23` - Get monthly panchang

### **Debug Endpoints**
- `GET /debug/hindu_month` - Debug Hindu month calculations
- `GET /debug/sun_position` - Debug sun position calculations

### **API Documentation**
Visit `http://localhost:8000/docs` for interactive API documentation

## 🧮 Panchang Calculations

### **Supported Elements**
- **Tithi** - Lunar day (1-30)
- **Nakshatra** - Lunar mansion (1-27)
- **Yoga** - Sun-Moon combination (1-27)
- **Karana** - Half-tithi period (1-11)
- **Vara** - Weekday
- **Rashi** - Zodiac signs
- **Lunar Months** - Amanta and Purnimanta systems

### **Festival Detection**
The application detects major Hindu festivals including:
- 🪔 **Diwali** (Kartika Amavasya)
- �� **Krishna Janmashtami** (Bhadrapada Krishna Ashtami + Rohini)
- �� **Holi** (Phalguna Purnima)
- �� **Raksha Bandhan** (Shravana Purnima)
- �� **Ganesh Chaturthi** (Bhadrapada Shukla Chaturthi)
- 🕉️ **Maha Shivratri** (Phalguna Krishna Chaturdashi)
- 🪔 **Navratri** (Ashwin Shukla Pratipada)
- 🌺 **Dussehra** (Ashwin Shukla Dashami)
- 🎆 **Makar Sankranti** (January 14-15)
- �� **Ram Navami** (Chaitra Shukla Navami)
- �� **Chhath Puja** (Kartika Shukla Shashthi)

## 🛠️ Development

### **Backend Development**
```bash
# Run with auto-reload
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# Run tests
python -m pytest

# Check code quality
flake8 .
```

### **Frontend Development**
```bash
# Run in debug mode
flutter run --debug

# Run in release mode
flutter run --release

# Build APK
flutter build apk

# Build for web
flutter build web
```

## 📱 Screenshots

### **Home Screen**
- Beautiful gradient header with date display
- Interactive panchang cards with emojis
- Festival notifications
- Sunrise/sunset information

### **Detail Screen**
- Comprehensive panchang information
- Astronomical data
- Festival descriptions
- Educational content

## 🔧 Troubleshooting

### **Common Issues**

#### **1. Backend Connection Error**
```
Error: Failed to connect to backend
```
**Solution**: 
- Ensure backend is running: `python run.py`
- Check API URL in `api_service.dart`
- Verify network connectivity

#### **2. Data Format Error**
```
type '_Map<String, dynamic>' is not a subtype of type 'String'
```
**Solution**: This has been fixed in the latest version. Update your code.

#### **3. Port Already in Use**
```
Error: Port 8000 is already in use
```
**Solution**:
```bash
# Kill process using port 8000
lsof -ti:8000 | xargs kill -9
```

#### **4. Flutter Dependencies**
```
Error: Could not resolve dependencies
```
**Solution**:
```bash
flutter clean
flutter pub get
```

### **Testing the Backend**
```bash
# Test daily panchang
curl http://localhost:8000/panchang?date=2025-09-10

# Test monthly panchang
curl http://localhost:8000/month?year=2025&month=9

# Check API documentation
open http://localhost:8000/docs
```

## 📚 Technical Details

### **Astronomical Accuracy**
- Uses **Skyfield** library for precise calculations
- **Lahiri Ayanamsa** for sidereal calculations
- **Topocentric** calculations for accurate local times
- **Ephemeris Data** from NASA JPL

### **Data Sources**
- **Ephemeris**: de421.bsp (NASA JPL)
- **Festival Logic**: Traditional Hindu calendar rules
- **Location Data**: Configurable latitude/longitude

### **Performance**
- **Backend**: FastAPI with async support
- **Frontend**: Flutter with efficient state management
- **Caching**: Built-in Flutter caching mechanisms

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -am 'Add feature'`
4. Push to branch: `git push origin feature-name`
5. Submit a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## �� Acknowledgments

- **Skyfield** - Astronomical calculations
- **FastAPI** - Modern web framework
- **Flutter** - Cross-platform UI framework
- **Hindu Calendar** - Traditional astronomical knowledge

## 📞 Support

For support and questions:
- Create an issue in the repository
- Check the troubleshooting section
- Review the API documentation

## 🔮 Future Enhancements

- [ ] **Offline Support** - Cache panchang data
- [ ] **Multiple Languages** - Hindi, Sanskrit support
- [ ] **Custom Locations** - GPS-based location detection
- [ ] **Push Notifications** - Festival reminders
- [ ] **Calendar Integration** - Export to device calendar
- [ ] **Advanced Features** - Muhurta, Choghadiya
- [ ] **Social Features** - Share panchang data

---

**Made with ❤️ for the Hindu community**

*Accurate astronomical calculations for traditional Hindu calendar and festival detection*
```

