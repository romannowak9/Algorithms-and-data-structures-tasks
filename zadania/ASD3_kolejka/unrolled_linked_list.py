from math import ceil


def realloc(tab, size):
    oldSize = len(tab)
    return [tab[i] if i < oldSize else None for i in range(size)]


TAB_SIZE = 6


class ListElem:
    def __init__(self, next=None):
        self.tab = realloc([], TAB_SIZE)
        self.fulfilment = 0
        self.next = next

    def insert(self, data, idx):
        if self.fulfilment < TAB_SIZE:
            tab1 = self.tab.copy()
            for i in range(idx, self.fulfilment):
                self.tab[i + 1] = tab1[i]

            self.tab[idx] = data
            self.fulfilment += 1
        else:
            raise ValueError("Tab is full!")

    def delete(self, idx):
        if idx >= TAB_SIZE:
            raise ValueError("Index out of range!")

        tab1 = self.tab.copy()
        i = 0
        for i in range(idx, self.fulfilment - 1):
            self.tab[i] = tab1[i + 1]

        if i + 1 < TAB_SIZE and i != 0:
            self.tab[i + 1] = None
        elif idx == self.fulfilment - 1:
            self.tab[idx] = None

        self.fulfilment -= 1

        return tab1[idx]

    def is_full(self):
        return True if self.fulfilment == TAB_SIZE else False

    def get(self, idx):
        return self.tab[idx]


class UnrolledList:
    def __init__(self):
        self.__head = None

    def __get_tab_by_idx(self, idx):
        el = self.__head
        current_idx = 0
        tab_idx = 0
        i = 0

        while el is not None and current_idx != idx:
            was_break = False
            for i in range(TAB_SIZE):
                if current_idx == idx:
                    was_break = True
                    break
                elif el.get(i) is not None:
                    current_idx += 1
                    tab_idx += 1

            # Nie znaleziono pasującego indeksu lub znaleziono go za ostatnim elementem nie ostatniej tablicy
            if (i == TAB_SIZE - 1 and not was_break) or \
                    (tab_idx == el.fulfilment and current_idx == idx and el.next is not None):
                el = el.next
                tab_idx = 0

        return el, tab_idx

    def is_empty(self):
        return True if self.__head is None else False

    def insert(self, data, idx=0):
        if self.is_empty():
            self.__head = ListElem()
            self.__head.insert(data, 0)
        else:
            tab, tab_idx = self.__get_tab_by_idx(idx)
            # print(tab, tab_idx)

            if tab is None:  # indeks poza zakresem
                # Nie optymalne
                new_elem = ListElem()
                el = self.__head
                while el.next is not None:
                    el = el.next

                el.next = new_elem
                new_elem.insert(data, 0)
            else:
                if not tab.is_full():  # Można zapisać w podtablicy
                    tab.insert(data, tab_idx)
                else:  # Nie ma już miejsca do zapisu
                    tab.next = ListElem(tab.next)
                    for i in range(TAB_SIZE // 2):
                        tab.next.insert(data=tab.delete(ceil(TAB_SIZE / 2)), idx=i)

                    if tab_idx < ceil(TAB_SIZE / 2):  # Zapis w starej cżęści
                        tab.insert(data, tab_idx)
                    else:  # Zapis w nowej części
                        tab.next.insert(data, tab_idx - ceil(TAB_SIZE / 2))

    def delete(self, idx):
        if self.is_empty():
            raise ValueError("List is already empty!")

        tab, tab_last_idx = self.__get_tab_by_idx(idx)

        if tab is None:  # indeks poza zakresem
            raise ValueError("Index out of range!")

        tab.delete(tab_last_idx)

        if tab.fulfilment < TAB_SIZE / 2:
            tab.insert(tab.next.delete(0), tab.fulfilment - 1)
            if tab.next.fulfilment >= TAB_SIZE / 2:
                for _ in range(tab.next.fulfilment):
                    tab.insert(tab.next.delete(0), tab.fulfilment - 1)

    def get(self, idx):
        if self.is_empty():
            return None

        tab, tab_idx = self.__get_tab_by_idx(idx)

        return tab.get(tab_idx)

    def __str__(self):
        el = self.__head
        s = '['
        i = 0
        while el is not None:
            for _ in range(el.fulfilment):
                s += "{}, ".format(self.get(i))
                i += 1
            el = el.next

        return s[:-2] + ']'

    def print_tabs(self):
        """ Funkcja do testów """
        el = self.__head
        while el is not None:
            print(el.tab)
            el = el.next


def main():
    l1 = UnrolledList()

    for i in range(1, 10):
        l1.insert(data=i, idx=i - 1)
    print()

    print(l1.get(4))
    print()

    l1.insert(data=10, idx=1)
    print(l1)
    print()
    l1.insert(data=11, idx=8)
    print(l1)
    print()

    l1.delete(1)
    l1.delete(2)

    print(l1)


if __name__ == '__main__':
    main()
