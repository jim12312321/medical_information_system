import 'package:flutter/material.dart';
import 'dart:math';

void main() async{
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context){
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

  CaseType casetype = new CaseType();
  String result = '';
  String curType = '';
  bool Check_type = false;
  Random objectname = Random();
  @override
  Widget build(BuildContext context){
    return MaterialApp(
      home: Scaffold(
        appBar: AppBar(
          title: Center(child: Text('119'),),
        ),
        body: Column(
          children: [
            Flexible(
              flex: 10,
              child: Container(
              child: ListView.builder(
                itemCount: Check_type? casetype.questions[curType].length : casetype.types.length,
                scrollDirection: Axis.vertical,
                itemBuilder: (BuildContext context, int index) {
                  return Padding(
                    padding: const EdgeInsets.all(10),
                    child: CheckboxListTile(
                        title: Text(Check_type?casetype.questions[curType][index]:casetype.types[index]),
                        value: Check_type?casetype.questions_checked[curType][index]:casetype.isChecked[index],
                        onChanged: (bool? value){
                          if (Check_type)
                            {
                              casetype.questions_checked[curType][index] = value!;
                            }
                          else
                            {
                              casetype.isChecked[index] = value!;
                          }
                        }
                    ),
                  );
                },
              ),
              ),
            ),
            Flexible(child: Center(child: buildOutputField())),
            Flexible(child: Center(child: buildRecord())),
            Flexible(child: Center(
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
                    style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
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
  bool isRecording = false;
  Widget buildRecord() {
    final icon = isRecording ? Icons.stop : Icons.mic;
    final primary = isRecording ? Colors.red : Colors.white;
    final text = isRecording ? 'STOP' : 'START';
    final onPrimary = isRecording ? Colors.white : Colors.black;

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
      onPressed: () {
        setState(() {
          isRecording = isRecording?false:true;
        });
        print(Check_type);
        print(isRecording);
        if (!Check_type && !isRecording)
          {
            print("enter1");
            Random_type();
          }
        else if (!isRecording)
          {
            print("enter2");
            Random_answer();
          }
        print(curType+" : "+result);
        isRecording?setTxt('錄音中'):setTxt('結束錄音，辨識結果為: '+result);
        if (!isRecording)
          {
            if (casetype.types.contains(result))
              {
                print("step1");
                Step1_type();
              }
            else
              {
                print("step2");
                Step2_question();
              }
          }

      },
    );
  }

  void init_setting(){
    casetype = new CaseType();
    result = '';
    curType = '';
    Check_type = false;
    isRecording = false;
  }

  void Random_type(){
    int num = objectname.nextInt(casetype.types.length);
    result = casetype.types[num];
    curType = result;
  }
  void Random_answer(){
    int num = objectname.nextInt(casetype.questions[curType].length);
    result = casetype.questions[curType][num];
  }
  void Step1_type(){
    for (int i =0;i<casetype.types.length;i++)
    {
      if (result == casetype.types[i])
      {
        casetype.isChecked[i] = true;
        Check_type = true;
      }
      else
      {
        casetype.isChecked[i] = false;
      }
    }
  }
  void Step2_question(){

    for (int i =0;i<casetype.questions[curType].length;i++)
    {
      if (result == casetype.questions[curType][i])
      {
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
}
class CheckItem extends StatelessWidget{
  CheckItem({
    Key? key,
    required this.isChecked,
    required this.plot,
  }) : super (key : key);
  bool isChecked;
  String plot;

  @override
  Widget build(BuildContext context) {
    return CheckboxListTile(
      title: Text(plot),
        value: isChecked,
        onChanged: (bool? value){
          isChecked = value!;
        }
    );

  }

}

class CaseType{
  final List<String> types = [
    '火災',
    '車禍',
    '昏迷',
  ];
  final List<bool> isChecked =[
    false,
    false,
    false,
  ];
  final Map questions = {
    '火災': Question.fire,
    '車禍':Question.traffic,
    '昏迷':Question.unconscious,
  };
  final Map questions_checked = {
    '火災': Question.fire_isChecked,
    '車禍':Question.traffic_isChecked,
    '昏迷':Question.unconscious_isChecked,
  };
}

class Question{
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
  static final List<bool> traffic_isChecked =[
    false,
    false,
    false,
    false,
  ];
  static final List<bool> fire_isChecked =[
    false,
    false,
    false,
    false,
  ];
  static final List<bool> unconscious_isChecked =[
    false,
    false,
    false,
    false,
    false,
  ];
}
