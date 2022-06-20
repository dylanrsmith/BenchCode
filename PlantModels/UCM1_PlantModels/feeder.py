class Feeder_hydro:
    global _Feeder, _io
    counter = 0
    prevFeederRPM = 0
    FeederRPM = 0
    TrueFeederRPM = 0
    FeederCombinedRPM = 0
    FeedRollRPM = 0

    def __init__(self, ob1, ob2):
        self._Feeder = ob1
        self._io = ob2

    def FeederPWMToFDispl(self, PWM):
        """

        :param PWM:
        :return:
        """
        flow = 0
        # print('PWM : ' , PWM)
        if (PWM > 0.93):
            if PWM < 2.76:
                flow = (90 / (2.76 - 0.93)) * (PWM - 0.93)
            else:
                flow = (90 / (2.76 - 0.93)) * (2.76 - 0.93)  # see comment on line448
        else:
            flow = 0
        return flow

    def FeederDisplToRPM(self, displ, incr, decr, ERPM):
        """

        :param displ:
        :param incr:
        :param decr:
        :param ERPM:
        :return:
        """
        RPM = 200
        flow = displ * ERPM * 1.355
        if flow != 0:
            if incr == 1:
                TrueRPM = int(flow / 63)
                #print("TrueRPM : ", TrueRPM)
                if TrueRPM <= 2380:
                    RPM = int(TrueRPM * 72 / 2060)
                if TrueRPM > 2380:
                    RPM = int(TrueRPM * 12 / 980) + 54
            elif decr == 1:
                TrueRPM = -int(flow / 63)
                #print("TrueRPM : ", TrueRPM)
                if TrueRPM <= 2380:
                    RPM = -int(TrueRPM * 72 / 2060)
                if TrueRPM > 2380:
                    RPM = -int(TrueRPM * 12 / 980) + 54
            else:
                RPM = 200
        else:
            RPM = 200
            TrueRPM = 0
        if RPM > self._Feeder.max_Feeder_spd:
            RPM = self._Feeder.max_Feeder_spd
        return RPM, TrueRPM

    def RPMAdaptation(self, Value):
        """

        :param Value:
        :return:
        """
        newRPM = Value * 300 * 94
        return newRPM

    def FeederClutchRPM(self, PWM, ERPM, clutchon):
        """

        :param PWM:
        :param ERPM:
        :param clutchon:
        :return:
        """
        if clutchon == 1:
            if PWM > 0.83:
                RPM = int(ERPM * 1.1356 * 0.833)
            else:
                RPM = 0
        else:
            RPM = 0
        return RPM

    def calculate_Feeder(self):
        FeederIncr = self._io.data_read(162)
        FeederDecr = self._io.data_read(163)
        AuxPTOValveOn = self._io.data_read(417)
        input_duty = 0
        etr_clutch = 0
        FeederClutchOn = self._io.data_read(164)
        if FeederIncr == 1:
            temp = self._io.data_read(119) * 5 / 1024
            if temp > 0.93:
                input_duty = temp
            else:
                input_duty = 0
        if FeederDecr == 1:
            temp = self._io.data_read(121) * 5 / 1024
            if temp > 0.93:
                input_duty = temp
            else:
                input_duty = 0
        if FeederClutchOn == 1:
            temp = self._io.data_read(120) * 5 / 1024
            if temp > 0.93:
                etr_clutch = temp
            else:
                etr_clutch = 0
        if self._Feeder.feederreverserEngaged == 0:
            #             print('self._Feeder.feederreverserEngaged : ' , self._Feeder.feederreverserEngaged)
            if (FeederIncr == 1 or FeederDecr == 1) and AuxPTOValveOn == 1:
                self.counter += 1
                #                 print('self.counter : ' , self.counter)
                if self.counter > 2: # Old = 12
                    FeederDispl = self.FeederPWMToFDispl(input_duty)
                    #                     print('FeederDispl : ' , FeederDispl)
                    self.FeederRPM, self.TrueFeederRPM = self.FeederDisplToRPM(FeederDispl, FeederIncr, FeederDecr,
                                                                            self._Feeder.current_spd)
                    #                     print('FeederRPM : ' , self.FeederRPM)
                    #                     print('True FeederRPM : ' , self.TrueFeederRPM)
                    if self.FeederRPM > self.prevFeederRPM:
                        self._io.data_to_board(94, abs(self.FeederRPM))
                        self.prevFeederRPM = self.FeederRPM
                    else:
                        if abs(self.FeederRPM - self.prevFeederRPM) > 4:
                            self._io.data_to_board(94, abs(self.FeederRPM))
                            self.prevFeederRPM = self.FeederRPM
                else:

                    if self.counter == 1:
                        self._io.data_to_board(92, 20)

                    if self.counter == 2:
                        self._io.data_to_board(94, 89)
                    self.TrueFeederRPM = 2960

                    if self.counter > 3:  # Old = 13
                        self.counter = 0
            else:
                self.writepotmeterRPM_fn(94, 200, self.FeederRPM)
                self.FeederRPM = 200
                self.counter = 0
        else:
            if (FeederIncr == 1 or FeederDecr == 1) and AuxPTOValveOn == 1:
                FeederDispl = self.FeederPWMToFDispl(input_duty)
                #print('FeederDispl : ' , FeederDispl)
                self.FeederRPM, self.TrueFeederRPM = self.FeederDisplToRPM(FeederDispl, FeederIncr, FeederDecr,
                                                                        self._Feeder.current_spd)
                #print('FeederRPM : ' , self.FeederRPM)
                #print('True FeederRPM : ' , self.TrueFeederRPM)
                if self.FeederRPM > self.prevFeederRPM:
                    self._io.data_to_board(94, abs(self.FeederRPM))
                    self.prevFeederRPM = self.FeederRPM
                else:
                    if abs(self.FeederRPM - self.prevFeederRPM) > 4:
                        self._io.data_to_board(94, abs(self.FeederRPM))
                        self.prevFeederRPM = self.FeederRPM
            else:
                self.writepotmeterRPM_fn(94, 200, self.FeederRPM)
                self.FeederRPM = 200
            
                
        if FeederClutchOn == 1:
            FeederETRRPM = self.FeederClutchRPM(etr_clutch, self._Feeder.current_spd, FeederClutchOn)
        else:
            FeederETRRPM = 200
        if self.FeederRPM == 200 and FeederETRRPM == 200:
            self.writepotmeterRPM_fn(92, 200, self.FeederCombinedRPM)
            self.FeederCombinedRPM = 200
        if self.FeederRPM != 200 and FeederETRRPM == 200:
            self.writepotmeterRPM_fn(92, abs(int((self.TrueFeederRPM * 20 / 300 * 0.099))),
                                     abs(self.FeederCombinedRPM))
            self.FeederCombinedRPM = int(self.TrueFeederRPM * 20 / 300 * 0.099)
#             print("self._Feeder.Feeder_gear_box : ", self._Feeder.Feeder_gear_box)
            #print('FeederCombinedRPM 1: ', self.FeederCombinedRPM)#was17
            #print('TrueFeederRPM 1: ', self.TrueFeederRPM)#was17
        if self.FeederRPM == 200 and FeederETRRPM != 200:
            if self._Feeder.ThreshingFeederStatus == 3:
                self.writepotmeterRPM_fn(92, 200, self.FeederCombinedRPM)
                self.FeederCombinedRPM = 200
            else:
                self.writepotmeterRPM_fn(92, int(FeederETRRPM / 14.3 * 0.596),
                                         self.FeederCombinedRPM)
                self.FeederCombinedRPM = int(FeederETRRPM / 14.3 * 0.596)
        if self.FeederRPM != 200 and FeederETRRPM != 200:
            #print("FeederETRRPM", FeederETRRPM)
            #print("FeederCombinedRPM", FeederCombinedRPM)
            #print("TrueFeederRPM", TrueFeederRPM)
            self.writepotmeterRPM_fn(92, int(
                ((FeederETRRPM / 14.3 * 0.596) + (self.TrueFeederRPM * 20 / 300 * 0.099))),
                                     self.FeederCombinedRPM)
            self.FeederCombinedRPM = int(((FeederETRRPM / 14.3 * 0.596) + (self.TrueFeederRPM * 20 / 300 * 0.099)))

        # if self.FeederCombinedRPM <= 75:
        #     self.writepotmeterRPM_fn(349, abs(int(
        #         ((self.FeederCombinedRPM / 1.37) * 1.045) * (self._Feeder.Feeder_gear_box) * (
        #                     1 - (self._Feeder.feed_roll / 100)))), self.FeedRollRPM)
        #     self.FeedRollRPM = int(
        #         (self.FeederCombinedRPM / 1.37) * 1.045)
        #
        # #         if self.FeederCombinedRPM == 0:
        # #             self._io.data_to_board(349, 200)
        #
        # else:
        #     if self.FeederCombinedRPM > 75:
        #         self.writepotmeterRPM_fn(349, abs(int(
        #             ((self.FeederCombinedRPM / 1.28) * 1.045) * (self._Feeder.Feeder_gear_box) * (
        #                         1 - (self._Feeder.feed_roll / 100)))), self.FeedRollRPM)
        #         self.FeedRollRPM = int(
        #             (self.FeederCombinedRPM / 1.28) * 1.045)
        #
        #     else:
        #         self._io.data_to_board(349, 200)

    def writepotmeterRPM_fn(self, td, value, prevValue):
        """

        :param td:
        :param value:
        :param prevValue:
        """
        if prevValue != value:
            self._io.data_to_board(td, value)