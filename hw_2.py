from collections import deque

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

# Функции преобразования списков без циклом в массивы и наоборот
# для правильного формата ввода в последней задаче,
# но я оформила ее по образцу предыдущих, рассчитывая, что она
# тоже принимает уже список на вход

def list_to_array(head):
    out = []
    while head is not None:
        out.append(head.val)
        head = head.next
    return out


def array_to_list(vals):
    dummy = ListNode(0)
    cur = dummy
    for v in vals:
        cur.next = ListNode(v)
        cur = cur.next
    return dummy.next

# Задача 1: Проверить, является ли список циклическим
def has_cycle(head):
    if head is None or head.next is None:
        return False
    slow, fast = head, head.next
    while slow is not fast:
        if fast is None or fast.next is None:
            return False
        slow = slow.next
        fast = fast.next.next
    return True

# Задача 2: Развернуть односвязный список
def reverse_linked_list(head):
    prev, current = None, head
    while current is not None:
        nxt = current.next
        current.next = prev
        prev = current
        current = nxt
    return prev

# Задача 3: Найти середину списка
def middle_node(head):
    slow = fast = head
    while fast is not None and fast.next is not None:
        slow = slow.next
        fast = fast.next.next
    return slow

# Задача 4: Удалить элемент из односвязного списка
def remove_elements(head, val):
    dummy = ListNode(0)
    dummy.next = head
    prev, cur = dummy, head
    while cur is not None:
        if cur.val == val:
            prev.next = cur.next
        else:
            prev = cur
        cur = cur.next
    return dummy.next

# Задача 5: Удаление n-ого элемента с конца списка
def remove_nth_from_end(head, n):
    dummy = ListNode(0, head)
    slow = fast = dummy
    for _ in range(n + 1):
        fast = fast.next
    while fast is not None:
        slow = slow.next
        fast = fast.next
    slow.next = slow.next.next
    return dummy.next

# Задача 6: Является ли одна строка исходной для другой (через очередь)
def is_subsequence_queue(a, b):
    q = deque(a)
    for el in b:
        if q and q[0] == el:
            q.popleft()
    return len(q) == 0

# Задача 6: Является ли одна строка исходной для другой (через 2 указателя)
def is_subsequence_two_pointers(a, b):
    i = j = 0
    while i < len(a) and j < len(b):
        if a[i] == b[j]:
            i += 1
        j += 1
    return i == len(a)

# Задача 6: Является ли одна строка исходной для другой (наивная реализация)
def is_subsequence_naive(a, b):
    i = 0
    for el1 in a:
        found = False
        for el2 in b:
            if el1 == el2:
                i += 1
                found = True
                break
        if not found:
            break
    return i == len(a)

# Задача 7: Является ли слово палиндромом (через стек)
def is_palindrome_stack(s):
    stack = []
    for char in s:
        stack.append(char)
    for char in s:
        if char != stack.pop():
            return False
    return True

# Задача 7: Является ли слово палиндромом (через 2 указателя)
def is_palindrome_two_pointers(s):
    left, right = 0, len(s) - 1
    while left < right:
        if s[left] != s[right]:
            return False
        left += 1
        right -= 1
    return True

# Задача 8: Сортировка массива через дополнительный стек
def sort_array_using_stack(arr):
    stack = []
    input_list = list(arr)
    while input_list:
        current = input_list.pop()
        while stack and stack[-1] > current:
            input_list.append(stack.pop())
        stack.append(current)
    return stack

# Задача 9: Слияние двух отсортированных списков
def merge_two_sorted_lists(head1, head2):
    dummy = ListNode(0)
    tail = dummy
    while head1 is not None and head2 is not None:
        if head1.val <= head2.val:
            tail.next = head1
            head1 = head1.next
        else:
            tail.next = head2
            head2 = head2.next
        tail = tail.next
    tail.next = head1 if head1 is not None else head2
    return dummy.next
