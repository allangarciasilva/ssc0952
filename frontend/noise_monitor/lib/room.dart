import 'package:flutter/material.dart';
import 'package:flutter/material.dart';
import 'package:syncfusion_flutter_charts/charts.dart';
import 'package:web_socket_channel/web_socket_channel.dart';

class RoomScreen extends StatefulWidget {
  const RoomScreen({super.key, required this.roomName});

  final String roomName;

  @override
  // ignore: library_private_types_in_public_api
  _RoomScreenState createState() => _RoomScreenState();
}

class _RoomScreenState extends State<RoomScreen> {
  @override
  Widget build(BuildContext context) {
    return Center(
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
    );
  }

  @override
  void dispose() {
    super.dispose();
  }
}
