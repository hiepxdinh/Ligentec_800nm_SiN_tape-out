import sys
import numpy as np
from PIL.ImageOps import mirror

sys.path.append("C:/pdk/Ligentec_SiN_2025/ipkiss")


import ligentec_an800.all as pdk
import ipkiss3.all as i3
import numpy as np

from Bragg_grating import BG_1, BG_2, BG_3, BG_4, BG_5, BG_6, BG_7, BG_8, SinusoidalGrating, SinusoidalGratingTaper
from Bragg_grating import array_1, array_2, array_3, array_4, array_5, array_6, array_7, array_8
from Bragg_grating import BG_1_width_2, BG_2_width_2, BG_3_width_2, BG_4_width_2, BG_5_width_2, BG_6_width_2, BG_7_width_2, BG_8_width_2

class BG_Test_1_lensed_fiber(i3.Circuit):
    fp_waveguide = i3.ChildCellProperty(doc="fabry perot waveguide")
    grating = i3.ChildCellProperty(doc="grating")
    fp_linear_taper = i3.ChildCellProperty(doc="linear taper")
    linear_taper_out = i3.ChildCellProperty(doc="linear taper")
    lensed_fiber = i3.ChildCellProperty(doc="lensed fiber")

    def _default_fp_waveguide(self):
        return pdk.Straight()

    def _default_fp_linear_taper(self):
        # return pdk.LinearTaperFromPort(start_trace_template = self.trace_template_in, end_trace_template = self.trace_template_out)
        return pdk.Taper()

    def _default_linear_taper_out(self):
        # return pdk.LinearTaperFromPort(start_trace_template = self.trace_template_in, end_trace_template = self.trace_template_out)
        return pdk.Taper()

    def _default_lensed_fiber(self):
        return pdk.AN800BB_EdgeCoupler_Lensed_C()

    def _default_grating(self):
        return BG_1()

    def _default_insts(self):
        return {"fp_waveguide": self.fp_waveguide,
                "fp_linear_taper": self.fp_linear_taper,
                "linear_taper_out": self.linear_taper_out,
                "lensed_fiber": self.lensed_fiber,
                "grating": self.grating,
                # "linear_transition_out": self.linear_transition,
                # # "linear_transition_in_ref": self.linear_transition,
                # # "linear_transition_out_ref": self.linear_transition,
                # # "in_taper_ref": self.taper,
                # # "out_taper_ref": self.taper,
                }

    def _default_specs(self):
        return [
            i3.Place("fp_waveguide", (0, 0)),
            i3.Place("fp_linear_taper", (0, 0), angle=180, relative_to="fp_waveguide:in0"),
            i3.Place("lensed_fiber", (125, 0), angle=0, relative_to="fp_waveguide:out0"),
            i3.Place("linear_taper_out", (25 - 15, 0), angle=0, relative_to="fp_waveguide:out0"),
            i3.Place("grating:out", (0, 0), relative_to="fp_linear_taper:out0"),
            i3.ConnectBend("linear_taper_out:out0", "lensed_fiber:in0"),
            i3.ConnectBend("linear_taper_out:in0", "fp_waveguide:out0"),
        ]

    class Layout(i3.LayoutView):
        fp_width = i3.PositiveNumberProperty(default=1.0, doc="width of fabry perot waveguide")
        fp_length = i3.PositiveNumberProperty(default=10.0, doc="length of fabry perot waveguide")
        end_fp_taper_width = i3.PositiveNumberProperty(default=0.5, doc="width of end fp taper port")
        fp_taper_length = i3.PositiveNumberProperty(default=50.0, doc="length of fp taper")
        tip_width = i3.PositiveNumberProperty(default=0.3, doc="tip width of linear taper out")
        linear_taper_out_length = i3.PositiveNumberProperty(default=100.0, doc="length of linear taper out")

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

        # print("BG_1:{}".format(BG_1_width_2[len(array_1) - 1]))

        def _default_fp_linear_taper(self):
            cell = self.cell.fp_linear_taper
            lv = cell.get_default_view(self)
            lv.set(
                in_width=self.fp_width,
                out_width=self.end_fp_taper_width,
                length=self.fp_taper_length,
            )
            return lv

        def _default_linear_taper_out(self):
            cell = self.cell.linear_taper_out
            lv = cell.get_default_view(self)
            lv.set(
                in_width=self.fp_width,
                out_width=1.8,
                length=self.linear_taper_out_length,
            )
            return lv

        def _generate_instances(self, insts):
            fp_waveguide = self.fp_waveguide
            fp_linear_taper = self.fp_linear_taper
            grating = self.grating
            linear_taper_out = self.linear_taper_out
            lensed_fiber = self.lensed_fiber

            insts += i3.SRef(name="fp_waveguide", reference=fp_waveguide, flatten=True)
            insts += i3.SRef(name="fp_linear_taper", reference=fp_linear_taper, flatten=True)
            insts += i3.SRef(name="linear_taper_out", reference=linear_taper_out, flatten=True)
            insts += i3.SRef(name="grating", reference=grating, flatten=True)
            insts += i3.SRef(name="lensed_fiber", reference=lensed_fiber, flatten=True)
            return i3.place_and_route(
                insts=insts,
                specs=[
                    i3.Place("fp_waveguide", (0, 0)),
                    i3.Place("fp_linear_taper", (0, 0), angle=180, relative_to="fp_waveguide:in0"),
                    i3.Place("lensed_fiber", (125, 0), angle=0, relative_to="fp_waveguide:out0"),
                    i3.Place("linear_taper_out", (25-15, 0), angle=0, relative_to="fp_waveguide:out0"),
                    i3.Place("grating:out", (0, 0), relative_to="fp_linear_taper:out0"),
                    i3.ConnectBend("linear_taper_out:out0", "lensed_fiber:in0"),
                    i3.ConnectBend("linear_taper_out:in0", "fp_waveguide:out0"),
                ]
            )


class BG_Test_2_lensed_fiber(i3.Circuit):
    fp_waveguide = i3.ChildCellProperty(doc="fabry perot waveguide")
    grating = i3.ChildCellProperty(doc="grating")
    fp_linear_taper = i3.ChildCellProperty(doc="linear taper")
    linear_taper_out = i3.ChildCellProperty(doc="linear taper")
    lensed_fiber = i3.ChildCellProperty(doc="lensed fiber")

    def _default_fp_waveguide(self):
        return pdk.Straight()

    def _default_fp_linear_taper(self):
        # return pdk.LinearTaperFromPort(start_trace_template = self.trace_template_in, end_trace_template = self.trace_template_out)
        return pdk.Taper()

    def _default_linear_taper_out(self):
        # return pdk.LinearTaperFromPort(start_trace_template = self.trace_template_in, end_trace_template = self.trace_template_out)
        return pdk.Taper()

    def _default_lensed_fiber(self):
        return pdk.AN800BB_EdgeCoupler_Lensed_C()


    def _default_grating(self):
        return BG_2()

    def _default_insts(self):
        return {"fp_waveguide": self.fp_waveguide,
                "fp_linear_taper": self.fp_linear_taper,
                "linear_taper_out": self.linear_taper_out,
                "lensed_fiber": self.lensed_fiber,
                "grating": self.grating,
                # "linear_transition_out": self.linear_transition,
                # # "linear_transition_in_ref": self.linear_transition,
                # # "linear_transition_out_ref": self.linear_transition,
                # # "in_taper_ref": self.taper,
                # # "out_taper_ref": self.taper,
                }

    def _default_specs(self):
        return [
            i3.Place("fp_waveguide", (0, 0)),
            i3.Place("fp_linear_taper", (0, 0), angle=180, relative_to="fp_waveguide:in0"),
            i3.Place("lensed_fiber", (125, 0), angle=0, relative_to="fp_waveguide:out0"),
            i3.Place("linear_taper_out", (25 - 15, 0), angle=0, relative_to="fp_waveguide:out0"),
            i3.Place("grating:out", (0, 0), relative_to="fp_linear_taper:out0"),
            i3.ConnectBend("linear_taper_out:out0", "lensed_fiber:in0"),
            i3.ConnectBend("linear_taper_out:in0", "fp_waveguide:out0"),
        ]

    class Layout(i3.LayoutView):
        fp_width = i3.PositiveNumberProperty(default=1.0, doc="width of fabry perot waveguide")
        fp_length = i3.PositiveNumberProperty(default=150.0, doc="length of fabry perot waveguide")
        end_fp_taper_width = i3.PositiveNumberProperty(default=0.5, doc="width of end fp taper port")
        fp_taper_length = i3.PositiveNumberProperty(default=50.0, doc="length of fp taper")
        tip_width = i3.PositiveNumberProperty(default=0.3, doc="tip width of linear taper out")
        linear_taper_out_length = i3.PositiveNumberProperty(default=100.0, doc="length of linear taper out")

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

        # print("BG_1:{}".format(BG_1_width_2[len(array_1) - 1]))

        def _default_fp_linear_taper(self):
            cell = self.cell.fp_linear_taper
            lv = cell.get_default_view(self)
            lv.set(
                in_width=self.fp_width,
                out_width=self.end_fp_taper_width,
                length=self.fp_taper_length,
            )
            return lv

        def _default_linear_taper_out(self):
            cell = self.cell.linear_taper_out
            lv = cell.get_default_view(self)
            lv.set(
                in_width=self.fp_width,
                out_width=1.8,
                length=self.linear_taper_out_length,
            )
            return lv

        def _generate_instances(self, insts):
            fp_waveguide = self.fp_waveguide
            fp_linear_taper = self.fp_linear_taper
            grating = self.grating
            linear_taper_out = self.linear_taper_out
            lensed_fiber = self.lensed_fiber

            insts += i3.SRef(name="fp_waveguide", reference=fp_waveguide, flatten=True)
            insts += i3.SRef(name="fp_linear_taper", reference=fp_linear_taper, flatten=True)
            insts += i3.SRef(name="linear_taper_out", reference=linear_taper_out, flatten=True)
            insts += i3.SRef(name="grating", reference=grating, flatten=True)
            insts += i3.SRef(name="lensed_fiber", reference=lensed_fiber, flatten=True)

            return i3.place_and_route(
                insts=insts,
                specs=[
                    i3.Place("fp_waveguide", (0, 0)),
                    i3.Place("fp_linear_taper", (0, 0), angle=180, relative_to="fp_waveguide:in0"),
                    i3.Place("lensed_fiber", (125, 0), angle=0, relative_to="fp_waveguide:out0"),
                    i3.Place("linear_taper_out", (25-15, 0), angle=0, relative_to="fp_waveguide:out0"),
                    i3.Place("grating:out", (0, 0), relative_to="fp_linear_taper:out0"),
                    i3.ConnectBend("linear_taper_out:out0", "lensed_fiber:in0"),
                    i3.ConnectBend("linear_taper_out:in0", "fp_waveguide:out0"),
                ]
            )

class BG_Test_3_lensed_fiber(i3.Circuit):
    fp_waveguide = i3.ChildCellProperty(doc="fabry perot waveguide")
    grating = i3.ChildCellProperty(doc="grating")
    fp_linear_taper = i3.ChildCellProperty(doc="linear taper")
    linear_taper_out = i3.ChildCellProperty(doc="linear taper")
    lensed_fiber = i3.ChildCellProperty(doc="lensed fiber")

    def _default_fp_waveguide(self):
        return pdk.Straight()

    def _default_fp_linear_taper(self):
        # return pdk.LinearTaperFromPort(start_trace_template = self.trace_template_in, end_trace_template = self.trace_template_out)
        return pdk.Taper()

    def _default_linear_taper_out(self):
        # return pdk.LinearTaperFromPort(start_trace_template = self.trace_template_in, end_trace_template = self.trace_template_out)
        return pdk.Taper()

    def _default_lensed_fiber(self):
        return pdk.AN800BB_EdgeCoupler_Lensed_C()


    def _default_grating(self):
        return BG_3()

    def _default_insts(self):
        return {"fp_waveguide": self.fp_waveguide,
                "fp_linear_taper": self.fp_linear_taper,
                "linear_taper_out": self.linear_taper_out,
                "lensed_fiber": self.lensed_fiber,
                "grating": self.grating,
                # "linear_transition_out": self.linear_transition,
                # # "linear_transition_in_ref": self.linear_transition,
                # # "linear_transition_out_ref": self.linear_transition,
                # # "in_taper_ref": self.taper,
                # # "out_taper_ref": self.taper,
                }

    def _default_specs(self):
        return [
            i3.Place("fp_waveguide", (0, 0)),
            i3.Place("fp_linear_taper", (0, 0), angle=180, relative_to="fp_waveguide:in0"),
            i3.Place("lensed_fiber", (125, 0), angle=0, relative_to="fp_waveguide:out0"),
            i3.Place("linear_taper_out", (25 - 15, 0), angle=0, relative_to="fp_waveguide:out0"),
            i3.Place("grating:out", (0, 0), relative_to="fp_linear_taper:out0"),
            i3.ConnectBend("linear_taper_out:out0", "lensed_fiber:in0"),
            i3.ConnectBend("linear_taper_out:in0", "fp_waveguide:out0"),
        ]

    class Layout(i3.LayoutView):
        fp_width = i3.PositiveNumberProperty(default=1.0, doc="width of fabry perot waveguide")
        fp_length = i3.PositiveNumberProperty(default=150.0, doc="length of fabry perot waveguide")
        end_fp_taper_width = i3.PositiveNumberProperty(default=0.5, doc="width of end fp taper port")
        fp_taper_length = i3.PositiveNumberProperty(default=50.0, doc="length of fp taper")
        tip_width = i3.PositiveNumberProperty(default=0.3, doc="tip width of linear taper out")
        linear_taper_out_length = i3.PositiveNumberProperty(default=100.0, doc="length of linear taper out")

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

        # print("BG_1:{}".format(BG_1_width_2[len(array_1) - 1]))

        def _default_fp_linear_taper(self):
            cell = self.cell.fp_linear_taper
            lv = cell.get_default_view(self)
            lv.set(
                in_width=self.fp_width,
                out_width=self.end_fp_taper_width,
                length=self.fp_taper_length,
            )
            return lv

        def _default_linear_taper_out(self):
            cell = self.cell.linear_taper_out
            lv = cell.get_default_view(self)
            lv.set(
                in_width=self.fp_width,
                out_width=1.8,
                length=self.linear_taper_out_length,
            )
            return lv

        def _generate_instances(self, insts):
            fp_waveguide = self.fp_waveguide
            fp_linear_taper = self.fp_linear_taper
            grating = self.grating
            linear_taper_out = self.linear_taper_out
            lensed_fiber = self.lensed_fiber

            insts += i3.SRef(name="fp_waveguide", reference=fp_waveguide, flatten=True)
            insts += i3.SRef(name="fp_linear_taper", reference=fp_linear_taper, flatten=True)
            insts += i3.SRef(name="linear_taper_out", reference=linear_taper_out, flatten=True)
            insts += i3.SRef(name="grating", reference=grating, flatten=True)
            insts += i3.SRef(name="lensed_fiber", reference=lensed_fiber, flatten=True)

            return i3.place_and_route(
                insts=insts,
                specs=[
                    i3.Place("fp_waveguide", (0, 0)),
                    i3.Place("fp_linear_taper", (0, 0), angle=180, relative_to="fp_waveguide:in0"),
                    i3.Place("lensed_fiber", (125, 0), angle=0, relative_to="fp_waveguide:out0"),
                    i3.Place("linear_taper_out", (25-15, 0), angle=0, relative_to="fp_waveguide:out0"),
                    i3.Place("grating:out", (0, 0), relative_to="fp_linear_taper:out0"),
                    i3.ConnectBend("linear_taper_out:out0", "lensed_fiber:in0"),
                    i3.ConnectBend("linear_taper_out:in0", "fp_waveguide:out0"),
                ]
            )

class BG_Test_4_lensed_fiber(i3.Circuit):
    fp_waveguide = i3.ChildCellProperty(doc="fabry perot waveguide")
    grating = i3.ChildCellProperty(doc="grating")
    fp_linear_taper = i3.ChildCellProperty(doc="linear taper")
    linear_taper_out = i3.ChildCellProperty(doc="linear taper")
    lensed_fiber = i3.ChildCellProperty(doc="lensed fiber")

    def _default_fp_waveguide(self):
        return pdk.Straight()

    def _default_fp_linear_taper(self):
        # return pdk.LinearTaperFromPort(start_trace_template = self.trace_template_in, end_trace_template = self.trace_template_out)
        return pdk.Taper()

    def _default_linear_taper_out(self):
        # return pdk.LinearTaperFromPort(start_trace_template = self.trace_template_in, end_trace_template = self.trace_template_out)
        return pdk.Taper()

    def _default_lensed_fiber(self):
        return pdk.AN800BB_EdgeCoupler_Lensed_C()


    def _default_grating(self):
        return BG_4()

    def _default_insts(self):
        return {"fp_waveguide": self.fp_waveguide,
                "fp_linear_taper": self.fp_linear_taper,
                "linear_taper_out": self.linear_taper_out,
                "lensed_fiber": self.lensed_fiber,
                "grating": self.grating,
                # "linear_transition_out": self.linear_transition,
                # # "linear_transition_in_ref": self.linear_transition,
                # # "linear_transition_out_ref": self.linear_transition,
                # # "in_taper_ref": self.taper,
                # # "out_taper_ref": self.taper,
                }

    def _default_specs(self):
        return [
            i3.Place("fp_waveguide", (0, 0)),
            i3.Place("fp_linear_taper", (0, 0), angle=180, relative_to="fp_waveguide:in0"),
            i3.Place("lensed_fiber", (125, 0), angle=0, relative_to="fp_waveguide:out0"),
            i3.Place("linear_taper_out", (25 - 15, 0), angle=0, relative_to="fp_waveguide:out0"),
            i3.Place("grating:out", (0, 0), relative_to="fp_linear_taper:out0"),
            i3.ConnectBend("linear_taper_out:out0", "lensed_fiber:in0"),
            i3.ConnectBend("linear_taper_out:in0", "fp_waveguide:out0"),
        ]

    class Layout(i3.LayoutView):
        fp_width = i3.PositiveNumberProperty(default=1.0, doc="width of fabry perot waveguide")
        fp_length = i3.PositiveNumberProperty(default=150.0, doc="length of fabry perot waveguide")
        end_fp_taper_width = i3.PositiveNumberProperty(default=0.5, doc="width of end fp taper port")
        fp_taper_length = i3.PositiveNumberProperty(default=50.0, doc="length of fp taper")
        tip_width = i3.PositiveNumberProperty(default=0.3, doc="tip width of linear taper out")
        linear_taper_out_length = i3.PositiveNumberProperty(default=100.0, doc="length of linear taper out")

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

        # print("BG_1:{}".format(BG_1_width_2[len(array_1) - 1]))

        def _default_fp_linear_taper(self):
            cell = self.cell.fp_linear_taper
            lv = cell.get_default_view(self)
            lv.set(
                in_width=self.fp_width,
                out_width=self.end_fp_taper_width,
                length=self.fp_taper_length,
            )
            return lv

        def _default_linear_taper_out(self):
            cell = self.cell.linear_taper_out
            lv = cell.get_default_view(self)
            lv.set(
                in_width=self.fp_width,
                out_width=1.8,
                length=self.linear_taper_out_length,
            )
            return lv

        def _generate_instances(self, insts):
            fp_waveguide = self.fp_waveguide
            fp_linear_taper = self.fp_linear_taper
            grating = self.grating
            linear_taper_out = self.linear_taper_out
            lensed_fiber = self.lensed_fiber

            insts += i3.SRef(name="fp_waveguide", reference=fp_waveguide, flatten=True)
            insts += i3.SRef(name="fp_linear_taper", reference=fp_linear_taper, flatten=True)
            insts += i3.SRef(name="linear_taper_out", reference=linear_taper_out, flatten=True)
            insts += i3.SRef(name="grating", reference=grating, flatten=True)
            insts += i3.SRef(name="lensed_fiber", reference=lensed_fiber, flatten=True)

            return i3.place_and_route(
                insts=insts,
                specs=[
                    i3.Place("fp_waveguide", (0, 0)),
                    i3.Place("fp_linear_taper", (0, 0), angle=180, relative_to="fp_waveguide:in0"),
                    i3.Place("lensed_fiber", (125, 0), angle=0, relative_to="fp_waveguide:out0"),
                    i3.Place("linear_taper_out", (25-15, 0), angle=0, relative_to="fp_waveguide:out0"),
                    i3.Place("grating:out", (0, 0), relative_to="fp_linear_taper:out0"),
                    i3.ConnectBend("linear_taper_out:out0", "lensed_fiber:in0"),
                    i3.ConnectBend("linear_taper_out:in0", "fp_waveguide:out0"),
                ]
            )

class BG_Test_5_lensed_fiber(i3.Circuit):
    fp_waveguide = i3.ChildCellProperty(doc="fabry perot waveguide")
    grating = i3.ChildCellProperty(doc="grating")
    fp_linear_taper = i3.ChildCellProperty(doc="linear taper")
    linear_taper_out = i3.ChildCellProperty(doc="linear taper")
    lensed_fiber = i3.ChildCellProperty(doc="lensed fiber")

    def _default_fp_waveguide(self):
        return pdk.Straight()

    def _default_fp_linear_taper(self):
        # return pdk.LinearTaperFromPort(start_trace_template = self.trace_template_in, end_trace_template = self.trace_template_out)
        return pdk.Taper()

    def _default_linear_taper_out(self):
        # return pdk.LinearTaperFromPort(start_trace_template = self.trace_template_in, end_trace_template = self.trace_template_out)
        return pdk.Taper()

    def _default_lensed_fiber(self):
        return pdk.AN800BB_EdgeCoupler_Lensed_C()

    def _default_grating(self):
        return BG_5()

    def _default_insts(self):
        return {"fp_waveguide": self.fp_waveguide,
                "fp_linear_taper": self.fp_linear_taper,
                "linear_taper_out": self.linear_taper_out,
                "lensed_fiber": self.lensed_fiber,
                "grating": self.grating,
                # "linear_transition_out": self.linear_transition,
                # # "linear_transition_in_ref": self.linear_transition,
                # # "linear_transition_out_ref": self.linear_transition,
                # # "in_taper_ref": self.taper,
                # # "out_taper_ref": self.taper,
                }

    def _default_specs(self):
        return [
            i3.Place("fp_waveguide", (0, 0)),
            i3.Place("fp_linear_taper", (0, 0), angle=180, relative_to="fp_waveguide:in0"),
            i3.Place("lensed_fiber", (125, 0), angle=0, relative_to="fp_waveguide:out0"),
            i3.Place("linear_taper_out", (25 - 15, 0), angle=0, relative_to="fp_waveguide:out0"),
            i3.Place("grating:out", (0, 0), relative_to="fp_linear_taper:out0"),
            i3.ConnectBend("linear_taper_out:out0", "lensed_fiber:in0"),
            i3.ConnectBend("linear_taper_out:in0", "fp_waveguide:out0"),
        ]

    class Layout(i3.LayoutView):
        fp_width = i3.PositiveNumberProperty(default=1.0, doc="width of fabry perot waveguide")
        fp_length = i3.PositiveNumberProperty(default=150.0, doc="length of fabry perot waveguide")
        end_fp_taper_width = i3.PositiveNumberProperty(default=0.5, doc="width of end fp taper port")
        fp_taper_length = i3.PositiveNumberProperty(default=50.0, doc="length of fp taper")
        tip_width = i3.PositiveNumberProperty(default=0.3, doc="tip width of linear taper out")
        linear_taper_out_length = i3.PositiveNumberProperty(default=100.0, doc="length of linear taper out")

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

        # print("BG_1:{}".format(BG_1_width_2[len(array_1) - 1]))

        def _default_fp_linear_taper(self):
            cell = self.cell.fp_linear_taper
            lv = cell.get_default_view(self)
            lv.set(
                in_width=self.fp_width,
                out_width=self.end_fp_taper_width,
                length=self.fp_taper_length,
            )
            return lv

        def _default_linear_taper_out(self):
            cell = self.cell.linear_taper_out
            lv = cell.get_default_view(self)
            lv.set(
                in_width=self.fp_width,
                out_width=1.8,
                length=self.linear_taper_out_length,
            )
            return lv

        def _generate_instances(self, insts):
            fp_waveguide = self.fp_waveguide
            fp_linear_taper = self.fp_linear_taper
            grating = self.grating
            linear_taper_out = self.linear_taper_out
            lensed_fiber = self.lensed_fiber

            insts += i3.SRef(name="fp_waveguide", reference=fp_waveguide, flatten=True)
            insts += i3.SRef(name="fp_linear_taper", reference=fp_linear_taper, flatten=True)
            insts += i3.SRef(name="linear_taper_out", reference=linear_taper_out, flatten=True)
            insts += i3.SRef(name="grating", reference=grating, flatten=True)
            insts += i3.SRef(name="lensed_fiber", reference=lensed_fiber, flatten=True)

            return i3.place_and_route(
                insts=insts,
                specs=[
                    i3.Place("fp_waveguide", (0, 0)),
                    i3.Place("fp_linear_taper", (0, 0), angle=180, relative_to="fp_waveguide:in0"),
                    i3.Place("lensed_fiber", (125, 0), angle=0, relative_to="fp_waveguide:out0"),
                    i3.Place("linear_taper_out", (25-15, 0), angle=0, relative_to="fp_waveguide:out0"),
                    i3.Place("grating:out", (0, 0), relative_to="fp_linear_taper:out0"),
                    i3.ConnectBend("linear_taper_out:out0", "lensed_fiber:in0"),
                    i3.ConnectBend("linear_taper_out:in0", "fp_waveguide:out0"),
                ]
            )

class BG_Test_6_lensed_fiber(i3.Circuit):
    fp_waveguide = i3.ChildCellProperty(doc="fabry perot waveguide")
    grating = i3.ChildCellProperty(doc="grating")
    fp_linear_taper = i3.ChildCellProperty(doc="linear taper")
    linear_taper_out = i3.ChildCellProperty(doc="linear taper")
    lensed_fiber = i3.ChildCellProperty(doc="lensed fiber")

    def _default_fp_waveguide(self):
        return pdk.Straight()

    def _default_fp_linear_taper(self):
        # return pdk.LinearTaperFromPort(start_trace_template = self.trace_template_in, end_trace_template = self.trace_template_out)
        return pdk.Taper()

    def _default_linear_taper_out(self):
        # return pdk.LinearTaperFromPort(start_trace_template = self.trace_template_in, end_trace_template = self.trace_template_out)
        return pdk.Taper()

    def _default_lensed_fiber(self):
        return pdk.AN800BB_EdgeCoupler_Lensed_C()

    def _default_grating(self):
        return BG_6()

    def _default_insts(self):
        return {"fp_waveguide": self.fp_waveguide,
                "fp_linear_taper": self.fp_linear_taper,
                "linear_taper_out": self.linear_taper_out,
                "lensed_fiber": self.lensed_fiber,
                "grating": self.grating,
                # "linear_transition_out": self.linear_transition,
                # # "linear_transition_in_ref": self.linear_transition,
                # # "linear_transition_out_ref": self.linear_transition,
                # # "in_taper_ref": self.taper,
                # # "out_taper_ref": self.taper,
                }

    def _default_specs(self):
        return [
            i3.Place("fp_waveguide", (0, 0)),
            i3.Place("fp_linear_taper", (0, 0), angle=180, relative_to="fp_waveguide:in0"),
            i3.Place("lensed_fiber", (125, 0), angle=0, relative_to="fp_waveguide:out0"),
            i3.Place("linear_taper_out", (25 - 15, 0), angle=0, relative_to="fp_waveguide:out0"),
            i3.Place("grating:out", (0, 0), relative_to="fp_linear_taper:out0"),
            i3.ConnectBend("linear_taper_out:out0", "lensed_fiber:in0"),
            i3.ConnectBend("linear_taper_out:in0", "fp_waveguide:out0"),
        ]

    class Layout(i3.LayoutView):
        fp_width = i3.PositiveNumberProperty(default=1.0, doc="width of fabry perot waveguide")
        fp_length = i3.PositiveNumberProperty(default=150.0, doc="length of fabry perot waveguide")
        end_fp_taper_width = i3.PositiveNumberProperty(default=0.5, doc="width of end fp taper port")
        fp_taper_length = i3.PositiveNumberProperty(default=50.0, doc="length of fp taper")
        tip_width = i3.PositiveNumberProperty(default=0.3, doc="tip width of linear taper out")
        linear_taper_out_length = i3.PositiveNumberProperty(default=100.0, doc="length of linear taper out")

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

        # print("BG_1:{}".format(BG_1_width_2[len(array_1) - 1]))

        def _default_fp_linear_taper(self):
            cell = self.cell.fp_linear_taper
            lv = cell.get_default_view(self)
            lv.set(
                in_width=self.fp_width,
                out_width=self.end_fp_taper_width,
                length=self.fp_taper_length,
            )
            return lv

        def _default_linear_taper_out(self):
            cell = self.cell.linear_taper_out
            lv = cell.get_default_view(self)
            lv.set(
                in_width=self.fp_width,
                out_width=1.8,
                length=self.linear_taper_out_length,
            )
            return lv


        def _generate_instances(self, insts):
            fp_waveguide = self.fp_waveguide
            fp_linear_taper = self.fp_linear_taper
            grating = self.grating
            linear_taper_out = self.linear_taper_out
            lensed_fiber = self.lensed_fiber

            insts += i3.SRef(name="fp_waveguide", reference=fp_waveguide, flatten=True)
            insts += i3.SRef(name="fp_linear_taper", reference=fp_linear_taper, flatten=True)
            insts += i3.SRef(name="linear_taper_out", reference=linear_taper_out, flatten=True)
            insts += i3.SRef(name="grating", reference=grating, flatten=True)
            insts += i3.SRef(name="lensed_fiber", reference=lensed_fiber, flatten=True)

            return i3.place_and_route(
                insts=insts,
                specs=[
                    i3.Place("fp_waveguide", (0, 0)),
                    i3.Place("fp_linear_taper", (0, 0), angle=180, relative_to="fp_waveguide:in0"),
                    i3.Place("lensed_fiber", (125, 0), angle=0, relative_to="fp_waveguide:out0"),
                    i3.Place("linear_taper_out", (25-15, 0), angle=0, relative_to="fp_waveguide:out0"),
                    i3.Place("grating:out", (0, 0), relative_to="fp_linear_taper:out0"),
                    i3.ConnectBend("linear_taper_out:out0", "lensed_fiber:in0"),
                    i3.ConnectBend("linear_taper_out:in0", "fp_waveguide:out0"),
                ]
            )

class BG_Test_7_lensed_fiber(i3.Circuit):
    fp_waveguide = i3.ChildCellProperty(doc="fabry perot waveguide")
    grating = i3.ChildCellProperty(doc="grating")
    fp_linear_taper = i3.ChildCellProperty(doc="linear taper")
    linear_taper_out = i3.ChildCellProperty(doc="linear taper")
    lensed_fiber = i3.ChildCellProperty(doc="lensed fiber")

    def _default_fp_waveguide(self):
        return pdk.Straight()

    def _default_fp_linear_taper(self):
        # return pdk.LinearTaperFromPort(start_trace_template = self.trace_template_in, end_trace_template = self.trace_template_out)
        return pdk.Taper()

    def _default_linear_taper_out(self):
        # return pdk.LinearTaperFromPort(start_trace_template = self.trace_template_in, end_trace_template = self.trace_template_out)
        return pdk.Taper()

    def _default_lensed_fiber(self):
        return pdk.AN800BB_EdgeCoupler_Lensed_C()

    def _default_grating(self):
        return BG_7()

    def _default_insts(self):
        return {"fp_waveguide": self.fp_waveguide,
                "fp_linear_taper": self.fp_linear_taper,
                "linear_taper_out": self.linear_taper_out,
                "lensed_fiber": self.lensed_fiber,
                "grating": self.grating,
                # "linear_transition_out": self.linear_transition,
                # # "linear_transition_in_ref": self.linear_transition,
                # # "linear_transition_out_ref": self.linear_transition,
                # # "in_taper_ref": self.taper,
                # # "out_taper_ref": self.taper,
                }

    def _default_specs(self):
        return [
            i3.Place("fp_waveguide", (0, 0)),
            i3.Place("fp_linear_taper", (0, 0), angle=180, relative_to="fp_waveguide:in0"),
            i3.Place("lensed_fiber", (125, 0), angle=0, relative_to="fp_waveguide:out0"),
            i3.Place("linear_taper_out", (25 - 15, 0), angle=0, relative_to="fp_waveguide:out0"),
            i3.Place("grating:out", (0, 0), relative_to="fp_linear_taper:out0"),
            i3.ConnectBend("linear_taper_out:out0", "lensed_fiber:in0"),
            i3.ConnectBend("linear_taper_out:in0", "fp_waveguide:out0"),
        ]

    class Layout(i3.LayoutView):
        fp_width = i3.PositiveNumberProperty(default=1.0, doc="width of fabry perot waveguide")
        fp_length = i3.PositiveNumberProperty(default=150.0, doc="length of fabry perot waveguide")
        end_fp_taper_width = i3.PositiveNumberProperty(default=0.5, doc="width of end fp taper port")
        fp_taper_length = i3.PositiveNumberProperty(default=50.0, doc="length of fp taper")
        tip_width = i3.PositiveNumberProperty(default=0.3, doc="tip width of linear taper out")
        linear_taper_out_length = i3.PositiveNumberProperty(default=100.0, doc="length of linear taper out")

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

        # print("BG_1:{}".format(BG_1_width_2[len(array_1) - 1]))

        def _default_fp_linear_taper(self):
            cell = self.cell.fp_linear_taper
            lv = cell.get_default_view(self)
            lv.set(
                in_width=self.fp_width,
                out_width=self.end_fp_taper_width,
                length=self.fp_taper_length,
            )
            return lv

        def _default_linear_taper_out(self):
            cell = self.cell.linear_taper_out
            lv = cell.get_default_view(self)
            lv.set(
                in_width=self.fp_width,
                out_width=1.8,
                length=self.linear_taper_out_length,
            )
            return lv

        def _generate_instances(self, insts):
            fp_waveguide = self.fp_waveguide
            fp_linear_taper = self.fp_linear_taper
            grating = self.grating
            linear_taper_out = self.linear_taper_out
            lensed_fiber = self.lensed_fiber

            insts += i3.SRef(name="fp_waveguide", reference=fp_waveguide, flatten=True)
            insts += i3.SRef(name="fp_linear_taper", reference=fp_linear_taper, flatten=True)
            insts += i3.SRef(name="linear_taper_out", reference=linear_taper_out, flatten=True)
            insts += i3.SRef(name="grating", reference=grating, flatten=True)
            insts += i3.SRef(name="lensed_fiber", reference=lensed_fiber, flatten=True)

            return i3.place_and_route(
                insts=insts,
                specs=[
                    i3.Place("fp_waveguide", (0, 0)),
                    i3.Place("fp_linear_taper", (0, 0), angle=180, relative_to="fp_waveguide:in0"),
                    i3.Place("lensed_fiber", (125, 0), angle=0, relative_to="fp_waveguide:out0"),
                    i3.Place("linear_taper_out", (25-15, 0), angle=0, relative_to="fp_waveguide:out0"),
                    i3.Place("grating:out", (0, 0), relative_to="fp_linear_taper:out0"),
                    i3.ConnectBend("linear_taper_out:out0", "lensed_fiber:in0"),
                    i3.ConnectBend("linear_taper_out:in0", "fp_waveguide:out0"),
                ]
            )

class BG_Test_8_lensed_fiber(i3.Circuit):
    fp_waveguide = i3.ChildCellProperty(doc="fabry perot waveguide")
    grating = i3.ChildCellProperty(doc="grating")
    fp_linear_taper = i3.ChildCellProperty(doc="linear taper")
    linear_taper_out = i3.ChildCellProperty(doc="linear taper")
    lensed_fiber = i3.ChildCellProperty(doc="lensed fiber")

    def _default_fp_waveguide(self):
        return pdk.Straight()

    def _default_fp_linear_taper(self):
        # return pdk.LinearTaperFromPort(start_trace_template = self.trace_template_in, end_trace_template = self.trace_template_out)
        return pdk.Taper()

    def _default_linear_taper_out(self):
        # return pdk.LinearTaperFromPort(start_trace_template = self.trace_template_in, end_trace_template = self.trace_template_out)
        return pdk.Taper()

    def _default_lensed_fiber(self):
        return pdk.AN800BB_EdgeCoupler_Lensed_C()

    def _default_grating(self):
        return BG_8()

    # def _default_insts(self):
    #     return {"fp_waveguide": self.fp_waveguide,
    #             "fp_linear_taper": self.fp_linear_taper,
    #             "linear_taper_out": self.linear_taper_out,
    #             "lensed_fiber": self.lensed_fiber,
    #             "grating": self.grating,
    #             # "linear_transition_out": self.linear_transition,
    #             # # "linear_transition_in_ref": self.linear_transition,
    #             # # "linear_transition_out_ref": self.linear_transition,
    #             # # "in_taper_ref": self.taper,
    #             # # "out_taper_ref": self.taper,
    #             }

    # def _default_specs(self):
    #     return [
    #         i3.Place("fp_waveguide", (0, 0)),
    #         i3.Place("fp_linear_taper", (0, 0), angle=180, relative_to="fp_waveguide:in0"),
    #         i3.Place("lensed_fiber", (125, 0), angle=0, relative_to="fp_waveguide:out0"),
    #         i3.Place("linear_taper_out", (25 - 15, 0), angle=0, relative_to="fp_waveguide:out0"),
    #         i3.Place("grating:out", (0, 0), relative_to="fp_linear_taper:out0"),
    #         i3.ConnectBend("linear_taper_out:out0", "lensed_fiber:in0"),
    #         i3.ConnectBend("linear_taper_out:in0", "fp_waveguide:out0"),
    #     ]

    class Layout(i3.LayoutView):
        fp_width = i3.PositiveNumberProperty(default=1.0, doc="width of fabry perot waveguide")
        fp_length = i3.PositiveNumberProperty(default=150.0, doc="length of fabry perot waveguide")
        end_fp_taper_width = i3.PositiveNumberProperty(default=0.5, doc="width of end fp taper port")
        fp_taper_length = i3.PositiveNumberProperty(default=50.0, doc="length of fp taper")
        tip_width = i3.PositiveNumberProperty(default=0.3, doc="tip width of linear taper out")
        linear_taper_out_length = i3.PositiveNumberProperty(default=100.0, doc="length of linear taper out")

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

        # print("BG_1:{}".format(BG_1_width_2[len(array_1) - 1]))

        def _default_fp_linear_taper(self):
            cell = self.cell.fp_linear_taper
            lv = cell.get_default_view(self)
            lv.set(
                in_width=self.fp_width,
                out_width=self.end_fp_taper_width,
                length=self.fp_taper_length,
            )
            return lv

        def _default_linear_taper_out(self):
            cell = self.cell.linear_taper_out
            lv = cell.get_default_view(self)
            lv.set(
                in_width=self.fp_width,
                out_width=1.8,
                length=self.linear_taper_out_length,
            )
            return lv

        def _generate_instances(self, insts):
            fp_waveguide = self.fp_waveguide
            fp_linear_taper = self.fp_linear_taper
            grating = self.grating
            linear_taper_out = self.linear_taper_out
            lensed_fiber = self.lensed_fiber

            insts += i3.SRef(name="fp_waveguide", reference=fp_waveguide, flatten=True)
            insts += i3.SRef(name="fp_linear_taper", reference=fp_linear_taper, flatten=True)
            insts += i3.SRef(name="linear_taper_out", reference=linear_taper_out, flatten=True)
            insts += i3.SRef(name="grating", reference=grating, flatten=True)
            insts += i3.SRef(name="lensed_fiber", reference=lensed_fiber, flatten=True)

            return i3.place_and_route(
                insts=insts,
                specs=[
                    i3.Place("fp_waveguide", (0, 0)),
                    i3.Place("fp_linear_taper", (0, 0), angle=180, relative_to="fp_waveguide:in0"),
                    i3.Place("lensed_fiber", (125, 0), angle=0, relative_to="fp_waveguide:out0"),
                    i3.Place("linear_taper_out", (25-15, 0), angle=0, relative_to="fp_waveguide:out0"),
                    i3.Place("grating:out", (0, 0), relative_to="fp_linear_taper:out0"),
                    i3.ConnectBend("linear_taper_out:out0", "lensed_fiber:in0"),
                    i3.ConnectBend("linear_taper_out:in0", "fp_waveguide:out0"),
                ]
            )

# class BG_Test_Sinusoidal(i3.Circuit):
#     fp_waveguide = i3.ChildCellProperty(doc="fabry perot waveguide")
#     grating = i3.ChildCellProperty(doc="grating")
#     fp_linear_taper = i3.ChildCellProperty(doc="linear taper")
#     linear_taper_out = i3.ChildCellProperty(doc="linear taper")
#     grating_taper = i3.ChildCellProperty(doc="grating")
#     lensed_fiber = i3.ChildCellProperty(doc="lensed fiber")
#
#     def _default_fp_waveguide(self):
#         return pdk.Straight()
#
#     def _default_fp_linear_taper(self):
#         # return pdk.LinearTaperFromPort(start_trace_template = self.trace_template_in, end_trace_template = self.trace_template_out)
#         return pdk.Taper()
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
#     def _default_grating_taper(self):
#         return SinusoidalGratingTaper()
#
#     class Layout(i3.LayoutView):
#         fp_width = i3.PositiveNumberProperty(default=1.0, doc="width of fabry perot waveguide")
#         fp_length = i3.PositiveNumberProperty(default=150.0, doc="length of fabry perot waveguide")
#         end_fp_taper_width = i3.PositiveNumberProperty(default=0.5, doc="width of end fp taper port")
#         fp_taper_length = i3.PositiveNumberProperty(default=50.0, doc="length of fp taper")
#         tip_width = i3.PositiveNumberProperty(default=0.3, doc="tip width of linear taper out")
#         linear_taper_out_length = i3.PositiveNumberProperty(default=250.0, doc="length of linear taper out")
#
#         def _default_fp_waveguide(self):
#             cell = self.cell.fp_waveguide
#             lv = cell.get_default_view(self)
#             lv.set(
#                 width=self.fp_width,
#                 length=self.fp_length,
#             )
#             return lv
#
#         def _default_end_fp_taper_width(self):
#             return BG_1_width_2[len(array_1)-1]
#
#         # print("BG_1:{}".format(BG_1_width_2[len(array_1) - 1]))
#
#         def _default_linear_taper_out(self):
#             cell = self.cell.linear_taper_out
#             lv = cell.get_default_view(self)
#             lv.set(
#                 in_width=self.fp_width,
#                 out_width=1.8,
#                 length=self.linear_taper_out_length,
#             )
#             return lv
#
#         def _default_fp_linear_taper(self):
#             cell = self.cell.fp_linear_taper
#             lv = cell.get_default_view(self)
#             lv.set(
#                 in_width=self.fp_width,
#                 out_width=0.6,
#             )
#             return lv
#
#         def _generate_instances(self, insts):
#             fp_waveguide = self.fp_waveguide
#             fp_linear_taper = self.fp_linear_taper
#             grating = self.grating
#             grating_taper = self.grating_taper
#             linear_taper_out = self.linear_taper_out
#             lensed_fiber = self.lensed_fiber
#
#             insts += i3.SRef(name="fp_waveguide", reference=fp_waveguide, flatten=True)
#             insts += i3.SRef(name="fp_linear_taper", reference=fp_linear_taper, flatten=True)
#             insts += i3.SRef(name="linear_taper_out", reference=linear_taper_out, flatten=True)
#             insts += i3.SRef(name="grating", reference=grating, flatten=True)
#             insts += i3.SRef(name="grating_taper", reference=grating_taper, flatten=True)
#             insts += i3.SRef(name="grating_taper_2", reference=grating_taper, flatten=True)
#             insts += i3.SRef(name="lensed_fiber", reference=lensed_fiber, flatten=True)
#
#             return i3.place_and_route(
#                 insts=insts,
#                 specs=[
#                     i3.Place("fp_waveguide", (0, 0)),
#                     i3.Place("fp_linear_taper", (0, 0), angle=180, relative_to="fp_waveguide:in0"),
#                     i3.Place("grating_taper", (0, 0), angle=180, relative_to="fp_linear_taper:out0"),
#                     i3.Place("linear_taper_out", (0, 0), angle=0, relative_to="fp_waveguide:out0"),
#                     i3.Place("grating", (0, 0), angle=180, relative_to="grating_taper:out"),
#                     i3.Place("grating_taper_2", (-47.5+0.475/2, 0), angle=180, relative_to="grating:out"),
#                     i3.FlipH("grating_taper_2")
#                 ]
#             )



