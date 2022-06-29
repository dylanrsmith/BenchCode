import can
import os
import time
from threading import Thread
import sys
from global_defines import global_defines
sys.path.insert(0, '/home/dev/Documents/Bench_Code_FEI_v6.01')



class CAN_FEI:
    """
    This class will contain all of the main functions for Sending and receiving CAN messages between the Pi and relay boards.
    """
    global can_bus
    global gd
    global msg
    global can1 

    def __init__(self):
        self.can_bus = can.interface.Bus(channel='can0', bustype = 'socketcan')
        self.msg = can.Message(data=[0,0,0,0,0,0,0,0], is_extended_id=True)
        self.id_prefix = 0x18DA
        self.id_suffix = 0xF9
        
        
    #def flip_one(self,board,relay,state):
    def flip_one(board,relay,state):
        """
        Sends a can message to change the state of a SINGLE relay
        """
        can_bus=can.interface.Bus(channel='can0', bustype = 'socketcan')
        msg=can.Message(data=[0,0,0,0,0,0,0,0],is_extended_id=True)
        
        board = int(board)
        relay = int(relay)
        state = int(state)
        msg.arbitration_id = ((0x18DA << 8 | board) << 8 | 0xF9)
        msg.data[7]=relay
        msg.data[6]=state

        can_bus.send(msg)
        
        

    def ping(self):
        """
        Sends a CAN message where 5th byte is 1, asking for a request from any online relay boards.

        Relay board should return same message, when response is received, that board will be updated as ready.

        Handled by a thread.
        """
        boards = [0,1,2,3,81,82]
        ping_msg=can.Message(data=[0,0,0,1,0,0,0,0],is_extended_id=True)
        thread = can.ThreadSafeBus(channel = 'can0', bustype='socketcan')
        for i in (boards):
            ping_msg.arbitration_id=((0x18DA << 8 | i) << 8 | 0xF9)
            thread.send(ping_msg)
    
    #Add parameter to 
    def flip_all_on(self):
        """
        Activates all relays on specified board.
        """
        can_bus=can.interface.Bus(channel='can0', bustype = 'socketcan')
        msg=can.Message(data=[0,0,0,0,0,0,4,0], is_extended_id=True)
        
        id_prefix = 0x18DA
        id_suffix = 0xF9
        board_num=int(input("Enter Board Number: "))

        msg.arbitration_id=((id_prefix << 8 | board_num) << 8 | id_suffix)
        can_bus.send(msg)
        print("All relays ON")

    def flip_all_off(self):
        """
        Deactivates all relays on specified board.
        """
        can_bus=can.interface.Bus(channel='can0', bustype = 'socketcan')
        msg = can.Message(data=[0,0,0,0,0,0,5,0], is_extended_id=True)

        id_prefix = 0x18DA
        id_suffix = 0xF9

        board_num = int(input("Enter Board Number: "))
        
        msg.arbitration_id=((id_prefix << 8 | board_num) << 8 | id_suffix)
        can_bus.send(msg)
        print("All relays OFF")

    def flip_loop(self, x):
        """
        Will toggle all relays on and then off, x amount of times.
        """
        for i in range(x):
            can_bus2=can.interface.Bus(channel='can0', bustype = 'socketcan')
            msg2 = can.Message(arbitration_id=0x18DA51F9, data=[0,0,0,0,0,0,4,0], is_extended_id=True)
            msg3 = can.Message(arbitration_id=0x18DA51F9, data=[0,0,0,0,0,0,5,0], is_extended_id=True)

            can_bus2.send(msg2)
            time.sleep(4)
            can_bus2.send(msg3)
            time.sleep(4)

    def output_test(self):
        inp = int(input("Enter 0-Normal 1-Open 2-Ground 3-Battery : "))
        num = int(input("Relay Number : "))
        msg = can.Message(arbitration_id=0x18DA51F9, data=[0,0,0,0,0,0,inp,num])

        can_bus=can.interface.Bus(channel='can0', bustype = 'socketcan')
        can_bus.send(msg)

    def receive_CAN(self):
        '''
        Method for receiving and deciphering CAN.
        '''
        thread_bus = can.ThreadSafeBus(channel = 'can0', bustype='socketcan')
        try:
            message=thread_bus.recv()
            address = (message.arbitration_id >> 0 & 0xFF) 
            if (address != 0xF9):
                global_defines.ping_dict.update({int(address) : 1})
                print(len(global_defines.ping_dict))
        except TimeoutError:
            print('got nothing')
             

    def initialize_can(self):
        """
        Runs command to activate Raspberry Pi CAN interface.

        Using WaveShare 2-CH CAN HAT.
        """
        os.system('sudo ifconfig can0 down')
        os.system('sudo ip link set can0 up type can bitrate 250000')


    def pingTest(self):
        import time
        for i in range(30):
            thread = can.ThreadSafeBus(channel = 'can0', bustype='socketcan')
            ping_msg1=can.Message(arbitration_id=0x18DA03F9, data=[0,0,0,1,0,0,0,0],is_extended_id=True)
            ping_msg2=can.Message(arbitration_id=0x18DA01F9, data=[0,0,0,1,0,0,0,0],is_extended_id=True)
            ping_msg3=can.Message(arbitration_id=0x18DA52F9, data=[0,0,0,1,0,0,0,0],is_extended_id=True)
            
            thread.send(ping_msg1)
            thread.send(ping_msg2)
            thread.send(ping_msg3)
            time.sleep(.5)

#TEST ENVIRONMENT:
can0 = CAN_FEI()
#can0.initialize_can()
#can0.flip_loop(1)
#can0.flip_all_on()
#time.sleep(5)
#can0.flip_all_off()
#can0.pingTest()
#can0.ping()
#can0.flip_one()
#can0.output_test()