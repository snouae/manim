
from manim import *
import numpy as np

class Scene1_Helper:
    def __init__(self, scene):
        self.scene = scene
    
    def create_triangle(self):
        triangle = Polygon(
            ORIGIN, [3, 0, 0], [0, 2, 0],
            stroke_color=GOLD,
            stroke_width=4,
            fill_opacity=0
        ).scale(0.6).move_to(ORIGIN)
        
        if max(abs(triangle.get_corner(UR)[0]), abs(triangle.get_corner(UR)[1])) > 3.5:
            self.scene.add(SurroundingRectangle(triangle, color=RED))
        return triangle
    
    def create_angle_marker(self, triangle):
        line1 = Line(triangle.get_vertices()[0], triangle.get_vertices()[1])
        line2 = Line(triangle.get_vertices()[0], triangle.get_vertices()[2])
        return RightAngle(line1, line2, length=0.4, color=GOLD, stroke_width=3)
    
    def create_side_labels(self, triangle):
        hypotenuse = Line(triangle.get_vertices()[1], triangle.get_vertices()[2])
        
        label_a = Tex("a", color=BLUE, font_size=36).next_to(
            triangle.get_left_side(), LEFT, buff=0.3
        )
        label_b = Tex("b", color=BLUE, font_size=36).next_to(
            triangle.get_bottom_side(), DOWN, buff=0.3
        )
        label_c = Tex("c", color=RED, font_size=36).next_to(
            hypotenuse, UP, buff=0.3
        ).rotate(-np.arctan(2/3))
        
        for label in [label_a, label_b, label_c]:
            if any(abs(coord) > 7 for coord in label.get_center()[:2]):
                self.scene.add(SurroundingRectangle(label, color=YELLOW))
        return VGroup(label_a, label_b, label_c)
    
    def create_angle_annotation(self, angle_marker):
        angle_label = MathTex(r"90^\circ", color=GOLD, font_size=28).next_to(
            angle_marker, UR, buff=0.3
        )
        arrow = CurvedArrow(
            angle_label.get_bottom(),
            angle_marker.get_center(),
            angle=TAU/4,
            color=GOLD,
            stroke_width=3,
            tip_length=0.15
        )
        return angle_label, arrow
    
    def create_terminology_labels(self, triangle):
        legs_text = Tex(r"\text{Legs}", color=BLUE, font_size=28).next_to(
            triangle, LEFT, buff=1.2
        ).align_to(triangle, UP)
        
        hypotenuse_text = Tex(r"\text{Hypotenuse}", color=RED, font_size=28).next_to(
            triangle, RIGHT, buff=1.2
        ).align_to(triangle, DOWN)
        
        if legs_text.get_left()[0] < -6.5 or hypotenuse_text.get_right()[0] > 6.5:
            self.scene.add(SurroundingRectangle(VGroup(legs_text, hypotenuse_text)))
        return VGroup(legs_text, hypotenuse_text)

class Scene1(Scene):
    def construct(self):
        helper = Scene1_Helper(self)
        
        # Stage 1: Triangle Construction
        triangle = helper.create_triangle()
        angle_marker = helper.create_angle_marker(triangle)
        self.play(Create(triangle), run_time=2)
        self.play(FadeIn(angle_marker))
        self.wait(0.5)
        
        # Stage 2: Side Labeling
        labels = helper.create_side_labels(triangle)
        self.play(LaggedStart(
            FadeIn(labels[0]),
            FadeIn(labels[1]),
            FadeIn(labels[2].rotate(-33.69*DEGREES)),
            lag_ratio=0.3
        ))
        self.wait(1)
        
        # Stage 3: Angle Clarification
        angle_label, arrow = helper.create_angle_annotation(angle_marker)
        self.play(Circumscribe(angle_marker, color=GOLD))
        self.play(Write(angle_label), Create(arrow))
        self.wait(1)
        
        # Stage 4: Terminology Reveal
        terms = helper.create_terminology_labels(triangle)
        connector = CurvedArrow(
            terms[0].get_right(),
            labels[2].get_left(),
            angle=-TAU/4,
            color=GOLD,
            stroke_width=3
        )
        self.play(
            FlashAround(labels[:2], color=BLUE),
            FadeIn(terms[0]),
            Create(connector),
            FadeIn(terms[1])
        )
        self.wait(2)
        
        debug_grid = NumberPlane().set_opacity(0.2)
        self.add(debug_grid)
        self.wait(0.5)
