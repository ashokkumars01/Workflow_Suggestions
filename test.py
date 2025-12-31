# =========================
# REDUNDANCY TEST FILE
# =========================

# -------- Case 1: Exact duplicate functions --------
def calculate_sum_v1(numbers):
    total = 0
    for n in numbers:
        total += n
    return total


def calculate_sum_v2(numbers):
    total = 0
    for n in numbers:
        total += n
    return total


# -------- Case 2: Near-duplicate logic (variable rename) --------
def find_max_v1(values):
    max_val = values[0]
    for v in values:
        if v > max_val:
            max_val = v
    return max_val


def find_max_v2(nums):
    current_max = nums[0]
    for n in nums:
        if n > current_max:
            current_max = n
    return current_max


# -------- Case 3: Copy-paste blocks inside functions --------
def process_orders(orders):
    total_price = 0
    for order in orders:
        total_price += order["price"]

    # duplicated block
    discount = 0
    for order in orders:
        discount += order["price"] * 0.1

    return total_price - discount


def process_orders_v2(orders):
    total_price = 0
    for order in orders:
        total_price += order["price"]

    # duplicated block (same as above)
    discount = 0
    for order in orders:
        discount += order["price"] * 0.1

    return total_price - discount


# -------- Case 4: Redundant condition checks --------
def check_user_access(user):
    if user is not None:
        if user is not None:
            if user.is_active:
                return True
    return False


# -------- Case 5: Inefficient repeated computation --------
def calculate_average(numbers):
    total = sum(numbers)
    count = len(numbers)

    # redundant recalculation
    avg1 = total / count
    avg2 = total / count

    return avg1, avg2


# -------- Case 6: Loop redundancy --------
def count_even_numbers(nums):
    count = 0
    for n in nums:
        if n % 2 == 0:
            count += 1

    # redundant second loop
    count2 = 0
    for n in nums:
        if n % 2 == 0:
            count2 += 1

    return count, count2
