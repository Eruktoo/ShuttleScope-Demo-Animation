"""
ShuttleScope — Act 0 & Act 1
Gemini visual spec: fast-paced, no fade, high density.
"""

from manim import *
import numpy as np

# ══════════════════════════════════════════════════
# GLOBAL CONSTANTS
# ══════════════════════════════════════════════════
BG = "#111112"
C_SYQ = "#00E5FF"
C_KUN = "#FF9100"
C_CLUTCH = "#FF3D00"
C_MUTED = "#4A4A4A"
C_TEXT = "#E1E4ED"
MONO = "Liberation Mono"

# ══════════════════════════════════════════════════
# MATCH DATA — Set 3, 2024 WT Finals
# ══════════════════════════════════════════════════
SET3_PTS = [
    [1,0],[2,0],[2,1],[2,2],[3,2],[3,3],[3,4],[3,5],[4,5],[4,6],
    [5,6],[6,6],[6,7],[6,8],[6,9],[6,10],[6,11],[6,12],[6,13],[6,14],
    [7,14],[8,14],[8,15],[9,15],[10,15],[11,15],[12,15],[13,15],[14,15],[15,15],
    [15,16],[16,16],[17,16],[17,17],[18,17],[19,17],[19,18],[20,18],[20,19],[20,20],
    [20,21],[21,21],[22,21],[22,22],[23,22],[23,23],[24,23],[25,23]
]
N_PTS = len(SET3_PTS)

DIFFS = [p[0] - p[1] for p in SET3_PTS]
SYQ_WON = [p[0] > (SET3_PTS[i-1][0] if i > 0 else 0) for i, p in enumerate(SET3_PTS)]

# dt values for Set 3 (47 intervals between 48 points)
DT_VALS = [45,35,45,31,22,83,22,34,58,52,48,56,43,54,29,50,98,16,33,31,
           52,25,44,32,47,80,85,101,77,38,30,45,46,46,36,54,60,33,36,49,
           58,45,58,50,69,36,62]

# Pad to 48: particle i gets interval leading TO point i (pt[0]=0s)
PARTICLE_DT = [0] + DT_VALS  # 48 values
DT_MIN, DT_MAX = min(DT_VALS), max(DT_VALS)  # 16, 101

def bar_width(dt_val):
    """Map dt seconds to particle bar width."""
    return 0.02 + (dt_val - DT_MIN) / (DT_MAX - DT_MIN) * 0.14  # 0.02-0.16

# ── Helpers ──
def bg_grid():
    """Return a faint background grid (add with self.add(grid))."""
    grid = VGroup()
    for x in np.arange(-14, 15, 1.5):
        grid.add(Line([x, -8, 0], [x, 8, 0], color=C_MUTED, stroke_width=0.5, stroke_opacity=0.08))
    for y in np.arange(-8, 9, 1.5):
        grid.add(Line([-14, y, 0], [14, y, 0], color=C_MUTED, stroke_width=0.5, stroke_opacity=0.08))
    return grid


# ══════════════════════════════════════════════════
# ACT 0: OPENING (00:00 - 00:10)
# ══════════════════════════════════════════════════
class Act0_Opening(MovingCameraScene):
    """10s — Score cards burst in, traditional stats fail, camera zooms into Set 3 raw data."""

    def construct(self):
        self.camera.background_color = BG
        self.add(bg_grid())

        # ── Phase 1: Score burst [00:00-00:03] ──
        lines_data = [
            ("14", "21", C_KUN),  # KUN won set 1
            ("21", "19", C_SYQ),  # SYQ won set 2
            ("25", "23", C_MUTED),  # ongoing → muted
        ]
        score_lines = VGroup()
        for i, (a, b, col) in enumerate(lines_data):
            lbl = Text(
                f"{a.rjust(2)} · {b.ljust(2)}",
                font_size=36, color=col, font=MONO, weight=BOLD
            )
            lbl.shift(UP * (0.8 - i * 0.9) + LEFT * 3.5)
            score_lines.add(lbl)

        # Duration line on the right
        dur_line = Line(
            UP * 1.8 + RIGHT * 2.5, DOWN * 1.8 + RIGHT * 2.5,
            color=C_MUTED, stroke_width=1.5
        )
        dur_label = Text("89m", font_size=14, color=C_MUTED, font=MONO)
        dur_label.next_to(dur_line, RIGHT, buff=0.15)

        # Burst in: Write each line with mechanical snap
        for lbl in score_lines:
            self.play(Write(lbl, run_time=0.3, rate_func=linear))
        self.play(
            GrowFromCenter(dur_line, run_time=0.3),
            Write(dur_label, run_time=0.3)
        )
        self.wait(0.2)  # total ~1.5s so far, tight

        # ── Phase 2: Traditional stats fail [00:03-00:06] ──
        # Two bar charts (模拟传统数据): 60% vs 63%
        bar_a = Rectangle(width=0, height=2.4, fill_color=C_MUTED,
                          fill_opacity=0.3, stroke_width=0)
        bar_a.move_to(RIGHT * 1.5 + DOWN * 0.3, aligned_edge=DOWN)
        bar_b = Rectangle(width=0, height=2.52, fill_color=C_MUTED,
                          fill_opacity=0.3, stroke_width=0)
        bar_b.move_to(RIGHT * 3.1 + DOWN * 0.3, aligned_edge=DOWN)

        bar_label_a = Text("60%", font_size=14, color=C_TEXT, font=MONO)
        bar_label_a.next_to(bar_a, UP, buff=0.08)
        bar_label_b = Text("63%", font_size=14, color=C_TEXT, font=MONO)
        bar_label_b.next_to(bar_b, UP, buff=0.08)

        not_equal = Text("≠", font_size=48, color=C_MUTED, weight=BOLD)
        not_equal.move_to(RIGHT * 2.3 + UP * 0.8)

        self.play(
            bar_a.animate.set_width(0.5).set_height(2.4),
            bar_b.animate.set_width(0.5).set_height(2.52),
            run_time=0.4
        )
        self.play(
            Write(bar_label_a, run_time=0.2),
            Write(bar_label_b, run_time=0.2),
        )
        self.play(Write(not_equal, run_time=0.15))
        self.wait(0.2)  # total ~3.5s

        # ── Phase 3: Camera pan into Set 3 [00:06-00:10] ──
        # Score tiles shrink to upper-left corner
        # Camera frame zooms & pans to reveal raw data zone on the right

        # Build the "raw data zone" markers (will be revealed by camera movement)
        raw_hint = Text("第三局 逐分数据", font_size=14, color=C_MUTED, font=MONO)
        raw_hint.move_to(RIGHT * 3 + UP * 1.5)

        # Score tiles as a group to shrink
        all_scores = VGroup(*score_lines, dur_line, dur_label)

        self.play(
            all_scores.animate.scale(0.3).move_to(
                ORIGIN + LEFT * 5.5 + UP * 3
            ).set_opacity(0.5),
            self.camera.frame.animate.scale(0.55).move_to(RIGHT * 1.5),
            run_time=1.0,
            rate_func=rate_functions.exponential_decay
        )
        # Write the raw data hint while camera is settling
        self.play(Write(raw_hint, run_time=0.3))
        self.wait(0.2)

        # Clean exit: camera snaps back (no fade for scene transition)
        # The next scene (Act1_DataExplosion) starts with the grid visible


# ══════════════════════════════════════════════════
# ACT 1: DATA EXPLOSION (00:10 - 00:28)
# ══════════════════════════════════════════════════
class Act1_DataExplosion(MovingCameraScene):
    """18s — 48 dt-particles explode, sweep scan, streak pop."""

    def construct(self):
        self.camera.background_color = BG
        grid = bg_grid()
        self.add(grid)

        # Phase 1: 48 particles explode horizontally [00:10-00:18]
        particles = VGroup()
        x_cursor = -5.8
        gaps = np.full(N_PTS, 0.015)
        widths = [bar_width(d) for d in PARTICLE_DT]

        for i in range(N_PTS):
            w = widths[i]
            color = C_SYQ if SYQ_WON[i] else C_KUN
            rect = Rectangle(
                width=w, height=0.35,
                fill_color=color, fill_opacity=0.85,
                stroke_width=0
            )
            cx = x_cursor + w/2
            rect.move_to([cx, 0.5, 0])
            rect.streak_zone = (23 <= i <= 29)  # mark 7-streak particles
            rect.save_state()
            rect.scale(0)  # start invisible
            particles.add(rect)
            x_cursor += w + gaps[i]

        # Fiber-optic explosion
        self.play(
            LaggedStart(*[
                rect.animate.restore()
                for rect in particles
            ], lag_ratio=0.02, run_time=1.4),
            rate_func=rate_functions.ease_out_expo
        )

        # ════════════════════════════════════════════
        # Phase 2: Sweep scan + streak pop [00:18-00:28]
        # ════════════════════════════════════════════

        # ─ a) Sweep beam ─
        beam = Rectangle(
            width=0.15, height=2.0,
            fill_color=C_SYQ, fill_opacity=0.15,
            stroke_width=0
        )
        beam.move_to(particles.get_left() + LEFT * 0.3 + UP * 0.2)
        # Quick flash: beam appears instantly
        self.add(beam)

        # ─ b) 7-streak zone indices: 23-29 ─
        streak_particles = [p for p in particles if p.streak_zone]
        streak_center_x = np.mean([p.get_center()[0] for p in streak_particles])

        # Sweep beam animation
        sweep_target_x = particles.get_right()[0] + 0.3

        self.play(
            beam.animate.move_to([sweep_target_x, 0.7, 0]),
            run_time=0.7,
            rate_func=rate_functions.ease_in_out_expo
        )

        # Streak pop: particles scale up + shift up simultaneously
        streak_label = Text("7-0 Run", font_size=20, color=C_SYQ, font=MONO, weight=BOLD)
        streak_label.move_to([streak_center_x, 1.8, 0])

        self.play(
            *[p.animate.scale(1.6).shift(UP * 0.35)
              for p in streak_particles],
            Write(streak_label, run_time=0.25),
            run_time=0.35
        )

        # ─ c) Counter bar: 3+ streaks frequency ─
        bar_chart_bg = Rectangle(
            width=0.06, height=0,
            fill_color=C_SYQ, fill_opacity=0.6, stroke_width=0
        )
        bar_chart_bg.move_to(RIGHT * 1.0 + DOWN * 1.5, aligned_edge=DOWN)

        bar_label = Text("3+ 连得 1次", font_size=13, color=C_TEXT, font=MONO)
        bar_label.next_to(bar_chart_bg, RIGHT, buff=0.2)

        self.play(
            bar_chart_bg.animate.set_width(0.5).set(height=0.8),
            Write(bar_label, run_time=0.2),
            run_time=0.4
        )
        self.wait(0.3)

        # Hold for the next scene to take over
        # No scene transition cleanup — Act1_ClutchZone starts from here


# ══════════════════════════════════════════════════
# ACT 1 — PART 2: CLUTCH ZONE (00:28 - 00:50)
# ══════════════════════════════════════════════════
class Act1_ClutchZone(MovingCameraScene):
    """22s — Diff curve, comeback arc, clutch zone reveal, 5-card entry."""

    def construct(self):
        self.camera.background_color = BG
        self.add(bg_grid())

        # Recreate the 48 particles (same as Act1_DataExplosion)
        particles = VGroup()
        x_cursor = -5.8
        gaps = np.full(N_PTS, 0.015)
        widths = [bar_width(d) for d in PARTICLE_DT]

        particle_centers = []
        for i in range(N_PTS):
            w = widths[i]
            color = C_SYQ if SYQ_WON[i] else C_KUN
            rect = Rectangle(
                width=w, height=0.35,
                fill_color=color, fill_opacity=0.85,
                stroke_width=0
            )
            cx = x_cursor + w/2
            rect.move_to([cx, 0.5, 0])
            particles.add(rect)
            particle_centers.append(cx)
            x_cursor += w + gaps[i]

        # Create all particles instantly (pre-created, not animated in)
        self.add(particles)

        # ─ ═══════════════════════════════════════════
        # Phase 1: Diff curve [00:28-00:38]
        # ─ ═══════════════════════════════════════════

        # Score difference curve positioned below the particles
        curve_y = -1.0
        diff_min = min(DIFFS)  # -8
        diff_max = max(DIFFS)  # 2
        diff_range = diff_max - diff_min  # 10

        def diff_to_y(d):
            return curve_y + (d - diff_min) / diff_range * 1.8

        # Build the diff curve as a VMobject
        diff_curve = VMobject(stroke_color=C_SYQ, stroke_width=2.5, fill_opacity=0)
        points = [np.array([particle_centers[i], diff_to_y(DIFFS[i]), 0])
                  for i in range(N_PTS)]
        diff_curve.set_points_smoothly(points)

        # Add a horizontal zero line
        zero_diff_y = diff_to_y(0)
        zero_line = Line(
            [particle_centers[0] - 0.2, zero_diff_y, 0],
            [particle_centers[-1] + 0.2, zero_diff_y, 0],
            color=C_MUTED, stroke_width=0.5, stroke_opacity=0.3
        )

        # Draw the curve like lightning
        self.play(
            Create(diff_curve, run_time=1.0, rate_func=rate_functions.ease_out_expo),
            Create(zero_line, run_time=0.4)
        )

        # Red flash at max deficit (6-14 → diff=-8, particle index 19)
        deficit_idx = 19  # 6-14
        deficit_pos = np.array([
            particle_centers[deficit_idx],
            diff_to_y(DIFFS[deficit_idx]),
            0
        ])

        flash = Circle(
            radius=0.2, fill_color=C_CLUTCH,
            fill_opacity=0.8, stroke_width=0
        )
        flash.move_to(deficit_pos)
        # Two flashes
        self.play(
            flash.animate.scale(3).set_opacity(0).set_stroke_opacity(0),
            run_time=0.25
        )
        flash2 = flash.copy()
        flash2.move_to(deficit_pos).set_opacity(0.8).scale(0.33)
        self.add(flash2)
        self.play(
            flash2.animate.scale(2.5).set_opacity(0),
            run_time=0.2
        )

        # Label the deficit
        deficit_label = Text("6-14", font_size=14, color=C_CLUTCH, font=MONO, weight=BOLD)
        deficit_label.move_to(deficit_pos + DOWN * 0.4)
        self.play(Write(deficit_label, run_time=0.15))

        # Curve reverses toward 15-15 — highlight the comeback arc
        comeback_pos = np.array([
            particle_centers[29],  # 15-15, index 29
            diff_to_y(0),
            0
        ])
        comeback_label = Text("15-15", font_size=14, color=C_SYQ, font=MONO, weight=BOLD)
        comeback_label.move_to(comeback_pos + UP * 0.4)
        self.play(Write(comeback_label, run_time=0.15))

        # ─ ═══════════════════════════════════════════
        # Phase 2: Everything slides down [00:38-00:44]
        # ─ ═══════════════════════════════════════════

        # Slide everything down
        all_elements = VGroup(particles, diff_curve, zero_line,
                              deficit_label, comeback_label)

        self.play(
            all_elements.animate.shift(DOWN * 1.8).set_opacity(0.15),
            run_time=0.4,
            rate_func=rate_functions.ease_in_expo
        )

        # ─ ═══════════════════════════════════════════
        # Phase 3: Clutch zone reveal [00:44-00:50]
        # ─ ═══════════════════════════════════════════

        # Red laser dashed line at 20-20 boundary
        # 20-20 is point index 39 (out of 48), at ~81% of the total width
        clutch_x = particle_centers[39]
        laser_line = DashedLine(
            [clutch_x, 2.5, 0], [clutch_x, -2.5, 0],
            color=C_CLUTCH, stroke_width=2.5, dash_length=0.06
        )
        self.play(Create(laser_line, run_time=0.25, rate_func=linear))

        # Flash the laser
        laser_glow = Rectangle(
            width=0.3, height=5,
            fill_color=C_CLUTCH, fill_opacity=0.2, stroke_width=0
        )
        laser_glow.move_to([clutch_x, 0, 0])
        self.play(FadeIn(laser_glow, run_time=0.1))
        self.play(FadeOut(laser_glow, run_time=0.1))

        # Tag: "CLUTCH ZONE"
        clutch_tag = Text("CLUTCH ZONE", font_size=18, color=C_CLUTCH, font=MONO, weight=BOLD)
        clutch_tag.move_to([clutch_x, 2.8, 0])
        self.play(Write(clutch_tag, run_time=0.2))

        # ─ 5-card UI framework ─
        cards_data = [
            ("⚡", "压制力"),
            ("🛡️", "韧性"),
            ("🎯", "关键分"),
            ("🧠", "战术弹性"),
            ("🏃", "体能让"),  # abbreviated to fit
        ]
        cards = VGroup()
        card_start_x = -4.5
        for i, (icon, label) in enumerate(cards_data):
            card_bg = Rectangle(
                width=1.8, height=0.7,
                fill_color=BG, fill_opacity=1,
                stroke_color=C_MUTED, stroke_width=1
            )
            card_bg.shift(RIGHT * card_start_x + DOWN * (0.0 - i * 0.85) +
                           LEFT * (0.0 if i < 2 else 0.0))
            # Position: 2-column layout
            col = i % 2
            row = i // 2
            card_bg.move_to(LEFT * (1.0 - col * 2.6) + UP * (1.5 - row * 0.85))

            txt = Text(f"{icon} {label}", font_size=10, color=C_TEXT, font=MONO)
            txt.move_to(card_bg.get_center())
            cards.add(card_bg, txt)

        # Cards burst in with staggered growth
        self.play(
            LaggedStart(*[
                Create(card_bg, run_time=0.25, rate_func=rate_functions.ease_out_expo)
                for card_bg in cards[::2]  # backgrounds only
            ], lag_ratio=0.08),
            run_time=0.8
        )
        self.play(
            LaggedStart(*[
                Write(txt, run_time=0.15)
                for txt in cards[1::2]  # text labels
            ], lag_ratio=0.08),
            run_time=0.5
        )

        self.wait(0.3)
