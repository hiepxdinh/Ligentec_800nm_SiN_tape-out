import sys

import ligentec_an800.all as pdk

import ipkiss3.all as i3
import numpy as np
from numpy.ma.core import angle

class All_pass_ring_GC(i3.Circuit):
    taper = i3.ChildCellProperty(doc="inverse_taper coupler")
    ring_in = i3.ChildCellProperty(doc="ring resonator")
    ring_out = i3.ChildCellProperty(doc="ring resonator")
    # trace_template_in = i3.TraceTemplateProperty(doc="waveguide template used in the circuit")
    # trace_template_out = i3.TraceTemplateProperty(doc="waveguide template used in the circuit")

    ring_position_x = i3.NumberProperty(default=0.0, doc="the x position of ring")
    ring_position_y = i3.NumberProperty(default=0.0, doc="the y position of ring")

    output_offset = i3.NumberProperty(default=100, doc="offset from ring output")

    out_taper_position = i3.NumberProperty(default=0, doc="out taper position")

    linear_transition = i3.ChildCellProperty(doc="linear transition waveguide")

    def _default_taper(self):
        return pdk.AN800BB_FGC_8_TE_C()

    def _default_ring_in(self):
        return pdk.MMI1x2()

    def _default_ring_out(self):
        return pdk.MMI1x2()

    # def _default_trace_template_in(self):
    #     return pdk.WireWaveguideTemplate()
    #
    # def _default_trace_template_out(self):
    #     return pdk.WireWaveguideTemplate()

    def _default_linear_transition(self):
        # return pdk.LinearTaperFromPort(start_trace_template = self.trace_template_in, end_trace_template = self.trace_template_out)
        return pdk.Taper()



    def _default_insts(self):
        return {"ring_in": self.ring_in,
                "ring_out": self.ring_out,
                "in_taper": self.taper,
                "out_taper": self.taper,
                # "linear_transition_in": self.linear_transition,
                # "linear_transition_out": self.linear_transition,
                }

    def _default_specs(self):

        ring_position = (self.ring_position_x, self.ring_position_y)

        return [
            i3.Place('ring_in', (355, 0), angle=0),
            i3.FlipH('ring_in'),
            i3.Place('ring_out', (0, 0), angle=0),

            i3.Place("in_taper", position=(10, 0), angle=0, relative_to="ring_in:in0"),
            i3.Place("out_taper", position=(-10, 0), angle=180, relative_to="ring_out:in0"),

            i3.ConnectManhattan("ring_in:out0", "ring_out:out0",
                                control_points=[i3.H(i3.START - 200),
                                                ],
        ),


            i3.ConnectManhattan("ring_in:out1", "ring_out:out1",
                                control_points=[i3.H(i3.START + 250),
                                                ],
                                ),
            #
            i3.ConnectBend("ring_in:in0", "in_taper:in0"),
            i3.ConnectBend("ring_out:in0", "out_taper:in0"),

        ]

    class Layout(i3.Circuit.Layout):
        # horizontal_spacing = i3.PositiveNumberProperty(default=9000, doc="horizontal spacing between input and output inverse_taper couplers")
        ring_radius = i3.PositiveNumberProperty(default=50.0, doc="radius of the ring")
        ring_gap = i3.PositiveNumberProperty(default=0.7, doc="the gap ")
        # ring_position_x=i3.NumberProperty (default=0.0, doc="the x position of ring")
        # ring_position_y=i3.NumberProperty (default=0.0, doc="the y position of ring")
        # ebl_field_size = i3.PositiveNumberProperty(default=100.0, doc="the ebl writing field size")
        #
        # v_separation = i3.NumberProperty(default=0.7, doc="the gap ")
        width_in = i3.PositiveNumberProperty(default=1.0, doc="width of input waveguide")
        width_out = i3.PositiveNumberProperty(default=1.8, doc="width of output waveguide")


        def _default_ring(self):
            lo = self.cell.ring_in.get_default_view(i3.LayoutView)
            # lo.set(radius=self.ring_radius)
            lo.set(gap0=self.ring_gap)
            return lo

        # def _default_trace_template_in(self):
        #     lo=self.cell.trace_template_in.get_default_view(i3.LayoutView)
        #     lo.set(core_width=self.width_in)
        #     return lo
        #
        # def _default_trace_template_out(self):
        #     lo=self.cell.trace_template_out.get_default_view(i3.LayoutView)
        #     lo.set(core_width=self.width_out)
        #     return lo

        def _default_linear_transition(self):
            cell = self.cell.linear_transition
            lv = cell.get_default_view(self)
            lv.set(
                in_width=self.width_in,
                out_width=self.width_out
            )
            return lv


class All_pass_ring_GC_2(i3.Circuit):
    taper = i3.ChildCellProperty(doc="inverse_taper coupler")
    ring = i3.ChildCellProperty(doc="ring resonator")
    # trace_template_in = i3.TraceTemplateProperty(doc="waveguide template used in the circuit")
    # trace_template_out = i3.TraceTemplateProperty(doc="waveguide template used in the circuit")

    ring_position_x = i3.NumberProperty(default=0.0, doc="the x position of ring")
    ring_position_y = i3.NumberProperty(default=0.0, doc="the y position of ring")

    output_offset = i3.NumberProperty(default=100, doc="offset from ring output")

    out_taper_position = i3.NumberProperty(default=0, doc="out taper position")

    linear_transition = i3.ChildCellProperty(doc="linear transition waveguide")

    def _default_taper(self):
        return pdk.AN800BB_FGC_8_TE_C()

    def _default_ring(self):
        return pdk.NotchRacetrack()

    # def _default_trace_template_in(self):
    #     return pdk.WireWaveguideTemplate()
    #
    # def _default_trace_template_out(self):
    #     return pdk.WireWaveguideTemplate()

    def _default_linear_transition(self):
        # return pdk.LinearTaperFromPort(start_trace_template = self.trace_template_in, end_trace_template = self.trace_template_out)
        return pdk.Taper()



    def _default_insts(self):
        return {"ring": self.ring,
                "in_taper": self.taper,
                "out_taper": self.taper,
                "linear_transition_in": self.linear_transition,
                "linear_transition_out": self.linear_transition,
                }

    def _default_specs(self):

        ring_position = (self.ring_position_x, self.ring_position_y)

        return [
            i3.Place('ring', position=ring_position, angle=0),
            i3.FlipV('ring'),
            i3.Place("linear_transition_in", position=(-2350/2+620+100+300, 0), angle=180, relative_to="ring:in0"),
            i3.Place("linear_transition_out", position=(2350/2-620-100-300, 0), angle=0, relative_to="ring:out0"),

            i3.Place('in_taper', position=(-15, 0), angle=0, relative_to="linear_transition_in:out0"),
            i3.FlipH("in_taper"),
            i3.Place('out_taper', position=(15, 0), angle=0, relative_to="linear_transition_out:out0"),

            i3.ConnectBend("in_taper:in0", "linear_transition_in:out0"),
            i3.ConnectBend("out_taper:in0", "linear_transition_out:out0"),

            i3.ConnectBend("ring:in0", "linear_transition_in:in0"),
            i3.ConnectBend("ring:out0", "linear_transition_out:in0"),

        ]

    class Layout(i3.Circuit.Layout):
        # horizontal_spacing = i3.PositiveNumberProperty(default=9000, doc="horizontal spacing between input and output inverse_taper couplers")
        ring_radius = i3.PositiveNumberProperty(default=50.0, doc="radius of the ring")
        ring_gap = i3.PositiveNumberProperty(default=0.7, doc="the gap ")
        # ring_position_x=i3.NumberProperty (default=0.0, doc="the x position of ring")
        # ring_position_y=i3.NumberProperty (default=0.0, doc="the y position of ring")
        # ebl_field_size = i3.PositiveNumberProperty(default=100.0, doc="the ebl writing field size")
        #
        # v_separation = i3.NumberProperty(default=0.7, doc="the gap ")
        width_in = i3.PositiveNumberProperty(default=1.8, doc="width of input waveguide")
        width_out = i3.PositiveNumberProperty(default=1.0, doc="width of output waveguide")


        def _default_ring(self):
            lo = self.cell.ring.get_default_view(i3.LayoutView)
            lo.set(radius=self.ring_radius)
            lo.set(ring_width = self.width_in)
            lo.set(gap0=self.ring_gap)
            return lo

        # def _default_trace_template_in(self):
        #     lo=self.cell.trace_template_in.get_default_view(i3.LayoutView)
        #     lo.set(core_width=self.width_in)
        #     return lo
        #
        # def _default_trace_template_out(self):
        #     lo=self.cell.trace_template_out.get_default_view(i3.LayoutView)
        #     lo.set(core_width=self.width_out)
        #     return lo

        def _default_linear_transition(self):
            cell = self.cell.linear_transition
            lv = cell.get_default_view(self)
            lv.set(
                in_width=self.width_in,
                out_width=self.width_out,
                length=100
            )
            return lv

        def _generate_elements(self, elems):
            """
            add labels at in/out put grating couplers regions
            """
            ring_position = (0,0)

            elems += i3.PolygonText(
                layer=i3.TECH.PPLAYER.X1P,
                coordinate=(-100, 18),
                text="R_G" +str(self.ring_gap),
                alignment=(i3.TEXT.ALIGN.CENTER, i3.TEXT.ALIGN.CENTER),
                font=i3.TEXT.FONT.DEFAULT,
                height=10,
                # transformation=i3.VMirror()
            )
            return elems


class All_pass_ring_GC_3(i3.Circuit):
    taper = i3.ChildCellProperty(doc="inverse_taper coupler")
    ring = i3.ChildCellProperty(doc="ring resonator")
    # trace_template_in = i3.TraceTemplateProperty(doc="waveguide template used in the circuit")
    # trace_template_out = i3.TraceTemplateProperty(doc="waveguide template used in the circuit")

    ring_position_x = i3.NumberProperty(default=0.0, doc="the x position of ring")
    ring_position_y = i3.NumberProperty(default=0.0, doc="the y position of ring")

    output_offset = i3.NumberProperty(default=100, doc="offset from ring output")

    out_taper_position = i3.NumberProperty(default=0, doc="out taper position")

    linear_transition = i3.ChildCellProperty(doc="linear transition waveguide")

    def _default_taper(self):
        return pdk.AN800BB_FGC_8_TE_C()

    def _default_ring(self):
        return pdk.NotchRacetrack()

    # def _default_trace_template_in(self):
    #     return pdk.WireWaveguideTemplate()
    #
    # def _default_trace_template_out(self):
    #     return pdk.WireWaveguideTemplate()

    def _default_linear_transition(self):
        # return pdk.LinearTaperFromPort(start_trace_template = self.trace_template_in, end_trace_template = self.trace_template_out)
        return pdk.Taper()



    def _default_insts(self):
        return {"ring": self.ring,
                "in_taper": self.taper,
                "out_taper": self.taper,
                "linear_transition_in": self.linear_transition,
                "linear_transition_out": self.linear_transition,
                }

    def _default_specs(self):

        ring_position = (self.ring_position_x, self.ring_position_y)

        return [
            i3.Place('ring', position=ring_position, angle=0),
            i3.FlipV('ring'),
            i3.Place("linear_transition_in", position=(-2350/2+620+100+300+100, 0), angle=180, relative_to="ring:in0"),
            i3.Place("linear_transition_out", position=(2350/2-620-100-300-100, 0), angle=0, relative_to="ring:out0"),

            i3.Place('in_taper', position=(-15, 0), angle=0, relative_to="linear_transition_in:out0"),
            i3.FlipH("in_taper"),
            i3.Place('out_taper', position=(15, 0), angle=0, relative_to="linear_transition_out:out0"),

            i3.ConnectBend("in_taper:in0", "linear_transition_in:out0"),
            i3.ConnectBend("out_taper:in0", "linear_transition_out:out0"),

            i3.ConnectBend("ring:in0", "linear_transition_in:in0"),
            i3.ConnectBend("ring:out0", "linear_transition_out:in0"),

        ]

    class Layout(i3.Circuit.Layout):
        # horizontal_spacing = i3.PositiveNumberProperty(default=9000, doc="horizontal spacing between input and output inverse_taper couplers")
        ring_radius = i3.PositiveNumberProperty(default=23.3, doc="radius of the ring")
        ring_gap = i3.PositiveNumberProperty(default=0.7, doc="the gap ")
        # ring_position_x=i3.NumberProperty (default=0.0, doc="the x position of ring")
        # ring_position_y=i3.NumberProperty (default=0.0, doc="the y position of ring")
        # ebl_field_size = i3.PositiveNumberProperty(default=100.0, doc="the ebl writing field size")
        #
        # v_separation = i3.NumberProperty(default=0.7, doc="the gap ")
        width_in = i3.PositiveNumberProperty(default=0.6, doc="width of input waveguide")
        width_out = i3.PositiveNumberProperty(default=1.0, doc="width of output waveguide")

        ring_width = i3.PositiveNumberProperty(default=2.6, doc="width of input waveguide")

        bus_length = i3.PositiveNumberProperty(default=100, doc="width of input waveguide")

        def _default_ring(self):
            lo = self.cell.ring.get_default_view(i3.LayoutView)
            lo.set(radius=self.ring_radius)
            lo.set(ring_width = self.ring_width)
            lo.set(gap0=self.ring_gap)
            lo.set(bus0_width=self.width_in)
            lo.set(bus0_length = self.bus_length)
            return lo

        # def _default_trace_template_in(self):
        #     lo=self.cell.trace_template_in.get_default_view(i3.LayoutView)
        #     lo.set(core_width=self.width_in)
        #     return lo
        #
        # def _default_trace_template_out(self):
        #     lo=self.cell.trace_template_out.get_default_view(i3.LayoutView)
        #     lo.set(core_width=self.width_out)
        #     return lo

        def _default_linear_transition(self):
            cell = self.cell.linear_transition
            lv = cell.get_default_view(self)
            lv.set(
                in_width=self.width_in,
                out_width=self.width_out,
                length=100
            )
            return lv

        def _generate_elements(self, elems):
            """
            add labels at in/out put grating couplers regions
            """
            ring_position = (0,0)

            elems += i3.PolygonText(
                layer=i3.TECH.PPLAYER.X1P,
                coordinate=(-100, 18),
                text="R_W" +str(self.ring_width),
                alignment=(i3.TEXT.ALIGN.CENTER, i3.TEXT.ALIGN.CENTER),
                font=i3.TEXT.FONT.DEFAULT,
                height=10,
                # transformation=i3.VMirror()
            )
            return elems

class All_pass_ring_GC_4(i3.Circuit):
    taper = i3.ChildCellProperty(doc="inverse_taper coupler")
    ring = i3.ChildCellProperty(doc="ring resonator")
    # trace_template_in = i3.TraceTemplateProperty(doc="waveguide template used in the circuit")
    # trace_template_out = i3.TraceTemplateProperty(doc="waveguide template used in the circuit")

    ring_position_x = i3.NumberProperty(default=0.0, doc="the x position of ring")
    ring_position_y = i3.NumberProperty(default=0.0, doc="the y position of ring")

    output_offset = i3.NumberProperty(default=100, doc="offset from ring output")

    out_taper_position = i3.NumberProperty(default=0, doc="out taper position")

    linear_transition = i3.ChildCellProperty(doc="linear transition waveguide")

    def _default_taper(self):
        return pdk.AN800BB_FGC_8_TE_C()

    def _default_ring(self):
        return pdk.NotchRacetrack()

    # def _default_trace_template_in(self):
    #     return pdk.WireWaveguideTemplate()
    #
    # def _default_trace_template_out(self):
    #     return pdk.WireWaveguideTemplate()

    def _default_linear_transition(self):
        # return pdk.LinearTaperFromPort(start_trace_template = self.trace_template_in, end_trace_template = self.trace_template_out)
        return pdk.Taper()



    def _default_insts(self):
        return {"ring": self.ring,
                "in_taper": self.taper,
                "out_taper": self.taper,
                "linear_transition_in": self.linear_transition,
                "linear_transition_out": self.linear_transition,
                }

    def _default_specs(self):

        ring_position = (self.ring_position_x, self.ring_position_y)

        return [
            i3.Place('ring', position=ring_position, angle=0),
            i3.FlipV('ring'),
            i3.Place("linear_transition_in", position=(-2350/2+620+100+300+100+35+5, 0), angle=180, relative_to="ring:in0"),
            i3.Place("linear_transition_out", position=(2350/2-620-100-300-100-35-5, 0), angle=0, relative_to="ring:out0"),

            i3.Place('in_taper', position=(-15, 0), angle=0, relative_to="linear_transition_in:out0"),
            i3.FlipH("in_taper"),
            i3.Place('out_taper', position=(15, 0), angle=0, relative_to="linear_transition_out:out0"),

            i3.ConnectBend("in_taper:in0", "linear_transition_in:out0"),
            i3.ConnectBend("out_taper:in0", "linear_transition_out:out0"),

            i3.ConnectBend("ring:in0", "linear_transition_in:in0"),
            i3.ConnectBend("ring:out0", "linear_transition_out:in0"),

        ]

    class Layout(i3.Circuit.Layout):
        # horizontal_spacing = i3.PositiveNumberProperty(default=9000, doc="horizontal spacing between input and output inverse_taper couplers")
        ring_radius = i3.PositiveNumberProperty(default=23.3, doc="radius of the ring")
        ring_gap = i3.PositiveNumberProperty(default=0.7, doc="the gap ")
        # ring_position_x=i3.NumberProperty (default=0.0, doc="the x position of ring")
        # ring_position_y=i3.NumberProperty (default=0.0, doc="the y position of ring")
        # ebl_field_size = i3.PositiveNumberProperty(default=100.0, doc="the ebl writing field size")
        #
        # v_separation = i3.NumberProperty(default=0.7, doc="the gap ")
        width_in = i3.PositiveNumberProperty(default=0.6, doc="width of input waveguide")
        width_out = i3.PositiveNumberProperty(default=1.0, doc="width of output waveguide")

        ring_width = i3.PositiveNumberProperty(default=2.6, doc="width of input waveguide")

        bus_length = i3.PositiveNumberProperty(default=100, doc="width of input waveguide")

        def _default_ring(self):
            lo = self.cell.ring.get_default_view(i3.LayoutView)
            lo.set(radius=self.ring_radius)
            lo.set(ring_width = self.ring_width)
            lo.set(gap0=self.ring_gap)
            lo.set(bus0_width=self.width_in)
            lo.set(bus0_length = self.bus_length)
            return lo

        # def _default_trace_template_in(self):
        #     lo=self.cell.trace_template_in.get_default_view(i3.LayoutView)
        #     lo.set(core_width=self.width_in)
        #     return lo
        #
        # def _default_trace_template_out(self):
        #     lo=self.cell.trace_template_out.get_default_view(i3.LayoutView)
        #     lo.set(core_width=self.width_out)
        #     return lo

        def _default_linear_transition(self):
            cell = self.cell.linear_transition
            lv = cell.get_default_view(self)
            lv.set(
                in_width=self.width_in,
                out_width=self.width_out,
                length=100
            )
            return lv

        def _generate_elements(self, elems):
            """
            add labels at in/out put grating couplers regions
            """
            ring_position = (0,0)

            elems += i3.PolygonText(
                layer=i3.TECH.PPLAYER.X1P,
                coordinate=(-80, 18),
                text="R_W" +str(self.ring_width),
                alignment=(i3.TEXT.ALIGN.CENTER, i3.TEXT.ALIGN.CENTER),
                font=i3.TEXT.FONT.DEFAULT,
                height=10,
                # transformation=i3.VMirror()
            )
            return elems
