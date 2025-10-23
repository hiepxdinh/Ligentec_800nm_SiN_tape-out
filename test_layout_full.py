import sys

from matplotlib.pyplot import annotate
from setuptools.command.rotate import rotate

sys.path.append("C:/pdk/Ligentec_SiN_2025/ipkiss")

# import asp_sin_lnoi_photonics.technology
# import asp_sin_lnoi_photonics.all as asp


import ligentec_an800.all as pdk

import ipkiss3.all as i3
import numpy as np

import math

from chip_frame import CSL_FRAME_10520_4870, CHS_FRAME_10520_4870_HALF, CHS_FRAME_10520_HALF_4870_HALF
#
# from ring_gc.cell import RingModulatorGC
# from ring_modulator.cell import AddDropRingWithElectrode
# from waveguide_loop.cell import WaveguideLoop
from Aux_ring import HeaterNotchRacetrack, Aux_add_drop_ring_1_2, Aux_add_drop_ring_3
from All_pass_ring_taper import All_pass_ring_Exspot, All_pass_ring_Exspot_200GHz, All_pass_ring_Exspot_100GHz, All_pass_ring_Exspot_50GHz, All_pass_ring_Exspot_Aux, All_pass_ring_Exspot_Test
from Add_drop_ring_taper import Add_drop_ring_Exspot_200GHz
from Aux_ring_taper import Aux_add_drop_ring_taper_1_2, Aux_add_drop_ring_taper_3
from waveguide_taper import Waveguide_Exspot, Waveguide_Exspot_2, Waveguide_Exspot_Ref
from bragg_grating_exspot import FP_BG_1_Exspot, FP_BG_2_Exspot, FP_BG_3_Exspot, FP_BG_4_Exspot, FP_BG_5_Exspot, FP_BG_6_Exspot, FP_BG_7_Exspot, FP_BG_8_Exspot, FP_BG_9_Exspot, Sinusoidal_BG_Exspot
from Bragg_grating_test import BG_Test_1, BG_Test_2, BG_Test_3, BG_Test_4, BG_Test_5, BG_Test_6, BG_Test_7, BG_Test_8, BG_Test_Sinusoidal
from exspot_test import Exspot_Spiral_Square, Exspot_Spiral_Circular_GC, Exspot_Spiral_Square_2

from Bragg_grating_test_lensed_fiber_bb import BG_Test_1_lense, BG_Test_2_lense
from Bragg_grating_test_lensed_fiber_bb import BG_Test_3_lense, BG_Test_4_lense
from Bragg_grating_test_lensed_fiber_bb import BG_Test_5_lense, BG_Test_6_lense, BG_Test_7_lense, BG_Test_8_lense, BG_Test_9_lense, BG_Test_Sin_lense
from grating_coupler_test import All_pass_ring_GC, All_pass_ring_GC_2, All_pass_ring_GC_3, All_pass_ring_GC_4
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
grid_1 = CSL_FRAME_10520_4870()
grid_1_lo = grid_1.Layout(ebl_writing_size=ebl_writing_size)
chip_elements.append(i3.SRef(reference=grid_1, position=(0.0, 0.0)))

grid_2 = CHS_FRAME_10520_4870_HALF()
grid_2_lo = grid_2.Layout(ebl_writing_size=ebl_writing_size)
chip_elements.append(i3.SRef(reference=grid_2, position=(10.0, 10.0)))

grid_3 = CHS_FRAME_10520_4870_HALF()
grid_3_lo = grid_3.Layout(ebl_writing_size=ebl_writing_size)
chip_elements.append(i3.SRef(reference=grid_3, position=(10.0, 4870/2 + 120/2)))

# grid_4 = CHS_FRAME_10500_HALF_4850_HALF()
# grid_4_lo = grid_4.Layout(ebl_writing_size=ebl_writing_size)
# chip_elements.append(i3.SRef(reference=grid_4, position=(10500/2 + 125/2, 4850/2 + 125/2)))


#Global parameters:

def ring_radius_from_fsr(fsr_ghz: float, n_eff: float) -> float:
    c = 3e8  # speed of light in m/s
    fsr_hz = fsr_ghz * 1e9  # convert GHz to Hz
    R = c / (2 * math.pi * n_eff * fsr_hz)
    return R*1e6

##################################
### Section for all-pass ring
##################################
# Radius: 50GHz
radius_50ghz = ring_radius_from_fsr(fsr_ghz=50, n_eff=2.1)
print(radius_50ghz)

radius = radius_50ghz
h_separation = 500.0
v_separation = 35.0
coupler_gap = [1.0, 1.0, 1.0, 1.0, 1.0]
offset = 125
gap_50ghz = [0.4, 0.5, 0.6]
ap_50ghz_ring_1 = All_pass_ring_Exspot_50GHz(ring_position_x=175, ring_position_y=0, output_offset=0)
ap_50ghz_ring_1_lv = ap_50ghz_ring_1.Layout(ring_radius=radius_50ghz, ring_width=1.8, ring_gap=gap_50ghz[0])
# ring_lv.visualize(annotate=True)
chip_elements.append(i3.SRef(reference=ap_50ghz_ring_1_lv, position=(2015, 3807.5+10), transformation=i3.Rotation(rotation=90)))

ap_50ghz_ring_2 = All_pass_ring_Exspot_50GHz(ring_position_x=175, ring_position_y=0, output_offset=0)
ap_50ghz_ring_2_lv = ap_50ghz_ring_2.Layout(ring_radius=radius_50ghz, ring_width=1.8, ring_gap=gap_50ghz[1])
# ring_lv.visualize(annotate=True)
chip_elements.append(i3.SRef(reference=ap_50ghz_ring_2_lv, position=(3031, 3807.5+10), transformation=i3.Rotation(rotation=90)))

ap_50ghz_ring_3 = All_pass_ring_Exspot_50GHz(ring_position_x=175, ring_position_y=0, output_offset=0)
ap_50ghz_ring_3_lv = ap_50ghz_ring_3.Layout(ring_radius=radius_50ghz, ring_width=1.8, ring_gap=gap_50ghz[2])
# ring_lv.visualize(annotate=True)
chip_elements.append(i3.SRef(reference=ap_50ghz_ring_3_lv, position=(4047, 3807.5+10), transformation=i3.Rotation(rotation=90)))

#
# Radius: 100GHz
radius_100ghz = ring_radius_from_fsr(fsr_ghz=100, n_eff=2.1)
print(radius_100ghz)

radius = radius_100ghz
h_separation = 300.0
h_separation_2 = 300.0
v_separation = 127/3
offset = 325-27-5
out_taper_position = 150
gap_100ghz = [0.4, 0.5, 0.6, 0.7]
# for i, gap in enumerate(gap_list):
#     name = "All_Pass_Ring_{}".format(radius)
ap_100ghz_ring_1 = All_pass_ring_Exspot_100GHz(ring_position_x=1*h_separation_2-400+50-7.5, ring_position_y=(2)*v_separation, output_offset=offset, out_taper_position = out_taper_position)
ap_100ghz_ring_1_lv = ap_100ghz_ring_1.Layout(ring_radius=radius_100ghz, ring_width=1.8, ring_gap=gap_100ghz[0])
# ring_lv.visualize(annotate=True)
chip_elements.append(i3.SRef(reference=ap_100ghz_ring_1_lv, position=(905, 3807.5+10), transformation=i3.Rotation(rotation=90)))

ap_100ghz_ring_2 = All_pass_ring_Exspot_100GHz(ring_position_x=-1*h_separation_2-300+50-7.5, ring_position_y=(1)*v_separation, output_offset=offset, out_taper_position = out_taper_position)
ap_100ghz_ring_2_lv = ap_100ghz_ring_2.Layout(ring_radius=radius_100ghz, ring_width=1.8, ring_gap=gap_100ghz[1])
chip_elements.append(i3.SRef(reference=ap_100ghz_ring_2_lv, position=(905, 3807.5+10), transformation=i3.Rotation(rotation=90)))
#
ap_100ghz_ring_3 = All_pass_ring_Exspot_100GHz(ring_position_x=1*h_separation_2-400+50-7.5, ring_position_y=(2)*v_separation, output_offset=offset, out_taper_position = out_taper_position)
ap_100ghz_ring_3_lv = ap_100ghz_ring_3.Layout(ring_radius=radius_100ghz, ring_width=1.8, ring_gap=gap_100ghz[2])
chip_elements.append(i3.SRef(reference=ap_100ghz_ring_3_lv, position=(1440-27, 3807.5+10), transformation=i3.Rotation(rotation=90)))
#
ap_100ghz_ring_4 = All_pass_ring_Exspot_100GHz(ring_position_x=-1*h_separation_2-300+50-7.5, ring_position_y=(1)*v_separation, output_offset=offset, out_taper_position = out_taper_position)
ap_100ghz_ring_4_lv = ap_100ghz_ring_4.Layout(ring_radius=radius_100ghz, ring_width=1.8, ring_gap=gap_100ghz[3])
chip_elements.append(i3.SRef(reference=ap_100ghz_ring_4_lv, position=(1440-27, 3807.5+10), transformation=i3.Rotation(rotation=90)))

# Radius: 200GHz
radius_200ghz = ring_radius_from_fsr(fsr_ghz=200, n_eff=2.1)
print(radius_200ghz)
radius=radius_200ghz

h_separation = 300.0
v_separation = 127/3
offset = 75
out_taper_position = 150
gap_list_200ghz_1 = [0.3, 0.4, 0.5]
for i, gap_200ghz in enumerate(gap_list_200ghz_1):
    # name = "All_Pass_Ring_{}".format(radius)
    ap_200ghz_ring = All_pass_ring_Exspot_200GHz(ring_position_x=-i*h_separation+25-7.5, ring_position_y=(1-i)*v_separation, output_offset=offset, out_taper_position = out_taper_position)
    ap_200ghz_ring_lv = ap_200ghz_ring.Layout(ring_radius=radius, ring_width=1.8, ring_gap=gap_200ghz)
    # ring_lv.visualize(annotate=True)
    chip_elements.append(i3.SRef(reference=ap_200ghz_ring_lv, position=(125, 3832.5+10), transformation=i3.Rotation(rotation=90)))

### Reference waveguide

waveguide_test_ref_2 = Waveguide_Exspot_Ref()
waveguide_test_ref_2_lv = waveguide_test_ref_2.Layout()
chip_elements.append(i3.SRef(reference=waveguide_test_ref_2_lv, position=(1944.666+28, 3107.5+10), transformation=i3.Rotation(rotation=90)))
#

waveguide_test_ref_3 = Waveguide_Exspot_Ref()
waveguide_test_ref_3_lv = waveguide_test_ref_3.Layout()
chip_elements.append(i3.SRef(reference=waveguide_test_ref_3_lv, position=(2992.666-4, 3107.5+10), transformation=i3.Rotation(rotation=90)))
#
waveguide_test_ref_4 = Waveguide_Exspot_Ref()
waveguide_test_ref_4_lv = waveguide_test_ref_4.Layout()
chip_elements.append(i3.SRef(reference=waveguide_test_ref_4_lv, position=(4012.666-8, 3107.5+10), transformation=i3.Rotation(rotation=90)))

waveguide_test_ref_5 = Waveguide_Exspot_Ref()
waveguide_test_ref_5_lv = waveguide_test_ref_5.Layout()
chip_elements.append(i3.SRef(reference=waveguide_test_ref_5_lv, position=(8762.166, 3107.5+10), transformation=i3.Rotation(rotation=90)))


gap_list_200ghz_2 = [0.6, 0.7, 0.8]
for i, gap_200ghz in enumerate(gap_list_200ghz_2):
    # name = "All_Pass_Ring_{}".format(radius)
    ap_200ghz_ring = All_pass_ring_Exspot_200GHz(ring_position_x=-i*h_separation-7.5, ring_position_y=(1-i)*v_separation, output_offset=offset, out_taper_position = out_taper_position)
    ap_200ghz_ring_lv = ap_200ghz_ring.Layout(ring_radius=radius, ring_width=1.8, ring_gap=gap_200ghz)
    # ring_lv.visualize(annotate=True)
    chip_elements.append(i3.SRef(reference=ap_200ghz_ring_lv, position=(506, 3832.5+10), transformation=i3.Rotation(rotation=90)))


### Ring Test
gap = [0.3, 0.4, 0.5, 0.6, 0.7]

radius_200ghz = ring_radius_from_fsr(fsr_ghz=200, n_eff=2.1)
print(radius_200ghz)
radius=radius_200ghz

ap_test_ring_1 = All_pass_ring_Exspot_Test()
ap_test_ring_1_lv = ap_test_ring_1.Layout(ring_radius=radius, ring_width=1.7, ring_gap=gap[0])
# ring_lv.visualize(annotate=True)
chip_elements.append(i3.SRef(reference=ap_test_ring_1_lv, position=(4995+100, 3290+10)))

ap_test_ring_2 = All_pass_ring_Exspot_Test()
ap_test_ring_2_lv = ap_test_ring_2.Layout(ring_radius=radius, ring_width=1.7, ring_gap=gap[1])
# ring_lv.visualize(annotate=True)
chip_elements.append(i3.SRef(reference=ap_test_ring_2_lv, position=(5395+100-19, 3290+10)))

ap_test_ring_3 = All_pass_ring_Exspot_Test()
ap_test_ring_3_lv = ap_test_ring_3.Layout(ring_radius=radius, ring_width=1.7, ring_gap=gap[2])
# ring_lv.visualize(annotate=True)
chip_elements.append(i3.SRef(reference=ap_test_ring_3_lv, position=(5795+100-19-19, 3290+10)))

ap_test_ring_4 = All_pass_ring_Exspot_Test()
ap_test_ring_4_lv = ap_test_ring_4.Layout(ring_radius=radius, ring_width=1.7, ring_gap=gap[3])
# ring_lv.visualize(annotate=True)
chip_elements.append(i3.SRef(reference=ap_test_ring_4_lv, position=(6195+100-19-19-19, 3290+10)))

ap_test_ring_5 = All_pass_ring_Exspot_Test()
ap_test_ring_5_lv = ap_test_ring_5.Layout(ring_radius=radius, ring_width=1.9, ring_gap=gap[0])
# ring_lv.visualize(annotate=True)
chip_elements.append(i3.SRef(reference=ap_test_ring_5_lv, position=(6595+100-19-19-19-19, 3290+10)))

ap_test_ring_6 = All_pass_ring_Exspot_Test()
ap_test_ring_6_lv = ap_test_ring_6.Layout(ring_radius=radius, ring_width=1.9, ring_gap=gap[1])
# ring_lv.visualize(annotate=True)
chip_elements.append(i3.SRef(reference=ap_test_ring_6_lv, position=(6995+100-19-19-19-19-19, 3290+10)))

ap_test_ring_7 = All_pass_ring_Exspot_Test()
ap_test_ring_7_lv = ap_test_ring_7.Layout(ring_radius=radius, ring_width=1.9, ring_gap=gap[2])
# ring_lv.visualize(annotate=True)
chip_elements.append(i3.SRef(reference=ap_test_ring_7_lv, position=(7395+100-19-19-19-19-19-19, 3290+10)))

#################################
## Section for add-drop ring
#################################

# Radius: 200GHz
radius_200ghz = ring_radius_from_fsr(fsr_ghz=200, n_eff=2.1)
print(radius_200ghz)

radius = radius_200ghz
h_separation = 500.0
v_separation = 35.0
coupler_gap = [1.0, 1.0]
offset = 125
gap_list = [0.3, 0.4, 0.5, 0.6]
#
ad_ring_1 = Add_drop_ring_Exspot_200GHz(ring_position_x=0, ring_position_y=0, gap_offset=0)
ad_ring_1_lv = ad_ring_1.Layout(ring_radius=radius, ring_width=1.8, ring_gap=gap_list[0])
# ring_lv.visualize(annotate=True)
chip_elements.append(i3.SRef(reference=ad_ring_1_lv, position=(2395-51.282, 3615+155-307.5-17.5+10), transformation=i3.Rotation(rotation=90)+i3.VMirror()))

ad_ring_3 = Add_drop_ring_Exspot_200GHz(ring_position_x=0, ring_position_y=0, gap_offset=0.1)
ad_ring_3_lv = ad_ring_3.Layout(ring_radius=radius, ring_width=1.8, ring_gap=gap_list[1])
# ring_lv.visualize(annotate=True)
chip_elements.append(i3.SRef(reference=ad_ring_3_lv, position=(3445-52.882-32.5, 3615+155-307.5-17.5+10), transformation=i3.Rotation(rotation=90)+i3.VMirror()))

ad_ring_2 = Add_drop_ring_Exspot_200GHz(ring_position_x=0, ring_position_y=0, gap_offset=0.2)
ad_ring_2_lv = ad_ring_2.Layout(ring_radius=radius, ring_width=1.8, ring_gap=gap_list[2])
# ring_lv.visualize(annotate=True)
chip_elements.append(i3.SRef(reference=ad_ring_2_lv, position=(4345+30.158+00.36, 3615-52.5-100-17.5+10), transformation=i3.Rotation(rotation=90)+i3.VMirror()))

#
##################################
### Section for aux ring
##################################

main_gap_1 = 0.3
aux_gap_1 = 0.67
ring_gap_1 = 0.42

aux_ring_1 = Aux_add_drop_ring_taper_1_2(main_gap0=main_gap_1, main_gap1=main_gap_1, aux_gap0=aux_gap_1, ring_gap=ring_gap_1-0.3)
aux_ring_1_lv = aux_ring_1.Layout(main_radius=227.82, aux_radius=60)
chip_elements.append(i3.SRef(reference=aux_ring_1_lv, position=(5475, 3500+125-100+10+20), transformation=i3.Rotation(rotation=-90)+i3.VMirror()))

aux_ring_2 = Aux_add_drop_ring_taper_1_2(main_gap0=main_gap_1, main_gap1=main_gap_1, aux_gap0=aux_gap_1, ring_gap=ring_gap_1-0.3)
aux_ring_2_lv = aux_ring_2.Layout(main_radius=227.82, aux_radius=60)
chip_elements.append(i3.SRef(reference=aux_ring_2_lv, position=(6415, 3500+125-100+10+20), transformation=i3.Rotation(rotation=-90)+i3.VMirror()))

main_gap_2 = 0.35
aux_gap_2 = 0.7
ring_gap_2 = 0.45

aux_ring_3 = Aux_add_drop_ring_taper_3(main_gap0=main_gap_2, main_gap1=main_gap_2, aux_gap0=aux_gap_2, ring_gap=ring_gap_2-0.3)
aux_ring_3_lv = aux_ring_3.Layout(main_radius=227.82, aux_radius=60)
chip_elements.append(i3.SRef(reference=aux_ring_3_lv, position=(7355, 3500+125-100+10+20), transformation=i3.Rotation(rotation=-90)+i3.VMirror()))

### Main ring test

radius = 227.82
h_separation = 300.0
h_separation_2 = 300.0
v_separation = 127/3
offset = 325-30
out_taper_position = 150
gap_list = [0.3, 0.4]
# for i, gap in enumerate(gap_list):
#     name = "All_Pass_Ring_{}".format(radius)
main_ring_test_1 = All_pass_ring_Exspot_100GHz(ring_position_x=1*h_separation_2-400+50-7.5, ring_position_y=(2)*v_separation, output_offset=offset, out_taper_position = out_taper_position)
main_ring_test_1_lv = main_ring_test_1.Layout(ring_radius=radius, ring_width=1.8, ring_gap=gap[0])
# ring_lv.visualize(annotate=True)
chip_elements.append(i3.SRef(reference=main_ring_test_1, position=(7905, 3807.5+10), transformation=i3.Rotation(rotation=90)))

main_ring_test_2 = All_pass_ring_Exspot_100GHz(ring_position_x=-1*h_separation_2-300+50-7.5, ring_position_y=(1)*v_separation, output_offset=offset, out_taper_position = out_taper_position)
main_ring_test_2_lv = main_ring_test_2.Layout(ring_radius=radius, ring_width=1.8, ring_gap=gap[1])
chip_elements.append(i3.SRef(reference=main_ring_test_2, position=(7905, 3807.5+10), transformation=i3.Rotation(rotation=90)))
#

### Aux ring test
radius = 60
h_separation = 205.0
v_separation = 127/3
offset = 75
out_taper_position = 150
aux_gap_list = [0.4, 0.5, 0.6, 0.7]
for i, gap in enumerate(aux_gap_list):
    # name = "All_Pass_Ring_{}".format(radius)
    aux_ring_test = All_pass_ring_Exspot_Aux(ring_position_x=-i*h_separation+17.5, ring_position_y=(1-i)*v_separation, output_offset=offset, out_taper_position = out_taper_position)
    aux_ring_test_lv = aux_ring_test.Layout(ring_radius=radius, ring_width=1.8, ring_gap=gap)
    # ring_lv.visualize(annotate=True)
    chip_elements.append(i3.SRef(reference=aux_ring_test, position=(8400, 3832.5+10), transformation=i3.Rotation(rotation=90)))

##################################
### Section Waveguide test -
##################################
waveguide_width = [0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0, 2.2, 2.4, 2.6]
separation =  127/3
for i, width in enumerate(waveguide_width):
    waveguide_test = Waveguide_Exspot()
    waveguide_test_lv = waveguide_test.Layout(width_out=width)
    chip_elements.append(i3.SRef(reference=waveguide_test, position=(615, 1800-252.3-900-78.6+127/3-32.5+650-49.266+127/3+9-0.4 + i*separation)))

waveguide_width = [0.8, 1.0, 1.2, 1.4, 1.4, 1.6, 1.6, 1.8, 1.8, 2.0, 2.0, 2.2, 2.2, 2.4, 2.6]
for i, width in enumerate(waveguide_width):
    waveguide_test = Waveguide_Exspot_2()
    waveguide_test_lv = waveguide_test.Layout(width_out=width)
    chip_elements.append(i3.SRef(reference=waveguide_test, position=(615, 2500-252.3-159.5-32.5-900+50-118.767+127/3+650-49.266+127/3-127+9-0.4 + i*separation)))

### Spiral Test
spiral_test_2um_1 = Exspot_Spiral_Square()
spiral_test_2um_1_lv = spiral_test_2um_1.Layout(spiral_length=25000, width_out=2.2, n_o_loops=6)
# spiral_test_lv.visualize(annotate=True)
chip_elements.append(i3.SRef(reference=spiral_test_2um_1_lv, position=(8835, 4308.014+20-5), transformation=i3.Rotation(rotation=-90)))

spiral_test_2um_2 = Exspot_Spiral_Square()
spiral_test_2um_2_lv = spiral_test_2um_2.Layout(spiral_length=9000, width_out=2.2, n_o_loops=3)
# spiral_test_lv.visualize(annotate=True)
chip_elements.append(i3.SRef(reference=spiral_test_2um_2_lv, position=(9200, 4308.014+20-5), transformation=i3.Rotation(rotation=-90)))

spiral_test_2um_3 = Exspot_Spiral_Square_2()
spiral_test_2um_3_lv = spiral_test_2um_3.Layout(spiral_length=9000, width_out=2.2, n_o_loops=2, bend_radius=100)
# spiral_test_lv.visualize(annotate=True)
chip_elements.append(i3.SRef(reference=spiral_test_2um_3_lv, position=(9510, 4269.041+20-5), transformation=i3.Rotation(rotation=-90)))

spiral_test_2um_4 = Exspot_Spiral_Square_2()
spiral_test_2um_4_lv = spiral_test_2um_4.Layout(spiral_length=9000, width_out=1.0, n_o_loops=2, bend_radius=100)
# spiral_test_lv.visualize(annotate=True)
chip_elements.append(i3.SRef(reference=spiral_test_2um_4_lv, position=(10002, 4269.041+20-5), transformation=i3.Rotation(rotation=-90)))

# #Circular spiral test
#
spiral_circular_test_2um_1 = Exspot_Spiral_Circular_GC()
spiral_circular_test_2um_1_lv = spiral_circular_test_2um_1.Layout(spiral_length=5000)
# spiral_test_lv.visualize(annotate=True)
chip_elements.append(i3.SRef(reference=spiral_circular_test_2um_1_lv, position=(10290, 4361.7644+0.236+8+20), transformation=i3.Rotation(rotation=-90)))

spiral_circular_test_2um_1_2 = Exspot_Spiral_Circular_GC()
spiral_circular_test_2um_1_2_lv = spiral_circular_test_2um_1_2.Layout(spiral_length=10000)
# spiral_test_lv.visualize(annotate=True)
chip_elements.append(i3.SRef(reference=spiral_circular_test_2um_1_2_lv, position=(10290, 2755+20), transformation=i3.Rotation(rotation=-90)))


spiral_circular_test_2um_2 = Exspot_Spiral_Circular_GC()
spiral_circular_test_2um_2_lv = spiral_circular_test_2um_2.Layout(spiral_length=7500)
# spiral_test_lv.visualize(annotate=True)
chip_elements.append(i3.SRef(reference=spiral_circular_test_2um_2_lv, position=(9812, 4361.764+0.236+8+20), transformation=i3.Rotation(rotation=-90)))

spiral_circular_test_2um_2_2 = Exspot_Spiral_Circular_GC()
spiral_circular_test_2um_2_2_lv = spiral_circular_test_2um_2_2.Layout(spiral_length=10000)
# spiral_test_lv.visualize(annotate=True)
chip_elements.append(i3.SRef(reference=spiral_circular_test_2um_2_2_lv, position=(9812, 2755+20), transformation=i3.Rotation(rotation=-90)))


spiral_circular_test_2um_3 = Exspot_Spiral_Circular_GC()
spiral_circular_test_2um_3_lv = spiral_circular_test_2um_3.Layout()
# spiral_test_lv.visualize(annotate=True)
chip_elements.append(i3.SRef(reference=spiral_circular_test_2um_3_lv, position=(8095, 4361.7644+0.236+8+20), transformation=i3.Rotation(rotation=-90)))


spiral_circular_test_2um_4 = Exspot_Spiral_Circular_GC()
spiral_circular_test_2um_4_lv = spiral_circular_test_2um_4.Layout(spiral_length=11000)
# spiral_test_lv.visualize(annotate=True)
chip_elements.append(i3.SRef(reference=spiral_circular_test_2um_4_lv, position=(1165-10, 2755+20), transformation=i3.Rotation(rotation=-90)))

spiral_circular_test_2um_5 = Exspot_Spiral_Circular_GC()
spiral_circular_test_2um_5_lv = spiral_circular_test_2um_5.Layout(spiral_length=25000)
# spiral_test_lv.visualize(annotate=True)
chip_elements.append(i3.SRef(reference=spiral_circular_test_2um_5_lv, position=(1760, 2755+20), transformation=i3.Rotation(rotation=-90)))


##################################
### Section Bragg grating
##################################
coupler_gap = 0.6

## Long chip
device_length_long = 10520

# BG_1: 4 devices
fp_width_1=0.8
fp_length_1=1486.0

bg_1_1 = FP_BG_1_Exspot(device_length=device_length_long)
bg_1_1_lv = bg_1_1.Layout(fp_width=fp_width_1, fp_length=fp_length_1, coupler_gap=coupler_gap)
chip_elements.append(i3.SRef(reference=bg_1_1_lv, position=(4507+10, 100+9)))

# BG_2: 4 devices
fp_width_2=1.0
fp_length_2=7070.0

bg_2_1 = FP_BG_2_Exspot(device_length=device_length_long)
bg_2_1_lv = bg_2_1.Layout(fp_width=fp_width_2, fp_length=fp_length_2, coupler_gap=coupler_gap)
# bg_2_lv.visualize(annotate=True)
chip_elements.append(i3.SRef(reference=bg_2_1_lv, position=(1715+10, 100+127/3+0.2+9)))

# BG_3: 4 devices
fp_width_3=1.0
fp_length_3=[6470.0, 6470.0-50.0, 6470.0+50.0]

bg_3_1 = FP_BG_3_Exspot(device_length=device_length_long)
bg_3_1_lv = bg_3_1.Layout(fp_width=fp_width_3, fp_length=fp_length_3[0], coupler_gap=coupler_gap)
chip_elements.append(i3.SRef(reference=bg_3_1_lv, position=(2015+10, 100+127*2/3+0.2+9)))

bg_3_2 = FP_BG_3_Exspot(device_length=device_length_long)
bg_3_2_lv = bg_3_2.Layout(fp_width=fp_width_3, fp_length=fp_length_3[1], coupler_gap=coupler_gap)
chip_elements.append(i3.SRef(reference=bg_3_2_lv, position=(2015+10+50/2, 100+127*3/3+0.2+9)))

bg_3_3 = FP_BG_3_Exspot(device_length=device_length_long)
bg_3_3_lv = bg_3_3.Layout(fp_width=fp_width_3, fp_length=fp_length_3[2], coupler_gap=coupler_gap)
chip_elements.append(i3.SRef(reference=bg_3_3_lv, position=(2015+10-50/2, 100+127*4/3+0.2+9)))

# BG_4: 4 devices
fp_width_4=0.8
fp_length_4=[1712.19, 1712.19-50.0, 1712.19+50.0]

bg_4_1 = FP_BG_4_Exspot(device_length=device_length_long)
bg_4_1_lv = bg_4_1.Layout(fp_width=fp_width_4, fp_length=fp_length_4[0], coupler_gap=coupler_gap)
chip_elements.append(i3.SRef(reference=bg_4_1_lv, position=(4393.905+10, 100+127*5/3+9)))

bg_4_2 = FP_BG_4_Exspot(device_length=device_length_long)
bg_4_2_lv = bg_4_2.Layout(fp_width=fp_width_4, fp_length=fp_length_4[1], coupler_gap=coupler_gap)
chip_elements.append(i3.SRef(reference=bg_4_2_lv, position=(4393.905+10+50/2, 100+127*6/3+9)))

bg_4_3 = FP_BG_4_Exspot(device_length=device_length_long)
bg_4_3_lv = bg_4_3.Layout(fp_width=fp_width_4, fp_length=fp_length_4[2], coupler_gap=coupler_gap)
chip_elements.append(i3.SRef(reference=bg_4_3_lv, position=(4393.905+10-50/2, 100+127*7/3+9)))

# BG_5: 4 devices
fp_width_5=0.8
fp_length_5=[2500.0, 2500.0-50.0, 2500.0+50.0]

bg_5_1 = FP_BG_5_Exspot(device_length=device_length_long)
bg_5_1_lv = bg_5_1.Layout(fp_width=fp_width_5, fp_length=fp_length_5[0], coupler_gap=coupler_gap)
chip_elements.append(i3.SRef(reference=bg_5_1_lv, position=(4000+10, 100+127*8/3+9)))

bg_5_2 = FP_BG_5_Exspot(device_length=device_length_long)
bg_5_2_lv = bg_5_2.Layout(fp_width=fp_width_5, fp_length=fp_length_5[1], coupler_gap=coupler_gap)
chip_elements.append(i3.SRef(reference=bg_5_2_lv, position=(4000+10+50/2, 100+127*9/3+9)))

bg_5_3 = FP_BG_5_Exspot(device_length=device_length_long)
bg_5_3_lv = bg_5_3.Layout(fp_width=fp_width_5, fp_length=fp_length_5[2], coupler_gap=coupler_gap)
chip_elements.append(i3.SRef(reference=bg_5_3_lv, position=(4000+10-50/2, 100+127*10/3+9)))
#
# BG_6: 4 devices
fp_width_6=1.0
fp_length_6=[3681.0, 3681.0-50.0, 3681.0+50.0]

bg_6_1 = FP_BG_6_Exspot(device_length=device_length_long)
bg_6_1_lv = bg_6_1.Layout(fp_width=fp_width_6, fp_length=fp_length_6[0], coupler_gap=coupler_gap)
chip_elements.append(i3.SRef(reference=bg_6_1_lv, position=(3409.5+10, 100+127*11/3+0.2+9)))

bg_6_2 = FP_BG_6_Exspot(device_length=device_length_long)
bg_6_2_lv = bg_6_2.Layout(fp_width=fp_width_6, fp_length=fp_length_6[1], coupler_gap=coupler_gap)
chip_elements.append(i3.SRef(reference=bg_6_2_lv, position=(3409.5+10+50/2, 100+127*12/3+0.2+9)))

bg_6_3 = FP_BG_6_Exspot(device_length=device_length_long)
bg_6_3_lv = bg_6_3.Layout(fp_width=fp_width_6, fp_length=fp_length_6[2], coupler_gap=coupler_gap)
chip_elements.append(i3.SRef(reference=bg_6_3_lv, position=(3409.5+10-50/2, 100+127*13/3+0.2+9)))
#
# BG_7: 4 devices
fp_width_7=1.0
fp_length_7=[1440.0, 1440.0-50.0, 1440.0+50.0]

bg_7_1 = FP_BG_7_Exspot(device_length=device_length_long)
bg_7_1_lv = bg_7_1.Layout(fp_width=fp_width_7, fp_length=fp_length_7[0], coupler_gap=coupler_gap)
chip_elements.append(i3.SRef(reference=bg_7_1_lv, position=(-3000+7530+10, 100+127*14/3+0.2+9)))

bg_7_2 = FP_BG_7_Exspot(device_length=device_length_long)
bg_7_2_lv = bg_7_2.Layout(fp_width=fp_width_7, fp_length=fp_length_7[1], coupler_gap=coupler_gap)
chip_elements.append(i3.SRef(reference=bg_7_2_lv, position=(-3000+7530+10+50/2, 100+127*15/3+0.2+9)))

bg_7_3 = FP_BG_7_Exspot(device_length=device_length_long)
bg_7_3_lv = bg_7_3.Layout(fp_width=fp_width_7, fp_length=fp_length_7[2], coupler_gap=coupler_gap)
chip_elements.append(i3.SRef(reference=bg_7_3_lv, position=(-3000+7530+10-50/2, 100+127*16/3+0.2+9)))

# BG_8: 4 devices
fp_width_8=1.0
fp_length_8=[2700.0, 2600.0, 2800.0]

bg_8_1 = FP_BG_8_Exspot(device_length=device_length_long)
bg_8_1_lv = bg_8_1.Layout(fp_width=fp_width_8, fp_length=fp_length_8[0], coupler_gap=coupler_gap)
chip_elements.append(i3.SRef(reference=bg_8_1_lv, position=(-3000+7010+10-100-10, 100+127*17/3+0.2+9)))

bg_8_2 = FP_BG_8_Exspot(device_length=device_length_long)
bg_8_2_lv = bg_8_2.Layout(fp_width=fp_width_8, fp_length=fp_length_8[1], coupler_gap=coupler_gap)
chip_elements.append(i3.SRef(reference=bg_8_2_lv, position=(-3000+7010+10-100+515-500+25, 100+127*18/3+0.2+9)))

bg_8_3 = FP_BG_8_Exspot(device_length=device_length_long)
bg_8_3_lv = bg_8_3.Layout(fp_width=fp_width_8, fp_length=fp_length_8[2], coupler_gap=coupler_gap)
chip_elements.append(i3.SRef(reference=bg_8_3_lv, position=(-3000+7010+10-100-35-25, 100+127*19/3+0.2+9)))
#
# BG_9: 4 devices
fp_width_9=[0.8, 1.0]
fp_length_9=5000.0

bg_9_1 = FP_BG_9_Exspot(device_length=device_length_long)
bg_9_1_lv = bg_9_1.Layout(fp_width=fp_width_9[0], fp_length=fp_length_9, coupler_gap=coupler_gap)
chip_elements.append(i3.SRef(reference=bg_9_1_lv, position=(-3000+7010+10-100-35-25-1100, 100+127*20/3+9)))

bg_9_2 = FP_BG_9_Exspot(device_length=device_length_long)
bg_9_2_lv = bg_9_2.Layout(fp_width=fp_width_9[0], fp_length=fp_length_9, coupler_gap=coupler_gap)
chip_elements.append(i3.SRef(reference=bg_9_2_lv, position=(-3000+7010+10-100-35-25-1100, 100+127*21/3+0+9)))

# BG_10: 4 devices
fp_width_10=1.2
fp_length_10=5000.0

bg_10_1 = FP_BG_4_Exspot(device_length=device_length_long)
bg_10_1_lv = bg_10_1.Layout(fp_width=fp_width_10, fp_length=fp_length_10, coupler_gap=coupler_gap)
chip_elements.append(i3.SRef(reference=bg_10_1_lv, position=(-3000+7010+10-100-35-25-1100, 100+127*22/3+0+0.4+9)))

bg_10_2 = FP_BG_4_Exspot(device_length=device_length_long)
bg_10_2_lv = bg_10_2.Layout(fp_width=fp_width_10, fp_length=fp_length_10, coupler_gap=coupler_gap)
chip_elements.append(i3.SRef(reference=bg_10_2_lv, position=(-3000+7010+10-100-35-25-1100, 100+127*23/3+0+0.4+9)))


# Sinusoidal BG

sinusoidal_bg_1 = Sinusoidal_BG_Exspot(device_length=device_length_long)
sinusoidal_bg_1_lv = sinusoidal_bg_1.Layout(fp_width=1.6, fp_length=3400, coupler_gap=coupler_gap)
chip_elements.append(i3.SRef(reference=sinusoidal_bg_1_lv, position=(-3000+10+7010-100-35-325, 100+127*24/3+0.8+0+9)))

sinusoidal_bg_2 = Sinusoidal_BG_Exspot(device_length=device_length_long)
sinusoidal_bg_2_lv = sinusoidal_bg_2.Layout(fp_width=1.6, fp_length=3350, coupler_gap=coupler_gap)
chip_elements.append(i3.SRef(reference=sinusoidal_bg_2_lv, position=(-3000+10+7010-100-35-325+25, 100+127*25/3+0.8+0+9)))

sinusoidal_bg_3 = Sinusoidal_BG_Exspot(device_length=device_length_long)
sinusoidal_bg_3_lv = sinusoidal_bg_3.Layout(fp_width=1.6, fp_length=3450, coupler_gap=coupler_gap)
chip_elements.append(i3.SRef(reference=sinusoidal_bg_3_lv, position=(-3000+10+7010-100-35-325-25, 100+127*26/3+0.8+0+9)))
#

# # #
##################################
### Section Bragg grating test lensed fiber
##################################
fp_length_test=50.0

# BG_Test_1: 4 devices
fp_width_1=0.8

#
bg_test_1 = BG_Test_1_lense()
bg_test_1_lv = bg_test_1.Layout(fp_width=fp_width_1, fp_length=fp_length_test)
chip_elements.append(i3.SRef(reference=bg_test_1_lv, position=(1800+50-1050-32-450 +25+ 1050+90-66.5-23-37.5, 3000+154+1186-50+20+10-40+20), transformation=i3.Rotation(rotation=90)))

# chip_elements.append(i3.SRef(reference=bg_test_1_lv, position=(1800+50-1050-32-450 +25+ 1050+90-66.5-37.5, 3000+154+1186-50+20+10-40), transformation=i3.Rotation(rotation=90)))


# BG_2: 4 devices
fp_width_2=1.0

bg_test_2 = BG_Test_2_lense()
bg_test_2_lv = bg_test_2.Layout(fp_width=fp_width_2, fp_length=fp_length_test)
chip_elements.append(i3.SRef(reference=bg_test_2_lv, position=(1800+50-1050-32-450 +25*2+ 1050+90-66.5-23-37.5, 3000+154+1186-50+20+10-40+20), transformation=i3.Rotation(rotation=90)))

chip_elements.append(i3.SRef(reference=bg_test_2_lv, position=(1800+50-1050-32-450 +25*3+ 1050+90-66.5-23-37.5, 3000+154+1186-50+20+10-40+20), transformation=i3.Rotation(rotation=90)))

#
# BG_3: 4 devices
fp_width_3=1.0

bg_test_3 = BG_Test_3_lense()
bg_test_3_lv = bg_test_3.Layout(fp_width=fp_width_3, fp_length=fp_length_test)
chip_elements.append(i3.SRef(reference=bg_test_3_lv, position=(1800+50-1050-32-450 +25*4+ 1050+90-66.5-23-37.5, 3000+154+1186-50+20+10-40+20), transformation=i3.Rotation(rotation=90)))

chip_elements.append(i3.SRef(reference=bg_test_3_lv, position=(1800+50-1050-32-450 +25*5+ 1050+90-66.5-23-37.5, 3000+154+1186-50+20+10-40+20), transformation=i3.Rotation(rotation=90)))

# BG_4: 4 devices
fp_width_4=0.8

bg_test_4 = BG_Test_4_lense()
bg_test_4_lv = bg_test_4.Layout(fp_width=fp_width_4, fp_length=fp_length_test)
chip_elements.append(i3.SRef(reference=bg_test_4_lv, position=(1800+50-1050-32-450 +25*6+ 1050+90-66.5-23-37.5, 3000+154+1186-50+20+10-40+20), transformation=i3.Rotation(rotation=90)))

chip_elements.append(i3.SRef(reference=bg_test_4_lv, position=(1800+50-1050-32-450 +25*7+ 1050+90-66.5-23-37.5, 3000+154+1186-50+20+10-40+20), transformation=i3.Rotation(rotation=90)))


# BG_5: 4 devices
fp_width_5=0.8

bg_test_5 = BG_Test_5_lense()
bg_test_5_lv = bg_test_5.Layout(fp_width=fp_width_5, fp_length=fp_length_test)
chip_elements.append(i3.SRef(reference=bg_test_5_lv, position=(1800+50-1050-32-450 +25*8+ 1050+90-66.5-23-37.5, 3000+154+1186-50+20+10-40+20), transformation=i3.Rotation(rotation=90)))

chip_elements.append(i3.SRef(reference=bg_test_5_lv, position=(1800+50-1050-32-450 +25*9+ 1050+90-66.5-23-37.5, 3000+154+1186-50+20+10-40+20), transformation=i3.Rotation(rotation=90)))


# BG_6: 4 devices
fp_width_6=1.0

bg_test_6 = BG_Test_6_lense()
bg_test_6_lv = bg_test_6.Layout(fp_width=fp_width_6, fp_length=fp_length_test)
chip_elements.append(i3.SRef(reference=bg_test_6_lv, position=(1800+50-1050-32-450 +25*10+ 1050+90-66.5-23-37.5, 3000+154+1186-50+20+10-40+20), transformation=i3.Rotation(rotation=90)))

chip_elements.append(i3.SRef(reference=bg_test_6_lv, position=(1800+50-1050-32-450 +25*11+ 1050+90-66.5-23-37.5, 3000+154+1186-50+20+10-40+20), transformation=i3.Rotation(rotation=90)))


# BG_7: 4 devices
fp_width_7=1.0

bg_test_7 = BG_Test_7_lense()
bg_test_7_lv = bg_test_7.Layout(fp_width=fp_width_7, fp_length=fp_length_test)
chip_elements.append(i3.SRef(reference=bg_test_7_lv, position=(1800+50-1050-32-450 +25*12+ 1050+90-66.5-23-37.5, 3000+154+1186-50+20+10-40+20), transformation=i3.Rotation(rotation=90)))

chip_elements.append(i3.SRef(reference=bg_test_7_lv, position=(1800+50-1050-32-450 +25*13 + 1050+90-66.5-23-37.5, 3000+154+1186-50+20+10-40+20), transformation=i3.Rotation(rotation=90)))


# BG_8: 4 devices
fp_width_8=1.0

bg_test_8 = BG_Test_8_lense()
bg_test_8_lv = bg_test_8.Layout(fp_width=fp_width_8, fp_length=fp_length_test)
chip_elements.append(i3.SRef(reference=bg_test_8_lv, position=(1800+50-1050-32-450 +25*14+ 1050+90-66.5-23-37.5, 3000+154+1186-50+20+10-40+20), transformation=i3.Rotation(rotation=90)))

chip_elements.append(i3.SRef(reference=bg_test_8_lv, position=(1800+50-1050-32-450 +25*15+ 1050+90-66.5-23-37.5, 3000+154+1186-50+20+10-40+20), transformation=i3.Rotation(rotation=90)))

# BG_8: 4 devices
fp_width_9=1.0

bg_test_9 = BG_Test_9_lense()
bg_test_9_lv = bg_test_9.Layout(fp_width=fp_width_9, fp_length=fp_length_test)
chip_elements.append(i3.SRef(reference=bg_test_9_lv, position=(1800+50-1050-32-450 +25*16+ 1050+90-66.5-23-37.5, 3000+154+1186-50+20+10-40+20), transformation=i3.Rotation(rotation=90)))

# chip_elements.append(i3.SRef(reference=bg_test_9_lv, position=(1800+50-1050-32-450 +25*17+ 1050+90-66.5-23-37.5, 3000+154+1186-50+20+10-40), transformation=i3.Rotation(rotation=90)))

#
##################################
### Section Bragg grating test
##################################
# BG_Test_1: 4 devices
fp_width_1=0.8
fp_length_test=300.0

bg_test_1 = BG_Test_1()
bg_test_1_lv = bg_test_1.Layout(fp_width=fp_width_1, fp_length=fp_length_test)
chip_elements.append(i3.SRef(reference=bg_test_1_lv, position=(1800+50-1050-32+100-37.5, 3000+154+1186-50+20), transformation=i3.Rotation(rotation=90)))

chip_elements.append(i3.SRef(reference=bg_test_1_lv, position=(1800+50-1050-32 +25+100-37.5, 3000+154+1186-50+20), transformation=i3.Rotation(rotation=90)))


# BG_2: 4 devices
fp_width_2=1.0

bg_test_2 = BG_Test_2()
bg_test_2_lv = bg_test_2.Layout(fp_width=fp_width_2, fp_length=fp_length_test)
chip_elements.append(i3.SRef(reference=bg_test_2_lv, position=(1800+50-1050-32 +25*2+100-37.5, 3000+154+1186-50+20), transformation=i3.Rotation(rotation=90)))

chip_elements.append(i3.SRef(reference=bg_test_2_lv, position=(1800+50-1050-32 +25*3+100-37.5, 3000+154+1186-50+20), transformation=i3.Rotation(rotation=90)))


# BG_3: 4 devices
fp_width_3=1.0

bg_test_3 = BG_Test_3()
bg_test_3_lv = bg_test_3.Layout(fp_width=fp_width_3, fp_length=fp_length_test)
chip_elements.append(i3.SRef(reference=bg_test_3_lv, position=(1800+50-1050-32 +25*4+100-37.5, 3000+154+1186-50+20), transformation=i3.Rotation(rotation=90)))

chip_elements.append(i3.SRef(reference=bg_test_3_lv, position=(1800+50-1050-32 +25*5+100-37.5, 3000+154+1186-50+20), transformation=i3.Rotation(rotation=90)))

# BG_4: 4 devices
fp_width_4=0.8

bg_test_4 = BG_Test_4()
bg_test_4_lv = bg_test_4.Layout(fp_width=fp_width_4, fp_length=fp_length_test)
chip_elements.append(i3.SRef(reference=bg_test_4_lv, position=(1800+50-1050-32 +25*6+100-37.5, 3000+154+1186-50+20), transformation=i3.Rotation(rotation=90)))

chip_elements.append(i3.SRef(reference=bg_test_4_lv, position=(1800+50-1050-32 +25*7+100-37.5, 3000+154+1186-50+20), transformation=i3.Rotation(rotation=90)))


# BG_5: 4 devices
fp_width_5=0.8

bg_test_5 = BG_Test_5()
bg_test_5_lv = bg_test_5.Layout(fp_width=fp_width_5, fp_length=fp_length_test)
chip_elements.append(i3.SRef(reference=bg_test_5_lv, position=(1800+50-1050-32 +25*8+100-37.5, 3000+154+1186-50+20), transformation=i3.Rotation(rotation=90)))

chip_elements.append(i3.SRef(reference=bg_test_5_lv, position=(1800+50-1050-32 +25*9+100-37.5, 3000+154+1186-50+20), transformation=i3.Rotation(rotation=90)))


# BG_6: 4 devices
fp_width_6=1.0

bg_test_6 = BG_Test_6()
bg_test_6_lv = bg_test_6.Layout(fp_width=fp_width_6, fp_length=fp_length_test)
chip_elements.append(i3.SRef(reference=bg_test_6_lv, position=(1800+50-1050-32 +25*10+100-37.5, 3000+154+1186-50+20), transformation=i3.Rotation(rotation=90)))

chip_elements.append(i3.SRef(reference=bg_test_6_lv, position=(1800+50-1050-32 +25*11+100-37.5, 3000+154+1186-50+20), transformation=i3.Rotation(rotation=90)))


# BG_7: 4 devices
fp_width_7=1.0

bg_test_7 = BG_Test_7()
bg_test_7_lv = bg_test_7.Layout(fp_width=fp_width_7, fp_length=fp_length_test)
chip_elements.append(i3.SRef(reference=bg_test_7_lv, position=(1800+50-1050-32 +25*12+100-37.5, 3000+154+1186-50+20), transformation=i3.Rotation(rotation=90)))

chip_elements.append(i3.SRef(reference=bg_test_7_lv, position=(1800+50-1050-32 +25*13+100-37.5, 3000+154+1186-50+20), transformation=i3.Rotation(rotation=90)))


# BG_8: 4 devices
fp_width_8=1.0

bg_test_8 = BG_Test_8()
bg_test_8_lv = bg_test_8.Layout(fp_width=fp_width_8, fp_length=fp_length_test)
chip_elements.append(i3.SRef(reference=bg_test_8_lv, position=(1800+50-1050-32 +25*14+100-37.5, 3000+154+1186-50+20), transformation=i3.Rotation(rotation=90)))

chip_elements.append(i3.SRef(reference=bg_test_8_lv, position=(1800+50-1050-32 +25*15+100-37.5, 3000+154+1186-50+20), transformation=i3.Rotation(rotation=90)))

# # Grating coupler
#
ring_test_1_gc = All_pass_ring_GC_2()
ring_test_1_gc_lv = ring_test_1_gc.Layout(ring_gap=0.3)
# ring_lv.visualize(annotate=True)
chip_elements.append(i3.SRef(reference=ring_test_1_gc_lv, position=(2455, 4757.5+20)))

ring_test_2_gc = All_pass_ring_GC_2()
ring_test_2_gc_lv = ring_test_2_gc.Layout(ring_gap=0.4)
# ring_lv.visualize(annotate=True)
chip_elements.append(i3.SRef(reference=ring_test_2_gc_lv, position=(2455, 4627.5+20)))

ring_test_3_gc = All_pass_ring_GC_2()
ring_test_3_gc_lv = ring_test_3_gc.Layout(ring_gap=0.5)
# ring_lv.visualize(annotate=True)
chip_elements.append(i3.SRef(reference=ring_test_3_gc_lv, position=(3455, 4757.5+20)))

ring_test_4_gc = All_pass_ring_GC_2()
ring_test_4_gc_lv = ring_test_4_gc.Layout(ring_gap=0.6)
# ring_lv.visualize(annotate=True)
chip_elements.append(i3.SRef(reference=ring_test_4_gc_lv, position=(3455, 4627.5+20)))


ring_test_5_gc = All_pass_ring_GC_2()
ring_test_5_gc_lv = ring_test_5_gc.Layout(ring_gap=0.7)
# ring_lv.visualize(annotate=True)
chip_elements.append(i3.SRef(reference=ring_test_5_gc_lv, position=(4505, 4757.5+20)))

ring_test_6_gc = All_pass_ring_GC_2()
ring_test_6_gc_lv = ring_test_6_gc.Layout(ring_gap=0.8)
# ring_lv.visualize(annotate=True)
chip_elements.append(i3.SRef(reference=ring_test_6_gc_lv, position=(4505, 4627.5+20)))
#
# #### Ring test width
ring_width_test_1_gc = All_pass_ring_GC_4()
ring_width_test_1_gc_lv = ring_width_test_1_gc.Layout(ring_gap=0.65, ring_width=1.68, bus_length=25)
# ring_lv.visualize(annotate=True)
chip_elements.append(i3.SRef(reference=ring_width_test_1_gc_lv, position=(8055, 2827.5-45+2.5+20), transformation=i3.Rotation(rotation=90)))

ring_width_test_2_gc = All_pass_ring_GC_4()
ring_width_test_2_gc_lv = ring_width_test_2_gc.Layout(ring_gap=0.65, ring_width=1.69, bus_length=25)
# ring_lv.visualize(annotate=True)
chip_elements.append(i3.SRef(reference=ring_width_test_2_gc_lv, position=(8155, 2827.5-45+2.5+20), transformation=i3.Rotation(rotation=90)))

ring_width_test_3_gc = All_pass_ring_GC_4()
ring_width_test_3_gc_lv = ring_width_test_3_gc.Layout(ring_gap=0.65, ring_width=1.70, bus_length=50)
# ring_lv.visualize(annotate=True)
chip_elements.append(i3.SRef(reference=ring_width_test_3_gc_lv, position=(8555+18, 2827.5-42.5+20), transformation=i3.Rotation(rotation=90)))

ring_width_test_4_gc = All_pass_ring_GC_4()
ring_width_test_4_gc_lv = ring_width_test_4_gc.Layout(ring_gap=0.65, ring_width=1.71, bus_length=50)
# ring_lv.visualize(annotate=True)
chip_elements.append(i3.SRef(reference=ring_width_test_4_gc_lv, position=(8655+18, 2827.5-42.5+20), transformation=i3.Rotation(rotation=90)))

ring_width_test_5_gc = All_pass_ring_GC_4()
ring_width_test_5_gc_lv = ring_width_test_5_gc.Layout(ring_gap=0.65, ring_radius=23.3, ring_width=1.72, bus_length=50)
# ring_lv.visualize(annotate=True)
chip_elements.append(i3.SRef(reference=ring_width_test_5_gc_lv, position=(8955+12, 2827.5-37.5-5+20), transformation=i3.Rotation(rotation=90)))

ring_width_test_6_gc = All_pass_ring_GC_4()
ring_width_test_6_gc_lv = ring_width_test_6_gc.Layout(ring_gap=0.65, ring_radius=23.3, ring_width=1.73, bus_length=50)
# ring_lv.visualize(annotate=True)
chip_elements.append(i3.SRef(reference=ring_width_test_6_gc_lv, position=(9055+12, 2827.5-37.5-5+20), transformation=i3.Rotation(rotation=90)))

ring_width_test_7_gc = All_pass_ring_GC_3()
ring_width_test_7_gc_lv = ring_width_test_7_gc.Layout(ring_gap=0.65, ring_radius=23.3, ring_width=1.74)
# ring_lv.visualize(annotate=True)
chip_elements.append(i3.SRef(reference=ring_width_test_7_gc_lv, position=(9305, 2827.5-2.5+20), transformation=i3.Rotation(rotation=90)))

ring_width_test_8_gc = All_pass_ring_GC_3()
ring_width_test_8_gc_lv = ring_width_test_8_gc.Layout(ring_gap=0.65, ring_radius=23.3, ring_width=1.75)
# ring_lv.visualize(annotate=True)
chip_elements.append(i3.SRef(reference=ring_width_test_8_gc_lv, position=(9405, 2827.5-2.5+20), transformation=i3.Rotation(rotation=90)))

ring_width_test_9_gc = All_pass_ring_GC_3()
ring_width_test_9_gc_lv = ring_width_test_9_gc.Layout(ring_gap=0.65, ring_radius=23.3, ring_width=1.76)
# ring_lv.visualize(annotate=True)
chip_elements.append(i3.SRef(reference=ring_width_test_9_gc_lv, position=(8905+60, 4227.5+120+7.5+20), transformation=i3.Rotation(rotation=90)))

ring_width_test_10_gc = All_pass_ring_GC_3()
ring_width_test_10_gc_lv = ring_width_test_10_gc.Layout(ring_gap=0.65, ring_radius=23.3, ring_width=1.77)
# ring_lv.visualize(annotate=True)
chip_elements.append(i3.SRef(reference=ring_width_test_10_gc_lv, position=(9005+60, 4227.5+120+7.5+20), transformation=i3.Rotation(rotation=90)))

ring_width_test_11_gc = All_pass_ring_GC_3()
ring_width_test_11_gc_lv = ring_width_test_11_gc.Layout(ring_gap=0.65, ring_radius=23.3, ring_width=1.78)
# ring_lv.visualize(annotate=True)
chip_elements.append(i3.SRef(reference=ring_width_test_11_gc_lv, position=(9305, 4327.5+27.5+20), transformation=i3.Rotation(rotation=90)))
#
ring_width_test_12_gc = All_pass_ring_GC_3()
ring_width_test_12_gc_lv = ring_width_test_12_gc.Layout(ring_gap=0.65, ring_radius=23.3, ring_width=1.79)
# ring_lv.visualize(annotate=True)
chip_elements.append(i3.SRef(reference=ring_width_test_12_gc_lv, position=(9405, 4327.5+27.5+20), transformation=i3.Rotation(rotation=90)))

####################################
### Generate the main layout
####################################
chip_design = i3.LayoutCell(name = "TOP")

chip_layout = chip_design.Layout(elements=chip_elements)

chip_layout.write_gdsii("gds_output/ligentec_all-components_9.4.gds")
