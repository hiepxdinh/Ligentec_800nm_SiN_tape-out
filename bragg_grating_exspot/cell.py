import ligentec_an800.all as pdk

import ipkiss3.all as i3

from Bragg_grating import FP_BG_1, FP_BG_2, FP_BG_3, FP_BG_4, FP_BG_5, FP_BG_6, FP_BG_7, FP_BG_8, Sinusoidal_BG

class FP_BG_1_Exspot(i3.Circuit):

    edge_coupler = i3.ChildCellProperty(doc="edge coupler")
    linear_taper = i3.ChildCellProperty(doc="linear taper")
    fp_grating = i3.ChildCellProperty(doc="fp grating")
    device_length = i3.PositiveNumberProperty(default=10500, doc="width of input waveguide")

    def _default_edge_coupler(self):
        return pdk.AN800BB_ExSpot_SMF_C()

    def _default_linear_taper(self):
        return pdk.Taper()

    def _default_fp_grating(self):
        return FP_BG_1()

    def _default_insts(self):
        return {
                "in_coupler": self.edge_coupler,
                "out_coupler": self.edge_coupler,
                "linear_taper_in": self.linear_taper,
                "linear_taper_out": self.linear_taper,
                "fp_grating":self.fp_grating,
                }

    def _default_specs(self):
        return[
            i3.Place("fp_grating", (0,0)),
            i3.Place("in_coupler", position=(-self.device_length/2+620+55, 0.0), angle=180, relative_to="fp_grating:in0"),
            i3.Place("out_coupler", position=(self.device_length/2-620-55, 0.0), angle=0, relative_to="fp_grating:out0"),

            i3.Place("linear_taper_in", position=(115, 0), relative_to="in_coupler:in0"),
            i3.FlipH("linear_taper_in"),
            i3.Place("linear_taper_out", position=(-115, 0), angle=0, relative_to="out_coupler:in0"),

            i3.ConnectBend("linear_taper_in:out0", "in_coupler:in0"),
            i3.ConnectBend("linear_taper_out:out0", "out_coupler:in0"),
            i3.ConnectBend("linear_taper_in:in0", "fp_grating:in0"),
            i3.ConnectBend("linear_taper_out:in0", "fp_grating:out0")

        ]

    class Layout(i3.Circuit.Layout):
        fp_width = i3.PositiveNumberProperty(default=1.0, doc="width of fp waveguide")
        fp_length= i3.PositiveNumberProperty(default=1.0, doc="length of fp waveguide")
        width_out = i3.PositiveNumberProperty(default=1.0, doc="width of output waveguide")
        coupler_gap = i3.PositiveNumberProperty(default=1.0, doc="coupling gap between sbend and fp waveguide")
        linear_taper_length = i3.PositiveNumberProperty(default=100, doc="length of linear taper")

        def _default_fp_grating(self):
            cell = self.cell.fp_grating
            lv = cell.get_default_view(self)
            lv.set(
                fp_width=self.fp_width,
                fp_length=self.fp_length,
                coupler_gap=self.coupler_gap,
            )
            return lv

        def _default_linear_taper(self):
            cell = self.cell.linear_taper
            lv = cell.get_default_view(self)
            lv.set(
                in_width=self.fp_width,
                out_width=self.width_out,
                length=self.linear_taper_length
            )
            return lv

class FP_BG_2_Exspot(i3.Circuit):

    edge_coupler = i3.ChildCellProperty(doc="edge coupler")
    linear_taper = i3.ChildCellProperty(doc="linear taper")
    fp_grating = i3.ChildCellProperty(doc="fp grating")
    device_length = i3.PositiveNumberProperty(default=10500, doc="width of input waveguide")

    def _default_edge_coupler(self):
        return pdk.AN800BB_ExSpot_SMF_C()

    def _default_linear_taper(self):
        return pdk.Taper()

    def _default_fp_grating(self):
        return FP_BG_2()

    def _default_insts(self):
        return {
                "in_coupler": self.edge_coupler,
                "out_coupler": self.edge_coupler,
                "linear_taper_in": self.linear_taper,
                "linear_taper_out": self.linear_taper,
                "fp_grating":self.fp_grating,
                }

    def _default_specs(self):
        return[
            i3.Place("fp_grating", (0,0)),

            i3.Place("in_coupler", position=(-self.device_length/2+620+55, 0.0), angle=180, relative_to="fp_grating:in0"),
            i3.Place("out_coupler", position=(self.device_length/2-620-55, 0.0), angle=0, relative_to="fp_grating:out0"),

            i3.Place("linear_taper_in", position=(115, 0), relative_to="in_coupler:in0"),
            i3.FlipH("linear_taper_in"),
            i3.Place("linear_taper_out", position=(-115, 0), angle=0, relative_to="out_coupler:in0"),

            i3.ConnectBend("linear_taper_in:out0", "in_coupler:in0"),
            i3.ConnectBend("linear_taper_out:out0", "out_coupler:in0"),
            i3.ConnectBend("linear_taper_in:in0", "fp_grating:in0"),
            i3.ConnectBend("linear_taper_out:in0", "fp_grating:out0")

        ]

    class Layout(i3.Circuit.Layout):
        fp_width = i3.PositiveNumberProperty(default=1.0, doc="width of fp waveguide")
        fp_length= i3.PositiveNumberProperty(default=1.0, doc="length of fp waveguide")
        width_out = i3.PositiveNumberProperty(default=1.0, doc="width of output waveguide")
        coupler_gap = i3.PositiveNumberProperty(default=1.0, doc="coupling gap between sbend and fp waveguide")
        linear_taper_length = i3.PositiveNumberProperty(default=100, doc="length of linear taper")

        def _default_fp_grating(self):
            cell = self.cell.fp_grating
            lv = cell.get_default_view(self)
            lv.set(
                fp_width=self.fp_width,
                fp_length=self.fp_length,
                coupler_gap=self.coupler_gap,
            )
            return lv

        def _default_linear_taper(self):
            cell = self.cell.linear_taper
            lv = cell.get_default_view(self)
            lv.set(
                in_width=self.fp_width,
                out_width=self.width_out,
                length=self.linear_taper_length
            )
            return lv

class FP_BG_3_Exspot(i3.Circuit):

    edge_coupler = i3.ChildCellProperty(doc="edge coupler")
    linear_taper = i3.ChildCellProperty(doc="linear taper")
    fp_grating = i3.ChildCellProperty(doc="fp grating")
    device_length = i3.PositiveNumberProperty(default=10500, doc="width of input waveguide")

    def _default_edge_coupler(self):
        return pdk.AN800BB_ExSpot_SMF_C()

    def _default_linear_taper(self):
        return pdk.Taper()

    def _default_fp_grating(self):
        return FP_BG_3()

    def _default_insts(self):
        return {
                "in_coupler": self.edge_coupler,
                "out_coupler": self.edge_coupler,
                "linear_taper_in": self.linear_taper,
                "linear_taper_out": self.linear_taper,
                "fp_grating":self.fp_grating,
                }

    def _default_specs(self):
        return[
            i3.Place("fp_grating", (0,0)),

            i3.Place("in_coupler", position=(-self.device_length/2+620+55, 0.0), angle=180, relative_to="fp_grating:in0"),
            i3.Place("out_coupler", position=(self.device_length/2-620-55, 0.0), angle=0, relative_to="fp_grating:out0"),

            i3.Place("linear_taper_in", position=(115, 0), relative_to="in_coupler:in0"),
            i3.FlipH("linear_taper_in"),
            i3.Place("linear_taper_out", position=(-115, 0), angle=0, relative_to="out_coupler:in0"),

            i3.ConnectBend("linear_taper_in:out0", "in_coupler:in0"),
            i3.ConnectBend("linear_taper_out:out0", "out_coupler:in0"),
            i3.ConnectBend("linear_taper_in:in0", "fp_grating:in0"),
            i3.ConnectBend("linear_taper_out:in0", "fp_grating:out0")

        ]

    class Layout(i3.Circuit.Layout):
        fp_width = i3.PositiveNumberProperty(default=1.0, doc="width of fp waveguide")
        fp_length= i3.PositiveNumberProperty(default=1.0, doc="length of fp waveguide")
        width_out = i3.PositiveNumberProperty(default=1.0, doc="width of output waveguide")
        coupler_gap = i3.PositiveNumberProperty(default=1.0, doc="coupling gap between sbend and fp waveguide")
        linear_taper_length = i3.PositiveNumberProperty(default=100, doc="length of linear taper")

        def _default_fp_grating(self):
            cell = self.cell.fp_grating
            lv = cell.get_default_view(self)
            lv.set(
                fp_width=self.fp_width,
                fp_length=self.fp_length,
                coupler_gap=self.coupler_gap,
            )
            return lv

        def _default_linear_taper(self):
            cell = self.cell.linear_taper
            lv = cell.get_default_view(self)
            lv.set(
                in_width=self.fp_width,
                out_width=self.width_out,
                length=self.linear_taper_length
            )
            return lv

class FP_BG_4_Exspot(i3.Circuit):

    edge_coupler = i3.ChildCellProperty(doc="edge coupler")
    linear_taper = i3.ChildCellProperty(doc="linear taper")
    fp_grating = i3.ChildCellProperty(doc="fp grating")
    device_length = i3.PositiveNumberProperty(default=10500, doc="width of input waveguide")

    def _default_edge_coupler(self):
        return pdk.AN800BB_ExSpot_SMF_C()

    def _default_linear_taper(self):
        return pdk.Taper()

    def _default_fp_grating(self):
        return FP_BG_4()

    def _default_insts(self):
        return {
                "in_coupler": self.edge_coupler,
                "out_coupler": self.edge_coupler,
                "linear_taper_in": self.linear_taper,
                "linear_taper_out": self.linear_taper,
                "fp_grating":self.fp_grating,
                }

    def _default_specs(self):
        return[
            i3.Place("fp_grating", (0,0)),

            i3.Place("in_coupler", position=(-self.device_length/2+620+55, 0.0), angle=180, relative_to="fp_grating:in0"),
            i3.Place("out_coupler", position=(self.device_length/2-620-55, 0.0), angle=0, relative_to="fp_grating:out0"),

            i3.Place("linear_taper_in", position=(115, 0), relative_to="in_coupler:in0"),
            i3.FlipH("linear_taper_in"),
            i3.Place("linear_taper_out", position=(-115, 0), angle=0, relative_to="out_coupler:in0"),

            i3.ConnectBend("linear_taper_in:out0", "in_coupler:in0"),
            i3.ConnectBend("linear_taper_out:out0", "out_coupler:in0"),
            i3.ConnectBend("linear_taper_in:in0", "fp_grating:in0"),
            i3.ConnectBend("linear_taper_out:in0", "fp_grating:out0")

        ]

    class Layout(i3.Circuit.Layout):
        fp_width = i3.PositiveNumberProperty(default=1.0, doc="width of fp waveguide")
        fp_length= i3.PositiveNumberProperty(default=1.0, doc="length of fp waveguide")
        width_out = i3.PositiveNumberProperty(default=1.0, doc="width of output waveguide")
        coupler_gap = i3.PositiveNumberProperty(default=1.0, doc="coupling gap between sbend and fp waveguide")
        linear_taper_length = i3.PositiveNumberProperty(default=100, doc="length of linear taper")

        def _default_fp_grating(self):
            cell = self.cell.fp_grating
            lv = cell.get_default_view(self)
            lv.set(
                fp_width=self.fp_width,
                fp_length=self.fp_length,
                coupler_gap=self.coupler_gap,
            )
            return lv

        def _default_linear_taper(self):
            cell = self.cell.linear_taper
            lv = cell.get_default_view(self)
            lv.set(
                in_width=self.fp_width,
                out_width=self.width_out,
                length=self.linear_taper_length
            )
            return lv

class FP_BG_5_Exspot(i3.Circuit):

    edge_coupler = i3.ChildCellProperty(doc="edge coupler")
    linear_taper = i3.ChildCellProperty(doc="linear taper")
    fp_grating = i3.ChildCellProperty(doc="fp grating")
    device_length = i3.PositiveNumberProperty(default=10500, doc="width of input waveguide")

    def _default_edge_coupler(self):
        return pdk.AN800BB_ExSpot_SMF_C()

    def _default_linear_taper(self):
        return pdk.Taper()

    def _default_fp_grating(self):
        return FP_BG_5()

    def _default_insts(self):
        return {
                "in_coupler": self.edge_coupler,
                "out_coupler": self.edge_coupler,
                "linear_taper_in": self.linear_taper,
                "linear_taper_out": self.linear_taper,
                "fp_grating":self.fp_grating,
                }

    def _default_specs(self):
        return[
            i3.Place("fp_grating", (0,0)),

            i3.Place("in_coupler", position=(-self.device_length/2+620+55, 0.0), angle=180, relative_to="fp_grating:in0"),
            i3.Place("out_coupler", position=(self.device_length/2-620-55, 0.0), angle=0, relative_to="fp_grating:out0"),

            i3.Place("linear_taper_in", position=(115, 0), relative_to="in_coupler:in0"),
            i3.FlipH("linear_taper_in"),
            i3.Place("linear_taper_out", position=(-115, 0), angle=0, relative_to="out_coupler:in0"),

            i3.ConnectBend("linear_taper_in:out0", "in_coupler:in0"),
            i3.ConnectBend("linear_taper_out:out0", "out_coupler:in0"),
            i3.ConnectBend("linear_taper_in:in0", "fp_grating:in0"),
            i3.ConnectBend("linear_taper_out:in0", "fp_grating:out0")

        ]

    class Layout(i3.Circuit.Layout):
        fp_width = i3.PositiveNumberProperty(default=1.0, doc="width of fp waveguide")
        fp_length= i3.PositiveNumberProperty(default=1.0, doc="length of fp waveguide")
        width_out = i3.PositiveNumberProperty(default=1.0, doc="width of output waveguide")
        coupler_gap = i3.PositiveNumberProperty(default=1.0, doc="coupling gap between sbend and fp waveguide")
        linear_taper_length = i3.PositiveNumberProperty(default=100, doc="length of linear taper")

        def _default_fp_grating(self):
            cell = self.cell.fp_grating
            lv = cell.get_default_view(self)
            lv.set(
                fp_width=self.fp_width,
                fp_length=self.fp_length,
                coupler_gap=self.coupler_gap,
            )
            return lv

        def _default_linear_taper(self):
            cell = self.cell.linear_taper
            lv = cell.get_default_view(self)
            lv.set(
                in_width=self.fp_width,
                out_width=self.width_out,
                length=self.linear_taper_length
            )
            return lv

class FP_BG_6_Exspot(i3.Circuit):

    edge_coupler = i3.ChildCellProperty(doc="edge coupler")
    linear_taper = i3.ChildCellProperty(doc="linear taper")
    fp_grating = i3.ChildCellProperty(doc="fp grating")
    device_length = i3.PositiveNumberProperty(default=10500, doc="width of input waveguide")

    def _default_edge_coupler(self):
        return pdk.AN800BB_ExSpot_SMF_C()

    def _default_linear_taper(self):
        return pdk.Taper()

    def _default_fp_grating(self):
        return FP_BG_6()

    def _default_insts(self):
        return {
                "in_coupler": self.edge_coupler,
                "out_coupler": self.edge_coupler,
                "linear_taper_in": self.linear_taper,
                "linear_taper_out": self.linear_taper,
                "fp_grating":self.fp_grating,
                }

    def _default_specs(self):
        return[
            i3.Place("fp_grating", (0,0)),

            i3.Place("in_coupler", position=(-self.device_length/2+620+55, 0.0), angle=180, relative_to="fp_grating:in0"),
            i3.Place("out_coupler", position=(self.device_length/2-620-55, 0.0), angle=0, relative_to="fp_grating:out0"),

            i3.Place("linear_taper_in", position=(115, 0), relative_to="in_coupler:in0"),
            i3.FlipH("linear_taper_in"),
            i3.Place("linear_taper_out", position=(-115, 0), angle=0, relative_to="out_coupler:in0"),

            i3.ConnectBend("linear_taper_in:out0", "in_coupler:in0"),
            i3.ConnectBend("linear_taper_out:out0", "out_coupler:in0"),
            i3.ConnectBend("linear_taper_in:in0", "fp_grating:in0"),
            i3.ConnectBend("linear_taper_out:in0", "fp_grating:out0")

        ]

    class Layout(i3.Circuit.Layout):
        fp_width = i3.PositiveNumberProperty(default=1.0, doc="width of fp waveguide")
        fp_length= i3.PositiveNumberProperty(default=1.0, doc="length of fp waveguide")
        width_out = i3.PositiveNumberProperty(default=1.0, doc="width of output waveguide")
        coupler_gap = i3.PositiveNumberProperty(default=1.0, doc="coupling gap between sbend and fp waveguide")
        linear_taper_length = i3.PositiveNumberProperty(default=100, doc="length of linear taper")

        def _default_fp_grating(self):
            cell = self.cell.fp_grating
            lv = cell.get_default_view(self)
            lv.set(
                fp_width=self.fp_width,
                fp_length=self.fp_length,
                coupler_gap=self.coupler_gap,
            )
            return lv

        def _default_linear_taper(self):
            cell = self.cell.linear_taper
            lv = cell.get_default_view(self)
            lv.set(
                in_width=self.fp_width,
                out_width=self.width_out,
                length=self.linear_taper_length
            )
            return lv

class FP_BG_7_Exspot(i3.Circuit):

    edge_coupler = i3.ChildCellProperty(doc="edge coupler")
    linear_taper = i3.ChildCellProperty(doc="linear taper")
    fp_grating = i3.ChildCellProperty(doc="fp grating")
    device_length = i3.PositiveNumberProperty(default=10500, doc="width of input waveguide")

    def _default_edge_coupler(self):
        return pdk.AN800BB_ExSpot_SMF_C()

    def _default_linear_taper(self):
        return pdk.Taper()

    def _default_fp_grating(self):
        return FP_BG_7()

    def _default_insts(self):
        return {
                "in_coupler": self.edge_coupler,
                "out_coupler": self.edge_coupler,
                "linear_taper_in": self.linear_taper,
                "linear_taper_out": self.linear_taper,
                "fp_grating":self.fp_grating,
                }

    def _default_specs(self):
        return[
            i3.Place("fp_grating", (0,0)),

            i3.Place("in_coupler", position=(-self.device_length / 2 + 620 + 55, 0.0), angle=180,
                     relative_to="fp_grating:in0"),
            i3.Place("out_coupler", position=(self.device_length / 2 - 620 - 55, 0.0), angle=0,
                     relative_to="fp_grating:out0"),

            i3.Place("linear_taper_in", position=(115, 0), relative_to="in_coupler:in0"),
            i3.FlipH("linear_taper_in"),
            i3.Place("linear_taper_out", position=(-115, 0), angle=0, relative_to="out_coupler:in0"),

            i3.ConnectBend("linear_taper_in:out0", "in_coupler:in0"),
            i3.ConnectBend("linear_taper_out:out0", "out_coupler:in0"),
            i3.ConnectBend("linear_taper_in:in0", "fp_grating:in0"),
            i3.ConnectBend("linear_taper_out:in0", "fp_grating:out0")

        ]

    class Layout(i3.Circuit.Layout):
        fp_width = i3.PositiveNumberProperty(default=1.0, doc="width of fp waveguide")
        fp_length= i3.PositiveNumberProperty(default=1.0, doc="length of fp waveguide")
        width_out = i3.PositiveNumberProperty(default=1.0, doc="width of output waveguide")
        coupler_gap = i3.PositiveNumberProperty(default=1.0, doc="coupling gap between sbend and fp waveguide")
        linear_taper_length = i3.PositiveNumberProperty(default=100, doc="length of linear taper")

        def _default_fp_grating(self):
            cell = self.cell.fp_grating
            lv = cell.get_default_view(self)
            lv.set(
                fp_width=self.fp_width,
                fp_length=self.fp_length,
                coupler_gap=self.coupler_gap,
            )
            return lv

        def _default_linear_taper(self):
            cell = self.cell.linear_taper
            lv = cell.get_default_view(self)
            lv.set(
                in_width=self.fp_width,
                out_width=self.width_out,
                length=self.linear_taper_length
            )
            return lv

class FP_BG_8_Exspot(i3.Circuit):

    edge_coupler = i3.ChildCellProperty(doc="edge coupler")
    linear_taper = i3.ChildCellProperty(doc="linear taper")
    fp_grating = i3.ChildCellProperty(doc="fp grating")
    device_length = i3.PositiveNumberProperty(default=10500, doc="width of input waveguide")

    def _default_edge_coupler(self):
        return pdk.AN800BB_ExSpot_SMF_C()

    def _default_linear_taper(self):
        return pdk.Taper()

    def _default_fp_grating(self):
        return FP_BG_8()

    def _default_insts(self):
        return {
                "in_coupler": self.edge_coupler,
                "out_coupler": self.edge_coupler,
                "linear_taper_in": self.linear_taper,
                "linear_taper_out": self.linear_taper,
                "fp_grating":self.fp_grating,
                }

    def _default_specs(self):
        return[
            i3.Place("fp_grating", (0,0)),

            i3.Place("in_coupler", position=(-self.device_length / 2 + 620 + 55, 0.0), angle=180,
                     relative_to="fp_grating:in0"),
            i3.Place("out_coupler", position=(self.device_length / 2 - 620 - 55, 0.0), angle=0,
                     relative_to="fp_grating:out0"),

            i3.Place("linear_taper_in", position=(115, 0), relative_to="in_coupler:in0"),
            i3.FlipH("linear_taper_in"),
            i3.Place("linear_taper_out", position=(-115, 0), angle=0, relative_to="out_coupler:in0"),

            i3.ConnectBend("linear_taper_in:out0", "in_coupler:in0"),
            i3.ConnectBend("linear_taper_out:out0", "out_coupler:in0"),
            i3.ConnectBend("linear_taper_in:in0", "fp_grating:in0"),
            i3.ConnectBend("linear_taper_out:in0", "fp_grating:out0")

        ]

    class Layout(i3.Circuit.Layout):
        fp_width = i3.PositiveNumberProperty(default=1.0, doc="width of fp waveguide")
        fp_length= i3.PositiveNumberProperty(default=1.0, doc="length of fp waveguide")
        width_out = i3.PositiveNumberProperty(default=1.0, doc="width of output waveguide")
        coupler_gap = i3.PositiveNumberProperty(default=1.0, doc="coupling gap between sbend and fp waveguide")
        linear_taper_length = i3.PositiveNumberProperty(default=100, doc="length of linear taper")

        def _default_fp_grating(self):
            cell = self.cell.fp_grating
            lv = cell.get_default_view(self)
            lv.set(
                fp_width=self.fp_width,
                fp_length=self.fp_length,
                coupler_gap=self.coupler_gap,
            )
            return lv
        def _default_linear_taper(self):
            cell = self.cell.linear_taper
            lv = cell.get_default_view(self)
            lv.set(
                in_width=self.fp_width,
                out_width=self.width_out,
                length=self.linear_taper_length
            )
            return lv


class Sinusoidal_BG_Exspot(i3.Circuit):

    edge_coupler = i3.ChildCellProperty(doc="edge coupler")
    linear_taper = i3.ChildCellProperty(doc="linear taper")
    fp_grating = i3.ChildCellProperty(doc="fp grating")
    device_length = i3.PositiveNumberProperty(default=10500, doc="width of input waveguide")

    def _default_edge_coupler(self):
        return pdk.AN800BB_ExSpot_SMF_C()

    def _default_linear_taper(self):
        return pdk.Taper()

    def _default_fp_grating(self):
        return Sinusoidal_BG()

    def _default_insts(self):
        return {
                "in_coupler": self.edge_coupler,
                "out_coupler": self.edge_coupler,
                "linear_taper_in": self.linear_taper,
                "linear_taper_out": self.linear_taper,
                "fp_grating":self.fp_grating,
                }

    def _default_specs(self):
        return[
            i3.Place("fp_grating", (0,0)),

            i3.Place("in_coupler", position=(-self.device_length / 2 + 620 + 55, 0.0), angle=180,
                     relative_to="fp_grating:in0"),
            i3.Place("out_coupler", position=(self.device_length / 2 - 620 - 55, 0.0), angle=0,
                     relative_to="fp_grating:out0"),

            i3.Place("linear_taper_in", position=(115, 0), relative_to="in_coupler:in0"),
            i3.FlipH("linear_taper_in"),
            i3.Place("linear_taper_out", position=(-115, 0), angle=0, relative_to="out_coupler:in0"),

            i3.ConnectBend("linear_taper_in:out0", "in_coupler:in0"),
            i3.ConnectBend("linear_taper_out:out0", "out_coupler:in0"),
            i3.ConnectBend("linear_taper_in:in0", "fp_grating:in0"),
            i3.ConnectBend("linear_taper_out:in0", "fp_grating:out0")

        ]

    class Layout(i3.Circuit.Layout):
        fp_width = i3.PositiveNumberProperty(default=1.0, doc="width of fp waveguide")
        fp_length= i3.PositiveNumberProperty(default=1.0, doc="length of fp waveguide")
        width_out = i3.PositiveNumberProperty(default=1.0, doc="width of output waveguide")
        coupler_gap = i3.PositiveNumberProperty(default=1.0, doc="coupling gap between sbend and fp waveguide")
        linear_taper_length = i3.PositiveNumberProperty(default=100, doc="length of linear taper")

        def _default_fp_grating(self):
            cell = self.cell.fp_grating
            lv = cell.get_default_view(self)
            lv.set(
                fp_width=self.fp_width,
                fp_length=self.fp_length,
                coupler_gap=self.coupler_gap,
            )
            return lv
        def _default_linear_taper(self):
            cell = self.cell.linear_taper
            lv = cell.get_default_view(self)
            lv.set(
                in_width=self.fp_width,
                out_width=self.width_out,
                length=self.linear_taper_length
            )
            return lv

