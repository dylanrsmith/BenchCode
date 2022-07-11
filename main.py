import time
from global_defines import *
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

start = time.time()
gd_obj = global_defines()

#testing_active is set to 1...

if gd_obj.testing_active == 0:
    from IOCtrl import *
    from ReadThread import *

if gd_obj.testing_active == 0:
    #start IO control
    io = IOCtrl(gd_obj)
    from startup_init import *
    st = start_init(gd_obj, io)
    st.init_key()
    st.init_freq()
    st.init_spn()
else:
    io = 0
    st = 0

pe = parse_excel(gd_obj)
sc = socket_py(io)  
gu = generate_ui(gd_obj, io)
ui = update_ui(gd_obj, io)
cn = CAN_FEI(gd_obj)
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

#parse_excel.py
pe.parse_excel()
gd_obj.add_compatible()

#generate_ui.py
if gd_obj.fei_compatible==1:
    gu.generate_actuator_ui()
    gu.generate_open_ui()

gu.generate_spn_ui()
# gu.generate_open_ui()
# gu.generate_actuator_ui()
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

#update_ui.py 
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
        ui.update_ui_open()
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
        ui.update_ui_open()
        threading.Timer(1, ui_update_thread).start()

def ping_thread():
    cn.ping()
    threading.Timer(1,ping_thread).start()

def listen_thread():
    cn.receive_CAN()
    threading.Timer(1,listen_thread).start()

ui_update_thread()
#Begin Polling threads | May cause 'Main Thread is not in Main loop' Error
#Non essential to main functionality
# ping_thread()
# listen_thread()

def plant_model_update_thread():
    if gd_obj.testing_active == 0:
        dv.calculate_speeds(gd_obj.current_spd)
        cl.calculate_speed()
        gh.calculate_state()
        rs.rsch_temp()
        gt.calculate()
        rsck.calculate()
        ghps.calculate()
        thcc.calculate()
        clfn.calculate_RPM()
        rssp.calculate_rpm()
        hdhr.calculate_hdr_volt()
        hdfn.calculate_hdr_pos()
        agge.agge_plant_cal()
        rotor_obj.calculate_rotor()
        feeder_obj.calculate_Feeder()
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

if gd_obj.testing_active == 0:
    # Start Socket
    sc.accept_socket()
    #start read thread
    read_ob = ReadThread(io)
    read_ob.read()

gd_obj = global_defines()

end = time.time()

boot_time = end-start
print("Time = %s seconds" % boot_time) 
ui.mainloop()