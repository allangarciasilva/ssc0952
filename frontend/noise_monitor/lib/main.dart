import 'dart:convert';
import 'login_screen.dart';
import 'menu.dart';
import 'package:flutter/material.dart';
import 'package:syncfusion_flutter_charts/charts.dart';
import 'package:web_socket_channel/web_socket_channel.dart';

void main() {
  runApp(const App());
}

class App extends StatefulWidget {
  const App({super.key});

  @override
  State<App> createState() => _AppState();
}

class Pair<T, U> {
  final T first;
  final U second;

  Pair(this.first, this.second);

  @override
  String toString() => '($first, $second)';
}

class _AppState extends State<App> {
  List<double> messages = List<double>.generate(10, (index) => 0);

  @override
  void initState() {
    super.initState();
  }

  static double maxV = 10;

  List<Pair<int, double>> _getData() {
    var data = <Pair<int, double>>[];
    // double sum = 0;
    // for (int i = 0; i < messages.length; i++) {
    //   sum += messages[i];
    // }

    // double average = sum / messages.length;
    for (int i = 0; i < messages.length; i++) {
      double v = messages[i] - 9 * messages.length;
      data.add(Pair(i, maxV - v));
    }

    print(data[1]);
    return data;
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: Scaffold(
        appBar: AppBar(
          title: Text('Monitoramento de Ruído e Ocupação de Salas'),
          backgroundColor: Colors.pink,
        ),
        body: MenuScreen(),
      ),
    );
  }

  @override
  void dispose() {
    super.dispose();
  }
}
