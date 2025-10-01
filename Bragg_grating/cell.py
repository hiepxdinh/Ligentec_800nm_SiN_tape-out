
import sys

sys.path.append("C:/pdk/Ligentec_SiN_2025/ipkiss")


import ligentec_an800.all as pdk
import ipkiss3.all as i3
import numpy as np

class Unit_Cell(i3.PCell):

    waveguide_1 = i3.ChildCellProperty(doc="straight waveguide", locked=True)

    waveguide_2 = i3.ChildCellProperty(doc="straight waveguide", locked=True)

    def _default_waveguide_1(self):
        wg_1 = pdk.Straight(name=self.name + "_WG1")
        return wg_1

    def _default_waveguide_2(self):
        wg_2 = pdk.Straight(name=self.name + "_WG2")
        return wg_2

    class Layout(i3.LayoutView):
        width_1 = i3.PositiveNumberProperty(default=1.0, doc="width of first waveguide")
        width_2 = i3.PositiveNumberProperty(default=2.0, doc="width of second waveguide")
        length_1 = i3.PositiveNumberProperty(default=1.0, doc="length of first waveguide")
        length_2 = i3.PositiveNumberProperty(default=2.0, doc="length of second waveguide")

        unit_cell_length = i3.PositiveNumberProperty(doc="length of unit cell")

        def _default_unit_cell_length (self):
            return self.length_1 + self.length_2

        def _default_waveguide_1(self):
            cell = self.cell.waveguide_1
            lv = cell.get_default_view(self)
            lv.set(
                width=self.width_1,
                length=self.length_1,
            )
            return lv

        def _default_waveguide_2(self):
            cell = self.cell.waveguide_2
            lv = cell.get_default_view(self)
            lv.set(
                width=self.width_2,
                length=self.length_2,
            )
            return lv

        def _generate_instances(self, insts):
            waveguide_1 = self.waveguide_1
            waveguide_2 = self.waveguide_2

            insts += i3.SRef(name="waveguide_1", reference=waveguide_1, flatten=True)
            insts += i3.SRef(name="waveguide_2", reference=waveguide_2, flatten=True)

            return i3.place_and_route(
                insts=insts,
                specs=[
                    i3.Place("waveguide_1", (0, 0)),
                    i3.Place("waveguide_2", (0, 0), relative_to="waveguide_1:out0"),
                    ]
            )

        def _generate_ports(self, ports):
            return i3.expose_ports(
                self.instances,
                {
                    "waveguide_1:in0": "in0",
                    "waveguide_2:out0": "out0",
                },
            )

unit_cell = Unit_Cell()
unit_cell_lo = unit_cell.Layout()

class Bragg_grating(i3.PCell):
    unit_cell_lo = i3.ChildCellProperty(doc='unit cell of the grating')

    # def _default_unit_cell(self):
    #     return Unit_Cell()

    class Layout(i3.LayoutView):

        grating_length = i3.PositiveNumberProperty(doc='Total length of the grating')

        period = i3.PositiveIntProperty(default = 10, doc= 'the number of times the unit cell repeats')

        def _default_grating_length(self):
            return unit_cell_lo.unit_cell_length * self.period

        def _generate_instances(self, insts):
            insts += i3.ARef(reference=self.unit_cell_lo, origin=(0, 0), period=(unit_cell_lo.unit_cell_length,0),
                             n_o_periods=(self.period,1))

            return insts







