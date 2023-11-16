import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:syncfusion_flutter_charts/charts.dart';
import 'package:web_socket_channel/io.dart';
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
  final WebSocketChannel channel =
      IOWebSocketChannel.connect('ws://192.168.15.25:12347/ws/1');

  List<double> messages = List<double>.generate(10, (index) => 0);

  @override
  void initState() {
    super.initState();

    channel.stream.listen(
      (message) {
        Map<String, dynamic> data = jsonDecode(message);
        print(message);

        setState(() {
          if (messages.length >= 10) {
            messages = messages.sublist(1);
          }
          messages.add(data["message"]);
        });
      },
      onError: (error) => print(error),
    );
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
          title: Text('WebSocket Example'),
        ),
        body: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: <Widget>[
              // for (var message in messages) Text(message.toString()),
              // SizedBox(height: 16.0),
              SfCartesianChart(
                // animationDuration: Duration.zero,
                primaryXAxis:
                    CategoryAxis(visibleMinimum: 0, visibleMaximum: 9),
                primaryYAxis: NumericAxis(minimum: 0, maximum: maxV),
                series: [
                  LineSeries<Pair<int, double>, int>(
                    dataSource: _getData(),
                    xValueMapper: (data, _) => data.first,
                    yValueMapper: (data, _) => data.second,
                    animationDuration: 0,
                  )
                ],
              ),
            ],
          ),
        ),
      ),
    );
  }

  @override
  void dispose() {
    channel.sink.close();
    super.dispose();
  }
}
