class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


# 1. Восстановление бинарного дерева из массива
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


# 2. Симметричное бинарное дерево
def is_symmetric(root):
    def check(left, right):
        # Сравниваются пары узлов, зеркальные относительно середины:
        # (левый узел левого поддерева, правый узел правого поддерева)
        # и (правый узел левого, левый узел правого).
        # Если на каждом уровне такие пары совпадают — дерево симметричное.
        if left is None and right is None:
            return True
        if left is None or right is None:
            return False
        return left.val == right.val and check(left.left, right.right) and check(left.right, right.left)

    return check(root, root) if root else True


# 3. Минимальная глубина бинарного дерева
def min_depth(root):
    # BFS обходит дерево по уровням: сначала корень, затем уровень 2,
    # уровень 3 и т.д. Поэтому первый встреченный лист (узел без
    # потомков) гарантированно находится на минимальной глубине.
    if root is None:
        return 0
    from collections import deque
    queue = deque([(root, 1)])
    while queue:
        node, depth = queue.popleft()
        if node.left is None and node.right is None:
            return depth
        if node.left:
            queue.append((node.left, depth + 1))
        if node.right:
            queue.append((node.right, depth + 1))


# 4. Произведение минимального и максимального элементов BST
def bst_min_max_product(arr):
    # В BST минимальный элемент — самый левый узел (у него нет левого
    # потомка), максимальный — самый правый. Идём по одному пути
    # от корня вниз: на каждом уровне выбираем левое/правое поддерево.
    # Путь занимает не более h узлов (высота дерева), поэтому O(h).
    if not arr or arr[0] is None:
        return -1
    root = build_tree(arr)
    cur = root
    while cur.left:
        cur = cur.left
    mn = cur.val
    cur = root
    while cur.right:
        cur = cur.right
    mx = cur.val
    return mn * mx


# 5. Сравнение двух бинарных деревьев
def is_same_tree(p, q):
    # Деревья идентичны, если одновременно выполняются три условия:
    # 1) оба узла пустые -> совпадают
    # 2) один пустой, другой нет -> не совпадают
    # 3) значения узлов равны И левые поддеревья идентичны
    #    И правые поддеревья идентичны (рекурсия)
    if p is None and q is None:
        return True
    if p is None or q is None:
        return False
    if p.val != q.val:
        return False
    return is_same_tree(p.left, q.left) and is_same_tree(p.right, q.right)
