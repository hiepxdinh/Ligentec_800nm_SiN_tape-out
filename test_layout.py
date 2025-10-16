import sys

from setuptools.command.rotate import rotate

sys.path.append("C:/pdk/Ligentec_SiN_2025/ipkiss")

# import asp_sin_lnoi_photonics.technology
# import asp_sin_lnoi_photonics.all as asp


import ligentec_an800.all as pdk

import ipkiss3.all as i3
import numpy as np

import math

from chip_frame import CSL_FRAME_10500_4850, CHS_FRAME_10500_4850_HALF, CHS_FRAME_10500_HALF_4850_HALF
#
# from ring_gc.cell import RingModulatorGC
# from ring_modulator.cell import AddDropRingWithElectrode
# from waveguide_loop.cell import WaveguideLoop
from Aux_ring import HeaterNotchRacetrack, Aux_all_pass_ring, Aux_add_drop_ring
from All_pass_ring_taper import All_pass_ring_Exspot, All_pass_ring_Exspot_200GHz, All_pass_ring_Exspot_100GHz
from Add_drop_ring_taper import Add_drop_ring_Exspot_100GHz, Add_drop_ring_Exspot_200GHz
from Aux_ring_taper import Aux_add_drop_ring_taper
from waveguide_taper import Waveguide_Exspot
from bragg_grating_exspot import FP_BG_1_Exspot, FP_BG_2_Exspot, FP_BG_3_Exspot, FP_BG_4_Exspot, FP_BG_5_Exspot, FP_BG_6_Exspot, FP_BG_7_Exspot, FP_BG_8_Exspot, FP_BG_9_Exspot, FP_BG_10_Exspot
from exspot_test import Exspot_Spiral_Square, Exspot_Spiral_Circular
#
# #######################################
# # Global parameters
# ######################################
# waveguide_spacing = 50 # spacing between adjacent waveguides
# bend_radius = 200  # Bending radius used in waveguide routing
# hot_electrode_width = 20
# fibre_array_pich = 127
ebl_writing_size = (1000, 1000)

chip_elements = list()

######################################
# 1. Grid
######################################
# # #
grid_1 = CSL_FRAME_10500_4850()
grid_1_lo = grid_1.Layout(ebl_writing_size=ebl_writing_size)
chip_elements.append(i3.SRef(reference=grid_1, position=(0.0, 0.0)))

grid_2 = CHS_FRAME_10500_4850_HALF()
grid_2_lo = grid_2.Layout(ebl_writing_size=ebl_writing_size)
chip_elements.append(i3.SRef(reference=grid_2, position=(5.0, 5.0)))

grid_3 = CHS_FRAME_10500_HALF_4850_HALF()
grid_3_lo = grid_3.Layout(ebl_writing_size=ebl_writing_size)
chip_elements.append(i3.SRef(reference=grid_3, position=(5.0, 4850/2 + 125/2)))

grid_4 = CHS_FRAME_10500_HALF_4850_HALF()
grid_4_lo = grid_4.Layout(ebl_writing_size=ebl_writing_size)
chip_elements.append(i3.SRef(reference=grid_4, position=(10500/2 + 125/2, 4850/2 + 125/2)))


#Global parameters:

def ring_radius_from_fsr(fsr_ghz: float, n_eff: float) -> float:
    c = 3e8  # speed of light in m/s
    fsr_hz = fsr_ghz * 1e9  # convert GHz to Hz
    R = c / (2 * math.pi * n_eff * fsr_hz)
    return R*1e6
##################################
### Section for all-pass ring
##################################
# # Radius: 50GHz
# radius_50ghz = ring_radius_from_fsr(fsr_ghz=50, n_eff=2.0)
# print(radius_50ghz)
#
# radius = radius_50ghz
# h_separation = 500.0
# v_separation = 35.0
# coupler_gap = [1.0, 1.0, 1.0, 1.0, 1.0]
# offset = 125
# gap_list = [2.05]
# for i, gap in enumerate(coupler_gap):
#     ring = All_pass_ring_Exspot(ring_position_x=0, ring_position_y=0, output_offset=0)
#     ring_lv = ring.Layout(ring_radius=radius)
#     # ring_lv.visualize(annotate=True)
#     chip_elements.append(i3.SRef(reference=ring, position=(4095 + 200*i, 3615), transformation=i3.Rotation(rotation=90)))
#


# # Radius: 100GHz
# radius_100ghz = ring_radius_from_fsr(fsr_ghz=100, n_eff=2.0)
# print(radius_100ghz)
#
# radius = radius_100ghz
# h_separation = 300.0
# h_separation_2 = 300.0
# v_separation = 127/3
# offset = 325
# out_taper_position = 150
# gap_list = [1.0, 1.0]
# # for i, gap in enumerate(gap_list):
# #     name = "All_Pass_Ring_{}".format(radius)
# ring = All_pass_ring_Exspot_100GHz(ring_position_x=1*h_separation_2-400, ring_position_y=(2)*v_separation, output_offset=offset, out_taper_position = out_taper_position)
# ring_lv = ring.Layout(ring_radius=radius_100ghz)
# # ring_lv.visualize(annotate=True)
# chip_elements.append(i3.SRef(reference=ring, position=(6595-5500+400-40+1000-500, 1500+1600+500+275-50), transformation=i3.Rotation(rotation=90)))
#
# ring = All_pass_ring_Exspot_100GHz(ring_position_x=-1*h_separation_2-300, ring_position_y=(1)*v_separation, output_offset=offset, out_taper_position = out_taper_position)
# ring_lv = ring.Layout(ring_radius=radius_100ghz)
# # ring_lv.visualize(annotate=True)
# chip_elements.append(i3.SRef(reference=ring, position=(6595-5500+400-40+1000-500, 1500+1600+500+275-50), transformation=i3.Rotation(rotation=90)))
#
# ring = All_pass_ring_Exspot_100GHz(ring_position_x=1*h_separation_2-400, ring_position_y=(2)*v_separation, output_offset=offset, out_taper_position = out_taper_position)
# ring_lv = ring.Layout(ring_radius=radius_100ghz)
# # ring_lv.visualize(annotate=True)
# chip_elements.append(i3.SRef(reference=ring, position=(6595-5500+400-40+1000-500+575, 1500+1600+500+275-50), transformation=i3.Rotation(rotation=90)))
#
# ring = All_pass_ring_Exspot_100GHz(ring_position_x=-1*h_separation_2-300, ring_position_y=(1)*v_separation, output_offset=offset, out_taper_position = out_taper_position)
# ring_lv = ring.Layout(ring_radius=radius_100ghz)
# # ring_lv.visualize(annotate=True)
# chip_elements.append(i3.SRef(reference=ring, position=(6595-5500+400-40+1000-500+575, 1500+1600+500+275-50), transformation=i3.Rotation(rotation=90)))
#
#
# # Radius: 200GHz
# radius_200ghz = ring_radius_from_fsr(fsr_ghz=200, n_eff=2.0)
# print(radius_200ghz)
# radius=radius_200ghz
#
# h_separation = 300.0
# v_separation = 127/3
# offset = 75
# out_taper_position = 150
# gap_list = [1.0, 1.0, 1.0]
# for i, gap in enumerate(gap_list):
#     name = "All_Pass_Ring_{}".format(radius)
#     ring = All_pass_ring_Exspot_200GHz(ring_position_x=-i*h_separation, ring_position_y=(1-i)*v_separation, output_offset=offset, out_taper_position = out_taper_position)
#     ring_lv = ring.Layout(ring_radius=radius)
#     # ring_lv.visualize(annotate=True)
#     chip_elements.append(i3.SRef(reference=ring, position=(6595-5500, 1500+1600+500+275-50), transformation=i3.Rotation(rotation=90)))
#
# gap_list = [1.0, 1.0]
# for i, gap in enumerate(gap_list):
#     name = "All_Pass_Ring_{}".format(radius)
#     ring = All_pass_ring_Exspot_200GHz(ring_position_x=-i*h_separation, ring_position_y=(1-i)*v_separation, output_offset=offset, out_taper_position = out_taper_position)
#     ring_lv = ring.Layout(ring_radius=radius)
#     # ring_lv.visualize(annotate=True)
#     chip_elements.append(i3.SRef(reference=ring, position=(6595-5500+400-40, 1500+1600+500+275-50), transformation=i3.Rotation(rotation=90)))

# ##################################
# ### Section for add-drop ring
# ##################################
#
# # Radius: 200GHz
# radius_200ghz = ring_radius_from_fsr(fsr_ghz=200, n_eff=2.0)
# print(radius_200ghz)
#
# radius = radius_200ghz
# h_separation = 500.0
# v_separation = 35.0
# coupler_gap = [1.0, 1.0]
# offset = 125
# gap_list = [2.05]
#
# ring = Add_drop_ring_Exspot_200GHz(ring_position_x=0, ring_position_y=0, output_offset=0)
# ring_lv = ring.Layout(ring_radius=radius)
# # ring_lv.visualize(annotate=True)
# chip_elements.append(i3.SRef(reference=ring, position=(7895 + 200*1-2500, 3615+155), transformation=i3.Rotation(rotation=90)))
#
# ring = Add_drop_ring_Exspot_200GHz(ring_position_x=0, ring_position_y=0, output_offset=0)
# ring_lv = ring.Layout(ring_radius=radius)
# # ring_lv.visualize(annotate=True)
# chip_elements.append(i3.SRef(reference=ring, position=(7895 + 200*1-2500, 3615-52.5), transformation=i3.Rotation(rotation=90)+i3.VMirror()))
#
# ring = Add_drop_ring_Exspot_200GHz(ring_position_x=0, ring_position_y=0, output_offset=0)
# ring_lv = ring.Layout(ring_radius=radius)
# # ring_lv.visualize(annotate=True)
# chip_elements.append(i3.SRef(reference=ring, position=(7895 + 200*1-2500+500, 3615+155), transformation=i3.Rotation(rotation=90)))
#
# ring = Add_drop_ring_Exspot_200GHz(ring_position_x=0, ring_position_y=0, output_offset=0)
# ring_lv = ring.Layout(ring_radius=radius)
# # ring_lv.visualize(annotate=True)
# chip_elements.append(i3.SRef(reference=ring, position=(7895 + 200*1-2500+500, 3615-52.5), transformation=i3.Rotation(rotation=90)+i3.VMirror()))
#
# # Radius: 200GHz
# radius_100ghz = ring_radius_from_fsr(fsr_ghz=100, n_eff=2.0)
# print(radius_100ghz)
#
# radius = radius_100ghz
# h_separation = 500.0
# v_separation = 35.0
# coupler_gap = [1.0, 1.0]
# offset = 125
# gap_list = [2.05]
#
# ring = Add_drop_ring_Exspot_100GHz(ring_position_x=0, ring_position_y=0, output_offset=0)
# ring_lv = ring.Layout(ring_radius=radius)
# # ring_lv.visualize(annotate=True)
# chip_elements.append(i3.SRef(reference=ring, position=(7895 + 200*1-2500+1000, 3615+155-200), transformation=i3.Rotation(rotation=90)))

##################################
### Section for aux ring
##################################
# name = "All_Pass_Ring"
aux_ring = Aux_add_drop_ring_taper()
aux_ring_lv = aux_ring.Layout(main_radius=300, aux_radius=50)
chip_elements.append(i3.SRef(reference=aux_ring, position=(9000, 3500), transformation=i3.Rotation(rotation=-90)))

# ##################################
# ### Section Waveguide test -
# ##################################
# waveguide_width = [1.8, 1.8, 1.9, 1.9, 2.0, 2.0, 2.1, 2.1, 2.2, 2.2]
# separation =  127/3
# for i, width in enumerate(waveguide_width):
#     waveguide_test = Waveguide_Exspot()
#     waveguide_test_lv = waveguide_test.Layout(width_out=width)
#     chip_elements.append(i3.SRef(reference=waveguide_test, position=(-3000+3625, 1800-252.3 + i*separation)))

##################################
### Section ExSpot
##################################

# spiral_length = [3500, 4000, 4500, 5000]
#
# for idx, length in enumerate(spiral_length):
#     exspot_pkg = Exspot_Spiral_Square()
#     exspot_pkg_lv = exspot_pkg.Layout(spiral_length=length)
#     # exspot_pkg_lv.visualize()
#     chip_elements.append(i3.SRef(reference=exspot_pkg, position=(500 + idx*300, 2500+730+221.25), transformation=i3.Rotation(rotation=90)))

##################################
### Section P1
##################################

# heater_test = pdk.MZIVertical()
#
# heater_test_lv = heater_test.Layout()
# chip_elements.append(i3.SRef(reference=heater_test, position=(-3000, 3100)))

# ##################################
# ### Section Bragg grating
# ##################################
# coupler_gap = [0.4, 0.5, 0.6, 0.7, 0.8]
#
# ### Long chip
# device_length_long = 10500
#
# # BG_2: 4 devices
# fp_width_2=1.0
# fp_length_2=7070
#
# for i, gap in enumerate(coupler_gap):
#     bg_2_1 = FP_BG_2_Exspot(device_length=device_length_long)
#     bg_2_1_lv = bg_2_1.Layout(fp_width=fp_width_2, fp_length=fp_length_2, coupler_gap=gap)
#     # bg_2_lv.visualize(annotate=True)
#     chip_elements.append(i3.SRef(reference=bg_2_1_lv, position=(-3000+4725, 45+ (127/3 + 0.1)*(i+1))))
#
# # BG_3: 4 devices
# fp_width_3=1.0
# fp_length_3=6470
#
# for i, gap in enumerate(coupler_gap):
#     bg_3_1 = FP_BG_3_Exspot(device_length=device_length_long)
#     bg_3_1_lv = bg_3_1.Layout(fp_width=fp_width_3, fp_length=fp_length_3, coupler_gap=gap)
#     chip_elements.append(i3.SRef(reference=bg_3_1_lv, position=(-3000+5025, 45+ -0.5+(127/3 + 0.1)*(i+1+len(coupler_gap)))))
#
# # BG_5: 4 devices
# fp_width_5=0.8
# fp_length_5=2500
#
# for i, gap in enumerate(coupler_gap):
#     bg_5_1 = FP_BG_5_Exspot(device_length=device_length_long)
#     bg_5_1_lv = bg_5_1.Layout(fp_width=fp_width_5, fp_length=fp_length_5, coupler_gap=gap)
#     chip_elements.append(i3.SRef(reference=bg_5_1_lv, position=(-3000+7010, 45+ -0.5-0.7+(127/3 + 0.1)*(i+1+2*len(coupler_gap)))))
#
# # BG_6: 4 devices
# fp_width_6=1.0
# fp_length_6=3681
#
# for i, gap in enumerate(coupler_gap):
#     bg_6_1 = FP_BG_6_Exspot(device_length=device_length_long)
#     bg_6_1_lv = bg_6_1.Layout(fp_width=fp_width_6, fp_length=fp_length_6, coupler_gap=gap)
#     chip_elements.append(i3.SRef(reference=bg_6_1_lv, position=(-3000+7010-590, 45+ -0.5-0.7-0.3+(127/3 + 0.1)*(i+1+3*len(coupler_gap)))))
#
# # BG_8: 4 devices
# fp_width_8=1.0
# fp_length_8=2700
#
# for i, gap in enumerate(coupler_gap):
#     bg_8_1 = FP_BG_8_Exspot(device_length=device_length_long)
#     bg_8_1_lv = bg_8_1.Layout(fp_width=fp_width_8, fp_length=fp_length_8, coupler_gap=gap)
#     chip_elements.append(i3.SRef(reference=bg_8_1_lv, position=(-3000+7010-100, 45+ -0.5-0.7-0.3-0.5+(127/3 + 0.1)*(i+1+4*len(coupler_gap)))))
# #
# # BG9: 4 devices
# fp_width_9=1.2
# fp_length_9=5000
#
# for i, gap in enumerate(coupler_gap):
#     bg_10_1 = FP_BG_10_Exspot(device_length=device_length_long)
#     bg_10_1_lv = bg_10_1.Layout(fp_width=fp_width_9, fp_length=fp_length_9, coupler_gap=gap)
#     chip_elements.append(i3.SRef(reference=bg_10_1_lv, position=(-3000+7010-1250, 45+ -0.5-0.7-0.3-0.5-0.3+(127/3 + 0.1)*(i+1+5*len(coupler_gap)))))
#
# # BG10: 4 devices
# fp_width_10=1.2
# fp_length_10=5000
#
# for i, gap in enumerate(coupler_gap):
#     bg_10_1 = FP_BG_10_Exspot(device_length=device_length_long)
#     bg_10_1_lv = bg_10_1.Layout(fp_width=fp_width_10, fp_length=fp_length_10, coupler_gap=gap)
#     chip_elements.append(i3.SRef(reference=bg_10_1_lv, position=(-3000+7010-1250, 45+ -0.5-0.7-0.3-0.5-0.3-0.5+(127/3 + 0.1)*(i+1+6*len(coupler_gap)))))

### Short chip
device_length_short = 2350

# # BG_1: 4 devices
# fp_width_1=0.8
# fp_length_1=1486
# for i, gap in enumerate(coupler_gap):
#     bg_1_1 = FP_BG_1_Exspot(device_length=device_length_short)
#     bg_1_1_lv = bg_1_1.Layout(fp_width=fp_width_1, fp_length=fp_length_1, coupler_gap=gap)
#     chip_elements.append(i3.SRef(reference=bg_1_1_lv, position=((127/3)*(i+1), 3100-255+77), transformation=i3.Rotation(rotation=90)))
#
# # BG_4: 4 devices
# fp_width_4=0.8
# fp_length_4=1712.19
#
# for i, gap in enumerate(coupler_gap):
#     bg_4_1 = FP_BG_4_Exspot(device_length=device_length_short)
#     bg_4_1_lv = bg_4_1.Layout(fp_width=fp_width_4, fp_length=fp_length_4, coupler_gap=gap)
#     chip_elements.append(i3.SRef(reference=bg_4_1_lv, position=((127/3)*(i+1+1*len(coupler_gap)), 3100-255+77-113), transformation=i3.Rotation(rotation=90)))
#
# # BG_7: 4 devices
# fp_width_7=1.0
# fp_length_7=1440
#
# for i, gap in enumerate(coupler_gap):
#     bg_7_1 = FP_BG_7_Exspot(device_length=device_length_short)
#     bg_7_1_lv = bg_7_1.Layout(fp_width=fp_width_7, fp_length=fp_length_7, coupler_gap=gap)
#     chip_elements.append(i3.SRef(reference=bg_7_1_lv, position=(-0.2+(127/3)*(i+1+2*len(coupler_gap)), 3100-255+77+23), transformation=i3.Rotation(rotation=90)))

####################################
### Generate the main layout
####################################
chip_design = i3.LayoutCell(name = "Top")

chip_layout = chip_design.Layout(elements=chip_elements)

chip_layout.write_gdsii("gds_output/ligentec.gds")
