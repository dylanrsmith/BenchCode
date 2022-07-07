import can
import os
import time
from threading import Thread
import sys
sys.path.insert(0, '/home/dev/Documents/Bench_Code_FEI_v6.01')



class CAN_FEI:
    """
    This class will contain all of the main functions for Sending and receiving CAN messages between the Pi and relay boards.
    """
    global can_bus
    global gd

    def __init__(self,ob):
        self.can_bus = can.interface.Bus(channel='can1', bustype = 'socketcan')
        self.gd=ob
        
    #def flip_one(self,board,relay,state):
    def flip_one(board,relay,state):
        """
        Sends a can message to change the state of a SINGLE relay
        """
        can_bus=can.interface.Bus(channel='can1', bustype = 'socketcan')
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

        [WIP]
        """
        #boards = [0,1,2,3,81,82]
        boards = self.gd.board_list
        ping_msg=can.Message(data=[0,0,0,1,0,0,0,0],is_extended_id=True)
        thread = can.ThreadSafeBus(channel = 'can1', bustype='socketcan')
        for i in (boards):
            ping_msg.arbitration_id=(((0x18DA << 8) | i) << 8 | 0xF9)
            thread.send(ping_msg)
            time.sleep(.05)
            print("Dictionary : "+str(self.gd.ping_dict.copy()))
    

    def flip_all_on(self, n):
        """
        Activates all relays on specified board.
        """
        can_bus=can.interface.Bus(channel='can1', bustype = 'socketcan')
        msg=can.Message(data=[0,0,0,0,0,0,4,0], is_extended_id=True)
        
        id_prefix = 0x18DA
        id_suffix = 0xF9
        board_num=int(n)

        msg.arbitration_id=((id_prefix << 8 | board_num) << 8 | id_suffix)
        can_bus.send(msg)
        #print("All relays ON")


    def flip_all_off(self, n):
        """
        Deactivates all relays on specified board.
        """
        can_bus=can.interface.Bus(channel='can1', bustype = 'socketcan')
        msg = can.Message(data=[0,0,0,0,0,0,5,0], is_extended_id=True)

        id_prefix = 0x18DA
        id_suffix = 0xF9
        board_num = int(n)
        
        msg.arbitration_id=((id_prefix << 8 | board_num) << 8 | id_suffix)
        can_bus.send(msg)
        #print("All relays OFF")


    def flip_loop(self, x):
        """
        Will toggle all relays on and then off, x amount of times.
        """
        for i in range(x):
            can_bus2=can.interface.Bus(channel='can1', bustype = 'socketcan')
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

        can_bus=can.interface.Bus(channel='can1', bustype = 'socketcan')
        can_bus.send(msg)


    def receive_CAN(self):
        '''
        Method for receiving and deciphering CAN.
        '''
        filters = [ {"can_id": 0x18DAF901, "can_mask": 0x18DAF900, "extended": True} ]
        thread_bus = can.ThreadSafeBus(channel = 'can1', bustype='socketcan', can_filters=filters)
        message=thread_bus.recv()
        time_recv = time.time()
        board = (message.arbitration_id >> 0 & 0xFF) 
        #if (board != 0xF9) and (board not in self.gd.ping_dict):
        if (board != 0xF9):
            self.gd.ping_dict.update({int(board) : 1})
            self.gd.time_dict.update({int(board) : time_recv})
        if ((time.time() - self.gd.time_dict[board]) > 20.0):
            #Update board to be offline if last response was received over 30 seconds ago:
            self.gd.ping_dict.update({int(board) : 0})
        time.sleep(0)
             

    def ez_recv(self):
        '''
        modified version of original polling plan

        here, only the esp32 is sending a broadcast message, and the pi will only be listening, instead of polling each board.
        '''
        filters = [ {"can_id": 0x18DAF901, "can_mask": 0x18DAF900, "extended": True} ]
        thread_bus = can.ThreadSafeBus(channel = 'can1', bustype='socketcan', can_filters=filters)
        message=thread_bus.recv()
        time_recv = time.time()
        address = (message.arbitration_id >> 0 & 0xFF) 
        #if (address != 0xF9) and (address not in self.gd.ping_dict):
        if (address != 0xF9):
            self.gd.ping_dict.update({int(address) : 1})
            self.gd.time_dict.update({int(address) : time_recv})
        if address in self.gd.time_dict:                                #Update board to be offline if last response was received over 30 seconds ago:
            if  ((time.time() - self.gd.time_dict[address]) > 30.0):
                self.gd.ping_dict.update({int(address) : 0})
        
        time.sleep(0)


    def initialize_can(self):
        """
        Runs command to activate Raspberry Pi CAN interface.

        Using WaveShare 2-CH CAN HAT.
        """
        os.system('sudo ifconfig can1 down')
        os.system('sudo ip link set can1 up type can bitrate 250000')


    def pingTest(self):
        import time
        for i in range(30):
            thread = can.ThreadSafeBus(channel = 'can1', bustype='socketcan')
            ping_msg1=can.Message(arbitration_id=0x18DA02F9, data=[0,0,0,1,0,0,0,0],is_extended_id=True)
            ping_msg2=can.Message(arbitration_id=0x18DA01F9, data=[0,0,0,1,0,0,0,0],is_extended_id=True)
            ping_msg3=can.Message(arbitration_id=0x18DA52F9, data=[0,0,0,1,0,0,0,0],is_extended_id=True)
            
            while True:
                thread.send(ping_msg1)
                time.sleep(.05)
                thread.send(ping_msg2)
                time.sleep(.05)
                thread.send(ping_msg3)
                time.sleep(.05)
            

#TEST ENVIRONMENT:
can0 = CAN_FEI(0)
#can0.initialize_can()
#can0.flip_all_on()
#time.sleep(5)
#can0.flip_all_off()
#can0.pingTest()
#can0.ping()
#can0.flip_loop(1)
#can0.output_test()