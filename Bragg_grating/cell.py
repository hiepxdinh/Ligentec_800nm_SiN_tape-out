
import sys
import numpy as np
from PIL.ImageOps import mirror

sys.path.append("C:/pdk/Ligentec_SiN_2025/ipkiss")


import ligentec_an800.all as pdk
import ipkiss3.all as i3
import numpy as np

x = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50]
y = [5, 3, 4, 5, 3, 4, 2, 1, 5, 3, 4]

array_1 = np.loadtxt("C:/Users/Administrator/Documents/GitHub/Ligentec_800nm_SiN_tape-out/Bragg_grating/Design_1_grating_params_2.csv", delimiter=',')
BG_1_length_1 = array_1[:, 0]
BG_1_width_1 = array_1[:, 2]
BG_1_length_2 = array_1[:, 1]
BG_1_width_2 = array_1[:, 3]


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

array_2 = np.loadtxt("C:/Users/Administrator/Documents/GitHub/Ligentec_800nm_SiN_tape-out/Bragg_grating/Design_2_grating_params_2.csv", delimiter=',')
BG_2_length_1 = array_2[:, 0]
BG_2_width_1 = array_2[:, 2]
BG_2_length_2 = array_2[:, 1]
BG_2_width_2 = array_2[:, 3]


class BG_2(i3.PCell):

    class Layout(i3.LayoutView):
        width_1 = i3.NonNegativeNumberProperty(default=1.0,doc="width of first waveguide")
        length_1 = i3.NonNegativeNumberProperty(default=1.0,doc="length of first waveguide")
        width_2 = i3.NonNegativeNumberProperty(default=1.0,doc="width of second waveguide")
        length_2 = i3.NonNegativeNumberProperty(default=1.0,doc="length of second waveguide")

        def _generate_instances(self, insts):
            insts += i3.InstanceDict()
            x_pos = 0
            for idx in range(len(BG_2_width_1)):
                width_1 = BG_2_width_1[idx]
                length_1 = BG_2_length_1[idx]
                width_2 = BG_2_width_2[idx]
                length_2 = BG_2_length_2[idx]

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
                    f"wg2_{len(BG_2_width_1) - 1}:out0": "out",  # End of the last waveguide
                },
            )

array_3 = np.loadtxt("C:/Users/Administrator/Documents/GitHub/Ligentec_800nm_SiN_tape-out/Bragg_grating/Design_3_grating_params_2.csv", delimiter=',')
BG_3_length_1 = array_3[:, 0]
BG_3_width_1 = array_3[:, 2]
BG_3_length_2 = array_3[:, 1]
BG_3_width_2 = array_3[:, 3]


class BG_3(i3.PCell):

    class Layout(i3.LayoutView):
        width_1 = i3.NonNegativeNumberProperty(default=1.0,doc="width of first waveguide")
        length_1 = i3.NonNegativeNumberProperty(default=1.0,doc="length of first waveguide")
        width_2 = i3.NonNegativeNumberProperty(default=1.0,doc="width of second waveguide")
        length_2 = i3.NonNegativeNumberProperty(default=1.0,doc="length of second waveguide")

        def _generate_instances(self, insts):
            insts += i3.InstanceDict()
            x_pos = 0
            for idx in range(len(BG_3_width_1)):
                width_1 = BG_3_width_1[idx]
                length_1 = BG_3_length_1[idx]
                width_2 = BG_3_width_2[idx]
                length_2 = BG_3_length_2[idx]

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
                    f"wg2_{len(BG_3_width_1) - 1}:out0": "out",  # End of the last waveguide
                },
            )

array_4 = np.loadtxt("C:/Users/Administrator/Documents/GitHub/Ligentec_800nm_SiN_tape-out/Bragg_grating/Design_4_grating_params_2.csv", delimiter=',')
BG_4_length_1 = array_4[:, 0]
BG_4_width_1 = array_4[:, 2]
BG_4_length_2 = array_4[:, 1]
BG_4_width_2 = array_4[:, 3]


class BG_4(i3.PCell):

    class Layout(i3.LayoutView):
        width_1 = i3.NonNegativeNumberProperty(default=1.0,doc="width of first waveguide")
        length_1 = i3.NonNegativeNumberProperty(default=1.0,doc="length of first waveguide")
        width_2 = i3.NonNegativeNumberProperty(default=1.0,doc="width of second waveguide")
        length_2 = i3.NonNegativeNumberProperty(default=1.0,doc="length of second waveguide")

        def _generate_instances(self, insts):
            insts += i3.InstanceDict()
            x_pos = 0
            for idx in range(len(BG_4_width_1)):
                width_1 = BG_4_width_1[idx]
                length_1 = BG_4_length_1[idx]
                width_2 = BG_4_width_2[idx]
                length_2 = BG_4_length_2[idx]

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
                    f"wg2_{len(BG_4_width_1) - 1}:out0": "out",  # End of the last waveguide
                },
            )

array_5 = np.loadtxt("C:/Users/Administrator/Documents/GitHub/Ligentec_800nm_SiN_tape-out/Bragg_grating/Design_5_grating_params_2.csv", delimiter=',')
BG_5_length_1 = array_5[:, 0]
BG_5_width_1 = array_5[:, 2]
BG_5_length_2 = array_5[:, 1]
BG_5_width_2 = array_5[:, 3]

class BG_5(i3.PCell):

    class Layout(i3.LayoutView):
        width_1 = i3.NonNegativeNumberProperty(default=1.0,doc="width of first waveguide")
        length_1 = i3.NonNegativeNumberProperty(default=1.0,doc="length of first waveguide")
        width_2 = i3.NonNegativeNumberProperty(default=1.0,doc="width of second waveguide")
        length_2 = i3.NonNegativeNumberProperty(default=1.0,doc="length of second waveguide")

        def _generate_instances(self, insts):
            insts += i3.InstanceDict()
            x_pos = 0
            for idx in range(len(BG_5_width_1)):
                width_1 = BG_5_width_1[idx]
                length_1 = BG_5_length_1[idx]
                width_2 = BG_5_width_2[idx]
                length_2 = BG_5_length_2[idx]

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
                    f"wg2_{len(BG_5_width_1) - 1}:out0": "out",  # End of the last waveguide
                },
            )

array_6 = np.loadtxt("C:/Users/Administrator/Documents/GitHub/Ligentec_800nm_SiN_tape-out/Bragg_grating/Design_6_grating_params_2.csv", delimiter=',')
BG_6_length_1 = array_6[:, 0]
BG_6_width_1 = array_6[:, 2]
BG_6_length_2 = array_6[:, 1]
BG_6_width_2 = array_6[:, 3]

class BG_6(i3.PCell):

    class Layout(i3.LayoutView):
        width_1 = i3.NonNegativeNumberProperty(default=1.0,doc="width of first waveguide")
        length_1 = i3.NonNegativeNumberProperty(default=1.0,doc="length of first waveguide")
        width_2 = i3.NonNegativeNumberProperty(default=1.0,doc="width of second waveguide")
        length_2 = i3.NonNegativeNumberProperty(default=1.0,doc="length of second waveguide")

        def _generate_instances(self, insts):
            insts += i3.InstanceDict()
            x_pos = 0
            for idx in range(len(BG_6_width_1)):
                width_1 = BG_6_width_1[idx]
                length_1 = BG_6_length_1[idx]
                width_2 = BG_6_width_2[idx]
                length_2 = BG_6_length_2[idx]

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
                    f"wg2_{len(BG_6_width_1) - 1}:out0": "out",  # End of the last waveguide
                },
            )

array_7 = np.loadtxt("C:/Users/Administrator/Documents/GitHub/Ligentec_800nm_SiN_tape-out/Bragg_grating/Design_7_grating_params_2.csv", delimiter=',')
BG_7_length_1 = array_7[:, 0]
BG_7_width_1 = array_7[:, 2]
BG_7_length_2 = array_7[:, 1]
BG_7_width_2 = array_7[:, 3]

class BG_7(i3.PCell):

    class Layout(i3.LayoutView):
        width_1 = i3.NonNegativeNumberProperty(default=1.0,doc="width of first waveguide")
        length_1 = i3.NonNegativeNumberProperty(default=1.0,doc="length of first waveguide")
        width_2 = i3.NonNegativeNumberProperty(default=1.0,doc="width of second waveguide")
        length_2 = i3.NonNegativeNumberProperty(default=1.0,doc="length of second waveguide")

        def _generate_instances(self, insts):
            insts += i3.InstanceDict()
            x_pos = 0
            for idx in range(len(BG_7_width_1)):
                width_1 = BG_7_width_1[idx]
                length_1 = BG_7_length_1[idx]
                width_2 = BG_7_width_2[idx]
                length_2 = BG_7_length_2[idx]

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
                    f"wg2_{len(BG_7_width_1) - 1}:out0": "out",  # End of the last waveguide
                },
            )

array_8 = np.loadtxt("C:/Users/Administrator/Documents/GitHub/Ligentec_800nm_SiN_tape-out/Bragg_grating/Design_8_grating_params_2.csv", delimiter=',')
BG_8_length_1 = array_8[:, 0]
BG_8_width_1 = array_8[:, 2]
BG_8_length_2 = array_8[:, 1]
BG_8_width_2 = array_8[:, 3]

class BG_8(i3.PCell):

    class Layout(i3.LayoutView):
        width_1 = i3.NonNegativeNumberProperty(default=1.0,doc="width of first waveguide")
        length_1 = i3.NonNegativeNumberProperty(default=1.0,doc="length of first waveguide")
        width_2 = i3.NonNegativeNumberProperty(default=1.0,doc="width of second waveguide")
        length_2 = i3.NonNegativeNumberProperty(default=1.0,doc="length of second waveguide")

        def _generate_instances(self, insts):
            insts += i3.InstanceDict()
            x_pos = 0
            for idx in range(len(BG_8_width_1)):
                width_1 = BG_8_width_1[idx]
                length_1 = BG_8_length_1[idx]
                width_2 = BG_8_width_2[idx]
                length_2 = BG_8_length_2[idx]

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
                    f"wg2_{len(BG_8_width_1) - 1}:out0": "out",  # End of the last waveguide
                },
            )

array_9 = np.loadtxt("C:/Users/Administrator/Documents/GitHub/Ligentec_800nm_SiN_tape-out/Bragg_grating/Design_9_grating_params_2.csv", delimiter=',')
BG_9_length_1 = array_9[:, 0]
BG_9_width_1 = array_9[:, 2]
BG_9_length_2 = array_9[:, 1]
BG_9_width_2 = array_9[:, 3]

class BG_9(i3.PCell):

    class Layout(i3.LayoutView):
        width_1 = i3.NonNegativeNumberProperty(default=1.0,doc="width of first waveguide")
        length_1 = i3.NonNegativeNumberProperty(default=1.0,doc="length of first waveguide")
        width_2 = i3.NonNegativeNumberProperty(default=1.0,doc="width of second waveguide")
        length_2 = i3.NonNegativeNumberProperty(default=1.0,doc="length of second waveguide")

        def _generate_instances(self, insts):
            insts += i3.InstanceDict()
            x_pos = 0
            for idx in range(len(BG_9_width_1)):
                width_1 = BG_9_width_1[idx]
                length_1 = BG_9_length_1[idx]
                width_2 = BG_9_width_2[idx]
                length_2 = BG_9_length_2[idx]

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
                    f"wg2_{len(BG_8_width_1) - 1}:out0": "out",  # End of the last waveguide
                },
            )

class FP_BG_1(i3.PCell):
    fp_waveguide = i3.ChildCellProperty(doc="fabry perot waveguide")
    fp_linear_taper = i3.ChildCellProperty(doc="linear taper")
    bus_waveguide = i3.ChildCellProperty(doc="bus_waveguide")
    BG = i3.ChildCellProperty(doc="bragg grating")

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

    def _default_fp_linear_taper(self):
        # return pdk.LinearTaperFromPort(start_trace_template = self.trace_template_in, end_trace_template = self.trace_template_out)
        return pdk.Taper()

    def _default_bus_waveguide(self):
        return pdk.Sbend()

    def _default_BG(self):
        return BG_1()

    class Layout(i3.LayoutView):
        fp_width = i3.PositiveNumberProperty(default=1.0, doc="width of fabry perot waveguide")
        fp_length = i3.PositiveNumberProperty(default=150.0, doc="length of fabry perot waveguide")
        end_fp_taper_width = i3.PositiveNumberProperty(default=0.5, doc="width of end fp taper port")
        fp_taper_length = i3.PositiveNumberProperty(default=50.0, doc="length of fp taper")
        coupler_gap = i3.PositiveNumberProperty(default=2.0, doc="coupling gap between sbend and fp waveguide")

        def _default_fp_waveguide(self):
            cell = self.cell.fp_waveguide
            lv = cell.get_default_view(self)
            lv.set(
                width=self.fp_width,
                length=self.fp_length,
            )
            return lv

        def _default_end_fp_taper_width(self):
            return BG_1_width_2[len(array_1)-1]

        print("BG_1:{}".format(BG_1_width_2[len(array_1) - 1]))

        def _default_fp_linear_taper(self):
            cell = self.cell.fp_linear_taper
            lv = cell.get_default_view(self)
            lv.set(
                in_width=self.fp_width,
                out_width=self.end_fp_taper_width,
                length=self.fp_taper_length,
            )
            return lv

        def _default_bus_waveguide(self):
            cell = self.cell.bus_waveguide
            lv = cell.get_default_view(self)
            lv.set(
                width=self.fp_width,
            )
            return lv

        def _generate_instances(self, insts):
            fp_waveguide = self.fp_waveguide
            fp_linear_taper = self.fp_linear_taper
            bus_waveguide = self.bus_waveguide
            BG = self.BG

            insts += i3.SRef(name="fp_waveguide", reference=fp_waveguide, flatten=True)
            insts += i3.SRef(name="fp_linear_taper_in", reference=fp_linear_taper, flatten=True)
            insts += i3.SRef(name="fp_linear_taper_out", reference=fp_linear_taper, flatten=True)
            insts += i3.SRef(name="bus_waveguide_1", reference=bus_waveguide, flatten=True)
            insts += i3.SRef(name="bus_waveguide_2", reference=bus_waveguide, flatten=True, transformation=i3.VMirror())
            insts += i3.SRef(name="BG_in", reference=BG, flatten=True)
            insts += i3.SRef(name="BG_out", reference=BG, flatten=True)

            return i3.place_and_route(
                insts=insts,
                specs=[
                    i3.Place("fp_waveguide", (0, 0)),
                    i3.Place("fp_linear_taper_in", (0, 0), angle=180, relative_to="fp_waveguide:in0"),
                    i3.Place("fp_linear_taper_out", (0, 0), angle=0, relative_to="fp_waveguide:out0"),
                    i3.Place("BG_in:out", (0,0), relative_to="fp_linear_taper_in:out0"),
                    i3.Place("BG_out:out", (0, 0), relative_to="fp_linear_taper_out:out0", angle=180),
                    i3.Place("bus_waveguide_1", (self.fp_length/2, -self.fp_width - self.coupler_gap), angle=-180),
                    i3.Place("bus_waveguide_2", (0,0), relative_to="bus_waveguide_1:in0"),
                    ]
            )

        def _generate_ports(self, ports):
            return i3.expose_ports(
                self.instances,
                {
                    "bus_waveguide_1:out0": "in0",
                    "bus_waveguide_2:out0": "out0",
                },
            )

class FP_BG_2(i3.PCell):
    fp_waveguide = i3.ChildCellProperty(doc="fabry perot waveguide")
    fp_linear_taper = i3.ChildCellProperty(doc="linear taper")
    bus_waveguide = i3.ChildCellProperty(doc="bus_waveguide")
    BG = i3.ChildCellProperty(doc="bragg grating")

    def _default_fp_waveguide(self):
        return pdk.Straight()

    def _default_fp_linear_taper(self):
        return pdk.Taper()

    def _default_bus_waveguide(self):
        return pdk.Sbend()

    def _default_BG(self):
        return BG_2()

    class Layout(i3.LayoutView):
        fp_width = i3.PositiveNumberProperty(default=1.0, doc="width of fabry perot waveguide")
        fp_length = i3.PositiveNumberProperty(default=150.0, doc="length of fabry perot waveguide")
        end_fp_taper_width = i3.PositiveNumberProperty(default=0.5, doc="width of end fp taper port")
        fp_taper_length = i3.PositiveNumberProperty(default=50.0, doc="length of fp taper")
        coupler_gap = i3.PositiveNumberProperty(default=2.0, doc="coupling gap between sbend and fp waveguide")

        def _default_fp_waveguide(self):
            cell = self.cell.fp_waveguide
            lv = cell.get_default_view(self)
            lv.set(
                width=self.fp_width,
                length=self.fp_length,
            )
            return lv

        def _default_end_fp_taper_width(self):
            return BG_2_width_2[len(array_2)-1]

        print("BG_2:{}".format(BG_2_width_2[len(array_2) - 1]))

        def _default_fp_linear_taper(self):
            cell = self.cell.fp_linear_taper
            lv = cell.get_default_view(self)
            lv.set(
                in_width=self.fp_width,
                out_width=self.end_fp_taper_width,
                length=self.fp_taper_length,
            )
            return lv

        def _default_bus_waveguide(self):
            cell = self.cell.bus_waveguide
            lv = cell.get_default_view(self)
            lv.set(
                width=self.fp_width,
            )
            return lv

        def _generate_instances(self, insts):
            fp_waveguide = self.fp_waveguide
            fp_linear_taper = self.fp_linear_taper
            bus_waveguide = self.bus_waveguide
            BG = self.BG

            insts += i3.SRef(name="fp_waveguide", reference=fp_waveguide, flatten=True)
            insts += i3.SRef(name="fp_linear_taper_in", reference=fp_linear_taper, flatten=True)
            insts += i3.SRef(name="fp_linear_taper_out", reference=fp_linear_taper, flatten=True)
            insts += i3.SRef(name="bus_waveguide_1", reference=bus_waveguide, flatten=True)
            insts += i3.SRef(name="bus_waveguide_2", reference=bus_waveguide, flatten=True, transformation=i3.VMirror())
            insts += i3.SRef(name="BG_in", reference=BG, flatten=True)
            insts += i3.SRef(name="BG_out", reference=BG, flatten=True)

            return i3.place_and_route(
                insts=insts,
                specs=[
                    i3.Place("fp_waveguide", (0, 0)),
                    i3.Place("fp_linear_taper_in", (0, 0), angle=180, relative_to="fp_waveguide:in0"),
                    i3.Place("fp_linear_taper_out", (0, 0), angle=0, relative_to="fp_waveguide:out0"),
                    i3.Place("BG_in:out", (0,0), relative_to="fp_linear_taper_in:out0"),
                    i3.Place("BG_out:out", (0, 0), relative_to="fp_linear_taper_out:out0", angle=180),
                    i3.Place("bus_waveguide_1", (self.fp_length/2, -self.fp_width - self.coupler_gap), angle=-180),
                    i3.Place("bus_waveguide_2", (0,0), relative_to="bus_waveguide_1:in0"),
                    ]
            )

        def _generate_ports(self, ports):
            return i3.expose_ports(
                self.instances,
                {
                    "bus_waveguide_1:out0": "in0",
                    "bus_waveguide_2:out0": "out0",
                },
            )


class FP_BG_3(i3.PCell):
    fp_waveguide = i3.ChildCellProperty(doc="fabry perot waveguide")
    fp_linear_taper = i3.ChildCellProperty(doc="linear taper")
    bus_waveguide = i3.ChildCellProperty(doc="bus_waveguide")
    BG = i3.ChildCellProperty(doc="bragg grating")

    def _default_fp_waveguide(self):
        return pdk.Straight()

    def _default_fp_linear_taper(self):
        return pdk.Taper()

    def _default_bus_waveguide(self):
        return pdk.Sbend()

    def _default_BG(self):
        return BG_3()

    class Layout(i3.LayoutView):
        fp_width = i3.PositiveNumberProperty(default=1.0, doc="width of fabry perot waveguide")
        fp_length = i3.PositiveNumberProperty(default=150.0, doc="length of fabry perot waveguide")
        end_fp_taper_width = i3.PositiveNumberProperty(default=0.5, doc="width of end fp taper port")
        fp_taper_length = i3.PositiveNumberProperty(default=50.0, doc="length of fp taper")
        coupler_gap = i3.PositiveNumberProperty(default=2.0, doc="coupling gap between sbend and fp waveguide")

        def _default_fp_waveguide(self):
            cell = self.cell.fp_waveguide
            lv = cell.get_default_view(self)
            lv.set(
                width=self.fp_width,
                length=self.fp_length,
            )
            return lv

        def _default_end_fp_taper_width(self):
            return BG_3_width_2[len(array_3)-1]

        print("BG_3:{}".format(BG_3_width_2[len(array_3) - 1]))

        def _default_fp_linear_taper(self):
            cell = self.cell.fp_linear_taper
            lv = cell.get_default_view(self)
            lv.set(
                in_width=self.fp_width,
                out_width=self.end_fp_taper_width,
                length=self.fp_taper_length,
            )
            return lv

        def _default_bus_waveguide(self):
            cell = self.cell.bus_waveguide
            lv = cell.get_default_view(self)
            lv.set(
                width=self.fp_width,
            )
            return lv

        def _generate_instances(self, insts):
            fp_waveguide = self.fp_waveguide
            fp_linear_taper = self.fp_linear_taper
            bus_waveguide = self.bus_waveguide
            BG = self.BG

            insts += i3.SRef(name="fp_waveguide", reference=fp_waveguide, flatten=True)
            insts += i3.SRef(name="fp_linear_taper_in", reference=fp_linear_taper, flatten=True)
            insts += i3.SRef(name="fp_linear_taper_out", reference=fp_linear_taper, flatten=True)
            insts += i3.SRef(name="bus_waveguide_1", reference=bus_waveguide, flatten=True)
            insts += i3.SRef(name="bus_waveguide_2", reference=bus_waveguide, flatten=True, transformation=i3.VMirror())
            insts += i3.SRef(name="BG_in", reference=BG, flatten=True)
            insts += i3.SRef(name="BG_out", reference=BG, flatten=True)

            return i3.place_and_route(
                insts=insts,
                specs=[
                    i3.Place("fp_waveguide", (0, 0)),
                    i3.Place("fp_linear_taper_in", (0, 0), angle=180, relative_to="fp_waveguide:in0"),
                    i3.Place("fp_linear_taper_out", (0, 0), angle=0, relative_to="fp_waveguide:out0"),
                    i3.Place("BG_in:out", (0,0), relative_to="fp_linear_taper_in:out0"),
                    i3.Place("BG_out:out", (0, 0), relative_to="fp_linear_taper_out:out0", angle=180),
                    i3.Place("bus_waveguide_1", (self.fp_length/2, -self.fp_width - self.coupler_gap), angle=-180),
                    i3.Place("bus_waveguide_2", (0,0), relative_to="bus_waveguide_1:in0"),
                    ]
            )

        def _generate_ports(self, ports):
            return i3.expose_ports(
                self.instances,
                {
                    "bus_waveguide_1:out0": "in0",
                    "bus_waveguide_2:out0": "out0",
                },
            )

class FP_BG_4(i3.PCell):
    fp_waveguide = i3.ChildCellProperty(doc="fabry perot waveguide")
    fp_linear_taper = i3.ChildCellProperty(doc="linear taper")
    bus_waveguide = i3.ChildCellProperty(doc="bus_waveguide")
    BG = i3.ChildCellProperty(doc="bragg grating")

    def _default_fp_waveguide(self):
        return pdk.Straight()

    def _default_fp_linear_taper(self):
        return pdk.Taper()

    def _default_bus_waveguide(self):
        return pdk.Sbend()

    def _default_BG(self):
        return BG_4()

    class Layout(i3.LayoutView):
        fp_width = i3.PositiveNumberProperty(default=1.0, doc="width of fabry perot waveguide")
        fp_length = i3.PositiveNumberProperty(default=150.0, doc="length of fabry perot waveguide")
        end_fp_taper_width = i3.PositiveNumberProperty(default=0.5, doc="width of end fp taper port")
        fp_taper_length = i3.PositiveNumberProperty(default=50.0, doc="length of fp taper")
        coupler_gap = i3.PositiveNumberProperty(default=2.0, doc="coupling gap between sbend and fp waveguide")

        def _default_fp_waveguide(self):
            cell = self.cell.fp_waveguide
            lv = cell.get_default_view(self)
            lv.set(
                width=self.fp_width,
                length=self.fp_length,
            )
            return lv

        def _default_end_fp_taper_width(self):
            return BG_4_width_2[len(array_4)-1]

        print("BG_4:{}".format(BG_4_width_2[len(array_4) - 1]))

        def _default_fp_linear_taper(self):
            cell = self.cell.fp_linear_taper
            lv = cell.get_default_view(self)
            lv.set(
                in_width=self.fp_width,
                out_width=self.end_fp_taper_width,
                length=self.fp_taper_length,
            )
            return lv

        def _default_bus_waveguide(self):
            cell = self.cell.bus_waveguide
            lv = cell.get_default_view(self)
            lv.set(
                width=self.fp_width,
            )
            return lv

        def _generate_instances(self, insts):
            fp_waveguide = self.fp_waveguide
            fp_linear_taper = self.fp_linear_taper
            bus_waveguide = self.bus_waveguide
            BG = self.BG

            insts += i3.SRef(name="fp_waveguide", reference=fp_waveguide, flatten=True)
            insts += i3.SRef(name="fp_linear_taper_in", reference=fp_linear_taper, flatten=True)
            insts += i3.SRef(name="fp_linear_taper_out", reference=fp_linear_taper, flatten=True)
            insts += i3.SRef(name="bus_waveguide_1", reference=bus_waveguide, flatten=True)
            insts += i3.SRef(name="bus_waveguide_2", reference=bus_waveguide, flatten=True, transformation=i3.VMirror())
            insts += i3.SRef(name="BG_in", reference=BG, flatten=True)
            insts += i3.SRef(name="BG_out", reference=BG, flatten=True)

            return i3.place_and_route(
                insts=insts,
                specs=[
                    i3.Place("fp_waveguide", (0, 0)),
                    i3.Place("fp_linear_taper_in", (0, 0), angle=180, relative_to="fp_waveguide:in0"),
                    i3.Place("fp_linear_taper_out", (0, 0), angle=0, relative_to="fp_waveguide:out0"),
                    i3.Place("BG_in:out", (0,0), relative_to="fp_linear_taper_in:out0"),
                    i3.Place("BG_out:out", (0, 0), relative_to="fp_linear_taper_out:out0", angle=180),
                    i3.Place("bus_waveguide_1", (self.fp_length/2, -self.fp_width - self.coupler_gap), angle=-180),
                    i3.Place("bus_waveguide_2", (0,0), relative_to="bus_waveguide_1:in0"),
                    ]
            )

        def _generate_ports(self, ports):
            return i3.expose_ports(
                self.instances,
                {
                    "bus_waveguide_1:out0": "in0",
                    "bus_waveguide_2:out0": "out0",
                },
            )

class FP_BG_5(i3.PCell):
    fp_waveguide = i3.ChildCellProperty(doc="fabry perot waveguide")
    fp_linear_taper = i3.ChildCellProperty(doc="linear taper")
    bus_waveguide = i3.ChildCellProperty(doc="bus_waveguide")
    BG = i3.ChildCellProperty(doc="bragg grating")

    def _default_fp_waveguide(self):
        return pdk.Straight()

    def _default_fp_linear_taper(self):
        return pdk.Taper()

    def _default_bus_waveguide(self):
        return pdk.Sbend()

    def _default_BG(self):
        return BG_5()

    class Layout(i3.LayoutView):
        fp_width = i3.PositiveNumberProperty(default=1.0, doc="width of fabry perot waveguide")
        fp_length = i3.PositiveNumberProperty(default=150.0, doc="length of fabry perot waveguide")
        end_fp_taper_width = i3.PositiveNumberProperty(default=0.5, doc="width of end fp taper port")
        fp_taper_length = i3.PositiveNumberProperty(default=50.0, doc="length of fp taper")
        coupler_gap = i3.PositiveNumberProperty(default=2.0, doc="coupling gap between sbend and fp waveguide")

        def _default_fp_waveguide(self):
            cell = self.cell.fp_waveguide
            lv = cell.get_default_view(self)
            lv.set(
                width=self.fp_width,
                length=self.fp_length,
            )
            return lv

        def _default_end_fp_taper_width(self):
            return BG_5_width_2[len(array_5)-1]

        print("BG_5:{}".format(BG_5_width_2[len(array_5) - 1]))

        def _default_fp_linear_taper(self):
            cell = self.cell.fp_linear_taper
            lv = cell.get_default_view(self)
            lv.set(
                in_width=self.fp_width,
                out_width=self.end_fp_taper_width,
                length=self.fp_taper_length,
            )
            return lv

        def _default_bus_waveguide(self):
            cell = self.cell.bus_waveguide
            lv = cell.get_default_view(self)
            lv.set(
                width=self.fp_width,
            )
            return lv

        def _generate_instances(self, insts):
            fp_waveguide = self.fp_waveguide
            fp_linear_taper = self.fp_linear_taper
            bus_waveguide = self.bus_waveguide
            BG = self.BG

            insts += i3.SRef(name="fp_waveguide", reference=fp_waveguide, flatten=True)
            insts += i3.SRef(name="fp_linear_taper_in", reference=fp_linear_taper, flatten=True)
            insts += i3.SRef(name="fp_linear_taper_out", reference=fp_linear_taper, flatten=True)
            insts += i3.SRef(name="bus_waveguide_1", reference=bus_waveguide, flatten=True)
            insts += i3.SRef(name="bus_waveguide_2", reference=bus_waveguide, flatten=True, transformation=i3.VMirror())
            insts += i3.SRef(name="BG_in", reference=BG, flatten=True)
            insts += i3.SRef(name="BG_out", reference=BG, flatten=True)

            return i3.place_and_route(
                insts=insts,
                specs=[
                    i3.Place("fp_waveguide", (0, 0)),
                    i3.Place("fp_linear_taper_in", (0, 0), angle=180, relative_to="fp_waveguide:in0"),
                    i3.Place("fp_linear_taper_out", (0, 0), angle=0, relative_to="fp_waveguide:out0"),
                    i3.Place("BG_in:out", (0,0), relative_to="fp_linear_taper_in:out0"),
                    i3.Place("BG_out:out", (0, 0), relative_to="fp_linear_taper_out:out0", angle=180),
                    i3.Place("bus_waveguide_1", (self.fp_length/2, -self.fp_width - self.coupler_gap), angle=-180),
                    i3.Place("bus_waveguide_2", (0,0), relative_to="bus_waveguide_1:in0"),
                    ]
            )

        def _generate_ports(self, ports):
            return i3.expose_ports(
                self.instances,
                {
                    "bus_waveguide_1:out0": "in0",
                    "bus_waveguide_2:out0": "out0",
                },
            )

class FP_BG_6(i3.PCell):
    fp_waveguide = i3.ChildCellProperty(doc="fabry perot waveguide")
    fp_linear_taper = i3.ChildCellProperty(doc="linear taper")
    bus_waveguide = i3.ChildCellProperty(doc="bus_waveguide")
    BG = i3.ChildCellProperty(doc="bragg grating")

    def _default_fp_waveguide(self):
        return pdk.Straight()

    def _default_fp_linear_taper(self):
        return pdk.Taper()

    def _default_bus_waveguide(self):
        return pdk.Sbend()

    def _default_BG(self):
        return BG_6()

    class Layout(i3.LayoutView):
        fp_width = i3.PositiveNumberProperty(default=1.0, doc="width of fabry perot waveguide")
        fp_length = i3.PositiveNumberProperty(default=150.0, doc="length of fabry perot waveguide")
        end_fp_taper_width = i3.PositiveNumberProperty(default=0.5, doc="width of end fp taper port")
        fp_taper_length = i3.PositiveNumberProperty(default=50.0, doc="length of fp taper")
        coupler_gap = i3.PositiveNumberProperty(default=2.0, doc="coupling gap between sbend and fp waveguide")

        def _default_fp_waveguide(self):
            cell = self.cell.fp_waveguide
            lv = cell.get_default_view(self)
            lv.set(
                width=self.fp_width,
                length=self.fp_length,
            )
            return lv

        def _default_end_fp_taper_width(self):
            return BG_6_width_2[len(array_6)-1]

        print("BG_6:{}".format(BG_6_width_2[len(array_6) - 1]))

        def _default_fp_linear_taper(self):
            cell = self.cell.fp_linear_taper
            lv = cell.get_default_view(self)
            lv.set(
                in_width=self.fp_width,
                out_width=self.end_fp_taper_width,
                length=self.fp_taper_length,
            )
            return lv

        def _default_bus_waveguide(self):
            cell = self.cell.bus_waveguide
            lv = cell.get_default_view(self)
            lv.set(
                width=self.fp_width,
            )
            return lv

        def _generate_instances(self, insts):
            fp_waveguide = self.fp_waveguide
            fp_linear_taper = self.fp_linear_taper
            bus_waveguide = self.bus_waveguide
            BG = self.BG

            insts += i3.SRef(name="fp_waveguide", reference=fp_waveguide, flatten=True)
            insts += i3.SRef(name="fp_linear_taper_in", reference=fp_linear_taper, flatten=True)
            insts += i3.SRef(name="fp_linear_taper_out", reference=fp_linear_taper, flatten=True)
            insts += i3.SRef(name="bus_waveguide_1", reference=bus_waveguide, flatten=True)
            insts += i3.SRef(name="bus_waveguide_2", reference=bus_waveguide, flatten=True, transformation=i3.VMirror())
            insts += i3.SRef(name="BG_in", reference=BG, flatten=True)
            insts += i3.SRef(name="BG_out", reference=BG, flatten=True)

            return i3.place_and_route(
                insts=insts,
                specs=[
                    i3.Place("fp_waveguide", (0, 0)),
                    i3.Place("fp_linear_taper_in", (0, 0), angle=180, relative_to="fp_waveguide:in0"),
                    i3.Place("fp_linear_taper_out", (0, 0), angle=0, relative_to="fp_waveguide:out0"),
                    i3.Place("BG_in:out", (0,0), relative_to="fp_linear_taper_in:out0"),
                    i3.Place("BG_out:out", (0, 0), relative_to="fp_linear_taper_out:out0", angle=180),
                    i3.Place("bus_waveguide_1", (self.fp_length/2, -self.fp_width - self.coupler_gap), angle=-180),
                    i3.Place("bus_waveguide_2", (0,0), relative_to="bus_waveguide_1:in0"),
                    ]
            )

        def _generate_ports(self, ports):
            return i3.expose_ports(
                self.instances,
                {
                    "bus_waveguide_1:out0": "in0",
                    "bus_waveguide_2:out0": "out0",
                },
            )

class FP_BG_7(i3.PCell):
    fp_waveguide = i3.ChildCellProperty(doc="fabry perot waveguide")
    fp_linear_taper = i3.ChildCellProperty(doc="linear taper")
    bus_waveguide = i3.ChildCellProperty(doc="bus_waveguide")
    BG = i3.ChildCellProperty(doc="bragg grating")

    def _default_fp_waveguide(self):
        return pdk.Straight()

    def _default_fp_linear_taper(self):
        return pdk.Taper()

    def _default_bus_waveguide(self):
        return pdk.Sbend()

    def _default_BG(self):
        return BG_7()

    class Layout(i3.LayoutView):
        fp_width = i3.PositiveNumberProperty(default=1.0, doc="width of fabry perot waveguide")
        fp_length = i3.PositiveNumberProperty(default=150.0, doc="length of fabry perot waveguide")
        end_fp_taper_width = i3.PositiveNumberProperty(default=0.5, doc="width of end fp taper port")
        fp_taper_length = i3.PositiveNumberProperty(default=50.0, doc="length of fp taper")
        coupler_gap = i3.PositiveNumberProperty(default=2.0, doc="coupling gap between sbend and fp waveguide")

        def _default_fp_waveguide(self):
            cell = self.cell.fp_waveguide
            lv = cell.get_default_view(self)
            lv.set(
                width=self.fp_width,
                length=self.fp_length,
            )
            return lv

        def _default_end_fp_taper_width(self):
            return BG_7_width_2[len(array_7)-1]

        print("BG_7:{}".format(BG_7_width_2[len(array_7) - 1]))

        def _default_fp_linear_taper(self):
            cell = self.cell.fp_linear_taper
            lv = cell.get_default_view(self)
            lv.set(
                in_width=self.fp_width,
                out_width=self.end_fp_taper_width,
                length=self.fp_taper_length,
            )
            return lv

        def _default_bus_waveguide(self):
            cell = self.cell.bus_waveguide
            lv = cell.get_default_view(self)
            lv.set(
                width=self.fp_width,
            )
            return lv

        def _generate_instances(self, insts):
            fp_waveguide = self.fp_waveguide
            fp_linear_taper = self.fp_linear_taper
            bus_waveguide = self.bus_waveguide
            BG = self.BG

            insts += i3.SRef(name="fp_waveguide", reference=fp_waveguide, flatten=True)
            insts += i3.SRef(name="fp_linear_taper_in", reference=fp_linear_taper, flatten=True)
            insts += i3.SRef(name="fp_linear_taper_out", reference=fp_linear_taper, flatten=True)
            insts += i3.SRef(name="bus_waveguide_1", reference=bus_waveguide, flatten=True)
            insts += i3.SRef(name="bus_waveguide_2", reference=bus_waveguide, flatten=True, transformation=i3.VMirror())
            insts += i3.SRef(name="BG_in", reference=BG, flatten=True)
            insts += i3.SRef(name="BG_out", reference=BG, flatten=True)

            return i3.place_and_route(
                insts=insts,
                specs=[
                    i3.Place("fp_waveguide", (0, 0)),
                    i3.Place("fp_linear_taper_in", (0, 0), angle=180, relative_to="fp_waveguide:in0"),
                    i3.Place("fp_linear_taper_out", (0, 0), angle=0, relative_to="fp_waveguide:out0"),
                    i3.Place("BG_in:out", (0,0), relative_to="fp_linear_taper_in:out0"),
                    i3.Place("BG_out:out", (0, 0), relative_to="fp_linear_taper_out:out0", angle=180),
                    i3.Place("bus_waveguide_1", (self.fp_length/2, -self.fp_width - self.coupler_gap), angle=-180),
                    i3.Place("bus_waveguide_2", (0,0), relative_to="bus_waveguide_1:in0"),
                    ]
            )

        def _generate_ports(self, ports):
            return i3.expose_ports(
                self.instances,
                {
                    "bus_waveguide_1:out0": "in0",
                    "bus_waveguide_2:out0": "out0",
                },
            )

class FP_BG_8(i3.PCell):
    fp_waveguide = i3.ChildCellProperty(doc="fabry perot waveguide")
    fp_linear_taper = i3.ChildCellProperty(doc="linear taper")
    bus_waveguide = i3.ChildCellProperty(doc="bus_waveguide")
    BG = i3.ChildCellProperty(doc="bragg grating")

    def _default_fp_waveguide(self):
        return pdk.Straight()

    def _default_fp_linear_taper(self):
        return pdk.Taper()

    def _default_bus_waveguide(self):
        return pdk.Sbend()

    def _default_BG(self):
        return BG_8()

    class Layout(i3.LayoutView):
        fp_width = i3.PositiveNumberProperty(default=1.0, doc="width of fabry perot waveguide")
        fp_length = i3.PositiveNumberProperty(default=150.0, doc="length of fabry perot waveguide")
        end_fp_taper_width = i3.PositiveNumberProperty(default=0.5, doc="width of end fp taper port")
        fp_taper_length = i3.PositiveNumberProperty(default=50.0, doc="length of fp taper")
        coupler_gap = i3.PositiveNumberProperty(default=2.0, doc="coupling gap between sbend and fp waveguide")

        def _default_fp_waveguide(self):
            cell = self.cell.fp_waveguide
            lv = cell.get_default_view(self)
            lv.set(
                width=self.fp_width,
                length=self.fp_length,
            )
            return lv

        def _default_end_fp_taper_width(self):
            return BG_8_width_2[len(array_8)-1]

        print("BG_8:{}".format(BG_8_width_2[len(array_8) - 1]))

        def _default_fp_linear_taper(self):
            cell = self.cell.fp_linear_taper
            lv = cell.get_default_view(self)
            lv.set(
                in_width=self.fp_width,
                out_width=self.end_fp_taper_width,
                length=self.fp_taper_length,
            )
            return lv

        def _default_bus_waveguide(self):
            cell = self.cell.bus_waveguide
            lv = cell.get_default_view(self)
            lv.set(
                width=self.fp_width,
            )
            return lv

        def _generate_instances(self, insts):
            fp_waveguide = self.fp_waveguide
            fp_linear_taper = self.fp_linear_taper
            bus_waveguide = self.bus_waveguide
            BG = self.BG

            insts += i3.SRef(name="fp_waveguide", reference=fp_waveguide, flatten=True)
            insts += i3.SRef(name="fp_linear_taper_in", reference=fp_linear_taper, flatten=True)
            insts += i3.SRef(name="fp_linear_taper_out", reference=fp_linear_taper, flatten=True)
            insts += i3.SRef(name="bus_waveguide_1", reference=bus_waveguide, flatten=True)
            insts += i3.SRef(name="bus_waveguide_2", reference=bus_waveguide, flatten=True, transformation=i3.VMirror())
            insts += i3.SRef(name="BG_in", reference=BG, flatten=True)
            insts += i3.SRef(name="BG_out", reference=BG, flatten=True)

            return i3.place_and_route(
                insts=insts,
                specs=[
                    i3.Place("fp_waveguide", (0, 0)),
                    i3.Place("fp_linear_taper_in", (0, 0), angle=180, relative_to="fp_waveguide:in0"),
                    i3.Place("fp_linear_taper_out", (0, 0), angle=0, relative_to="fp_waveguide:out0"),
                    i3.Place("BG_in:out", (0,0), relative_to="fp_linear_taper_in:out0"),
                    i3.Place("BG_out:out", (0, 0), relative_to="fp_linear_taper_out:out0", angle=180),
                    i3.Place("bus_waveguide_1", (self.fp_length/2, -self.fp_width - self.coupler_gap), angle=-180),
                    i3.Place("bus_waveguide_2", (0,0), relative_to="bus_waveguide_1:in0"),
                    ]
            )

        def _generate_ports(self, ports):
            return i3.expose_ports(
                self.instances,
                {
                    "bus_waveguide_1:out0": "in0",
                    "bus_waveguide_2:out0": "out0",
                },
            )

class FP_BG_9(i3.PCell):
    fp_waveguide = i3.ChildCellProperty(doc="fabry perot waveguide")
    fp_linear_taper = i3.ChildCellProperty(doc="linear taper")
    bus_waveguide = i3.ChildCellProperty(doc="bus_waveguide")
    BG = i3.ChildCellProperty(doc="bragg grating")

    def _default_fp_waveguide(self):
        return pdk.Straight()

    def _default_fp_linear_taper(self):
        return pdk.Taper()

    def _default_bus_waveguide(self):
        return pdk.Sbend()

    def _default_BG(self):
        return BG_9()

    class Layout(i3.LayoutView):
        fp_width = i3.PositiveNumberProperty(default=1.0, doc="width of fabry perot waveguide")
        fp_length = i3.PositiveNumberProperty(default=150.0, doc="length of fabry perot waveguide")
        end_fp_taper_width = i3.PositiveNumberProperty(default=0.5, doc="width of end fp taper port")
        fp_taper_length = i3.PositiveNumberProperty(default=50.0, doc="length of fp taper")
        coupler_gap = i3.PositiveNumberProperty(default=2.0, doc="coupling gap between sbend and fp waveguide")

        def _default_fp_waveguide(self):
            cell = self.cell.fp_waveguide
            lv = cell.get_default_view(self)
            lv.set(
                width=self.fp_width,
                length=self.fp_length,
            )
            return lv

        def _default_end_fp_taper_width(self):
            return BG_9_width_2[len(array_9)-1]

        print("BG_9:{}".format(BG_9_width_2[len(array_9) - 1]))

        def _default_fp_linear_taper(self):
            cell = self.cell.fp_linear_taper
            lv = cell.get_default_view(self)
            lv.set(
                in_width=self.fp_width,
                out_width=self.end_fp_taper_width,
                length=self.fp_taper_length,
            )
            return lv

        def _default_bus_waveguide(self):
            cell = self.cell.bus_waveguide
            lv = cell.get_default_view(self)
            lv.set(
                width=self.fp_width,
            )
            return lv

        def _generate_instances(self, insts):
            fp_waveguide = self.fp_waveguide
            fp_linear_taper = self.fp_linear_taper
            bus_waveguide = self.bus_waveguide
            BG = self.BG

            insts += i3.SRef(name="fp_waveguide", reference=fp_waveguide, flatten=True)
            insts += i3.SRef(name="fp_linear_taper_in", reference=fp_linear_taper, flatten=True)
            insts += i3.SRef(name="fp_linear_taper_out", reference=fp_linear_taper, flatten=True)
            insts += i3.SRef(name="bus_waveguide_1", reference=bus_waveguide, flatten=True)
            insts += i3.SRef(name="bus_waveguide_2", reference=bus_waveguide, flatten=True, transformation=i3.VMirror())
            insts += i3.SRef(name="BG_in", reference=BG, flatten=True)
            insts += i3.SRef(name="BG_out", reference=BG, flatten=True)

            return i3.place_and_route(
                insts=insts,
                specs=[
                    i3.Place("fp_waveguide", (0, 0)),
                    i3.Place("fp_linear_taper_in", (0, 0), angle=180, relative_to="fp_waveguide:in0"),
                    i3.Place("fp_linear_taper_out", (0, 0), angle=0, relative_to="fp_waveguide:out0"),
                    i3.Place("BG_in:out", (0,0), relative_to="fp_linear_taper_in:out0"),
                    i3.Place("BG_out:out", (0, 0), relative_to="fp_linear_taper_out:out0", angle=180),
                    i3.Place("bus_waveguide_1", (self.fp_length/2, -self.fp_width - self.coupler_gap), angle=-180),
                    i3.Place("bus_waveguide_2", (0,0), relative_to="bus_waveguide_1:in0"),
                    ]
            )

        def _generate_ports(self, ports):
            return i3.expose_ports(
                self.instances,
                {
                    "bus_waveguide_1:out0": "in0",
                    "bus_waveguide_2:out0": "out0",
                },
            )

class SinusoidalGrating(i3.PCell):
    class Layout(i3.LayoutView):
        period = i3.PositiveNumberProperty(default=0.475, doc="Grating period (um)")
        n_periods = i3.PositiveIntProperty(default=100, doc="Number of periods")
        w_min = i3.PositiveNumberProperty(default=0.3, doc="Minimum waveguide width (µm)")
        w_max = i3.PositiveNumberProperty(default=0.9, doc="Maximum waveguide width (µm)")

        def _default_name(self):
            return "sinusoidal_grating"

        def _generate_elements(self, elems):
            # Generate sinusoidal edge
            length = self.period * self.n_periods
            z = np.linspace(0, length, 2000)  # higher resolution for smooth edges

            w_base = 0.5 * (self.w_max + self.w_min)
            delta_w = 0.5 * (self.w_max - self.w_min)

            # --- Compute sinusoidal width along z ---
            w_z = w_base + delta_w * np.sin(2 * np.pi * z / self.period)

            y_top = +w_z / 2.0
            y_bot = -w_z / 2.0

            # --- Construct polygon ---
            top_pts = [(zi, yi) for zi, yi in zip(z, y_top)]
            bot_pts = [(zi, yi) for zi, yi in zip(z[::-1], y_bot[::-1])]
            shape = i3.Shape(points=top_pts + bot_pts)

            elems += i3.Boundary(shape=shape, layer=i3.TECH.PPLAYER.X1P)
            return elems
        def _generate_ports(self, ports):
            total_length = self.period * self.n_periods
            ports += i3.OpticalPort(name="in", position=(0.0, 0.0), angle=180.0)
            ports += i3.OpticalPort(name="out", position=(total_length, 0.0), angle=0.0)
            return ports

class SinusoidalGratingTaper(i3.PCell):
    class Layout(i3.LayoutView):
        period = i3.PositiveNumberProperty(default=0.475, doc="Grating period (um)")
        n_periods = i3.PositiveIntProperty(default=100, doc="Number of periods")
        n_fade = i3.PositiveIntProperty(default=100, doc="Number of periods to fade out")
        w_min = i3.PositiveNumberProperty(default=0.3, doc="Minimum waveguide width (µm)")
        w_max = i3.PositiveNumberProperty(default=0.9, doc="Maximum waveguide width (µm)")

        def _default_name(self):
            return "sinusoidal_grating_taper"

        def _generate_elements(self, elems):

            total_length = self.period * self.n_periods
            fade_length = self.n_fade * self.period
            z = np.linspace(0, total_length, 2000)

            w_base = 0.5 * (self.w_max + self.w_min)
            A0 = 0.5 * (self.w_max - self.w_min)

            # --- Envelope function ---
            A_z = np.zeros_like(z)
            for i, zi in enumerate(z):
                if zi < fade_length:  # Fade-in
                    A_z[i] = A0 * (zi / fade_length)
                elif zi > (total_length - fade_length):  # Fade-out
                    A_z[i] = A0 * (1 - (zi - (total_length - fade_length)) / fade_length)
                else:  # Full modulation
                    A_z[i] = A0

            # --- Modulated width ---
            W_z = w_base + A_z * np.sin(2 * np.pi * z / self.period)

            y_top = +W_z / 2.0
            y_bot = -W_z / 2.0

            top_pts = [(zi, yi) for zi, yi in zip(z, y_top)]
            bot_pts = [(zi, yi) for zi, yi in zip(z[::-1], y_bot[::-1])]
            shape = i3.Shape(points=top_pts + bot_pts)

            elems += i3.Boundary(shape=shape, layer=i3.TECH.PPLAYER.X1P)
            return elems

        def _generate_ports(self, ports):
            total_length = self.period * self.n_periods
            ports += i3.OpticalPort(name="in", position=(0.0, 0.0), angle=180.0)
            ports += i3.OpticalPort(name="out", position=(total_length, 0.0), angle=0.0)
            return ports

class Sinusoidal_BG(i3.PCell):
    fp_waveguide = i3.ChildCellProperty(doc="fabry perot waveguide")
    fp_linear_taper = i3.ChildCellProperty(doc="linear taper")
    bus_waveguide = i3.ChildCellProperty(doc="bus_waveguide")
    BG = i3.ChildCellProperty(doc="bragg grating")
    BG_Taper = i3.ChildCellProperty(doc="bragg grating taper")

    def _default_fp_waveguide(self):
        return pdk.Straight()

    def _default_fp_linear_taper(self):
        return pdk.Taper()

    def _default_bus_waveguide(self):
        return pdk.Sbend()

    def _default_BG(self):
        return SinusoidalGrating()

    def _default_BG_Taper(self):
        return SinusoidalGratingTaper()

    class Layout(i3.LayoutView):
        fp_width = i3.PositiveNumberProperty(default=1.0, doc="width of fabry perot waveguide")
        fp_length = i3.PositiveNumberProperty(default=150.0, doc="length of fabry perot waveguide")
        end_fp_taper_width = i3.PositiveNumberProperty(default=0.5, doc="width of end fp taper port")
        fp_taper_length = i3.PositiveNumberProperty(default=200.0, doc="length of fp taper")
        coupler_gap = i3.PositiveNumberProperty(default=2.0, doc="coupling gap between sbend and fp waveguide")

        def _default_fp_waveguide(self):
            cell = self.cell.fp_waveguide
            lv = cell.get_default_view(self)
            lv.set(
                width=self.fp_width,
                length=self.fp_length,
            )
            return lv

        def _default_end_fp_taper_width(self):
            return 0.6

        # print("BG_8:{}".format(BG_8_width_2[len(array_8) - 1]))

        def _default_fp_linear_taper(self):
            cell = self.cell.fp_linear_taper
            lv = cell.get_default_view(self)
            lv.set(
                in_width=self.fp_width,
                out_width=self.end_fp_taper_width,
                length=self.fp_taper_length,
            )
            return lv

        def _default_bus_waveguide(self):
            cell = self.cell.bus_waveguide
            lv = cell.get_default_view(self)
            lv.set(
                width=self.fp_width,
            )
            return lv

        def _generate_instances(self, insts):
            fp_waveguide = self.fp_waveguide
            fp_linear_taper = self.fp_linear_taper
            bus_waveguide = self.bus_waveguide
            BG = self.BG
            BG_Taper = self.BG_Taper

            insts += i3.SRef(name="fp_waveguide", reference=fp_waveguide, flatten=True)
            insts += i3.SRef(name="fp_linear_taper_in", reference=fp_linear_taper, flatten=True)
            insts += i3.SRef(name="fp_linear_taper_out", reference=fp_linear_taper, flatten=True)
            insts += i3.SRef(name="bus_waveguide_1", reference=bus_waveguide, flatten=True)
            insts += i3.SRef(name="bus_waveguide_2", reference=bus_waveguide, flatten=True, transformation=i3.VMirror())
            insts += i3.SRef(name="BG_Taper_in_1", reference=BG_Taper, flatten=True)
            insts += i3.SRef(name="BG_Taper_out_1", reference=BG_Taper, flatten=True)
            insts += i3.SRef(name="BG_Taper_in_2", reference=BG_Taper, flatten=True)
            insts += i3.SRef(name="BG_Taper_out_2", reference=BG_Taper, flatten=True)
            #
            insts += i3.SRef(name="BG_in", reference=BG, flatten=True)
            insts += i3.SRef(name="BG_out", reference=BG, flatten=True)

            return i3.place_and_route(
                insts=insts,
                specs=[
                    i3.Place("fp_waveguide", (0, 0)),
                    i3.Place("fp_linear_taper_in", (0, 0), angle=180, relative_to="fp_waveguide:in0"),
                    i3.Place("fp_linear_taper_out", (0, 0), angle=0, relative_to="fp_waveguide:out0"),
                    i3.Place("BG_Taper_in_1", (0,0), relative_to="fp_linear_taper_in:out0"),
                    i3.FlipH("BG_Taper_in_1"),
                    i3.Place("BG_Taper_in_2", (0,0), relative_to="fp_linear_taper_out:out0"),
                    i3.Place("BG_in", (0, 0), relative_to="BG_Taper_in_1:out"),
                    i3.FlipH("BG_in"),
                    i3.Place("BG_out", (0, 0), relative_to="BG_Taper_in_2:out"),
                    i3.Place("BG_Taper_out_1:out", (0.475/2, 0), relative_to="BG_in:out"),
                    # i3.FlipH("BG_Taper_out_1"),
                    i3.Place("BG_Taper_out_2:out", (-0.475/2, 0), relative_to="BG_out:out"),
                    i3.FlipH("BG_Taper_out_2"),
                    i3.Place("bus_waveguide_1", (self.fp_length/2, -self.fp_width - self.coupler_gap), angle=-180),
                    i3.Place("bus_waveguide_2", (0,0), relative_to="bus_waveguide_1:in0"),
                    ]
            )

        def _generate_ports(self, ports):
            return i3.expose_ports(
                self.instances,
                {
                    "bus_waveguide_1:out0": "in0",
                    "bus_waveguide_2:out0": "out0",
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







