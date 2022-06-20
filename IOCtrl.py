import time
import threading
#from Configuration.hashmap import *
from HwConnect.HwConnect import *
#from JSON.Json_String import *

class IOCtrl:
    global _gd
    data_buffer = []
    IOCtrl_dict = {}
    IOCtrl_dict_prev = {}
    I2C_buffer_1 = []
    I2C_buffer_2 = []
    I2C_buffer_3 = []
    I2C_add_list_read  = [0x20, 0x21, 0x22, 0x23]
    I2C_add_list_write = [0x24, 0x25, 0x26, 0x27]
    StartTime = 0
    StopTime = 0
    HwConnect_obj = HwConnect()

    def __init__(self, ob):
        self._gd = ob
        self.init_buffer()
        self.init_I2C_buffer()

    def init_buffer(self):
        """
        Initalizes data buffer list and dictionary with values of 0.
        """
        for i in range(1000):
            self.data_buffer.append(0)                # Update all buffers to zero
            self.IOCtrl_dict.update({i + 1: 0})
            self.IOCtrl_dict_prev.update({i + 1: 0})

    def init_I2C_buffer(self):
        """
        Initialize i2c buffer lists to 0
        """
        self.I2C_buffer_1 = [0, 0, 0, 0]
        self.I2C_buffer_2 = [0, 0, 0, 0]
        self.I2C_buffer_3 = [0, 0, 0, 0]
        for i in range(0):
            for j in range(4):
                self.HwConnect_obj.writei2cbus2bytes_fn(Racknr=(i + 1),
                                                        address=self.I2C_add_list_write[j],
                                                        value1=0, value2=0)

    def data_to_board(self, SPN, val):
        """
        Writes data to I/O board, only when data is not the same as data already stored in buffer.
        """
        if self.IOCtrl_dict[SPN] != val: # only write data when data is not same as in buffer
            self.IOCtrl_dict[SPN] = val
            self.data_buffer[SPN] = val  # update the data buffer
            

            
    def data_write_board(self, key):
        """
        Uses `HWConnect` functions: `writepotmeter_fn` and `writei2cbus2bytes_fn`
        """
        SPN = int(key)
        val = self.IOCtrl_dict[SPN]
        prev_val = self.IOCtrl_dict_prev[SPN]
        if val != prev_val:
            self.IOCtrl_dict_prev[SPN] = val
            type = self.eval_cmd(SPN)
            type = type.split(',')
            if int((type[0])[1:]) == 3:
                self.HwConnect_obj.writepotmeter_fn(UCMnr=int((type[1])[1:]), busnr=int((type[2])[1:]), ic=int((type[3])[1:]), potmeter=int((type[4])[1:-1]),value=int(val))
            elif int((type[0])[1:]) == 4:
                bit_pos = int((type[3])[1:])
                for j in range(4):
                    if int((type[2])[1:]) == self.I2C_add_list_write[j]:
                        addr_pos = j
                i = int((type[1])[1:])
                if i == 0:
                    data = self.I2C_buffer_1[addr_pos]
                elif i == 1:
                    data = self.I2C_buffer_2[addr_pos]
                else:
                    data = self.I2C_buffer_3[addr_pos]
                temp = pow(2, bit_pos)
                if (data & temp) == 0:
                    if val != 0:
                        final_data = data | temp
                        self.HwConnect_obj.writei2cbus2bytes_fn(Racknr=int((type[1])[1:]),
                                                                address=int((type[2])[1:]),
                                                                value1=(final_data & 0x00FF),
                                                                value2=((final_data & 0xFF00) >> 8))
                        if i == 0:
                            self.I2C_buffer_1[addr_pos] = final_data
                        elif i == 1:
                            self.I2C_buffer_2[addr_pos] = final_data
                        else:
                            self.I2C_buffer_3[addr_pos] = final_data
                else:
                    if val == 0:
                        final_data = data - temp
                        self.HwConnect_obj.writei2cbus2bytes_fn(Racknr=int((type[1])[1:]),
                                                                address=int((type[2])[1:]),
                                                                value1=(final_data & 0x00FF),
                                                                value2=((final_data & 0xFF00) >> 8))
                        if i == 0:
                            self.I2C_buffer_1[addr_pos] = final_data
                        elif i == 1:
                            self.I2C_buffer_2[addr_pos] = final_data
                        else:
                            self.I2C_buffer_3[addr_pos] = final_data
 
    def data_from_board(self, SPN):
        """
        :param SPN:

        Calls from the read thread and stores data in buffer, which is then passed to UI.

        Uses `HwConnect.analogInput_fn` to read analog input.

        Uses `HwConnect.readi2cbus2bytes_fn` to read input from i2c.

        Once data is received, the buffer and IOctrl dictionaries are updated.
        """
        type = self.eval_cmd(SPN)
        type = type.split(',')
        
        if int((type[0])[1:]) == 2:  # analog read
            val = self.HwConnect_obj.analogInput_fn(Racknr=int((type[1])[1:]), channel=int((type[2])[1:]),
                                                    ADCnr=int((type[3])[1:]))
            if val != self.IOCtrl_dict[SPN]:
                self.data_buffer[SPN] = val  # update the data buffer
                self.IOCtrl_dict[SPN] = val  # update the IO ctrl dict
                
        elif int((type[0])[1:]) == 1:  # i2c read
            bit_pos = int((type[3])[1:])
            read_val = self.HwConnect_obj.readi2cbus2bytes_fn(Racknr=int((type[1])[1:]), address=int((type[2])[1:]))
            temp = pow(2, bit_pos)     
              
            if read_val & temp == 0:
                val = 0
            else:              
                val = 1
                
            if val != self.IOCtrl_dict[SPN]:
                self.data_buffer[SPN] = val  # update the data buffer
                self.IOCtrl_dict[SPN] = val  # update the IO ctrl dict

    def empty_string(self, id):
        """
        Error feedback: "the function is not available for the selected SPN "
        """
        print("the function is not available for SPN : ", id)

    def SPN_not_available(self, id):
        """
        Error feedback: "the selected SPN is not available"
        """
        print("the selected SPN : ", id, " is not available")

    def unknown_command(self, id):
        """
        Error feedback: the selected SPN has an unknown command."
        """
        print("the selected SPN : ", id, " has an unknown command")

    def error_occured(self, id):
        """
        Error Feedback: error occured while reading SPN
        """
        print("error occured while reading SPN : ", id)

    def eval_cmd(self, SPN):
        """
        Takes an SPN identifier, and casts it to a string.
        """
        spn_number = "SPN" + str(SPN)
        return (eval(spn_number))
#         x = eval(spn_number)
#         y = x
#         return y

    
    def data_from_pytest_to_board(self, SPN, val):
        """
        This function will be called from the socket, which will pass SPN and value received from pytest via TCP/IP over Ethernet.
        """
        self.data_to_board(SPN=SPN, val=val)

    def data_to_pytest_from_board(self, SPN):
        """
        When called, reads SPN and value from socket and writes to pytest via TCP.
        """
        cmd = 'getio'
        type = self._gd.type_dict[SPN]
        spn = SPN
        val1 = self.data_read(SPN=SPN)
        val2 = 0
        val3 = 0
        json_class = UcmJsonClass(cmd=cmd, typ=type, spn=spn, val1=val1, val2=val2, val3=val3)
        msg = str.encode(json_class.to_json())
        return msg

    def key_switch(self, state):
        """
        Calls `HwConnect.writei2cbus2bytes_fn`
        """
        self.HwConnect_obj.writei2cbus2bytes_fn(Racknr=1, address=0x27, value1=(state & 0x00FF), value2=((state & 0xFF00) >> 8))

    def data_read(self, SPN):
        """
        Returns current IOCtrl Dictionary
        """
        return self.IOCtrl_dict[SPN]
    
    def scale_voltage(self, spn, val):
        """
        Calculates a voltage value based off `volt_scale_max` and `slope` value.
        """
        max =  self._gd.volt_scale_max_dict[spn]
        slope = (255-0) / max
        new_val = slope * val
        return  new_val
io = IOCtrl()
io.data_write_board(1)