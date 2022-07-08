import itertools
import tkinter as tk
from tkinter import ttk
from functools import partial
import threading
import psutil
from HwConnect.CAN_FEI import *
#from IOCtrl import *

class update_ui:

    global _ui, io_ob

    def __init__(self, ob1, ob2):
        self._ui = ob1
        self.can2 = CAN_FEI(0)

        if self._ui.testing_active == 0:
            self.io_ob = ob2

    def update_ui_dict(self):
        for key in self._ui.UI_dict:
            if self._ui.testing_active == 0:
                val = self.io_ob.data_read(key)
            else:
                if self._ui.toggle == 0:
                    val = 1
                else:
                    val = 0

            self._ui.UI_dict.update({key: val})
        if self._ui.testing_active == 1:
            if self._ui.toggle == 0:
                self._ui.toggle = 1
            else:
                self._ui.toggle = 0

        self.update_ui_spn()


    def update_ui_spn(self):
        '''
        Function to update UI based on dictionary data
        
        This is what causes the buttons to flash red and green in testing mode.
        '''
        for key in self._ui.UI_dict:
            data = self._ui.UI_dict[key]

            #DIG I/P
            if key in self._ui.dig_ip_spn:
                ind = self._ui.dig_ip_spn.index(key)  
                if self._ui.dig_state[key] == 1:      
                    self._ui.dig_ip_button[ind].config( bg="Green")
                else:
                    self._ui.dig_ip_button[ind].config( bg="Red")
                i = ind
                if i < 19:
                    self._ui.dig_ip_button[i].grid(row=i, column=1)
                else:
                    self._ui.dig_ip_button[i].grid(row=i - 19, column=4)

            #DIG O/P
            elif key in self._ui.dig_op_spn:
                ind = self._ui.dig_op_spn.index(key)  # find position of that spn
                if data == 1:
                    self._ui.dig_op_button[ind].config(bg="Green")
                else:
                    self._ui.dig_op_button[ind].config( bg="Red")
                i = ind
                if 0 <= i < 31:
                    row = i
                    column = 1
                elif 31 <= i < 62:
                    row = i - 31
                    column = 3
                elif 62 <= i < 94:
                    row = i - 62
                    column = 5
                self._ui.dig_op_button[i].grid(row=row, column=column + 2)

            #Update Voltage Tab
            elif key in self._ui.vol_ip_spn:
                ind = self._ui.vol_ip_spn.index(key)

                i = ind
                if i < 29:
                    self._ui.volt_label[i].grid(row=i, column=1)
                else:
                    self._ui.volt_label[i].grid(row=i - 29, column=5)

                if self._ui.SimMode == 1:
                    if self._ui.volt_state[key] == 1:
                        self._ui.volt_toggle[ind].config(bg="Green")
                    else:
                        self._ui.volt_toggle[ind].config(bg="Red")
    
                self._ui.volt_label[ind].delete(0, 100)
                self._ui.volt_label[ind].insert(0, data)

            #Update PWM I/P tab
            elif key in self._ui.pwm_ip_spn:
                ind = self._ui.pwm_ip_spn.index(key)
                self._ui.pwm_ip_label[ind].delete(0, 100)
                self._ui.pwm_ip_label[ind].insert(0, data)

                if self._ui.SimMode==1:
                    if self._ui.pwm_state[key] == 1:
                        self._ui.pwm_ip_toggle[ind].config(bg="Green")
                    else:
                        self._ui.pwm_ip_toggle[ind].config(bg="Red")

            
            #Update PWM O/P tab
            elif key in self._ui.pwm_op_spn:
                ind = self._ui.pwm_op_spn.index(key)
                self._ui.pwm_op_label[ind].delete(0, 100)
                self._ui.pwm_op_label[ind].insert(0, data)

            #Update Freq Tab
            elif key in self._ui.fq_ip_spn:
                ind = self._ui.fq_ip_spn.index(key)
                self._ui.freq_label[ind].delete(0, 100)
                self._ui.freq_label[ind].insert(0, data)

                if self._ui.SimMode==1:
                    if self._ui.freq_state[key]==1:
                        self._ui.freq_toggle[ind].config(bg="Green")
                    else:
                        self._ui.freq_toggle[ind].config(bg="Red")

            #Update Pulse tab
            elif key in self._ui.pulse_spn:
                ind = self._ui.pulse_spn.index(key)
                self._ui.pulse_label[ind].delete(0, 100)
                self._ui.pulse_label[ind].insert(0, data)

                if self._ui.SimMode==1:
                    if self._ui.pulse_state[key]==1:
                        self._ui.pulse_toggle[ind].config(bg="Green")
                    else:
                        self._ui.pulse_toggle[ind].config(bg="Red")


    def update_ui_driveline(self):
        for i in range(len(self._ui.sp_val)):
            self._ui.drive_label[i].delete(0, 100)
            self._ui.drive_label[i].insert(0, "{:.2f}".format(float(self._ui.sp_val[i])))
        self._ui.current_spd_label.delete(0, 100)
        self._ui.current_spd_label.insert(0, "{:.2f}".format(float(self._ui.current_spd)))

    def update_ui_clrm(self):
        if self._ui.clrm_enabled == 1:
            self._ui.clrm_label.delete(0, 100)
            self._ui.clrm_label.insert(0, "{:.2f}".format(float(self._ui.tail_sensor_spd)))

    def update_ui_ghcv(self):
        self._ui.open_label.delete(0, 100)
        self._ui.open_label.insert(0, "{:.2f}".format(float(self._ui.cover_open_sensor)))
        self._ui.close_label.delete(0, 100)
        self._ui.close_label.insert(0, "{:.2f}".format(float(self._ui.cover_close_sensor)))

        self._ui.ghcv_label_open.delete(0, 100)
        self._ui.ghcv_label_open.insert(0, "{:.2f}".format(float(self._ui.g_opened_tmr_ms_u16)))
        self._ui.ghcv_label_close.delete(0, 100)
        self._ui.ghcv_label_close.insert(0, "{:.2f}".format(float(self._ui.g_closed_tmr_ms_u16)))

    def update_ui_rsch(self):
        self._ui.rsch_label.delete(0, 100)
        self._ui.rsch_label.insert(0, "{:.2f}".format(float(self._ui.rsch_spd)))

    def update_ui_ghts(self):
        self._ui.ghts_label_pwm.delete(0, 100)
        self._ui.ghts_label_pwm.insert(0, "{:.2f}".format(float(self._ui.ghts_pwm)))

        self._ui.ghts_label_pos.delete(0, 100)
        self._ui.ghts_label_pos.insert(0, "{:.2f}".format(float(self._ui.ghts_position)))

        self._ui.ghts_label_current.delete(0, 100)
        self._ui.ghts_label_current.insert(0, "{:.2f}".format(float(self._ui.ghts_current)))

        self._ui.ghts_label_pos_volt.delete(0, 100)
        self._ui.ghts_label_pos_volt.insert(0, "{:.2f}".format(float(self._ui.ghts_position_volt)))

        if self._ui.cradle_status == 0:
            self._ui.cradle_button.config(bg="Red")
        else:
            self._ui.cradle_button.config(bg="Green")

    def update_ui_rsck(self):
        self._ui.rsck_label_in_out_current.delete(0, 100)
        self._ui.rsck_label_in_out_current.insert(0, "{:.2f}".format(float(self._ui.in_out_curr)))

        self._ui.rsck_label_in_out_pwm.delete(0, 100)
        self._ui.rsck_label_in_out_pwm.insert(0, "{:.2f}".format(float(self._ui.in_out_pwm)))

        self._ui.rsck_label_high_speed_current.delete(0, 100)
        self._ui.rsck_label_high_speed_current.insert(0, "{:.2f}".format(float(self._ui.high_speed_current)))

        self._ui.rsck_label_high_speed_pwm.delete(0, 100)
        self._ui.rsck_label_high_speed_pwm.insert(0, "{:.2f}".format(float(self._ui.high_speed_pwm)))

        self._ui.rsck_label_pos.delete(0, 100)
        self._ui.rsck_label_pos.insert(0, "{:.2f}".format(float(self._ui.rsck_pos)))

        self._ui.rsck_label_volt.delete(0, 100)
        self._ui.rsck_label_volt.insert(0, "{:.2f}".format(float(self._ui.rsck_volt)))

    def update_ui_ghps(self):
        self._ui.ghps_curr_label.delete(0, 100)
        self._ui.ghps_curr_label.insert(0, "{:.2f}".format(float(self._ui.ghps_curr)))

        self._ui.ghps_pwm_label.delete(0, 100)
        self._ui.ghps_pwm_label.insert(0, "{:.2f}".format(float(self._ui.ghps_pwm)))

        self._ui.ghps_pos_label.delete(0, 100)
        self._ui.ghps_pos_label.insert(0, "{:.2f}".format(float(self._ui.ghps_pos)))

        self._ui.ghps_pos_volt_label.delete(0, 100)
        self._ui.ghps_pos_volt_label.insert(0, "{:.2f}".format(float(self._ui.ghps_pos_volt)))

        if self._ui.ghps_bridge_enable == 0:
            self._ui.ghps_bridge_button.config(bg="Red")
        else:
            self._ui.ghps_bridge_button.config(bg="Green")

    def update_ui_thcc(self):
        self._ui.thcc_curr_label.delete(0, 100)
        self._ui.thcc_curr_label.insert(0, "{:.2f}".format(float(self._ui.thcc_curr)))

        self._ui.thcc_pwm_label.delete(0, 100)
        self._ui.thcc_pwm_label.insert(0, "{:.2f}".format(float(self._ui.thcc_pwm)))

        self._ui.thcc_pos_label.delete(0, 100)
        self._ui.thcc_pos_label.insert(0, "{:.2f}".format(float(self._ui.thcc_pos)))

        self._ui.thcc_pos_volt_label.delete(0, 100)
        self._ui.thcc_pos_volt_label.insert(0, "{:.2f}".format(float(self._ui.thcc_pos_volt)))

        if self._ui.thcc_bridge_enable == 0:
            self._ui.thcc_bridge_button.config(bg="Red")
        else:
            self._ui.thcc_bridge_button.config(bg="Green")

    def update_ui_clfn(self):
        self._ui.clfn_RPM_label.delete(0, 100)
        self._ui.clfn_RPM_label.insert(0, "{:.2f}".format(float(self._ui.clfn_rpm)))

    def update_ui_rssp(self):
        self._ui.rssp_right_spd_label.delete(0, 100)
        self._ui.rssp_right_spd_label.insert(0, "{:.2f}".format(float(self._ui.rssp_right_spd)))

        self._ui.rssp_right_curr_label.delete(0, 100)
        self._ui.rssp_right_curr_label.insert(0, "{:.2f}".format(float(self._ui.rssp_right_curr)))

        self._ui.rssp_left_spd_label.delete(0, 100)
        self._ui.rssp_left_spd_label.insert(0, "{:.2f}".format(float(self._ui.rssp_left_spd)))

        self._ui.rssp_left_curr_label.delete(0, 100)
        self._ui.rssp_left_curr_label.insert(0, "{:.2f}".format(float(self._ui.rssp_left_curr)))

    def update_ui_hdhr(self):
        self._ui.hdhr_type_volt_label.delete(0, 100)
        self._ui.hdhr_type_volt_label.insert(0, "{:.2f}".format(float(self._ui.hdhr_type_volt)))

        self._ui.hdhr_ext1_volt_label.delete(0, 100)
        self._ui.hdhr_ext1_volt_label.insert(0, "{:.2f}".format(float(self._ui.hdhr_ext1_volt)))

        self._ui.hdhr_ext2_volt_label.delete(0, 100)
        self._ui.hdhr_ext2_volt_label.insert(0, "{:.2f}".format(float(self._ui.hdhr_ext2_volt)))

    def update_ui_hdfn(self):
        self._ui.hdfn_hor_pos_label.delete(0, 100)
        self._ui.hdfn_hor_pos_label.insert(0, "{:.2f}".format(float(self._ui.hdfn_hor_pos)))

        self._ui.hdfn_ver_pos_label.delete(0, 100)
        self._ui.hdfn_ver_pos_label.insert(0, "{:.2f}".format(float(self._ui.hdfn_ver_pos)))

        self._ui.hdfn_vari_pos_label.delete(0, 100)
        self._ui.hdfn_vari_pos_label.insert(0, "{:.2f}".format(float(self._ui.hdfn_vari_pos)))

        self._ui.hdfn_reel_spd_label.delete(0, 100)
        self._ui.hdfn_reel_spd_label.insert(0, "{:.2f}".format(float(self._ui.hdfn_reel_spd)))

        self._ui.hdfn_ffa_spd_label.delete(0, 100)
        self._ui.hdfn_ffa_spd_label.insert(0, "{:.2f}".format(float(self._ui.hdfn_ffa_spd)))

    def update_ui_agge(self):
        self._ui.agge_angle_label.delete(0, 100)
        self._ui.agge_angle_label.insert(0, "{:.2f}".format(float(self._ui.agge_angle)))

        if self._ui.agge_wheel == 3500:
            self._ui.agge_wheel_button.config(bg="Red")
        elif self._ui.agge_wheel == 7000:
            self._ui.agge_wheel_button.config(bg="Green")

    def update_settings(self):
        """
        Updates Color Of Settings Buttons depending on their linked value.
        
        [ButtonName] -> [ValueName]:

        Key_Button -> KeyIsON

        debug_mode_button -> debug_mode

        sim_button -> SimMode

        """
        #all_widgets=list(itertools.chain(self._ui.dig_ip_button,self._ui.dig_op_button,self._ui.open_option,self._ui.open_button,self._ui.volt_button,self._ui.volt_toggle,self._ui.pwm_ip_button,self._ui.pwm_ip_toggle,self._ui.freq_button,self._ui.freq_toggle,self._ui.button_pulse,self._ui.pulse_toggle))
        all_widgets=list(itertools.chain(self._ui.dig_ip_option,self._ui.open_option,self._ui.volt_toggle,self._ui.pwm_ip_toggle,self._ui.freq_toggle,self._ui.pulse_toggle,self._ui.actuator_load,self._ui.actuator_set))
        if self._ui.KeyIsON == 1:
            self._ui.Key_Button.config(bg="Red")
        elif self._ui.KeyIsON == 0:
            self._ui.Key_Button.config(bg="Green")
        
        if self._ui.debug_mode == 0:
            self._ui.debug_mode_button.config(bg="Red")
        elif self._ui.debug_mode == 1:
            self._ui.debug_mode_button.config(bg="Green")
        

        if self._ui.fei_compatible == 1:

            if self._ui.SimMode ==1:
                for i in range(80):
                    self.can2.flip_all_off(i)
            else:
                for i in range(80):
                    self.can2.flip_all_on(i)

            if self._ui.SimMode==1:
                self._ui.sim_button.config(bg="Green")
                #for i in range(len(list(itertools.chain(self._ui.dig_ip_button,self._ui.dig_op_button,self._ui.volt_toggle,self._ui.pwm_ip_toggle,self._ui.freq_toggle,self._ui.pulse_toggle)))):
                for i in range(len(all_widgets)):
                    try:
                        all_widgets[i].config(state=tk.NORMAL)
                    except AttributeError:
                        pass
                for i in range(80):
                    self.can2.flip_all_on(i)
            elif self._ui.SimMode==0: 
                self._ui.sim_button.config(bg="Red")
                #for i in range(len(list(itertools.chain(self._ui.dig_ip_button,self._ui.dig_op_button,self._ui.volt_toggle,self._ui.pwm_ip_toggle,self._ui.freq_toggle,self._ui.pulse_toggle)))):
                for i in range(len(all_widgets)):
                    try:
                        all_widgets[i].config(state=tk.DISABLED,bg="azure3")
                    except AttributeError:
                        #all_widgets[i].config(state=tk.DISABLED)
                        pass
                for i in range(80):
                    self.can2.flip_all_off(i)

            
    def update_cpu(self):          
        """
        Displays CPU usage under Settings tab
        """
        if self._ui.fei_compatible == 1:
            cpu=str(psutil.cpu_percent(0.5))+'%'
            self._ui.cpu_entry.delete(0,100)
            self._ui.cpu_entry.insert(0, cpu)
        
    #Don't touch this
    def mainloop(self):
        tk.mainloop()