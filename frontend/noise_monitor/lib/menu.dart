import 'package:flutter/material.dart';

class MenuScreen extends StatefulWidget {
  const MenuScreen({super.key});

  @override
  // ignore: library_private_types_in_public_api
  _MenuScreenState createState() => _MenuScreenState();
}

class _MenuScreenState extends State<MenuScreen> {

  void _goToConfigureEsp() async {
    // ignore: avoid_print
    print("Go to config esp");
  }

  void _goToConfiguredRooms() async {
    // ignore: avoid_print
    print("Go to configured rooms");
  }

  void _goToSubbedRooms() async {
    // ignore: avoid_print
    print("Go to subbed rooms");
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Menu'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            ElevatedButton(
              onPressed: _goToConfigureEsp, // Call the _handleLogin method
              child: const Text('Configure ESP32'),
              style: ElevatedButton.styleFrom(
              fixedSize: Size(150, 70),
            ),
            ),
            const SizedBox(height: 16),
            ElevatedButton(
              onPressed: _goToConfiguredRooms, // Call the _handleLogin method
              child: const Text('View configured rooms'),
              style: ElevatedButton.styleFrom(
              fixedSize: Size(150, 70),
            ),
            ),
            const SizedBox(height: 16),
            ElevatedButton(
              onPressed: _goToSubbedRooms, // Call the _handleLogin method
              child: const Text('View subscribed rooms'),
              style: ElevatedButton.styleFrom(
              fixedSize: Size(150, 70),
            ),
            ),
            const SizedBox(height: 16),
          ],
        ),
      ),
    );
  }

  @override
  void dispose() {
    super.dispose();
  }

}
