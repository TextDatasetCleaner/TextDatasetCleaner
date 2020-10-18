from pytest import mark

from textdatasetcleaner.processors import CleanHTMLProcessor


class TestCleanHTML:

    @mark.parametrize('condition', [False, True])
    def test__text(self, condition: bool):
        processor = CleanHTMLProcessor(condition)

        line = 'Text without tags'
        assert processor.process_line(line) == line

        line = 'Text with < symbol'
        assert processor.process_line(line) == line

    def test__html__condition_and(self):
        processor = CleanHTMLProcessor()

        should_be = 'text with  google  link'
        assert processor.process_line('text with <a href="google.com">google</a> link') == should_be
        assert processor.process_line('text with <strong>google</strong> link') == should_be
        assert processor.process_line('text with <div><span>google</span></div> link') == should_be
        assert processor.process_line('text with <div><span>google</div></span> link') == should_be

        line = '5 <a'
        assert processor.process_line(line) == line

    def test__html_condition_or(self):
        processor = CleanHTMLProcessor(True)

        assert processor.process_line('text with <a href="google.com">yandex</a> link') == 'text with  yandex  link'
        assert processor.process_line('5 <a') == '5 a'
