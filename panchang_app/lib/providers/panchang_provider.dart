import 'package:flutter/foundation.dart';
import '../models/panchang_model.dart';
import '../services/api_service.dart';

class PanchangProvider with ChangeNotifier {
  PanchangModel? _currentPanchang;
  List<PanchangModel> _monthlyPanchang = [];
  bool _isLoading = false;
  String? _error;
  DateTime _selectedDate = DateTime.now();
  double _latitude = 28.61; // Default: Delhi
  double _longitude = 77.23;

  // Getters
  PanchangModel? get currentPanchang => _currentPanchang;
  List<PanchangModel> get monthlyPanchang => _monthlyPanchang;
  bool get isLoading => _isLoading;
  String? get error => _error;
  DateTime get selectedDate => _selectedDate;
  double get latitude => _latitude;
  double get longitude => _longitude;

  // Set location
  void setLocation(double lat, double lon) {
    _latitude = lat;
    _longitude = lon;
    notifyListeners();
  }

  // Set selected date
  void setSelectedDate(DateTime date) {
    _selectedDate = date;
    notifyListeners();
  }

  // Format date for API
  String _formatDate(DateTime date) {
    return '${date.year}-${date.month.toString().padLeft(2, '0')}-${date.day.toString().padLeft(2, '0')}';
  }

  // Fetch panchang for selected date
  Future<void> fetchPanchang({DateTime? date}) async {
    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      final targetDate = date ?? _selectedDate;
      final dateString = _formatDate(targetDate);
      
      _currentPanchang = await ApiService.getPanchang(
        date: dateString,
        lat: _latitude,
        lon: _longitude,
      );
      
      _selectedDate = targetDate;
    } catch (e) {
      _error = e.toString();
      if (kDebugMode) {
        print('Error fetching panchang: $e');
      }
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  // Fetch monthly panchang
  Future<void> fetchMonthlyPanchang({int? year, int? month}) async {
    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      final targetYear = year ?? _selectedDate.year;
      final targetMonth = month ?? _selectedDate.month;
      
      _monthlyPanchang = await ApiService.getMonthlyPanchang(
        year: targetYear,
        month: targetMonth,
        lat: _latitude,
        lon: _longitude,
      );
    } catch (e) {
      _error = e.toString();
      if (kDebugMode) {
        print('Error fetching monthly panchang: $e');
      }
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  // Refresh current panchang
  Future<void> refreshPanchang() async {
    await fetchPanchang();
  }

  // Clear error
  void clearError() {
    _error = null;
    notifyListeners();
  }

  // Get festivals for a specific date
  List<String> getFestivalsForDate(DateTime date) {
    final dateString = _formatDate(date);
    final panchang = _monthlyPanchang.firstWhere(
      (p) => p.date == dateString,
      orElse: () => PanchangModel(
        date: dateString,
        tithi: '',
        paksha: '',
        nakshatra: '',
        yoga: '',
        karana: '',
        vara: '',
        sunrise: '',
        sunset: '',
        festivals: [],
      ),
    );
    return panchang.festivals;
  }

  // Check if a date has festivals
  bool hasFestivals(DateTime date) {
    return getFestivalsForDate(date).isNotEmpty;
  }

  // Get today's panchang
  Future<void> getTodayPanchang() async {
    await fetchPanchang(date: DateTime.now());
  }

  // Get tomorrow's panchang
  Future<void> getTomorrowPanchang() async {
    final tomorrow = DateTime.now().add(const Duration(days: 1));
    await fetchPanchang(date: tomorrow);
  }

  // Get yesterday's panchang
  Future<void> getYesterdayPanchang() async {
    final yesterday = DateTime.now().subtract(const Duration(days: 1));
    await fetchPanchang(date: yesterday);
  }
}
