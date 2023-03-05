# butchered toml-like data parser. requires table head and does not support nested table and only accepts string (????)


class _DataContainer: 
    def __init__(self, name=''):
        self._tables = []
        self.name = name

    def add_table(self, table):
        self._tables.append(table)

    def get_multiple_prfx(self, prfx):
        return [i for i in self._tables if i.name.startswith(prfx)]

    def get_multiple(self, name):
        return [i for i in self._tables if i.name == name]

    def get(self, name):
        _r = self.get_multiple(name)
        if _r:
            return self.get_multiple(name)[0]
        return

    def pop(self, table):
        return self._tables.pop(self._tables.index(table))

    def __repr__(self):
        r = ''
        r += self.name + '\n'
        for i in self._tables:
            r += str(i) + '\n'
        return r

class _Table: 
    def __init__(self, name=''):
        self._key_value = dict()
        self.name = name

    def unpack_name(self, pattern_assignment=[None, None, 'part', None, 'test']):
        split = self.name.split('_')
        name_dict = dict()
        for i, k in enumerate(pattern_assignment):
            if i > len(split):
                name_dict[k] = None
                continue
            if k:
                name_dict[k] = split[i]
        return name_dict

    def set_value(self, key, value):
        self._key_value[key] = value

    def get(self, key):
        return self._key_value.get(key)

    def pop(self, key):
        return self._key_value.pop(key)

    
    def __repr__(self):
        r = ''
        r += '| ' + self.name + ' : '
        r += str(self._key_value)
        return r

def parse(b):
    lines = b.decode('utf-8').splitlines()
    data = _DataContainer('data')
    last_table_name = None
    while lines:
        line = lines.pop(0)
        if line.strip().startswith('[') and line.strip().endswith(']'):
            last_table_name = line.strip()[1:-1]
            table = _Table(last_table_name)
            data.add_table(table)
            continue

        elif ' = ' in line:
            split = line.strip().split(' = ')
            table = data.get(last_table_name)
            key = split[0].strip()
            value = split[1].strip()
            if (value.startswith('\'\'\'') and value.endswith('\'\'\'')) or \
                (value.startswith('"""') and value.endswith('"""')):
                while lines and not (lines[0].endswith('\'\'\'') or lines[0].endswith('"""')):
                    value += '\n' + lines.pop(0)
                value += '\n' + lines.pop(0)
                if value.endswith('"""'):
                    value = value[3:-3]
                else:
                    value = value[4:-3].rstrip()

            elif (value.startswith('\'') and value.endswith('\'')) or \
                (value.startswith('"') and value.endswith('"')):
                value = value[1:-1]

            table.set_value(key, value)
    return data
if __name__ == '__main__':
    sample = b"""
    [data_part_1_test_1]
    bar = 'baz'
    blargh = \"\"\"
    foo
    bar
    baz\"\"\"
    [bar]
    bar = 'baz'
    blargh = \"\"\"
    \"\"\"
    """

    res = parse(sample)
    print(dir(res))
    print(res)