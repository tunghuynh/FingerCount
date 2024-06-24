/* 
   ================================================================
   LƯU Ý: NGẮT CHÂN RX, TX CỦA HC-05 RA KHỎI UNO TRƯỚC KHI NẠP CODE
   ================================================================
*/

// Định nghĩa các chân kết nối LED 7 đoạn
const int a = 6;
const int b = 7;
const int c = 8;
const int d = 9;
const int e = 10;
const int f = 11;
const int g = 12;

// Định nghĩa các chân kết nối 5 bóng LED
const int led1 = 2;
const int led2 = 3;
const int led3 = 4;
const int key = 5;

int number[10][8] = {
  {0,0,0,0,0,0,1,1},//0
  {1,0,0,1,1,1,1,1},//1
  {0,0,1,0,0,1,0,1},//2
  {0,0,0,0,1,1,0,1},//3
  {1,0,0,1,1,0,0,1},//4
  {0,1,0,0,1,0,0,1},//5
  {0,1,0,0,0,0,0,1},//6
  {0,0,0,1,1,1,1,1},//7
  {0,0,0,0,0,0,0,1},//8
  {0,0,0,0,1,0,0,1}//9
 };


void numberShow(int i){
  if (i<0 || i >9) {
    i = 0;
  }
  for(int pin = 6; pin <= 12 ; pin++){
    digitalWrite(pin, number[i][pin-6]);
  }
}

void setup() {
  Serial.begin(9600);
  // Đặt các chân LED 7 đoạn là output
  pinMode(a, OUTPUT);

  pinMode(b, OUTPUT);
  pinMode(c, OUTPUT);
  pinMode(d, OUTPUT);
  pinMode(e, OUTPUT);
  pinMode(f, OUTPUT);
  pinMode(g, OUTPUT);

  // Đặt các chân 5 bóng LED là output
  pinMode(led1, OUTPUT);
  pinMode(led2, OUTPUT);
  pinMode(led3, OUTPUT);
  pinMode(key, OUTPUT);
  
  digitalWrite(key, HIGH);//HIGH: Data mode; LOW: Command mode
}

void loop() {
    if (Serial.available() > 0) {
    String data = Serial.readStringUntil('\n'); // Read the incoming data
    data.trim();
    numberShow(data.toInt());

    if (data.equalsIgnoreCase("1")){
      digitalWrite(led1, HIGH);
      digitalWrite(led2, LOW);
      digitalWrite(led3, LOW);
    }else if (data.equalsIgnoreCase("2")){
      digitalWrite(led1, LOW);
      digitalWrite(led2, HIGH);
      digitalWrite(led3, LOW);
    }else if (data.equalsIgnoreCase("3")){
      digitalWrite(led1, LOW);
      digitalWrite(led2, LOW);
      digitalWrite(led3, HIGH);
    }else if (data.equalsIgnoreCase("4")){
      digitalWrite(led1, HIGH);
      delay(50);
      digitalWrite(led1, LOW);
      digitalWrite(led2, HIGH);
      delay(50);
      digitalWrite(led2, LOW);
      digitalWrite(led3, HIGH);
      delay(50);
      digitalWrite(led3, LOW);
    }else if (data.equalsIgnoreCase("5")){
      digitalWrite(led1, HIGH);
      digitalWrite(led2, HIGH);
      digitalWrite(led3, HIGH);
      delay(50);
      digitalWrite(led1, LOW);
      digitalWrite(led2, LOW);
      digitalWrite(led3, LOW);
    }else{
      digitalWrite(led1, LOW);
      digitalWrite(led2, LOW);
      digitalWrite(led3, LOW);
    }
    Serial.println("Received: " + data); // Print the received data
  }
}
