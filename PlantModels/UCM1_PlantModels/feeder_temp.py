class Feeder_hydro:
    global _Feeder, _io
    counter = 0
    prevFeederRPM = 0
    FeederRPM = 0

    def __init__(self, ob1, ob2):
        self._Feeder = ob1
        self._io = ob2

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