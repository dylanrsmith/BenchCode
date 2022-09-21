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
from PlantModels.UCM3_PlantModels.gdpb import *
from PlantModels.UCM1_PlantModels.hdhc import *
from PlantModels.UCM1_PlantModels.fffa import *
from PlantModels.UCM1_PlantModels.rrts import *
from PlantModels.UCM4_PlantModels.gdst import *
from PlantModels.UCM3_PlantModels.gdhd import *
from IOCtrl import *
from ReadThread import *

start = time.time()
gd_obj = global_defines()


# testing_active is set to 1...

if gd_obj.testing_active == 0:
    # start IO control
    io = IOCtrl(gd_obj)
    from startup_init import *

    st = start_init(gd_obj, io)
    st.init_key()
    st.init_freq()
    st.init_spn()
else:
    io = IOCtrl(gd_obj)
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
thcc = thcc_plant(gd_obj, io)
gdpb = gdpb_plant(gd_obj, io)
gdhd = gdhd_plant(gd_obj, io)
clfn = clfn_plant(gd_obj, io)
rssp = rssp_plant(gd_obj, io)
hdhr = hdhr_plant(gd_obj, io)
hdfn = hdfn_plant(gd_obj, io)
agge = agge_plant(gd_obj, io)
hdhc = hdhc_plant(gd_obj, io)
fffa = fffa_plant(gd_obj, io)
rrts = rrts_plant(gd_obj, io)
gdst = gdst_plant(gd_obj, io)
rotor_obj = rotor_hydro(gd_obj, io)
feeder_obj = Feeder_hydro(gd_obj, io)

# parse_excel.py
pe.parse_excel()
gd_obj.add_compatible()
cn.start_thread()
cn.ping()

# generate_ui.py
if gd_obj.fei_compatible == 1:
    gu.generate_actuator_ui()
    gu.generate_open_ui()

gu.generate_spn_ui()
gu.generate_driveline_ui()
gu.generate_clrm_ui()
gu.generate_ghcv_ui()
gu.generate_ui_rsch()
gu.generate_ui_ghts()
gu.generate_ui_rsck()
gu.generate_ui_ghps()
gu.generate_ui_thcc()
gu.generate_ui_gdpb()
gu.generate_ui_gdhd()
gu.generate_clfn_ui()
gu.generate_ui_rssp()
gu.generate_ui_hdhr()
gu.generate_ui_hdhc()
gu.generate_ui_fffa()
gu.generate_ui_hdfn()
gu.generate_ui_agge()
gu.generate_ui_rrts()
gu.generate_ui_gdst()
gu.generate_setting_ui()
gu.generate_cc_console_ui()
gu.get_sim_mode()


# update_ui.py
def ui_update_thread():
    if gd_obj.testing_active == 0:
        ui.update_ui_spn()
        ui.update_ui_dict()
        ui.update_ui_driveline()
        ui.update_ui_clrm()
        ui.update_ui_ghcv()
        ui.update_ui_rsch()
        ui.update_ui_ghts()
        # ui.update_ui_rsck()
        ui.update_ui_ghps()
        ui.update_ui_thcc()
        ui.update_ui_gdpb()
        ui.update_ui_gdhd()
        ui.update_ui_clfn()
        ui.update_ui_rssp()
        ui.update_ui_hdhr()
        ui.update_ui_hdfn()
        ui.update_ui_agge()
        ui.update_ui_rrts()
        ui.update_ui_hdhc()
        ui.update_ui_fffa()
        ui.update_ui_gdst()
        ui.update_settings()
        ui.update_cc_console()
        ui.update_cpu()
        ui.update_ui_offline()

        th1 = threading.Timer(0.01, ui_update_thread)
        th1.setDaemon(True)
        th1.start()  # 1 Second Read Thread
    else:
        ui.update_ui_spn()
        ui.update_ui_dict()
        ui.update_ui_driveline()
        ui.update_ui_clrm()
        ui.update_ui_ghcv()
        ui.update_ui_rsch()
        ui.update_ui_ghts()
        # ui.update_ui_rsck()
        ui.update_ui_ghps()
        ui.update_ui_thcc()
        ui.update_ui_gdpb()
        ui.update_ui_gdhd()
        ui.update_ui_clfn()
        ui.update_ui_rssp()
        ui.update_ui_hdhr()
        ui.update_ui_hdfn()
        ui.update_ui_agge()
        ui.update_ui_rrts()
        ui.update_ui_hdhc()
        ui.update_ui_fffa()
        ui.update_ui_gdst()
        ui.update_settings()
        ui.update_cc_console()
        ui.update_cpu()
        ui.update_ui_offline()

        th1 = threading.Timer(1, ui_update_thread)
        th1.setDaemon(True)
        th1.start()


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
        gdpb.calculate()
        gdhd.calculate()
        clfn.calculate_RPM()
        rssp.calculate_rpm()
        hdhr.calculate_hdr_volt()
        hdfn.calculate_hdr_pos()
        agge.calculate()
        rrts.calculate()
        hdhc.calculate()
        fffa.calculate()
        gdst.calculate()
        rotor_obj.calculate_rotor()
        feeder_obj.calculate_Feeder()
        # 1 second read thread
        th2 = threading.Timer(0.01, plant_model_update_thread)
        th2.setDaemon(True)
        th2.start()
    else:
        dv.calculate_speeds(gd_obj.current_spd)
        cl.calculate_speed()
        gh.calculate_state()
        rs.calculate()
        gt.calculate()
        rsck.calculate()
        ghps.calculate()
        thcc.calculate()
        gdpb.calculate()
        gdhd.calculate()
        clfn.calculate_RPM()
        rssp.calculate_rpm()
        hdhr.calculate_hdr_volt()
        hdfn.calculate_hdr_pos()
        agge.calculate()
        rrts.calculate()
        hdhc.calculate()
        fffa.calculate()
        gdst.calculate()
        # 2 second read thread
        th2 = threading.Timer(0.01, plant_model_update_thread)
        th2.setDaemon(True)
        th2.start()


if gd_obj.testing_active == 0:
    # Start Socket
    sc.accept_socket()
    # start read thread
    read_ob = ReadThread(io)
    read_ob.read()

ui_update_thread()
plant_model_update_thread()
ui.mainloop()


end = time.time()
boot_time = end - start
print("Boot Time = %s seconds" % boot_time)
