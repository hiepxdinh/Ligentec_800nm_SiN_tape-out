import sys

import ligentec_an800.all as pdk


import ipkiss3.all as i3
from ipkiss3.pcell.wiring.window_trace import ElectricalWindowWire
from ipkiss3.pcell.layout.port_list import PortList

class ElectricalWindowWire(ElectricalWindowWire):
    def _default_template(self):
        # workaround for OA export: the ElectricalWindoWire in IPKISS does not have a default template
        return MetalWireTemplate_Ring_Coupler()


class MetalWireTemplate_Ring_Coupler(i3.ElectricalWindowWireTemplate):
    """Metal wire template."""

    _doc_properties = []
    _templated_class = ElectricalWindowWire

    class Layout(i3.ElectricalWindowWireTemplate.Layout):
        _doc_properties = ["core_width", "p1_module"]
        core_width = i3.PositiveNumberProperty(doc="Width of the metal [um]")
        p1_module = i3.BoolProperty(
            doc="If True, it will use the P1 module layers (default set by the technology variant imported)"
        )

        def _default_p1_module(self):
            return i3.TECH.OPTIONS["P1"]

        def _default_layer(self):
            if self.p1_module:
                return i3.TECH.PPLAYER.P1P
            else:
                return i3.TECH.PPLAYER.M1P

        def _default_core_width(self):
            return i3.TECH.METAL.LINE_WIDTH

        def _default_width(self):
            return self.core_width

        def _default_windows(self):
            width = self.width

            windows = [i3.PathTraceWindow(layer=self.layer, start_offset=-width / 2.0, end_offset=width / 2.0)]
            return windows

class MetalWire_Ring_Coupler(i3.ElectricalWire):
    """
    Metal wire.

    **Note**:
    The Metal routing should be done using a 45 degree manhattan.
    To do that, you can use the reshaper ShapeManhattanStub implemented in the PDK.
    It takes a shape that should be Manhattan (returns an error if not Manhattan) and 'bend_radius'
    to give a new shape based on the one given with corner cut at 45 degree according to 'bend_radius'.
    """

    _name_prefix = "Metal_Wire"

    def _default_trace_template(self):
        return MetalWireTemplate_Ring_Coupler()

    class Layout(i3.ElectricalWire.Layout):
        _doc_properties = ["core_width", "shape", "p1_module"]
        core_width = i3.PositiveNumberProperty(doc="Width of the metal [um]")
        p1_module = i3.BoolProperty(
            doc="If True, it will use the P1 module layers (default set by the technology variant imported)"
        )

        # def validate_properties(self):
        #     validate_on_grid("core_width", self.core_width, self.__class__.__name__)
        #     return True

        def _default_core_width(self):
            return i3.TECH.METAL.LINE_WIDTH

        def _default_trace_template(self):
            lv = self.cell.trace_template.get_default_view(self)
            lv.set(core_width=self.core_width, p1_module=self.p1_module)
            return lv

        def _default_p1_module(self):
            return i3.TECH.OPTIONS["P1"]

        def _default_shape(self):
            return i3.Shape([i3.Coord2(0.0, 0.0), i3.Coord2(50.0, 0.0)])

        def _generate_ports(self, ports):
            from numpy import arctan2
            from ipkiss.constants import RAD2DEG

            default_ports = super(MetalWire_Ring_Coupler.Layout, self)._generate_ports(ports)
            offset = self.trace_template.core_width / 2.0
            ports = PortList()

            points = self.shape.points
            in_vector = points[0] - points[1]
            in_angle = RAD2DEG * arctan2(in_vector[1], in_vector[0])
            in_angle = self.shape.start_face_angle + 180 if self.shape.start_face_angle else in_angle

            out_vector = points[-1] - points[-2]
            out_angle = RAD2DEG * arctan2(out_vector[1], out_vector[0])
            out_angle = self.shape.end_face_angle if self.shape.end_face_angle else out_angle
            angles = [in_angle, out_angle]
            if self.p1_module:
                layer = i3.TECH.PPLAYER.P1P
            else:
                layer = i3.TECH.PPLAYER.M1P

            for idx, p in enumerate(default_ports):
                ports += i3.ElectricalPort(
                    name=p.name + "0",
                    layer=layer,
                    position=p.position.move_polar_copy(offset, angles[idx]),
                    angle=angles[idx],
                    direction=p.direction,
                    trace_template=p.trace_template,
                )

            return ports

    class Netlist(i3.NetlistFromLayout):
        pass
