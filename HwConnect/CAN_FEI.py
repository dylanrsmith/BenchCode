import threading
import can
import os
import time
#from threading import Thread
import sys
sys.path.insert(0, '/home/dev/Documents/Bench_Code_FEI_v6.01')



class CAN_FEI:
    """
    This class will contain all of the main functions for Sending and receiving CAN messages between the Pi and relay boards.
    """
    global can_bus
    global gd
    global time

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
        """
        #boards = [82]
        boards = self.gd.board_list
        ping_msg=can.Message(data=[0,0,0,1,0,0,0,0],is_extended_id=True)
        thread = can.ThreadSafeBus(channel = 'can1', bustype='socketcan')
        for i in (boards):
            ping_msg.arbitration_id=(((0x18DA << 8) | i) << 8 | 0xF9)
            thread.send(ping_msg)
            time.sleep(.05)
        #print("Dictionary : "+str(self.gd.ping_dict.copy()))

        time.sleep(1)

        for board in self.gd.time_dict:
            if ((time.time() - self.gd.time_dict[board]) > 35.0 and board in self.gd.ping_dict and self.gd.ping_dict[board] != 0):
                #Update board to be offline if last response was received over 30 seconds ago:
                self.gd.ping_dict.update({int(board) : 0})
                print("Dictionary : "+str(self.gd.ping_dict.copy()))
                
    

    def flip_all_on(self,n):
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
            msg2 = can.Message(arbitration_id=0x18DA52F9, data=[0,0,0,0,0,0,4,0], is_extended_id=True)
            msg3 = can.Message(arbitration_id=0x18DA52F9, data=[0,0,0,0,0,0,5,0], is_extended_id=True)
  
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
        message=thread_bus.recv(timeout=1)
        time_recv = time.time()

        if (message != None):
            board = (message.arbitration_id >> 0 & 0xFF) 

            if (message.is_extended_id == True):
                self.gd.time_dict.update({int(board) : time_recv})

                if (board not in self.gd.ping_dict or self.gd.ping_dict[board] != 1):
                    self.gd.ping_dict.update({int(board) : 1})
                    print("Dictionary : "+str(self.gd.ping_dict.copy()))
        
        # for board in self.gd.time_dict:
        #     if ((time.time() - self.gd.time_dict[board]) > 35.0 and board in self.gd.ping_dict and self.gd.ping_dict[board] != 0):
        #         #Update board to be offline if last response was received over 30 seconds ago:
        #         self.gd.ping_dict.update({int(board) : 0})
        #         print("Dictionary : "+str(self.gd.ping_dict.copy()))
        # time.sleep(0)

    def receive_CAN_while(self):
        '''
        Method for receiving and deciphering CAN.
        '''
        filters = [ {"can_id": 0x18DAF901, "can_mask": 0x18DAF900, "extended": True} ]
        thread_bus = can.ThreadSafeBus(channel = 'can1', bustype='socketcan', can_filters=filters)

        while(True):
            message=thread_bus.recv(timeout=1)
            time_recv = time.time()

            if (message != None):
                board = (message.arbitration_id >> 0 & 0xFF) 

                if (message.is_extended_id == True):
                    self.gd.time_dict.update({int(board) : time_recv})

                    if (board not in self.gd.ping_dict or self.gd.ping_dict[board] != 1):
                        self.gd.ping_dict.update({int(board) : 1})
                        print("Dictionary : "+str(self.gd.ping_dict.copy()))
            
            time.sleep(0)
    
    #while_thread = threading.Thread(target=receive_CAN_while)

    
    def check_time(self):
        for board in self.gd.time_dict:
            if ((time.time() - self.gd.time_dict[board]) > 15.0 and board in self.gd.ping_dict and self.gd.ping_dict[board] != 0):
                #Update board to be offline if last response was received over 30 seconds ago:
                self.gd.ping_dict.update({int(board) : 0})
                print("Dictionary : "+str(self.gd.ping_dict.copy()))
                time.sleep(0)

    def initialize_can(self):
        """
        Runs command to activate Raspberry Pi CAN interface.

        Using WaveShare 2-CH CAN HAT.
        """
        os.system('sudo ifconfig can1 down')
        os.system('sudo ip link set can1 up type can bitrate 250000')

    def ping_thread(self):
        self.ping()
        #self.check_time()
        threading.Timer(30,self.ping_thread).start()

    def listen_thread(self):
        self.receive_CAN()
        threading.Timer(0.050,self.listen_thread).start()

    def start_thread(self):
        self.ping_thread()
        #self.listen_thread()
        while_thread = threading.Thread(target=self.receive_CAN_while)
        while_thread.start()


#TEST ENVIRONMENT:
#can0 = CAN_FEI(0)
#can0.initialize_can()
#can0.flip_all_on()
#time.sleep(5)
#can0.flip_all_off()
#can0.pingTest()
# can0.ping()
#can0.flip_loop(2)
#can0.output_test()