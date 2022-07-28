import itertools
from tkinter import ttk
import tkinter as tk
from tkinter import *
import subprocess
import can


class global_defines:
    # testing with all hardware : 0, else 1
    testing_active = 1
    debug_mode = 0
    debug_mode_button = 0

    # Create the master object
    master = tk.Tk()
    master.geometry("1450x1190")
    master.title("Raspberry Pi simulator - FEI")
    mygreen = "#CEF743"
    red = "#B1CCE7"
    black = "#000000"

    style = ttk.Style()
    style.theme_create("raspi", parent="alt", settings={
        "TNotebook": {"configure": {"tabmargins": [3, 5, 3, 0]}},
        "TNotebook.Tab": {
            "configure": {"padding": [5, 1], "background": "lightblue", "foreground": black},
            "map": {"background": [("selected", "SteelBlue1")],
                    "expand": [("selected", [1, 1, 1, 0])]}}})
    style.theme_use("raspi")

    tc = ttk.Notebook(master)

    # DIG I/P
    tc_dig_ip = ttk.Frame(tc)
    tc_dig_ip.pack(side='left')
    dig_ip_canvas = Canvas(tc_dig_ip, width=6, height=6,
                           scrollregion=(0, 0, 1450, 1100))
    hbar = Scrollbar(tc_dig_ip, orient=HORIZONTAL)
    hbar.pack(side=BOTTOM, fill=X)
    hbar.config(command=dig_ip_canvas.xview)
    vbar = Scrollbar(tc_dig_ip, orient=VERTICAL)
    vbar.pack(side=RIGHT, fill=Y)
    vbar.config(command=dig_ip_canvas.yview)
    dig_ip_canvas.config(width=6, height=6)
    dig_ip_canvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
    dig_ip_canvas.pack(side=LEFT, expand=True, fill=BOTH)
    dig_ip_frame = Frame(dig_ip_canvas)
    dig_ip_canvas.create_window((0, 0), window=dig_ip_frame, anchor="nw")

    # DIG O/P
    tc_dig_op = ttk.Frame(tc)
    tc_dig_op.pack(side='left')
    dig_op_canvas = Canvas(tc_dig_op, width=6, height=6,
                           scrollregion=(0, 0, 1450, 1100))
    hbar = Scrollbar(tc_dig_op, orient=HORIZONTAL)
    hbar.pack(side=BOTTOM, fill=X)
    hbar.config(command=dig_op_canvas.xview)
    vbar = Scrollbar(tc_dig_op, orient=VERTICAL)
    vbar.pack(side=RIGHT, fill=Y)
    vbar.config(command=dig_op_canvas.yview)
    dig_op_canvas.config(width=6, height=6)
    dig_op_canvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
    dig_op_canvas.pack(side=LEFT, expand=True, fill=BOTH)
    dig_op_frame = Frame(dig_op_canvas)
    dig_op_canvas.create_window((0, 0), window=dig_op_frame, anchor="nw")

    # VOLTAGE
    tc_vol_ip = ttk.Frame(tc)
    tc_vol_ip.pack(side='left')
    vol_ip_canvas = Canvas(tc_vol_ip, width=6, height=6,
                           scrollregion=(0, 0, 1450, 1100))
    hbar = Scrollbar(tc_vol_ip, orient=HORIZONTAL)
    hbar.pack(side=BOTTOM, fill=X)
    hbar.config(command=vol_ip_canvas.xview)
    vbar = Scrollbar(tc_vol_ip, orient=VERTICAL)
    vbar.pack(side=RIGHT, fill=Y)
    vbar.config(command=vol_ip_canvas.yview)
    vol_ip_canvas.config(width=6, height=6)
    vol_ip_canvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
    vol_ip_canvas.pack(side=LEFT, expand=True, fill=BOTH)
    volt_ip_frame = Frame(vol_ip_canvas)
    vol_ip_canvas.create_window((0, 0), window=volt_ip_frame, anchor="nw")

    # PWM I/P
    tc_pwm_ip = ttk.Frame(tc)
    tc_pwm_ip.pack(side='left')
    pwm_ip_canvas = Canvas(tc_pwm_ip, width=6, height=6,
                           scrollregion=(0, 0, 1450, 1100))
    hbar = Scrollbar(tc_pwm_ip, orient=HORIZONTAL)
    hbar.pack(side=BOTTOM, fill=X)
    hbar.config(command=pwm_ip_canvas.xview)
    vbar = Scrollbar(tc_pwm_ip, orient=VERTICAL)
    vbar.pack(side=RIGHT, fill=Y)
    vbar.config(command=pwm_ip_canvas.yview)
    pwm_ip_canvas.config(width=6, height=6)
    pwm_ip_canvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
    pwm_ip_canvas.pack(side=LEFT, expand=True, fill=BOTH)
    pwm_ip_frame = Frame(pwm_ip_canvas)
    pwm_ip_canvas.create_window((0, 0), window=pwm_ip_frame, anchor="nw")

    # PWM O/P
    tc_pwm_op = ttk.Frame(tc)
    tc_pwm_op.pack(side='left')
    pwm_op_canvas = Canvas(tc_pwm_op, width=6, height=6,
                           scrollregion=(0, 0, 1450, 1100))
    hbar = Scrollbar(tc_pwm_op, orient=HORIZONTAL)
    hbar.pack(side=BOTTOM, fill=X)
    hbar.config(command=pwm_op_canvas.xview)
    vbar = Scrollbar(tc_pwm_op, orient=VERTICAL)
    vbar.pack(side=RIGHT, fill=Y)
    vbar.config(command=pwm_op_canvas.yview)
    pwm_op_canvas.config(width=6, height=6)
    pwm_op_canvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
    pwm_op_canvas.pack(side=LEFT, expand=True, fill=BOTH)
    pwm_op_frame = Frame(pwm_op_canvas)
    pwm_op_canvas.create_window((0, 0), window=pwm_op_frame, anchor="nw")

    # Frequency
    tc_freq_ip = ttk.Frame(tc)
    tc_freq_ip.pack(side='left')
    freq_ip_canvas = Canvas(tc_freq_ip, width=6, height=6,
                            scrollregion=(0, 0, 1450, 1100))
    hbar = Scrollbar(tc_freq_ip, orient=HORIZONTAL)
    hbar.pack(side=BOTTOM, fill=X)
    hbar.config(command=freq_ip_canvas.xview)
    vbar = Scrollbar(tc_freq_ip, orient=VERTICAL)
    vbar.pack(side=RIGHT, fill=Y)
    vbar.config(command=freq_ip_canvas.yview)
    freq_ip_canvas.config(width=6, height=6)
    freq_ip_canvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
    freq_ip_canvas.pack(side=LEFT, expand=True, fill=BOTH)
    freq_ip_frame = Frame(freq_ip_canvas)
    freq_ip_canvas.create_window((0, 0), window=freq_ip_frame, anchor="nw")

    # Pulse
    tc_pulse = ttk.Frame(tc)
    tc_pulse.pack(side='left')
    pulse_canvas = Canvas(tc_pulse, width=6, height=6,
                          scrollregion=(0, 0, 1450, 1100))
    hbar = Scrollbar(tc_pulse, orient=HORIZONTAL)
    hbar.pack(side=BOTTOM, fill=X)
    hbar.config(command=pulse_canvas.xview)
    vbar = Scrollbar(tc_pulse, orient=VERTICAL)
    vbar.pack(side=RIGHT, fill=Y)
    vbar.config(command=pulse_canvas.yview)
    pulse_canvas.config(width=6, height=6)
    pulse_canvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
    pulse_canvas.pack(side=LEFT, expand=True, fill=BOTH)
    pulse_frame = Frame(pulse_canvas)
    pulse_canvas.create_window((0, 0), window=pulse_frame, anchor="nw")

    # Driveline
    tc_drive = ttk.Frame(tc)
    tc_drive.pack(side='left')
    drive_canvas = Canvas(tc_drive, width=6, height=6,
                          scrollregion=(0, 0, 1450, 1100))
    hbar = Scrollbar(tc_drive, orient=HORIZONTAL)
    hbar.pack(side=BOTTOM, fill=X)
    hbar.config(command=drive_canvas.xview)
    vbar = Scrollbar(tc_drive, orient=VERTICAL)
    vbar.pack(side=RIGHT, fill=Y)
    vbar.config(command=drive_canvas.yview)
    drive_canvas.config(width=6, height=6)
    drive_canvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
    drive_canvas.pack(side=LEFT, expand=True, fill=BOTH)
    driveline_frame = Frame(drive_canvas)
    drive_canvas.create_window((0, 0), window=driveline_frame, anchor="nw")

    # UCM1
    tc_plant_model_ucm1 = ttk.Frame(tc)
    tc_plant_model_ucm1.pack(side='left')
    ucm1_canvas = Canvas(tc_plant_model_ucm1, width=6,
                         height=6, scrollregion=(0, 0, 1450, 1100))
    hbar = Scrollbar(tc_plant_model_ucm1, orient=HORIZONTAL)
    hbar.pack(side=BOTTOM, fill=X)
    hbar.config(command=ucm1_canvas.xview)
    vbar = Scrollbar(tc_plant_model_ucm1, orient=VERTICAL)
    vbar.pack(side=RIGHT, fill=Y)
    vbar.config(command=ucm1_canvas.yview)
    ucm1_canvas.config(width=6, height=6)
    ucm1_canvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
    ucm1_canvas.pack(side=LEFT, expand=True, fill=BOTH)
    plant_model_ucm1_frame = Frame(ucm1_canvas)
    ucm1_canvas.create_window(
        (0, 0), window=plant_model_ucm1_frame, anchor="nw")

    # UCM2
    tc_plant_model_ucm2 = ttk.Frame(tc)
    tc_plant_model_ucm2.pack(side='left')
    ucm2_canvas = Canvas(tc_plant_model_ucm2, width=6,
                         height=6, scrollregion=(0, 0, 1450, 1100))
    hbar = Scrollbar(tc_plant_model_ucm2, orient=HORIZONTAL)
    hbar.pack(side=BOTTOM, fill=X)
    hbar.config(command=ucm2_canvas.xview)
    vbar = Scrollbar(tc_plant_model_ucm2, orient=VERTICAL)
    vbar.pack(side=RIGHT, fill=Y)
    vbar.config(command=ucm2_canvas.yview)
    ucm2_canvas.config(width=6, height=6)
    ucm2_canvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
    ucm2_canvas.pack(side=LEFT, expand=True, fill=BOTH)
    plant_model_ucm2_frame = Frame(ucm2_canvas)
    ucm2_canvas.create_window(
        (0, 0), window=plant_model_ucm2_frame, anchor="nw")

    # UCM3
    tc_plant_model_ucm3 = ttk.Frame(tc)
    tc_plant_model_ucm3.pack(side='left')
    ucm3_canvas = Canvas(tc_plant_model_ucm3, width=6,
                         height=6, scrollregion=(0, 0, 1450, 1100))
    hbar = Scrollbar(tc_plant_model_ucm3, orient=HORIZONTAL)
    hbar.pack(side=BOTTOM, fill=X)
    hbar.config(command=ucm3_canvas.xview)
    vbar = Scrollbar(tc_plant_model_ucm3, orient=VERTICAL)
    vbar.pack(side=RIGHT, fill=Y)
    vbar.config(command=ucm3_canvas.yview)
    ucm3_canvas.config(width=6, height=6)
    ucm3_canvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
    ucm3_canvas.pack(side=LEFT, expand=True, fill=BOTH)
    plant_model_ucm3_frame = Frame(ucm3_canvas)
    ucm3_canvas.create_window(
        (0, 0), window=plant_model_ucm3_frame, anchor="nw")

    # UCM4
    tc_plant_model_ucm4=ttk.Frame(tc)
    tc_plant_model_ucm4.pack(side='left')
    ucm4_canvas = Canvas (tc_plant_model_ucm4,width = 6, height =6, scrollregion=(0,0,1450,1100))
    hbar = Scrollbar(tc_plant_model_ucm4, orient=HORIZONTAL)
    hbar.pack(side=BOTTOM, fill=X)
    hbar.config(command=ucm4_canvas.xview)
    vbar = Scrollbar(tc_plant_model_ucm4, orient = VERTICAL)
    vbar.pack(side=RIGHT, fill=Y)
    vbar.config(command=ucm4_canvas.yview)
    ucm4_canvas.config(width=6, height=6)
    ucm4_canvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
    ucm4_canvas.pack(side=LEFT, expand=True, fill=BOTH)
    plant_model_ucm4_frame = Frame(ucm4_canvas)
    ucm4_canvas.create_window((0,0), window=plant_model_ucm4_frame, anchor="nw")


    # Settings
    tc_settings = ttk.Frame(tc)
    tc_settings.pack(side='left')
    settings_canvas = Canvas(tc_settings, width=6,
                             height=6, scrollregion=(0, 0, 1450, 1100))
    hbar = Scrollbar(tc_settings, orient=HORIZONTAL)
    hbar.pack(side=BOTTOM, fill=X)
    hbar.config(command=settings_canvas.xview)
    vbar = Scrollbar(tc_settings, orient=VERTICAL)
    vbar.pack(side=RIGHT, fill=Y)
    vbar.config(command=settings_canvas.yview)
    settings_canvas.config(width=6, height=6)
    settings_canvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
    settings_canvas.pack(side=LEFT, expand=True, fill=BOTH)
    setting_frame = Frame(settings_canvas)
    settings_canvas.create_window((0, 0), window=setting_frame, anchor="nw")

    def add_compatible(self):

        if self.fei_compatible == 1:
            # Open_to Tab
            self.tc_open = ttk.Frame(self.tc)
            self.tc_open.pack(side='left')
            self.open_canvas = Canvas(
                self.tc_open, width=6, height=6, scrollregion=(0, 0, 1450, 1100))
            self.hbar = Scrollbar(self.tc_open, orient=HORIZONTAL)
            self.hbar.pack(side=BOTTOM, fill=X)
            self.hbar.config(command=self.open_canvas.xview)
            self.vbar = Scrollbar(self.tc_open, orient=VERTICAL)
            self.vbar.pack(side=RIGHT, fill=Y)
            self.vbar.config(command=self.open_canvas.yview)
            self.open_canvas.config(width=6, height=6)
            self.open_canvas.pack(side=LEFT, expand=True, fill=BOTH)
            self.open_frame = Frame(self.open_canvas)
            self.open_canvas.create_window(
                (0, 0), window=self.open_frame, anchor="nw")

            # Actuator Tab
            self.tc_actuator = ttk.Frame(self.tc)
            self.tc_actuator.pack(side='left')
            self.actuator_canvas = Canvas(
                self.tc_actuator, width=6, height=6, scrollregion=(0, 0, 1450, 1100))
            self.hbar = Scrollbar(self.tc_actuator, orient=HORIZONTAL)
            self.hbar.pack(side=BOTTOM, fill=X)
            self.hbar.config(command=self.actuator_canvas.xview)
            self.vbar = Scrollbar(self.tc_actuator, orient=VERTICAL)
            self.vbar.pack(side=RIGHT, fill=Y)
            self.vbar.config(command=self.actuator_canvas.yview)
            self.actuator_canvas.config(width=6, height=6)
            self.actuator_canvas.config(width=6, height=6)
            self.actuator_canvas.pack(side=LEFT, expand=True, fill=BOTH)
            self.actuator_frame = Frame(self.actuator_canvas)
            self.actuator_canvas.create_window(
                (0, 0), window=self.actuator_frame, anchor="nw")

            self.tc.add(self.tc_open, text='Open')
            self.tc.add(self.tc_actuator, text='Actuator')

        self.tc.add(self.tc_dig_ip, text='DIG I/P')
        self.tc.add(self.tc_dig_op, text='DIG O/P')
        self.tc.add(self.tc_vol_ip, text='VOLTAGE')
        self.tc.add(self.tc_pwm_ip, text='PWM I/P')
        self.tc.add(self.tc_pwm_op, text='PWM O/P')
        self.tc.add(self.tc_freq_ip, text='Freq')
        self.tc.add(self.tc_pulse, text='Pulse')
        self.tc.add(self.tc_drive, text='Driveline')
        self.tc.add(self.tc_plant_model_ucm1, text='PlantModel_UCM1')
        self.tc.add(self.tc_plant_model_ucm2, text='PlantModel_UCM2')
        self.tc.add(self.tc_plant_model_ucm3, text='PlantModel_UCM3')
        self.tc.add(self.tc_plant_model_ucm4, text='PlantModel_UCM4')
        self.tc.add(self.tc_settings, text='Settings')

        self.tc.pack(expand=1, fill="both")

    # Non-UI Variables:

    eng_spd = tk.StringVar()
    chopper_type = 1
    chopper_type_var = tk.StringVar()
    dig_ip_option_var = []
    open_option_var = []
    HHMC_gear = tk.StringVar()
    IC_gear = tk.StringVar()
    Aux_PTO_enabled_str = tk.StringVar()
    feeder_type = tk.StringVar()
    unload_rate = tk.StringVar()

    # general spn/widgets
    toggle = 0  # Used for update_ui dictionary
    dig_ip_button = []  # Array of buttons listed on DIG I/P
    dig_ip_options = []  # Array of option menus listed on DIG I/P
    dig_op_button = []  # Array of buttons under DIG O/P
    open_option = []
    open_button = []
    open_mode = {}
    volt_label = []
    pwm_ip_label = []
    pwm_op_label = []
    freq_label = []
    pulse_label = []
    volt_button = []

    dig_ip_mode = {}
    volt_toggle = []  # list of toggle buttons on voltage tab
    relay_switch = []  # 1 for relay on, 0 for relay off

    pwm_ip_button = []
    pwm_ip_toggle = []
    freq_button = []
    freq_toggle = []
    button_pulse = []
    pulse_toggle = []
    brand = 0  # 0 = CIH, 1 = NH
    board_Num = 0  # 0 or Empty = Invalid Board.
    config_dict = {}

    # Create a list of all buttons and options for disabling at once.
    all_widgets = list(itertools.chain(dig_ip_button, dig_ip_options, dig_op_button, open_option, open_button,
                       volt_button, volt_toggle, pwm_ip_button, pwm_ip_toggle, freq_button, freq_toggle, button_pulse, pulse_toggle))

    # Parse Strings
    dig_ip_str = "DigitalInput"
    dig_op_str = "DigitalOutput"
    vol_ip_str = "VoltageInput"
    pwm_op_str = "PWMOutput"
    pwm_ip_str = "PWMINput"
    fq_ip_str = "FrequencyInput"
    pulse_str = "PulseInput"

    # Lists for Channel/Board
    ping_dict = {}  # Dictionary with Board Number : Boolean active value
    time_dict = {}  # Dictionary containing CAN timestamps
    board_dict = {}  # Dictionary with SPN : Board Number pairs
    # Actuator Widgets
    actuator_dict = {0: 0, 1: "actuator_1", 2: "actuator_2",
                     3: "actuator_3", 4: "actuator_4", 5: "actuator_5"}
    actuator_label = []
    actuator_load = []
    actuator_pos = []
    actuator_set = []
    actuator_btn = []

    board_list = []
    channel_dict = {}  # Dictionary with SPN : relay(channel) pairs
    dig_state = {}  # Dictionary with SPN : default state of 0
    board_wid_dict = {}  # Dictionary with Board No : [list of widget] pairs
    volt_state = {}
    freq_state = {}
    pulse_state = {}
    pwm_state = {}
    ground_dict = {}  # Contains SPNs that are open to battery xor ground
    bool_both = {}  # Indicate if both Channel and Board number are listed
    # Indicate if all board, channel, and openTo(Ground or Board or Both) are listed
    bool_all = {}
    UI_dict = {}
    UI_spn = []
    button_list = []
    spn_list = []
    name_list = []
    dig_ip_spn = []
    dig_ip_option = []
    dig_op_spn = []
    vol_ip_spn = []
    pwm_op_spn = []
    pwm_ip_spn = []
    fq_ip_spn = []
    pulse_spn = []
    dig_ip_name = []
    dig_op_name = []
    vol_ip_name = []
    pwm_op_name = []
    pwm_ip_name = []
    fq_ip_name = []
    pulse_name = []
    spare_list_1 = []
    spare_list_2 = []
    volt_string = []
    pwm_ip_string = []
    freq_string = []
    pulse_string = []
    type_dict = {}
    volt_scale_max_dict = {}
    volt_scale_default_dict = {}

    # driveline
    sp_name = ['Aux_PTO', 'Aux_PTO_Thresher', 'Pumps_ZE', 'Cross_Over_Belt', 'Unload_Belt_Drive',
               'Integral_Chopper',
               'HHMC', 'Unloading_stubshaft',
               'Unloading_Belt_Drive_2', 'Unloading_Gbx', 'Unl_Cross_Auger_Rear', 'Unloading_Gbx_2',
               'Unl_Cross_Auger_Rear',
               'Beater_Belt_Drive', 'Elevator_Drive_Belt', 'Elevator_Cross_Shaft',
               'Grain_Elev_Top_Shaft', 'Bubble_Up', 'Cleaning_Belt_Drive', 'Tailings_Cross_Auger_Rethresher',
               'Tailing_Gearbox', 'Tailings_Incline_Auger',
               'Eccentric', 'Main_Clean_Grain_Cross_Auger', 'Auger_Belt_Drive', 'XA_Clean_Grain_Cross_Auger',
               'Feeder_Hydromech', 'Rotor_RPM', 'Clutch_RPM', 'Feeder_Header_Gbx', 'Feeder_Jack_Shaft',
               'Feeder_Top_Shaft']

    sp_val = []
    drive_label = []

    current_spd = 0
    current_spd_label = 0
    reverserEngaged = 0
    feederreverserEngaged = 0
    ThreshingRotorStatus = 0
    ThreshingFeederStatus = 0
    Rotor_enabled = 1
    Feeder_enabled = 1
    rotor_pwm = 50
    feeder_pwm = 50
    flow = 1
    max_rotor_spd = 101
    max_Feeder_spd = 101
    rotor_incr = 1
    rotor_decr = 1
    max_feeder_spd = 101
    feeder_incr = 1
    feeder_decr = 1
    clutch_on = 1
    clutch_pwm = 1

    IC = 0
    HHMC = 1
    Gear0 = 0
    Gear1 = 1
    Gear2 = 2
    enabled = 1
    disabled = 0
    fixed = 0
    variable = 1
    slow_unload = 0
    fast_unload = 1

    PTO_LSD = 0
    PTO_HSD = 0
    pto_lsd_label = 0
    pto_hsd_label = 0
    Aux_PTO_enabled = 0

    Normal = 1
    Open_Circuit = 2

    # clrm
    tail_sensor_spd = 0
    periodstate = 1

    clrm_enabled = 1
    pulse = 10
    period = 80
    degree = 200

    clrm_plant_enabled = tk.StringVar()
    period_slide = tk.StringVar()
    pulse_slide = tk.StringVar()
    degree_slide = tk.StringVar()

    clrm_label = 0

    # ghcv
    cover_open_sensor = 0
    cover_close_sensor = 1
    ghcv_plant_enabled = tk.StringVar()
    error_open = tk.StringVar()
    error_close = tk.StringVar()
    ghcv_enabled = 1
    open_error = 0
    close_error = 0
    # remove it at last, only for testing below 4 lines
    cover_open = tk.StringVar()
    cover_closed = tk.StringVar()
    iscoveropenactive = 0
    iscoverclosedactive = 0
    g_min_sens_volt_mv_s32 = 3500
    g_max_sens_volt_mv_s32 = 7000
    g_error_sens_volt_mv_s32 = 8000
    if testing_active == 0:
        g_tmr_max_val_ms_u32 = 1500
        g_opened_tmr_ms_u16 = 1500
        g_closed_tmr_ms_u16 = 1500
    else:
        g_tmr_max_val_ms_u32 = 1500
        g_opened_tmr_ms_u16 = 1500
        g_closed_tmr_ms_u16 = 1500
    close_label = 0
    open_label = 0
    ghcv_label_open = 0
    ghcv_label_close = 0

    # rsch
    rsch_enabled = 1
    rsch_spd = 0
    crop_load_rsch = 0
    rsch_gear = 0
    rsch_type = 0

    chopper_plant_enabled = tk.StringVar()
    gear = tk.StringVar()
    load = tk.StringVar()
    rsch_type_select = tk.StringVar()
    rsch_label = 0

    # ghts
    ghts_enabled = 1
    ghts_pos_sensor_enabled = 1
    ghts_cradle_sensor_enabled = 1
    ghts_current = 0
    ghts_pwm = 0
    cradle_status = 0

    #Update values from new code (18052022)
    ghts_position = 200
    ghts_position_volt = 1470

    isswinginactive = 0
    isswingoutactive = 0

    ghts_enabled_input = tk.StringVar()
    ghts_pos_sensor_enabled_input = tk.StringVar()
    ghts_cradle_sensor_enabled_input = tk.StringVar()
    ghts_input_solenoid = tk.StringVar()
    ghts_output_solenoid = tk.StringVar()
    ghts_travel_limit = tk.StringVar()

    ghts_label_pwm = 0
    ghts_label_pos = 0
    ghts_label_current = 0
    ghts_label_pos_volt = 0
    cradle_button = 0

    g_pos_tick_inc_0p1_mV_s32 = 10
    g_min_pos_volt_mv_s32 = 933
    g_max_pos_volt_mv_s32 = 4300
    g_min_pos_mm_0p1_s32 = 0
    g_max_pos_mm_0p1_s32 = 120
    g_curr_crack_out_ma_s32 = 50
    g_curr_crack_in_ma_s32 = 50
    swing_in_current = 0
    swing_out_current = 0

    ghts_travel_limiter = 100

    # rsck
    rsck_enabled = 1
    in_curr = 0
    out_curr = 0
    in_out_curr = 0
    in_out_pwm = 0
    high_speed_current = 0
    high_speed_pwm = 0
    rsck_pos = 45
    rsck_max_volt = 4300
    rsck_min_volt = 1000
    rsck_volt = 2500
    rsck_travel_limiter = 100

    rsck_in_sol = 0
    rsck_out_sol = 0
    rsck_high_spd_sol = 0

    rsck_enabled_var = tk.StringVar()
    rsck_in_sol_var = tk.StringVar()
    rsck_out_sol_var = tk.StringVar()
    rsck_high_spd_sol_var = tk.StringVar()
    rsck_travel_limiter_var = tk.StringVar()

    rsck_tick_rate = 5

    rsck_label_in_out_current = 0
    rsck_label_in_out_pwm = 0
    rsck_label_high_speed_current = 0
    rsck_label_high_speed_pwm = 0
    rsck_label_pos = 0
    rsck_label_volt = 0

    rsck_label_in_current = 0
    rsck_label_out_current = 0


    # ghps
    ghps_enable = 1
    ghps_curr = 0
    ghps_pwm = 0
    ghps_h_curr = 0
    ghps_h_pwm = 0
    ghps_pos = 3000
    ghps_pos_volt = 2500
    ghps_bridge_enable = 0

    ghps_enable_var = tk.StringVar()
    ghps_h_curr_var = tk.StringVar()
    ghps_h_pwm_var = tk.StringVar()
    ghps_bridge_enable_var = tk.StringVar()

    ghps_bridge_button = 0
    ghps_pos_label = 0
    ghps_pos_volt_label = 0
    ghps_curr_label = 0
    ghps_pwm_label = 0

    ghps_max_volt = 4500
    ghps_min_volt = 500

    ghps_tick_rate_pos = 6

    # thcc
    thcc_enable = 1
    thcc_curr = 0
    thcc_pwm = 0
    thcc_h_curr = 0
    thcc_h_pwm = 0
    thcc_pos = 10
    thcc_pos_volt = 2500
    thcc_bridge_enable = 0
    thcc_rotor_gear = 0


    #added from new code:
    thcc_set_pos = 0
    thcc_pot_volt = 0
    thcc_breakaway_state = 1
    thcc_concave_state = 1
    thcc_time_taken = 0
    thcc_time_pos = 0
    thcc_sensor_link = 1


    thcc_enable_var = tk.StringVar()
    thcc_h_curr_var = tk.StringVar()
    thcc_h_pwm_var = tk.StringVar()
    thcc_sensor_link_var = tk.StringVar()

    thcc_bridge_button = 0
    thcc_pos_label = 0
    thcc_pos_volt_label = 0
    thcc_curr_label = 0
    thcc_pwm_label = 0
    thcc_pos_var = 0

    thcc_max_volt = 4500
    thcc_min_volt = 500

    thcc_tick_rate_pos = 6

    single_rotor = 0
    twin_rotor = 1
    thcc_off = 0
    thcc_on = 2
    rotor_gear = tk.StringVar()
    thcc_stat = tk.StringVar()


    #Added from new code :[gdpb, gdgs, gdhd]
    #gdpb
    gdpb_enable_var = tk.StringVar()
    gdpb_link_to_sensor_var = tk.StringVar()
    gdpb_park_brake_sensor_var = tk.StringVar()  

    gdpb_disenage_sol_label = 0
    gdpb_park_brake_sensor = 0.5 
    gdpb_enabled = 1
    gdpb_link_to_sensor = 1 
    gdpb_disenage_sol = 0 
    gdpb_RH_brake_pressure_state = 0 
    gdpb_LH_brake_pressure_state = 0 
    gdpb_park_brake_sensor_label = 0.5
    
    #gdgs
    gdgs_enable_var = tk.StringVar()
    gdgs_link_to_gearshift_var = tk.StringVar()
    gdgs_electric_shift_pos_sensor_var = tk.StringVar()

    gdgs_enabled = 1
    gdgs_gear_shift_inc = 0
    gdgs_gear_shift_dec = 0 
    gdgs_electric_shift_pos_sensor = 2.5
    gdgs_link_to_elec_pos_sensor = 1 
    gdgs_ground_drive_shift_label = 0  
    gdgs_electric_shift_pos_sensor_label = 2.5
    
    #gdhd
    gdhd_enable_var = tk.StringVar() 
    gdhd_motor_displacement_var = tk.StringVar()
    gdhd_pump_displacement_var = tk.StringVar()
    gdhd_enabled = 1

    gdhd_enabled = 1
    gdhd_fwd_sol_label = 0
    gdhd_rev_sol_label = 0
    gdhd_ground_speed_label = 0
    gdhd_gear_speed_label = 0
    
    gdhd_fwd_sol = 0
    gdhd_rev_sol = 0
    gdhd_ground_speed = 0
    gdhd_gear_speed = 0
    
    gdhd_max_pump_displacement = 175
    gdhd_max_motor_displacement = 215
    gdhd_gear_state = 1



    # clfn
    clfn_enable = 1
    clfn_enable_var = tk.StringVar()
    clfn_curr = 0
    clfn_pwm = 0
    clfn_pwm_var = tk.StringVar()
    clfn_rpm = 0
    clfn_RPM_label = 0

    # rssp
    rssp_enable = 1
    rssp_enable_var = tk.StringVar()
    rssp_right_pwm = 0
    rssp_right_pwm_var = tk.StringVar()
    rssp_left_pwm = 0
    rssp_left_pwm_var = tk.StringVar()

    crop_load_right_rssp = 0
    crop_load_right_rssp_var = tk.StringVar()
    crop_load_left_rssp = 0
    crop_load_left_rssp_var = tk.StringVar()

    rssp_right_spd = 0
    rssp_right_curr = 0
    rssp_left_spd = 0
    rssp_left_curr = 0

    rssp_right_spd_label = 0
    rssp_right_curr_label = 0
    rssp_left_spd_label = 0
    rssp_left_curr_label = 0

    # hdhr
    hdhr_enable = 1
    hdhr_enable_var = tk.StringVar()
    hdhr_type = 3
    hdhr_type_var = tk.StringVar()

    hdhr_ext1_volt = 1
    hdhr_ext2_volt = 1
    hdhr_type_volt = 2500

    hdhr_ext1_volt_label = 0
    hdhr_ext2_volt_label = 0
    hdhr_type_volt_label = 0

    NO_HEAD = 0
    CORN = 1
    GRAIN = 2
    DRAPER_VARIFEED = 3
    PICKUP = 4
    OTHER = 5
    FOLDING_CORN = 6
    SPARE7 = 7
    DRAPER_WITH_FA = 8
    SPARE9 = 9
    SPARE10 = 10
    SPARE11 = 11
    SPARE12 = 12
    VARIFEED = 13
    SPARE14 = 14
    SPARE15 = 15
    SPARE16 = 16
    SPARE17 = 17
    DRAPER_WITHOUT_FA = 18
    SPARE19 = 19
    SPARE20 = 20

    #Following code up until hdfn is added from new code
        # hdhc
    hdhc_lift_prs_enable_var = tk.StringVar()
    hdhc_frd_ang_enable_var = tk.StringVar()
    hdhc_gnd_height_enable_var = tk.StringVar()
    hdhc_lat_float_enable_var = tk.StringVar()
    hdhc_skid_plate_range_var = tk.StringVar()
    hdhc_lift_pressure_enabled = 1
    hdhc_frd_ang_enabled = 1
    hdhc_gnd_height_enabled = 1
    hdhc_lat_float_enabled = 1

    hdhc_skid_plate_range_label = 0
    hdhc_skid_plate_range = 400

    hdhc_feeder_angle_volt = 2175
    hdhc_lift_prs_volt = 0
    hdhc_lateral_float_cw = 0
    hdhc_lateral_float_ccw = 0
    hdhc_flow_cmd_extend = 0
    hdhc_flow_cmd_retract = 0
    hdhc_flow_pct = 0
    hdhc_header_platform_type = 1
    hdhc_lh_height_tilt_volt = 0
    hdhc_center_rh_height_volt = 0
    hdhc_center_lh_height_volt = 0
    hdhc_rh_height_tilt_volt = 0
    hdhc_lateral_position_volt = 0
    ################# JUST FOR TESTING AND COMPARE ##################

    hdhc_lift_prs_volt_pot = 0
    hdhc_feeder_angle_volt_pot = 0
    hdhc_lh_height_tilt_volt_pot = 0
    hdhc_center_lh_height_volt_pot = 0
    hdhc_center_rh_height_volt_pot = 0
    hdhc_rh_height_tilt_volt_pot = 0
    hdhc_lateral_position_volt_pot = 0

    hdhc_lift_prs_volt_pot_label = 0
    hdhc_feeder_angle_volt_pot_label = 0
    hdhc_lh_height_tilt_volt_pot_label = 0
    hdhc_center_lh_height_volt_pot_label = 0
    hdhc_center_rh_height_volt_pot_label = 0
    hdhc_rh_height_tilt_volt_pot_label = 0
    hdhc_lateral_position_volt_pot_label = 0
    #################################################################
    
    # fffa
    fffa_enable_var = tk.StringVar()
    fffa_block_enable_var = tk.StringVar()
    fffa_min_position_var = tk.StringVar()
    fffa_max_position_var = tk.StringVar()
    fffa_travel_rate_var = tk.StringVar()
    fffa_enabled = 1
    fffa_block_enabled = 1
    fffa_min_position_label = 0
    fffa_max_position_label = 0
    fffa_sol_fore_label = 0
    fffa_sol_aft_label = 0    
    fffa_min_position = 500
    fffa_max_position = 4400
    fffa_travel_rate = 1
    fffa_sol_fore = 0
    fffa_sol_aft = 0
    fffa_position_volt = 500
    
    fffa_position_pot_label = 0
    fffa_position_pot = 0
    
    # gdst
    gdst_enable_var = tk.StringVar()
    gdst_left_track_var = tk.StringVar()
    gdst_right_track_var = tk.StringVar()
    gdst_left_front_var = tk.StringVar()
    gdst_left_rear_var = tk.StringVar()
    gdst_right_front_var = tk.StringVar()
    gdst_right_rear_var = tk.StringVar()
    gdst_enabled = 1
    gdst_left_track_label = 0
    gdst_right_track_label = 0
    gdst_left_front_label = 0
    gdst_left_rear_label = 0
    gdst_right_front_label = 0
    gdst_right_rear_label = 0
    gdst_leftTensionInput = 70
    gdst_rightTensionInput = 70
    gdst_leftFrontInput = 50
    gdst_leftRearInput = 50
    gdst_rightFrontInput = 50
    gdst_rightRearInput = 50

    gdst_TracksDischarge = 0
    gdst_LeftShutOff = 0
    gdst_RightShutOff = 0
    gdst_RightRearUp = 0
    gdst_RightRearDown = 0
    gdst_RightFrontUp = 0
    gdst_RightFrontDown = 0
    gdst_LeftRearUp = 0
    gdst_LeftRearDown = 0
    gdst_LeftFrontUp = 0
    gdst_LeftFrontDown = 0
    ################# JUST FOR TESTING AND COMPARE ##################
    LeftTensionPressure_pot = 0
    RightTensionPressure_pot = 0
    LeftFrontDisp_pot = 0
    LeftRearDisp_pot = 0
    RightFrontDisp_pot = 0
    RightRearDisp_pot = 0
    #################################################################
    

    # hdfn
    hdfn_hor_enable = 1
    hdfn_ver_enable = 1
    hdfn_hor_install = 1
    hdfn_ver_install = 1
    hdfn_vari_enable = 1
    hdfn_vari_install = 1

    hdfn_sol_reel_up = 0
    hdfn_sol_reel_down = 0
    hdfn_sol_reel_fore = 0
    hdfn_sol_reel_aft = 0

    hdfn_swap_1 = 0
    hdfn_swap_2 = 0
    hdfn_swap_3 = 0

    hdfn_hor_enable_var = tk.StringVar()
    hdfn_ver_enable_var = tk.StringVar()
    hdfn_hor_install_var = tk.StringVar()
    hdfn_ver_install_var = tk.StringVar()
    hdfn_vari_enable_var = tk.StringVar()
    hdfn_vari_install_var = tk.StringVar()

    hdfn_sol_reel_up_var = tk.StringVar()
    hdfn_sol_reel_down_var = tk.StringVar()
    hdfn_sol_reel_fore_var = tk.StringVar()
    hdfn_sol_reel_aft_var = tk.StringVar()

    hdfn_swap_1_var = tk.StringVar()
    hdfn_swap_2_var = tk.StringVar()
    hdfn_swap_3_var = tk.StringVar()

    hdfn_hor_pos = 2500
    hdfn_ver_pos = 2500
    hdfn_vari_pos = 2500

    hdfn_hor_pos_label = 0
    hdfn_ver_pos_label = 0
    hdfn_vari_pos_label = 0

    hdfn_max_voltage = 4400
    hdfn_min_voltage = 500
    hdfn_min_voltage_vari = 1420

    hdfn_reel_enable = 1
    hdfn_ffa_enable = 1
    hdfn_reel_sol = 0
    hdfn_ffa_sol_fore = 0
    hdfn_ffa_sol_aft = 0
    hdfn_reel_pulse = 120
    hdfn_ffa_install = 1
    hdfn_reel_curr = 0

    hdfn_reel_enable_var = tk.StringVar()
    hdfn_ffa_enable_var = tk.StringVar()
    hdfn_reel_sol_var = tk.StringVar()
    hdfn_ffa_sol_fore_var = tk.StringVar()
    hdfn_ffa_sol_aft_var = tk.StringVar()
    hdfn_reel_pulse_var = tk.StringVar()
    hdfn_ffa_install_var = tk.StringVar()

    hdfn_reel_spd = 2500
    hdfn_reel_spd_tmp = 0
    hdfn_ffa_spd = 2500

    hdfn_reel_spd_label = 0
    hdfn_ffa_spd_label = 0

    hdfn_ffa_max_volt = 4400
    hdfn_ffa_min_volt = 500

    # agge
    agge_enable = 1
    agge_steer_wheel_enable = 1
    agge_sol_right = 0
    agge_sol_left = 0
    agge_calib_token = 0
    agge_calib_id = 0
    agge_cid = 0

    agge_enable_var = tk.StringVar()
    agge_steer_wheel_enable_var = tk.StringVar()
    agge_sol_right_var = tk.StringVar()
    agge_sol_left_var = tk.StringVar()
    agge_calib_token_var = tk.StringVar()
    agge_calib_id_var = tk.StringVar()
    agge_cid_var = tk.StringVar()

    agge_wheel = 3500
    agge_angle = 2500
    agge_pulse = 0

    agge_wheel_button = 0
    agge_angle_label = 0

    #from new code:
    agge_steer_right = 0
    agge_steer_left = 0
    agge_steering_wheel_override = 0
    agge_steering_state = 0
    agge_right_steer_sol_label = 0
    agge_left_steer_sol_label = 0


    NONE = 0
    COARSE_RIGHT = 1
    COARSE_LEFT = 2
    FINE_RIGHT = 3
    FINE_LEFT = 4
    TEST_RIGHT = 5
    TEST_LEFT = 6
    DONE = 7

    STEER_CALIB = 0x101B
    WHEEL_CALIB = 0X101C

    CALIB_NONE = 0X00
    CALIB_COARSE_RIGHT = 0X0A
    CALIB_COARSE_LEFT = 0X0F
    CALIB_FINE_RIGHT = 0X14
    CALIB_FINE_LEFT = 0X19
    CALIB_TEST_RIGHT = 0X1E
    CALIB_TEST_LEFT = 0X22
    CALIB_DONE = 0XDC

    STEER_VALVE_STEP = 0

    #rrts
    rrts_enable_var = tk.StringVar()
    rrts_rocktrap_open_sw = 0
    rrts_rocktrap_close_sw = 0
    rrts_rocktrap_open = 0
    rrts_rocktrap_close = 0
    rrts_rocktrap_open_sol_label = 0
    rrts_rocktrap_close_sol_label = 0
    rrts_door_closed_state = 0

    # settings
    KeyIsON = 1
    Key_Button = 0
    fei_compatible = 0

    Battery_KeyIsON = 1
    Battery_Key_Button = 0

    Key_and_Battery_State = 0

    #CC console states
    thresher_engage_state = 0
    feeder_engage_state =0


    # This variable will control the ui Simulator mode or not.
    # IF simmode=0,gray out all widgets,if simmode=1
    # SimMode=0
    file = open("SimMode.txt", "r")
    SimMode = file.read()
    SimMode = int(SimMode)
    file.close()

    # rotor
    rotor_gear_0 = 0.26
    rotor_gear_1 = 0.42
    rotor_gear_2 = 0.60
    rotor_gear_box = 1
    rotor_gear_box_var = tk.StringVar()

    # feed roll
    feed_roll = 0
    feed_roll_var = tk.StringVar()

    # CAN
    can_bus = can.interface.Bus(channel='can0', bustype='socketcan')
    msg = can.Message(data=[0, 0, 0, 0, 0, 0, 0, 0], is_extended_id=True)
    id_prefix = 0x18DA
    id_suffix = 0xF9


    if testing_active == 0:
        import can
        import os
        from collections import deque

        os.system("sudo /sbin/ip link set can0 up type can bitrate 500000")

        try:
            canbus1 = can.interface.Bus(
                channel='slcan0', bustype='socketcan', bitrate=500000)
        except OSError:
            print('Cannot find PiCAN board.')
            exit()
        msg_buffer = deque(maxlen=10)
