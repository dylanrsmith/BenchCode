class rsck_plant:
    global _rsck, _io
    prev_pos = 0

    def __init__(self, ob1, ob2):
        self._rsck = ob1
        self._io = ob2

    def calculate(self):
        if self._rsck.rsck_enabled == 1:
            if self._rsck.testing_active == 0:
                self._rsck.rsck_in_sol = self._io.data_read(640)
                self._rsck.rsck_out_sol = self._io.data_read(645)
                self._rsck.rsck_high_spd_sol = self._io.data_read(652)

            self._rsck.in_curr = self._rsck.rsck_in_sol * 1.2/3.65
            self._rsck.out_curr = self._rsck.rsck_out_sol * 1.2/3.65

            self._rsck.high_speed_current = self._rsck.rsck_high_spd_sol * 1.2/3.65
            self._rsck.in_out_curr = self._rsck.in_curr + self._rsck.out_curr
            self._rsck.in_out_pwm = self._rsck.rsck_in_sol + self._rsck.rsck_out_sol
            self._rsck.high_speed_pwm = self._rsck.rsck_high_spd_sol

            if self._rsck.rsck_high_spd_sol > 700:
                self._rsck.rsck_tick_rate = (10*(self._rsck.rsck_travel_limiter / 100))
            else:
                self._rsck.rsck_tick_rate = (5*(self._rsck.rsck_travel_limiter / 100))

            if self._rsck.in_curr != 0 and self._rsck.out_curr == 0:
                if self._rsck.rsck_volt <= 1000:
                    self._rsck.rsck_volt = 1000
                    self._rsck.rsck_in_sol_var.set(0)
                    self._rsck.in_curr = 0
                else:
                    self._rsck.rsck_volt -= self._rsck.rsck_tick_rate
            elif self._rsck.in_curr == 0 and self._rsck.out_curr != 0:
                if self._rsck.rsck_volt >= 4300:
                    self._rsck.rsck_volt = 4300
                    self._rsck.rsck_out_sol_var.set(0)
                    self._rsck.out_curr = 0
                else:
                    self._rsck.rsck_volt += self._rsck.rsck_tick_rate
            self._rsck.rsck_pos = ((2.25 * self._rsck.rsck_volt) - 1125)/100
            if self._rsck.testing_active == 0:
                self._io.data_to_board(598, self._rsck.rsck_volt)  # chopper counter knife pos
