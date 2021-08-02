/*************************************************************************
  License GPL-3.0
  Copyright (c) 2020 Petar Crnjak
  License file :
  https://github.com/PCrnjak/S_Drive---small-BLDC-driver/blob/master/LICENSE
**************************************************************************/

/*************************************************************************
  Created by: Petar Crnjak
  Version: 1.0
  Date: 21.3.2021.
**************************************************************************/

/*************************************************************************
  https://www.pjrc.com/store/teensy41.html Datasheet for teensy 4.1
  This code runs on motherboard of CM series of robotic arms.
  Some of the functions of this code are:
  * Act as a point where all Driver data is being sent and and then passed to PC thru only one serial line.
  * So in CM6 example we have 6 joints and each is connected to one of 6 serial ports of teensy 4.1 ( of 8)
    Drivers send data every 10 ms and this code then packs data from all 6 joints and sends them thru USB to master PC.
  * Act as a safety mechanism in case of errors, driver disconnects, Estpo triggers, external interrupts, temperature errors
  
**************************************************************************/



// IMPORTANT CHANGE THIS TO THE NUMBER OF JOINTS OF YOUR ROBOT!!!
# define Joint_num 6

int motor[Joint_num][6]; // Here is stored data from "Get_input" functions. Stored as they come:
                         // data in order: position, current, speed, temperature, voltage, error.
                         //  data is stored as int values
                         
byte data_coming = 0; // Indicates if data is comming or not. 0 for not comming 1 for comming.
/*****************************************************************************
  Use dummy data to test if you dont have drivers available
  data in order: position,current,speed,temperature,voltage,error
******************************************************************************/
int dummy_motor[6][6] = {{1000, 100, 10, 15, 1500, 1}, {2000, 200, 20, 25, 2400, 1}, {3000, 300, 30, 35, 3400, 1}, {4000, 400, 40, 45, 4500, 1}, {5000, 500, 50, 55, 5400, 1}, {6000, 600, 67, 65, 6500, 1}};



void setup() {
  pinMode(LED_BUILTIN, OUTPUT);

  // Begin serial communications 
  Serial.begin(10000000);
  Serial1.begin(1000000);
  Serial2.begin(1000000);
  Serial3.begin(1000000);
  Serial4.begin(1000000);
  Serial5.begin(1000000);
  Serial6.begin(1000000);
  //Serial7.begin(1000000);
  //Serial8.begin(1000000);

  // Check why i did this ?!?! xD
  Serial.setTimeout(40);
  delay(100);

  Serial1.print("b"); Serial1.print("\n");
  delay(300);
  Serial2.print("b"); Serial2.print("\n");
  delay(300);
  Serial3.print("b"); Serial3.print("\n");
  delay(300);
  Serial4.print("b"); Serial4.print("\n");
  delay(300);
  Serial5.print("b"); Serial5.print("\n");
  delay(300);
  Serial6.print("b"); Serial6.print("\n");

  // mozda ga sjebu oni # koji pošalje ili motor setup stringovi
  // Whitout this it does not work so just leave it
  // Startup delay reads motor data for x micro seconds but does not forward it to usb serial.
  // Without this data gets corrupted or does not even work so leave it atm until this bug is fixed.
  // Possible solutions:
  // * drivers send # after we send b so maybe that breaks it ?
  // * possible motor setup strings that guide us thru setup ?
  startup_delay(1500000);

}

void loop() {

  // Gets motor data and save to motor[x] variable 
  Get_input1(Serial1, motor[0]);
  Get_input2(Serial2, motor[1]);
  Get_input3(Serial3, motor[2]);
  Get_input4(Serial4, motor[3]);
  Get_input5(Serial5, motor[4]);
  Get_input6(Serial6, motor[5]);

  // Pack all received data from Get_input functions and send to PC serial!
  Motors_data_pack_send(20000); 
  
  // Unpack data we received from PC serial and send it to specific driver!
  PC_data_unpack_send();

  // Check if we are connected to PC serial. We need to get any data usefull data every 10 ms from PC. 
  // If we dont get that data from PC for 60ms signal that we are no longer connected and it is error.
  check_if_connected(80000); //60ms

}


/*****************************************************************************
  Pin definitions
  They are specific for S-drive V3 dont change them.
******************************************************************************/

// Do this every x ms !!
// Send data from all motors to PC every 10ms
void Motors_data_pack_send(uint32_t sample_time) {

  static uint32_t previousMicros_ = 0;
  uint32_t currentMicros_ = micros();
  int voltage_mean = 0;

  if (currentMicros_ - previousMicros_ >= sample_time) {
    previousMicros_ = currentMicros_;

    // i = rows(data elements), j = columns(motor number)
    for (int i = 0; i < 4 ; i++) { // only 4 here since we are sending position, speed, current and temperature
      for (int j = 0; j < Joint_num ; j++) {
        Serial.print(motor[j][i]);
        Serial.print(",");

      }
    }

    for (int i = 0; i < Joint_num ; i++) {
      voltage_mean = motor[i][4] + voltage_mean;
    }

    voltage_mean = voltage_mean / 3;
    Serial.print(voltage_mean);
    Serial.print(",");
    int Error_temp = 0;
    Serial.print(Error_temp);
    Serial.print("\n");

  }
}


/*****************************************************************************
  Pin definitions
  They are specific for S-drive V3 dont change them.
******************************************************************************/

// Geta data from PC and send it to motors instantly
void PC_data_unpack_send() {

  if (Serial.available()) {
    data_coming = 1;
    digitalWrite(LED_BUILTIN, LOW);

    String PC_out_string = Serial.readStringUntil('\n'); // Read string until '\n'
    int Joint_to_send = PC_out_string[1] - '0'; // This stuff converts ASCII number in this case PC_out_string[1] to int
    PC_out_string.remove(1, 1); // Remove joint number from our data string to prepare it to be forwarded to appropriate joint

    switch (Joint_to_send) {
      case 1: //Joint 1
        Serial1.print(PC_out_string);
        Serial1.print('\n');
        break;
      case 2: //Joint 2
        Serial2.print(PC_out_string);
        Serial2.print('\n');
        break;
      case 3: //Joint 3
        Serial3.print(PC_out_string);
        Serial3.print('\n');
        break;
      case 4: //Joint 4
        Serial4.print(PC_out_string);
        Serial4.print('\n');
        break;
      case 5: //Joint 5
        Serial5.print(PC_out_string);
        Serial5.print('\n');
        break;
      case 6: //Joint 6
        Serial6.print(PC_out_string);
        Serial6.print('\n');
        //
        break;

    }
  }
}


/*****************************************************************************
  Pin definitions
  They are specific for S-drive V3 dont change them.
******************************************************************************/

void check_if_connected(uint32_t sample_time) {

  static uint32_t previousMicros_ = 0;
  uint32_t currentMicros_ = micros();

  if (data_coming == 1) {
    previousMicros_ = currentMicros_;

  }

  if (currentMicros_ - previousMicros_ >= sample_time) {
    previousMicros_ = currentMicros_;
    digitalWrite(LED_BUILTIN, HIGH);
  }
  data_coming = 0;


}



/*****************************************************************************
  Pin definitions
  They are specific for S-drive V3 dont change them.
******************************************************************************/

void startup_delay(uint32_t sample_time) {
  static bool var = 0;
  while (var == 0) {
    static uint32_t previousMicros_c = 0;
    uint32_t currentMicros_c = micros();
    Get_input1(Serial1, motor[0]);
    Get_input2(Serial2, motor[1]);
    Get_input3(Serial3, motor[2]); /// motor 2?
    Get_input4(Serial4, motor[3]);
    Get_input5(Serial5, motor[4]);
    Get_input6(Serial6, motor[5]); /// motor 2?
    if (currentMicros_c - previousMicros_c >= sample_time) {
      previousMicros_c = currentMicros_c;
      var = 1;
    }
  }
}
