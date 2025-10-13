
import ligentec_an800.all as ligentec
import ipkiss3.all as i3

class Exspot_Spiral_Square(i3.Circuit):
    exspot = i3.ChildCellProperty(doc="exspot")
    spiral = i3.ChildCellProperty(doc="spiral")

    def _default_exspot(self):
        return ligentec.AN800BB_ExSpot_SMF_C()

    def _default_spiral(self):
        return ligentec.SpiralSquare()

    def _default_insts(self):
        return {"exspot_in": self.exspot,
                "exspot_out": self.exspot,
                "spiral": self.spiral,
                }

    def _default_specs(self):
        x_spiral_length = self.spiral.get_default_view(i3.LayoutView).x_output
        # print(x_spiral_length)
        exspot_length = 620
        chip_size = 2357.5
        return[
            i3.Place("spiral", position=(0.0, 0.0), angle=0),
            i3.Place("exspot_in", position=(chip_size/2-x_spiral_length, 0.0), angle=0, relative_to="spiral:in0"),
            i3.Place("exspot_out", position=(-chip_size/2+x_spiral_length+30,0.0), angle=180, relative_to="spiral:out0"),
            i3.ConnectBend("spiral:in0", "exspot_out:in0"),
            i3.ConnectBend("spiral:out0", "exspot_in:in0"),
        ]

    class Layout(i3.Circuit.Layout):
        spiral_length = i3.PositiveNumberProperty(default=100, doc="length of spiral")

        def _default_spiral(self):
            lo = self.cell.spiral.get_default_view(i3.LayoutView)
            lo.set(total_length=self.spiral_length)
            return lo

class Exspot_Spiral_Circular(i3.Circuit):
    exspot = i3.ChildCellProperty(doc="exspot")
    spiral = i3.ChildCellProperty(doc="spiral")

    def _default_exspot(self):
        return ligentec.AN800BB_ExSpot_SMF_C()

    def _default_spiral(self):
        return ligentec.SpiralCircular()

    def _default_insts(self):
        return {"exspot_in": self.exspot,
                "exspot_out": self.exspot,
                "spiral": self.spiral,
                }

    def _default_specs(self):
        return[
            i3.Place("spiral", position=(0.0, 0.0), angle=0),
            i3.Place("exspot_in", position=(1000.0, 0.0), angle=0, relative_to="spiral:in0"),
            i3.Place("exspot_out", position=(-1000.0,0.0), angle=180, relative_to="spiral:out0"),
            i3.ConnectBend("spiral:in0", "exspot_out:in0"),
            i3.ConnectBend("spiral:out0", "exspot_in:in0"),
        ]

    class Layout(i3.Circuit.Layout):
        spiral_length = i3.PositiveNumberProperty(default=100, doc="length of spiral")

        def _default_spiral(self):
            lo = self.cell.spiral.get_default_view(i3.LayoutView)
            lo.set(length=self.spiral_length)
            return lo
