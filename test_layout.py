import sys

sys.path.append("C:/pdk/Ligentec_SiN_2025/ipkiss")

# import asp_sin_lnoi_photonics.technology
# import asp_sin_lnoi_photonics.all as asp


import ligentec_an800.all as pdk

import ipkiss3.all as i3
import numpy as np
#
# from ring_gc.cell import RingModulatorGC
# from ring_modulator.cell import AddDropRingWithElectrode
# from waveguide_loop.cell import WaveguideLoop
from Aux_ring import HeaterNotchRacetrack, Aux_all_pass_ring, Aux_add_drop_ring
from All_pass_ring_taper import All_pass_ring_taper
#
# #######################################
# # Global parameters
# ######################################
# waveguide_spacing = 50 # spacing between adjacent waveguides
# bend_radius = 200  # Bending radius used in waveguide routing
# hot_electrode_width = 20
# fibre_array_pich = 127
# ebl_writing_size = (1000, 1000)

chip_elements = list()

###################################
# Section for all-pass ring
###################################

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
    chip_elements.append(i3.SRef(reference=ring, position=(0, 0)))

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
    chip_elements.append(i3.SRef(reference=ring, position=(0, 600)))

# Radius: 200um
radius = 200.0
h_separation = 550.0
v_separation = 35.0
separation = (0, 175, 175, 175, 175, 175, 175, 175, 175, 175)
offset = 250
out_taper_position = 150
gap_list = [2.05]
for i, gap in enumerate(separation):
    ring = All_pass_ring_taper(ring_position_x=-i*h_separation+350, ring_position_y=(1-i)*v_separation, output_offset=offset, out_taper_position = out_taper_position)
    ring_lv = ring.Layout(ring_radius=radius)
    # ring_lv.visualize(annotate=True)
    chip_elements.append(i3.SRef(reference=ring, position=(0, 1500)))

# ####################################
# # Generate the main layout
# ####################################
chip_design = i3.LayoutCell(name = "Top")

chip_layout = chip_design.Layout(elements=chip_elements)

chip_layout.write_gdsii("gds_output/ligentec.gds")

############################
# For component testing
############################
#
# chip_elements = list()
#
# test_compnent = Aux_add_drop_ring()
#
# # test_compnent = pdk.HeaterNotchRacetrack()
#
# test_compnent_lv = test_compnent.Layout(main_radius=450.0, aux_radius=45.0, ring_gap=2.0)
# test_compnent_lv.visualize(annotate=True)
# test_compnent_lv.write_gdsii("gds_output/test_compnent_lv.gds")