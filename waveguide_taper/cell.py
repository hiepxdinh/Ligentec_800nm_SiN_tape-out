import ligentec_an800.all as pdk

import ipkiss3.all as i3


class Waveguide_Exspot(i3.Circuit):

    taper = i3.ChildCellProperty("edge coupler")
    # trace_template_in = i3.TraceTemplateProperty(doc="waveguide template used in the circuit")
    # trace_template_out = i3.TraceTemplateProperty(doc="waveguide template used in the circuit")
    linear_transition = i3.ChildCellProperty(doc="linear transition waveguide")

    def _default_taper(self):
        return pdk.AN800BB_ExSpot_SMF_C()

    # def _default_trace_template_in(self):
    #     return pdk.WireWaveguideTemplate()
    #
    # def _default_trace_template_out(self):
    #     return pdk.WireWaveguideTemplate()

    def _default_linear_transition(self):
        # return ligentec.LinearTaperFromPort(start_trace_template=self.trace_template_in, end_trace_template=self.trace_template_out)
        return pdk.Taper()

    def _default_insts(self):
        return {
                "in_taper": self.taper,
                "out_taper": self.taper,
                "linear_transition_in": self.linear_transition,
                "linear_transition_out": self.linear_transition,
                }

    def _default_specs(self):
        return[
            i3.Place("in_taper", position = (0,0), angle = 180),
            i3.Place("out_taper", position = (10000-750+20,0), angle = 0),
            i3.Place("linear_transition_in", position = (15,0), angle = 0, relative_to="in_taper:in0"),
            i3.Place("linear_transition_out", position=(-15, 0), angle = 180, relative_to="out_taper:in0"),
            i3.ConnectBend("in_taper:in0", "linear_transition_in:in0"),
            i3.ConnectBend("out_taper:in0", "linear_transition_out:in0"),
            i3.ConnectBend("linear_transition_in:out0", "linear_transition_out:out0"),
        ]

    class Layout(i3.Circuit.Layout):
        width_in = i3.PositiveNumberProperty(default=1.0, doc="width of input waveguide")
        width_out = i3.PositiveNumberProperty(default=1.5, doc="width of output waveguide")
        linear_taper_length=i3.PositiveNumberProperty(default=100, doc="length of linear taper")

        def _default_trace_template_in(self):
                lo = self.cell.trace_template_in.get_default_view(i3.LayoutView)
                lo.set(core_width=self.width_in)
                return lo

        def _default_trace_template_out(self):
                lo = self.cell.trace_template_out.get_default_view(i3.LayoutView)
                lo.set(core_width=self.width_out)
                return lo

        def _default_linear_transition(self):
            cell = self.cell.linear_transition
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
            in_port = self.instances["in_taper"].ports["in0"]
            in_text_position = in_port.position
            in_x = in_port.position.x
            in_y = in_port.position.y

            out_port = self.instances["out_taper"].ports["in0"]
            out_text_position = out_port.position
            out_x = out_port.position.x
            out_y = out_port.position.y

            elems += i3.PolygonText(
                layer=i3.TECH.PPLAYER.X1P,
                coordinate=(in_x+60, in_y+10+10),
                text="SC_WG_" +str(self.width_out),
                alignment=(i3.TEXT.ALIGN.CENTER, i3.TEXT.ALIGN.CENTER),
                font=i3.TEXT.FONT.DEFAULT,
                height=10,
                # transformation=i3.VMirror()
            )

            elems += i3.PolygonText(
                layer=i3.TECH.PPLAYER.X1P,
                coordinate=(out_x-60, out_y+10+10),
                text="SC_WG_" +str(self.width_out),
                alignment=(i3.TEXT.ALIGN.CENTER, i3.TEXT.ALIGN.CENTER),
                font=i3.TEXT.FONT.DEFAULT,
                height=10,
                # transformation=i3.VMirror()
            )

            return elems

class Waveguide_Exspot_2(i3.Circuit):

    taper = i3.ChildCellProperty("edge coupler")
    # trace_template_in = i3.TraceTemplateProperty(doc="waveguide template used in the circuit")
    # trace_template_out = i3.TraceTemplateProperty(doc="waveguide template used in the circuit")
    linear_transition = i3.ChildCellProperty(doc="linear transition waveguide")
    linear_transition_2 = i3.ChildCellProperty(doc="linear transition waveguide")

    def _default_taper(self):
        return pdk.AN800BB_ExSpot_SMF_C()

    # def _default_trace_template_in(self):
    #     return pdk.WireWaveguideTemplate()
    #
    # def _default_trace_template_out(self):
    #     return pdk.WireWaveguideTemplate()

    def _default_linear_transition(self):
        # return ligentec.LinearTaperFromPort(start_trace_template=self.trace_template_in, end_trace_template=self.trace_template_out)
        return pdk.Taper()

    def _default_linear_transition_2(self):
        # return ligentec.LinearTaperFromPort(start_trace_template=self.trace_template_in, end_trace_template=self.trace_template_out)
        return pdk.Taper()

    def _default_insts(self):
        return {
                "in_taper": self.taper,
                "out_taper": self.taper,
                "linear_transition_in": self.linear_transition,
                "linear_transition_in_2": self.linear_transition_2,
                "linear_transition_out": self.linear_transition_2,
                }

    def _default_specs(self):
        return[
            i3.Place("in_taper", position = (0,0), angle = 180),
            i3.Place("out_taper", position = (10000-750+20,50), angle = 0),
            i3.Place("linear_transition_in", position=(15, 0), angle=0, relative_to="in_taper:in0"),
            i3.Place("linear_transition_in_2", position = (175,50), angle = 0, relative_to="in_taper:in0"),
            i3.Place("linear_transition_out", position=(-15, 0), angle = 180, relative_to="out_taper:in0"),
            i3.ConnectBend("in_taper:in0", "linear_transition_in:in0", bend_radius=300),
            i3.ConnectBend("out_taper:in0", "linear_transition_out:in0", bend_radius=300),
            i3.ConnectBend("linear_transition_in:out0", "linear_transition_in_2:in0"),
            i3.ConnectBend("linear_transition_in_2:out0", "linear_transition_out:out0"),
        ]

    class Layout(i3.Circuit.Layout):
        width_in = i3.PositiveNumberProperty(default=1.0, doc="width of input waveguide")
        width_out = i3.PositiveNumberProperty(default=1.5, doc="width of output waveguide")
        linear_taper_length=i3.PositiveNumberProperty(default=100, doc="length of linear taper")

        def _default_trace_template_in(self):
                lo = self.cell.trace_template_in.get_default_view(i3.LayoutView)
                lo.set(core_width=self.width_in)
                return lo

        def _default_trace_template_out(self):
                lo = self.cell.trace_template_out.get_default_view(i3.LayoutView)
                lo.set(core_width=self.width_out)
                return lo

        def _default_linear_transition(self):
            cell = self.cell.linear_transition
            lv = cell.get_default_view(self)
            lv.set(
                in_width=1.0,
                out_width=1.0,
            )
            return lv

        def _default_linear_transition_2(self):
            cell = self.cell.linear_transition_2
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
            in_port = self.instances["in_taper"].ports["in0"]
            in_text_position = in_port.position
            in_x = in_port.position.x
            in_y = in_port.position.y

            out_port = self.instances["out_taper"].ports["in0"]
            out_text_position = out_port.position
            out_x = out_port.position.x
            out_y = out_port.position.y

            elems += i3.PolygonText(
                layer=i3.TECH.PPLAYER.X1P,
                coordinate=(in_x+110-50, in_y+25),
                text="SC_WG_" +str(self.width_out),
                alignment=(i3.TEXT.ALIGN.CENTER, i3.TEXT.ALIGN.CENTER),
                font=i3.TEXT.FONT.DEFAULT,
                height=10,
                # transformation=i3.VMirror()
            )

            elems += i3.PolygonText(
                layer=i3.TECH.PPLAYER.X1P,
                coordinate=(out_x-110+50, out_y+10+10),
                text="SC_WG_" +str(self.width_out),
                alignment=(i3.TEXT.ALIGN.CENTER, i3.TEXT.ALIGN.CENTER),
                font=i3.TEXT.FONT.DEFAULT,
                height=10,
                # transformation=i3.VMirror()
            )

            return elems

class Waveguide_Exspot_Ref(i3.Circuit):

    taper = i3.ChildCellProperty("edge coupler")
    # trace_template_in = i3.TraceTemplateProperty(doc="waveguide template used in the circuit")
    # trace_template_out = i3.TraceTemplateProperty(doc="waveguide template used in the circuit")
    linear_transition = i3.ChildCellProperty(doc="linear transition waveguide")

    def _default_taper(self):
        return pdk.AN800BB_ExSpot_SMF_C()

    # def _default_trace_template_in(self):
    #     return pdk.WireWaveguideTemplate()
    #
    # def _default_trace_template_out(self):
    #     return pdk.WireWaveguideTemplate()

    def _default_linear_transition(self):
        # return ligentec.LinearTaperFromPort(start_trace_template=self.trace_template_in, end_trace_template=self.trace_template_out)
        return pdk.Taper()

    def _default_insts(self):
        return {
                "in_taper": self.taper,
                "out_taper": self.taper,
                "linear_transition_in": self.linear_transition,
                "linear_transition_out": self.linear_transition,
                }

    def _default_specs(self):
        return[
            i3.Place("in_taper", position = (0-17.5,0), angle = 180),
            i3.Place("out_taper", position = (2350-750-485+2.5+10,0), angle = 0),
            i3.Place("linear_transition_in", position = (15,0), angle = 0, relative_to="in_taper:in0"),
            i3.Place("linear_transition_out", position=(-15, 0), angle = 180, relative_to="out_taper:in0"),
            i3.ConnectBend("in_taper:in0", "linear_transition_in:in0"),
            i3.ConnectBend("out_taper:in0", "linear_transition_out:in0"),
            i3.ConnectBend("linear_transition_in:out0", "linear_transition_out:out0"),
        ]

    class Layout(i3.Circuit.Layout):
        width_in = i3.PositiveNumberProperty(default=1.0, doc="width of input waveguide")
        width_out = i3.PositiveNumberProperty(default=1.0, doc="width of output waveguide")
        linear_taper_length=i3.PositiveNumberProperty(default=100, doc="length of linear taper")

        def _default_trace_template_in(self):
                lo = self.cell.trace_template_in.get_default_view(i3.LayoutView)
                lo.set(core_width=self.width_in)
                return lo

        def _default_trace_template_out(self):
                lo = self.cell.trace_template_out.get_default_view(i3.LayoutView)
                lo.set(core_width=self.width_out)
                return lo

        def _default_linear_transition(self):
            cell = self.cell.linear_transition
            lv = cell.get_default_view(self)
            lv.set(
                in_width=self.width_in,
                out_width=self.width_out,
                length=self.linear_taper_length
            )
            return lv