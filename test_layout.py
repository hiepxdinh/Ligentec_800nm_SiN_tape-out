import sys

sys.path.append("C:/pdk/Ligentec_SiN_2025/ipkiss")

# import asp_sin_lnoi_photonics.technology
# import asp_sin_lnoi_photonics.all as asp


import ligentec_an800.all as pdk

import ipkiss3.all as i3
import numpy as np

from chip_frame import CSL_FRAME_10500_4850, CHS_FRAME_10500_4850_HALF, CHS_FRAME_10500_HALF_4850_HALF
#
# from ring_gc.cell import RingModulatorGC
# from ring_modulator.cell import AddDropRingWithElectrode
# from waveguide_loop.cell import WaveguideLoop
from Aux_ring import HeaterNotchRacetrack, Aux_all_pass_ring, Aux_add_drop_ring
from All_pass_ring_taper import All_pass_ring_taper
from Aux_ring_taper import Aux_add_drop_ring_taper
from waveguide_taper import Waveguide_test
from Bragg_grating import Unit_Cell, Bragg_grating
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

##################################
### Section for all-pass ring
##################################

# Radius: 50um
radius = 50.0
h_separation = 500.0
v_separation = 35.0
separation = (0, 175, 175, 175, 175, 175, 175, 175, 175, 175)
offset = 125
gap_list = [2.05]
for i, gap in enumerate(separation):
    ring = All_pass_ring_taper(ring_position_x=-i*h_separation, ring_position_y=(1-i)*v_separation, output_offset=offset)
    ring_lv = ring.Layout(ring_radius=radius)
    # ring_lv.visualize(annotate=True)
    chip_elements.append(i3.SRef(reference=ring, position=(5395, 0)))

# Radius: 100um
radius = 100.0
h_separation = 500.0
v_separation = 35.0
separation = (0, 175, 175, 175, 175, 175, 175, 175, 175, 175)
offset = 200
gap_list = [2.05]
for i, gap in enumerate(separation):
    ring = All_pass_ring_taper(ring_position_x=-i*h_separation, ring_position_y=(1-i)*v_separation, output_offset=offset)
    ring_lv = ring.Layout(ring_radius=radius)
    # ring_lv.visualize(annotate=True)
    chip_elements.append(i3.SRef(reference=ring, position=(5395, 600)))

# Radius: 200um
radius = 200.0
h_separation = 550.0
v_separation = 35.0
separation = (0, 175, 175, 175, 175, 175, 175, 175, 175, 175)
offset = 250
out_taper_position = 150
gap_list = [2.05]
for i, gap in enumerate(separation):
    name = "All_Pass_Ring_{}".format(radius)
    ring = All_pass_ring_taper(ring_position_x=-i*h_separation+350, ring_position_y=(1-i)*v_separation, output_offset=offset, out_taper_position = out_taper_position)
    ring_lv = ring.Layout(ring_radius=radius)
    # ring_lv.visualize(annotate=True)
    chip_elements.append(i3.SRef(reference=ring, position=(5395, 1500)))

##################################
### Section for aux ring
##################################
name = "All_Pass_Ring"
aux_ring = Aux_add_drop_ring_taper(name=name)
aux_ring_lv = aux_ring.Layout(main_radius=300, aux_radius=50)
chip_elements.append(i3.SRef(reference=aux_ring, position=(0, 2500)))

##################################
### Section Waveguide test
##################################
waveguide_width = [1.0, 1.5, 2.0]
separation =  100
for i, width in enumerate(waveguide_width):
    waveguide_test = Waveguide_test()
    waveguide_test_lv = waveguide_test.Layout(width_in=waveguide_width[i])
    chip_elements.append(i3.SRef(reference=waveguide_test, position=(-3000, i*separation)))

##################################
### Section ExSpot
##################################

exspot_pkg = pdk.AN800BB_ExSpot_packaging_SMF_C()
exspot_pkg_lv = exspot_pkg.Layout()
chip_elements.append(i3.SRef(reference=exspot_pkg, position=(-3000, 3000)))

##################################
### Section P1
##################################

elecvia = pdk.ElecVia()
elecvia_pkg_lv = elecvia.Layout()
chip_elements.append(i3.SRef(reference=elecvia, position=(-3000, 3100)))

####################################
### Generate the main layout
####################################
chip_design = i3.LayoutCell(name = "Top")

chip_layout = chip_design.Layout(elements=chip_elements)

chip_layout.write_gdsii("gds_output/ligentec.gds")

############################
### For component testing
############################

# test_component = pdk.LinearTaperFromPort()
# test_component_lv = test_component.Layout()
# test_component_lv.visualize(annotate=True)
# # test_component_lv.write_gdsii("gds_output/test_component_lv.gds")