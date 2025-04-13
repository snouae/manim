
from manim import *
from manim_voiceover import VoiceoverScene
from src.utils.kokoro_voiceover import KokoroService
import numpy as np

# Helper class for scene-specific utilities
class Scene1_Helper:
    def __init__(self, scene):
        self.scene = scene
    
    def create_triangle(self):
        """Create right-angled triangle with specified proportions and styling"""
        triangle = Polygon(
            ORIGIN, [3, 0, 0], [0, 2, 0],
            stroke_color=GOLD,
            stroke_width=4,
            fill_opacity=0
        ).scale(0.6).move_to(ORIGIN)
        
        # Validate triangle position within safe area
        if max(abs(triangle.get_corner(UR)[0]), abs(triangle.get_corner(UR)[1])) > 3.5:
            self.scene.add(SurroundingRectangle(triangle, color=RED))  # Visual debug
            # Comment: Potential safe area violation - manual position check required
        return triangle
    
    def create_angle_marker(self, triangle):
        """Create right angle marker at triangle vertex"""
        line1 = Line(triangle.get_vertices()[0], triangle.get_vertices()[1])
        line2 = Line(triangle.get_vertices()[0], triangle.get_vertices()[2])
        return RightAngle(line1, line2, length=0.4, color=GOLD, stroke_width=3)
    
    def create_side_labels(self, triangle):
        """Generate properly positioned side labels with buffer spacing"""
        hypotenuse = Line(triangle.get_vertices()[1], triangle.get_vertices()[2])
        
        label_a = Tex("a", color=BLUE, font_size=36).next_to(
            triangle.get_left_side(), LEFT, buff=0.3
        )
        label_b = Tex("b", color=BLUE, font_size=36).next_to(
            triangle.get_bottom_side(), DOWN, buff=0.3
        )
        label_c = Tex("c", color=RED, font_size=36).next_to(
            hypotenuse, UP, buff=0.3
        ).rotate(-np.arctan(2/3))  # Matches slope of hypotenuse
        
        # Validate label positions
        for label in [label_a, label_b, label_c]:
            if any(abs(coord) > 7 for coord in label.get_center()[:2]):
                # Comment: Label position exceeds safe margins - manual adjustment needed
                self.scene.add(SurroundingRectangle(label, color=YELLOW))
        return VGroup(label_a, label_b, label_c)
    
    def create_angle_annotation(self, angle_marker):
        """Generate 90° label with connecting arrow"""
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
        """Generate legs/hypotenuse terminology labels"""
        legs_text = Tex(r"\text{Legs}", color=BLUE, font_size=28).next_to(
            triangle, LEFT, buff=1.2
        ).align_to(triangle, UP)
        
        hypotenuse_text = Tex(r"\text{Hypotenuse}", color=RED, font_size=28).next_to(
            triangle, RIGHT, buff=1.2
        ).align_to(triangle, DOWN)
        
        # Spacing validation
        if legs_text.get_left()[0] < -6.5 or hypotenuse_text.get_right()[0] > 6.5:
            # Comment: Terminology labels near safe area limits - verify rendering
            self.scene.add(SurroundingRectangle(VGroup(legs_text, hypotenuse_text)))
        return VGroup(legs_text, hypotenuse_text)

class Scene1(VoiceoverScene):
    def construct(self):
        self.set_speech_service(KokoroService())
        helper = Scene1_Helper(self)
        
        # Stage 1: Triangle Construction
        with self.voiceover(text="At the heart of the Pythagorean theorem lies a fundamental shape - the right-angled triangle. Let's construct one with two perpendicular sides meeting at a 90-degree angle.") as tracker:
            triangle = helper.create_triangle()
            angle_marker = helper.create_angle_marker(triangle)
            self.play(Create(triangle), run_time=2)
            self.play(FadeIn(angle_marker))
            self.wait(0.5)
        
        # Stage 2: Side Labeling
        with self.voiceover(text="Every right-angled triangle has three key components. We call the two shorter sides that form the right angle the 'legs' - let's label them 'a' and 'b'. The third side, which always sits opposite the right angle, has a special name - can you guess what it might be?") as tracker:
            labels = helper.create_side_labels(triangle)
            self.play(LaggedStart(
                FadeIn(labels[0]),
                FadeIn(labels[1]),
                FadeIn(labels[2].rotate(-33.69*DEGREES)),
                lag_ratio=0.3
            ))
            self.wait(1)
        
        # Stage 3: Angle Clarification
        with self.voiceover(text="That's right - we call this longest side the hypotenuse, labeled 'c'. Remember this distinction: legs create the right angle, while the hypotenuse always opposes it.") as tracker:
            angle_label, arrow = helper.create_angle_annotation(angle_marker)
            self.play(Circumscribe(angle_marker, color=GOLD))
            self.play(Write(angle_label), Create(arrow))
            self.wait(1)
        
        # Stage 4: Terminology Reveal
        with self.voiceover(text="Let's solidify these terms. The 'legs' (a and b) form the foundation of the triangle, while the 'hypotenuse' (c) acts as the connecting bridge between them.") as tracker:
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
        
        # Final validation overlay
        debug_grid = NumberPlane().set_opacity(0.2)
        self.add(debug_grid)  # Comment: Remove for final render
        self.wait(0.5)
