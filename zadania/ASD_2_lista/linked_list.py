class ListElem:
    def __init__(self, data, next=None, prev=None):
        self.data = data
        self.next = next
        self.prev = prev


class TwoDirectionList:
    def __init__(self):
        self.__head = None
        self.__tail = None

    def destroy(self):
        if not self.is_empty():
            self.__head.next.prev = None
            self.__tail.prev.next = None

        self.__tail = None
        self.__head = None

    def add(self, data):
        if not self.is_empty():
            self.__head = ListElem(data, next=self.__head, prev=None)
            self.__head.next.prev = self.__head
        else:
            self.__head = ListElem(data, next=self.__head, prev=None)
            self.__tail = self.__head

    def append(self, data):
        if not self.is_empty():
            self.__tail = ListElem(data, next=None, prev=self.__tail)
            self.__tail.prev.next = self.__tail
        else:
            self.__head = ListElem(data, next=self.__tail, prev=None)
            self.__tail = self.__head

    def remove(self):
        if not self.is_empty():
            self.__head = self.__head.next
            self.__head.prev = None
            self.__head.next.prev = self.__head

    def remove_end(self):
        if not self.is_empty():
            self.__tail = self.__tail.prev
            self.__tail.next = None
            self.__tail.prev.next = self.__tail

    def is_empty(self):
        return True if self.__head is None else False

    def __len__(self):
        if self.is_empty():
            return 0
        el = self.__head
        count = 0
        while el.next is not None:
            el = el.next
            count += 1

        return count

    def get(self):
        return self.__head.data if not self.is_empty() else None

    def __str__(self):
        if self.is_empty():
            return ""

        el = self.__head
        str_list = ""
        while el.next is not None:
            str_list += "-> {}\n".format(el.data)
            el = el.next

        return str_list


def main():
    example = [('AGH', 'Kraków', 1919),
               ('UJ', 'Kraków', 1364),
               ('PW', 'Warszawa', 1915),
               ('UW', 'Warszawa', 1915),
               ('UP', 'Poznań', 1919),
               ('PG', 'Gdańsk', 1945)]

    uczelnie = TwoDirectionList()
    for el in example:
        uczelnie.append(el)

    print(uczelnie)
    print("Długość listy wiązanej:", len(uczelnie))

    uczelnie.remove()

    print("Pierwszy element po usunięciu poprzedniego:", uczelnie.get())

    uczelnie.remove_end()

    print()
    print(uczelnie)

    uczelnie.destroy()

    print("Wynik is_empty() po usunięciu listy uczelnie:", uczelnie.is_empty())

    uczelnie.remove()
    uczelnie.remove_end()


if __name__ == "__main__":
    main()
