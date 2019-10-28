from tempfile import gettempdir
from os.path import join


class File:

    def __init__(self, path):
        self.path = path
        self.current = 0

    def write(self, text):
        with open(self.path, 'w') as f:
            f.write(text)

    def __add__(self, another):
        new_file = 'new_file.txt'
        with open(self.path, 'r') as f1:
            with open(another.path, 'r') as f2:
                new_dir = join(gettempdir())
                print(new_dir)
                with open(new_dir + "/" + new_file, 'w') as f3:
                    f3.write(f1.read() + f2.read())

    def __iter__(self):
        return self

    def __next__(self):
        with open(self.path, 'r') as f:
            f.seek(self.current)
            row = f.readline()
            if not row:
                self.current = 0
                raise StopIteration('EOF')
            self.current = f.tell()
            return row

    def __str__(self):
        return self.path
