import ligentec_an800.all as ligentec

import ipkiss3.all as i3


class Waveguide_test(i3.Circuit):

    taper = i3.ChildCellProperty("edge coupler")
    trace_template_in = i3.TraceTemplateProperty(doc="waveguide template used in the circuit")
    trace_template_out = i3.TraceTemplateProperty(doc="waveguide template used in the circuit")
    linear_transition = i3.ChildCellProperty(doc="linear transition waveguide")

    def _default_taper(self):
        return ligentec.AN800BB_EdgeCoupler_Lensed_C()

    def _default_trace_template_in(self):
        return ligentec.WireWaveguideTemplate()

    def _default_trace_template_out(self):
        return ligentec.WireWaveguideTemplate()

    def _default_linear_transition(self):
        return ligentec.LinearTaperFromPort(start_trace_template=self.trace_template_in, end_trace_template=self.trace_template_out)

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
            i3.Place("out_taper", position = (10000,0), angle = 0),
            i3.Place("linear_transition_in", position = (35,0), angle = 180, relative_to="in_taper:in0"),
            i3.Place("linear_transition_out", position=(-35, 0), relative_to="out_taper:in0"),
            i3.ConnectBend("in_taper:in0", "linear_transition_in:out"),
            i3.ConnectBend("out_taper:in0", "linear_transition_out:out"),
            i3.ConnectBend("linear_transition_in:in", "linear_transition_out:in"),
        ]

    class Layout(i3.Circuit.Layout):
        width_in = i3.PositiveNumberProperty(default=1.0, doc="width of input waveguide")
        width_out = i3.PositiveNumberProperty(default=1.8, doc="width of output waveguide")

        def _default_trace_template_in(self):
                lo = self.cell.trace_template_in.get_default_view(i3.LayoutView)
                lo.set(core_width=self.width_in)
                return lo

        def _default_trace_template_out(self):
                lo = self.cell.trace_template_out.get_default_view(i3.LayoutView)
                lo.set(core_width=self.width_out)
                return lo
