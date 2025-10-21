import sys

from setuptools.command.rotate import rotate

sys.path.append("C:/pdk/Ligentec_SiN_2025/ipkiss")

# import asp_sin_lnoi_photonics.technology
# import asp_sin_lnoi_photonics.all as asp

from bragg_grating_exspot import FP_BG_1_Exspot, Sinusoidal_BG_Exspot
from waveguide_taper import Waveguide_Exspot, Waveguide_Exspot_2
from Bragg_grating import SinusoidalGratingTaper, Sinusoidal_BG, SinusoidalGrating
# from Bragg_grating_test import BG_Test_Sinusoidal

from Bragg_grating_test_lensed_fiber_bb import BG_Test_1_lensed_fiber, BG_Test_2_lensed_fiber

from exspot_test import Exspot_Spiral_Circular_GC

import ligentec_an800.all as pdk

from grating_coupler_test import  All_pass_ring_GC
from All_pass_ring_taper import All_pass_ring_Exspot_Test

from Aux_ring import Aux_add_drop_ring_1_2

import ipkiss3.all as i3
import numpy as np

from chip_frame import CSL_FRAME_10500_4850

chip_elements = list()
###########################
## For component testing
###########################

test_component =Aux_add_drop_ring_1_2()
test_component_lv = test_component.Layout(p1_module=True)
test_component_lv.write_gdsii("gds_output/test_component_lv_2.gds")