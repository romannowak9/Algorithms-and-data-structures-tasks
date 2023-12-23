from typing import Union, Any, List, Optional


class HashElem:
    def __init__(self, key: Union[str, float, int], data: Any) -> None:
        self.key = key
        self.data = data


class HashTable:
    def __init__(self, size: int, c1: Union[int, float] = 1, c2: Union[int, float] = 0) -> None:
        self.__size = size
        self.__tab: List[Optional[HashElem]] = [None for i in range(size)]
        self.__c1 = c1
        self.__c2 = c2

    def hash_fun(self, key: Union[str, float, int]) -> int:
        if isinstance(key, float) or isinstance(key, int):
            return key % self.__size
        if isinstance(key, str):
            return sum([ord(letter) for letter in key]) % self.__size

    def collision(self, key: Union[str, float, int]) -> int:
        idx = self.hash_fun(key)
        i = 1
        new_idx = None
        while i <= self.__size:
            new_idx = (idx + self.__c1 * i + self.__c2 * i ** 2) % self.__size
            if not self.__tab[new_idx]:
                break
            i += 1

        return new_idx if i <= self.__size else None

    def search(self, key: Union[str, float, int]) -> Any:
        for el in self.__tab:
            if el:
                if el.key == key:
                    return el.data

        return None

    def insert(self, data: Any, key: Union[str, float, int]) -> None:
        el = self.search(key)
        if not el and all(self.__tab):
            raise ValueError("No space!")

        idx = self.hash_fun(key)

        if self.__tab[idx]:
            if self.__tab[idx].key != key:
                idx = self.collision(key)

        if idx is not None:
            self.__tab[idx] = HashElem(key, data)

    def remove(self, key: Union[str, float, int]) -> None:
        el = self.search(key)
        if not el:
            raise ValueError("No matching data!")

        idx = self.hash_fun(key)
        self.__tab[idx] = None

    def __str__(self) -> str:
        s = "{"
        for el in self.__tab:
            if el:
                s += "{}:{}, ".format(el.key, el.data)
            else:
                s += "{}, ".format(el)

        return s[:-2] + "}"


def test_fun1(size, c1=1, c2=0):
    h_table = HashTable(size, c1, c2)

    for i in range(size + 2):
        try:
            if i == 5:
                h_table.insert(data=chr(65 + i), key=18)
            elif i == 6:
                h_table.insert(data=chr(65 + i), key=31)
            else:
                h_table.insert(data=chr(65 + i), key=i + 1)
        except ValueError as ex:
            print(ex)

    print(h_table)

    print(h_table.search(5))
    print(h_table.search(14))

    h_table.insert(data='Z', key=5)
    print(h_table.search(5))

    h_table.remove(5)

    print(h_table)
    print(h_table.search(31))

    h_table.insert(data='W', key='test')
    print(h_table)


def test_fun2(size, c1=1, c2=0):
    h_table = HashTable(size, c1, c2)

    for i in range(size):
        try:
            h_table.insert(data=chr(65 + i), key=(i + 1) * 13)
        except ValueError as ex:
            print(ex)

    print(h_table)


def main():
    print("Pierwsza funkcja testująca")
    test_fun1(13)
    print("Druga funkcja testująca, próbkowanie liniowe")
    test_fun2(13)
    print("Druga funkcja testująca, próbkowanie kwadratowe")
    test_fun2(13, 0, 1)


if __name__ == '__main__':
    main()
