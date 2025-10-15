import sys

from setuptools.command.rotate import rotate

sys.path.append("C:/pdk/Ligentec_SiN_2025/ipkiss")

# import asp_sin_lnoi_photonics.technology
# import asp_sin_lnoi_photonics.all as asp

from Bragg_grating import FP_BG_1

import ligentec_an800.all as pdk

import ipkiss3.all as i3
import numpy as np

chip_elements = list()
###########################
## For component testing
###########################

test_component = FP_BG_1()
test_component_lv = test_component.Layout(fp_width = 0.8, fp_length = 1486)
# test_component_lv.visualize(annotate=True)
test_component_lv.write_gdsii("gds_output/test_component_lv_2.gds")