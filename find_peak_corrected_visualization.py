from manimlib import *

from pathlib import Path
import sys

PROJECT_DIR = Path(__file__).resolve().parent
if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))
from visualization_settings import NUMS, validate_settings


validate_settings()


# Correct O(log n) binary search: the slope between k and k + 1 determines
# which half is guaranteed to contain a peak.
CPP_SOURCE = """class Solution {
public:
    int findPeakElement(vector<int>& nums) {
        int i = 0;
        int j = nums.size() - 1;

        while (i < j) {
            int k = i + (j - i) / 2;

            if (nums[k] > nums[k + 1]) {
                j = k;
            } else {
                i = k + 1;
            }
        }

        return i;
    }
};"""


class FindPeakElementCorrectedTrace(Scene):
    """A native-display trace of the corrected binary-search solution."""

    BG = "#07111F"
    SURFACE = "#0E1B2B"
    SURFACE_2 = "#12243A"
    BORDER = "#28415C"
    GRID = "#18304A"
    TEXT = "#EEF5FF"
    MUTED = "#8DA6BE"
    CYAN = "#4DDCF0"
    BLUE = "#5B8CFF"
    GOLD = "#FFC857"
    PINK = "#FF6B9D"
    GREEN = "#6FE7A2"
    RED = "#FF6B6B"
    PURPLE = "#A98BFF"

    nums = list(NUMS)

    def construct(self):
        self.camera.background_color = self.BG
        self.frame_w = FRAME_WIDTH
        self.frame_h = FRAME_HEIGHT

        self._build_background()
        self._build_header()
        self._build_panels()
        self._build_code()
        self._build_array()

        self.play(
            FadeIn(self.header, shift=0.16 * DOWN),
            FadeIn(self.code_panel, shift=0.18 * RIGHT),
            FadeIn(self.trace_panel, shift=0.18 * LEFT),
            run_time=1.0,
        )
        self.play(
            LaggedStart(*[FadeIn(line, shift=0.05 * RIGHT) for line in self.code_lines], lag_ratio=0.025),
            LaggedStart(*[FadeIn(item, shift=0.12 * UP) for item in self.array_items], lag_ratio=0.035),
            FadeIn(self.graph_lines),
            FadeIn(self.array_heading),
            run_time=1.6,
        )
        self.add(self.dim_overlays)

        # Initialization: the closed interval [i, j] always contains a peak.
        right_boundary = len(self.nums) - 1
        self._move_highlight(3, color=self.CYAN, run_time=0.45)
        self._set_status("SETUP", [("i", "0", self.CYAN)], "left boundary", run_time=0.5)
        self._move_highlight(4, color=self.CYAN, run_time=0.4)
        self._set_status(
            "SETUP",
            [("i", "0", self.CYAN), ("j", str(right_boundary), self.PINK)],
            "[i, j] contains a peak",
            run_time=0.6,
        )
        widths = [len(self.nums)]
        self._set_interval(0, right_boundary, widths, run_time=0.7, initial=True)
        self.wait(0.35)

        i = 0
        j = right_boundary
        iteration = 1
        while i < j:
            k = i + (j - i) // 2
            if self.nums[k] > self.nums[k + 1]:
                next_i, next_j = i, k
                decision = f"falling slope   →   j = k = {k}"
                decision_color = self.PINK
                source_line = 10
            else:
                next_i, next_j = k + 1, j
                decision = f"rising slope   →   i = k + 1 = {k + 1}"
                decision_color = self.CYAN
                source_line = 12

            widths.append(next_j - next_i + 1)
            self._iteration(
                number=iteration,
                i=i,
                j=j,
                k=k,
                decision=decision,
                decision_color=decision_color,
                source_line=source_line,
                next_interval=(next_i, next_j),
                widths=list(widths),
            )
            i, j = next_i, next_j
            iteration += 1

        self.search_widths = widths
        self._finish_peak(i)

    # ------------------------------------------------------------------
    # Static composition
    # ------------------------------------------------------------------
    def _build_background(self):
        grid = VGroup()
        for x in np.arange(-self.frame_w / 2, self.frame_w / 2 + 0.01, 0.55):
            grid.add(Line([x, -self.frame_h / 2, 0], [x, self.frame_h / 2, 0]))
        for y in np.arange(-self.frame_h / 2, self.frame_h / 2 + 0.01, 0.55):
            grid.add(Line([-self.frame_w / 2, y, 0], [self.frame_w / 2, y, 0]))
        grid.set_stroke(self.GRID, width=1, opacity=0.19)
        glow = Circle(radius=2.9).set_fill(self.BLUE, opacity=0.035).set_stroke(width=0)
        glow.shift(3.8 * RIGHT + 1.5 * UP)
        self.add(grid, glow)

    def _build_header(self):
        icon_bars = VGroup(
            RoundedRectangle(width=0.10, height=h, corner_radius=0.035)
            .set_fill(color, opacity=1)
            .set_stroke(width=0)
            for h, color in [(0.20, self.CYAN), (0.38, self.BLUE), (0.60, self.GOLD), (0.32, self.PINK)]
        ).arrange(RIGHT, buff=0.055, aligned_edge=DOWN)

        title = Text("Find Peak Element", font="Avenir Next", font_size=34, weight=BOLD, color=self.TEXT)
        subtitle = Text("corrected binary-search trace", font="Avenir Next", font_size=16, color=self.MUTED)
        title_group = VGroup(title, subtitle).arrange(DOWN, buff=0.01, aligned_edge=LEFT)
        icon_bars.next_to(title_group, LEFT, buff=0.22).align_to(title_group, DOWN).shift(0.04 * UP)

        badge_text = Text("O(log n)", font="Avenir Next", font_size=18, weight=BOLD, color=self.GREEN)
        badge = RoundedRectangle(width=1.33, height=0.46, corner_radius=0.23)
        badge.set_fill(self.GREEN, opacity=0.09).set_stroke(self.GREEN, width=1.5, opacity=0.8)
        badge_text.move_to(badge)
        badge_group = VGroup(badge, badge_text)

        title_block = VGroup(icon_bars, title_group)
        title_block.move_to([-self.frame_w / 2 + 0.4, 3.46, 0], aligned_edge=LEFT)
        badge_group.move_to([self.frame_w / 2 - 0.42, 3.46, 0], aligned_edge=RIGHT)
        self.header = VGroup(title_block, badge_group)

    def _build_panels(self):
        margin = 0.36
        gap = 0.26
        self.code_w = self.frame_w * 0.43
        self.trace_w = self.frame_w - 2 * margin - gap - self.code_w
        self.panel_h = 6.28
        panel_y = -0.42
        self.code_x = -self.frame_w / 2 + margin + self.code_w / 2
        self.trace_x = self.code_x + self.code_w / 2 + gap + self.trace_w / 2

        self.code_panel = self._panel(self.code_w, self.panel_h).move_to([self.code_x, panel_y, 0])
        self.trace_panel = self._panel(self.trace_w, self.panel_h).move_to([self.trace_x, panel_y, 0])

        # Editor chrome.
        dots = VGroup(*[
            Circle(radius=0.055).set_fill(c, opacity=0.9).set_stroke(width=0)
            for c in (self.RED, self.GOLD, self.GREEN)
        ]).arrange(RIGHT, buff=0.08)
        dots.move_to(self.code_panel.get_corner(UL) + np.array([0.28, -0.25, 0]))
        file_name = Text("findPeakElement_corrected.cpp", font="Avenir Next", font_size=13, color=self.MUTED)
        file_name.next_to(dots, RIGHT, buff=0.16)
        divider = Line(
            self.code_panel.get_left() + np.array([0.18, self.panel_h / 2 - 0.46, 0]),
            self.code_panel.get_right() + np.array([-0.18, self.panel_h / 2 - 0.46, 0]),
        ).set_stroke(self.BORDER, width=1.1, opacity=0.8)
        self.code_panel.add(dots, file_name, divider)

    def _panel(self, width, height):
        panel = RoundedRectangle(width=width, height=height, corner_radius=0.20)
        panel.set_fill(self.SURFACE, opacity=0.96)
        panel.set_stroke(self.BORDER, width=1.4, opacity=0.9)
        return panel

    def _build_code(self):
        raw_lines = CPP_SOURCE.splitlines()
        rendered_lines = VGroup()
        indentation = []
        for raw in raw_lines:
            content = raw.lstrip(" ")
            indentation.append(len(raw) - len(content))
            shown = content.replace(" ", "\u00a0") if content else "\u00a0"
            mob = Text(shown, font="Menlo", font_size=15, color=self.TEXT)
            self._color_code_line(mob)
            rendered_lines.add(mob)
        rendered_lines.arrange(DOWN, buff=0.047, aligned_edge=LEFT)

        # Pango does not include leading spaces in a Text mobject's visible
        # bounds, so aligning the lines directly would flatten the indentation.
        # Offset each line by an explicit monospace character width instead.
        indent_probe = Text("0000", font="Menlo", font_size=15)
        space_width = indent_probe.get_width() / 4
        for line, spaces in zip(rendered_lines, indentation):
            line.shift(spaces * space_width * RIGHT)

        max_w = self.code_w - 0.64
        if rendered_lines.get_width() > max_w:
            rendered_lines.set_width(max_w)
        rendered_lines.move_to([self.code_x, -0.62, 0])
        rendered_lines.shift((self.code_panel.get_left()[0] + 0.42 - rendered_lines.get_left()[0]) * RIGHT)

        line_numbers = VGroup()
        for number, line in enumerate(rendered_lines, start=1):
            number_mob = Text(str(number), font="Menlo", font_size=10, color=self.MUTED)
            number_mob.set_opacity(0.48)
            number_mob.move_to([self.code_panel.get_left()[0] + 0.21, line.get_y(), 0])
            line_numbers.add(number_mob)

        self.code_lines = rendered_lines
        self.line_numbers = line_numbers
        self.code_panel.add(line_numbers)
        self.active_highlight = self._highlight_box(3, 3, self.CYAN).set_opacity(0)
        self.code_panel.add(self.active_highlight)
        self.add(self.code_panel)

    def _color_code_line(self, line):
        for word in ("class", "public", "while", "if", "else"):
            line.set_color_by_text(word, self.PURPLE)
        for word in ("int", "vector"):
            line.set_color_by_text(word, self.CYAN)
        line.set_color_by_text("return", self.PINK)
        for number in ("0", "1", "2"):
            line.set_color_by_text(number, self.GOLD)

    def _build_array(self):
        array_title = Text("nums", font="Avenir Next", font_size=19, weight=BOLD, color=self.TEXT)
        array_meta = Text(f"{len(self.nums)} values", font="Avenir Next", font_size=13, color=self.MUTED)
        self.iteration_label = Text("SETUP", font="Avenir Next", font_size=12, weight=BOLD, color=self.PURPLE)
        iteration_box = RoundedRectangle(width=1.06, height=0.32, corner_radius=0.16)
        iteration_box.set_fill(self.PURPLE, opacity=0.12).set_stroke(self.PURPLE, width=1, opacity=0.7)
        self.iteration_label.move_to(iteration_box)
        self.iteration_badge = VGroup(iteration_box, self.iteration_label)

        array_title.move_to([self.trace_panel.get_left()[0] + 0.26, 2.39, 0], aligned_edge=LEFT)
        array_meta.next_to(array_title, RIGHT, buff=0.15).shift(0.01 * DOWN)
        self.iteration_badge.move_to([self.trace_panel.get_right()[0] - 0.26, 2.39, 0], aligned_edge=RIGHT)
        self.array_heading = VGroup(array_title, array_meta, self.iteration_badge)

        usable_w = self.trace_w - 0.55
        step = usable_w / len(self.nums)
        self.cell_w = step * 0.81
        x0 = self.trace_x - usable_w / 2 + step / 2
        bar_base = 0.77
        min_value = min(self.nums)
        max_value = max(self.nums)
        value_span = max(1, max_value - min_value)
        self.array_items = VGroup()
        self.dim_overlays = VGroup()
        self.bars = []
        self.dots = []
        self.cells = []
        self.values = []
        self.indices = []
        self.x_positions = []

        for index, value in enumerate(self.nums):
            x = x0 + index * step
            self.x_positions.append(x)
            bar_h = 0.15 + 1.12 * (value - min_value) / value_span
            bar = RoundedRectangle(width=self.cell_w * 0.56, height=bar_h, corner_radius=0.055)
            bar.set_fill(self.BLUE, opacity=0.55).set_stroke(self.CYAN, width=1.1, opacity=0.65)
            bar.move_to([x, bar_base + bar_h / 2, 0])
            dot = Dot([x, bar_base + bar_h, 0], radius=0.045, color=self.CYAN)
            cell = RoundedRectangle(width=self.cell_w, height=0.47, corner_radius=0.07)
            cell.set_fill(self.SURFACE_2, opacity=1).set_stroke(self.BORDER, width=1.1)
            cell.move_to([x, 0.34, 0])
            value_text = Text(str(value), font="Avenir Next", font_size=16, weight=BOLD, color=self.TEXT)
            value_text.move_to(cell)
            index_text = Text(str(index), font="Menlo", font_size=10, color=self.MUTED)
            index_text.move_to([x, -0.05, 0])
            item = VGroup(bar, dot, cell, value_text, index_text)
            self.array_items.add(item)
            overlay = Rectangle(width=step * 0.96, height=2.42)
            overlay.set_fill(self.SURFACE, opacity=0).set_stroke(width=0)
            overlay.move_to([x, 1.02, 0])
            self.dim_overlays.add(overlay)
            self.bars.append(bar)
            self.dots.append(dot)
            self.cells.append(cell)
            self.values.append(value_text)
            self.indices.append(index_text)

        self.graph_lines = VGroup(*[
            Line(self.dots[index].get_center(), self.dots[index + 1].get_center())
            .set_stroke(self.CYAN, width=2.2, opacity=0.55)
            for index in range(len(self.dots) - 1)
        ])
        self.trace_panel.add(self.graph_lines)
        self.add(self.trace_panel)

        # Dynamic lower-half placeholders.
        self.status_group = VGroup()
        self.comparison_group = VGroup()
        self.decision_group = VGroup()
        self.interval_group = VGroup()
        self.k_marker = VGroup()

    # ------------------------------------------------------------------
    # Dynamic trace
    # ------------------------------------------------------------------
    def _iteration(
        self,
        number,
        i,
        j,
        k,
        decision,
        decision_color,
        source_line,
        next_interval,
        widths,
    ):
        if number > 1:
            self.remove(self.k_marker, self.comparison_group, self.decision_group, self.status_group)
            self.k_marker = VGroup()
            self.comparison_group = VGroup()
            self.decision_group = VGroup()
            self.status_group = VGroup()
            self.wait(0.20)
        self._move_highlight(6, color=self.GOLD, run_time=0.35)
        self._move_highlight(7, color=self.GOLD, run_time=0.45)
        self._set_iteration_badge(f"STEP {number}", self.GOLD)
        self._set_status(
            f"ITERATION {number}",
            [("i", str(i), self.CYAN), ("k", str(k), self.GOLD), ("j", str(j), self.PINK)],
            f"k = {i} + ({j} - {i}) / 2 = {k}",
            run_time=0.65,
        )
        self._set_k_marker(k)

        self._move_highlight(9, color=self.BLUE, run_time=0.5)
        self._show_comparison(k, k + 1, run_time=0.75)
        self._move_highlight(source_line, color=decision_color, run_time=0.45)
        self._show_decision(decision, decision_color, run_time=0.65)

        if next_interval is not None:
            self._set_interval(next_interval[0], next_interval[1], widths, run_time=0.95)
        else:
            self.wait(0.45)

    def _move_highlight(self, start, end=None, color=None, run_time=0.45):
        if end is None:
            end = start
        color = color or self.CYAN
        target = self._highlight_box(start, end, color)
        if self.active_highlight.get_opacity() == 0:
            self.active_highlight.become(target)
            self.play(FadeIn(self.active_highlight), run_time=run_time)
        else:
            self.play(Transform(self.active_highlight, target), run_time=run_time)

    def _highlight_box(self, start, end, color):
        top_line = self.code_lines[start]
        bottom_line = self.code_lines[end]
        top = top_line.get_top()[1] + 0.035
        bottom = bottom_line.get_bottom()[1] - 0.035
        box = RoundedRectangle(
            width=self.code_w - 0.28,
            height=max(0.18, top - bottom),
            corner_radius=0.055,
        )
        box.set_fill(color, opacity=0.12).set_stroke(color, width=1.05, opacity=0.65)
        box.move_to([self.code_x, (top + bottom) / 2, 0])
        return box

    def _set_iteration_badge(self, text, color):
        label = Text(text, font="Avenir Next", font_size=12, weight=BOLD, color=color)
        box = RoundedRectangle(width=1.06, height=0.32, corner_radius=0.16)
        box.set_fill(color, opacity=0.12).set_stroke(color, width=1, opacity=0.7)
        label.move_to(box)
        new_badge = VGroup(box, label).move_to(self.iteration_badge)
        self.iteration_badge.become(new_badge)
        self.wait(0.20)

    def _make_status(self, eyebrow, entries, detail):
        eyebrow_text = Text(eyebrow, font="Avenir Next", font_size=11, weight=BOLD, color=self.MUTED)
        eyebrow_text.set_opacity(0.78)
        chips = VGroup()
        for key, value, color in entries:
            chip_text = Text(f"{key} = {value}", font="Menlo", font_size=15, weight=BOLD, color=color)
            chip_box = RoundedRectangle(width=1.17, height=0.45, corner_radius=0.10)
            chip_box.set_fill(color, opacity=0.09).set_stroke(color, width=1.0, opacity=0.64)
            chip_text.move_to(chip_box)
            chips.add(VGroup(chip_box, chip_text))
        chips.arrange(RIGHT, buff=0.16)
        detail_text = Text(detail, font="Menlo", font_size=12, color=self.MUTED)
        body = VGroup(eyebrow_text, chips, detail_text).arrange(DOWN, buff=0.08)
        body.move_to([self.trace_x, -0.72, 0])
        return body

    def _set_status(self, eyebrow, entries, detail, run_time=0.55):
        new_group = self._make_status(eyebrow, entries, detail)
        if len(self.status_group) == 0:
            self.status_group.become(new_group)
            self.add(self.status_group)
        else:
            self.status_group.become(new_group)
        self.wait(run_time)

    def _set_k_marker(self, k):
        ring = Circle(radius=0.12).set_stroke(self.GOLD, width=2.4).set_fill(self.GOLD, opacity=0.06)
        ring.move_to(self.dots[k])
        pointer = Triangle().scale(0.065).rotate(PI)
        pointer.set_fill(self.GOLD, opacity=1).set_stroke(width=0)
        pointer.next_to(ring, UP, buff=0.035)
        label = Text(f"k={k}", font="Menlo", font_size=11, weight=BOLD, color=self.GOLD)
        label.next_to(pointer, UP, buff=0.025)
        new_marker = VGroup(ring, pointer, label)
        if len(self.k_marker) == 0:
            self.k_marker.become(new_marker)
            self.add(self.k_marker)
        else:
            self.k_marker.become(new_marker)
        self.play(FlashAround(self.k_marker[0], color=self.GOLD), run_time=0.65)

    def _make_value_box(self, role, index, color):
        label = Text(f"{role} · nums[{index}]", font="Avenir Next", font_size=11, color=self.MUTED)
        value = Text(str(self.nums[index]), font="Avenir Next", font_size=22, weight=BOLD, color=color)
        content = VGroup(label, value).arrange(DOWN, buff=0.025)
        box = RoundedRectangle(width=1.48, height=0.76, corner_radius=0.11)
        box.set_fill(color, opacity=0.07).set_stroke(color, width=1.0, opacity=0.54)
        content.move_to(box)
        return VGroup(box, content)

    def _show_comparison(self, center_index, right_index, run_time=0.7):
        boxes = VGroup(
            self._make_value_box("mid", center_index, self.GOLD),
            self._make_value_box("next", right_index, self.PINK),
        ).arrange(RIGHT, buff=0.28)
        boxes.move_to([self.trace_x, -1.78, 0])
        if len(self.comparison_group) == 0:
            self.comparison_group.become(boxes)
            self.add(self.comparison_group)
        else:
            self.comparison_group.become(boxes)
        self.play(
            *[FlashAround(self.cells[idx], color=color) for idx, color in [
                (center_index, self.GOLD), (right_index, self.PINK)
            ]],
            run_time=run_time,
        )

    def _show_decision(self, text, color, run_time=0.55):
        statement = Text(text, font="Menlo", font_size=14, weight=BOLD, color=color)
        statement.move_to([self.trace_x, -2.42, 0])
        underline = Line(statement.get_left(), statement.get_right()).set_stroke(color, width=1.5, opacity=0.65)
        underline.next_to(statement, DOWN, buff=0.055)
        new_group = VGroup(statement, underline)
        if len(self.decision_group) == 0:
            self.decision_group.become(new_group)
            self.add(self.decision_group)
        else:
            self.decision_group.become(new_group)
        self.wait(run_time)

    def _make_interval(self, i, j, widths):
        y = -2.93
        left = self.x_positions[i] - self.cell_w / 2
        right = self.x_positions[j] + self.cell_w / 2
        bracket = VGroup(
            Line([left, y, 0], [right, y, 0]),
            Line([left, y - 0.08, 0], [left, y + 0.08, 0]),
            Line([right, y - 0.08, 0], [right, y + 0.08, 0]),
        ).set_stroke(self.CYAN, width=2.0, opacity=0.88)
        width_string = "  →  ".join(str(value) for value in widths)
        caption = Text(f"active widths   {width_string}", font="Menlo", font_size=11, color=self.MUTED)
        caption.next_to(bracket, DOWN, buff=0.12)
        caption.set_x(self.trace_x)
        return VGroup(bracket, caption)

    def _set_interval(self, i, j, widths, run_time=0.85, initial=False):
        new_group = self._make_interval(i, j, widths)
        dim_anims = []
        for index, overlay in enumerate(self.dim_overlays):
            target_opacity = 0.0 if i <= index <= j else 0.78
            dim_anims.append(overlay.animate.set_fill(self.SURFACE, opacity=target_opacity))
        for index, line in enumerate(self.graph_lines):
            target_opacity = 0.55 if i <= index and index + 1 <= j else 0.10
            dim_anims.append(line.animate.set_opacity(target_opacity))

        if initial or len(self.interval_group) == 0:
            self.interval_group.become(new_group)
            self.add(self.interval_group)
        else:
            self.interval_group.become(new_group)
        self.play(*dim_anims, run_time=run_time)

    def _finish_peak(self, peak_index):
        self._move_highlight(6, color=self.GREEN, run_time=0.35)
        self._show_decision("i == j   →   search converged", self.GREEN, run_time=0.5)
        self._move_highlight(16, color=self.GREEN, run_time=0.45)
        self._show_decision(f"return {peak_index}", self.GREEN, run_time=0.55)

        # Fade secondary trace information and make the returned element dominant.
        peak_bar = self.bars[peak_index]
        peak_dot = self.dots[peak_index]
        peak_cell = self.cells[peak_index]
        halo = Circle(radius=0.31).set_fill(self.GREEN, opacity=0.10).set_stroke(self.GREEN, width=2.2, opacity=0.8)
        halo.move_to(peak_dot)
        result = Text(
            f"peak index = {peak_index}    value = {self.nums[peak_index]}",
            font="Avenir Next",
            font_size=22,
            weight=BOLD,
            color=self.GREEN,
        )
        result.move_to([self.trace_x, -2.42, 0])
        width_trace = "  →  ".join(str(width) for width in self.search_widths)
        complexity = Text(f"{width_trace}     O(log n)", font="Menlo", font_size=13, color=self.TEXT)
        complexity.move_to([self.trace_x, -3.15, 0])

        self.remove(self.comparison_group)
        self.decision_group.become(result)
        self.interval_group.become(complexity)
        self.play(
            peak_bar.animate.set_fill(self.GREEN, opacity=0.80).set_stroke(self.GREEN, width=2.0, opacity=1),
            peak_cell.animate.set_fill(self.GREEN, opacity=0.15).set_stroke(self.GREEN, width=2.0, opacity=1),
            peak_dot.animate.scale(1.55).set_color(self.GREEN),
            FadeIn(halo, scale=0.7),
            run_time=1.05,
        )
        self.play(
            halo.animate.scale(1.16).set_stroke(self.GREEN, width=3.4, opacity=1),
            self.active_highlight.animate.set_fill(self.GREEN, opacity=0.18),
            run_time=0.4,
        )
        self.play(
            halo.animate.scale(1 / 1.16).set_stroke(self.GREEN, width=2.2, opacity=0.8),
            run_time=0.4,
        )
        self.wait(2.0)
