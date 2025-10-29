import sys
import numpy as np
from PIL.ImageOps import mirror

sys.path.append("C:/pdk/Ligentec_SiN_2025/ipkiss")


import ligentec_an800.all as pdk
import ipkiss3.all as i3
import numpy as np

from Bragg_grating_test import BG_Test_1, BG_Test_2, BG_Test_3, BG_Test_4, BG_Test_5, BG_Test_6, BG_Test_7, BG_Test_8
from Bragg_grating import array_1, array_2, array_3, array_4, array_5, array_6, array_7, array_8, array_9
from Bragg_grating import BG_1_width_2, BG_2_width_2, BG_3_width_2, BG_4_width_2, BG_5_width_2, BG_6_width_2, BG_7_width_2, BG_8_width_2, BG_9_width_2
from Bragg_grating import BG_1_width_1, BG_2_width_1, BG_3_width_1, BG_4_width_1, BG_5_width_1, BG_6_width_1, BG_7_width_1, BG_8_width_1, BG_9_width_1


class BG_Test_1_lense(i3.Circuit):
    grating = i3.ChildCellProperty(doc="grating")
    linear_taper_out = i3.ChildCellProperty(doc="linear taper")
    lensed_fiber = i3.ChildCellProperty(doc="lensed fiber")

    def _default_linear_taper_out(self):
        # return pdk.LinearTaperFromPort(start_trace_template = self.trace_template_in, end_trace_template = self.trace_template_out)
        return pdk.Taper()

    def _default_lensed_fiber(self):
        return pdk.AN800BB_EdgeCoupler_Lensed_C()

    def _default_grating(self):
        return BG_Test_1()

    def _default_insts(self):
        return {
                "linear_taper_out": self.linear_taper_out,
                "lensed_fiber": self.lensed_fiber,
                "grating": self.grating,
                }

    def _default_specs(self):
        return [
            i3.Place("lensed_fiber", (0, 0)),
            i3.Place("linear_taper_out:out0", (-15, 0), angle=0, relative_to="lensed_fiber:in0"),
            i3.Place("grating:in0", (-10, 0), angle=0, relative_to="linear_taper_out:in0"),
            i3.ConnectBend("linear_taper_out:out0", "lensed_fiber:in0"),
            i3.ConnectBend("linear_taper_out:in0", "grating:in0"),
        ]

    class Layout(i3.Circuit.Layout):
        fp_width = i3.PositiveNumberProperty(default=1.0, doc="width of fabry perot waveguide")
        fp_length = i3.PositiveNumberProperty(default=10.0, doc="length of fabry perot waveguide")
        fp_taper_length = i3.PositiveNumberProperty(default=50.0, doc="length of fp taper")
        tip_width = i3.PositiveNumberProperty(default=0.3, doc="tip width of linear taper out")
        linear_taper_out_length = i3.PositiveNumberProperty(default=100.0, doc="length of linear taper out")


        def _default_linear_taper_out(self):
            cell = self.cell.linear_taper_out
            lv = cell.get_default_view(i3.LayoutView)
            lv.set(
                in_width=self.fp_width,
                out_width=1.8,
                length=self.linear_taper_out_length,
            )
            return lv

        def _default_grating(self):
            cell = self.cell.grating
            lv = cell.get_default_view(i3.LayoutView)
            lv.set(
                fp_width=self.fp_width,
                fp_length=self.fp_length,
            )
            return lv

        # def _generate_elements(self, elems):
        #     """
        #     add labels at in/out put grating couplers regions
        #     """
        #     in_port = self.instances["lensed_fiber"].ports["in0"]
        #     in_text_position = in_port.position
        #     in_x = in_port.position.x
        #     in_y = in_port.position.y
        #
        #     elems += i3.PolygonText(
        #         layer=i3.TECH.PPLAYER.X1P,
        #         coordinate=(in_x-100,in_y),
        #         text="BG_1",
        #         alignment=(i3.TEXT.ALIGN.CENTER, i3.TEXT.ALIGN.CENTER),
        #         font=i3.TEXT.FONT.DEFAULT,
        #         height=10,
        #         # transformation=i3.VMirror()
        #     )
        #     return elems

class BG_Test_2_lense(i3.Circuit):
    grating = i3.ChildCellProperty(doc="grating")
    linear_taper_out = i3.ChildCellProperty(doc="linear taper")
    lensed_fiber = i3.ChildCellProperty(doc="lensed fiber")

    def _default_linear_taper_out(self):
        # return pdk.LinearTaperFromPort(start_trace_template = self.trace_template_in, end_trace_template = self.trace_template_out)
        return pdk.Taper()

    def _default_lensed_fiber(self):
        return pdk.AN800BB_EdgeCoupler_Lensed_C()

    def _default_grating(self):
        return BG_Test_2()

    def _default_insts(self):
        return {
                "linear_taper_out": self.linear_taper_out,
                "lensed_fiber": self.lensed_fiber,
                "grating": self.grating,
                }

    def _default_specs(self):
        return [
            i3.Place("lensed_fiber", (0, 0)),
            i3.Place("linear_taper_out:out0", (-15, 0), angle=0, relative_to="lensed_fiber:in0"),
            i3.Place("grating:in0", (-10, 0), angle=0, relative_to="linear_taper_out:in0"),
            i3.ConnectBend("linear_taper_out:out0", "lensed_fiber:in0"),
            i3.ConnectBend("linear_taper_out:in0", "grating:in0"),
        ]

    class Layout(i3.Circuit.Layout):
        fp_width = i3.PositiveNumberProperty(default=1.0, doc="width of fabry perot waveguide")
        fp_length = i3.PositiveNumberProperty(default=10.0, doc="length of fabry perot waveguide")
        fp_taper_length = i3.PositiveNumberProperty(default=50.0, doc="length of fp taper")
        tip_width = i3.PositiveNumberProperty(default=0.3, doc="tip width of linear taper out")
        linear_taper_out_length = i3.PositiveNumberProperty(default=100.0, doc="length of linear taper out")

        def _default_linear_taper_out(self):
            cell = self.cell.linear_taper_out
            lv = cell.get_default_view(i3.LayoutView)
            lv.set(
                in_width=self.fp_width,
                out_width=1.8,
                length=self.linear_taper_out_length,
            )
            return lv

        def _default_grating(self):
            cell = self.cell.grating
            lv = cell.get_default_view(i3.LayoutView)
            lv.set(
                fp_width=self.fp_width,
                fp_length=self.fp_length,
            )
            return lv

        # def _generate_elements(self, elems):
        #     """
        #     add labels at in/out put grating couplers regions
        #     """
        #     in_port = self.instances["lensed_fiber"].ports["in0"]
        #     in_text_position = in_port.position
        #     in_x = in_port.position.x
        #     in_y = in_port.position.y
        #
        #     elems += i3.PolygonText(
        #         layer=i3.TECH.PPLAYER.X1P,
        #         coordinate=(in_x-100,in_y),
        #         text="BG_1",
        #         alignment=(i3.TEXT.ALIGN.CENTER, i3.TEXT.ALIGN.CENTER),
        #         font=i3.TEXT.FONT.DEFAULT,
        #         height=10,
        #         # transformation=i3.VMirror()
        #     )
        #     return elems

class BG_Test_3_lense(i3.Circuit):
    grating = i3.ChildCellProperty(doc="grating")
    linear_taper_out = i3.ChildCellProperty(doc="linear taper")
    lensed_fiber = i3.ChildCellProperty(doc="lensed fiber")

    def _default_linear_taper_out(self):
        # return pdk.LinearTaperFromPort(start_trace_template = self.trace_template_in, end_trace_template = self.trace_template_out)
        return pdk.Taper()

    def _default_lensed_fiber(self):
        return pdk.AN800BB_EdgeCoupler_Lensed_C()

    def _default_grating(self):
        return BG_Test_3()

    def _default_insts(self):
        return {
                "linear_taper_out": self.linear_taper_out,
                "lensed_fiber": self.lensed_fiber,
                "grating": self.grating,
                }

    def _default_specs(self):
        return [
            i3.Place("lensed_fiber", (0, 0)),
            i3.Place("linear_taper_out:out0", (-15, 0), angle=0, relative_to="lensed_fiber:in0"),
            i3.Place("grating:in0", (-10, 0), angle=0, relative_to="linear_taper_out:in0"),
            i3.ConnectBend("linear_taper_out:out0", "lensed_fiber:in0"),
            i3.ConnectBend("linear_taper_out:in0", "grating:in0"),
        ]

    class Layout(i3.Circuit.Layout):
        fp_width = i3.PositiveNumberProperty(default=1.0, doc="width of fabry perot waveguide")
        fp_length = i3.PositiveNumberProperty(default=10.0, doc="length of fabry perot waveguide")
        fp_taper_length = i3.PositiveNumberProperty(default=50.0, doc="length of fp taper")
        linear_taper_out_length = i3.PositiveNumberProperty(default=100.0, doc="length of linear taper out")

        def _default_linear_taper_out(self):
            cell = self.cell.linear_taper_out
            lv = cell.get_default_view(i3.LayoutView)
            lv.set(
                in_width=self.fp_width,
                out_width=1.8,
                length=self.linear_taper_out_length,
            )
            return lv

        def _default_grating(self):
            cell = self.cell.grating
            lv = cell.get_default_view(i3.LayoutView)
            lv.set(
                fp_width=self.fp_width,
                fp_length=self.fp_length,
            )
            return lv

        # def _generate_elements(self, elems):
        #     """
        #     add labels at in/out put grating couplers regions
        #     """
        #     in_port = self.instances["lensed_fiber"].ports["in0"]
        #     in_text_position = in_port.position
        #     in_x = in_port.position.x
        #     in_y = in_port.position.y
        #
        #     elems += i3.PolygonText(
        #         layer=i3.TECH.PPLAYER.X1P,
        #         coordinate=(in_x-100,in_y),
        #         text="BG_1",
        #         alignment=(i3.TEXT.ALIGN.CENTER, i3.TEXT.ALIGN.CENTER),
        #         font=i3.TEXT.FONT.DEFAULT,
        #         height=10,
        #         # transformation=i3.VMirror()
        #     )
        #     return elems

class BG_Test_4_lense(i3.Circuit):
    grating = i3.ChildCellProperty(doc="grating")
    linear_taper_out = i3.ChildCellProperty(doc="linear taper")
    lensed_fiber = i3.ChildCellProperty(doc="lensed fiber")

    def _default_linear_taper_out(self):
        # return pdk.LinearTaperFromPort(start_trace_template = self.trace_template_in, end_trace_template = self.trace_template_out)
        return pdk.Taper()

    def _default_lensed_fiber(self):
        return pdk.AN800BB_EdgeCoupler_Lensed_C()

    def _default_grating(self):
        return BG_Test_4()

    def _default_insts(self):
        return {
                "linear_taper_out": self.linear_taper_out,
                "lensed_fiber": self.lensed_fiber,
                "grating": self.grating,
                }

    def _default_specs(self):
        return [
            i3.Place("lensed_fiber", (0, 0)),
            i3.Place("linear_taper_out:out0", (-15, 0), angle=0, relative_to="lensed_fiber:in0"),
            i3.Place("grating:in0", (-10, 0), angle=0, relative_to="linear_taper_out:in0"),
            i3.ConnectBend("linear_taper_out:out0", "lensed_fiber:in0"),
            i3.ConnectBend("linear_taper_out:in0", "grating:in0"),
        ]

    class Layout(i3.Circuit.Layout):
        fp_width = i3.PositiveNumberProperty(default=1.0, doc="width of fabry perot waveguide")
        fp_length = i3.PositiveNumberProperty(default=10.0, doc="length of fabry perot waveguide")
        fp_taper_length = i3.PositiveNumberProperty(default=50.0, doc="length of fp taper")
        linear_taper_out_length = i3.PositiveNumberProperty(default=100.0, doc="length of linear taper out")


        def _default_linear_taper_out(self):
            cell = self.cell.linear_taper_out
            lv = cell.get_default_view(i3.LayoutView)
            lv.set(
                in_width=self.fp_width,
                out_width=1.8,
                length=self.linear_taper_out_length,
            )
            return lv

        def _default_grating(self):
            cell = self.cell.grating
            lv = cell.get_default_view(i3.LayoutView)
            lv.set(
                fp_width=self.fp_width,
                fp_length=self.fp_length,
            )
            return lv

        # def _generate_elements(self, elems):
        #     """
        #     add labels at in/out put grating couplers regions
        #     """
        #     in_port = self.instances["lensed_fiber"].ports["in0"]
        #     in_text_position = in_port.position
        #     in_x = in_port.position.x
        #     in_y = in_port.position.y
        #
        #     elems += i3.PolygonText(
        #         layer=i3.TECH.PPLAYER.X1P,
        #         coordinate=(in_x-100,in_y),
        #         text="BG_1",
        #         alignment=(i3.TEXT.ALIGN.CENTER, i3.TEXT.ALIGN.CENTER),
        #         font=i3.TEXT.FONT.DEFAULT,
        #         height=10,
        #         # transformation=i3.VMirror()
        #     )
        #     return elems

class BG_Test_5_lense(i3.Circuit):
    grating = i3.ChildCellProperty(doc="grating")
    linear_taper_out = i3.ChildCellProperty(doc="linear taper")
    lensed_fiber = i3.ChildCellProperty(doc="lensed fiber")

    def _default_linear_taper_out(self):
        # return pdk.LinearTaperFromPort(start_trace_template = self.trace_template_in, end_trace_template = self.trace_template_out)
        return pdk.Taper()

    def _default_lensed_fiber(self):
        return pdk.AN800BB_EdgeCoupler_Lensed_C()

    def _default_grating(self):
        return BG_Test_5()

    def _default_insts(self):
        return {
                "linear_taper_out": self.linear_taper_out,
                "lensed_fiber": self.lensed_fiber,
                "grating": self.grating,
                }

    def _default_specs(self):
        return [
            i3.Place("lensed_fiber", (0, 0)),
            i3.Place("linear_taper_out:out0", (-15, 0), angle=0, relative_to="lensed_fiber:in0"),
            i3.Place("grating:in0", (-10, 0), angle=0, relative_to="linear_taper_out:in0"),
            i3.ConnectBend("linear_taper_out:out0", "lensed_fiber:in0"),
            i3.ConnectBend("linear_taper_out:in0", "grating:in0"),
        ]

    class Layout(i3.Circuit.Layout):
        fp_width = i3.PositiveNumberProperty(default=1.0, doc="width of fabry perot waveguide")
        fp_length = i3.PositiveNumberProperty(default=10.0, doc="length of fabry perot waveguide")
        fp_taper_length = i3.PositiveNumberProperty(default=50.0, doc="length of fp taper")
        linear_taper_out_length = i3.PositiveNumberProperty(default=100.0, doc="length of linear taper out")

        def _default_linear_taper_out(self):
            cell = self.cell.linear_taper_out
            lv = cell.get_default_view(i3.LayoutView)
            lv.set(
                in_width=self.fp_width,
                out_width=1.8,
                length=self.linear_taper_out_length,
            )
            return lv

        def _default_grating(self):
            cell = self.cell.grating
            lv = cell.get_default_view(i3.LayoutView)
            lv.set(
                fp_width=self.fp_width,
                fp_length=self.fp_length,
            )
            return lv

        # def _generate_elements(self, elems):
        #     """
        #     add labels at in/out put grating couplers regions
        #     """
        #     in_port = self.instances["lensed_fiber"].ports["in0"]
        #     in_text_position = in_port.position
        #     in_x = in_port.position.x
        #     in_y = in_port.position.y
        #
        #     elems += i3.PolygonText(
        #         layer=i3.TECH.PPLAYER.X1P,
        #         coordinate=(in_x-100,in_y),
        #         text="BG_1",
        #         alignment=(i3.TEXT.ALIGN.CENTER, i3.TEXT.ALIGN.CENTER),
        #         font=i3.TEXT.FONT.DEFAULT,
        #         height=10,
        #         # transformation=i3.VMirror()
        #     )
        #     return elems

class BG_Test_6_lense(i3.Circuit):
    grating = i3.ChildCellProperty(doc="grating")
    linear_taper_out = i3.ChildCellProperty(doc="linear taper")
    lensed_fiber = i3.ChildCellProperty(doc="lensed fiber")

    def _default_linear_taper_out(self):
        # return pdk.LinearTaperFromPort(start_trace_template = self.trace_template_in, end_trace_template = self.trace_template_out)
        return pdk.Taper()

    def _default_lensed_fiber(self):
        return pdk.AN800BB_EdgeCoupler_Lensed_C()

    def _default_grating(self):
        return BG_Test_6()

    def _default_insts(self):
        return {
                "linear_taper_out": self.linear_taper_out,
                "lensed_fiber": self.lensed_fiber,
                "grating": self.grating,
                }

    def _default_specs(self):
        return [
            i3.Place("lensed_fiber", (0, 0)),
            i3.Place("linear_taper_out:out0", (-15, 0), angle=0, relative_to="lensed_fiber:in0"),
            i3.Place("grating:in0", (-10, 0), angle=0, relative_to="linear_taper_out:in0"),
            i3.ConnectBend("linear_taper_out:out0", "lensed_fiber:in0"),
            i3.ConnectBend("linear_taper_out:in0", "grating:in0"),
        ]

    class Layout(i3.Circuit.Layout):
        fp_width = i3.PositiveNumberProperty(default=1.0, doc="width of fabry perot waveguide")
        fp_length = i3.PositiveNumberProperty(default=10.0, doc="length of fabry perot waveguide")
        fp_taper_length = i3.PositiveNumberProperty(default=50.0, doc="length of fp taper")
        linear_taper_out_length = i3.PositiveNumberProperty(default=100.0, doc="length of linear taper out")

        def _default_linear_taper_out(self):
            cell = self.cell.linear_taper_out
            lv = cell.get_default_view(i3.LayoutView)
            lv.set(
                in_width=self.fp_width,
                out_width=1.8,
                length=self.linear_taper_out_length,
            )
            return lv

        def _default_grating(self):
            cell = self.cell.grating
            lv = cell.get_default_view(i3.LayoutView)
            lv.set(
                fp_width=self.fp_width,
                fp_length=self.fp_length,
            )
            return lv

        # def _generate_elements(self, elems):
        #     """
        #     add labels at in/out put grating couplers regions
        #     """
        #     in_port = self.instances["lensed_fiber"].ports["in0"]
        #     in_text_position = in_port.position
        #     in_x = in_port.position.x
        #     in_y = in_port.position.y
        #
        #     elems += i3.PolygonText(
        #         layer=i3.TECH.PPLAYER.X1P,
        #         coordinate=(in_x-100,in_y),
        #         text="BG_1",
        #         alignment=(i3.TEXT.ALIGN.CENTER, i3.TEXT.ALIGN.CENTER),
        #         font=i3.TEXT.FONT.DEFAULT,
        #         height=10,
        #         # transformation=i3.VMirror()
        #     )
        #     return elems

class BG_Test_7_lense(i3.Circuit):
    grating = i3.ChildCellProperty(doc="grating")
    linear_taper_out = i3.ChildCellProperty(doc="linear taper")
    lensed_fiber = i3.ChildCellProperty(doc="lensed fiber")

    def _default_linear_taper_out(self):
        # return pdk.LinearTaperFromPort(start_trace_template = self.trace_template_in, end_trace_template = self.trace_template_out)
        return pdk.Taper()

    def _default_lensed_fiber(self):
        return pdk.AN800BB_EdgeCoupler_Lensed_C()

    def _default_grating(self):
        return BG_Test_7()

    def _default_insts(self):
        return {
                "linear_taper_out": self.linear_taper_out,
                "lensed_fiber": self.lensed_fiber,
                "grating": self.grating,
                }

    def _default_specs(self):
        return [
            i3.Place("lensed_fiber", (0, 0)),
            i3.Place("linear_taper_out:out0", (-15, 0), angle=0, relative_to="lensed_fiber:in0"),
            i3.Place("grating:in0", (-10, 0), angle=0, relative_to="linear_taper_out:in0"),
            i3.ConnectBend("linear_taper_out:out0", "lensed_fiber:in0"),
            i3.ConnectBend("linear_taper_out:in0", "grating:in0"),
        ]

    class Layout(i3.Circuit.Layout):
        fp_width = i3.PositiveNumberProperty(default=1.0, doc="width of fabry perot waveguide")
        fp_length = i3.PositiveNumberProperty(default=10.0, doc="length of fabry perot waveguide")
        fp_taper_length = i3.PositiveNumberProperty(default=50.0, doc="length of fp taper")
        linear_taper_out_length = i3.PositiveNumberProperty(default=100.0, doc="length of linear taper out")

        def _default_linear_taper_out(self):
            cell = self.cell.linear_taper_out
            lv = cell.get_default_view(i3.LayoutView)
            lv.set(
                in_width=self.fp_width,
                out_width=1.8,
                length=self.linear_taper_out_length,
            )
            return lv

        def _default_grating(self):
            cell = self.cell.grating
            lv = cell.get_default_view(i3.LayoutView)
            lv.set(
                fp_width=self.fp_width,
                fp_length=self.fp_length,
            )
            return lv

        # def _generate_elements(self, elems):
        #     """
        #     add labels at in/out put grating couplers regions
        #     """
        #     in_port = self.instances["lensed_fiber"].ports["in0"]
        #     in_text_position = in_port.position
        #     in_x = in_port.position.x
        #     in_y = in_port.position.y
        #
        #     elems += i3.PolygonText(
        #         layer=i3.TECH.PPLAYER.X1P,
        #         coordinate=(in_x-100,in_y),
        #         text="BG_1",
        #         alignment=(i3.TEXT.ALIGN.CENTER, i3.TEXT.ALIGN.CENTER),
        #         font=i3.TEXT.FONT.DEFAULT,
        #         height=10,
        #         # transformation=i3.VMirror()
        #     )
        #     return elems

class BG_Test_8_lense(i3.Circuit):
    grating = i3.ChildCellProperty(doc="grating")
    linear_taper_out = i3.ChildCellProperty(doc="linear taper")
    lensed_fiber = i3.ChildCellProperty(doc="lensed fiber")

    def _default_linear_taper_out(self):
        # return pdk.LinearTaperFromPort(start_trace_template = self.trace_template_in, end_trace_template = self.trace_template_out)
        return pdk.Taper()

    def _default_lensed_fiber(self):
        return pdk.AN800BB_EdgeCoupler_Lensed_C()

    def _default_grating(self):
        return BG_Test_8()

    def _default_insts(self):
        return {
                "linear_taper_out": self.linear_taper_out,
                "lensed_fiber": self.lensed_fiber,
                "grating": self.grating,
                }

    def _default_specs(self):
        return [
            i3.Place("lensed_fiber", (0, 0)),
            i3.Place("linear_taper_out:out0", (-15, 0), angle=0, relative_to="lensed_fiber:in0"),
            i3.Place("grating:in0", (-10, 0), angle=0, relative_to="linear_taper_out:in0"),
            i3.ConnectBend("linear_taper_out:out0", "lensed_fiber:in0"),
            i3.ConnectBend("linear_taper_out:in0", "grating:in0"),
        ]

    class Layout(i3.Circuit.Layout):
        fp_width = i3.PositiveNumberProperty(default=1.0, doc="width of fabry perot waveguide")
        fp_length = i3.PositiveNumberProperty(default=10.0, doc="length of fabry perot waveguide")
        fp_taper_length = i3.PositiveNumberProperty(default=50.0, doc="length of fp taper")
        linear_taper_out_length = i3.PositiveNumberProperty(default=100.0, doc="length of linear taper out")

        def _default_linear_taper_out(self):
            cell = self.cell.linear_taper_out
            lv = cell.get_default_view(i3.LayoutView)
            lv.set(
                in_width=self.fp_width,
                out_width=1.8,
                length=self.linear_taper_out_length,
            )
            return lv

        def _default_grating(self):
            cell = self.cell.grating
            lv = cell.get_default_view(i3.LayoutView)
            lv.set(
                fp_width=self.fp_width,
                fp_length=self.fp_length,
            )
            return lv

        # def _generate_elements(self, elems):
        #     """
        #     add labels at in/out put grating couplers regions
        #     """
        #     in_port = self.instances["lensed_fiber"].ports["in0"]
        #     in_text_position = in_port.position
        #     in_x = in_port.position.x
        #     in_y = in_port.position.y
        #
        #     elems += i3.PolygonText(
        #         layer=i3.TECH.PPLAYER.X1P,
        #         coordinate=(in_x-100,in_y),
        #         text="BG_1",
        #         alignment=(i3.TEXT.ALIGN.CENTER, i3.TEXT.ALIGN.CENTER),
        #         font=i3.TEXT.FONT.DEFAULT,
        #         height=10,
        #         # transformation=i3.VMirror()
        #     )
        #     return elems

# class BG_Test_1_lense(i3.Circuit):
#     grating = i3.ChildCellProperty(doc="grating")
#     linear_taper_out = i3.ChildCellProperty(doc="linear taper")
#     lensed_fiber = i3.ChildCellProperty(doc="lensed fiber")
#
#     def _default_linear_taper_out(self):
#         # return pdk.LinearTaperFromPort(start_trace_template = self.trace_template_in, end_trace_template = self.trace_template_out)
#         return pdk.Taper()
#
#     def _default_lensed_fiber(self):
#         return pdk.AN800BB_EdgeCoupler_Lensed_C()
#
#     def _default_grating(self):
#         return BG_Test_1()
#
#     def _default_insts(self):
#         return {
#                 "linear_taper_out": self.linear_taper_out,
#                 "lensed_fiber": self.lensed_fiber,
#                 "grating": self.grating,
#                 }
#
#     def _default_specs(self):
#         return [
#             i3.Place("lensed_fiber", (0, 0)),
#             i3.Place("linear_taper_out:out0", (-15, 0), angle=0, relative_to="lensed_fiber:in0"),
#             i3.Place("grating:in0", (-10, 0), angle=0, relative_to="linear_taper_out:in0"),
#             i3.ConnectBend("linear_taper_out:out0", "lensed_fiber:in0"),
#             i3.ConnectBend("linear_taper_out:in0", "grating:in0"),
#         ]
#
#     class Layout(i3.Circuit.Layout):
#         fp_width = i3.PositiveNumberProperty(default=1.0, doc="width of fabry perot waveguide")
#         fp_length = i3.PositiveNumberProperty(default=10.0, doc="length of fabry perot waveguide")
#         end_fp_taper_width = i3.PositiveNumberProperty(default=0.5, doc="width of end fp taper port")
#         fp_taper_length = i3.PositiveNumberProperty(default=50.0, doc="length of fp taper")
#         tip_width = i3.PositiveNumberProperty(default=0.3, doc="tip width of linear taper out")
#         linear_taper_out_length = i3.PositiveNumberProperty(default=100.0, doc="length of linear taper out")
#
#         def _default_end_fp_taper_width(self):
#             return BG_1_width_2[len(array_1)-1]
#
#         # print("BG_1:{}".format(BG_1_width_2[len(array_1) - 1]))
#
#         def _default_linear_taper_out(self):
#             cell = self.cell.linear_taper_out
#             lv = cell.get_default_view(i3.LayoutView)
#             lv.set(
#                 in_width=self.fp_width,
#                 out_width=1.8,
#                 length=self.linear_taper_out_length,
#             )
#             return lv
#
#         def _default_grating(self):
#             cell = self.cell.grating
#             lv = cell.get_default_view(i3.LayoutView)
#             lv.set(
#                 fp_width=self.fp_width,
#                 fp_length=self.fp_length,
#             )
#             return lv
#
#         # def _generate_elements(self, elems):
#         #     """
#         #     add labels at in/out put grating couplers regions
#         #     """
#         #     in_port = self.instances["lensed_fiber"].ports["in0"]
#         #     in_text_position = in_port.position
#         #     in_x = in_port.position.x
#         #     in_y = in_port.position.y
#         #
#         #     elems += i3.PolygonText(
#         #         layer=i3.TECH.PPLAYER.X1P,
#         #         coordinate=(in_x-100,in_y),
#         #         text="BG_1",
#         #         alignment=(i3.TEXT.ALIGN.CENTER, i3.TEXT.ALIGN.CENTER),
#         #         font=i3.TEXT.FONT.DEFAULT,
#         #         height=10,
#         #         # transformation=i3.VMirror()
#         #     )
#         #     return elems


# class BG_Test_Sin_lense(i3.Circuit):
#     fp_waveguide = i3.ChildCellProperty(doc="fabry perot waveguide")
#     grating = i3.ChildCellProperty(doc="grating")
#     fp_linear_taper = i3.ChildCellProperty(doc="linear taper")
#     linear_taper_out = i3.ChildCellProperty(doc="linear taper")
#     lensed_fiber = i3.ChildCellProperty(doc="lensed fiber")
#
#     def _default_fp_waveguide(self):
#         return pdk.Straight()
#
#     def _default_fp_linear_taper(self):
#         # return pdk.LinearTaperFromPort(start_trace_template = self.trace_template_in, end_trace_template = self.trace_template_out)
#         return SinusoidalGratingTaper()
#
#     def _default_linear_taper_out(self):
#         # return pdk.LinearTaperFromPort(start_trace_template = self.trace_template_in, end_trace_template = self.trace_template_out)
#         return pdk.Taper()
#
#     def _default_lensed_fiber(self):
#         return pdk.AN800BB_EdgeCoupler_Lensed_C()
#
#     def _default_grating(self):
#         return SinusoidalGrating()
#
#     def _default_insts(self):
#         return {"fp_waveguide": self.fp_waveguide,
#                 "fp_linear_taper": self.fp_linear_taper,
#                 "fp_linear_taper_2": self.fp_linear_taper,
#                 "linear_taper_out": self.linear_taper_out,
#                 "lensed_fiber": self.lensed_fiber,
#                 "grating": self.grating,
#                 }
#
#     def _default_specs(self):
#         return [
#             i3.Place("fp_waveguide", (0, 0)),
#             i3.Place("fp_linear_taper", (0, 0), angle=180, relative_to="fp_waveguide:in0"),
#             i3.Place("lensed_fiber", (115, 0), angle=0, relative_to="fp_waveguide:out0"),
#             i3.Place("linear_taper_out", (25 - 15, 0), angle=0, relative_to="fp_waveguide:out0"),
#             i3.Place("grating", (0, 0), angle=180, relative_to="fp_linear_taper:out"),
#             i3.Place("fp_linear_taper_2", (0, 0), angle=0, relative_to="grating:out"),
#             i3.FlipH("fp_linear_taper_2"),
#             i3.ConnectBend("linear_taper_out:out0", "lensed_fiber:in0"),
#             i3.ConnectBend("linear_taper_out:in0", "fp_waveguide:out0"),
#         ]
#
#     class Layout(i3.Circuit.Layout):
#         fp_width = i3.PositiveNumberProperty(default=1.0, doc="width of fabry perot waveguide")
#         fp_length = i3.PositiveNumberProperty(default=10.0, doc="length of fabry perot waveguide")
#         end_fp_taper_width = i3.PositiveNumberProperty(default=0.5, doc="width of end fp taper port")
#         fp_taper_length = i3.PositiveNumberProperty(default=50.0, doc="length of fp taper")
#         tip_width = i3.PositiveNumberProperty(default=0.3, doc="tip width of linear taper out")
#         linear_taper_out_length = i3.PositiveNumberProperty(default=100.0, doc="length of linear taper out")
#
#         def _default_fp_waveguide(self):
#             cell = self.cell.fp_waveguide
#             lv = cell.get_default_view(i3.LayoutView)
#             lv.set(
#                 width=self.fp_width,
#                 length=self.fp_length,
#             )
#             return lv
#
#         # def _default_end_fp_taper_width(self):
#         #     return BG_3_width_2[len(array_3)-1]
#
#         # print("BG_1:{}".format(BG_1_width_2[len(array_1) - 1]))
#
#         # def _default_fp_linear_taper(self):
#         #     cell = self.cell.fp_linear_taper
#         #     lv = cell.get_default_view(i3.LayoutView)
#         #     lv.set(
#         #         in_width=self.fp_width,
#         #         out_width=self.end_fp_taper_width,
#         #         length=self.fp_taper_length,
#         #     )
#         #     return lv
#
#         def _default_linear_taper_out(self):
#             cell = self.cell.linear_taper_out
#             lv = cell.get_default_view(i3.LayoutView)
#             lv.set(
#                 in_width=self.fp_width,
#                 out_width=1.8,
#                 length=self.linear_taper_out_length,
#             )
#             return lv
#
#         # def _generate_elements(self, elems):
#         #     """
#         #     add labels at in/out put grating couplers regions
#         #     """
#         #     in_port = self.instances["lensed_fiber"].ports["in0"]
#         #     in_text_position = in_port.position
#         #     in_x = in_port.position.x
#         #     in_y = in_port.position.y
#         #
#         #     elems += i3.PolygonText(
#         #         layer=i3.TECH.PPLAYER.X1P,
#         #         coordinate=(in_x-100,in_y),
#         #         text="BG_8",
#         #         alignment=(i3.TEXT.ALIGN.CENTER, i3.TEXT.ALIGN.CENTER),
#         #         font=i3.TEXT.FONT.DEFAULT,
#         #         height=10,
#         #         # transformation=i3.VMirror()
#         #     )
#         #     return elems
