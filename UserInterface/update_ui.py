import itertools
import tkinter as tk
from tkinter import ttk
from functools import partial
import threading
import psutil
from HwConnect.CAN_FEI import *


class update_ui:

    global _ui, io_ob

    def __init__(self, ob1, ob2):
        """
        This module handles all updating of UI widgets and displayed values
        :param ob1: Set to _ui...references global_defines
        :param ob2: Set to io_ob...initially referenced IO_Ctrl(deprecated)
        """
        self._ui = ob1
        self.can2 = CAN_FEI(ob1)
        self.label_refresh_rate=0

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
        """
        Function to update UI based on dictionary data.

        Tied to First 7 SPN Tabs.

        This is what causes the buttons to flash red and green in testing mode.
        """
        for key in self._ui.UI_dict:
            data = self._ui.UI_dict[key]

            try:
                # DIG I/P
                if key in self._ui.dig_ip_spn:
                    ind = self._ui.dig_ip_spn.index(key)
                    if self._ui.dig_state[key] == 1:
                        self._ui.dig_ip_button[ind].config(bg="Green")
                    else:
                        self._ui.dig_ip_button[ind].config(
                            bg="Red")  # runtime error
                    i = ind
                    if i < 19:
                        self._ui.dig_ip_button[i].grid(row=i, column=1)
                    else:
                        self._ui.dig_ip_button[i].grid(row=i - 19, column=4)

                # DIG O/P
                elif key in self._ui.dig_op_spn:
                    ind = self._ui.dig_op_spn.index(
                        key)  # find position of that spn
                    if data == 1:
                        self._ui.dig_op_button[ind].config(bg="Green")
                    else:
                        self._ui.dig_op_button[ind].config(bg="Red")
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

                # Update Voltage Tab
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

                # Update PWM I/P tab
                elif key in self._ui.pwm_ip_spn:
                    ind = self._ui.pwm_ip_spn.index(key)
                    self._ui.pwm_ip_label[ind].delete(0, 100)
                    self._ui.pwm_ip_label[ind].insert(0, data)

                    if self._ui.SimMode == 1:
                        if self._ui.pwm_state[key] == 1:
                            self._ui.pwm_ip_toggle[ind].config(bg="Green")
                        else:
                            self._ui.pwm_ip_toggle[ind].config(bg="Red")

                # Update PWM O/P tab
                elif key in self._ui.pwm_op_spn:
                    ind = self._ui.pwm_op_spn.index(key)
                    self._ui.pwm_op_label[ind].delete(0, 100)
                    self._ui.pwm_op_label[ind].insert(0, data)

                # Update Freq Tab
                elif key in self._ui.fq_ip_spn:
                    ind = self._ui.fq_ip_spn.index(key)
                    self._ui.freq_label[ind].delete(0, 100)
                    self._ui.freq_label[ind].insert(0, data)

                    if self._ui.SimMode == 1:
                        if self._ui.freq_state[key] == 1:
                            self._ui.freq_toggle[ind].config(bg="Green")
                        else:
                            self._ui.freq_toggle[ind].config(bg="Red")

                # Update Pulse tab
                elif key in self._ui.pulse_spn:
                    ind = self._ui.pulse_spn.index(key)
                    self._ui.pulse_label[ind].delete(0, 100)
                    self._ui.pulse_label[ind].insert(0, data)

                    if self._ui.SimMode == 1:
                        if self._ui.pulse_state[key] == 1:
                            self._ui.pulse_toggle[ind].config(bg="Green")
                        else:
                            self._ui.pulse_toggle[ind].config(bg="Red")

            except RuntimeError:
                pass

    def update_ui_driveline(self):
        for i in range(len(self._ui.sp_val)):
            self._ui.drive_label[i].delete(0, 100)
            self._ui.drive_label[i].insert(
                0, "{:.2f}".format(float(self._ui.sp_val[i])))
        self._ui.current_spd_label.delete(0, 100)
        self._ui.current_spd_label.insert(
            0, "{:.2f}".format(float(self._ui.current_spd)))
        self._ui.pto_lsd_label.delete(0,100)
        self._ui.pto_lsd_label.insert(0, "{:.2f}".format(float(self._ui.current_spd)))
        self._ui.pto_hsd_label.delete(0,100)
        self._ui.pto_hsd_label.insert(0, "{:.2f}".format(float(self._ui.PTO_HSD)))
        self._ui.Aux_PTO_enabled_label.delete(0,100)
        self._ui.Aux_PTO_enabled_label.insert(0, int(self._ui.Aux_PTO_enabled))

    def update_ui_clrm(self):
        if self._ui.clrm_enabled == 1:
            self._ui.clrm_label.delete(0, 100)
            self._ui.clrm_label.insert(
                0, "{:.2f}".format(float(self._ui.tail_sensor_spd)))

    def update_ui_ghcv(self):
        self._ui.open_label.delete(0, 100)
        self._ui.open_label.insert(0, "{:.2f}".format(
            float(self._ui.cover_open_sensor)))
        self._ui.close_label.delete(0, 100)
        self._ui.close_label.insert(0, "{:.2f}".format(
            float(self._ui.cover_close_sensor)))

        self._ui.ghcv_label_open.delete(0, 100)
        self._ui.ghcv_label_open.insert(
            0, "{:.2f}".format(float(self._ui.g_opened_tmr_ms_u16)))
        self._ui.ghcv_label_close.delete(0, 100)
        self._ui.ghcv_label_close.insert(
            0, "{:.2f}".format(float(self._ui.g_closed_tmr_ms_u16)))

    def update_ui_rsch(self):
        self._ui.rsch_label.delete(0, 100)
        self._ui.rsch_label.insert(
            0, "{:.2f}".format(float(self._ui.rsch_spd)))

    def update_ui_ghts(self):
        self._ui.ghts_label_pwm.delete(0, 100)
        self._ui.ghts_label_pwm.insert(
            0, "{:.2f}".format(float(self._ui.ghts_pwm)))

        self._ui.ghts_label_pos.delete(0, 100)
        self._ui.ghts_label_pos.insert(
            0, "{:.2f}".format(float(self._ui.ghts_position)))

        self._ui.ghts_label_current.delete(0, 100)
        self._ui.ghts_label_current.insert(
            0, "{:.2f}".format(float(self._ui.ghts_current)))

        self._ui.ghts_label_pos_volt.delete(0, 100)
        self._ui.ghts_label_pos_volt.insert(
            0, "{:.2f}".format(float(self._ui.ghts_position_volt)))

        if self._ui.cradle_status == 0:
            self._ui.cradle_button.config(bg="Red")
        else:
            self._ui.cradle_button.config(bg="Green")

    def update_ui_rsck(self):
        self._ui.rsck_label_in_out_current.delete(0, 100)
        self._ui.rsck_label_in_out_current.insert(
            0, "{:.2f}".format(float(self._ui.in_out_curr)))

        self._ui.rsck_label_in_out_pwm.delete(0, 100)
        self._ui.rsck_label_in_out_pwm.insert(
            0, "{:.2f}".format(float(self._ui.in_out_pwm)))

        self._ui.rsck_label_high_speed_current.delete(0, 100)
        self._ui.rsck_label_high_speed_current.insert(
            0, "{:.2f}".format(float(self._ui.high_speed_current)))

        self._ui.rsck_label_high_speed_pwm.delete(0, 100)
        self._ui.rsck_label_high_speed_pwm.insert(
            0, "{:.2f}".format(float(self._ui.high_speed_pwm)))

        self._ui.rsck_label_pos.delete(0, 100)
        self._ui.rsck_label_pos.insert(
            0, "{:.2f}".format(float(self._ui.rsck_pos)))

        self._ui.rsck_label_volt.delete(0, 100)
        self._ui.rsck_label_volt.insert(
            0, "{:.2f}".format(float(self._ui.rsck_volt)))

    def update_ui_ghps(self):
        self._ui.ghps_curr_label.delete(0, 100)
        self._ui.ghps_curr_label.insert(
            0, "{:.2f}".format(float(self._ui.ghps_curr)))

        self._ui.ghps_pwm_label.delete(0, 100)
        self._ui.ghps_pwm_label.insert(
            0, "{:.2f}".format(float(self._ui.ghps_pwm)))

        self._ui.ghps_pos_label.delete(0, 100)
        self._ui.ghps_pos_label.insert(
            0, "{:.2f}".format(float(self._ui.ghps_pos)))

        self._ui.ghps_pos_volt_label.delete(0, 100)
        self._ui.ghps_pos_volt_label.insert(
            0, "{:.2f}".format(float(self._ui.ghps_pos_volt)))

        if self._ui.ghps_bridge_enable == 0:
            self._ui.ghps_bridge_button.config(bg="Red")
        else:
            self._ui.ghps_bridge_button.config(bg="Green")

    # def update_ui_thcc(self):
    #     self._ui.thcc_curr_label.delete(0, 100)
    #     self._ui.thcc_curr_label.insert(
    #         0, "{:.2f}".format(float(self._ui.thcc_curr)))

    #     self._ui.thcc_pwm_label.delete(0, 100)
    #     self._ui.thcc_pwm_label.insert(
    #         0, "{:.2f}".format(float(self._ui.thcc_pwm)))

    #     self._ui.thcc_pos_label.delete(0, 100)
    #     self._ui.thcc_pos_label.insert(
    #         0, "{:.2f}".format(float(self._ui.thcc_pos)))

    #     self._ui.thcc_pos_volt_label.delete(0, 100)
    #     self._ui.thcc_pos_volt_label.insert(
    #         0, "{:.2f}".format(float(self._ui.thcc_pos_volt)))

    #     if self._ui.thcc_bridge_enable == 0:
    #         self._ui.thcc_bridge_button.config(bg="Red")
    #     else:
    #         self._ui.thcc_bridge_button.config(bg="Green")

    def update_ui_thcc(self):
        self._ui.thcc_pos_label.delete(0, 100)
        self._ui.thcc_pos_label.insert(0, "{:.2f}".format(float(self._ui.thcc_pos)))
        
        self._ui.thcc_time_taken_label.delete(0, 100)
        self._ui.thcc_time_taken_label.insert(0, "{:.2f}".format(float(self._ui.thcc_time_taken)))

        self._ui.thcc_pot_volt_label.delete(0, 100)
        self._ui.thcc_pot_volt_label.insert(0, "{:.2f}".format(float(self._ui.thcc_pot_volt)))
        
        if self._ui.thcc_breakaway_state == 0:
            self._ui.thcc_breakaway_button.config(bg="Red")
            self._ui.thcc_breakaway_status.config(text="Disengaged")
        else:
            self._ui.thcc_breakaway_button.config(bg="Green")
            self._ui.thcc_breakaway_status.config(text="Engaged")

    def update_ui_gdpb(self):
        self._ui.gdpb_park_brake_sensor_label.delete(0, 100)
        self._ui.gdpb_park_brake_sensor_label.insert(0, "{:.2f}".format(float(self._ui.gdpb_park_brake_sensor)))
        self._ui.gdpb_disenage_sol_label.delete(0, 100)
        self._ui.gdpb_disenage_sol_label.insert(0, "{:.2f}".format(float(self._ui.gdpb_disenage_sol)))      
    
    def update_ui_gdhd(self):
        self._ui.gdhd_fwd_sol_label.delete(0, 100)
        self._ui.gdhd_fwd_sol_label.insert(0, "{:.2f}".format(float(self._ui.gdhd_fwd_sol)))
        self._ui.gdhd_rev_sol_label.delete(0, 100)
        self._ui.gdhd_rev_sol_label.insert(0, "{:.2f}".format(float(self._ui.gdhd_rev_sol)))
        self._ui.gdhd_ground_speed_label.delete(0, 100)
        self._ui.gdhd_ground_speed_label.insert(0, "{:.2f}".format(float(self._ui.gdhd_ground_speed)))
        self._ui.gdhd_gear_speed_label.delete(0, 100)
        self._ui.gdhd_gear_speed_label.insert(0, "{:.2f}".format(float(self._ui.gdhd_gear_speed)))

    def update_ui_clfn(self):
        self._ui.clfn_RPM_label.delete(0, 100)
        self._ui.clfn_RPM_label.insert(
            0, "{:.2f}".format(float(self._ui.clfn_rpm)))

    def update_ui_rssp(self):
        self._ui.rssp_right_spd_label.delete(0, 100)
        self._ui.rssp_right_spd_label.insert(
            0, "{:.2f}".format(float(self._ui.rssp_right_spd)))

        self._ui.rssp_right_curr_label.delete(0, 100)
        self._ui.rssp_right_curr_label.insert(
            0, "{:.2f}".format(float(self._ui.rssp_right_curr)))

        self._ui.rssp_left_spd_label.delete(0, 100)
        self._ui.rssp_left_spd_label.insert(
            0, "{:.2f}".format(float(self._ui.rssp_left_spd)))

        self._ui.rssp_left_curr_label.delete(0, 100)
        self._ui.rssp_left_curr_label.insert(
            0, "{:.2f}".format(float(self._ui.rssp_left_curr)))

    def update_ui_hdhr(self):
        self._ui.hdhr_type_volt_label.delete(0, 100)
        self._ui.hdhr_type_volt_label.insert(
            0, "{:.2f}".format(float(self._ui.hdhr_type_volt)))

        self._ui.hdhr_ext1_volt_label.delete(0, 100)
        self._ui.hdhr_ext1_volt_label.insert(
            0, "{:.2f}".format(float(self._ui.hdhr_ext1_volt)))

        self._ui.hdhr_ext2_volt_label.delete(0, 100)
        self._ui.hdhr_ext2_volt_label.insert(
            0, "{:.2f}".format(float(self._ui.hdhr_ext2_volt)))


    def update_ui_hdhc(self):
        ##### Just for testing purpose ####
        self._ui.hdhc_lift_prs_volt_pot_label.delete(0, 100)
        self._ui.hdhc_lift_prs_volt_pot_label.insert(0, int(self._ui.hdhc_lift_prs_volt_pot))
        self._ui.hdhc_feeder_angle_volt_pot_label.delete(0, 100)
        self._ui.hdhc_feeder_angle_volt_pot_label.insert(0, int(self._ui.hdhc_feeder_angle_volt_pot))
        self._ui.hdhc_lh_height_tilt_volt_pot_label.delete(0, 100)
        self._ui.hdhc_lh_height_tilt_volt_pot_label.insert(0, int(self._ui.hdhc_lh_height_tilt_volt_pot))
        self._ui.hdhc_center_lh_height_volt_pot_label.delete(0, 100)
        self._ui.hdhc_center_lh_height_volt_pot_label.insert(0, int(self._ui.hdhc_center_lh_height_volt_pot))
        self._ui.hdhc_center_rh_height_volt_pot_label.delete(0, 100)
        self._ui.hdhc_center_rh_height_volt_pot_label.insert(0, int(self._ui.hdhc_center_rh_height_volt_pot))
        self._ui.hdhc_rh_height_tilt_volt_pot_label.delete(0, 100)
        self._ui.hdhc_rh_height_tilt_volt_pot_label.insert(0, int(self._ui.hdhc_rh_height_tilt_volt_pot))
        self._ui.hdhc_lateral_position_volt_pot_label.delete(0, 100)
        self._ui.hdhc_lateral_position_volt_pot_label.insert(0, int(self._ui.hdhc_lateral_position_volt_pot))
        
        
    def update_ui_gdst(self):
        self._ui.gdst_left_track_label.delete(0, 100)
        self._ui.gdst_left_track_label.insert(0, "{:.2f}".format(float(self._ui.gdst_leftTensionInput)))
        self._ui.gdst_right_track_label.delete(0, 100)
        self._ui.gdst_right_track_label.insert(0, "{:.2f}".format(float(self._ui.gdst_rightTensionInput)))
        self._ui.gdst_left_front_label.delete(0, 100)
        self._ui.gdst_left_front_label.insert(0, "{:.2f}".format(float(self._ui.gdst_leftFrontInput)))
        self._ui.gdst_left_rear_label.delete(0, 100)
        self._ui.gdst_left_rear_label.insert(0, "{:.2f}".format(float(self._ui.gdst_leftRearInput)))
        self._ui.gdst_right_front_label.delete(0, 100)
        self._ui.gdst_right_front_label.insert(0, "{:.2f}".format(float(self._ui.gdst_rightFrontInput)))
        self._ui.gdst_right_rear_label.delete(0, 100)
        self._ui.gdst_right_rear_label.insert(0, "{:.2f}".format(float(self._ui.gdst_rightRearInput)))

        ################# JUST FOR TESTING AND COMPARE ##################
        self._ui.gdst_LeftTensionPressure_pot_label.delete(0, 100)
        self._ui.gdst_LeftTensionPressure_pot_label.insert(0, "{:.2f}".format(float(self._ui.LeftTensionPressure_pot)))
        self._ui.gdst_RightTensionPressure_pot_label.delete(0, 100)
        self._ui.gdst_RightTensionPressure_pot_label.insert(0, "{:.2f}".format(float(self._ui.RightTensionPressure_pot)))
        self._ui.gdst_LeftFrontDisp_pot_label.delete(0, 100)
        self._ui.gdst_LeftFrontDisp_pot_label.insert(0, "{:.2f}".format(float(self._ui.LeftFrontDisp_pot)))
        self._ui.gdst_LeftRearDisp_pot_label.delete(0, 100)
        self._ui.gdst_LeftRearDisp_pot_label.insert(0, "{:.2f}".format(float(self._ui.LeftRearDisp_pot)))
        self._ui.gdst_RightFrontDisp_pot_label.delete(0, 100)
        self._ui.gdst_RightFrontDisp_pot_label.insert(0, "{:.2f}".format(float(self._ui.RightFrontDisp_pot)))
        self._ui.gdst_RightRearDisp_pot_label.delete(0, 100)
        self._ui.gdst_RightRearDisp_pot_label.insert(0, "{:.2f}".format(float(self._ui.RightRearDisp_pot)))
        #################################################################
        
    def update_ui_fffa(self):
        self._ui.fffa_min_position_label.delete(0, 100)
        self._ui.fffa_min_position_label.insert(0, int(self._ui.fffa_min_position))
        self._ui.fffa_max_position_label.delete(0, 100)
        self._ui.fffa_max_position_label.insert(0, int(self._ui.fffa_max_position))
        self._ui.fffa_travel_rate_label.delete(0, 100)
        self._ui.fffa_travel_rate_label.insert(0, int(self._ui.fffa_travel_rate))
        self._ui.fffa_sol_fore_label.delete(0, 100)
        self._ui.fffa_sol_fore_label.insert(0, int(self._ui.fffa_sol_fore))
        self._ui.fffa_sol_aft_label.delete(0, 100)
        self._ui.fffa_sol_aft_label.insert(0, int(self._ui.fffa_position_volt))
        self._ui.fffa_position_pot_label.delete(0, 100)
        self._ui.fffa_position_pot_label.insert(0, int(self._ui.fffa_position_pot))


    def update_ui_hdfn(self):
        self._ui.hdfn_hor_pos_label.delete(0, 100)
        self._ui.hdfn_hor_pos_label.insert(
            0, "{:.2f}".format(float(self._ui.hdfn_hor_pos)))

        self._ui.hdfn_ver_pos_label.delete(0, 100)
        self._ui.hdfn_ver_pos_label.insert(
            0, "{:.2f}".format(float(self._ui.hdfn_ver_pos)))

        self._ui.hdfn_vari_pos_label.delete(0, 100)
        self._ui.hdfn_vari_pos_label.insert(
            0, "{:.2f}".format(float(self._ui.hdfn_vari_pos)))

        self._ui.hdfn_reel_spd_label.delete(0, 100)
        self._ui.hdfn_reel_spd_label.insert(
            0, "{:.2f}".format(float(self._ui.hdfn_reel_spd)))

        self._ui.hdfn_ffa_spd_label.delete(0, 100)
        self._ui.hdfn_ffa_spd_label.insert(
            0, "{:.2f}".format(float(self._ui.hdfn_ffa_spd)))

    def update_ui_agge(self):
        self._ui.agge_angle_label.delete(0, 100)
        self._ui.agge_angle_label.insert(0, "{:.2f}".format(float(self._ui.agge_angle)))
        self._ui.agge_wheel_label.delete(0, 100)
        self._ui.agge_wheel_label.insert(0, "{:.2f}".format(float(self._ui.agge_wheel)))
        self._ui.agge_right_steer_sol_label.delete(0, 100)
        self._ui.agge_right_steer_sol_label.insert(0, "{:.2f}".format(float(self._ui.agge_steer_right)))
        self._ui.agge_left_steer_sol_label.delete(0, 100)
        self._ui.agge_left_steer_sol_label.insert(0, "{:.2f}".format(float(self._ui.agge_steer_left)))

        if self._ui.agge_wheel == 3500:
            self._ui.agge_steering_wheel_override.config(bg="Red")
        elif self._ui.agge_wheel == 7000:
            self._ui.agge_steering_wheel_override.config(bg="Green")

    def update_ui_rrts(self):
        self._ui.rrts_rocktrap_open_sol_label.delete(0,100)
        self._ui.rrts_rocktrap_open_sol_label.insert(0, "{:.2f}".format(float(self._ui.rrts_rocktrap_open)))
        self._ui.rrts_rocktrap_close_sol_label.delete(0,100)
        self._ui.rrts_rocktrap_close_sol_label.insert(0, "{:.2f}".format(float(self._ui.rrts_rocktrap_close)))

        if self._ui.rrts_rocktrap_close_sw == 0:
            self._ui.rrts_close_switch.config(bg="Red")
        else:
            self._ui.rrts_rocktrap_open_switch.config(bg="Green")


    def update_settings(self):
        """
        Updates Color Of Settings Buttons depending on their linked value.
        """
        all_widgets = list(itertools.chain(self._ui.dig_ip_option, self._ui.open_option, self._ui.volt_toggle,
                           self._ui.pwm_ip_toggle, self._ui.freq_toggle, self._ui.pulse_toggle, self._ui.actuator_load, self._ui.actuator_set))
        if self._ui.KeyIsON == 1:
            self._ui.Key_Button.config(bg="Green")
        elif self._ui.KeyIsON == 0:
            self._ui.Key_Button.config(bg="Red")

        if self._ui.debug_mode == 0:
            self._ui.debug_mode_button.config(bg="Red")
        elif self._ui.debug_mode == 1:
            self._ui.debug_mode_button.config(bg="Green")

    def update_cc_console(self):
        if self._ui.thresher_engage_state == 0:
            self._ui.thresher_engage_button.config(bg="Red")
        else:
            self._ui.thresher_engage_button.config(bg="Green")

        if self._ui.feeder_engage_state == 0:
            self._ui.feeder_engage_button.config(bg="Red")
        else:
            self._ui.feeder_engage_button.config(bg="Green")
        

    def update_cpu(self):
        """
        Displays CPU usage under Settings tab

        Uses 'psutil'
        """
        if self._ui.fei_compatible == 1:
            cpu = str(psutil.cpu_percent(0.5))+'%'
            self._ui.cpu_entry.delete(0, 100)
            self._ui.cpu_entry.insert(0, cpu)

    def update_ui_offline(self):
        """
        Part of ui_update thread.

        Checks to see if any boards are offline. If so, linked UI widgets will be disabled.
        """
        for bno in self._ui.board_wid_dict:
            online = 0
            if(bno in self._ui.ping_dict and self._ui.ping_dict[bno] == 1):
                online = 1

            for widg in self._ui.board_wid_dict[bno]:
                try:
                    if(online):
                        widg.config(state=tk.NORMAL)
                    else:
                        widg.config(state=tk.DISABLED)
                        if(widg.__class__.__name__ != "OptionMenu"):
                            widg.config(bg="azure3")
                except AttributeError:
                    pass

    def mainloop(self):
        """
        Holds Tkinter .mainloop()

        Main function for running UI. 

        DO NOT REMOVE
        """
        tk.mainloop()
