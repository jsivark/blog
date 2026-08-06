"""One BPE merge — small pedagogical Manim scene for the blog."""

from manim import *


INK = "#1c1917"
MUTED = "#57534e"
PAPER = "#faf7f2"
ACCENT = "#c2410c"
TEAL = "#0f4c5c"
TOKEN_FILL = "#efeae2"
MERGE_FILL = "#d8eee8"


class BPEMerge(Scene):
    """Show count → highlight → merge for a case with no overlapping ambiguity."""

    def construct(self):
        self.camera.background_color = PAPER

        # "aabaa": ("a","a") appears twice, non-overlapping — count matches merges.
        chars = list("aabaa")

        title = Text("One BPE merge", font_size=36, color=INK, weight=BOLD)
        title.to_edge(UP, buff=0.4)
        subtitle = Text(
            'start from characters:  "a a b a a"',
            font_size=22,
            color=MUTED,
        )
        subtitle.next_to(title, DOWN, buff=0.22)

        self.play(FadeIn(title), FadeIn(subtitle))

        before_label = Text("before", font_size=20, color=MUTED)
        tokens = self._token_row(chars, y=0.85)
        before_label.next_to(tokens, LEFT, buff=0.35)

        self.play(FadeIn(before_label), LaggedStart(*[FadeIn(t, shift=UP * 0.1) for t in tokens], lag_ratio=0.07))
        self.wait(0.35)

        # Step 1 — count adjacent pairs
        step1 = Text("1. count adjacent pairs", font_size=24, color=TEAL)
        step1.next_to(tokens, DOWN, buff=0.55)
        counts = Text('("a","a") × 2   ·   ("a","b") × 1   ·   ("b","a") × 1', font_size=22, color=INK)
        counts.next_to(step1, DOWN, buff=0.22)
        winner = Text('winner → merge ("a","a")', font_size=24, color=ACCENT)
        winner.next_to(counts, DOWN, buff=0.22)

        self.play(Write(step1))
        self.play(FadeIn(counts))
        self.play(FadeIn(winner))
        self.wait(0.4)

        # Highlight only the pairs that the left-to-right merge will consume
        merge_spans = [(0, 1), (3, 4)]
        highlights = VGroup()
        for i, j in merge_spans:
            box = SurroundingRectangle(
                VGroup(tokens[i], tokens[j]),
                color=ACCENT,
                buff=0.07,
                corner_radius=0.05,
                stroke_width=3,
            )
            highlights.add(box)
        self.play(LaggedStart(*[Create(h) for h in highlights], lag_ratio=0.2))
        self.wait(0.55)

        # Step 2 — show result under the explanation
        merged = self._apply_merge(chars, ("a", "a"), "aa")  # ["aa", "b", "aa"]
        step2 = Text("2. replace each winning pair with one new token", font_size=24, color=TEAL)
        step2.next_to(winner, DOWN, buff=0.4)

        after_tokens = self._token_row(merged, y=0.0, merged_label="aa")
        after_label = Text("after", font_size=20, color=MUTED)

        self.play(FadeOut(highlights), FadeIn(step2))
        after_tokens.next_to(step2, DOWN, buff=0.45)
        after_label.next_to(after_tokens, LEFT, buff=0.35)
        self.play(FadeIn(after_label), FadeIn(after_tokens))

        length = Text(
            f"sequence length  {len(chars)}  →  {len(merged)}",
            font_size=26,
            color=INK,
        )
        length.next_to(after_tokens, DOWN, buff=0.35)
        note = Text("then repeat on the new sequence", font_size=22, color=MUTED)
        note.next_to(length, DOWN, buff=0.25)
        self.play(FadeIn(length), FadeIn(note))
        self.wait(1.8)

    def _token_row(self, labels, y=0.0, merged_label=None):
        row = VGroup()
        for lab in labels:
            is_merged = merged_label is not None and lab == merged_label
            fill = MERGE_FILL if is_merged else TOKEN_FILL
            stroke = TEAL if is_merged else MUTED
            txt = Text(lab, font_size=28 if len(lab) == 1 else 24, color=INK)
            box = RoundedRectangle(
                width=max(0.72, 0.4 * len(lab) + 0.5),
                height=0.72,
                corner_radius=0.08,
                fill_color=fill,
                fill_opacity=1,
                stroke_color=stroke,
                stroke_width=2,
            )
            g = VGroup(box, txt)
            txt.move_to(box.get_center())
            row.add(g)
        row.arrange(RIGHT, buff=0.16)
        row.move_to(UP * y)
        return row

    @staticmethod
    def _apply_merge(chars, pair, new_tok):
        out = []
        i = 0
        while i < len(chars):
            if i < len(chars) - 1 and (chars[i], chars[i + 1]) == pair:
                out.append(new_tok)
                i += 2
            else:
                out.append(chars[i])
                i += 1
        return out
