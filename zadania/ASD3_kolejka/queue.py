def realloc(tab, size):
    oldSize = len(tab)
    return [tab[i] if i < oldSize else None for i in range(size)]


# Dodawanie na koniec pobieranie z początku
class Queue:
    def __init__(self):
        self.size = 5
        self.__tab = realloc([], self.size)
        self.__write_idx = 0
        self.__read_idx = 0

    def is_empty(self):
        return True if self.__write_idx == self.__read_idx else False

    def peek(self):
        return self.__tab[self.__read_idx] if not self.is_empty() else None

    def dequeue(self):
        if self.is_empty():
            return None

        data = self.__tab[self.__read_idx]
        self.__read_idx = (self.__read_idx + 1) if self.__read_idx != self.size - 1 else 0
        return data

    def enqueue(self, data):
        self.__tab[self.__write_idx] = data
        #print("w:", self.__write_idx, "r:", self.__read_idx)
        self.__write_idx = (self.__write_idx + 1) if self.__write_idx != self.size - 1 else 0

        if self.is_empty():
            self.__tab = realloc(self.__tab, self.size * 2)
            for i, el in enumerate(self.__tab[self.__write_idx:self.size]):
                self.__tab[i + self.__write_idx + self.size] = el

            self.__read_idx += self.size
            self.size = self.size * 2

    def __str__(self):
        if self.is_empty():
            return "[]"

        s = "["
        i = 0
        while self.__read_idx + i != self.size - 1:
            s += "{}, ".format(self.__tab[self.__read_idx + i])
            i += 1

        if self.__write_idx < self.__read_idx:
            for i in range(self.__write_idx):
                s += "{}, ".format(self.__tab[i])

        return s[:-2] + "]"

    def print_raw(self):
        print(self.__tab)


def main():
    q1 = Queue()
    for i in range(1, 5):
        q1.enqueue(i)

    print("wynik dequeue():", q1.dequeue())
    print("wynik peek():", q1.peek())

    print("kolejka:", q1)

    for i in range(5, 9):
        q1.enqueue(i)

    print("tablica po dodaniu pięci kolejnych elementów: ", end='')
    q1.print_raw()

    while not q1.is_empty():
        print("wynik dequeue():", q1.dequeue())

    print("kolejka:", q1)

if __name__ == '__main__':
    main()
