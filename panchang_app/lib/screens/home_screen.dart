import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:intl/intl.dart';
import '../providers/panchang_provider.dart';
import '../models/panchang_model.dart';
import 'panchang_detail_screen.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  @override
  void initState() {
    super.initState();
    // Load today's panchang when the screen initializes
    WidgetsBinding.instance.addPostFrameCallback((_) {
      context.read<PanchangProvider>().getTodayPanchang();
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF1A1A2E),
      body: SafeArea(
        child: Consumer<PanchangProvider>(
          builder: (context, provider, child) {
            if (provider.isLoading && provider.currentPanchang == null) {
              return const Center(
                child: CircularProgressIndicator(
                  valueColor: AlwaysStoppedAnimation<Color>(Color(0xFFE94560)),
                ),
              );
            }

            if (provider.error != null) {
              return Center(
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    const Icon(
                      Icons.error_outline,
                      size: 64,
                      color: Color(0xFFE94560),
                    ),
                    const SizedBox(height: 16),
                    Text(
                      'Error loading Panchang',
                      style: GoogleFonts.poppins(
                        fontSize: 18,
                        fontWeight: FontWeight.w600,
                        color: Colors.white,
                      ),
                    ),
                    const SizedBox(height: 8),
                    Text(
                      provider.error!,
                      style: GoogleFonts.poppins(
                        fontSize: 14,
                        color: Colors.white70,
                      ),
                      textAlign: TextAlign.center,
                    ),
                    const SizedBox(height: 24),
                    ElevatedButton(
                      onPressed: () => provider.getTodayPanchang(),
                      style: ElevatedButton.styleFrom(
                        backgroundColor: const Color(0xFFE94560),
                        foregroundColor: Colors.white,
                      ),
                      child: const Text('Retry'),
                    ),
                  ],
                ),
              );
            }

            final panchang = provider.currentPanchang;
            if (panchang == null) {
              return const Center(
                child: Text(
                  'No data available',
                  style: TextStyle(color: Colors.white),
                ),
              );
            }

            return CustomScrollView(
              slivers: [
                // App Bar
                SliverAppBar(
                  expandedHeight: 200,
                  floating: false,
                  pinned: true,
                  backgroundColor: const Color(0xFF16213E),
                  flexibleSpace: FlexibleSpaceBar(
                    title: Text(
                      'Hindu Panchang',
                      style: GoogleFonts.poppins(
                        fontWeight: FontWeight.bold,
                        color: Colors.white,
                      ),
                    ),
                    background: Container(
                      decoration: const BoxDecoration(
                        gradient: LinearGradient(
                          begin: Alignment.topLeft,
                          end: Alignment.bottomRight,
                          colors: [
                            Color(0xFF16213E),
                            Color(0xFF0F3460),
                            Color(0xFFE94560),
                          ],
                        ),
                      ),
                      child: Center(
                        child: Column(
                          mainAxisAlignment: MainAxisAlignment.center,
                          children: [
                            const SizedBox(height: 40),
                            Text(
                              DateFormat(
                                'EEEE, MMMM d, y',
                              ).format(provider.selectedDate),
                              style: GoogleFonts.poppins(
                                fontSize: 18,
                                fontWeight: FontWeight.w500,
                                color: Colors.white,
                              ),
                            ),
                            const SizedBox(height: 8),
                            Text(
                              '${panchang.lunarMonthChosen ?? 'Unknown'} Month',
                              style: GoogleFonts.poppins(
                                fontSize: 16,
                                color: Colors.white70,
                              ),
                            ),
                          ],
                        ),
                      ),
                    ),
                  ),
                  actions: [
                    IconButton(
                      onPressed: () => _showDatePicker(context, provider),
                      icon: const Icon(
                        Icons.calendar_today,
                        color: Colors.white,
                      ),
                    ),
                    IconButton(
                      onPressed: () => provider.refreshPanchang(),
                      icon: const Icon(Icons.refresh, color: Colors.white),
                    ),
                  ],
                ),

                // Panchang Cards
                SliverPadding(
                  padding: const EdgeInsets.all(16),
                  sliver: SliverList(
                    delegate: SliverChildListDelegate([
                      // Tithi Card
                      _buildPanchangCard(
                        'Tithi',
                        panchang.tithi,
                        '🌙',
                        const Color(0xFF4A90E2),
                        () => _navigateToDetail(context, 'Tithi', panchang),
                      ),
                      const SizedBox(height: 16),

                      // Nakshatra Card
                      _buildPanchangCard(
                        'Nakshatra',
                        panchang.nakshatra,
                        '⭐',
                        const Color(0xFF7B68EE),
                        () => _navigateToDetail(context, 'Nakshatra', panchang),
                      ),
                      const SizedBox(height: 16),

                      // Yoga Card
                      _buildPanchangCard(
                        'Yoga',
                        panchang.yoga,
                        '🧘',
                        const Color(0xFF20B2AA),
                        () => _navigateToDetail(context, 'Yoga', panchang),
                      ),
                      const SizedBox(height: 16),

                      // Karana Card
                      _buildPanchangCard(
                        'Karana',
                        panchang.karana,
                        '⏰',
                        const Color(0xFFFF6B6B),
                        () => _navigateToDetail(context, 'Karana', panchang),
                      ),
                      const SizedBox(height: 16),

                      // Vara Card
                      _buildPanchangCard(
                        'Vara',
                        panchang.vara,
                        '📅',
                        const Color(0xFFFFA726),
                        () => _navigateToDetail(context, 'Vara', panchang),
                      ),
                      const SizedBox(height: 24),

                      // Festivals Section
                      if (panchang.festivals.isNotEmpty) ...[
                        Text(
                          'Festivals Today',
                          style: GoogleFonts.poppins(
                            fontSize: 20,
                            fontWeight: FontWeight.bold,
                            color: Colors.white,
                          ),
                        ),
                        const SizedBox(height: 16),
                        ...panchang.festivals.map(
                          (festival) => _buildFestivalCard(festival),
                        ),
                        const SizedBox(height: 24),
                      ],

                      // Sunrise/Sunset Info
                      _buildSunInfoCard(panchang),
                      const SizedBox(height: 100), // Bottom padding
                    ]),
                  ),
                ),
              ],
            );
          },
        ),
      ),
    );
  }

  Widget _buildPanchangCard(
    String title,
    String value,
    String emoji,
    Color color,
    VoidCallback onTap,
  ) {
    return GestureDetector(
      onTap: onTap,
      child: Container(
        padding: const EdgeInsets.all(20),
        decoration: BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topLeft,
            end: Alignment.bottomRight,
            colors: [color.withOpacity(0.8), color],
          ),
          borderRadius: BorderRadius.circular(16),
          boxShadow: [
            BoxShadow(
              color: color.withOpacity(0.3),
              blurRadius: 10,
              offset: const Offset(0, 5),
            ),
          ],
        ),
        child: Row(
          children: [
            Text(emoji, style: const TextStyle(fontSize: 32)),
            const SizedBox(width: 16),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    title,
                    style: GoogleFonts.poppins(
                      fontSize: 14,
                      fontWeight: FontWeight.w500,
                      color: Colors.white70,
                    ),
                  ),
                  const SizedBox(height: 4),
                  Text(
                    value,
                    style: GoogleFonts.poppins(
                      fontSize: 18,
                      fontWeight: FontWeight.bold,
                      color: Colors.white,
                    ),
                  ),
                ],
              ),
            ),
            const Icon(
              Icons.arrow_forward_ios,
              color: Colors.white70,
              size: 16,
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildFestivalCard(String festivalName) {
    final festival = FestivalModel.festivalData[festivalName];
    return Container(
      margin: const EdgeInsets.only(bottom: 12),
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: const Color(0xFFE94560).withOpacity(0.1),
        borderRadius: BorderRadius.circular(12),
        border: Border.all(
          color: const Color(0xFFE94560).withOpacity(0.3),
          width: 1,
        ),
      ),
      child: Row(
        children: [
          Text(festival?.emoji ?? '🎉', style: const TextStyle(fontSize: 24)),
          const SizedBox(width: 12),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  festivalName,
                  style: GoogleFonts.poppins(
                    fontSize: 16,
                    fontWeight: FontWeight.bold,
                    color: Colors.white,
                  ),
                ),
                if (festival != null) ...[
                  const SizedBox(height: 4),
                  Text(
                    festival.description,
                    style: GoogleFonts.poppins(
                      fontSize: 12,
                      color: Colors.white70,
                    ),
                  ),
                ],
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildSunInfoCard(PanchangModel panchang) {
    return Container(
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: const Color(0xFF16213E),
        borderRadius: BorderRadius.circular(16),
        border: Border.all(color: const Color(0xFF0F3460), width: 1),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            'Sunrise & Sunset',
            style: GoogleFonts.poppins(
              fontSize: 18,
              fontWeight: FontWeight.bold,
              color: Colors.white,
            ),
          ),
          const SizedBox(height: 16),
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceAround,
            children: [
              _buildSunInfo('🌅', 'Sunrise', _formatTime(panchang.sunrise)),
              _buildSunInfo('🌇', 'Sunset', _formatTime(panchang.sunset)),
            ],
          ),
        ],
      ),
    );
  }

  Widget _buildSunInfo(String emoji, String label, String time) {
    return Column(
      children: [
        Text(emoji, style: const TextStyle(fontSize: 24)),
        const SizedBox(height: 8),
        Text(
          label,
          style: GoogleFonts.poppins(fontSize: 12, color: Colors.white70),
        ),
        const SizedBox(height: 4),
        Text(
          time,
          style: GoogleFonts.poppins(
            fontSize: 16,
            fontWeight: FontWeight.bold,
            color: Colors.white,
          ),
        ),
      ],
    );
  }

  String _formatTime(String timeString) {
    try {
      // Extract time from the full datetime string
      final parts = timeString.split(' ');
      if (parts.length >= 2) {
        final timePart = parts[1];
        final timeComponents = timePart.split(':');
        if (timeComponents.length >= 2) {
          return '${timeComponents[0]}:${timeComponents[1]}';
        }
      }
      return timeString;
    } catch (e) {
      return timeString;
    }
  }

  void _showDatePicker(BuildContext context, PanchangProvider provider) {
    showDatePicker(
      context: context,
      initialDate: provider.selectedDate,
      firstDate: DateTime(2020),
      lastDate: DateTime(2030),
      builder: (context, child) {
        return Theme(
          data: Theme.of(context).copyWith(
            colorScheme: const ColorScheme.dark(
              primary: Color(0xFFE94560),
              onPrimary: Colors.white,
              surface: Color(0xFF1A1A2E),
              onSurface: Colors.white,
            ),
          ),
          child: child!,
        );
      },
    ).then((selectedDate) {
      if (selectedDate != null) {
        provider.fetchPanchang(date: selectedDate);
      }
    });
  }

  void _navigateToDetail(
    BuildContext context,
    String title,
    PanchangModel panchang,
  ) {
    Navigator.push(
      context,
      MaterialPageRoute(
        builder: (context) =>
            PanchangDetailScreen(title: title, panchang: panchang),
      ),
    );
  }
}
