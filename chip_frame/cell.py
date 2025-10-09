import sys

sys.path.append("C:/pdk/Ligentec_SiN_2025/ipkiss")


from ipkiss3 import all as i3
import ligentec_an800.all as pdk

class Chip_Size_Layer_Frame(i3.PCell):
    owner = i3.StringProperty(default="", doc="Owner of the design")

    _name_prefix = "FRAME"

    class Layout(i3.LayoutView):
        boundary_line_width = i3.PositiveNumberProperty(default=5.0, doc="line width of the payload boundary",
                                                        locked=True)
        size = i3.Size2Property(default=(500, 500), doc="frame size")
        boundary_doc_layer = i3.LayerProperty(doc="documentation layer of the boundary")
        boundary_layer = i3.LayerProperty(doc="layer of the bounding box")
        with_ebl_writing_grid = i3.BoolProperty(default=False, doc="include EBL writing grid on the frame")
        ebl_writing_size = i3.Size2Property(default=(500, 500),
                                            doc="size of EBL writing field. Default is 500um x 500um")

        with_reference_waveguides = i3.BoolProperty(default=True, doc="include referencing waveguides at four corners")

        def _default_boundary_doc_layer(self):
            return i3.TECH.PPLAYER.CSL

        def _default_boundary_layer(self):
            return i3.TECH.PPLAYER.NONE.BBOX

        def _generate_elements(self, elems):
            X = self.size.x
            Y = self.size.y

            if self.with_ebl_writing_grid:
                # # Include dummy features at the origin
                # elems += i3.Path(layer=i3.TECH.PPLAYER.WG.TRENCH,
                #                  shape=i3.Shape([(10, self.boundary_line_width * 0.5),
                #                                  (self.boundary_line_width * 0.5, self.boundary_line_width * 0.5),
                #                                  (self.boundary_line_width * 0.5, 10)]),
                #                  line_width=self.boundary_line_width)
                #
                # elems += i3.Path(layer=i3.TECH.PPLAYER.WG.TRENCH,
                #                  shape=i3.Shape([(10, self.boundary_line_width * 0.5),
                #                                  (self.boundary_line_width * 0.5, self.boundary_line_width * 0.5),
                #                                  (self.boundary_line_width * 0.5, 10)]),
                #                  line_width=self.boundary_line_width)

                # Add EBL writing grid
                n_rows = int(Y / self.ebl_writing_size[1])
                n_cols = int(X / self.ebl_writing_size[0])
                for i in range(n_rows - 1):
                    elems += i3.Path(layer=self.boundary_doc_layer,
                                     shape=i3.Shape([(0, (i + 1) * self.ebl_writing_size[1]),
                                                     (n_cols * self.ebl_writing_size[0],
                                                      (i + 1) * self.ebl_writing_size[1])]),
                                     line_width=self.boundary_line_width)
                for i in range(n_cols - 1):
                    elems += i3.Path(layer=self.boundary_doc_layer,
                                     shape=i3.Shape([((i + 1) * self.ebl_writing_size[0], 0),
                                                     ((i + 1) * self.ebl_writing_size[0],
                                                      n_rows * self.ebl_writing_size[1])]),
                                     line_width=self.boundary_line_width)

            elems += i3.RectanglePath(layer=self.boundary_doc_layer,
                                      center=0.5 * self.size,
                                      box_size=(X - self.boundary_line_width,
                                                Y - self.boundary_line_width),
                                      line_width=self.boundary_line_width)

            elems += i3.Label(layer=self.boundary_doc_layer,
                              text=self.owner,
                              height=15.0,
                              coordinate=(0.5 * X, Y - 20),
                              alignment=(i3.TEXT.ALIGN.CENTER, i3.TEXT.ALIGN.TOP)
                              )

            return elems

        # def _generate_instances(self, insts):
            # if self.with_reference_waveguides:
            #     from picazzo3.routing.place_route import PlaceAndAutoRoute
            #     gc_y = pdk.GC_1550_ypropagation()
            #     gc_z = pdk.GC_1550_zpropagation()
            #     length = 500
            #     wg_t = pdk.WG1_TMPL()
            #     wg = i3.Waveguide(trace_template=wg_t)
            #     wg.Layout(shape=[(0, 0), (length, 0)])
            #     ref_y = PlaceAndAutoRoute(
            #                             name="REF_Y",
            #                             child_cells={
            #                                 'gc1': gc_y,
            #                                 'gc2': gc_y,
            #                             },
            #                             links=[('gc1:a0', 'gc2:a0')],
            #                             external_port_names={"gc1:vertical_in": "input",
            #                                                 "gc2:vertical_in": "output"
            #                                                 }
            #                         )
            #     ref_y_lo = ref_y.Layout(child_transformations={'gc1': (0, 0),
            #                                                 'gc2':  i3.HMirror() + i3.Translation(translation=(length, 0))}
            #                             )
            #
            #     insts += i3.SRef(name="REF_BOTTOM_LEFT_Y_1", reference=ref_y_lo, position=(75, 50))
            #     insts += i3.SRef(name="REF_BOTTOM_LEFT_Y_2", reference=ref_y_lo, position=(125, 100))
            #     insts += i3.SRef(name="REF_BOTTOM_RIGHT_Y_1", reference=ref_y_lo, position=(self.size[0] - length - 75, 50))
            #     insts += i3.SRef(name="REF_BOTTOM_RIGHT_Y_2", reference=ref_y_lo, position=(self.size[0] - length - 125, 100))
            #
            #     insts += i3.SRef(name="REF_TOP_LEFT_Y_1", reference=ref_y_lo, position=(75, self.size[1] - 50))
            #     insts += i3.SRef(name="REF_TOP_LEFT_Y_2", reference=ref_y_lo, position=(125, self.size[1] - 100))
            #     insts += i3.SRef(name="REF_TOP_RIGHT_Y_1", reference=ref_y_lo,
            #                     position=(self.size[0] - length - 75, self.size[1] - 50))
            #     insts += i3.SRef(name="REF_TOP_RIGHT_Y_2", reference=ref_y_lo,
            #                     position=(self.size[0] - length - 125, self.size[1] - 100))
            #
            #     ref_z = PlaceAndAutoRoute(
            #         name="REF_Z",
            #         child_cells={
            #             'gc1': gc_z,
            #             'gc2': gc_z,
            #         },
            #         links=[('gc1:a0', 'gc2:a0')],
            #         external_port_names={"gc1:vertical_in": "input",
            #                             "gc2:vertical_in": "output"
            #                             }
            #     )
            #     ref_z_lo = ref_z.Layout(child_transformations={'gc1': i3.Rotation(rotation=90),
            #                                                 'gc2': i3.Rotation(rotation=-90) + i3.Translation(
            #                                                     translation=(0, length))}
            #                             )
            #
            #     insts += i3.SRef(name="REF_BOTTOM_LEFT_Z_1", reference=ref_z_lo, position=(50, 75))
            #     insts += i3.SRef(name="REF_BOTTOM_LEFT_Z_2", reference=ref_z_lo, position=(100, 125))
            #     insts += i3.SRef(name="REF_BOTTOM_RIGHT_Z_1", reference=ref_z_lo,
            #                     position=(self.size[0] - 50, 75))
            #     insts += i3.SRef(name="REF_BOTTOM_RIGHT_Z_2", reference=ref_z_lo,
            #                     position=(self.size[0] - 100, 125))
            #
            #     insts += i3.SRef(name="REF_TOP_LEFT_Z_1", reference=ref_z_lo, position=(50, self.size[1] - length - 75))
            #     insts += i3.SRef(name="REF_TOP_LEFT_Z_2", reference=ref_z_lo, position=(100, self.size[1] - length - 125))
            #     insts += i3.SRef(name="REF_TOP_RIGHT_Z_1", reference=ref_z_lo,
            #                     position=(self.size[0] - 50, self.size[1] - length - 75))
            #     insts += i3.SRef(name="REF_TOP_RIGHT_Z_2", reference=ref_z_lo,
            #                     position=(self.size[0] - 100, self.size[1] - length - 125))
            #
            # return insts

    class Netlist(i3.NetlistView):
        # empty
        pass

class Chip_Handling_Size_Frame(i3.PCell):
    owner = i3.StringProperty(default="", doc="Owner of the design")

    _name_prefix = "FRAME"

    class Layout(i3.LayoutView):
        boundary_line_width = i3.PositiveNumberProperty(default=5.0, doc="line width of the payload boundary",
                                                        locked=True)
        size = i3.Size2Property(default=(500, 500), doc="frame size")
        boundary_doc_layer = i3.LayerProperty(doc="documentation layer of the boundary")
        boundary_layer = i3.LayerProperty(doc="layer of the bounding box")
        with_ebl_writing_grid = i3.BoolProperty(default=False, doc="include EBL writing grid on the frame")
        ebl_writing_size = i3.Size2Property(default=(500, 500),
                                            doc="size of EBL writing field. Default is 500um x 500um")

        with_reference_waveguides = i3.BoolProperty(default=True, doc="include referencing waveguides at four corners")

        def _default_boundary_doc_layer(self):
            return i3.TECH.PPLAYER.CHS

        def _default_boundary_layer(self):
            return i3.TECH.PPLAYER.NONE.BBOX

        def _generate_elements(self, elems):
            X = self.size.x
            Y = self.size.y

            if self.with_ebl_writing_grid:
                # # Include dummy features at the origin
                # elems += i3.Path(layer=i3.TECH.PPLAYER.WG.TRENCH,
                #                  shape=i3.Shape([(10, self.boundary_line_width * 0.5),
                #                                  (self.boundary_line_width * 0.5, self.boundary_line_width * 0.5),
                #                                  (self.boundary_line_width * 0.5, 10)]),
                #                  line_width=self.boundary_line_width)
                #
                # elems += i3.Path(layer=i3.TECH.PPLAYER.WG.TRENCH,
                #                  shape=i3.Shape([(10, self.boundary_line_width * 0.5),
                #                                  (self.boundary_line_width * 0.5, self.boundary_line_width * 0.5),
                #                                  (self.boundary_line_width * 0.5, 10)]),
                #                  line_width=self.boundary_line_width)

                # Add EBL writing grid
                n_rows = int(Y / self.ebl_writing_size[1])
                n_cols = int(X / self.ebl_writing_size[0])
                for i in range(n_rows - 1):
                    elems += i3.Path(layer=self.boundary_doc_layer,
                                     shape=i3.Shape([(0, (i + 1) * self.ebl_writing_size[1]),
                                                     (n_cols * self.ebl_writing_size[0],
                                                      (i + 1) * self.ebl_writing_size[1])]),
                                     line_width=self.boundary_line_width)
                for i in range(n_cols - 1):
                    elems += i3.Path(layer=self.boundary_doc_layer,
                                     shape=i3.Shape([((i + 1) * self.ebl_writing_size[0], 0),
                                                     ((i + 1) * self.ebl_writing_size[0],
                                                      n_rows * self.ebl_writing_size[1])]),
                                     line_width=self.boundary_line_width)

            elems += i3.RectanglePath(layer=self.boundary_doc_layer,
                                      center=0.5 * self.size,
                                      box_size=(X - self.boundary_line_width,
                                                Y - self.boundary_line_width),
                                      line_width=self.boundary_line_width)

            elems += i3.Label(layer=self.boundary_doc_layer,
                              text=self.owner,
                              height=15.0,
                              coordinate=(0.5 * X, Y - 20),
                              alignment=(i3.TEXT.ALIGN.CENTER, i3.TEXT.ALIGN.TOP)
                              )

            return elems

        # def _generate_instances(self, insts):
            # if self.with_reference_waveguides:
            #     from picazzo3.routing.place_route import PlaceAndAutoRoute
            #     gc_y = pdk.GC_1550_ypropagation()
            #     gc_z = pdk.GC_1550_zpropagation()
            #     length = 500
            #     wg_t = pdk.WG1_TMPL()
            #     wg = i3.Waveguide(trace_template=wg_t)
            #     wg.Layout(shape=[(0, 0), (length, 0)])
            #     ref_y = PlaceAndAutoRoute(
            #                             name="REF_Y",
            #                             child_cells={
            #                                 'gc1': gc_y,
            #                                 'gc2': gc_y,
            #                             },
            #                             links=[('gc1:a0', 'gc2:a0')],
            #                             external_port_names={"gc1:vertical_in": "input",
            #                                                 "gc2:vertical_in": "output"
            #                                                 }
            #                         )
            #     ref_y_lo = ref_y.Layout(child_transformations={'gc1': (0, 0),
            #                                                 'gc2':  i3.HMirror() + i3.Translation(translation=(length, 0))}
            #                             )
            #
            #     insts += i3.SRef(name="REF_BOTTOM_LEFT_Y_1", reference=ref_y_lo, position=(75, 50))
            #     insts += i3.SRef(name="REF_BOTTOM_LEFT_Y_2", reference=ref_y_lo, position=(125, 100))
            #     insts += i3.SRef(name="REF_BOTTOM_RIGHT_Y_1", reference=ref_y_lo, position=(self.size[0] - length - 75, 50))
            #     insts += i3.SRef(name="REF_BOTTOM_RIGHT_Y_2", reference=ref_y_lo, position=(self.size[0] - length - 125, 100))
            #
            #     insts += i3.SRef(name="REF_TOP_LEFT_Y_1", reference=ref_y_lo, position=(75, self.size[1] - 50))
            #     insts += i3.SRef(name="REF_TOP_LEFT_Y_2", reference=ref_y_lo, position=(125, self.size[1] - 100))
            #     insts += i3.SRef(name="REF_TOP_RIGHT_Y_1", reference=ref_y_lo,
            #                     position=(self.size[0] - length - 75, self.size[1] - 50))
            #     insts += i3.SRef(name="REF_TOP_RIGHT_Y_2", reference=ref_y_lo,
            #                     position=(self.size[0] - length - 125, self.size[1] - 100))
            #
            #     ref_z = PlaceAndAutoRoute(
            #         name="REF_Z",
            #         child_cells={
            #             'gc1': gc_z,
            #             'gc2': gc_z,
            #         },
            #         links=[('gc1:a0', 'gc2:a0')],
            #         external_port_names={"gc1:vertical_in": "input",
            #                             "gc2:vertical_in": "output"
            #                             }
            #     )
            #     ref_z_lo = ref_z.Layout(child_transformations={'gc1': i3.Rotation(rotation=90),
            #                                                 'gc2': i3.Rotation(rotation=-90) + i3.Translation(
            #                                                     translation=(0, length))}
            #                             )
            #
            #     insts += i3.SRef(name="REF_BOTTOM_LEFT_Z_1", reference=ref_z_lo, position=(50, 75))
            #     insts += i3.SRef(name="REF_BOTTOM_LEFT_Z_2", reference=ref_z_lo, position=(100, 125))
            #     insts += i3.SRef(name="REF_BOTTOM_RIGHT_Z_1", reference=ref_z_lo,
            #                     position=(self.size[0] - 50, 75))
            #     insts += i3.SRef(name="REF_BOTTOM_RIGHT_Z_2", reference=ref_z_lo,
            #                     position=(self.size[0] - 100, 125))
            #
            #     insts += i3.SRef(name="REF_TOP_LEFT_Z_1", reference=ref_z_lo, position=(50, self.size[1] - length - 75))
            #     insts += i3.SRef(name="REF_TOP_LEFT_Z_2", reference=ref_z_lo, position=(100, self.size[1] - length - 125))
            #     insts += i3.SRef(name="REF_TOP_RIGHT_Z_1", reference=ref_z_lo,
            #                     position=(self.size[0] - 50, self.size[1] - length - 75))
            #     insts += i3.SRef(name="REF_TOP_RIGHT_Z_2", reference=ref_z_lo,
            #                     position=(self.size[0] - 100, self.size[1] - length - 125))
            #
            # return insts

    class Netlist(i3.NetlistView):
        # empty
        pass

class CSL_FRAME_10500_4850(Chip_Size_Layer_Frame):
    _name_prefix = "FRAME_10500_4850"

    class Layout(Chip_Size_Layer_Frame.Layout):
        size = i3.Size2Property(default=(10500, 4850), doc="frame size", locked=True)


class CHS_FRAME_10500_4850_HALF(Chip_Handling_Size_Frame):
    _name_prefix = "CHS_FRAME_10500_4850_HALF"

    class Layout(Chip_Handling_Size_Frame.Layout):
        size = i3.Size2Property(default=(10500-10, (4850-10)/2 - 125/2), doc="frame size", locked=True)


class CHS_FRAME_10500_HALF_4850_HALF(Chip_Handling_Size_Frame):
    _name_prefix = "CHS_FRAME_10500_HALF_4850_HALF"

    class Layout(Chip_Handling_Size_Frame.Layout):
        size = i3.Size2Property(default=((10500-10)/2 - 125/2, (4850-10)/2 - 125/2), doc="frame size", locked=True)


class FRAME_10500_4850_WITH_EBL_GRID(Chip_Handling_Size_Frame):
    _name_prefix = "FRAME_10500_4850_EBL"

    class Layout(Chip_Handling_Size_Frame.Layout):
        size = i3.Size2Property(default=(10500, 4850/2 - 125/2), doc="frame size", locked=True)
        with_ebl_writing_grid = i3.BoolProperty(default=True, doc="include EBL writing grid on the frame", locked=True)
