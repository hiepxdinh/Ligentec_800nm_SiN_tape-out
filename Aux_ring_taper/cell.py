import sys

import ligentec_an800.all as pdk

import ipkiss3.all as i3
import numpy as np

from ipkiss3.pcell.cell.pcell import NameProperty

from Aux_ring import Aux_add_drop_ring


class Aux_add_drop_ring_taper(i3.Circuit):
    taper = i3.ChildCellProperty(doc="inverse_taper coupler")
    aux_ring = i3.ChildCellProperty(doc="ring resonator")
    # trace_template_in = i3.TraceTemplateProperty(doc="waveguide template used in the circuit")
    # trace_template_out = i3.TraceTemplateProperty(doc="waveguide template used in the circuit")

    ring_position = i3.Coord2Property(default=(0, 0),
                                      doc="the position of the ring with respect to the gc.")

    linear_transition = i3.ChildCellProperty(doc="linear transition waveguide")

    name = NameProperty()

    def _default_name(self):
        return "RING"

    def _default_taper(self):
        return pdk.AN800BB_ExSpot_SMF_C()

    def _default_aux_ring(self):
        return Aux_add_drop_ring()

    # def _default_trace_template_in(self):
    #     return ligentec.WireWaveguideTemplate()
    #
    # def _default_trace_template_out(self):
    #     return ligentec.WireWaveguideTemplate()

    def _default_linear_transition(self):
        # return ligentec.LinearTaperFromPort(start_trace_template = self.trace_template_in, end_trace_template = self.trace_template_out)
        return pdk.Taper()


    def _default_insts(self):
        return {"aux_ring": self.aux_ring,
                "in_taper": self.taper,
                "through_taper": self.taper,
                "add_taper": self.taper,
                "drop_taper": self.taper,
                "aux_in_taper": self.taper,
                "aux_through_taper": self.taper,
                "linear_transition_in": self.linear_transition,
                "linear_transition_through": self.linear_transition,
                "linear_transition_add": self.linear_transition,
                "linear_transition_drop": self.linear_transition,
                "linear_transition_aux_in": self.linear_transition,
                "linear_transition_aux_through": self.linear_transition,
                }

    def _default_specs(self):
        return [
            i3.Place('aux_ring', position=self.ring_position, angle=0),
            i3.Place('through_taper', position=(-500+1500-250-75-75, 0+239-127), angle=0, relative_to="aux_ring:in"),
            i3.Place('in_taper', position=(-600+1500-250-75-75, -100+212-127), angle=0, relative_to="aux_ring:through"),
            i3.Place('drop_taper', position=(-500+1500-250-75-75, 0-239+127), angle=0, relative_to="aux_ring:add"),
            i3.Place('add_taper', position=(-600+1500-250-75-75, 100-212+127), angle=0, relative_to="aux_ring:drop"),
            i3.Place('aux_in_taper', position=(-900-55.5+1500+127-250-75-75-1.08, 50-127/2), angle=0, relative_to="aux_ring:aux_in"),
            i3.Place('aux_through_taper', position=(-900-55.5+1500+127-250-75-75-1.08, -50+127/2), angle=0, relative_to="aux_ring:aux_through"),

            i3.Place("linear_transition_in", position=(-75, 0), angle=0, relative_to="in_taper:in0"),
            # i3.FlipH("linear_transition_in"),
            i3.Place("linear_transition_through", position=(-75, 0), angle=0, relative_to="through_taper:in0"),
            # i3.FlipH("linear_transition_through"),
            i3.Place("linear_transition_add", position=(-75, 0), angle=0, relative_to="add_taper:in0"),
            # i3.FlipH("linear_transition_add"),
            i3.Place("linear_transition_drop", position=(-75, 0), angle=0, relative_to="drop_taper:in0"),
            # i3.FlipH("linear_transition_drop"),
            # #
            i3.Place("linear_transition_aux_in", position=(-75, 0), angle=0, relative_to="aux_in_taper:in0"),
            i3.Place("linear_transition_aux_through", position=(-75, 0), angle=0, relative_to="aux_through_taper:in0"),
            #
            i3.ConnectBend("linear_transition_in:out0", "in_taper:in0"),
            i3.ConnectBend("linear_transition_through:out0", "through_taper:in0"),
            i3.ConnectBend("linear_transition_add:out0", "add_taper:in0"),
            i3.ConnectManhattan("linear_transition_drop:out0", "drop_taper:in0"),
            i3.ConnectBend("linear_transition_aux_in:out0", "aux_in_taper:in0"),
            i3.ConnectBend("linear_transition_aux_through:out0", "aux_through_taper:in0"),
            #
            i3.ConnectManhattan("linear_transition_aux_in:in0", "aux_ring:aux_in"),
            i3.ConnectManhattan("linear_transition_aux_through:in0", "aux_ring:aux_through"),

            i3.ConnectManhattan("aux_ring:in", "linear_transition_in:in0"),
            i3.ConnectManhattan("aux_ring:through", "linear_transition_through:in0"),
            i3.ConnectManhattan("aux_ring:add", "linear_transition_add:in0"),
            i3.ConnectManhattan("aux_ring:drop", "linear_transition_drop:in0"),

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

        name_position = i3.Coord2Property(default =(0.0,0.0), doc="name position", locked=True)
        name_fontsize = i3.PositiveNumberProperty(default=10.0, doc="black box font size", locked=True)

        width_in = i3.PositiveNumberProperty(default=1.8, doc="width of input waveguide")
        width_out = i3.PositiveNumberProperty(default=1.0, doc="width of output waveguide")


        def _default_aux_ring(self):
            lo = self.cell.aux_ring.get_default_view(i3.LayoutView)
            lo.set(main_radius=self.main_radius)
            lo.set(aux_radius=self.aux_radius)
            return lo
        #
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

        def _generate_elements(self, elems):
            """
            add labels at in/out put grating couplers regions
            """
            name_position = self.name_position
            fontsize = self.name_fontsize

            elems += i3.PolygonText(
                layer=i3.TECH.PPLAYER.CELLNAME,
                coordinate=name_position,
                text=self.name,
                alignment=(i3.TEXT.ALIGN.CENTER, i3.TEXT.ALIGN.CENTER),
                font=i3.TEXT.FONT.DEFAULT,
                height=fontsize,
            )
            return elems