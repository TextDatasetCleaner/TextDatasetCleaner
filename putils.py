from itertools import (takewhile, repeat)


def file_lines_count(filename):
    f = open(filename, 'rb')
    bufgen = takewhile(lambda x: x, (f.raw.read(1024*1024) for _ in repeat(None)))
    return sum( buf.count(b'\n') for buf in bufgen if buf )


def write_wrong(fh, text):
    if fh:
        fh.write(text)
