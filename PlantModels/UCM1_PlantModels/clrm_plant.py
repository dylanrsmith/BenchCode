#from IOCtrl import *
class clrm_plant:
    global _cl, _io

    def __init__(self, ob1, ob2):
        self._cl = ob1
        self._io = ob2
        #print("init")

    def calculate_speed(self):
        spd_temp = self._cl.sp_val[19]

        prev_output_spd = self._cl.tail_sensor_spd

        if self._cl.clrm_enabled == 1:

            if spd_temp > 0:
                spd = (60*1000)/spd_temp
            else:
                spd = 2000

            if self._cl.periodstate == 1:
                new_spd = spd - ((self._cl.period*self._cl.degree)/360)
            else:
                new_spd = (spd*self._cl.degree)/360
            self._cl.periodstate = 1 - self._cl.periodstate #toggle the periods for tb and ts
            self._cl.tail_sensor_spd = new_spd

        else:
            self._cl.tail_sensor_spd = prev_output_spd
        if self._cl.testing_active == 0:
            self._io.data_to_board(91, self._cl.tail_sensor_spd)

