import builtins
import app
from unittest.mock import patch


def test_get_pdf_text(monkeypatch):
    class DummyPage:
        def __init__(self, text):
            self.text = text
        def extract_text(self):
            return self.text

    class DummyReader:
        def __init__(self, file):
            pass
        @property
        def pages(self):
            return [DummyPage('text1'), DummyPage(None)]

    monkeypatch.setattr(app, 'PdfReader', lambda _: DummyReader(_))
    result = app.get_pdf_text([object(), object()])
    assert result == 'text1text1'


def test_get_text_chunks(monkeypatch):
    calls = {}
    class DummySplitter:
        def __init__(self, separator, chunk_size, chunk_overlap, length_function):
            calls['params'] = (separator, chunk_size, chunk_overlap, length_function)
        def split_text(self, text):
            calls['text'] = text
            return ['chunkA', 'chunkB']

    monkeypatch.setattr(app, 'CharacterTextSplitter', DummySplitter)
    chunks = app.get_text_chunks('sample text')
    assert chunks == ['chunkA', 'chunkB']
    assert calls['text'] == 'sample text'
    assert calls['params'][0] == '\n'
    assert calls['params'][1] == 1000
    assert calls['params'][2] == 100
    assert calls['params'][3]('ab') == 2
