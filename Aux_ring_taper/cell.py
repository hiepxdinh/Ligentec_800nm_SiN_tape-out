import sys

import ligentec_an800.all as ligentec

import ipkiss3.all as i3
import numpy as np

from Aux_ring import Aux_add_drop_ring



class Aux_add_drop_ring_taper(i3.Circuit):
    taper = i3.ChildCellProperty(doc="inverse_taper coupler")
    aux_ring = i3.ChildCellProperty(doc="ring resonator")
    trace_template = i3.TraceTemplateProperty(doc="waveguide template used in the circuit")

    ring_position = i3.Coord2Property(default=(0, 0),
                                      doc="the position of the ring with respect to the gc.")

    def _default_taper(self):
        return ligentec.AN800BB_EdgeCoupler_Lensed_C()

    def _default_aux_ring(self):
        return Aux_add_drop_ring()

    def _default_trace_template(self):
        return ligentec.ligentec.WireWaveguideTemplate()

    def _default_insts(self):
        return {"aux_ring": self.aux_ring,
                "in_taper": self.taper,
                "through_taper": self.taper,
                "add_taper": self.taper,
                "drop_taper": self.taper,
                "aux_in_taper": self.taper,
                "aux_through_taper": self.taper,
                }

    def _default_specs(self):
        return [
            i3.Place('aux_ring', position=self.ring_position, angle=0),
            i3.Place('in_taper', position=(-500, 0), angle=0, relative_to="aux_ring:in"),
            i3.FlipH("in_taper"),
            i3.Place('through_taper', position=(-600, -100), angle=0, relative_to="aux_ring:through"),
            i3.FlipH("through_taper"),
            i3.Place('add_taper', position=(-500, 0), angle=0, relative_to="aux_ring:add"),
            i3.FlipH("add_taper"),
            i3.Place('drop_taper', position=(-600, 100), angle=0, relative_to="aux_ring:drop"),
            i3.FlipH("drop_taper"),
            i3.Place('aux_in_taper', position=(-900, -450), angle=0, relative_to="aux_ring:aux_in"),
            i3.FlipH("aux_in_taper"),
            i3.Place('aux_through_taper', position=(-900, 450), angle=0, relative_to="aux_ring:aux_through"),
            i3.FlipH("aux_through_taper"),
            i3.ConnectBend("aux_ring:in", "in_taper:in0"),
            i3.ConnectBend("aux_ring:through", "through_taper:in0"),
            i3.ConnectBend("aux_ring:add", "add_taper:in0"),
            i3.ConnectBend("aux_ring:drop", "drop_taper:in0"),
            i3.ConnectBend("aux_ring:aux_in", "aux_in_taper:in0"),
            i3.ConnectBend("aux_ring:aux_through", "aux_through_taper:in0"),


        ]

    class Layout(i3.Circuit.Layout):
        horizontal_spacing = i3.PositiveNumberProperty(default=9000, doc="horizontal spacing between input and output inverse_taper couplers")
        ring_radius = i3.PositiveNumberProperty(default=100.0, doc="radius of the ring")
        ring_gap = i3.PositiveNumberProperty(default=0.7, doc="the gap ")
        ring_position_x=i3.NumberProperty (default=0.0, doc="the x position of ring")
        ring_position_y=i3.NumberProperty (default=0.0, doc="the y position of ring")
        ebl_field_size = i3.PositiveNumberProperty(default=100.0, doc="the ebl writing field size")

        v_separation = i3.NumberProperty(default=0.7, doc="the gap ")

        main_radius = i3.PositiveNumberProperty(default=50.0,doc="Radius of main rings [um]")
        aux_radius = i3.PositiveNumberProperty(default=50.0,doc="Radius of aux rings [um]")


        def _default_aux_ring(self):
            lo = self.cell.aux_ring.get_default_view(i3.LayoutView)
            lo.set(main_radius=self.main_radius)
            lo.set(aux_radius=self.aux_radius)
            return lo

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