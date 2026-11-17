from collections import deque
import heapq


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
        self.balance_factor = 0


def build_tree(arr, i=0):
    # Связь родитель-потомок: для узла с индексом i в level-order
    # массиве его левый потомок находится в arr[2*i+1],
    # правый — в arr[2*i+2].
    # Хранение: узел TreeNode со значениями val, left, right.
    if i >= len(arr) or arr[i] is None:
        return None
    root = TreeNode(arr[i])
    root.left = build_tree(arr, 2 * i + 1)
    root.right = build_tree(arr, 2 * i + 2)
    return root


# 1. Полное бинарное дерево
def is_complete(root):
    # Условие заполненности уровней: все уровни, кроме последнего,
    # заполнены целиком, а последний — слева направо, без пропусков.
    # Эквивалентно: после первого узла, у которого нет левого или
    # правого потомка, все остальные узлы должны быть листьями.
    # Выбран BFS (обход по уровням): только он идёт ровно в том
    # порядке, в котором определено условие — уровень за уровнем
    # слева направо, поэтому первая же найденная "дырка" сразу
    # говорит о неполноте. Время O(n), память O(ширины дерева).
    if root is None:
        return True
    queue = deque([root])
    found_gap = False
    while queue:
        node = queue.popleft()
        for child in (node.left, node.right):
            if child is None:
                found_gap = True      # дырка: дальше только листья
            elif found_gap:
                return False          # узел после дырки — не полное
            else:
                queue.append(child)
    return True


# 2. Объединение K отсортированных массивов
def merge_k_sorted(arrays):
    # В каждый момент нужен минимум из K текущих "голов" массивов.
    # Мин-куча находит его за O(log k) вместо линейного просмотра O(k).
    # Кладём (значение, индекс массива, индекс элемента); забрав
    # минимум, подставляем следующий элемент из того же массива.
    #
    # Сложность: всего n = sum(len(arr)) элементов, на каждый — одно
    # извлечение и одна вставка в кучу размера <= k, то есть O(log k).
    # Итого O(n log k) времени, O(k) памяти на кучу (+ O(n) на ответ).
    heap = []
    for i, arr in enumerate(arrays):
        if arr:
            heapq.heappush(heap, (arr[0], i, 0))
    result = []
    while heap:
        val, arr_idx, elem_idx = heapq.heappop(heap)
        result.append(val)
        if elem_idx + 1 < len(arrays[arr_idx]):
            heapq.heappush(heap, (arrays[arr_idx][elem_idx + 1], arr_idx, elem_idx + 1))
    return result


# 3. K-ый наименьший / наибольший элемент
def kth_smallest(nums, k):
    # Держим max-кучу (min-heap с отрицанием) размера k из k наименьших
    # элементов. Корень — самый большой из них, то есть k-ый наименьший.
    # Время O(n log k) (каждый элемент — не более одной операции с кучей
    # размера k), память O(k). Полная сортировка была бы O(n log n);
    # быстрый выбор (quickselect) даёт O(n) в среднем, но O(n^2) в худшем.
    heap = []
    for num in nums:
        if len(heap) < k:
            heapq.heappush(heap, -num)
        elif num < -heap[0]:      # исправлено: заменяем, если новое меньше
            heapq.heapreplace(heap, -num)
    return -heap[0]


def kth_largest(nums, k):
    # Симметрично: min-куча размера k из k наибольших, корень — самый
    # маленький из них, то есть k-ый наибольший. O(n log k), память O(k).
    heap = []
    for num in nums:
        if len(heap) < k:
            heapq.heappush(heap, num)
        elif heap[0] < num:
            heapq.heapreplace(heap, num)
    return heap[0]


# 4. K-ый наименьший / наибольший элемент в BST
def kth_smallest_bst(root, k):
    # Свойство BST: узел больше всех в левом поддереве и меньше всех
    # в правом. Поэтому inorder-обход (лево -> узел -> право) выдаёт
    # значения строго по возрастанию, и k-ое посещённое значение —
    # k-ый наименьший. Останавливаемся сразу на k-м узле.
    # Время O(h + k), память O(h) на стек рекурсии (h — высота).
    count = 0
    result = None

    def inorder(node):
        nonlocal count, result
        if node is None or result is not None:
            return
        inorder(node.left)
        count += 1
        if count == k:
            result = node.val
            return
        inorder(node.right)

    inorder(root)
    return result


def kth_largest_bst(root, k):
    # Зеркальный inorder (право -> узел -> лево) выдаёт значения
    # по убыванию, значит k-ое посещённое — k-ый наибольший.
    # Время O(h + k), память O(h).
    count = 0
    result = None

    def reverse_inorder(node):
        nonlocal count, result
        if node is None or result is not None:
            return
        reverse_inorder(node.right)
        count += 1
        if count == k:
            result = node.val
            return
        reverse_inorder(node.left)

    reverse_inorder(root)
    return result


# 5. Balance factor
def compute_balance(root):
    # Высота узла = 1 + max(высота левого, высота правого поддерева),
    # высота пустого поддерева = 0.
    # Считаем снизу вверх в одном postorder-проходе: сначала высоты
    # детей, затем balance_factor = высота левого - высота правого,
    # затем высота самого узла (её возвращаем наверх).
    # Высоты детей сохраняются в переменных, повторных спусков нет,
    # поэтому каждый узел обрабатывается один раз: O(n) времени, O(h) стека.
    def height(node):
        if node is None:
            return 0
        left_h = height(node.left)
        right_h = height(node.right)
        node.balance_factor = left_h - right_h
        return 1 + max(left_h, right_h)

    height(root)
    return root


# 6. Преобразование в зеркальное дерево
def mirror_tree(root):
    # Меняем местами left и right у каждого узла.
    #
    # Корректность (индукция по высоте):
    # - пустое дерево зеркально само себе;
    # - для непустого: после обмена поддеревьями корня на месте левого
    #   стоит правое поддерево, на месте правого — левое, как и требует
    #   зеркало; затем рекурсивно отражаем каждое поддерево, и по
    #   предположению индукции они тоже становятся зеркальными.
    # Значит зеркально всё дерево.
    #
    # Время O(n): каждый узел посещается ровно один раз (обмен — O(1)).
    # Память O(h) на стек рекурсии.
    if root is None:
        return None
    root.left, root.right = root.right, root.left
    mirror_tree(root.left)
    mirror_tree(root.right)
    return root
