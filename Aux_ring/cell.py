import sys

from numpy.f2py.rules import aux_rules
from wx.lib.agw.cubecolourdialog import deg2rad

sys.path.append("C:/pdk/Ligentec_SiN_2025/ipkiss")

import ligentec_an800.all as pdk
from ligentec.technology import TECH

from ipkiss3 import all as i3
from ipkiss3.pcell.cell.pcell import NameProperty

# from ..directional_coupler.cell import (
#     DirectionalCouplerRing,
#     EulerDirectionalCouplerRing,
# )
# from ..metal.heater import HeaterTemplate, HeaterWaveguide
# from ..metal.wire import DCTaper
import numpy as np
# from ..waveguides.waveguides import Straight, Arc, EulerBend
# from ..metal.via import ElecViaArray
# from ...utils import validate_on_grid

def index_of_point(point, points_array):
    # returns the index of a point (X, Y) in a numpy array of points
    x, y = point
    mask = np.logical_and(points_array[:, 0] == x, points_array[:, 1] == y)
    idx = np.argmax(mask)

    if idx >= points_array.shape[0]:
        raise ValueError(f"Point {point} not in array {points_array}")

    return idx

def find_side_elements(dc):
    arcbend1_inst = dc.instances["arcbend1"]
    arcbend2_inst = dc.instances["arcbend2"]
    left = i3.Shape(_get_points(arcbend2_inst, upper_treshold=135))
    right = i3.Shape(_get_points(arcbend1_inst, upper_treshold=135))
    return left, right

def validate_on_grid(prop_name, value, class_name):
    is_not_on_grid = round(value * i3.get_grids_per_unit()) % 2
    if is_not_on_grid:
        raise i3.PropertyValidationError(
            f"{prop_name} of {class_name} is not aligned to the grid."
            f" It should be having a precision of {2 * TECH.METRICS.GRID}"
        )

def _get_points(arcbend, upper_treshold=180, angle=0):
    shape = arcbend.reference.center_line_shape
    bend_points = shape.transform_copy(arcbend.transformation + i3.Translation(arcbend.position)).points
    bend_angles = np.array(
        [i3.angle_deg(bend_points[idx + 1], bend_points[idx]) for idx in range(len(bend_points) - 1)]
    )
    return bend_points[np.where((bend_angles[1:-1] >= 45 - angle) & (bend_angles[1:-1] <= upper_treshold - angle))[0]]


def find_top_connector_elements(dc):
    arcbend1_inst = dc.instances["arcbend1"]
    arcbend2_inst = dc.instances["arcbend2"]

    points = []
    right_points = _get_points(arcbend1_inst, angle=60)
    right_points_reversed = right_points[::-1]
    points.extend(right_points_reversed)
    left_points = _get_points(arcbend2_inst, angle=-15)
    left_points_reversed = left_points[::1]
    points.extend(left_points_reversed)
    return i3.Shape(points=points)

class AddDropRacetrack(i3.PCell):
    """
    A racetrack resonator coupled to two straight waveguides using circular bend/ Euler bend.

    Does not have a validated simulation model yet.
    Only TE will be propagated.
    """

    _name_prefix = "AddDropRacetrack"
    wg_top = i3.ChildCellProperty(doc="Waveguide at the top of ring resonator", locked=True)

    def _default_wg_top(self):
        wg = pdk.Straight(name=self.name + "_st")
        return wg

    class Layout(i3.LayoutView):
        _doc_properties = [
            "bus0_width",
            "ring_width",
            "bus1_width",
            "bus1_length",
            "bus0_length",
            "gap0",
            "gap1",
            "radius",
            "coupler_length",
            "euler",
        ]

        bus0_width = i3.PositiveNumberProperty(doc="Width of the straight waveguide at the bottom [um]")
        bus1_width = i3.PositiveNumberProperty(doc="Width of the straight waveguide at the top [um]")
        ring_width = i3.PositiveNumberProperty(doc="Width of the arc waveguides [um]", default=1.0)
        bus0_length = i3.PositiveNumberProperty(doc="Length of the straight waveguide at the bottom[um]", default=100.0)
        bus1_length = i3.PositiveNumberProperty(doc="Length of the straight waveguide at the top [um]")
        gap0 = i3.PositiveNumberProperty(doc="Gap of bottom directional coupler", default=1.0)
        gap1 = i3.PositiveNumberProperty(doc="Gap of top directional coupler")
        coupler_length = i3.NonNegativeNumberProperty(doc="Coupling Length of the directional coupler[um]", default=0.0)
        radius = i3.PositiveNumberProperty(doc="Radius of arc waveguide")
        euler = i3.IntProperty(
            default=0,
            doc="Use Euler Bend?",
            restriction=i3.RestrictValueList((0, 1)),
        )
        total_ring_length = i3.PositiveNumberProperty(doc="Total ring Length", locked=True)

        directional_coupler = i3.ChildCellProperty(
            doc="Directional coupler at the bottom of ring resonator", locked=True
        )

        def validate_properties(self):
            for param in ["bus0_width", "bus1_width", "ring_width"]:
                validate_on_grid(param, getattr(self, param), self.__class__.__name__)
            return True

        def _default_total_ring_length(self):
            if self.euler:
                return (
                    2 * self.directional_coupler.get_default_view(i3.LayoutView).instances["arcbend2"].reference.length
                    + 2 * self.coupler_length
                )
            else:
                return 2 * np.pi * self.radius + 2 * self.coupler_length

        def _default_radius(self):
            return i3.TECH.TECH.MINIMUM_BEND_RADIUS

        def _default_bus0_width(self):
            return self.ring_width

        def _default_bus1_width(self):
            return self.bus0_width

        def _default_bus1_length(self):
            return self.bus0_length

        def _default_gap1(self):
            return self.gap0

        def _default_directional_coupler(self):
            if not self.euler:
                cell = pdk.DirectionalCouplerRing(name=self.name + "_dc")
                lv = cell.get_default_view(self)
                lv.set(
                    bus_width=self.bus0_width,
                    ring_width=self.ring_width,
                    bus_length=self.bus0_length,
                    gap=self.gap0,
                    bend_radius=self.radius,
                    coupler_length=self.coupler_length,
                    bend_angle=180,
                )
            else:
                cell = pdk.EulerDirectionalCouplerRing(name=self.name + "_dc")
                lv = cell.get_default_view(self)
                lv.set(
                    bus_width=self.bus0_width,
                    ring_width=self.ring_width,
                    bus_length=self.bus0_length,
                    gap=self.gap0,
                    bend_radius=self.radius * 0.726304,
                    coupler_length=self.coupler_length,
                    bend_angle=180,
                )
            return lv

        def _default_wg_top(self):
            cell = self.cell.wg_top
            lv = cell.get_default_view(self)
            lv.set(
                width=self.bus1_width,
                length=self.bus1_length,
            )
            return lv

        def _generate_instances(self, insts):
            dc = self.directional_coupler
            wg_top = self.wg_top
            radius = self.radius

            insts += i3.InstanceDict()
            insts += i3.SRef(name="dc", reference=dc, flatten=True)
            insts += i3.SRef(name="wg_top", reference=wg_top, flatten=True)
            return i3.place_and_route(
                insts=insts,
                specs=[
                    i3.Place("dc", (0, 0)),
                    i3.Place(
                        "wg_top",
                        (
                            self.bus0_length / 2.0 - self.bus1_length / 2.0,
                            2 * radius
                            + self.gap0
                            + self.gap1
                            + 0.5 * (self.bus0_width + self.bus1_width)
                            + self.ring_width,
                        ),
                    ),
                    i3.ConnectBend(
                        [
                            ("dc:in1", "dc:out1"),
                        ]
                    ),
                ],
            )

        def _generate_ports(self, ports):
            ports += i3.OpticalPort(name="center", position=(0.0, self.radius))
            ports += i3.expose_ports(
                self.instances,
                {
                    "dc:in0": "in0",
                    "dc:out0": "out0",
                    "wg_top:out0": "out1",
                    "wg_top:in0": "in1",
                },
            )
            return ports

    class Netlist(i3.NetlistFromLayout):
        pass

    class CircuitModel(i3.CircuitModelView):
        def _generate_model(self):
            return i3.HierarchicalModel.from_netlistview(self.netlist_view)


class HeaterAddDropRacetrack(AddDropRacetrack):
    """
    A racetrack resonator with heater coupled to two straight waveguides.
    No model not hierarchical netlist yet.
    """

    _name_prefix = "HeaterAddDropRacetrack"
    trace_template = i3.TraceTemplateProperty()

    def _default_trace_template(self):
        return pdk.HeaterTemplate(name=f"{self.name}_ring_tt")

    class Layout(AddDropRacetrack.Layout):
        _doc_properties = [
            "bus0_width",
            "bus1_width",
            "radius",
            "ring_width",
            "bus0_length",
            "bus1_length",
            "heater_width",
            "wire_length",
            "routing_width",
            "gap0",
            "gap1",
            "coupler_length",
            "p1_module",
            "add_heater_width",
            "euler",
        ]

        p1_module = i3.BoolProperty(
            doc="If True, it will use the P1 module layers (default set by the technology variant imported)"
        )
        heater_width = i3.NonNegativeNumberProperty(default=1.5, doc="Width of the Heater path [um]")
        wire_length = i3.NonNegativeNumberProperty(
            default=5.0,
            doc="Length of wire routing south from heater with heater_width width [um]"
            "\nNo wire nor taper if wire_length = 0.",
        )
        routing_width = i3.PositiveNumberProperty(default=8.0, doc="End width of DCTaper [um]")
        add_heater_width = i3.PositiveNumberProperty(doc="Width of the heater junction [um]")

        def validate_properties(self):
            super(HeaterAddDropRacetrack.Layout, self).validate_properties()
            max_junction_width = 2 * self._default_add_heater_width()
            min_junction_width = np.sin(45) * self.heater_width + 0.2
            if self.add_heater_width > max_junction_width:
                raise ValueError(
                    f"add_heater_width ({self.add_heater_width}) should be smaller than {max_junction_width}."
                )
            elif self.add_heater_width < min_junction_width:
                raise ValueError(
                    f"add_heater_width ({self.add_heater_width}) should be bigger than {min_junction_width}."
                )
            return True

        def _default_p1_module(self):
            return i3.TECH.OPTIONS["P1"]

        def _default_add_heater_width(self):
            return self.routing_width

        def _default_trace_template(self):
            lv = self.cell.trace_template.get_default_view(self)
            lv.set(
                core_width=self.ring_width,
                p1_module=self.p1_module,
                heater_width=self.heater_width,
                _remove_X1=True,
            )
            return lv

        def _generate_elements(self, elems):
            junction_width = self.add_heater_width
            insts = self.instances
            metal_hw = self.heater_width / 2.0
            vert_insts = i3.InstanceDict([insts["vert_l"], insts["vert_r"]])
            if self.trace_template.p1_module:
                layer = i3.TECH.PPLAYER.P1P
            else:
                layer = i3.TECH.PPLAYER.M1P

            vert_elems = i3.get_layer_elements(
                i3.LayoutCell(name=self.name + "_dummy").Layout(instances=vert_insts),
                [layer],
            )
            points = vert_elems.convex_hull().points
            max_y = max(points[:, 1])
            min_y = max_y - junction_width
            idxs = np.where(points[:, 1] > min_y)[0]
            points = points[idxs]

            shape = i3.Shape(points=points)
            points = shape.remove_identicals().points
            orientation = shape.orientation()
            if orientation == 1:
                points = points[::-1]
            min_pts = sorted(points, key=lambda p: p[1])[0:2]
            min_pts = sorted(min_pts, key=lambda p: p[0])
            min_pts_idx = sorted([index_of_point(p, points) for p in min_pts])
            add_points = [
                (min_pts[0][0] + metal_hw, min_y),
                (min_pts[1][0] - metal_hw, min_y),
            ]
            if min_pts_idx[0] != 0:
                points = np.roll(points, -2 * min_pts_idx[1])
            points = np.concatenate([add_points, points])
            elems += i3.Boundary(layer=layer, shape=points)
            return elems

        def _generate_instances(self, insts):
            name = self.name
            metal_width = self.trace_template.heater_width
            if self.p1_module:
                taper = metal_width != 8
                taper_width = 8.0
            else:
                taper = metal_width != self.routing_width
                taper_width = self.routing_width
            wire_length = self.wire_length
            insts = super(HeaterAddDropRacetrack.Layout, self)._generate_instances(insts)
            routing_south_insts = {}
            routing_south_specs = []
            left_shape, right_shape = find_side_elements(insts["dc"].reference)
            left_shape.start_face_angle = 135
            left_shape.end_face_angle = 45
            right_shape.start_face_angle = 45
            right_shape.end_face_angle =135

            num_o_points = 50

            angle_0 = np.linspace(-15, -60, num_o_points)
            angle_1  = np.linspace(240, 120, num_o_points)
            angle_2 = np.linspace(15, 60, num_o_points)

            left_points = []
            mid_points = []
            right_points = []

            for i in range(num_o_points):
                x_0 = self.bus0_length/2 +self.radius * np.cos(deg2rad(angle_0[i]))
                y_0 = self.bus0_width - self.gap0/2 + self.radius + self.ring_width + self.radius * np.sin(deg2rad(angle_0[i]))
                left_points.append((x_0, y_0))

            for i in range(num_o_points):
                x_1 = self.bus0_length/2 +self.radius * np.cos(deg2rad(angle_1[i]))
                y_1 = self.bus0_width - self.gap0/2 + self.radius + self.ring_width + self.radius * np.sin(deg2rad(angle_1[i]))

                left_points.append((x_1, y_1))

                x_2 = self.bus0_length/2 + self.radius * np.cos(deg2rad(angle_2[i]))
                y_2 = self.bus0_width - self.gap0/2 + self.radius + self.ring_width + self.radius * np.sin(deg2rad(angle_2[i]))
                right_points.append((x_2, y_2))

            left_shape = i3.Shape(points=left_points)
            right_shape = i3.Shape(points=right_points)

            right_wg = self.trace_template.cell(name=self.name + "_right_wg")
            right_wg.Layout(shape=right_shape)

            left_wg = self.trace_template.cell(name=self.name + "_left_wg")
            left_wg.Layout(shape=left_shape)
            insts += i3.SRef(name="vert_l", reference=left_wg, flatten=True)
            # insts += i3.SRef(name="vert_m", reference=mid_wg, flatten=True)
            insts += i3.SRef(name="vert_r", reference=right_wg, flatten=True)

            if wire_length > 0.0:
                half_width = metal_width / 2.0
                elec_in = insts["vert_l"].ports["elec_in0"]
                elec_out = insts["vert_r"].ports["elec_in0"]
                relative_in = elec_in.position.move_polar_copy(half_width, elec_in.angle +90) - (half_width, 0.5)
                relative_out = elec_out.position.move_polar_copy(half_width, elec_out.angle - 90) + (half_width - 1.5, 0.5)
                wire = pdk.HeaterWaveguide(name=name + "_wire")
                wire.Layout(
                    core_width=0,
                    heater_width=metal_width,
                    shape=[(0.0, 0.0), (self.wire_length, 0.0)],
                    p1_module=self.p1_module,
                )
                routing_south_insts.update({"wire_in": wire, "wire_out": wire})
                routing_south_specs += [
                    i3.Place("wire_in", relative_in, -15),
                    i3.Place("wire_out", relative_out, 15),
                ]

                if taper:
                    dc_taper = pdk.DCTaper(name=name + "_dc_taper")
                    dc_taper_lay = dc_taper.Layout(
                        in_width=metal_width,
                        out_width=taper_width,
                        p1_module=self.p1_module,
                    )
                    routing_south_insts.update({"taper_in": dc_taper, "taper_out": dc_taper})
                    routing_south_specs += [
                        i3.Join("wire_in:out0", "taper_in:in0"),
                        i3.Join("wire_out:out0", "taper_out:in0"),
                    ]
                if self.p1_module:
                    elec_in0 = relative_in + (0, -self.wire_length) + (0, -dc_taper_lay.length)
                    elec_out0 = relative_out + (0, -self.wire_length) + (0, -dc_taper_lay.length)
                    elec_via = pdk.ElecViaArray(name=self.name + "_elec")
                    elec_via.Layout(n_o_vias=(9, 9), width=0.36, spacing=0.35, margin=0.98)
                    routing_south_insts.update(
                        {
                            "elec_via_ll": elec_via,
                            "elec_via_lr": elec_via,
                        }
                    )

                    routing_south_specs += [
                        i3.Place("elec_via_ll:dc0", elec_in0 + (0, -4)),
                        i3.Place("elec_via_lr:dc0", elec_out0 + (0, -4)),
                    ]

                insts += i3.place_and_route(insts=routing_south_insts, specs=routing_south_specs)
            return insts

        def _generate_ports(self, ports):
            ports = super(HeaterAddDropRacetrack.Layout, self)._generate_ports(ports)
            instances = self.instances
            if "elec_via_ll" in instances:
                inst_ports = ["elec_via_ll:dc0", "elec_via_lr:dc0"]
            elif "taper_in" in instances:
                inst_ports = ["taper_in:out0", "taper_out:out0"]
            else:
                inst_ports = ["vert_l:elec_in0", "vert_r:elec_out0"]
            ports += i3.expose_ports(
                self.instances,
                {inst_pt: pt for inst_pt, pt in zip(inst_ports, ["elec_in0", "elec_out0"])},
            )
            return ports

    class Netlist(i3.NetlistView):
        def _generate_terms(self, terms):
            terms += i3.OpticalTerm(name="in0", n_modes=2)
            terms += i3.OpticalTerm(name="out0", n_modes=2)
            terms += i3.OpticalTerm(name="in1", n_modes=2)
            terms += i3.OpticalTerm(name="out1", n_modes=2)
            terms += i3.ElectricalTerm(name="elec_in0")
            terms += i3.ElectricalTerm(name="elec_out0")
            return terms

class NotchRacetrack(i3.PCell):
    """
    A racetrack resonator with Circular bend/Euler bend coupled to one straight waveguide that can be used in the
    Ligentec waveguide geometry.

    No model yet.
    """

    _name_prefix = "NotchRacetrack"

    class Layout(i3.LayoutView):
        _doc_properties = [
            "bus0_width",
            "bus0_length",
            "gap0",
            "radius",
            "coupler_length",
            "ring_width",
            "euler",
        ]

        bus0_width = i3.PositiveNumberProperty(doc="Width of the straight waveguide at the bottom [um]")
        ring_width = i3.PositiveNumberProperty(doc="Width of the arc waveguides [um]", default=1.0)
        bus0_length = i3.PositiveNumberProperty(doc="Length of the straight waveguide at the bottom[um]", default=100.0)
        gap0 = i3.PositiveNumberProperty(doc="Gap of bottom directional coupler", default=1.0)
        coupler_length = i3.NonNegativeNumberProperty(doc="Coupling Length of the directional coupler[um]", default=0.0)
        radius = i3.PositiveNumberProperty(doc="Radius of arc waveguide")
        euler = i3.IntProperty(
            default=0,
            doc="Use Euler Bend?",
            restriction=i3.RestrictValueList((0, 1)),
        )
        total_ring_length = i3.PositiveNumberProperty(doc="Total ring Length", locked=True)
        directional_coupler = i3.ChildCellProperty(doc="Directional couplers used for the ring resonator", locked=True)

        def validate_properties(self):
            for param in ["bus0_width", "ring_width"]:
                validate_on_grid(param, getattr(self, param), self.__class__.__name__)
            return True

        def _default_total_ring_length(self):
            if self.euler:
                return (
                    2 * self.directional_coupler.get_default_view(i3.LayoutView).instances["arcbend2"].reference.length
                    + 2 * self.coupler_length
                )
            else:
                return 2 * np.pi * self.radius + 2 * self.coupler_length

        def _default_radius(self):
            return i3.TECH.TECH.MINIMUM_BEND_RADIUS

        def _default_bus0_width(self):
            return self.ring_width

        def _default_directional_coupler(self):
            if not self.euler:
                cell = pdk.DirectionalCouplerRing(name=self.name + "_dc")
                lv = cell.get_default_view(self)
                lv.set(
                    bus_width=self.bus0_width,
                    ring_width=self.ring_width,
                    bus_length=self.bus0_length,
                    gap=self.gap0,
                    bend_radius=self.radius,
                    coupler_length=self.coupler_length,
                    bend_angle=180.0,
                )
            else:
                cell = pdk.EulerDirectionalCouplerRing(name=self.name + "_dc")
                lv = cell.get_default_view(self)
                lv.set(
                    bus_width=self.bus0_width,
                    ring_width=self.ring_width,
                    bus_length=self.bus0_length,
                    gap=self.gap0,
                    bend_radius=self.radius * 0.726304,
                    coupler_length=self.coupler_length,
                    bend_angle=180.0,
                )
            return lv

        def _generate_instances(self, insts):
            dc = self.directional_coupler
            insts = i3.InstanceDict()
            insts += i3.SRef(name="dc", reference=dc)
            return i3.place_and_route(
                insts=insts,
                specs=[
                    i3.ConnectBend(
                        [
                            ("dc:in1", "dc:out1"),
                        ]
                    ),
                ],
            )

        def _generate_ports(self, ports):
            ports += i3.OpticalPort(name="center", position=(0, self.radius))
            ports += i3.expose_ports(
                self.instances,
                {
                    "dc:in0": "in0",
                    "dc:out0": "out0",
                },
            )
            return ports

    class Netlist(i3.NetlistFromLayout):
        pass

    class CircuitModel(i3.CircuitModelView):
        def _generate_model(self):
            return i3.HierarchicalModel.from_netlistview(self.netlist_view)

class HeaterNotchRacetrack(NotchRacetrack):
    """
    A racetrack resonator with heater coupled to one straight waveguide.
    No model not hierarchical netlist yet.
    """

    _name_prefix = "HeaterNotchRacetrack"
    trace_template = i3.TraceTemplateProperty()

    def _default_trace_template(self):
        return pdk.HeaterTemplate(name=f"{self.name}_ring_tt")

    class Layout(NotchRacetrack.Layout):
        _doc_properties = [
            "bus0_width",
            "radius",
            "ring_width",
            "bus0_length",
            "heater_width",
            "wire_length",
            "routing_width",
            "gap0",
            "coupler_length",
            "p1_module",
            "euler",
        ]

        p1_module = i3.BoolProperty(
            doc="If True, it will use the P1 module layers (default set by the technology variant imported)"
        )
        heater_width = i3.NonNegativeNumberProperty(default=1.5, doc="Width of the Heater path [um]")
        wire_length = i3.NonNegativeNumberProperty(
            default=5.0,
            doc="Length of wire routing south from heater with heater_width width [um]"
            "\nNo wire nor taper if wire_length = 0.",
        )
        routing_width = i3.PositiveNumberProperty(default=8.0, doc="End width of DCTaper [um]")

        def _default_p1_module(self):
            return i3.TECH.OPTIONS["P1"]

        def _default_trace_template(self):
            lv = self.cell.trace_template.get_default_view(self)
            lv.set(
                core_width=self.ring_width,
                p1_module=self.p1_module,
                heater_width=self.heater_width,
                _remove_X1=True,
            )
            return lv

        def _generate_instances(self, insts):
            name = self.name
            metal_width = self.trace_template.heater_width
            if self.p1_module:
                taper = metal_width != 8
                taper_width = 8.0
            else:
                taper = metal_width != self.routing_width
                taper_width = self.routing_width
            wire_length = self.wire_length
            insts = super(HeaterNotchRacetrack.Layout, self)._generate_instances(insts)
            routing_south_insts = {}
            routing_south_specs = []
            top_shape = find_top_connector_elements(insts["dc"].reference)
            top_connect_wg = self.trace_template.cell(name=self.name + "_top_connect_wg")
            top_connect_wg.Layout(shape=top_shape)

            insts += i3.SRef(name="top_ring", reference=top_connect_wg, flatten=True)

            if wire_length > 0.0:
                half_width = metal_width / 2.0
                elec_in = insts["top_ring"].ports["elec_in0"]
                elec_out = insts["top_ring"].ports["elec_out0"]
                relative_in = elec_in.position.move_polar_copy(half_width, elec_in.angle + 90) - (half_width - 0.75, 0.75)
                relative_out = elec_out.position.move_polar_copy(half_width, elec_out.angle - 90) + (half_width - 0.75, - 0.75)
                wire = pdk.HeaterWaveguide(name=name + "_wire")
                wire.Layout(
                    core_width=0,
                    heater_width=metal_width,
                    shape=[(0.0, 0.0), (self.wire_length, 0.0)],
                    p1_module=self.p1_module,
                )
                routing_south_insts.update({"wire_in": wire, "wire_out": wire})
                routing_south_specs += [
                    i3.Place("wire_in", relative_in, 30),
                    i3.Place("wire_out", relative_out, 150),
                ]

                if taper:
                    dc_taper = pdk.DCTaper(name=name + "_dc_taper")
                    dc_taper_lay = dc_taper.Layout(
                        in_width=metal_width,
                        out_width=taper_width,
                        p1_module=self.p1_module,
                    )
                    routing_south_insts.update({"taper_in": dc_taper, "taper_out": dc_taper})
                    routing_south_specs += [
                        i3.Join("wire_in:out0", "taper_in:in0"),
                        i3.Join("wire_out:out0", "taper_out:in0"),
                    ]
                if self.p1_module:
                    elec_in0 = relative_in + (0, -self.wire_length) + (0, -dc_taper_lay.length)
                    elec_out0 = relative_out + (0, -self.wire_length) + (0, -dc_taper_lay.length)
                    elec_via = pdk.ElecViaArray(name=self.name + "_elec")
                    elec_via.Layout(n_o_vias=(9, 9), width=0.36, spacing=0.35, margin=0.98)
                    routing_south_insts.update(
                        {
                            "elec_via_ll": elec_via,
                            "elec_via_lr": elec_via,
                        }
                    )

                    routing_south_specs += [
                        i3.Place("elec_via_ll:dc0", elec_in0 + (0, -4)),
                        i3.Place("elec_via_lr:dc0", elec_out0 + (0, -4)),
                    ]

                insts += i3.place_and_route(insts=routing_south_insts, specs=routing_south_specs)

            return insts

        def _generate_ports(self, ports):
            ports = super(HeaterNotchRacetrack.Layout, self)._generate_ports(ports)
            instances = self.instances
            if "elec_via_ll" in instances:
                inst_ports = ["elec_via_ll:dc0", "elec_via_lr:dc0"]
            elif "taper_in" in instances:
                inst_ports = ["taper_in:out0", "taper_out:out0"]
            else:
                inst_ports = ["top_ring:elec_in0", "top_ring:elec_out0"]
            ports += i3.expose_ports(
                self.instances,
                {inst_pt: pt for inst_pt, pt in zip(inst_ports, ["elec_in0", "elec_out0"])},
            )
            return ports

    class Netlist(i3.NetlistView):
        def _generate_terms(self, terms):
            terms += i3.OpticalTerm(name="in0", n_modes=2)
            terms += i3.OpticalTerm(name="out0", n_modes=2)
            terms += i3.ElectricalTerm(name="elec_in0")
            terms += i3.ElectricalTerm(name="elec_out0")
            return terms

class Aux_add_drop_ring(i3.PCell):
    """
    Auxiliary coupled resonators
    """

    # _name_prefix = "ring"
    #
    # name = NameProperty(locked=True)


    # straight = i3.ChildCellProperty(locked=True)
    main_ring = i3.ChildCellProperty(locked=True)
    aux_ring = i3.ChildCellProperty(locked=True)

    # def _default_straight(self):
    #     return pdk.Straight(name=self.name + "straight")

    def _default_main_ring(self):
        return HeaterAddDropRacetrack()

    def _default_aux_ring(self):
        return HeaterNotchRacetrack()

    class Layout(i3.LayoutView):

        _doc_properties = ["radius", "width", "length", "gap", "euler"]

        main_radius = i3.PositiveNumberProperty(doc="Radius of main rings [um]")
        aux_radius = i3.PositiveNumberProperty(doc="Radius of aux rings [um]")
        width = i3.PositiveNumberProperty(doc="Width of all the access waveguides [um]", default=1.0)
        length = i3.PositiveNumberProperty(doc="Length of the straight waveguides [um]", default=100.0)
        coupler_gap = i3.PositiveNumberProperty(doc="Gap between ring and coupler [um]", default=1.0)
        ring_gap = i3.PositiveNumberProperty(doc="Gap between two rings [um]", default=1.5)
        ring_width = i3.PositiveNumberProperty(doc="Width of the arc waveguides [um]", default=1.5)
        euler = i3.IntProperty(
            default=0,
            doc="Use Euler Bend?",
            restriction=i3.RestrictValueList((0, 1)),
        )

        # name_position = i3.Coord2Property(default =(0.0,0.0), doc="name position", locked=True)
        # name_fontsize = i3.PositiveNumberProperty(default=10.0, doc="black box font size", locked=True)

        def validate_properties(self):
            validate_on_grid("width", self.width, self.__class__.__name__)
            return True

        def _default_main_radius(self):
            return i3.TECH.TECH.MINIMUM_BEND_RADIUS

        print("Minium bend radius: {}".format(i3.TECH.TECH.MINIMUM_BEND_RADIUS))

        def _default_aux_radius(self):
            return i3.TECH.TECH.MINIMUM_BEND_RADIUS

        # def _default_straight(self):
        #     lv = self.cell.straight.get_default_view(self)
        #     lv.set(width=self.width, length=self.length)
        #     return lv

        def _default_main_ring(self):
            lv = self.cell.main_ring.get_default_view(self)
            lv.set(radius=self.main_radius)
            lv.set(gap0=self.coupler_gap)
            lv.set(ring_width=self.ring_width)
            return lv

        def _default_aux_ring(self):
            lv = self.cell.aux_ring.get_default_view(self)
            lv.set(radius=self.aux_radius)
            lv.set(ring_width=self.ring_width)
            return lv

        def _generate_instances(self, insts):
            ring_gap = self.ring_gap
            coupler_gap = self.coupler_gap
            ring_width = self.ring_width
            main_radius = self.main_radius
            aux_radius = self.aux_radius
            ring_width = self.ring_width
            length = self.length

            main_ring_height = coupler_gap + ring_width + 2*main_radius + ring_width
            aux_ring_height = coupler_gap +  ring_width + 2*aux_radius + ring_width

            insts_dict = { "main_ring":self.main_ring, "aux_ring":self.aux_ring}
            instances = insts_dict

            specs = [
                i3.Place("main_ring:center", (0.0, 0.0)),
                i3.Place("aux_ring:center", (51.0 + ring_width + (main_radius + aux_radius + ring_width + ring_gap) * np.cos(np.deg2rad(0)),-49 + ring_width + (main_radius + aux_radius + ring_width + ring_gap) * np.sin(np.deg2rad(0))),
                         relative_to="main_ring:center", angle=90),
                ]

            # i3.Place("aux_ring:center",
            #          (50.0 + (main_radius + aux_radius + 2 * ring_width + ring_gap) * np.cos(np.deg2rad(0)),
            #           -50.0 + (main_radius + aux_radius + 2 * ring_width + ring_gap) * np.sin(np.deg2rad(0))),
            #          relative_to="main_ring:center", angle=90),
            # ]


            return i3.place_and_route(instances, specs)

        # def _generate_elements(self, elems):
        #     """
        #     add labels at in/out put grating couplers regions
        #     """
        #     name_position = self.name_position
        #     fontsize = self.name_fontsize
        #
        #     elems += i3.PolygonText(
        #         layer=i3.TECH.PPLAYER.CELLNAME,
        #         coordinate=name_position,
        #         text=self.name,
        #         alignment=(i3.TEXT.ALIGN.CENTER, i3.TEXT.ALIGN.CENTER),
        #         font=i3.TEXT.FONT.DEFAULT,
        #         height=fontsize,
        #     )
        #     return elems


        def _generate_ports(self, ports):
                return i3.expose_ports(
                    self.instances,
                    {
                        "main_ring:in0": "in",
                        "main_ring:in1": "add",
                        "main_ring:out0": "through",
                        "main_ring:out1": "drop",
                        "aux_ring:in0": "aux_in",
                        "aux_ring:out0": "aux_through",

                    },
                )

    class Netlist(i3.NetlistFromLayout):
        pass

class Aux_all_pass_ring(i3.PCell):
    """
    Auxiliary coupled resonators
    """

    _name_prefix = "Aux_ring"
    # straight = i3.ChildCellProperty(locked=True)
    main_ring = i3.ChildCellProperty(locked=True)
    aux_ring = i3.ChildCellProperty(locked=True)

    # def _default_straight(self):
    #     return pdk.Straight(name=self.name + "straight")

    def _default_main_ring(self):
        return HeaterNotchRacetrack()

    def _default_aux_ring(self):
        return NotchRacetrack()

    class Layout(i3.LayoutView):

        _doc_properties = ["radius", "width", "length", "gap", "euler"]

        main_radius = i3.PositiveNumberProperty(doc="Radius of main rings [um]")
        aux_radius = i3.PositiveNumberProperty(doc="Radius of aux rings [um]")
        width = i3.PositiveNumberProperty(doc="Width of all the access waveguides [um]", default=1.0)
        length = i3.PositiveNumberProperty(doc="Length of the straight waveguides [um]", default=100.0)
        coupler_gap = i3.PositiveNumberProperty(doc="Gap between ring and coupler [um]", default=1.0)
        ring_gap = i3.PositiveNumberProperty(doc="Gap between two rings [um]", default=1.0)
        ring_width = i3.PositiveNumberProperty(doc="Width of the arc waveguides [um]", default=1.0)
        euler = i3.IntProperty(
            default=0,
            doc="Use Euler Bend?",
            restriction=i3.RestrictValueList((0, 1)),
        )

        def validate_properties(self):
            validate_on_grid("width", self.width, self.__class__.__name__)
            return True

        def _default_main_radius(self):
            return i3.TECH.TECH.MINIMUM_BEND_RADIUS

        def _default_aux_radius(self):
            return i3.TECH.TECH.MINIMUM_BEND_RADIUS

        # def _default_straight(self):
        #     lv = self.cell.straight.get_default_view(self)
        #     lv.set(width=self.width, length=self.length)
        #     return lv

        def _default_main_ring(self):
            lv = self.cell.main_ring.get_default_view(self)
            lv.set(radius=self.main_radius)
            lv.set(gap0=self.coupler_gap)
            lv.set(ring_width=self.ring_width)
            return lv

        def _default_aux_ring(self):
            lv = self.cell.aux_ring.get_default_view(self)
            lv.set(radius=self.aux_radius)
            lv.set(ring_width=self.ring_width)
            return lv

        def _generate_instances(self, insts):
            ring_gap = self.ring_gap
            coupler_gap = self.coupler_gap
            ring_width = self.ring_width
            main_radius = self.main_radius
            aux_radius = self.aux_radius
            ring_width = self.ring_width
            length = self.length

            main_ring_height = coupler_gap + ring_width + 2*main_radius + ring_width
            aux_ring_height = coupler_gap +  ring_width + 2 * aux_radius + ring_width

            insts_dict = { "main_ring":self.main_ring, "aux_ring":self.aux_ring}
            instances = insts_dict

            specs = [
                # i3.Place("straight_0:in0", (0.0, 0.0)),

                i3.Place("main_ring:in0", (0.0, 0.0)),

                i3.Place("aux_ring", (0 + (main_radius+ aux_radius + ring_width + ring_gap)*np.cos(np.deg2rad(0)), (main_radius+ aux_radius + ring_width + ring_gap)*np.sin(np.deg2rad(0)) + main_ring_height/2  - aux_ring_height/2),
                         relative_to="main_ring:in0"),
                # i3.FlipV("aux_ring")

                ]

            return i3.place_and_route(instances, specs)

        def _generate_ports(self, ports):
                return i3.expose_ports(
                    self.instances,
                    {
                        # "main_ring:in0": "in0",
                        # "straight_0:in0": "in1",
                        # "main_ring:out0": "out0",
                        # "straight_0:out0": "out1",
                    },
                )

    class Netlist(i3.NetlistFromLayout):
        pass





