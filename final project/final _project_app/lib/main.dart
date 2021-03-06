import 'package:flutter/material.dart';
import 'package:just_audio/just_audio.dart';
import 'dart:math';
import 'dart:io';
import 'sound_player.dart';
import 'sound_recorder.dart';
import 'package:path_provider/path_provider.dart' as path_provider;
import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:path/path.dart';
import 'package:flutter_downloader/flutter_downloader.dart';
import 'package:just_audio/just_audio.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      initialRoute: '/',
      routes: {
        '/': (context) => MainPage(),
      },
    );
  }
}

class MainPage extends StatefulWidget {
  const MainPage({Key? key}) : super(key: key);

  @override
  State<MainPage> createState() => _MainPage();
}

class _MainPage extends State<MainPage> {
  // get SoundRecorder
  final recorder = SoundRecorder();
  // get soundPlayer
  final player = SoundPlayer();

  // create new audio player
  final ja_player = AudioPlayer();

  CaseType casetype = new CaseType();
  String result = '';
  String curType = '';
  bool Check_type = false;
  Random objectname = Random();
  @override
  void initState() {
    super.initState();
    recorder.init();
    player.init();
  }

  @override
  void dispose() {
    recorder.dispose();
    player.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: Scaffold(
        appBar: AppBar(
          title: Center(
            child: Text('119'),
          ),
        ),
        body: Column(
          children: [
            Flexible(
              flex: 10,
              child: Container(
                child: ListView.builder(
                  itemCount: Check_type
                      ? casetype.questions[curType].length
                      : casetype.types.length,
                  scrollDirection: Axis.vertical,
                  itemBuilder: (BuildContext context, int index) {
                    return Padding(
                      padding: const EdgeInsets.all(10),
                      child: CheckboxListTile(
                          title: Text(Check_type
                              ? casetype.questions[curType][index]
                              : casetype.types[index]),
                          value: Check_type
                              ? casetype.questions_checked[curType][index]
                              : casetype.isChecked[index],
                          onChanged: (bool? value) {
                            if (Check_type) {
                              casetype.questions_checked[curType][index] =
                                  value!;
                            } else {
                              casetype.isChecked[index] = value!;
                            }
                          }),
                    );
                  },
                ),
              ),
            ),
            Flexible(child: Center(child: buildOutputField())),
            Flexible(child: Center(child: buildRecord())),
            Flexible(
                child: Center(
              child: ElevatedButton.icon(
                style: ElevatedButton.styleFrom(
                  minimumSize: const Size(175, 50),
                  primary: Colors.red,
                  onPrimary: Colors.white,
                ),
                icon: Icon(Icons.autorenew),
                label: Text(
                  'RESET',
                  // 設定字體大小及字體粗細（bold粗體，normal正常體）
                  style: const TextStyle(
                      fontSize: 16, fontWeight: FontWeight.bold),
                ),
                onPressed: () {
                  setState(() {
                    init_setting();
                  });
                },
              ),
            )),
          ],
        ),
      ),
    );
  }

  Widget buildRecord() {
    // whether is recording
    final isRecording = !recorder.isRecording;
    final icon = !isRecording ? Icons.stop : Icons.mic;
    final primary = !isRecording ? Colors.red : Colors.white;
    final text = !isRecording ? 'STOP' : 'START';
    final onPrimary = !isRecording ? Colors.white : Colors.black;

    return ElevatedButton.icon(
      style: ElevatedButton.styleFrom(
        minimumSize: const Size(175, 50),
        primary: primary,
        onPrimary: onPrimary,
      ),
      icon: Icon(icon),
      label: Text(
        text,
        // 設定字體大小及字體粗細（bold粗體，normal正常體）
        style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
      ),
      onPressed: () async {
        Directory tempDir = await path_provider.getTemporaryDirectory();
        // define file directory
        String path = '${tempDir.path}/SpeechRecognition.wav';
        // 控制開始錄音或停止錄音
        await recorder.toggleRecording(path);
        isRecording ? setTxt('Recording...') : setTxt('Processing...');

        if (!isRecording) {
          Future<String> response;
          if (curType == "車禍") {
            response =
                upload(File(path), 'http://140.116.246.16:5000/upload/crash');
          } else if (curType == "火災") {
            response =
                upload(File(path), 'http://140.116.246.16:5000/upload/fire');
          } else if (curType == "昏迷") {
            response =
                upload(File(path), 'http://140.116.246.16:5000/upload/faint');
          } else {
            response =
                upload(File(path), 'http://140.116.246.16:5000/upload/init');
          }

          String resStr = await response;
          print("result: " + resStr);
          Map<String, dynamic> resJSON =
              jsonDecode(resStr).cast<String, String>();
          print(resJSON);
          var duration = await ja_player.setAudioSource(
              AudioSource.uri(Uri.parse(resJSON['responseMedia'])));
          ja_player.play();

          var r = resJSON['result'];
          if (Check_type == false) {
            if (r.contains('火災')) {
              casetype.isChecked[0] = true;
              curType = '火災';
              Check_type = true;
            } else if (r.contains('車禍')) {
              casetype.isChecked[1] = true;
              curType = '車禍';
              Check_type = true;
            } else if (r.contains('失去意識')) {
              casetype.isChecked[2] = true;
              curType = '昏迷';
              Check_type = true;
            } else {
              print("無法判別");
            }
          } else {
            if (r.contains('已確認有人受困於現場')) {
              casetype.questions_checked[curType][0] = true;
            } else if (r.contains('已確認現場無易燃物')) {
              casetype.questions_checked[curType][1] = true;
            } else if (r.contains('已確認現場有緊急出口')) {
              casetype.questions_checked[curType][2] = true;
            } else if (r.contains('已確認現場有緩降機')) {
              casetype.questions_checked[curType][3] = true;
            } else if (r.contains('確認人員都在安全處')) {
              casetype.questions_checked[curType][0] = true;
            } else if (r.contains('已確認現場有醫護箱')) {
              casetype.questions_checked[curType][1] = true;
            } else if (r.contains('已確認現場傷者皆有意識')) {
              casetype.questions_checked[curType][2] = true;
            } else if (r.contains('已確認現場無人員重傷')) {
              casetype.questions_checked[curType][3] = true;
            } else if (r.contains('確認人員有呼吸心跳')) {
              casetype.questions_checked[curType][0] = true;
            } else if (r.contains('確認人員目前平躺')) {
              casetype.questions_checked[curType][1] = true;
            } else if (r.contains('已確認傷者在陰涼處')) {
              casetype.questions_checked[curType][2] = true;
            } else if (r.contains('已確認傷者無呼吸困難')) {
              casetype.questions_checked[curType][3] = true;
            } else if (r.contains('已確認傷者恢復意識')) {
              casetype.questions_checked[curType][4] = true;
            }
          }
          setTxt(r);
        }
        setState(() {
          recorder.isRecording;
        });
      },
    );
  }

  void init_setting() {
    casetype = new CaseType();
    result = '';
    curType = '';
    Check_type = false;
  }

  void Random_type() {
    int num = objectname.nextInt(casetype.types.length);
    result = casetype.types[num];
    curType = result;
  }

  void Random_answer() {
    int num = objectname.nextInt(casetype.questions[curType].length);
    result = casetype.questions[curType][num];
  }

  void Step1_type() {
    for (int i = 0; i < casetype.types.length; i++) {
      if (result == casetype.types[i]) {
        casetype.isChecked[i] = true;
        Check_type = true;
      } else {
        casetype.isChecked[i] = false;
      }
    }
  }

  void Step2_question() {
    for (int i = 0; i < casetype.questions[curType].length; i++) {
      if (result == casetype.questions[curType][i]) {
        casetype.questions_checked[curType][i] = true;
      }
    }
  }

  final TextEditingController myController = new TextEditingController();

  void setTxt(taiTxt) {
    setState(() {
      myController.text = taiTxt;
    });
  }

  Widget buildOutputField() {
    return Padding(
      padding: const EdgeInsets.only(left: 40, right: 40),
      child: TextField(
        controller: myController, // 設定 controller
        enabled: false, // 設定不能接受輸入
        decoration: const InputDecoration(
          fillColor: Colors.white, // 背景顏色，必須結合filled: true,才有效
          filled: true, // 重點，必須設定為true，fillColor才有效
          disabledBorder: OutlineInputBorder(
            borderRadius: BorderRadius.all(Radius.circular(10)), // 設定邊框圓角弧度
            borderSide: BorderSide(
              color: Colors.black87, // 設定邊框的顏色
              width: 2.0, // 設定邊框的粗細
            ),
          ),
        ),
      ),
    );
  }

  void _requestDownload(String url, String savedDir) async {
    final taskId = await FlutterDownloader.enqueue(
        url: url, savedDir: savedDir, showNotification: true);
  }

  Future play(String pathToReadAudio) async {
    await player.play(pathToReadAudio);
    setState(() {
      player.init();
      player.isPlaying;
    });
  }

  Future<String> upload(File speechFile, String url) async {
    var stream = new http.ByteStream(speechFile.openRead());
    var length = await speechFile.length();
    var uri = Uri.parse(url);
    var request = new http.MultipartRequest("POST", uri);
    var multipartFile = new http.MultipartFile('file', stream, length,
        filename: basename(speechFile.path));
    request.files.add(multipartFile);
    var response = await request.send();

    print(response.statusCode);
    String return_str = await response.stream.transform(utf8.decoder).join();
    return return_str;
  }
}

class CheckItem extends StatelessWidget {
  CheckItem({
    Key? key,
    required this.isChecked,
    required this.plot,
  }) : super(key: key);
  bool isChecked;
  String plot;

  @override
  Widget build(BuildContext context) {
    return CheckboxListTile(
        title: Text(plot),
        value: isChecked,
        onChanged: (bool? value) {
          isChecked = value!;
        });
  }
}

class CaseType {
  final List<String> types = [
    '火災',
    '車禍',
    '昏迷',
  ];
  final List<bool> isChecked = [
    false,
    false,
    false,
  ];
  final Map questions = {
    '火災': Question.fire,
    '車禍': Question.traffic,
    '昏迷': Question.unconscious,
  };
  final Map questions_checked = {
    '火災': Question.fire_isChecked,
    '車禍': Question.traffic_isChecked,
    '昏迷': Question.unconscious_isChecked,
  };
}

class Question {
  static final List<String> traffic = [
    '事故相關人員是否已移動至安全處',
    '現場是否存在緊急醫護箱等器材',
    '人員是否還有意識，若喪失意識是否還有呼吸、心跳',
    '是否有呼吸困難、出血、骨折等症狀，有的話是否有物品可以緊急處置',
  ];
  static final List<String> fire = [
    '火災現場是否有人受困在內，受困人員是否還有意識',
    '火災現場是否有易燃物',
    '火災現場是否有緊急出口可以使用',
    '是否有緩降機等設備能讓人員逃生',
  ];
  static final List<String> unconscious = [
    '傷者是否還有呼吸、心跳，若否，現場是否有人會 CPR 急救或現場是否有 AED 器材',
    '傷者是否能平躺於某處、並將傷者腳部抬高',
    '傷者是否在陰涼處，若否，是否能移動到陰涼處',
    '傷者是否呼吸困難，若是，是否能改成坐姿',
    '傷者是否有恢復意識，或傷者呼吸、心跳是否有持續減弱',
  ];
  static final List<bool> traffic_isChecked = [
    false,
    false,
    false,
    false,
  ];
  static final List<bool> fire_isChecked = [
    false,
    false,
    false,
    false,
  ];
  static final List<bool> unconscious_isChecked = [
    false,
    false,
    false,
    false,
    false,
  ];
}
