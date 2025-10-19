import sys

import ligentec_an800.all as pdk

import ipkiss3.all as i3
import numpy as np
from numpy.ma.core import angle

class All_pass_ring_Exspot(i3.Circuit):
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
        return pdk.AN800BB_ExSpot_SMF_C()

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
            i3.Place("linear_transition_in", position=(-2350/2+620+100, 0), angle=180, relative_to="ring:in0"),
            i3.Place("linear_transition_out", position=(2350/2-620-100, 0), angle=0, relative_to="ring:out0"),

            i3.Place('in_taper', position=(-5, 0), angle=0, relative_to="linear_transition_in:out0"),
            i3.FlipH("in_taper"),
            i3.Place('out_taper', position=(5, 0), angle=0, relative_to="linear_transition_out:out0"),

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
        width_in = i3.PositiveNumberProperty(default=1.0, doc="width of input waveguide")
        width_out = i3.PositiveNumberProperty(default=1.0, doc="width of output waveguide")


        def _default_ring(self):
            lo = self.cell.ring.get_default_view(i3.LayoutView)
            lo.set(radius=self.ring_radius)
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

class All_pass_ring_Exspot_50GHz(i3.Circuit):
    taper = i3.ChildCellProperty(doc="inverse_taper coupler")
    ring = i3.ChildCellProperty(doc="ring resonator")
    # trace_template_in = i3.TraceTemplateProperty(doc="waveguide template used in the circuit")
    # trace_template_out = i3.TraceTemplateProperty(doc="waveguide template used in the circuit")

    ring_position_x = i3.NumberProperty(default=0.0, doc="the x position of ring")
    ring_position_y = i3.NumberProperty(default=0.0, doc="the y position of ring")

    output_offset = i3.NumberProperty(default=50, doc="offset from ring output")

    out_taper_position = i3.NumberProperty(default=0, doc="out taper position")

    linear_transition = i3.ChildCellProperty(doc="linear transition waveguide")

    def _default_taper(self):
        return pdk.AN800BB_ExSpot_SMF_C()

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
            i3.Place('in_taper', position=(-700 - self.ring_position_x , 0), angle=0, relative_to="ring:in0"),
            i3.FlipH("in_taper"),
            i3.Place('out_taper', position=(300+25-7.5- self.ring_position_x, -self.output_offset - self.out_taper_position), angle=0, relative_to="ring:out0"),

            i3.Place("linear_transition_in",position=(115, 0), angle=180, relative_to="in_taper:in0"),
            i3.Place("linear_transition_out", position=(-115, 0), angle=0, relative_to="out_taper:in0"),

            i3.ConnectBend("linear_transition_in:out0", "in_taper:in0"),
            i3.ConnectBend("linear_transition_out:out0", "out_taper:in0"),
            #
            i3.ConnectBend("ring:in0", "linear_transition_in:in0"),

            i3.ConnectBend(
                "ring:out0", "linear_transition_out:in0",
                # control_points=[i3.V(i3.START+200)
                #                 ],
                # bend_radius=50,
            ),

        ]

    class Layout(i3.Circuit.Layout):
        # horizontal_spacing = i3.PositiveNumberProperty(default=9000, doc="horizontal spacing between input and output inverse_taper couplers")
        ring_radius = i3.PositiveNumberProperty(default=50.0, doc="radius of the ring")
        ring_width = i3.PositiveNumberProperty(default=1.0, doc="width of the ring")
        ring_gap = i3.PositiveNumberProperty(default=0.7, doc="the gap ")
        # ring_position_x=i3.NumberProperty (default=0.0, doc="the x position of ring")
        # ring_position_y=i3.NumberProperty (default=0.0, doc="the y position of ring")
        # ebl_field_size = i3.PositiveNumberProperty(default=100.0, doc="the ebl writing field size")
        #
        # v_separation = i3.NumberProperty(default=0.7, doc="the gap ")
        width_in = i3.PositiveNumberProperty(default=1.0, doc="width of input waveguide")
        width_out = i3.PositiveNumberProperty(default=1.0, doc="width of output waveguide")
        linear_taper_length = i3.PositiveNumberProperty(default=100, doc="length of linear taper")

        def _default_ring(self):
            lo = self.cell.ring.get_default_view(i3.LayoutView)
            lo.set(radius=self.ring_radius)
            lo.set(ring_width=self.ring_width)
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
                in_width=self.ring_width,
                out_width=self.width_out,
                length=self.linear_taper_length
            )
            return lv

class All_pass_ring_Exspot_100GHz(i3.Circuit):
    taper = i3.ChildCellProperty(doc="inverse_taper coupler")
    ring = i3.ChildCellProperty(doc="ring resonator")
    # trace_template_in = i3.TraceTemplateProperty(doc="waveguide template used in the circuit")
    # trace_template_out = i3.TraceTemplateProperty(doc="waveguide template used in the circuit")

    ring_position_x = i3.NumberProperty(default=0.0, doc="the x position of ring")
    ring_position_y = i3.NumberProperty(default=0.0, doc="the y position of ring")

    output_offset = i3.NumberProperty(default=50, doc="offset from ring output")

    out_taper_position = i3.NumberProperty(default=0, doc="out taper position")

    linear_transition = i3.ChildCellProperty(doc="linear transition waveguide")

    def _default_taper(self):
        return pdk.AN800BB_ExSpot_SMF_C()

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
            i3.Place('in_taper', position=(-700 - self.ring_position_x , 0), angle=0, relative_to="ring:in0"),
            i3.FlipH("in_taper"),
            i3.Place('out_taper', position=(300+25-7.5- self.ring_position_x, -self.output_offset - self.out_taper_position), angle=0, relative_to="ring:out0"),

            i3.Place("linear_transition_in",position=(115, 0), angle=180, relative_to="in_taper:in0"),
            i3.Place("linear_transition_out", position=(-115, 0), angle=0, relative_to="out_taper:in0"),

            i3.ConnectBend("linear_transition_in:out0", "in_taper:in0"),
            i3.ConnectBend("linear_transition_out:out0", "out_taper:in0"),

            i3.ConnectBend("ring:in0", "linear_transition_in:in0"),

            i3.ConnectManhattan(
                "ring:out0", "linear_transition_out:in0",
                control_points=[i3.V(i3.START+200)
                                ],
                bend_radius=50,
            ),

        ]

    class Layout(i3.Circuit.Layout):
        # horizontal_spacing = i3.PositiveNumberProperty(default=9000, doc="horizontal spacing between input and output inverse_taper couplers")
        ring_radius = i3.PositiveNumberProperty(default=50.0, doc="radius of the ring")
        ring_width = i3.PositiveNumberProperty(default=1.0, doc="width of the ring")
        ring_gap = i3.PositiveNumberProperty(default=0.7, doc="the gap ")
        # ring_position_x=i3.NumberProperty (default=0.0, doc="the x position of ring")
        # ring_position_y=i3.NumberProperty (default=0.0, doc="the y position of ring")
        # ebl_field_size = i3.PositiveNumberProperty(default=100.0, doc="the ebl writing field size")
        #
        # v_separation = i3.NumberProperty(default=0.7, doc="the gap ")
        width_in = i3.PositiveNumberProperty(default=1.0, doc="width of input waveguide")
        width_out = i3.PositiveNumberProperty(default=1.0, doc="width of output waveguide")
        linear_taper_length = i3.PositiveNumberProperty(default=100, doc="length of linear taper")

        def _default_ring(self):
            lo = self.cell.ring.get_default_view(i3.LayoutView)
            lo.set(radius=self.ring_radius)
            lo.set(ring_width=self.ring_width)
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
                in_width=self.ring_width,
                out_width=self.width_out,
                length=self.linear_taper_length
            )
            return lv


class All_pass_ring_Exspot_200GHz(i3.Circuit):
    taper = i3.ChildCellProperty(doc="inverse_taper coupler")
    ring = i3.ChildCellProperty(doc="ring resonator")
    # trace_template_in = i3.TraceTemplateProperty(doc="waveguide template used in the circuit")
    # trace_template_out = i3.TraceTemplateProperty(doc="waveguide template used in the circuit")

    ring_position_x = i3.NumberProperty(default=0.0, doc="the x position of ring")
    ring_position_y = i3.NumberProperty(default=0.0, doc="the y position of ring")

    output_offset = i3.NumberProperty(default=50, doc="offset from ring output")

    out_taper_position = i3.NumberProperty(default=0, doc="out taper position")

    linear_transition = i3.ChildCellProperty(doc="linear transition waveguide")

    def _default_taper(self):
        return pdk.AN800BB_ExSpot_SMF_C()

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
            i3.Place('in_taper', position=(-700-25 - self.ring_position_x , 0), angle=0, relative_to="ring:in0"),
            i3.FlipH("in_taper"),
            i3.Place('out_taper', position=(300-7.5- self.ring_position_x, -self.output_offset - self.out_taper_position), angle=0, relative_to="ring:out0"),

            i3.Place("linear_transition_in",position=(115, 0), angle=180, relative_to="in_taper:in0"),
            i3.Place("linear_transition_out", position=(-115, 0), angle=0, relative_to="out_taper:in0"),

            i3.ConnectBend("linear_transition_in:out0", "in_taper:in0"),
            i3.ConnectBend("linear_transition_out:out0", "out_taper:in0"),


            i3.ConnectBend("ring:in0", "linear_transition_in:in0"),
            # #
            i3.ConnectManhattan(
                "ring:out0", "linear_transition_out:in0",
                control_points=[i3.V(i3.START+100),
                                ],
                bend_radius=50,
            ),

        ]

    class Layout(i3.Circuit.Layout):
        # horizontal_spacing = i3.PositiveNumberProperty(default=9000, doc="horizontal spacing between input and output inverse_taper couplers")
        ring_radius = i3.PositiveNumberProperty(default=50.0, doc="radius of the ring")
        ring_width = i3.PositiveNumberProperty(default=1.0, doc="width of the ring")
        ring_gap = i3.PositiveNumberProperty(default=0.7, doc="the gap ")
        # ring_position_x=i3.NumberProperty (default=0.0, doc="the x position of ring")
        # ring_position_y=i3.NumberProperty (default=0.0, doc="the y position of ring")
        # ebl_field_size = i3.PositiveNumberProperty(default=100.0, doc="the ebl writing field size")
        #
        # v_separation = i3.NumberProperty(default=0.7, doc="the gap ")
        width_in = i3.PositiveNumberProperty(default=1.0, doc="width of input waveguide")
        width_out = i3.PositiveNumberProperty(default=1.0, doc="width of output waveguide")
        linear_taper_length = i3.PositiveNumberProperty(default=100, doc="length of linear taper")

        def _default_ring(self):
            lo = self.cell.ring.get_default_view(i3.LayoutView)
            lo.set(radius=self.ring_radius)
            lo.set(ring_width=self.ring_width)
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
                in_width=self.ring_width,
                out_width=self.width_out,
                length=self.linear_taper_length
            )
            return lv

class All_pass_ring_Exspot_Aux(i3.Circuit):
    taper = i3.ChildCellProperty(doc="inverse_taper coupler")
    ring = i3.ChildCellProperty(doc="ring resonator")
    # trace_template_in = i3.TraceTemplateProperty(doc="waveguide template used in the circuit")
    # trace_template_out = i3.TraceTemplateProperty(doc="waveguide template used in the circuit")

    ring_position_x = i3.NumberProperty(default=0.0, doc="the x position of ring")
    ring_position_y = i3.NumberProperty(default=0.0, doc="the y position of ring")

    output_offset = i3.NumberProperty(default=50, doc="offset from ring output")

    out_taper_position = i3.NumberProperty(default=0, doc="out taper position")

    linear_transition = i3.ChildCellProperty(doc="linear transition waveguide")

    def _default_taper(self):
        return pdk.AN800BB_ExSpot_SMF_C()

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
            i3.Place('in_taper', position=(-700-25 - self.ring_position_x , 0), angle=0, relative_to="ring:in0"),
            i3.FlipH("in_taper"),
            i3.Place('out_taper', position=(300-7.5- self.ring_position_x, -self.output_offset - self.out_taper_position), angle=0, relative_to="ring:out0"),

            i3.Place("linear_transition_in",position=(115, 0), angle=180, relative_to="in_taper:in0"),
            i3.Place("linear_transition_out", position=(-115, 0), angle=0, relative_to="out_taper:in0"),

            i3.ConnectBend("linear_transition_in:out0", "in_taper:in0"),
            i3.ConnectBend("linear_transition_out:out0", "out_taper:in0"),


            i3.ConnectBend("ring:in0", "linear_transition_in:in0"),
            # #
            i3.ConnectManhattan(
                "ring:out0", "linear_transition_out:in0",
                control_points=[i3.V(i3.START+75),
                                ],
                bend_radius=50,
            ),

        ]

    class Layout(i3.Circuit.Layout):
        # horizontal_spacing = i3.PositiveNumberProperty(default=9000, doc="horizontal spacing between input and output inverse_taper couplers")
        ring_radius = i3.PositiveNumberProperty(default=50.0, doc="radius of the ring")
        ring_gap = i3.PositiveNumberProperty(default=0.7, doc="the gap ")
        # ring_position_x=i3.NumberProperty (default=0.0, doc="the x position of ring")
        # ring_position_y=i3.NumberProperty (default=0.0, doc="the y position of ring")
        # ebl_field_size = i3.PositiveNumberProperty(default=100.0, doc="the ebl writing field size")
        ring_width = i3.PositiveNumberProperty(default=1.0, doc="width of the ring")
        #
        # v_separation = i3.NumberProperty(default=0.7, doc="the gap ")
        width_in = i3.PositiveNumberProperty(default=1.8, doc="width of input waveguide")
        width_out = i3.PositiveNumberProperty(default=1.0, doc="width of output waveguide")
        linear_taper_length = i3.PositiveNumberProperty(default=100, doc="length of linear taper")

        def _default_ring(self):
            lo = self.cell.ring.get_default_view(i3.LayoutView)
            lo.set(radius=self.ring_radius)
            lo.set(ring_width=self.ring_width)
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
                in_width=self.ring_width,
                out_width=self.width_out,
                length=self.linear_taper_length
            )
            return lv

class All_pass_ring_Exspot_Test(i3.Circuit):
    taper = i3.ChildCellProperty(doc="inverse_taper coupler")
    ring = i3.ChildCellProperty(doc="ring resonator")
    # trace_template_in = i3.TraceTemplateProperty(doc="waveguide template used in the circuit")
    # trace_template_out = i3.TraceTemplateProperty(doc="waveguide template used in the circuit")

    ring_position_x = i3.NumberProperty(default=0.0, doc="the x position of ring")
    ring_position_y = i3.NumberProperty(default=0.0, doc="the y position of ring")

    output_offset = i3.NumberProperty(default=50, doc="offset from ring output")

    out_taper_position = i3.NumberProperty(default=0, doc="out taper position")

    linear_transition = i3.ChildCellProperty(doc="linear transition waveguide")

    def _default_taper(self):
        return pdk.AN800BB_EdgeCoupler_Lensed_C()

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
            i3.Place('in_taper', position=(+100-50+127/2,-420), angle=90, relative_to="ring:in0"),
            i3.FlipH("in_taper"),
            i3.Place('out_taper', position=(-100+50-127/2, -420), angle=-90, relative_to="ring:out0"),

            i3.Place("linear_transition_in",position=(0, 115), angle=90, relative_to="in_taper:in0"),
            i3.FlipH("linear_transition_in"),
            i3.Place("linear_transition_out", position=(0, 115), angle=90, relative_to="out_taper:in0"),
            i3.FlipH("linear_transition_out"),
            i3.ConnectBend("linear_transition_in:out0", "in_taper:in0"),
            i3.ConnectBend("linear_transition_out:out0", "out_taper:in0"),
            # #
            i3.ConnectManhattan(
                "ring:in0", "linear_transition_out:in0",
                # control_points=[i3.V(i3.START+200)
                #                 ],
                # bend_radius=50,
            ),
            i3.ConnectManhattan(
                "ring:out0", "linear_transition_in:in0",
                # control_points=[i3.V(i3.START+200)
                #                 ],
                # bend_radius=50,
            ),

        ]

    class Layout(i3.Circuit.Layout):
        # horizontal_spacing = i3.PositiveNumberProperty(default=9000, doc="horizontal spacing between input and output inverse_taper couplers")
        ring_radius = i3.PositiveNumberProperty(default=50.0, doc="radius of the ring")
        ring_width = i3.PositiveNumberProperty(default=1.0, doc="width of the ring")
        ring_gap = i3.PositiveNumberProperty(default=0.7, doc="the gap ")
        # ring_position_x=i3.NumberProperty (default=0.0, doc="the x position of ring")
        # ring_position_y=i3.NumberProperty (default=0.0, doc="the y position of ring")
        # ebl_field_size = i3.PositiveNumberProperty(default=100.0, doc="the ebl writing field size")
        #
        # v_separation = i3.NumberProperty(default=0.7, doc="the gap ")
        width_in = i3.PositiveNumberProperty(default=1.0, doc="width of input waveguide")
        width_out = i3.PositiveNumberProperty(default=1.8, doc="width of output waveguide")
        linear_taper_length = i3.PositiveNumberProperty(default=100, doc="length of linear taper")

        def _default_ring(self):
            lo = self.cell.ring.get_default_view(i3.LayoutView)
            lo.set(radius=self.ring_radius)
            lo.set(ring_width=self.ring_width)
            lo.set(gap0 = self.ring_gap)
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
                in_width=self.ring_width,
                out_width=self.width_out,
                length=self.linear_taper_length
            )
            return lv