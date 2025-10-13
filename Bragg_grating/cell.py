
import sys
import numpy as np

sys.path.append("C:/pdk/Ligentec_SiN_2025/ipkiss")


import ligentec_an800.all as pdk
import ipkiss3.all as i3
import numpy as np

x = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50]
y = [5, 3, 4, 5, 3, 4, 2, 1, 5, 3, 4]

array = np.loadtxt("C:/Users/Administrator/Documents/GitHub/Ligentec_800nm_SiN_tape-out/Bragg_grating/Design1_grating_params_2.csv", delimiter=',')
BG_1_length_1 = array[:, 0]
BG_1_width_1 = array[:, 2]
BG_1_length_2 = array[:, 1]
BG_1_width_2 = array[:, 3]


class BG_1(i3.PCell):

    # waveguide_1 = i3.ChildCellProperty(doc="first waveguide")
    # waveguide_2 = i3.ChildCellProperty(doc="second waveguide")

    # These lines cause errors. Do not need if a for loop is required.

    # def _default_waveguide_1(self):
    #     return pdk.Straight()
    #
    # def _default_waveguide_2(self):
    #     return pdk.Straight()

    # NOTE: Referencing a child cell directly reuses the same instance, and even if we pass different parameters to its layout,
    # the actual layout might not be applied unless handled properly.
    # since waveguide_1 is PCell, when we call .layout, it returns a view of the same cell with different parameters. However, the actual instance referenced in SRef may still point to the same base cell.
    # As a result, IPKISS internally optimizes and deduplicate layouts, and it might end up showing only the last one, or the same one for all iterations.
    # To solve it, we must instantiate a new PCell with its parameters, not reuse the same ChildCellProperty inside the loop.
    # DO NOT USE:     wg1_lv = self.cell.waveguide_1.Layout(width=width_1, length=length_1)
    #                 wg2_lv = self.cell.waveguide_2.Layout(width=width_2, length=length_2)

    class Layout(i3.LayoutView):
        width_1 = i3.NonNegativeNumberProperty(default=1.0,doc="width of first waveguide")
        length_1 = i3.NonNegativeNumberProperty(default=1.0,doc="length of first waveguide")
        width_2 = i3.NonNegativeNumberProperty(default=1.0,doc="width of second waveguide")
        length_2 = i3.NonNegativeNumberProperty(default=1.0,doc="length of second waveguide")

        def _generate_instances(self, insts):
            insts += i3.InstanceDict()
            x_pos = 0
            for idx in range(len(BG_1_width_1)):
                width_1 = BG_1_width_1[idx]
                length_1 = BG_1_length_1[idx]
                width_2 = BG_1_width_2[idx]
                length_2 = BG_1_length_2[idx]

                wg1 = pdk.Straight(name=f"wg1_{idx}")
                wg1_lv = wg1.Layout(width=width_1, length=length_1)
                # print(f"wg1_{idx} ports:", wg1_lv.ports.keys())
                wg2 = pdk.Straight(name=f"wg2_{idx}")
                wg2_lv = wg2.Layout(width=width_2, length=length_2)
                insts += i3.SRef(name=f"wg1_{idx}",reference=wg1_lv, flatten=True, position=(x_pos, 0))
                x_pos += length_1
                insts += i3.SRef(name=f"wg2_{idx}",reference=wg2_lv, flatten=True, position=(x_pos, 0))
                x_pos += length_2

                # print(insts)

            return insts

        def _generate_ports(self, ports):
            return i3.expose_ports(
                self.instances,
                {
                    f"wg1_0:in0": "in",  # Start of the waveguide chain
                    f"wg2_{len(BG_1_width_1) - 1}:out0": "out",  # End of the last waveguide
                },
            )


class FP_Waveguide_width_Linear_Taper(i3.PCell):
    fp_waveguide = i3.ChildCellProperty(doc="fabry perot waveguide")
    linear_taper = i3.ChildCellProperty(doc="linear taper")

    # trace_template_in = i3.ChildCellProperty(doc="input template for linear taper")
    # trace_template_out = i3.ChildCellProperty(doc="out template for linear taper")

    def _default_fp_waveguide(self):
        return pdk.Straight()

    # These trace template used if linear taper not pre-defined.

    # def _default_trace_template_in(self):
    #     return pdk.WireWaveguideTemplate()
    #
    # def _default_trace_template_out(self):
    #     return pdk.WireWaveguideTemplate()

    def _default_linear_taper(self):
        # return pdk.LinearTaperFromPort(start_trace_template = self.trace_template_in, end_trace_template = self.trace_template_out)
        return pdk.Taper()

    class Layout(i3.LayoutView):
        fp_width = i3.PositiveNumberProperty(default=1.0, doc="width of fabry perot waveguide")
        fp_length = i3.PositiveNumberProperty(default=150.0, doc="length of fabry perot waveguide")
        end_taper_width = i3.PositiveNumberProperty(default=0.5, doc="width of end taper port")
        linear_taper_length = i3.PositiveNumberProperty(default=10.0, doc="width of end taper port")

        def _default_fp_waveguide(self):
            cell = self.cell.fp_waveguide
            lv = cell.get_default_view(self)
            lv.set(
                width=self.fp_width,
                length=self.fp_length,
            )
            return lv

        def _default_linear_taper(self):
            cell = self.cell.linear_taper
            lv = cell.get_default_view(self)
            lv.set(
                in_width=self.fp_width,
                out_width=self.end_taper_width,
                length=self.linear_taper_length,
            )
            return lv

        # def _default_trace_template_in(self):
        #     cell = self.cell.trace_template_in
        #     lv = cell.get_default_view(i3.LayoutView)
        #     lv.set(core_width=self.fp_width)
        #     return lv
        #
        # def _default_trace_template_out(self):
        #     cell = self.cell.trace_template_out
        #     lv = cell.get_default_view(i3.LayoutView)
        #     lv.set(core_width=self.end_taper_width)
        #     return lv

        def _generate_instances(self, insts):
            fp_waveguide = self.fp_waveguide
            linear_taper = self.linear_taper
            insts += i3.SRef(name="fp_waveguide", reference=fp_waveguide, flatten=True)
            insts += i3.SRef(name="linear_taper_in", reference=linear_taper, flatten=True)
            insts += i3.SRef(name="linear_taper_out", reference=linear_taper, flatten=True)

            return i3.place_and_route(
                insts=insts,
                specs=[
                    i3.Place("fp_waveguide", (0, 0)),
                    i3.Place("linear_taper_in", (0, 0), angle=180, relative_to="fp_waveguide:in0"),
                    i3.Place("linear_taper_out", (0, 0), angle=0, relative_to="fp_waveguide:out0"),
                    ]
            )

        def _generate_ports(self, ports):
            return i3.expose_ports(
                self.instances,
                {
                    "linear_taper_in:out0": "in",
                    "linear_taper_out:out0": "out",
                },
            )




# class Unit_Cell(i3.PCell):
#
#     waveguide_1 = i3.ChildCellProperty(doc="straight waveguide", locked=True)
#
#     waveguide_2 = i3.ChildCellProperty(doc="straight waveguide", locked=True)
#
#     def _default_waveguide_1(self):
#         wg_1 = pdk.Straight(name=self.name + "_WG1")
#         return wg_1
#
#     def _default_waveguide_2(self):
#         wg_2 = pdk.Straight(name=self.name + "_WG2")
#         return wg_2
#
#     class Layout(i3.LayoutView):
#         width_1 = i3.PositiveNumberProperty(default=1.0, doc="width of first waveguide")
#         width_2 = i3.PositiveNumberProperty(default=2.0, doc="width of second waveguide")
#         length_1 = i3.PositiveNumberProperty(default=1.0, doc="length of first waveguide")
#         length_2 = i3.PositiveNumberProperty(default=2.0, doc="length of second waveguide")
#
#         unit_cell_length = i3.PositiveNumberProperty(doc="length of unit cell")
#
#         def _default_unit_cell_length (self):
#             return self.length_1 + self.length_2
#
#         def _default_waveguide_1(self):
#             cell = self.cell.waveguide_1
#             lv = cell.get_default_view(self)
#             lv.set(
#                 width=self.width_1,
#                 length=self.length_1,
#             )
#             return lv
#
#         def _default_waveguide_2(self):
#             cell = self.cell.waveguide_2
#             lv = cell.get_default_view(self)
#             lv.set(
#                 width=self.width_2,
#                 length=self.length_2,
#             )
#             return lv
#
#         def _generate_instances(self, insts):
#             waveguide_1 = self.waveguide_1
#             waveguide_2 = self.waveguide_2
#
#             insts += i3.SRef(name="waveguide_1", reference=waveguide_1, flatten=True)
#             insts += i3.SRef(name="waveguide_2", reference=waveguide_2, flatten=True)
#
#             return i3.place_and_route(
#                 insts=insts,
#                 specs=[
#                     i3.Place("waveguide_1", (0, 0)),
#                     i3.Place("waveguide_2", (0, 0), relative_to="waveguide_1:out0"),
#                     ]
#             )
#
#         def _generate_ports(self, ports):
#             return i3.expose_ports(
#                 self.instances,
#                 {
#                     "waveguide_1:in0": "in0",
#                     "waveguide_2:out0": "out0",
#                 },
#             )
#
# class Bragg_grating(i3.PCell):
#     unit_cell = i3.ChildCellProperty(doc='unit cell of the grating')
#
#     def _default_unit_cell(self):
#         return Unit_Cell()
#
#     class Layout(i3.LayoutView):
#
#         width_1 = i3.PositiveNumberProperty(default=1.0, doc="width of first waveguide")
#         width_2 = i3.PositiveNumberProperty(default=2.0, doc="width of second waveguide")
#         length_1 = i3.PositiveNumberProperty(default=1.0, doc="length of first waveguide")
#         length_2 = i3.PositiveNumberProperty(default=2.0, doc="length of second waveguide")
#
#         # grating_length = i3.PositiveNumberProperty(doc='Total length of the grating')
#
#         period = i3.PositiveIntProperty(default = 10, doc= 'the number of times the unit cell repeats')
#
#         def _default_unit_cell(self):
#             unit_cell_layout = self.cell.unit_cell.get_default_view(i3.LayoutView)
#             unit_cell_layout.set(width_1=self.width_1)
#             unit_cell_layout.set(width_2=self.width_2)
#             unit_cell_layout.set(length_1=self.length_1)
#             unit_cell_layout.set(length_2=self.length_2)
#             return unit_cell_layout
#
#         def _generate_instances(self, insts):
#             unit_cell_lo = self.cell.unit_cell.get_default_view(i3.LayoutView)
#             cell_length = unit_cell_lo.unit_cell_length
#             insts += i3.ARef(name='unit_cell', reference=self.unit_cell, origin=(0, 0), period=(cell_length,0),
#                              n_o_periods=(self.period,1))
#
#             return insts
#
#         def _generate_ports(self, ports):
#             unit_cell_lo = self.cell.unit_cell.get_default_view(i3.LayoutView)
#             cell_length = unit_cell_lo.unit_cell_length
#             ports += i3.OpticalPort(name="in", position=(0.0, 0))
#             ports += i3.OpticalPort(name="out", position=(self.period*cell_length, 0))
#             return ports







