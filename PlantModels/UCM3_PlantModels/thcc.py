
class thcc_plant:
    global _thcc
    prev_pos = 0

    def __init__(self, ob):
        self._thcc = ob

    def pos_to_voltage(self, pos):
        volt = ((pos + 750)*(2/3))
        return volt

    def voltage_to_pos(self, vol):
        if self._thcc.thcc_rotor_gear == self._thcc.single_rotor:
            pos = ((1.82*vol)-1203.64)
        else:
            pos = ((3.67*vol)-5596.33)
        return pos

    def rotor_type(self):
        if self._thcc.thcc_rotor_gear == self._thcc.single_rotor:
            self._thcc.thcc_min_volt = 660
            self._thcc.thcc_max_volt = 3950
        else:
            self._thcc.thcc_min_volt = 1525
            self._thcc.thcc_max_volt = 3160

    def calculate(self):
        self.rotor_type()
        if self._thcc.thcc_enable == 1:
            if self._thcc.thcc_bridge_enable == 2:
                self._thcc.thcc_curr = self._thcc.thcc_h_curr
                self._thcc.thcc_pwm = self._thcc.thcc_h_pwm
                if self._thcc.thcc_curr > 0:
                    if self._thcc.thcc_pos_volt >= self._thcc.thcc_max_volt:
                        self._thcc.thcc_pos_volt = self._thcc.thcc_max_volt
                    else:
                        self._thcc.thcc_pos_volt += self._thcc.thcc_tick_rate_pos
                elif self._thcc.thcc_curr < 0:
                    if self._thcc.thcc_pos_volt <= self._thcc.thcc_min_volt:
                        self._thcc.thcc_pos_volt = self._thcc.thcc_min_volt
                    else:
                        self._thcc.thcc_pos_volt -= self._thcc.thcc_tick_rate_pos
                temp = self.voltage_to_pos(self._thcc.thcc_pos_volt)
                if temp >= 0:
                    self._thcc.thcc_pos = temp
                else:
                    self._thcc.thcc_pos = 0