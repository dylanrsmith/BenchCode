class agge_plant:
    global _agge, _io

    def __init__(self, ob1, ob2):
        self._agge = ob1
        self._io = ob2
        #print("init")

    def agge_pgn_callback(self):
        if self._agge.agge_calib_id == self._agge.WHEEL_CALIB:
            print("wheel calib")
            #todo as it is not implemented in c# code
        elif self._agge.agge_calib_id == self._agge.STEER_CALIB:
            if self._agge.agge_cid == self._agge.CALIB_NONE:
                self._agge.STEER_VALVE_STEP = self._agge.NONE

            elif self._agge.agge_cid == self._agge.CALIB_COARSE_RIGHT:
                self._agge.STEER_VALVE_STEP = self._agge.COARSE_RIGHT

            elif self._agge.agge_cid == self._agge.CALIB_COARSE_LEFT:
                self._agge.STEER_VALVE_STEP = self._agge.COARSE_LEFT

            elif self._agge.agge_cid == self._agge.CALIB_FINE_RIGHT:
                self._agge.STEER_VALVE_STEP = self._agge.FINE_RIGHT

            elif self._agge.agge_cid == self._agge.CALIB_FINE_LEFT:
                self._agge.STEER_VALVE_STEP = self._agge.FINE_LEFT

            elif self._agge.agge_cid == self._agge.CALIB_TEST_RIGHT:
                self._agge.STEER_VALVE_STEP = self._agge.TEST_RIGHT

            elif self._agge.agge_cid == self._agge.CALIB_TEST_LEFT:
                self._agge.STEER_VALVE_STEP = self._agge.TEST_LEFT

            elif self._agge.agge_cid == self._agge.CALIB_DONE:
                self._agge.STEER_VALVE_STEP = self._agge.NONE


    def agge_calculate(self):
        if self._agge.agge_enable == 1:
            if self._agge.STEER_VALVE_STEP == self._agge.COARSE_RIGHT:
                if self._agge.agge_sol_right > 1100:
                    self._agge.agge_angle += 20
            elif self._agge.STEER_VALVE_STEP == self._agge.COARSE_LEFT:
                if self._agge.agge_sol_left > 1100:
                    self._agge.agge_angle -= 20
            elif self._agge.STEER_VALVE_STEP == self._agge.FINE_RIGHT:
                if self._agge.agge_sol_right > 800:
                    self._agge.agge_angle += 5
            elif self._agge.STEER_VALVE_STEP == self._agge.FINE_LEFT:
                if self._agge.agge_sol_left > 800:
                    self._agge.agge_angle -= 5

            if self._agge.agge_steer_wheel_enable == 1:
                if self._agge.agge_pulse < 4:
                    self._agge.agge_wheel = 3500
                    self._agge.agge_pulse += 1
                elif self._agge.agge_pulse < 6:
                    self._agge.agge_wheel = 7000
                    self._agge.agge_pulse = 0
            else:
                self._agge.agge_wheel = 3500
                self._agge.agge_pulse = 0


    def agge_plant_cal(self):
        self.agge_pgn_callback()
        self.agge_calculate()