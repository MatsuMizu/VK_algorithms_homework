from collections import deque

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

# Функции преобразования списков без циклом в массивы и наоборот
# для правильного формата ввода в последней задаче,
# но я оформила ее по образцу предыдущих, рассчитывая, что она
# тоже принимает уже список на вход


# Новые задачи из файла, но не из презентации:
# 1. Метод двух указателей (поиск пары)
def has_pair_with_sum(nums, target):
    # Один указатель в начале (left), другой в конце (right).
    # На каждом шаге считаем сумму nums[left] + nums[right]:
    #   - равна target -> пара найдена;
    #   - меньше target -> даже самый большой возможный партнёр
    #     для nums[left] (это nums[right]) слишком мал, значит
    #     nums[left] не подходит ни с кем -> left += 1;
    #   - больше target -> nums[right] слишком велик даже с самым
    #     маленьким (nums[left]) -> right -= 1.
    #
    # Почему O(n): на каждом шаге мы проверяем одну пару и
    # отбрасываем один элемент, к которому уже никогда не вернёмся.
    # Всего n шагов, каждый за O(1), сортировка не нужна (массив
    # уже отсортирован). Итого O(n) времени и O(1) памяти.
    left, right = 0, len(nums) - 1
    while left < right:
        s = nums[left] + nums[right]
        if s == target:
            return True
        if s < target:
            left += 1
        else:
            right -= 1
    return False


# 2. Метод двух указателей (удаление дубликатов)
def remove_duplicates(nums):
    # slow — позиция последнего уникального элемента (граница
    #          "готовой" части массива),
    # fast — позиция текущего проверяемого элемента.
    # Если nums[fast] отличается от nums[slow], это новый уникальный
    # элемент: сдвигаем slow и перезаписываем nums[slow] = nums[fast].
    #
    # Почему без дополнительной памяти: перезапись всегда идёт
    # в позицию slow <= fast, то есть только в уже прочитанную
    # часть массива. Значение nums[fast] мы берём ДО того, как
    # его может затронуть запись, а всё, что левее slow, — уже
    # готовый результат, который больше не меняется.
    # Массив отсортирован, поэтому одинаковые элементы идут
    # подряд, и достаточно сравнения с последним уникальным.
    #
    # Время O(n) (один проход), память O(1).
    # Возвращаем новую длину: nums[:length] — массив без дублей.
    if not nums:
        return 0
    slow = 0
    for fast in range(1, len(nums)):
        if nums[fast] != nums[slow]:
            slow += 1
            nums[slow] = nums[fast]
    return slow + 1


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
