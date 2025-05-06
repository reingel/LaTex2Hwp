import re


class Latex2HwpEq:
    def __init__(self):
        pass

    def convert(self, latex_str):
        def replace_dot_bold(match):
            modifier = match.group(1).strip()
            var = match.group(2).strip()
            subscript = match.group(3).strip() if match.group(3) else ""
            superscript = match.group(4).strip() if match.group(4) else ""
            converted = f"{{{modifier}{{bold {var}}}}}{subscript}{superscript}"
            return converted

        def replace_frac(match):
            numerator = match.group(1)
            denominator = match.group(2)
            # 분자와 분모를 재귀적으로 변환
            numerator = self.convert(numerator)
            denominator = self.convert(denominator)
            return f"{{{numerator}}} over {{{denominator}}}"

        def replace_matrix(match):
            matrix_type = match.group(1).strip()
            if matrix_type == 'array':
                matrix_type = 'matrix'
            content = match.group(3).strip()
            content = content.replace('\\hdashline', '')
            rows = [row.strip() for row in content.split('\\\\') if row.strip()]
            matrix_elements = []
            for row in rows:
                elements = [elem.strip() for elem in row.split('&') if elem.strip()]
                elements = [self.convert(elem) for elem in elements]
                matrix_elements.append(' & '.join(elements))
            matrix_content = ' # '.join(matrix_elements)
            return f"{matrix_type}{{{matrix_content}}}"

        # \dot{\mathbf {var}}_{sub}^{sup} 변환
        dot_bold_pattern = r'\\(dot|tilde|bar)\{\\mathbf\s*\{?([^{}\s]+)\}?\}(_\{[^{}]*\})?(\^\{[^{}]*\})?'
        latex_str = re.sub(dot_bold_pattern, replace_dot_bold, latex_str)

        # \frac
        frac_pattern = r'\\frac{((?:[^{}]|{[^{}]*})*)}{((?:[^{}]|{[^{}]*})*)}'
        latex_str = re.sub(frac_pattern, replace_frac, latex_str)

        # \begin{?matrix}...\end{?matrix}
        matrix_pattern = r'\\begin{(bmatrix|pmatrix|dmatrix|array)}(?:{([^{}]*?)})?([\s\S]*?)\\end{\1}'
        latex_str = re.sub(matrix_pattern, replace_matrix, latex_str)

        # aligned
        latex_str = re.sub(r'\\(begin|end){aligned}', lambda m: '', latex_str)
        latex_str = latex_str.replace('\\\\', ' # ')
        # mathbf
        latex_str = latex_str.replace('\\mathbf', 'bold')
        latex_str = latex_str.replace('\\boldsymbol', 'bold')
        # all the other commands
        latex_str = latex_str.replace('\\', ' ')
        # special cases
        latex_str = latex_str.replace('in', '\in')

        return latex_str

if __name__ == "__main__":
    test_cases = [
        r'\frac{a}{b}',
        r'\frac{\frac{c}{d}}{e}',
        r'\frac{a}{\frac{b}}{\frac{c}{d}}',
        r'x + \frac{1}{2} - \frac{\frac{3}{4}}{5}'
        r'\frac{a}{b}',
        r'\sqrt{x}',
        r'\frac{\sqrt{y}}{\frac{z}{w}}',
        r'\begin{bmatrix}a&b\\c&d\end{bmatrix}',
        r'x + \frac{1}{\sqrt{2}} - \begin{bmatrix}\frac{a}{b}&c\\\sqrt{d}&e\end{bmatrix}',
        r'\begin{bmatrix}a&\frac{b}{c}\\d&\sqrt{e}\end{bmatrix}',
        r'\begin{pmatrix}a&\frac{b}{c}\\d&\sqrt{e}\end{pmatrix}',
        r'\begin{dmatrix}a&\frac{b}{c}\\d&\sqrt{e}\end{dmatrix}',
        r'\begin{array}{cc}a&b\\c&d\end{array}',
        r'\begin{array}{ccc:cc}a&b&c&d&e\\\hdashline f&g&h&i&j\end{array}',
        r'\left[\begin{array}{c:c}\frac{a}{b}&\sqrt{c}\\\hdashline d&\frac{e}{f}\end{array}\right]',
        r'\begin{aligned}a &= b \\ cdec &= d+1234\end{aligned}',
        r'\begin{aligned}\frac{a}{b} &= \sqrt{c} \\ \mathbf A &= \begin{dmatrix}a&\frac{b}{c}\\d&\sqrt{e}\end{dmatrix}\end{aligned}',
        r'\dot{\mathbf v}_{1\times2}^2',
        r'\tilde{\mathbf v}_{1\times2}^2',
        r'\bar{\mathbf v}_{1\times2}^2',
        r'\alpha \boldsymbol\beta \dot{\boldsymbol\Omega}_{in}^n',
    ]

    for test in test_cases:
        l2h = Latex2HwpEq()
        result = l2h.convert(test)
        print(f"Input: {test}")
        print(f"{result}\n")
