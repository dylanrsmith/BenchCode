from global_defines import *
from HwConnect.CAN_FEI import *
from PlantModels.Driveline import *
from startup_init import *
import time

key_battery_init_count = 0

class ui_callbacks:

    global _uc, _dv, io_ob, can2

    def __init__(self, ob1, ob2):
        """
        Initializes collection of UI callbacks.

        :param ob1: instance of global_defines
        :type ob1: Module
        :param ob2: Instance of IO_Ctrl
        :type ob2: Module
        """
        self._uc = ob1  # add dictionary to glcc
        self._dv = driveline(ob1, ob2)
        if self._uc.testing_active == 0:
            self.io_ob = ob2
        self.can2 = CAN_FEI

    def buttonDig(self, i):
        """
        Callback for buttons contained within Digital I/P tab

        On click, will toggle state of linked Relay.

        :param i: Index of corresponding SPN
        :type i: int
        """
        sp = self._uc.dig_ip_spn[i]
        brd_num = int(self._uc.board_dict[sp])
        rel_num = int(self._uc.channel_dict[sp])
        current_data = int(self._uc.UI_dict[sp])
        new_data = 1 - current_data
        self._uc.dig_state[sp] = 1 - self._uc.dig_state[sp]
        state = self._uc.dig_state[sp]

        self.pass_to_board(spn_number=sp, data=new_data)
        self.can2.flip_one(brd_num, rel_num, state)

    def output_send(self, spn, selected_val):
        """
        Callback for dropdown menus (Output Boards)

        Will set Relay on Output Board to selected State.

        :param spn: SPN number
        :type spn: int
        :param selected_val: State to set Relay to:['Normal', 'Open-Circuit','Battery', 'Ground']
        :type selected_val: String
        """

        if (selected_val != "Normal"):
            for selected_val in self._uc.all_widgets:
                selected_val.config(stat=tk.DISABLED)

            sp = spn
            state = selected_val
            brd_num = self._uc.board_dict[sp]
            rel_num = self._uc.channel_dict[sp]
            if state == 'Normal':
                self.can2.flip_one(brd_num, rel_num, 0)
            elif state == 'Open_Circuit':
                self.can2.flip_one(brd_num, rel_num, 1)
            elif state == 'Ground':
                self.can2.flip_one(brd_num, rel_num, 2)
            elif state == 'Battery':
                self.can2.flip_one(brd_num, rel_num, 3)

            time.sleep(5)

            for selected_val in self._uc.all_widgets:
                selected_val.config(stat=tk.NORMAL)

            indexOfSPN = self._uc.dig_ip_spn.index(spn)

            # Reset Option Menu Display Value
            if state == 'Normal' or state == 'Open_Circuit':
                self._uc.dig_ip_option_var[indexOfSPN].set("")

            if state == 'Ground' or state == 'Battery':
                self._uc.open_option_var[indexOfSPN].set("")

    def buttonVolt(self, i):
        new_data = self._uc.volt_string[i].get()
        sp = self._uc.vol_ip_spn[i]
        self.pass_to_board(spn_number=sp, data=new_data)
        self._uc.label_update = 1

    def voltToggle(self, i):
        """
        Toggles state of Relays configured as Voltage Inputs.

        :param i: index of SPN to be toggled
        :type i: int
        """

        sp = self._uc.vol_ip_spn[i]
        brd_num = int(self._uc.board_dict[sp])
        rel_num = int(self._uc.channel_dict[sp])
        current_data = int(self._uc.UI_dict[sp])
        new_data = 1 - current_data
        self._uc.volt_state[sp] = 1-self._uc.volt_state[sp]
        state = self._uc.volt_state[sp]

        self.pass_to_board(spn_number=sp, data=new_data)
        self.can2.flip_one(brd_num, rel_num, state)

    def freqToggle(self, i):
        """
        Callback for toggling SPN's configured as Frequency Input.

        :param i: index of SPN to be toggled
        :type i: int
        """
        sp = self._uc.fq_ip_spn[i]
        brd_num = int(self._uc.board_dict[sp])
        rel_num = int(self._uc.channel_dict[sp])
        current_data = int(self._uc.UI_dict[sp])
        new_data = 1 - current_data
        self._uc.freq_state[sp] = 1-self._uc.freq_state[sp]
        state = self._uc.freq_state[sp]

        self.pass_to_board(spn_number=sp, data=new_data)
        self.can2.flip_one(brd_num, rel_num, state)

    def pulseToggle(self, i):
        """
        Callback for toggling Relays configured as Pulse Input.

        :param i: index of SPN to be toggled.
        :type i: int
        """
        sp = self._uc.pulse_spn[i]
        brd_num = int(self._uc.board_dict[sp])
        rel_num = int(self._uc.channel_dict[sp])
        current_data = int(self._uc.UI_dict[sp])
        new_data = 1 - current_data
        self._uc.pulse_state[sp] = 1-self._uc.pulse_state[sp]
        state = self._uc.pulse_state[sp]

        self.pass_to_board(spn_number=sp, data=new_data)
        self.can2.flip_one(brd_num, rel_num, state)

    def pwmToggle(self, i):
        """
        Callback for toggling Relays configured as PWM input.

        :param i: SPN index
        :type i: int
        """
        sp = self._uc.pwm_ip_spn[i]
        brd_num = int(self._uc.board_dict[sp])
        rel_num = int(self._uc.channel_dict[sp])
        current_data = int(self._uc.UI_dict[sp])
        new_data = 1-current_data
        self._uc.pwm_state[sp] = 1-self._uc.pwm_state[sp]
        state = self._uc.pwm_state[sp]

        self.pass_to_board(spn_number=sp, data=new_data)
        self.can2.flip_one(brd_num, rel_num, state)

    def dig_ip_callback(i, selection):
        """
        Updates Value of Digital Inputs and saves in Dictionary.

        'dig_ip_mode' dictionary updated with SPN : State

        :param i: SPN index
        :type i: int
        :param selection: 'Normal' or 'Open-Circuit'
        :type selection: String
        """
        selection = 'self._uc.' + selection
        selInt = int(eval(selection))
        _uc.dig_ip_mode.update({i: selInt})

        _uc.dig_ip_option[i] = tk.StringVar()

    def open_option_callback(self, i, selection):
        """
        Updates values of 'Open to' SPNS.

        Dictionary `open_mode` will be updated with specified SPN id and selected value. (open to ground or open to battery)

        :param i: Index of SPN
        :type i: int
        :param selection: "Ground" or "Battery"
        :type selection: String
        """
        selection = 'self._uc' + selection
        self._uc.open_mode.update({i: selection})

    def open_button_callback(self):
        x = 1
        selection = "button"
        self._uc.open_option_callback(x, selection)

    def buttonPwmip(self, i):
        new_data = self._uc.pwm_ip_string[i].get()
        sp = self._uc.pwm_ip_spn[i]
        self.pass_to_board(spn_number=sp, data=new_data)
        self._uc.label_update = 1

    def buttonFreq(self, i):
        new_data = self._uc.freq_string[i].get()
        sp = self._uc.fq_ip_spn[i]
        self.pass_to_board(spn_number=sp, data=new_data)
        self._uc.label_update = 1

    def buttonPulse(self, i):
        new_data = self._uc.pulse_string[i].get()
        sp = self._uc.pulse_spn[i]
        self.pass_to_board(spn_number=sp, data=new_data)
        self._uc.label_update = 1

    def dv_eng_spd(self):
        spd = self._uc.eng_spd.get()
        self._uc.current_spd = float(spd)
        self._dv.calculate_speeds(self._uc.current_spd)

    def chopper_type_callback(self, selection):
        selection = 'self._uc.' + selection
        self._uc.chopper_type = int(eval(selection))
        self._dv.calculate_speeds(self._uc.current_spd)

    def HHMC_gear_callback(self, selection):
        selection = 'self._uc.' + selection
        self._uc.HHMC_gear = int(eval(selection))
        self._dv.calculate_speeds(self._uc.current_spd)

    def IC_gear_callback(self, selection):
        selection = 'self._uc.' + selection
        self._uc.IC_gear = int(eval(selection))
        self._dv.calculate_speeds(self._uc.current_spd)

    def aux_callback(self, selection):
        selection = 'self._uc.' + selection
        self._uc.Aux_PTO_enabled = int(eval(selection))
        if self._uc.Aux_PTO_enabled == 1:
            self._dv.calculate_speeds(self._uc.current_spd)
        else:
            self._dv.calculate_speeds(0)

    def feeder_callback(self, selection):
        selection = 'self._uc.' + selection
        self._uc.feeder_type = int(eval(selection))
        self._dv.calculate_speeds(self._uc.current_spd)

    def unload_type_callback(self, selection):
        selection = 'self._uc.' + selection
        self._uc.unload_rate = int(eval(selection))
        self._dv.calculate_speeds(self._uc.current_spd)

    def rotor_gear_box_callback(self, selection):
        selection = 'self._uc.' + selection
        self._uc.rotor_gear_box = float(eval(selection))

    def clrm_callback(self):
        self._uc.clrm_enabled = int(self._uc.clrm_plant_enabled.get())
        self._uc.period = int(self._uc.period_slide.get())
        self._uc.pulse = int(self._uc.pulse_slide.get())
        self._uc.degree = int(self._uc.degree_slide.get())

    def frfr_callback(self):
        self._uc.feed_roll = float(self._uc.feed_roll_var.get())

    def ghcv_callback(self):
        self._uc.ghcv_enabled = int(self._uc.ghcv_plant_enabled.get())

        self._uc.iscoveropenactive = int(self._uc.cover_open.get())
        self._uc.iscoverclosedactive = int(self._uc.cover_closed.get())

        self._uc.open_error = int(self._uc.error_open.get())
        self._uc.close_error = int(self._uc.error_close.get())

    def rsch_callback(self):
        self._uc.rsch_enabled = int(self._uc.chopper_plant_enabled.get())
        self._uc.crop_load_rsch = int(self._uc.load.get())

    def rsch_type_callback(self, selection):
        selection = 'self._uc.' + selection
        self._uc.rsch_type = int(eval(selection))

    def rsch_gear_callback(self, selection):
        selection = 'self._uc.' + selection
        self._uc.rsch_gear = int(eval(selection))

    def ghts_callback(self):
        self._uc.ghts_enabled = int(self._uc.ghts_enabled_input.get())
        self._uc.ghts_pos_sensor_enabled = int(
            self._uc.ghts_pos_sensor_enabled_input.get())
        self._uc.ghts_cradle_sensor_enabled = int(
            self._uc.ghts_cradle_sensor_enabled_input.get())
        self._uc.isswinginactive = int(self._uc.ghts_input_solenoid.get())
        self._uc.isswingoutactive = int(self._uc.ghts_output_solenoid.get())
        self._uc.ghts_travel_limiter = int(self._uc.ghts_travel_limit.get())

    def rsck_callback(self):
        self._uc.rsck_enabled = int(self._uc.rsck_enabled_var.get())
        self._uc.rsck_in_sol = int(self._uc.rsck_in_sol_var.get())
        self._uc.rsck_out_sol = int(self._uc.rsck_out_sol_var.get())
        self._uc.rsck_high_spd_sol = int(self._uc.rsck_high_spd_sol_var.get())
        self._uc.rsck_travel_limiter = int(
            self._uc.rsck_travel_limiter_var.get())

    def ghps_callback(self):
        self._uc.ghps_enable = int(self._uc.ghps_enable_var.get())
        self._uc.ghps_h_curr = int(self._uc.ghps_h_curr_var.get())
        self._uc.ghps_h_pwm = int(self._uc.ghps_h_pwm_var.get())
        self._uc.ghps_bridge_enable = int(
            self._uc.ghps_bridge_enable_var.get())

    def thcc_callback(self):
        self._uc.thcc_enable = int(self._uc.thcc_enable_var.get())
        self._uc.thcc_sensor_link = int(self._uc.thcc_sensor_link_var.get())

    def thcc_breakaway(self):
        if self._uc.thcc_breakaway_state == 0:
            self._uc.thcc_breakaway_state = 1
        else:
            self._uc.thcc_breakaway_state = 0

    def gdpb_callback(self):
        self._uc.gdpb_enabled = int(self._uc.gdpb_enable_var.get())
        self._uc.gdpb_link_to_sensor = int(self._uc.gdpb_link_to_sensor_var.get())
        if self._uc.gdpb_link_to_sensor == 0:
            self._uc.gdpb_park_brake_sensor = float(self._uc.gdpb_park_brake_sensor_var.get())
    
    def gdhd_callback(self):
        self._uc.gdhd_enabled = int(self._uc.gdhd_enable_var.get())
        self._uc.gdhd_max_pump_displacement = int(self._uc.gdhd_pump_displacement_var.get())
        self._uc.gdhd_max_motor_displacement = int(self._uc.gdhd_motor_displacement_var.get())
        
    def gdhd_gear_callback(self, selection):
        selection = 'self._uc.' + selection
        self._uc.gdhd_gear_state = int(eval(selection)) 

    def rotor_gear_callback(self, selection):
        selection = 'self._uc.' + selection
        self._uc.thcc_rotor_gear = int(eval(selection))

    def thcc_stat_callback(self, selection):
        selection = 'self._uc.' + selection
        self._uc.thcc_bridge_enable = int(eval(selection))

    def clfn_callback(self):
        self._uc.clfn_enable = int(self._uc.clfn_enable_var.get())
        self._uc.clfn_pwm = int(self._uc.clfn_pwm_var.get())

    def rssp_callback(self):
        self._uc.rssp_enable = int(self._uc.rssp_enable_var.get())
        self._uc.rssp_right_pwm = int(self._uc.rssp_right_pwm_var.get())
        self._uc.rssp_left_pwm = int(self._uc.rssp_left_pwm_var.get())
        self._uc.crop_load_right_rssp = int(
            self._uc.crop_load_right_rssp_var.get())
        self._uc.crop_load_left_rssp = int(
            self._uc.crop_load_left_rssp_var.get())

    def hdhr_type_callback(self, selection):
        selection = 'self._uc.' + selection
        self._uc.hdhr_type = int(eval(selection))

    def hdhr_callback(self):
        self._uc.hdhr_enable = int(self._uc.hdhr_enable_var.get())

    def hdhc_callback(self):
        self._uc.hdhc_lift_pressure_enabled = int(self._uc.hdhc_lift_prs_enable_var.get())
        self._uc.hdhc_frd_ang_enabled = int(self._uc.hdhc_frd_ang_enable_var.get())
        self._uc.hdhc_gnd_height_enabled = int(self._uc.hdhc_gnd_height_enable_var.get())
        self._uc.hdhc_lat_float_enabled = int(self._uc.hdhc_lat_float_enable_var.get())
        
    def fffa_callback(self):
        self._uc.fffa_enabled = int(self._uc.fffa_enable_var.get())
        self._uc.fffa_block_enabled = int(self._uc.fffa_block_enable_var.get())
        if self._uc.fffa_block_enabled == 1:
            self._uc.fffa_min_position = int(self._uc.fffa_min_position_var.get())
            self._uc.fffa_max_position = int(self._uc.fffa_max_position_var.get())
            self._uc.fffa_travel_rate = int(self._uc.fffa_travel_rate_var.get())

    def gdst_callback(self):
        self._uc.gdst_enabled = int(self._uc.gdst_enable_var.get())
        self._uc.gdst_leftTensionInput = int(self._uc.gdst_left_track_var.get())
        self._uc.gdst_rightTensionInput = int(self._uc.gdst_right_track_var.get())
        self._uc.gdst_leftFrontInput = int(self._uc.gdst_left_front_var.get())
        self._uc.gdst_leftRearInput = int(self._uc.gdst_left_rear_var.get())
        self._uc.gdst_rightFrontInput = int(self._uc.gdst_right_front_var.get())
        self._uc.gdst_rightRearInput = int(self._uc.gdst_right_rear_var.get())

    def hdfn_callback(self):
        self._uc.hdfn_hor_enable = int(self._uc.hdfn_hor_enable_var.get())
        self._uc.hdfn_ver_enable = int(self._uc.hdfn_ver_enable_var.get())
        self._uc.hdfn_vari_enable = int(self._uc.hdfn_vari_enable_var.get())
        self._uc.hdfn_hor_install = int(self._uc.hdfn_hor_install_var.get())
        self._uc.hdfn_ver_install = int(self._uc.hdfn_ver_install_var.get())
        self._uc.hdfn_vari_install = int(self._uc.hdfn_vari_install_var.get())

        self._uc.hdfn_sol_reel_up = int(self._uc.hdfn_sol_reel_up_var.get())
        self._uc.hdfn_sol_reel_down = int(
            self._uc.hdfn_sol_reel_down_var.get())
        self._uc.hdfn_sol_reel_fore = int(
            self._uc.hdfn_sol_reel_fore_var.get())
        self._uc.hdfn_sol_reel_aft = int(self._uc.hdfn_sol_reel_aft_var.get())

        self._uc.hdfn_swap_1 = int(self._uc.hdfn_swap_1_var.get())
        self._uc.hdfn_swap_2 = int(self._uc.hdfn_swap_2_var.get())
        self._uc.hdfn_swap_3 = int(self._uc.hdfn_swap_3_var.get())

        self._uc.hdfn_reel_enable = int(self._uc.hdfn_reel_enable_var.get())
        self._uc.hdfn_ffa_enable = int(self._uc.hdfn_ffa_enable_var.get())
        self._uc.hdfn_reel_sol = int(self._uc.hdfn_reel_sol_var.get())
        self._uc.hdfn_ffa_sol_fore = int(self._uc.hdfn_ffa_sol_fore_var.get())
        self._uc.hdfn_ffa_sol_aft = int(self._uc.hdfn_ffa_sol_aft_var.get())
        self._uc.hdfn_reel_pulse = int(self._uc.hdfn_reel_pulse_var.get())
        self._uc.hdfn_ffa_install = int(self._uc.hdfn_ffa_install_var.get())

    def agge_callback(self):
        self._uc.agge_enable = int(self._uc.agge_enable_var.get())
        self._uc.agge_steer_wheel_enable = int(
            self._uc.agge_steer_wheel_enable_var.get())
        self._uc.agge_sol_right = int(self._uc.agge_sol_right_var.get())
        self._uc.agge_sol_left = int(self._uc.agge_sol_left_var.get())

    def agge_steering_override(self):
        if self._uc.agge_wheel == 3500:
            self._uc.agge_wheel = 7000
        else:
            self._uc.agge_wheel = 3500

    def agge_steering_left_callback(self):
        self._uc.agge_steering_state = 1 # left
        self._uc.agge_steering_trigger = 1

    def agge_steering_center_callback(self):
        self._uc.agge_steering_state = 0 # center
        self._uc.agge_steering_trigger = 1

    def agge_steering_right_callback(self):
        self._uc.agge_steering_state = 2 # right
        self._uc.agge_steering_trigger = 1

    def agge_token_callback(self, selection):
        selection = 'self._uc.' + selection
        self._uc.agge_calib_token = int(eval(selection))

    def agge_calib_callback(self, selection):
        selection = 'self._uc.' + selection
        self._uc.agge_calib_id = int(eval(selection))

    def agge_cid_callback(self, selection):
        selection = 'self._uc.' + selection
        self._uc.agge_cid = int(eval(selection))

    def rrts_callback(self):
        self._uc.rrts_enable = int(self._uc.rrts_enable_var.get())

    def rrts_rocktrap_open_sw_callback(self):
        if self._uc.rrts_rocktrap_open_sw == 0:
            self._uc.rrts_rocktrap_open_sw = 1
        else:
            self._uc.rrts_rocktrap_open_sw = 0

    def rrts_rocktrap_close_sw_callback(self):
        if self._uc.rrts_rocktrap_close_sw == 0:
            self._uc.rrts_rocktrap_close_sw = 1
        else:
            self._uc.rrts_rocktrap_close_sw = 0
        
    def thresher_engage_callback(self):
        if self._uc.thresher_engage_state == 0:
            self._uc.thresher_engage_state = 1
            if self._uc.testing_active == 0:
                self.io_ob.data_to_board(322,int(0))
        else:
            self._uc.thresher_engage_state = 0
            if self._uc.testing_active == 0:
                self.io_ob.data_to_board(322,int(1))
            
    def feeder_engage_callback(self):
        if self._uc.feeder_engage_state == 0:
            self._uc.feeder_engage_state = 1
            if self._uc.testing_active == 0:
                self.io_ob.data_to_board(66,int(0))
        else:
            self._uc.feeder_engage_state = 0
            if self._uc.testing_active == 0:
                self.io_ob.data_to_board(66,int(1))

    def key_callback(self):
        current = self._uc.KeyIsON
        new = 1 - current
        self._uc.KeyIsON = new
        if self._uc.testing_active == 0:
            self.io_ob.key_switch(state=new)
        else:
            print(self._uc.KeyIsON)

    def battery_key_callback(self):
        #print("Battery Call Back")
        self.Key_and_Battery_Button(switch='Battery')

    def Key_and_Battery_Button(self,switch):

        if self._uc.Key_and_Battery_State == 3 and switch == 'Key':
            self._uc.Key_and_Battery_State = 1
            
        if self._uc.Key_and_Battery_State == 1 and switch == 'Battery':
            self._uc.Key_and_Battery_State = 2
            
        if self._uc.Key_and_Battery_State == 2 and switch == 'Key':
            self._uc.Key_and_Battery_State = 3


        #print("Name of Button Pressed : \t",switch)
        #print("Key_and_Battery_State : \t", self._uc.Key_and_Battery_State)
        
        if self._uc.Key_and_Battery_State == 1:
            self.io_ob.Key_and_Battery_Write(Byte_1=5)
        if self._uc.Key_and_Battery_State == 2:
            self.io_ob.Key_and_Battery_Write(Byte_1=1)
        if self._uc.Key_and_Battery_State == 3:
            self.io_ob.Key_and_Battery_Write(Byte_1=4)
            if self._uc.testing_active == 0:
                st = start_init(self._uc, self.io_ob)
                st.init_spn()
                self.io_ob.data_to_board(322, int(0))
                time.sleep(0.5)
                self.io_ob.data_to_board(322, int(1))
                time.sleep(0.5)
                self.io_ob.data_to_board(66, int(0))
                time.sleep(0.5)
                self.io_ob.data_to_board(66, int(1))

    def debug_callback(self):
        current = self._uc.debug_mode
        new = 1 - current
        self._uc.debug_mode = new
        if self._uc.debug_mode == 0:
            self._uc.agge_enable = 0
            self._uc.hdfn_ffa_enable = 0
            self._uc.hdfn_hor_enable = 0
            self._uc.hdfn_ver_enable = 0
            self._uc.hdfn_vari_enable = 0
            self._uc.hdfn_reel_enable = 0
            self._uc.clrm_enabled = 0
            self._uc.hdhr_enable = 0
            self._uc.ghcv_enabled = 0
            self._uc.rsch_enabled = 0
            self._uc.clfn_enable = 0
            self._uc.ghts_enabled = 0
            self._uc.ghps_enable = 0
            self._uc.rsck_enabled = 0
            self._uc.thcc_enable = 0
            self._uc.rssp_enable = 0
        else:
            self._uc.agge_enable = 1
            self._uc.hdfn_ffa_enable = 1
            self._uc.hdfn_hor_enable = 1
            self._uc.hdfn_ver_enable = 1
            self._uc.hdfn_vari_enable = 1
            self._uc.hdfn_reel_enable = 1
            self._uc.clrm_enabled = 1
            self._uc.hdhr_enable = 1
            self._uc.ghcv_enabled = 1
            self._uc.rsch_enabled = 1
            self._uc.clfn_enable = 1
            self._uc.ghts_enabled = 1
            self._uc.ghps_enable = 1
            self._uc.rsck_enabled = 1
            self._uc.thcc_enable = 1
            self._uc.rssp_enable = 1

    def sim_callback(self):
        """
        Function to toggle the UI between simulator mode and normal mode.

        Greys out widgets when simulator mode is not active.

        Writes state of simMode to text file.
        """
        all_widgets = list(itertools.chain(self._uc.dig_ip_option, self._uc.open_option, self._uc.volt_toggle,
                           self._uc.pwm_ip_toggle, self._uc.freq_toggle, self._uc.pulse_toggle, self._uc.actuator_load, self._uc.actuator_set, self._uc.actuator_pos, self._uc.actuator_btn))
        new = 1-self._uc.SimMode
        self._uc.SimMode = new
        file = open("SimMode.txt", "w")
        a = str(self._uc.SimMode)
        file.write(a)
        file.close()

        if self._uc.SimMode == 1:
            self._uc.sim_button.config(bg="Green")
            for i in range(len(all_widgets)):
                try:
                    all_widgets[i].config(state=tk.NORMAL)
                except AttributeError:
                    pass
            for i in range(80):
                self.can2.flip_all_off(i, i)

        elif self._uc.SimMode == 0:
            self._uc.sim_button.config(bg="Red")
            for i in range(len(all_widgets)):
                try:
                    all_widgets[i].config(state=tk.DISABLED)
                    if(all_widgets[i].__class__.__name__ != "OptionMenu"):
                        all_widgets[i].config(bg="azure3")
                except AttributeError:
                    pass
            for i in range(80):
                self.can2.flip_all_on(i, i)

    def reset_CAN(self):
        """
        When Button is clicked, this function will run a bash script to reset the CAN network.

        The script 'resetCAN.sh' sets the CAN bus down and back up.

        Baud Rate: 250,000
        """
        os.system("bash ./HwConnect/resetCAN.sh")

    def pass_to_board(self, spn_number, data):
        """
        Passes SPN number and index to terminal to be printed.

        {deprecated}
        """
        if self._uc.testing_active == 0:
            self.io_ob.data_to_board(SPN=spn_number, val=int(data))
        else:
            print("spn : ", spn_number)
            print("val : ", data)
