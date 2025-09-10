import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import '../models/panchang_model.dart';

class PanchangDetailScreen extends StatelessWidget {
  final String title;
  final PanchangModel panchang;

  const PanchangDetailScreen({
    super.key,
    required this.title,
    required this.panchang,
  });

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF1A1A2E),
      appBar: AppBar(
        title: Text(
          title,
          style: GoogleFonts.poppins(
            fontWeight: FontWeight.bold,
            color: Colors.white,
          ),
        ),
        backgroundColor: const Color(0xFF16213E),
        iconTheme: const IconThemeData(color: Colors.white),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            _buildDetailCard(),
            const SizedBox(height: 24),
            _buildRelatedInfo(),
            const SizedBox(height: 24),
            _buildAstronomicalData(),
          ],
        ),
      ),
    );
  }

  Widget _buildDetailCard() {
    String emoji = '📅';
    String description = '';
    String additionalInfo = '';

    switch (title) {
      case 'Tithi':
        emoji = '🌙';
        description = 'Tithi is a lunar day in the Hindu calendar. It represents the angular relationship between the Sun and Moon.';
        additionalInfo = 'Paksha: ${panchang.paksha}';
        break;
      case 'Nakshatra':
        emoji = '⭐';
        description = 'Nakshatra is a lunar mansion in Hindu astrology. There are 27 nakshatras, each spanning 13°20\' of the ecliptic.';
        additionalInfo = panchang.nakshatraPada != null 
            ? 'Pada: ${panchang.nakshatraPada}' 
            : 'Lunar mansion';
        break;
      case 'Yoga':
        emoji = '🧘';
        description = 'Yoga is a combination of the Sun and Moon longitudes. There are 27 yogas, each representing different qualities.';
        additionalInfo = 'Combination of Sun and Moon positions';
        break;
      case 'Karana':
        emoji = '⏰';
        description = 'Karana is half of a tithi. There are 11 karanas, with the first 7 repeating and the last 4 occurring once.';
        additionalInfo = 'Half-tithi period';
        break;
      case 'Vara':
        emoji = '📅';
        description = 'Vara is the weekday in the Hindu calendar, corresponding to the seven days of the week.';
        additionalInfo = 'Weekday';
        break;
    }

    return Container(
      padding: const EdgeInsets.all(24),
      decoration: BoxDecoration(
        gradient: const LinearGradient(
          begin: Alignment.topLeft,
          end: Alignment.bottomRight,
          colors: [
            Color(0xFF16213E),
            Color(0xFF0F3460),
          ],
        ),
        borderRadius: BorderRadius.circular(20),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.3),
            blurRadius: 15,
            offset: const Offset(0, 8),
          ),
        ],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Text(
                emoji,
                style: const TextStyle(fontSize: 48),
              ),
              const SizedBox(width: 16),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      title,
                      style: GoogleFonts.poppins(
                        fontSize: 24,
                        fontWeight: FontWeight.bold,
                        color: Colors.white,
                      ),
                    ),
                    const SizedBox(height: 8),
                    Text(
                      _getValueForTitle(),
                      style: GoogleFonts.poppins(
                        fontSize: 18,
                        fontWeight: FontWeight.w600,
                        color: const Color(0xFFE94560),
                      ),
                    ),
                  ],
                ),
              ),
            ],
          ),
          const SizedBox(height: 20),
          Text(
            description,
            style: GoogleFonts.poppins(
              fontSize: 16,
              color: Colors.white70,
              height: 1.5,
            ),
          ),
          const SizedBox(height: 16),
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
            decoration: BoxDecoration(
              color: const Color(0xFFE94560).withOpacity(0.2),
              borderRadius: BorderRadius.circular(8),
              border: Border.all(
                color: const Color(0xFFE94560).withOpacity(0.3),
              ),
            ),
            child: Text(
              additionalInfo,
              style: GoogleFonts.poppins(
                fontSize: 14,
                fontWeight: FontWeight.w500,
                color: const Color(0xFFE94560),
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildRelatedInfo() {
    return Container(
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: const Color(0xFF16213E),
        borderRadius: BorderRadius.circular(16),
        border: Border.all(
          color: const Color(0xFF0F3460),
          width: 1,
        ),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            'Complete Panchang for ${panchang.date}',
            style: GoogleFonts.poppins(
              fontSize: 18,
              fontWeight: FontWeight.bold,
              color: Colors.white,
            ),
          ),
          const SizedBox(height: 16),
          _buildInfoRow('🌙', 'Tithi', panchang.tithi),
          _buildInfoRow('⭐', 'Nakshatra', panchang.nakshatra),
          _buildInfoRow('🧘', 'Yoga', panchang.yoga),
          _buildInfoRow('⏰', 'Karana', panchang.karana),
          _buildInfoRow('📅', 'Vara', panchang.vara),
          if (panchang.moonRashi != null)
            _buildInfoRow('🌕', 'Moon Rashi', panchang.moonRashi!),
          if (panchang.sunRashi != null)
            _buildInfoRow('☀️', 'Sun Rashi', panchang.sunRashi!),
          if (panchang.lunarMonthChosen != null)
            _buildInfoRow('📆', 'Lunar Month', panchang.lunarMonthChosen!),
        ],
      ),
    );
  }

  Widget _buildInfoRow(String emoji, String label, String value) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 12),
      child: Row(
        children: [
          Text(emoji, style: const TextStyle(fontSize: 20)),
          const SizedBox(width: 12),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  label,
                  style: GoogleFonts.poppins(
                    fontSize: 12,
                    color: Colors.white70,
                  ),
                ),
                Text(
                  value,
                  style: GoogleFonts.poppins(
                    fontSize: 16,
                    fontWeight: FontWeight.w600,
                    color: Colors.white,
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildAstronomicalData() {
    if (panchang.debug == null) return const SizedBox.shrink();

    return Container(
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: const Color(0xFF16213E),
        borderRadius: BorderRadius.circular(16),
        border: Border.all(
          color: const Color(0xFF0F3460),
          width: 1,
        ),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            'Astronomical Data',
            style: GoogleFonts.poppins(
              fontSize: 18,
              fontWeight: FontWeight.bold,
              color: Colors.white,
            ),
          ),
          const SizedBox(height: 16),
          if (panchang.debug!['ayanamsa_deg_at_sunrise'] != null)
            _buildDebugRow('Ayanamsa', '${panchang.debug!['ayanamsa_deg_at_sunrise']}°'),
          if (panchang.debug!['sun_lon_tropical_at_sunrise'] != null)
            _buildDebugRow('Sun Longitude', '${panchang.debug!['sun_lon_tropical_at_sunrise']}°'),
          if (panchang.debug!['moon_lon_tropical_at_sunrise'] != null)
            _buildDebugRow('Moon Longitude', '${panchang.debug!['moon_lon_tropical_at_sunrise']}°'),
          if (panchang.debug!['sidereal_sun_lon_at_sunrise'] != null)
            _buildDebugRow('Sidereal Sun', '${panchang.debug!['sidereal_sun_lon_at_sunrise']}°'),
          if (panchang.debug!['sidereal_moon_lon_at_sunrise'] != null)
            _buildDebugRow('Sidereal Moon', '${panchang.debug!['sidereal_moon_lon_at_sunrise']}°'),
        ],
      ),
    );
  }

  Widget _buildDebugRow(String label, String value) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 8),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Text(
            label,
            style: GoogleFonts.poppins(
              fontSize: 14,
              color: Colors.white70,
            ),
          ),
          Text(
            value,
            style: GoogleFonts.poppins(
              fontSize: 14,
              fontWeight: FontWeight.w500,
              color: Colors.white,
            ),
          ),
        ],
      ),
    );
  }

  String _getValueForTitle() {
    switch (title) {
      case 'Tithi':
        return panchang.tithi;
      case 'Nakshatra':
        return panchang.nakshatra;
      case 'Yoga':
        return panchang.yoga;
      case 'Karana':
        return panchang.karana;
      case 'Vara':
        return panchang.vara;
      default:
        return '';
    }
  }
}
