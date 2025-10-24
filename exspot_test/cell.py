
import ligentec_an800.all as ligentec
import ipkiss3.all as i3

class Exspot_Spiral_Square(i3.Circuit):
    exspot = i3.ChildCellProperty(doc="exspot")
    spiral = i3.ChildCellProperty(doc="spiral")
    linear_taper = i3.ChildCellProperty(doc="linear_taper")

    def _default_exspot(self):
        return ligentec.AN800BB_ExSpot_SMF_C()

    def _default_spiral(self):
        return ligentec.SpiralSquare()

    def _default_linear_taper(self):
        return ligentec.Taper()

    def _default_insts(self):
        return {"exspot_in": self.exspot,
                "exspot_out": self.exspot,
                "spiral": self.spiral,
                "linear_taper_in":self.linear_taper,
                "linear_taper_out":self.linear_taper,
                }

    def _default_specs(self):
        x_spiral_length = self.spiral.get_default_view(i3.LayoutView).x_output
        # print(x_spiral_length)
        exspot_length = 620
        chip_size = 2357.5-10-38.97309+20+7.5+10
        return[
            i3.Place("spiral", position=(225, 0.0), angle=0),
            i3.Place("exspot_in", position=(chip_size/2-x_spiral_length+225, 0.0), angle=0, relative_to="spiral:in0"),
            i3.Place("exspot_out", position=(-chip_size/2+x_spiral_length+30+225,0.0), angle=180, relative_to="spiral:out0"),

            i3.Place("linear_taper_in", position=(-15, 0.0), angle=180, relative_to="exspot_in:in0"),
            i3.Place("linear_taper_out", position=(15, 0.0), angle=0,relative_to="exspot_out:in0"),

            i3.ConnectBend("linear_taper_in:in0", "exspot_in:in0"),
            i3.ConnectBend("linear_taper_out:in0", "exspot_out:in0"),
            #
            i3.ConnectBend("linear_taper_in:out0", "spiral:out0"),
            i3.ConnectBend("linear_taper_out:out0", "spiral:in0"),
        ]

    class Layout(i3.Circuit.Layout):
        spiral_length = i3.PositiveNumberProperty(default=100, doc="length of spiral")

        width_in = i3.PositiveNumberProperty(default=1.0, doc="width of input waveguide")
        width_out = i3.PositiveNumberProperty(default=1.8, doc="width of output waveguide")
        linear_taper_length = i3.PositiveNumberProperty(default=100, doc="length of linear taper")
        n_o_loops = i3.PositiveIntProperty(default=2, doc="number of loops")
        bend_radius = i3.PositiveIntProperty(default=50, doc="number of loops")

        def _default_spiral(self):
            lo = self.cell.spiral.get_default_view(i3.LayoutView)
            lo.set(total_length=self.spiral_length)
            lo.set(straight_width=self.width_out)
            lo.set(bend_width=self.width_out)
            lo.set(euler=1)
            lo.set(n_o_loops=self.n_o_loops)
            lo.set(bend_radius=self.bend_radius)
            # lo.set(x_output = 650)
            return lo

        def _default_linear_taper(self):
            cell = self.cell.linear_taper
            lv = cell.get_default_view(self)
            lv.set(
                in_width=self.width_in,
                out_width=self.width_out,
                length=self.linear_taper_length
            )
            return lv

        def _generate_elements(self, elems):
            """
            add labels at in/out put grating couplers regions
            """
            in_port = self.instances["exspot_in"].ports["in0"]
            in_text_position = in_port.position
            in_x = in_port.position.x
            in_y = in_port.position.y

            out_port = self.instances["exspot_out"].ports["in0"]
            out_text_position = out_port.position
            out_x = out_port.position.x
            out_y = out_port.position.y

            elems += i3.PolygonText(
                layer=i3.TECH.PPLAYER.X1P,
                coordinate=(in_x+110+0, in_y+35),
                text="SPIRAL_" +str(self.spiral_length) + "_" +str(self.width_out),
                alignment=(i3.TEXT.ALIGN.CENTER, i3.TEXT.ALIGN.CENTER),
                font=i3.TEXT.FONT.DEFAULT,
                height=10,
                # transformation=i3.VMirror()
            )

            elems += i3.PolygonText(
                layer=i3.TECH.PPLAYER.X1P,
                coordinate=(out_x-110-0, out_y+35),
                text="SPIRAL_" +str(self.spiral_length) + "_" +str(self.width_out),
                alignment=(i3.TEXT.ALIGN.CENTER, i3.TEXT.ALIGN.CENTER),
                font=i3.TEXT.FONT.DEFAULT,
                height=10,
                # transformation=i3.VMirror()
            )

            return elems

class Exspot_Spiral_Square_2(i3.Circuit):
    exspot = i3.ChildCellProperty(doc="exspot")
    spiral = i3.ChildCellProperty(doc="spiral")
    linear_taper = i3.ChildCellProperty(doc="linear_taper")

    def _default_exspot(self):
        return ligentec.AN800BB_ExSpot_SMF_C()

    def _default_spiral(self):
        return ligentec.SpiralSquare()

    def _default_linear_taper(self):
        return ligentec.Taper()

    def _default_insts(self):
        return {"exspot_in": self.exspot,
                "exspot_out": self.exspot,
                "spiral": self.spiral,
                "linear_taper_in":self.linear_taper,
                "linear_taper_out":self.linear_taper,
                }

    def _default_specs(self):
        x_spiral_length = self.spiral.get_default_view(i3.LayoutView).x_output
        # print(x_spiral_length)
        exspot_length = 620
        chip_size = 2357.5-10-38.97309+20+7.5+10
        return[
            i3.Place("spiral", position=(225, 0.0), angle=0),
            i3.Place("exspot_in", position=(chip_size/2-x_spiral_length+225-38.973, 0.0), angle=0, relative_to="spiral:in0"),
            i3.Place("exspot_out", position=(-chip_size/2+x_spiral_length+30+225,0.0), angle=180, relative_to="spiral:out0"),

            i3.Place("linear_taper_in", position=(-15, 0.0), angle=180, relative_to="exspot_in:in0"),
            i3.Place("linear_taper_out", position=(15, 0.0), angle=0,relative_to="exspot_out:in0"),

            i3.ConnectBend("linear_taper_in:in0", "exspot_in:in0"),
            i3.ConnectBend("linear_taper_out:in0", "exspot_out:in0"),
            #
            i3.ConnectBend("linear_taper_in:out0", "spiral:out0"),
            i3.ConnectBend("linear_taper_out:out0", "spiral:in0"),
        ]

    class Layout(i3.Circuit.Layout):
        spiral_length = i3.PositiveNumberProperty(default=100, doc="length of spiral")

        width_in = i3.PositiveNumberProperty(default=1.0, doc="width of input waveguide")
        width_out = i3.PositiveNumberProperty(default=1.8, doc="width of output waveguide")
        linear_taper_length = i3.PositiveNumberProperty(default=100, doc="length of linear taper")
        n_o_loops = i3.PositiveIntProperty(default=2, doc="number of loops")
        bend_radius = i3.PositiveIntProperty(default=50, doc="number of loops")

        def _default_spiral(self):
            lo = self.cell.spiral.get_default_view(i3.LayoutView)
            lo.set(total_length=self.spiral_length)
            lo.set(straight_width=self.width_out)
            lo.set(bend_width=self.width_out)
            lo.set(euler=1)
            lo.set(n_o_loops=self.n_o_loops)
            lo.set(bend_radius=self.bend_radius)
            # lo.set(x_output = 650)
            return lo

        def _default_linear_taper(self):
            cell = self.cell.linear_taper
            lv = cell.get_default_view(self)
            lv.set(
                in_width=self.width_in,
                out_width=self.width_out,
                length=self.linear_taper_length
            )
            return lv

        def _generate_elements(self, elems):
            """
            add labels at in/out put grating couplers regions
            """
            in_port = self.instances["exspot_in"].ports["in0"]
            in_text_position = in_port.position
            in_x = in_port.position.x
            in_y = in_port.position.y

            out_port = self.instances["exspot_out"].ports["in0"]
            out_text_position = out_port.position
            out_x = out_port.position.x
            out_y = out_port.position.y

            elems += i3.PolygonText(
                layer=i3.TECH.PPLAYER.X1P,
                coordinate=(in_x+110+0, in_y+30+5),
                text="SPIRAL_" +str(self.spiral_length) + "_" +str(self.width_out),
                alignment=(i3.TEXT.ALIGN.CENTER, i3.TEXT.ALIGN.CENTER),
                font=i3.TEXT.FONT.DEFAULT,
                height=10,
                # transformation=i3.VMirror()
            )

            elems += i3.PolygonText(
                layer=i3.TECH.PPLAYER.X1P,
                coordinate=(out_x-110-0, out_y+30+5),
                text="SPIRAL_" +str(self.spiral_length) + "_" +str(self.width_out),
                alignment=(i3.TEXT.ALIGN.CENTER, i3.TEXT.ALIGN.CENTER),
                font=i3.TEXT.FONT.DEFAULT,
                height=10,
                # transformation=i3.VMirror()
            )

            return elems

class Exspot_Spiral_Circular_GC(i3.Circuit):
    exspot = i3.ChildCellProperty(doc="exspot")
    spiral = i3.ChildCellProperty(doc="spiral")
    linear_taper = i3.ChildCellProperty(doc="linear_taper")

    def _default_exspot(self):
        return ligentec.AN800BB_FGC_8_TE_C()

    def _default_spiral(self):
        return ligentec.SpiralCircular()

    def _default_linear_taper(self):
        return ligentec.Taper()


    def _default_insts(self):
        return {"exspot_in": self.exspot,
                "exspot_out": self.exspot,
                "spiral": self.spiral,
                "linear_taper_in": self.linear_taper,
                # "linear_taper_out": self.linear_taper,
                }

    def _default_specs(self):
        return[
            i3.Place("spiral", position=(0.0, 0.0), angle=0),
            i3.Place("exspot_in", position=(-225.0, 120.0), angle=180, relative_to="spiral:in0"),
            i3.Place("exspot_out", position=(150.0-40-10, 120.0), angle=0, relative_to="spiral:in0"),

            i3.Place("linear_taper_in", position=(20, 0.0), angle=0, relative_to="exspot_in:in0"),

            i3.ConnectBend("exspot_in:in0", "linear_taper_in:in0"),
            i3.ConnectBend("spiral:out0", "linear_taper_in:out0"),
            i3.ConnectBend("spiral:in0", "exspot_out:in0"),
        ]

    class Layout(i3.Circuit.Layout):
        spiral_length = i3.PositiveNumberProperty(default=10000, doc="length of spiral")

        width_in = i3.PositiveNumberProperty(default=1.0, doc="width of input waveguide")
        width_out = i3.PositiveNumberProperty(default=1.0, doc="width of output waveguide")
        linear_taper_length = i3.PositiveNumberProperty(default=10, doc="length of linear taper")

        def _default_spiral(self):
            lo = self.cell.spiral.get_default_view(i3.LayoutView)
            lo.set(length=self.spiral_length)
            lo.set(radius=50)
            lo.set(spacing=2)
            return lo

        def _default_linear_taper(self):
            cell = self.cell.linear_taper
            lv = cell.get_default_view(self)
            lv.set(
                in_width=self.width_in,
                out_width=self.width_out,
                length=self.linear_taper_length
            )
            return lv

        def _generate_elements(self, elems):
            """
            add labels at in/out put grating couplers regions
            """
            ring_position = (0,0)

            elems += i3.PolygonText(
                layer=i3.TECH.PPLAYER.X1P,
                coordinate=(-150, 18),
                text="SPIRAL" +str(self.spiral_length),
                alignment=(i3.TEXT.ALIGN.CENTER, i3.TEXT.ALIGN.CENTER),
                font=i3.TEXT.FONT.DEFAULT,
                height=10,
                # transformation=i3.VMirror()
            )
            return elems

class Exspot_Spiral_Circular(i3.Circuit):
    exspot = i3.ChildCellProperty(doc="exspot")
    spiral = i3.ChildCellProperty(doc="spiral")
    linear_taper = i3.ChildCellProperty(doc="linear_taper")

    def _default_exspot(self):
        return ligentec.AN800BB_ExSpot_SMF_C()

    def _default_spiral(self):
        return ligentec.SpiralCircular()

    def _default_linear_taper(self):
        return ligentec.Taper()


    def _default_insts(self):
        return {"exspot_in": self.exspot,
                "exspot_out": self.exspot,
                "spiral": self.spiral,
                "linear_taper_in": self.linear_taper,
                "linear_taper_out": self.linear_taper,
                }

    def _default_specs(self):
        return[
            i3.Place("spiral", position=(0.0, 0.0), angle=0),
            i3.Place("exspot_in", position=(-300.0, 127.0), angle=180, relative_to="spiral:in0"),
            i3.Place("exspot_out", position=(-300.0, 0), angle=180, relative_to="spiral:in0"),

            i3.Place("linear_taper_in", position=(115, 0.0), angle=180, relative_to="exspot_in:in0"),
            i3.Place("linear_taper_out", position=(115, 0.0), angle=180, relative_to="exspot_out:in0"),

            i3.ConnectBend("linear_taper_in:out0", "exspot_in:in0"),
            i3.ConnectBend("linear_taper_out:out0", "exspot_out:in0"),

            i3.ConnectBend("spiral:in0", "linear_taper_in:in0"),
            i3.ConnectBend("spiral:out0", "linear_taper_out:in0"),
        ]

    class Layout(i3.Circuit.Layout):
        spiral_length = i3.PositiveNumberProperty(default=10000, doc="length of spiral")

        width_in = i3.PositiveNumberProperty(default=1.0, doc="width of input waveguide")
        width_out = i3.PositiveNumberProperty(default=1.0, doc="width of output waveguide")
        linear_taper_length = i3.PositiveNumberProperty(default=100, doc="length of linear taper")

        def _default_spiral(self):
            lo = self.cell.spiral.get_default_view(i3.LayoutView)
            lo.set(length=self.spiral_length)
            lo.set(radius=100)
            return lo

        def _default_linear_taper(self):
            cell = self.cell.linear_taper
            lv = cell.get_default_view(self)
            lv.set(
                in_width=self.width_in,
                out_width=self.width_out,
                length=self.linear_taper_length
            )
            return lv
