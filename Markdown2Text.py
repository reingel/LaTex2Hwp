import os
from Latex2HwpEq import Latex2HwpEq
import re


class Markdown2Text:
    def __init__(self):
        self.latex_converter = Latex2HwpEq()

    def convert(self, markdown_str):
        def replace_math(match):
            latex_content = match.group(1).strip()
            converted = self.latex_converter.convert(latex_content)
            return f"{converted}"

        # $$...$$ 변환
        block_math_pattern = r'\$\$([\s\S]*?)\$\$'
        result = re.sub(block_math_pattern, replace_math, markdown_str)
        block_math_pattern = '$' + block_math_pattern + '$'

        # $...$ 변환 (단일 $로 둘러싸인 경우, \$는 제외)
        inline_math_pattern = r'(?<!\\)\$([^\$]+?)(?<!\\)\$'
        result = re.sub(inline_math_pattern, replace_math, result)
        inline_math_pattern = '$$' + inline_math_pattern + '$$'

        return result

if __name__ == "__main__":
    test_cases = [
        r"This is inline math: $\frac{a}{b}$ and text.",
        r"Block math: $$\frac{a}{\frac{b}{\frac{c}{d}}}$$",
        r"Mixed: $a + b$ and $$\sqrt{x}$$ and $\begin{bmatrix}a&b\\c&d\end{bmatrix}$.",
        r"Array: $$\begin{array}{ccc:cc}a&b&c&d&e\\\hdashline f&g&h&i&j\end{array}$$",
        r"No alignment: $$\begin{array}a&b\\c&d\end{array}$$",
        r"Complex: Let $x = \frac{1}{\sqrt{2}}$ and $$y = \begin{pmatrix}\frac{a}{b}&c\\d&\sqrt{e}\end{pmatrix}$$."
    ]

    for test in test_cases:
        converter = Markdown2Text()
        result = converter.convert(test)
        print(f"Input: {test}")
        print(f"Output: {result}\n")
