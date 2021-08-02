void Get_input1(Stream &serialport, int *data_) {

  static uint8_t i_ = 0;
  static uint8_t i2 = 0;
  static char data[30];
  static char data2[30];
  static uint8_t comma = 1;
  static bool flag_2 = 0;

  // 6 vars i svi su int
  static int out1_ ;
  static int out2_ ;
  static int out3_ ;
  static int out4_ ;
  static int out5_ ;
  static int out6_ ;


  if (serialport.available() > 0) {

    data[i_] = serialport.read();

    if (data[i_] == 't') {
      flag_2 = 1;
    }
    if ( data[i_] == '\n') {
      flag_2 = 0;
    }

    if (i_ != 0) {
      switch (data[0]) {

        /*****************************************************************************
          GOTO position and hold (with error comp)
        ******************************************************************************/
        case 't':
          data2[i2 - 1] = data[i_];

          if (data[i_]  == '\n' and comma == 6) {
            data[i_] = '\0';
            data2[i2 - 1] = data[i_];
            out6_ = atoi(data2);
            data_[5] = out6_;
            data_[4] = out5_;
            data_[3] = out4_;
            data_[2] = out3_;
            data_[1] = out2_;
            data_[0] = out1_;

            //Serial.println(Position_var);
            comma = 1 ;
            i2 = 0;
            i_ = 0;

          }

          if (data[i_]  == ',' and comma == 5) {
            data[i_] = '\0';
            data2[i2 - 1] = data[i_];
            out5_ = atoi(data2);
            comma = comma + 1 ;
            i2 = 0;
          }


          if (data[i_]  == ',' and comma == 4) {
            data[i_] = '\0';
            data2[i2 - 1] = data[i_];
            out4_ = atoi(data2);
            comma = comma + 1 ;
            i2 = 0;
          }


          if (data[i_]  == ',' and comma == 3) {
            data[i_] = '\0';
            data2[i2 - 1] = data[i_];
            out3_ = atoi(data2);
            comma = comma + 1 ;
            i2 = 0;
          }

          if (data[i_]  == ',' and comma == 2) {
            data[i_] = '\0';
            data2[i2 - 1] = data[i_];
            out2_ = atoi(data2);
            comma = comma + 1 ;
            i2 = 0;
          }


          if (data[i_]  == ',' and comma == 1) {
            data[i_] = '\0';
            data2[i2 - 1] = data[i_];
            out1_ = atoi(data2);
            comma = comma + 1 ;
            i2 = 0;
          }

          break;

      }
    }
    if (flag_2 == 1) {
      i_ = i_ + 1;
      i2 = i2 + 1;
    }
    if (flag_2 == 0) {
      i_ = 0;
      i2 = 0;
      comma = 1 ;
    }


  }
}

void Get_input2(Stream &serialport, int *data_) {

  static uint8_t i_ = 0;
  static uint8_t i2 = 0;
  static char data[30];
  static char data2[30];
  static uint8_t comma = 1;
  static bool flag_2 = 0;

  // 6 vars i svi su int
  static int out1_ = 0;
  static int out2_ = 0;
  static int out3_ = 0;
  static int out4_ = 0;
  static int out5_ = 0;
  static int out6_ = 0;


  if (serialport.available() > 0) {

    data[i_] = serialport.read();

    if (data[i_] == 't') {
      flag_2 = 1;
    }
    if ( data[i_] == '\n') {
      flag_2 = 0;
    }

    if (i_ != 0) {
      switch (data[0]) {

        /*****************************************************************************
          GOTO position and hold (with error comp)
        ******************************************************************************/
        case 't':
          data2[i2 - 1] = data[i_];

          if (data[i_]  == '\n' and comma == 6) {
            data[i_] = '\0';
            data2[i2 - 1] = data[i_];
            out6_ = atoi(data2);

            data_[5] = out6_;
            data_[4] = out5_;
            data_[3] = out4_;
            data_[2] = out3_;
            data_[1] = out2_;
            data_[0] = out1_;
            comma = 1 ;
            i2 = 0;
            i_ = 0;

          }

          if (data[i_]  == ',' and comma == 5) {
            data[i_] = '\0';
            data2[i2 - 1] = data[i_];
            out5_ = atoi(data2);
            comma = comma + 1 ;
            i2 = 0;
          }


          if (data[i_]  == ',' and comma == 4) {
            data[i_] = '\0';
            data2[i2 - 1] = data[i_];
            out4_ = atoi(data2);
            comma = comma + 1 ;
            i2 = 0;
          }


          if (data[i_]  == ',' and comma == 3) {
            data[i_] = '\0';
            data2[i2 - 1] = data[i_];
            out3_ = atoi(data2);
            comma = comma + 1 ;
            i2 = 0;
          }

          if (data[i_]  == ',' and comma == 2) {
            data[i_] = '\0';
            data2[i2 - 1] = data[i_];
            out2_ = atoi(data2);
            comma = comma + 1 ;
            i2 = 0;
          }


          if (data[i_]  == ',' and comma == 1) {
            data[i_] = '\0';
            data2[i2 - 1] = data[i_];
            out1_ = atoi(data2);
            comma = comma + 1 ;
            i2 = 0;
          }

          break;

      }
    }
    if (flag_2 == 1) {
      i_ = i_ + 1;
      i2 = i2 + 1;
    }
    if (flag_2 == 0) {
      i_ = 0;
      i2 = 0;
      comma = 1 ;
    }


  }
}

void Get_input3(Stream &serialport, int *data_) {

  static uint8_t i_ = 0;
  static uint8_t i2 = 0;
  static char data[30];
  static char data2[30];
  static uint8_t comma = 1;
  static bool flag_2 = 0;

  // 6 vars i svi su int
  static int out1_ = 0;
  static int out2_ = 0;
  static int out3_ = 0;
  static int out4_ = 0;
  static int out5_ = 0;
  static int out6_ = 0;


  if (serialport.available() > 0) {

    data[i_] = serialport.read();

    if (data[i_] == 't') {
      flag_2 = 1;
    }
    if ( data[i_] == '\n') {
      flag_2 = 0;
    }

    if (i_ != 0) {
      switch (data[0]) {

        case 't':
          data2[i2 - 1] = data[i_];

          if (data[i_]  == '\n' and comma == 6) {
            data[i_] = '\0';
            data2[i2 - 1] = data[i_];
            out6_ = atoi(data2);

            data_[5] = out6_;
            data_[4] = out5_;
            data_[3] = out4_;
            data_[2] = out3_;
            data_[1] = out2_;
            data_[0] = out1_;
            //Serial.println(Position_var);
            comma = 1 ;
            i2 = 0;
            i_ = 0;

          }

          if (data[i_]  == ',' and comma == 5) {
            data[i_] = '\0';
            data2[i2 - 1] = data[i_];
            out5_ = atoi(data2);
            comma = comma + 1 ;
            i2 = 0;
          }


          if (data[i_]  == ',' and comma == 4) {
            data[i_] = '\0';
            data2[i2 - 1] = data[i_];
            out4_ = atoi(data2);
            comma = comma + 1 ;
            i2 = 0;
          }


          if (data[i_]  == ',' and comma == 3) {
            data[i_] = '\0';
            data2[i2 - 1] = data[i_];
            out3_ = atoi(data2);
            comma = comma + 1 ;
            i2 = 0;
          }

          if (data[i_]  == ',' and comma == 2) {
            data[i_] = '\0';
            data2[i2 - 1] = data[i_];
            out2_ = atoi(data2);
            comma = comma + 1 ;
            i2 = 0;
          }


          if (data[i_]  == ',' and comma == 1) {
            data[i_] = '\0';
            data2[i2 - 1] = data[i_];
            out1_ = atoi(data2);
            comma = comma + 1 ;
            i2 = 0;
          }

          break;

      }
    }
    if (flag_2 == 1) {
      i_ = i_ + 1;
      i2 = i2 + 1;
    }
    if (flag_2 == 0) {
      i_ = 0;
      i2 = 0;
      comma = 1 ;
    }


  }
}


void Get_input4(Stream &serialport, int *data_) {

  static uint8_t i_ = 0;
  static uint8_t i2 = 0;
  static char data[30];
  static char data2[30];
  static uint8_t comma = 1;
  static bool flag_2 = 0;

  // 6 vars i svi su int
  static int out1_ ;
  static int out2_ ;
  static int out3_ ;
  static int out4_ ;
  static int out5_ ;
  static int out6_ ;


  if (serialport.available() > 0) {

    data[i_] = serialport.read();

    if (data[i_] == 't') {
      flag_2 = 1;
    }
    if ( data[i_] == '\n') {
      flag_2 = 0;
    }

    if (i_ != 0) {
      switch (data[0]) {

        /*****************************************************************************
          GOTO position and hold (with error comp)
        ******************************************************************************/
        case 't':
          data2[i2 - 1] = data[i_];

          if (data[i_]  == '\n' and comma == 6) {
            data[i_] = '\0';
            data2[i2 - 1] = data[i_];
            out6_ = atoi(data2);
            data_[5] = out6_;
            data_[4] = out5_;
            data_[3] = out4_;
            data_[2] = out3_;
            data_[1] = out2_;
            data_[0] = out1_;

            //Serial.println(Position_var);
            comma = 1 ;
            i2 = 0;
            i_ = 0;

          }

          if (data[i_]  == ',' and comma == 5) {
            data[i_] = '\0';
            data2[i2 - 1] = data[i_];
            out5_ = atoi(data2);
            comma = comma + 1 ;
            i2 = 0;
          }


          if (data[i_]  == ',' and comma == 4) {
            data[i_] = '\0';
            data2[i2 - 1] = data[i_];
            out4_ = atoi(data2);
            comma = comma + 1 ;
            i2 = 0;
          }


          if (data[i_]  == ',' and comma == 3) {
            data[i_] = '\0';
            data2[i2 - 1] = data[i_];
            out3_ = atoi(data2);
            comma = comma + 1 ;
            i2 = 0;
          }

          if (data[i_]  == ',' and comma == 2) {
            data[i_] = '\0';
            data2[i2 - 1] = data[i_];
            out2_ = atoi(data2);
            comma = comma + 1 ;
            i2 = 0;
          }


          if (data[i_]  == ',' and comma == 1) {
            data[i_] = '\0';
            data2[i2 - 1] = data[i_];
            out1_ = atoi(data2);
            comma = comma + 1 ;
            i2 = 0;
          }

          break;

      }
    }
    if (flag_2 == 1) {
      i_ = i_ + 1;
      i2 = i2 + 1;
    }
    if (flag_2 == 0) {
      i_ = 0;
      i2 = 0;
      comma = 1 ;
    }


  }
}

void Get_input5(Stream &serialport, int *data_) {

  static uint8_t i_ = 0;
  static uint8_t i2 = 0;
  static char data[30];
  static char data2[30];
  static uint8_t comma = 1;
  static bool flag_2 = 0;

  // 6 vars i svi su int
  static int out1_ ;
  static int out2_ ;
  static int out3_ ;
  static int out4_ ;
  static int out5_ ;
  static int out6_ ;


  if (serialport.available() > 0) {

    data[i_] = serialport.read();

    if (data[i_] == 't') {
      flag_2 = 1;
    }
    if ( data[i_] == '\n') {
      flag_2 = 0;
    }

    if (i_ != 0) {
      switch (data[0]) {

        /*****************************************************************************
          GOTO position and hold (with error comp)
        ******************************************************************************/
        case 't':
          data2[i2 - 1] = data[i_];

          if (data[i_]  == '\n' and comma == 6) {
            data[i_] = '\0';
            data2[i2 - 1] = data[i_];
            out6_ = atoi(data2);
            data_[5] = out6_;
            data_[4] = out5_;
            data_[3] = out4_;
            data_[2] = out3_;
            data_[1] = out2_;
            data_[0] = out1_;

            //Serial.println(Position_var);
            comma = 1 ;
            i2 = 0;
            i_ = 0;

          }

          if (data[i_]  == ',' and comma == 5) {
            data[i_] = '\0';
            data2[i2 - 1] = data[i_];
            out5_ = atoi(data2);
            comma = comma + 1 ;
            i2 = 0;
          }


          if (data[i_]  == ',' and comma == 4) {
            data[i_] = '\0';
            data2[i2 - 1] = data[i_];
            out4_ = atoi(data2);
            comma = comma + 1 ;
            i2 = 0;
          }


          if (data[i_]  == ',' and comma == 3) {
            data[i_] = '\0';
            data2[i2 - 1] = data[i_];
            out3_ = atoi(data2);
            comma = comma + 1 ;
            i2 = 0;
          }

          if (data[i_]  == ',' and comma == 2) {
            data[i_] = '\0';
            data2[i2 - 1] = data[i_];
            out2_ = atoi(data2);
            comma = comma + 1 ;
            i2 = 0;
          }


          if (data[i_]  == ',' and comma == 1) {
            data[i_] = '\0';
            data2[i2 - 1] = data[i_];
            out1_ = atoi(data2);
            comma = comma + 1 ;
            i2 = 0;
          }

          break;

      }
    }
    if (flag_2 == 1) {
      i_ = i_ + 1;
      i2 = i2 + 1;
    }
    if (flag_2 == 0) {
      i_ = 0;
      i2 = 0;
      comma = 1 ;
    }


  }
}

void Get_input6(Stream &serialport, int *data_) {

  static uint8_t i_ = 0;
  static uint8_t i2 = 0;
  static char data[30];
  static char data2[30];
  static uint8_t comma = 1;
  static bool flag_2 = 0;

  // 6 vars i svi su int
  static int out1_ ;
  static int out2_ ;
  static int out3_ ;
  static int out4_ ;
  static int out5_ ;
  static int out6_ ;


  if (serialport.available() > 0) {

    data[i_] = serialport.read();

    if (data[i_] == 't') {
      flag_2 = 1;
    }
    if ( data[i_] == '\n') {
      flag_2 = 0;
    }

    if (i_ != 0) {
      switch (data[0]) {

        /*****************************************************************************
          GOTO position and hold (with error comp)
        ******************************************************************************/
        case 't':
          data2[i2 - 1] = data[i_];

          if (data[i_]  == '\n' and comma == 6) {
            data[i_] = '\0';
            data2[i2 - 1] = data[i_];
            out6_ = atoi(data2);
            data_[5] = out6_;
            data_[4] = out5_;
            data_[3] = out4_;
            data_[2] = out3_;
            data_[1] = out2_;
            data_[0] = out1_;

            //Serial.println(Position_var);
            comma = 1 ;
            i2 = 0;
            i_ = 0;

          }

          if (data[i_]  == ',' and comma == 5) {
            data[i_] = '\0';
            data2[i2 - 1] = data[i_];
            out5_ = atoi(data2);
            comma = comma + 1 ;
            i2 = 0;
          }


          if (data[i_]  == ',' and comma == 4) {
            data[i_] = '\0';
            data2[i2 - 1] = data[i_];
            out4_ = atoi(data2);
            comma = comma + 1 ;
            i2 = 0;
          }


          if (data[i_]  == ',' and comma == 3) {
            data[i_] = '\0';
            data2[i2 - 1] = data[i_];
            out3_ = atoi(data2);
            comma = comma + 1 ;
            i2 = 0;
          }

          if (data[i_]  == ',' and comma == 2) {
            data[i_] = '\0';
            data2[i2 - 1] = data[i_];
            out2_ = atoi(data2);
            comma = comma + 1 ;
            i2 = 0;
          }


          if (data[i_]  == ',' and comma == 1) {
            data[i_] = '\0';
            data2[i2 - 1] = data[i_];
            out1_ = atoi(data2);
            comma = comma + 1 ;
            i2 = 0;
          }

          break;

      }
    }
    if (flag_2 == 1) {
      i_ = i_ + 1;
      i2 = i2 + 1;
    }
    if (flag_2 == 0) {
      i_ = 0;
      i2 = 0;
      comma = 1 ;
    }


  }
}
