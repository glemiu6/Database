ANY = '_'  # constante a usar na definição dos padrões de registo


class Table:
    def __init__(self, scheme, key_idx, widths):

        self._scheme = scheme.split(' ')  # list[]
        self._key_idx = key_idx  # primary key
        self._table = {}  # punem continutul aici
        self._widths = widths

    def add(self, insert):  # add value to the table
        key = tuple(insert[i] for i in self._key_idx )

        self._table[key] = insert

    def delete(self, pattern):  # deletes from the table
        to_remove = [key for key, row in self._table.items() if
                     all(p == ANY or p == val for p, val in zip(pattern, row))]
        for key in to_remove:
            del self._table[key]

    def lookup(self, pattern):  # serches for the pattern in the table and returns the result
        result = [row for row in self._table.values() if all(p==ANY or p==val for p, val in zip(pattern, row))]
        """for row in self._table.values():
            if all(p == ANY or p == val for p, val in zip(pattern, row)):
                result.append(row)"""
        return result

    def select(self, p):  # selects a parameter and return a new table
        new_table = Table(' '.join(self._scheme), key_idx=self._key_idx, widths=self._widths)
        for row in self._table.values():
            if p(row):
                new_table.add(row)
        return new_table


    def project(self, subscheme, subkey_idx):
        subscheme=subscheme.split(' ')
        index_col=[self._scheme[i] for i in subscheme]
        new_width=[self._widths[x] for x in index_col]
        new_table=Table(' '.join(subscheme), key_idx=subkey_idx, widths=new_width)
        for row in self._table.values():
            project_row=[row[i] for i in index_col]
            new_table.add(project_row)
        return new_table

    def __add__(self, other):  # return a new table where the new values/table are concatenated

        result = Table(' '.join(self._scheme), key_idx=self._key_idx, widths=self._widths)
        for row in self._table.values():
            result.add(row)
        for row in other._table.values():
            result.add(row)
        return result

    def __mul__(self, other):  # return a new table where we get the common value
        result = Table(' '.join(self._scheme), key_idx=self._key_idx, widths=self._widths)
        other_key = set(other._table.keys())
        for key, row in self._table.items():
            if key in other_key:
                result.add(row)
        return result

    def __sub__(self, other):  # return the difference between the tables
        result = Table(' '.join(self._scheme), key_idx=self._key_idx, widths=self._widths)
        other_key = set(other._table.keys())
        for key, row in self._table.items():
            if key not in other_key:
                result.add(row)
        return result


    def __pow__(self,other):
        """

        :param other: object
        :return: object
        """

        new_scheme=[]
        for col in self._scheme + other._scheme:
            if col not in new_scheme:
                new_scheme.append(col)

        new_key_idx = [new_scheme.index(col) for col in self._key_idx + other._key_idx if col in new_scheme]

        new_width= self._widths
        for col , w in zip(other._scheme, other._widths ):
            if col not in self._scheme:
                new_width.append(w)

        new_table=Table(' '.join(new_scheme),key_idx=new_key_idx, widths=new_width)

        for row in self._table.values():
            new_table.add(row)
        for row in other._table.values():
            new_table.add(row)

        return new_table

    ##### não alterar __repr__ #####
    def __repr__(self):
        header = ' | '.join((k + '!' * (i in self._key_idx)).ljust(self._widths[i])
                            for i, k in enumerate(self._scheme))
        content = '\n'.join(' | '.join(str(column).ljust(self._widths[i])
                                       for i, column in enumerate(row))
                            for row in self._table.values())
        return '\n'.join((header + '\n' + content).split('\n'))

def make_db():
    addresses = Table('id num address country', key_idx=[0], widths=[3, 5, 36, 8])
    # [id , num, address, country], id!, widths=[len(id),len(num),len(address),len(country)] reprezinta cate caractere este in fiecare coloana
    addresses.add((1, 50000, "Campo Grande 016, 1749-016 Lisboa", 'PT'))
    addresses.add((2, 50000, "Av. da Liberdade 2, 1250-144 Lisboa", 'PT'))
    addresses.add((3, 50001, "Av. da Republica 12, 1210-54 Lisboa", 'PT'))
    addresses.add((4, 50002, "Av. Infante Santo 8, 1350-001 Lisboa", 'PT'))

    students = Table('num name grad year', key_idx=[0], widths=[5, 12, 5, 4])
    students.add((50000, 'Ana', 'LEI', 2020))
    students.add((50001, 'Rui', 'LEI', 2022))
    students.add((50002, 'Pedro', 'LTI', 2022))
    students.add((50003, 'Dulce', 'LF', 2021))
    students.add((50004, 'Pedro', 'LMA', 2022))

    return addresses, students

