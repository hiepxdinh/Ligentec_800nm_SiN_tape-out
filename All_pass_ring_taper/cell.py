import sys

import ligentec_an800.all as ligentec

import ipkiss3.all as i3
import numpy as np
from numpy.ma.core import angle


class All_pass_ring_taper(i3.Circuit):
    taper = i3.ChildCellProperty(doc="inverse_taper coupler")
    ring = i3.ChildCellProperty(doc="ring resonator")
    trace_template = i3.TraceTemplateProperty(doc="waveguide template used in the circuit")

    ring_position_x = i3.NumberProperty(default=0.0, doc="the x position of ring")
    ring_position_y = i3.NumberProperty(default=0.0, doc="the y position of ring")

    output_offset = i3.NumberProperty(default=100, doc="offset from ring output")

    out_taper_position = i3.NumberProperty(default=0, doc="out taper position")

    # def _default_name(self):
    #     return "RING"

    def _default_taper(self):
        return ligentec.AN800BB_EdgeCoupler_Lensed_C()

    def _default_ring(self):
        return ligentec.NotchRacetrack()

    def _default_trace_template(self):
        return ligentec.WireWaveguideTemplate()

    def _default_insts(self):
        return {"ring": self.ring,
                "in_taper": self.taper,
                "out_taper": self.taper,
                }

    def _default_specs(self):

        ring_position = (self.ring_position_x, self.ring_position_y)

        return [
            i3.Place('ring', position=ring_position, angle=0),
            i3.FlipV('ring'),
            i3.Place('in_taper', position=(-5000 - self.ring_position_x , 0), angle=0, relative_to="ring:in0"),
            i3.FlipH("in_taper"),
            i3.Place('out_taper', position=(1000- self.ring_position_x, -self.output_offset - self.out_taper_position), angle=0, relative_to="ring:out0"),

            # i3.ConnectManhattan(
            #     "in_taper:in0", "ring:in0",
            #     control_points=[i3.V(i3.START+0),
            #                     i3.H(i3.END+0)
            #                     ],
            #     bend_radius=50,
            # ),
            i3.ConnectBend("in_taper:in0", "ring:in0"),
            # i3.ConnectBend("out_taper:in0", "ring:out0")
            #
            i3.ConnectManhattan(
                "ring:out0", "out_taper:in0",
                control_points=[i3.V(i3.START+self.output_offset),
                                i3.H(i3.END)
                                ],
                # bend_radius=self.bend_radius,
            ),

        ]

    class Layout(i3.Circuit.Layout):
        # horizontal_spacing = i3.PositiveNumberProperty(default=9000, doc="horizontal spacing between input and output inverse_taper couplers")
        ring_radius = i3.PositiveNumberProperty(default=50.0, doc="radius of the ring")
        # ring_gap = i3.PositiveNumberProperty(default=0.7, doc="the gap ")
        # ring_position_x=i3.NumberProperty (default=0.0, doc="the x position of ring")
        # ring_position_y=i3.NumberProperty (default=0.0, doc="the y position of ring")
        # ebl_field_size = i3.PositiveNumberProperty(default=100.0, doc="the ebl writing field size")
        #
        # v_separation = i3.NumberProperty(default=0.7, doc="the gap ")


        def _default_ring(self):
            lo = self.cell.ring.get_default_view(i3.LayoutView)
            lo.set(radius=self.ring_radius)
            return lo

        def _default_trace_template(self):
            lo=self.cell.trace_template.get_default_view(i3.LayoutView)
            # lo.set(core_width=self.bus_wg_width)
            return lo