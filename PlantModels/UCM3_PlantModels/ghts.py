
class ghts_plant:
    global _gh, _io
    prev_pos = 0

    def __init__(self, ob1, ob2):
        self._gh = ob1
        self._io = ob2

    def calculate(self):
        if self._gh.ghts_enabled == 1:
            if self._gh.debug_mode == 0:
                self._gh.isswinginactive = self._io.data_read(624)
                self._gh.isswingoutactive = self._io.data_read(625)

            self._gh.swing_in_current = self._gh.isswinginactive * 1 # 1.2/2.5
            self._gh.swing_out_current = self._gh.isswingoutactive * 1.2/2.5
                        
            self._gh.ghts_pwm = self._gh.isswinginactive + self._gh.isswingoutactive
            if self._gh.ghts_pos_sensor_enabled == 1:
                if self._gh.isswinginactive != 0 and self._gh.swing_in_current > self._gh.g_curr_crack_in_ma_s32:  # IN
                    if self._gh.ghts_position_volt <= self._gh.g_min_pos_volt_mv_s32:
                        self._gh.ghts_position_volt = self._gh.g_min_pos_volt_mv_s32
                        self._gh.ghts_input_solenoid.set(0)

                    else:
                        self._gh.ghts_position_volt -= (2*(self._gh.ghts_travel_limiter / 100))
                elif self._gh.isswingoutactive != 0 and self._gh.swing_out_current > self._gh.g_curr_crack_out_ma_s32: # OUT
                    if self._gh.ghts_position_volt >= self._gh.g_max_pos_volt_mv_s32:
                        self._gh.ghts_position_volt = self._gh.g_max_pos_volt_mv_s32
                        self._gh.ghts_output_solenoid.set(0)

                    else:
                        self._gh.ghts_position_volt += (2*(self._gh.ghts_travel_limiter / 100))
                self._gh.ghts_position = (self._gh.ghts_position_volt / 28.06) - 33.25
                self._gh.ghts_current = self._gh.swing_in_current + self._gh.swing_out_current
                self.prev_pos = self._gh.ghts_position
            if self._gh.ghts_cradle_sensor_enabled == 1:
                if  self._gh.ghts_position_volt < 1000:
                    self._gh.cradle_status = 1
                else:
                    self._gh.cradle_status = 0
            if self._gh.testing_active == 0:
                #print(self._gh.isswinginactive,self._gh.swing_in_current,self._gh.isswingoutactive,self._gh.swing_out_current,(1-self._gh.cradle_status),self._gh.ghts_position_volt)
                self._io.data_to_board(513, (1-self._gh.cradle_status)) #cradle status
                self._io.data_to_board(595, self._gh.ghts_position_volt) #tube position
                #print(self._gh.isswinginactive,self._gh.swing_in_current,self._gh.isswingoutactive,self._gh.swing_out_current,self._gh.ghts_position_volt,(1-self._gh.cradle_status))



# Edge based logic act only when switch is pressed maintainn previous state or read and act contn.
# Voltage levels according to specs????
# SPN working status in phase 2
# calibration and changes in default voltage levels defined in global_defines file or from GUI

