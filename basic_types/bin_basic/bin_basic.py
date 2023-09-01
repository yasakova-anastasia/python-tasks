def find_value(nums: list[int] | range, value: int) -> bool:
    """
    Find value in sorted sequence
    :param nums: sequence of integers. Could be empty
    :param value: integer to find
    :return: True if value exists, False otherwise
    """
    if not len(nums):
        return False
    left = 0
    right = len(nums)
    while right > left + 1:
        median = (left + right) // 2
        if nums[median] < value + 1:
            left = median
        else:
            right = median
    if nums[left] == value:
        return True
    return False
