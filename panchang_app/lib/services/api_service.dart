import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/panchang_model.dart';

class ApiService {
  // Change this to your FastAPI server URL
  // For local development, use: http://10.0.2.2:8000 (Android emulator)
  // For physical device, use your computer's IP address
  // Prefer setting this via --dart-define=API_BASE_URL=your_url
  // Example: flutter run --dart-define=API_BASE_URL=https://your-domain.com
  // Default falls back to Android emulator loopback (10.0.2.2)
  static const String baseUrl = String.fromEnvironment(
    'API_BASE_URL',
    defaultValue: 'http://10.0.2.2:8000',
  );

  // For testing with your actual device, replace with your computer's IP
  // Example: static const String baseUrl = 'http://192.168.1.100:8000';

  static Future<PanchangModel> getPanchang({
    required String date,
    double lat = 28.61,
    double lon = 77.23,
  }) async {
    try {
      final uri = Uri.parse('$baseUrl/panchang').replace(
        queryParameters: {
          'date': date,
          'lat': lat.toString(),
          'lon': lon.toString(),
        },
      );

      final response = await http.get(uri);

      if (response.statusCode == 200) {
        final Map<String, dynamic> data = json.decode(response.body);

        // Check if the response contains an error
        if (data.containsKey('error')) {
          throw Exception('Backend error: ${data['error']}');
        }

        return PanchangModel.fromJson(data);
      } else {
        throw Exception(
          'Failed to load panchang data: ${response.statusCode} - ${response.body}',
        );
      }
    } catch (e) {
      if (e.toString().contains(
        'type \'_Map<String, dynamic>\' is not a subtype of type \'String\'',
      )) {
        throw Exception(
          'Data format error: Backend returned unexpected data structure. Please check the API response format.',
        );
      }
      throw Exception('Error fetching panchang data: $e');
    }
  }

  static Future<List<PanchangModel>> getMonthlyPanchang({
    required int year,
    required int month,
    double lat = 28.61,
    double lon = 77.23,
  }) async {
    try {
      final uri = Uri.parse('$baseUrl/month').replace(
        queryParameters: {
          'year': year.toString(),
          'month': month.toString(),
          'lat': lat.toString(),
          'lon': lon.toString(),
        },
      );

      final response = await http.get(uri);

      if (response.statusCode == 200) {
        final List<dynamic> data = json.decode(response.body);
        return data.map((json) => PanchangModel.fromJson(json)).toList();
      } else {
        throw Exception(
          'Failed to load monthly panchang data: ${response.statusCode} - ${response.body}',
        );
      }
    } catch (e) {
      if (e.toString().contains(
        'type \'_Map<String, dynamic>\' is not a subtype of type \'String\'',
      )) {
        throw Exception(
          'Data format error: Backend returned unexpected data structure for monthly data.',
        );
      }
      throw Exception('Error fetching monthly panchang data: $e');
    }
  }

  static Future<Map<String, dynamic>> getDebugHinduMonth({
    required String date,
    double lat = 28.61,
    double lon = 77.23,
  }) async {
    try {
      final uri = Uri.parse('$baseUrl/debug/hindu_month').replace(
        queryParameters: {
          'date': date,
          'lat': lat.toString(),
          'lon': lon.toString(),
        },
      );

      final response = await http.get(uri);

      if (response.statusCode == 200) {
        return json.decode(response.body);
      } else {
        throw Exception('Failed to load debug data: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Error fetching debug data: $e');
    }
  }

  static Future<Map<String, dynamic>> getDebugSunPosition({
    required String date,
    double lat = 28.61,
    double lon = 77.23,
  }) async {
    try {
      final uri = Uri.parse('$baseUrl/debug/sun_position').replace(
        queryParameters: {
          'date': date,
          'lat': lat.toString(),
          'lon': lon.toString(),
        },
      );

      final response = await http.get(uri);

      if (response.statusCode == 200) {
        return json.decode(response.body);
      } else {
        throw Exception(
          'Failed to load sun position data: ${response.statusCode}',
        );
      }
    } catch (e) {
      throw Exception('Error fetching sun position data: $e');
    }
  }
}
