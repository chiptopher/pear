from unittest import TestCase
from unittest.mock import Mock
from pathlib import Path
from pear.loader import FileContainer, Line


class TestFileContainer(TestCase):
    def test_constructor_loads_lines_of_file(self):
        container = FileContainer(Path('test/files/Test.java'), Path('out'))
        self.assertEqual(container.lines, [
            Line('class Foo {\n', 1),
            Line('    Foo() {\n', 2),
            Line('    }\n', 3),
            Line('}\n', 4)
        ])

    def test_apply_applies_all_formatters_sequentially_to_lines(self):
        formatter = Mock()
        container = FileContainer(Path('test/files/Test.java'), Path('out'))
        container.formatters.append(formatter)

        container.apply()

        formatter.apply.assert_called_with(container.lines)

    def test_write_saves_file_with_formatter_applied(self):
        container = FileContainer(Path('test/files/Test.java'), Path('out'))
        container.write()

        with open('out/test/files/Test.java') as f:
            lines = f.readlines()

        self.assertEqual(lines, [
            'class Foo {\n',
            '    Foo() {\n',
            '    }\n',
            '}\n',
        ])

    def test_final_path_combines_output_dir_with_path(self):
        container = FileContainer(Path('test/files/Test.java'), Path('out'))
        expected = Path('out/test/files/Test.java')
        self.assertEqual(expected, container.final_path())

    def test_final_path_includes_tag(self):
        container = FileContainer(Path('test/files/Test.java'), Path('out'), tag='tag')
        expected = Path('out/test/files/Test.java_tag')
        self.assertEqual(expected, container.final_path())
