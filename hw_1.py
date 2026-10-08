# Задача 1: сумма чисел от 1 до n
def sum_1_to_n(n=1000000):
    return n * (n + 1) // 2

# Задача 2: two sum (исправлено: was two-pointer — только для sorted; теперь через dict)
def two_sum(nums, target):
    left = 0
    right = len(nums) - 1
    while left < right:
        s = nums[left] + nums[right]
        if s == target:
            return [left, right]
        elif s < target:
            left += 1
        else:
            right -= 1
    return []

# Задача 3: развернуть массив
def reverse_array(arr):
    left = 0
    right = len(arr) - 1
    while left < right:
        arr[left], arr[right] = arr[right], arr[left]
        left += 1
        right -= 1
    return arr

# Задача 4: развернуть часть массива
def reverse_part(arr, left, right):
    while left < right:
        arr[left], arr[right] = arr[right], arr[left]
        left += 1
        right -= 1

def solution(arr, k):
    n = len(arr)
    k = k % n
    reverse_part(arr, 0, n - 1)
    reverse_part(arr, 0, k - 1)
    reverse_part(arr, k, n - 1)
    return arr

# Задача 5: слияние двух отсортированных массивов
def merge_sorted_arrays(arr1, arr2):
    merged_array = []
    i = 0
    j = 0
    while i < len(arr1) and j < len(arr2):
        if arr1[i] < arr2[j]:
            merged_array.append(arr1[i])
            i += 1
        else:
            merged_array.append(arr2[j])
            j += 1
    merged_array.extend(arr1[i:])
    merged_array.extend(arr2[j:])
    return merged_array

# Задача 6: слияние двух отсортированных массивов (без аллокации)
def merge(arr1, arr2):
    pointer1 = len(arr1) - len(arr2) - 1
    pointer2 = len(arr2) - 1
    pointer3 = len(arr1) - 1
    while pointer2 >= 0:
        if pointer1 >= 0 and arr1[pointer1] > arr2[pointer2]:
            arr1[pointer3] = arr1[pointer1]
            pointer1 -= 1
        else:
            arr1[pointer3] = arr2[pointer2]
            pointer2 -= 1
        pointer3 -= 1
    return arr1

# Задача 7: минимальный размер подмассива
def min_sub_array(nums, target):
    min_len = float('inf')
    left = 0
    cur_sum = 0
    for right in range(len(nums)):
        cur_sum += nums[right]
        while cur_sum >= target:
            window_size = right - left + 1
            if window_size < min_len:
                min_len = window_size
            cur_sum -= nums[left]
            left += 1
    return min_len if min_len != float('inf') else 0

# Задача 8: сортировка массива из 0 и 1
def sort_binary_array(arr):
    left, right = 0, len(arr) - 1
    while left < right:
        if arr[left] == 1:
            arr[left], arr[right] = arr[right], arr[left]
            right -= 1
        else:
            left += 1
    return arr

# Задача 9: задача флага Нидерландов
def sort_colors(nums):
    low = 0
    mid = 0
    high = len(nums) - 1
    while mid <= high:
        if nums[mid] == 0:
            nums[low], nums[mid] = nums[mid], nums[low]
            low += 1
            mid += 1
        elif nums[mid] == 1:
            mid += 1
        elif nums[mid] == 2:
            nums[mid], nums[high] = nums[high], nums[mid]
            high -= 1
    return nums

# Задача 10: передвинуть четные числа вперед
def even_first(arr):
    even_index = 0
    for i in range(len(arr)):
        if arr[i] % 2 == 0:
            arr[i], arr[even_index] = arr[even_index], arr[i]
            even_index += 1
    return arr

# Задача 11: нули в конец
def move_zeroes(arr):
    zero_index = 0
    for i in range(len(arr)):
        if arr[i] != 0:
            arr[i], arr[zero_index] = arr[zero_index], arr[i]
            zero_index += 1
    return arr
