def read_last_lines(filename, lines_count=10, block_size=1800, encoding='utf-8'):
    with open(filename, 'rb') as f:
        f.seek(0, 2)
        end = f.tell()
        start = max(0, end-block_size)
        f.seek(start)
        lines = f.readlines()
        for line in lines[-lines_count:]:
            yield line.decode(encoding).strip()