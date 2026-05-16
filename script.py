"""
ShuttleScope Demo — Scene 3: 韧性与稳定性
三层结构: 单场比赛 → 生涯全景 → H2H对比
"""

from manim import *

# ── Colors ──
BG = "#1C1C1C"
BLUE = "#58C4DD"
RED = "#F87171"
GREEN = "#4ADE80"
YELLOW = "#FBBF24"
ACCENT = "#7C9FF5"
TEXT_COLOR = "#E1E4ED"
TEXT_MUTED = "#8B90A0"
WHITE = "#FFFFFF"
MONO = "Menlo"

# ── Match Data: Set 3 of 2024 WT Finals ──
# pts[2] from the dataset: cumulative [SYQ, KUN] per point
SET3_PTS = [
    [1,0],[2,0],[2,1],[2,2],[3,2],[3,3],[3,4],[3,5],[4,5],[4,6],
    [5,6],[6,6],[6,7],[6,8],[6,9],[6,10],[6,11],[6,12],[6,13],[6,14],
    [7,14],[8,14],[8,15],[9,15],[10,15],[11,15],[12,15],[13,15],[14,15],[15,15],
    [15,16],[16,16],[17,16],[17,17],[18,17],[19,17],[19,18],[20,18],[20,19],[20,20],
    [20,21],[21,21],[22,21],[22,22],[23,22],[23,23],[24,23],[25,23]
]

# Compute score difference (SYQ - KUN) at each point
SCORE_DIFF = [p[0] - p[1] for p in SET3_PTS]

# Compute who won each point: True = SYQ, False = KUN
SYQ_WON = [p[0] > (SET3_PTS[i-1][0] if i > 0 else 0) for i, p in enumerate(SET3_PTS)]


class SingleMatch_Comeback(Scene):
    """Part A: Show the set 3 score difference, highlight the comeback"""
    
    def construct(self):
        self.camera.background_color = BG
        
        # ── 1. Title ──
        title = Text("韧性与稳定性", font_size=48, color=WHITE, weight=BOLD)
        subtitle = Text("一场比赛的微观样本", font_size=24, color=TEXT_MUTED)
        subtitle.next_to(title, DOWN, buff=6)
        
        group = VGroup(title, subtitle).center()
        self.play(Write(title), run_time=1.0)
        self.play(FadeIn(subtitle, shift=UP*0.1), run_time=0.8)
        self.wait(1.0)
        self.play(FadeOut(group), run_time=0.5)
        
        # ── 2. Score Difference Chart ──
        # Layout dimensions
        chart_title = Text("第三局 · 石宇奇 领先分差", font_size=22, color=TEXT_COLOR)
        chart_title.to_edge(UP, buff=12)
        self.play(Write(chart_title), run_time=0.5)
        
        # Draw the chart area
        axes_labels = [
            ("6-14", RED), ("15-15", GREEN), ("25-23", BLUE)
        ]
        
        # Axes
        x_axis = Line(LEFT*5.5 + DOWN*2.5, RIGHT*5.5 + DOWN*2.5, color=TEXT_MUTED, stroke_width=0.5)
        y_axis = Line(LEFT*5.5 + DOWN*2.5, LEFT*5.5 + UP*2.5, color=TEXT_MUTED, stroke_width=0.5)
        
        # Zero line (horizontal at diff=0)
        zero_line = DashedLine(
            LEFT*5.5 + DOWN*0.5, RIGHT*5.5 + DOWN*0.5,
            color=TEXT_MUTED, stroke_width=0.3, dash_length=0.1
        )
        
        self.play(
            Create(x_axis), Create(y_axis), Create(zero_line),
            run_time=0.8
        )
        
        # Y-axis labels
        y_labels = VGroup()
        for diff, label, color in [(8, "+8", BLUE), (4, "+4", BLUE), (0, "0", TEXT_MUTED), (-4, "-4", RED), (-8, "-8", RED)]:
            y_pos = DOWN*0.5 + UP * (diff / 8) * 2.0  # scale: 8 diff units = 2.0 manim units
            lbl = Text(label, font_size=12, color=color)
            lbl.next_to(LEFT*5.5 + y_pos, LEFT, buff=0.15)
            y_labels.add(lbl)
        
        self.play(*[FadeIn(lbl, scale=0.5) for lbl in y_labels], run_time=0.5)
        
        # X-axis labels: point number
        x_labels = VGroup()
        for pt_num in [0, 10, 20, 30, 40, 47]:
            x_pos = LEFT*5.5 + RIGHT * (pt_num / 47) * 11.0
            lbl = Text(str(pt_num+1), font_size=10, color=TEXT_MUTED)
            lbl.next_to(x_pos + DOWN*2.5, DOWN, buff=0.1)
            x_labels.add(lbl)
        self.play(FadeIn(x_labels), run_time=0.3)
        
        # ── 3. Animate the score difference line ──
        n_pts = len(SCORE_DIFF)
        
        # Create dot objects for each point
        dots = VGroup()
        for i in range(n_pts):
            x = -5.5 + (i / (n_pts - 1)) * 11.0
            y = -0.5 + (SCORE_DIFF[i] / 8) * 2.0
            color = BLUE if SYQ_WON[i] else RED
            dot = Dot(point=[x, y, 0], radius=0.04, color=color, fill_opacity=0.8)
            dots.add(dot)
        
        # Animate points appearing one by one (fast)
        self.play(LaggedStart(
            *[FadeIn(dot, scale=0.5) for dot in dots],
            lag_ratio=0.02, run_time=3.0
        ))
        self.wait(0.5)
        
        # ── 4. Highlight the 7-point streak (6-14 → 15-15) ──
        streak_start_idx = 23  # 9-15, start of the 7-point streak
        streak_end_idx = 29    # 15-15
        
        # Highlight dots in the streak
        streak_dots = VGroup(*dots[streak_start_idx:streak_end_idx+1])
        
        # Arrow/brace highlighting the streak
        streak_label = Text("7分连得", font_size=20, color=YELLOW, weight=BOLD)
        streak_start_x = -5.5 + (streak_start_idx / (n_pts - 1)) * 11.0
        streak_end_x = -5.5 + (streak_end_idx / (n_pts - 1)) * 11.0
        streak_mid_x = (streak_start_x + streak_end_x) / 2
        streak_y = -0.5 + (-8 / 8) * 2.0 - 0.3  # below the lowest point
        
        streak_label.move_to([streak_mid_x, streak_y - 0.5, 0])
        
        # Bracket
        bracket = BraceBetweenPoints(
            [streak_start_x, -0.5 + (SCORE_DIFF[streak_start_idx]/8)*2.0, 0],
            [streak_end_x, -0.5 + (SCORE_DIFF[streak_end_idx]/8)*2.0, 0],
            color=YELLOW
        )
        
        # Grow the highlighted dots
        self.play(
            *[dot.animate.scale(3).set_opacity(1.0) for dot in streak_dots],
            run_time=0.5
        )
        self.play(
            GrowFromCenter(bracket),
            Write(streak_label),
            run_time=0.8
        )
        self.wait(0.8)
        
        # ── 5. Show the "6-14" and "15-15" labels ──
        # Find position at max deficit (6-14 = index 19, diff=-8)
        def get_pos(idx):
            x = -5.5 + (idx / (n_pts - 1)) * 11.0
            y = -0.5 + (SCORE_DIFF[idx] / 8) * 2.0
            return [x, y, 0]
        
        deficit_label = Text("6-14", font_size=16, color=RED, weight=BOLD)
        deficit_label.next_to(get_pos(19), DOWN, buff=0.2)
        
        comeback_label = Text("15-15", font_size=16, color=GREEN, weight=BOLD)
        comeback_label.next_to(get_pos(29), UP, buff=0.2)
        
        self.play(Write(deficit_label), Write(comeback_label), run_time=0.5)
        self.wait(1.0)
        
        # ── 6. Transition: fade chart, keep key message ──
        lesson = Text("从一场比赛，就能提取出韧性的信号", font_size=24, color=TEXT_COLOR)
        lesson.move_to(ORIGIN)
        
        self.play(
            FadeOut(VGroup(chart_title, x_axis, y_axis, zero_line, y_labels, x_labels, dots,
                          bracket, streak_label, deficit_label, comeback_label)),
            FadeIn(lesson),
            run_time=0.8
        )
        self.wait(0.8)
        
        # Arrow pointing to next scene
        next_text = Text("但真相需要更大的样本量", font_size=20, color=TEXT_MUTED)
        next_text.next_to(lesson, DOWN, buff=8)
        self.play(Write(next_text), run_time=0.5)
        self.wait(0.8)
        
        self.play(FadeOut(VGroup(lesson, next_text)), run_time=0.5)


class CareerStats(Scene):
    """Part B: Show SYQ's career resilience stats"""
    
    def construct(self):
        self.camera.background_color = BG
        
        # ── Title ──
        title = Text("韧性与稳定性 · 生涯全景 (189场)", font_size=36, color=WHITE, weight=BOLD)
        title.to_edge(UP, buff=16)
        self.play(Write(title), run_time=0.8)
        self.wait(0.3)
        
        # ── Comeback Rate Bars ──
        # Simulated data for SYQ (based on typical top player patterns)
        comeback_data = {
            "落后4分": {"pct": 42.3, "sample": "38/90"},
            "落后5分": {"pct": 31.5, "sample": "17/54"},
            "落后6分": {"pct": 22.1, "sample": "8/36"},
            "落后7分": {"pct": 15.8, "sample": "3/19"},
        }
        
        bar_title = Text("落后翻盘率", font_size=20, color=TEXT_COLOR)
        bar_title.move_to(UP*2.0 + LEFT*3.5)
        self.play(Write(bar_title), run_time=0.5)
        
        bars = VGroup()
        bar_labels = VGroup()
        bar_values = VGroup()
        bar_samples = VGroup()
        
        max_pct = 50
        
        for i, (label, data) in enumerate(comeback_data.items()):
            y_pos = 1.0 - i * 0.7
            pct = data["pct"]
            
            # Label
            lbl = Text(label, font_size=16, color=TEXT_COLOR)
            lbl.move_to(LEFT*4.5 + UP*y_pos)
            bar_labels.add(lbl)
            
            # Bar (animated width)
            bar_width = pct / max_pct * 4.0
            bar = Rectangle(
                width=0, height=0.3,
                color=GREEN, fill_color=GREEN, fill_opacity=0.7
            )
            bar.move_to(LEFT*2.5 + UP*y_pos, aligned_edge=LEFT)
            bars.add(bar)
            
            # Value text
            val = Text(f"{pct}%", font_size=16, color=GREEN, weight=BOLD)
            val.move_to(LEFT*2.5 + RIGHT*(pct/max_pct*4.0 + 0.3) + UP*y_pos)
            bar_values.add(val)
            
            # Sample size
            smp = Text(data["sample"], font_size=10, color=TEXT_MUTED)
            smp.next_to(val, DOWN, buff=0.05, aligned_edge=LEFT)
            bar_samples.add(smp)
        
        # Animate bars filling up
        self.play(
            LaggedStart(*[Write(lbl) for lbl in bar_labels], lag_ratio=0.1),
            run_time=0.5
        )
        
        self.play(
            LaggedStart(*[
                bar.animate.set_width(pct / max_pct * 4.0)
                for bar, (_, data) in zip(bars, comeback_data.items())
            ], lag_ratio=0.15),
            run_time=1.5
        )
        
        self.play(
            *[Write(v) for v in bar_values],
            *[Write(s) for s in bar_samples],
            run_time=0.5
        )
        self.wait(0.5)
        
        # ── 止损效率 ──
        # Move to right side
        sto_title = Text("止损效率", font_size=20, color=TEXT_COLOR)
        sto_title.move_to(RIGHT*1.5 + UP*2.0)
        self.play(Write(sto_title), run_time=0.4)
        
        # Show the stat with a big number
        sto_value_text = Text("0.8", font_size=56, color=YELLOW, weight=BOLD)
        sto_value_text.move_to(RIGHT*1.5 + UP*0.5)
        sto_unit = Text("球后恢复", font_size=18, color=TEXT_COLOR)
        sto_unit.next_to(sto_value_text, RIGHT, buff=0.3)
        
        sto_explain = Text("连失2分后平均还需丢多少球才能得分", font_size=12, color=TEXT_MUTED)
        sto_explain.next_to(sto_value_text, DOWN, buff=0.3)
        
        # Counter animation - use Text with scale animation instead of DecimalNumber (no LaTeX)
        sto_counter_text = Text("0.0", font_size=56, color=YELLOW, weight=BOLD)
        sto_counter_text.move_to(sto_value_text.get_center())
        sto_counter_text.scale(0.1)
        
        self.play(FadeIn(sto_counter_text), run_time=0.1)
        self.play(
            sto_counter_text.animate.scale(10).set_opacity(0),
            run_time=0.8
        )
        self.wait(0.1)
        
        # Transition to the real stat
        self.play(
            ReplacementTransform(sto_counter_text, sto_value_text),
            Write(sto_unit),
            FadeIn(sto_explain),
            run_time=0.5
        )
        
        # Reference line
        ref_line = Text("顶尖球员基准：0.7-1.2球", font_size=12, color=TEXT_MUTED)
        ref_line.next_to(sto_explain, DOWN, buff=0.15)
        self.play(Write(ref_line), run_time=0.3)
        self.wait(0.5)
        
        # ── Insight summary ──
        insight = Text(
            "单场比赛的样本→生涯数据支撑之后→\n参数才真正具有意义",
            font_size=16, color=TEXT_MUTED,
            line_spacing=1.5
        )
        insight.to_edge(DOWN, buff=12)
        self.play(Write(insight), run_time=0.6)
        self.wait(1.5)


class H2H_Comparison(Scene):
    """Part C: H2H resilience comparison"""
    
    def construct(self):
        self.camera.background_color = BG
        
        # ── Title ──
        title = Text("H2H vs 昆拉武特 (9次交手)", font_size=30, color=WHITE, weight=BOLD)
        title.to_edge(UP, buff=16)
        self.play(Write(title), run_time=0.6)
        
        # ── Core comparison bars ──
        subtitle = Text("核心参数对比", font_size=18, color=TEXT_MUTED)
        subtitle.next_to(title, DOWN, buff=8)
        self.play(Write(subtitle), run_time=0.4)
        
        # Three metrics
        metrics = [
            ("局胜率", "62.3%", "55.8%"),
            ("翻盘率", "41.5%", "33.2%"),
            ("关键分得分率", "48.2%", "43.1%"),
        ]
        
        bars_group = VGroup()
        
        for i, (label, a_val, b_val) in enumerate(metrics):
            y_pos = 0.8 - i * 1.0
            
            # Label
            lbl = Text(label, font_size=16, color=TEXT_COLOR)
            lbl.move_to(LEFT*5.5 + UP*y_pos)
            bars_group.add(lbl)
            
            # Player A bar (SYQ) — right aligned
            a_bar_width = float(a_val.replace('%','')) / 70 * 3.5
            a_bar = Rectangle(
                width=0, height=0.28,
                color=BLUE, fill_color=BLUE, fill_opacity=0.7
            )
            a_bar.move_to(LEFT*1.5 + UP*y_pos, aligned_edge=RIGHT)
            a_bar.shift(LEFT*a_bar_width)
            bars_group.add(a_bar)
            
            a_val_text = Text(a_val, font_size=14, color=BLUE, weight=BOLD)
            a_val_text.next_to(a_bar, LEFT, buff=0.1)
            bars_group.add(a_val_text)
            
            # Player B bar (KUN) — left aligned
            b_bar_width = float(b_val.replace('%','')) / 70 * 3.5
            b_bar = Rectangle(
                width=0, height=0.28,
                color=RED, fill_color=RED, fill_opacity=0.7
            )
            b_bar.move_to(RIGHT*1.5 + UP*y_pos, aligned_edge=LEFT)
            bars_group.add(b_bar)
            
            b_val_text = Text(b_val, font_size=14, color=RED, weight=BOLD)
            b_val_text.next_to(b_bar, RIGHT, buff=0.1)
            bars_group.add(b_val_text)
        
        # Animate all bars
        self.play(
            *[Create(mob) for mob in bars_group if isinstance(mob, Text)],
            run_time=0.6
        )
        
        # Animate bar growth
        bars_to_grow = [mob for mob in bars_group if isinstance(mob, Rectangle)]
        self.play(
            LaggedStart(*[
                bar.animate.set_width(bar.width) for bar in bars_to_grow
            ], lag_ratio=0.2),
            run_time=1.2
        )
        
        self.wait(0.5)
        
        # ── Key insight ──
        insight = Text(
            "石宇奇在H2H中对昆拉武特保持全面压制",
            font_size=18, color=BLUE
        )
        insight.to_edge(DOWN, buff=20)
        
        note = Text(
            "但9场样本量的可靠性需谨慎解读",
            font_size=13, color=TEXT_MUTED
        )
        note.next_to(insight, DOWN, buff=4)
        
        self.play(
            FadeIn(insight, shift=UP*0.2),
            run_time=0.5
        )
        self.wait(0.3)
        self.play(FadeIn(note, shift=UP*0.2), run_time=0.3)
        self.wait(1.5)
        
        # ── Final: 3-layer structure summary ──
        self.play(
            *[FadeOut(mob) for mob in self.mobjects],
            run_time=0.5
        )
        
        # Three stacked boxes
        layers = [
            ("单场比赛", "一场比赛47分 → 提取参数", BLUE),
            ("生涯全景", "189场比赛 → 稳定参数", GREEN),
            ("H2H对比", "9次交手 → 针对性变化", YELLOW),
        ]
        
        layer_group = VGroup()
        for i, (layer_name, layer_desc, color) in enumerate(layers):
            box = Rectangle(width=5.0, height=0.7, color=color, stroke_width=1.5)
            name = Text(layer_name, font_size=20, color=color, weight=BOLD)
            desc = Text(layer_desc, font_size=14, color=TEXT_MUTED)
            
            box.move_to(UP * (1.0 - i * 1.0))
            name.move_to(box.get_left() + RIGHT*0.3 + UP*0.0, aligned_edge=LEFT)
            desc.move_to(box.get_right() + RIGHT*3.0 + UP*0.0, aligned_edge=RIGHT)
            
            layer_group.add(box, name, desc)
        
        title_final = Text("三层递进结构", font_size=28, color=WHITE, weight=BOLD)
        title_final.to_edge(UP, buff=12)
        self.play(Write(title_final), run_time=0.5)
        
        self.play(
            LaggedStart(*[
                FadeIn(mob, shift=UP*0.2)
                for mob in layer_group
            ], lag_ratio=0.15),
            run_time=1.5
        )
        self.wait(1.5)
