import sys

import ligentec_an800.all as ligentec

import ipkiss3.all as i3
import numpy as np

from Aux_ring import Aux_ring



class all_pass_ring(i3.Circuit):
    taper = i3.ChildCellProperty(doc="inverse_taper coupler")
    ring = i3.ChildCellProperty(doc="ring resonator")
    trace_template = i3.TraceTemplateProperty(doc="waveguide template used in the circuit")

    ring_position = i3.Coord2Property(default=(-1000, -2000),
                                      doc="the position of the ring with respect to the gc.")

    def _default_taper(self):
        return ligentec.

    def _default_ring(self):
        return Aux_ring()

    def _default_trace_template(self):
        return ligentec.

    def _default_insts(self):
        return {"ring": self.ring,
                "in_taper": self.taper,
                "out_taper": self.taper,
                }

    def _default_specs(self):
        return [
            i3.Place('ring', position=self.ring_position, angle=0),
            i3.Place('taper', position=(self.gc_spacing, 0), angle=-90),
            i3.Place('taper', position=(self.gc_spacing * 2, 0), angle=-90),

            i3.ConnectManhattan(
                "in_taper:out", "ring:in",
                control_points=[i3.H(i3.START - self.gc_wg_distance),
                                i3.V(i3.END - self.ring_wg_distance)
                                ],
                bend_radius=self.bend_radius,
            ),

            i3.ConnectManhattan(
                "out_taper:out", "ring:in",
                control_points=[i3.H(i3.START - self.gc_wg_distance),
                                i3.V(i3.END - self.ring_wg_distance)
                                ],
                bend_radius=self.bend_radius,
            ),

        ]

    class Layout(i3.Circuit.Layout):
        horizontal_spacing = i3.PositiveNumberProperty(default=9000, doc="horizontal spacing between input and output inverse_taper couplers")
        ring_radius = i3.PositiveNumberProperty(default=100.0, doc="radius of the ring")
        ring_gap = i3.PositiveNumberProperty(default=0.7, doc="the gap ")
        ring_position_x=i3.NumberProperty (default=0.0, doc="the x position of ring")
        ring_position_y=i3.NumberProperty (default=0.0, doc="the y position of ring")
        ebl_field_size = i3.PositiveNumberProperty(default=100.0, doc="the ebl writing field size")

        v_separation = i3.NumberProperty(default=0.7, doc="the gap ")


        def _default_ring(self):
            lo = self.cell.ring.get_default_view(i3.LayoutView)

            # lo.set(ring_radius=self.ring_radius)
            # lo.set(coupler_radius=self.ring_radius + self.ring_gap + self.ring_wg_width*0.5 + self.bus_wg_width*0.5)
            # lo.set(ring_wg_width=self.ring_wg_width)
            # lo.set(bus_wg_width=self.bus_wg_width)
            # lo.set(gap=self.ring_gap)
            # lo.set(ring_straight_length=self.ring_straight_length)

        def _default_trace_template(self):
            lo=self.cell.trace_template.get_default_view(i3.LayoutView)
            # lo.set(core_width=self.bus_wg_width)
            return lo

        # def _generate_instances(self, insts):
        #     insts += i3.SRef(reference=self.inverse_taper)
        #     insts += i3.SRef(reference=self.inverse_taper)
        #     insts += i3.SRef(reference=self.ring)
        #
        #     return insts