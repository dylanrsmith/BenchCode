import time
from global_defines import *

gd_obj = global_defines()

from socket1 import *
from UserInterface.parse_excel import *
from UserInterface.generate_ui import *
from UserInterface.update_ui import *
from PlantModels.Driveline import *
from PlantModels.UCM1_PlantModels.clrm_plant import *
from PlantModels.UCM1_PlantModels.hdhr import *
from PlantModels.UCM1_PlantModels.hdfn import *
from PlantModels.UCM1_PlantModels.agge import *
from PlantModels.UCM2_PlantModels.clfn import *
from PlantModels.UCM2_PlantModels.ghcv import *
from PlantModels.UCM2_PlantModels.rsch import *
from PlantModels.UCM3_PlantModels.ghts import *
from PlantModels.UCM3_PlantModels.rsck import *
from PlantModels.UCM3_PlantModels.ghps import *
from PlantModels.UCM3_PlantModels.thcc import *
from PlantModels.UCM3_PlantModels.rssp import *
from PlantModels.UCM2_PlantModels.rotor import *
from PlantModels.UCM1_PlantModels.feeder import *


if gd_obj.testing_active == 0:
    from IOCtrl import *
    from ReadThread import *

if gd_obj.testing_active == 0:
    #start IO control
    io = IOCtrl(gd_obj)
    #initialize all freq to 200
    from startup_init import *
    st = start_init(gd_obj, io)
    st.init_key()
    st.init_freq()
    st.init_spn()
else:
    io = 0
    st = 0

pe = parse_excel(gd_obj)
#st.init_volt()
sc = socket_py(io)  
gu = generate_ui(gd_obj, io)
ui = update_ui(gd_obj, io)
cn = CAN_FEI()
dv = driveline(gd_obj, io)
cl = clrm_plant(gd_obj, io)
gh = ghcv_plant(gd_obj, io)
rs = rsch_plant(gd_obj, io)
gt = ghts_plant(gd_obj, io)
rsck = rsck_plant(gd_obj, io)
ghps = ghps_plant(gd_obj)
thcc = thcc_plant(gd_obj)
clfn = clfn_plant(gd_obj, io)
rssp = rssp_plant(gd_obj, io)
hdhr = hdhr_plant(gd_obj, io)
hdfn = hdfn_plant(gd_obj, io)
agge = agge_plant(gd_obj, io)
rotor_obj = rotor_hydro(gd_obj, io)
feeder_obj = Feeder_hydro(gd_obj, io)

pe.parse_excel()
gu.generate_spn_ui()
gu.generate_open_ui()
gu.generate_driveline_ui()
gu.generate_clrm_ui()
gu.generate_ghcv_ui()
gu.generate_ui_rsch()
gu.generate_ui_ghts()
gu.generate_ui_rsck()
gu.generate_ui_ghps()
gu.generate_ui_thcc()
gu.generate_clfn_ui()
gu.generate_ui_rssp()
gu.generate_ui_hdhr()
gu.generate_ui_hdfn()
gu.generate_ui_agge()
gu.generate_setting_ui()

def ui_update_thread():
    if gd_obj.testing_active == 0:
        ui.update_ui_dict()
        ui.update_ui_driveline()
        ui.update_ui_clrm()
        ui.update_ui_ghcv()
        ui.update_ui_rsch()
        ui.update_ui_ghts()
        ui.update_ui_rsck()
        ui.update_ui_ghps()
        ui.update_ui_thcc()
        ui.update_ui_clfn()
        ui.update_ui_rssp()
        ui.update_ui_hdhr()
        ui.update_ui_hdfn()
        ui.update_ui_agge()
        ui.update_settings()
        ui.update_cpu()
        threading.Timer(1, ui_update_thread).start()  # 1 second read thread
    else:
        ui.update_ui_dict()
        ui.update_ui_driveline()
        ui.update_ui_clrm()
        ui.update_ui_ghcv()
        ui.update_ui_rsch()
        ui.update_ui_ghts()
        ui.update_ui_rsck()
        ui.update_ui_ghps()
        ui.update_ui_thcc()
        ui.update_ui_clfn()
        ui.update_ui_rssp()
        ui.update_ui_hdhr()
        ui.update_ui_hdfn()
        ui.update_ui_agge()
        ui.update_settings()
        ui.update_cpu()
        threading.Timer(1, ui_update_thread).start()  # 2 second read thread
ui_update_thread()

def plant_model_update_thread():
    if gd_obj.testing_active == 0:
        #start_time = time.time()  # Ifdef
        dv.calculate_speeds(gd_obj.current_spd)
        #drivline_time = time.time() # Ifdef
        cl.calculate_speed()
        #clrm_time = time.time() # Ifdef
        gh.calculate_state()
        #ghcv_time = time.time() # Ifdef
        #rs.calculate()
        rs.rsch_temp()
        #rsch_time = time.time() # Ifddef
        gt.calculate()
        #ghts_time = time.time() #Ifdef
        rsck.calculate()
        #rsck_time = time.time() #Ifdef
        ghps.calculate()
        #ghps_time = time.time() # Ifdef
        thcc.calculate()
        #thcc_time = time.time() # Ifdef
        clfn.calculate_RPM()
        #clfn_time = time.time() # Ifdef
        rssp.calculate_rpm()
        #rssp_time = time.time() # Ifdef
        hdhr.calculate_hdr_volt()
        #hdhr_time = time.time() # Ifdef
        hdfn.calculate_hdr_pos()
        #hdfn_time = time.time() # Ifdef
        agge.agge_plant_cal()
        #agge_time = time.time() # Ifdef
        rotor_obj.calculate_rotor()
        #rotor_time = time.time() # Ifdef
        feeder_obj.calculate_Feeder()
        #feeder_time = time.time() # Ifdef

#        print("\n")
#         print("Drive Line : ",drivline_time -start_time)
#         print("CLRM Time : ", clrm_time-drivline_time)
#         print("GHCV Time : ", ghcv_time-clrm_time)
#         print("RSCH Time : ", rsch_time-ghcv_time)
#         print("GHTS Time : ", ghts_time-rsch_time)
#         print("RSCK Time : ", rsck_time -ghts_time)
#         print("GHPS Time :", ghps_time-rsck_time)
#         print("THCC Time :", thcc_time-ghps_time)
#         print("CLFN Time :", clfn_time-thcc_time)
#         print("RSSP Time :", rssp_time-clfn_time)
#         print("HDHR Time :", hdhr_time-rssp_time)
#         print("HDFN Time :", hdfn_time-hdhr_time)
#         print("AGGE Time :", agge_time-hdfn_time)
#        print("Rotor Time :", rotor_time-agge_time)
#         print("Feeder Time :", feeder_time-rotor_time)
#         print("\n")
        
        threading.Timer(0.0001, plant_model_update_thread).start()  # 1 second read thread
    else:
        dv.calculate_speeds(gd_obj.current_spd)
        cl.calculate_speed()
        gh.calculate_state()
        rs.calculate()
        gt.calculate()
        rsck.calculate()
        ghps.calculate()
        thcc.calculate()
        clfn.calculate_RPM()
        rssp.calculate_rpm()
        hdhr.calculate_hdr_volt()
        hdfn.calculate_hdr_pos()
        agge.agge_plant_cal()
        threading.Timer(0.0001, plant_model_update_thread).start()  # 2 second read thread

if gd_obj.testing_active == 0:
    plant_model_update_thread()

#CAN
if gd_obj.testing_active == 0:
    from HwConnect.CAN_interface import *
    canbus1 = CANbus(gd_obj.canbus1, gd_obj.msg_buffer, gd_obj)
    canbus1.RecvCAN()


if gd_obj.testing_active == 0:
    # Start Socket
    sc.accept_socket()
    #start read thread
    read_ob = ReadThread(io)
    read_ob.read()

ui.mainloop()