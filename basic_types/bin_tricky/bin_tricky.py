from collections.abc import Sequence


def find_median(nums1: Sequence[int], nums2: Sequence[int]) -> float:
    """
    Find median of two sorted sequences. At least one of sequences should be not empty.
    :param nums1: sorted sequence of integers
    :param nums2: sorted sequence of integers
    :return: middle value if sum of sequences' lengths is odd
             average of two middle values if sum of sequences' lengths is even
    """
    if not len(nums2):
        if not len(nums1) % 2:
            return (nums1[len(nums1) // 2] + nums1[len(nums1) // 2 - 1]) / 2
        else:
            return float(nums1[len(nums1) // 2])

    if not len(nums1):
        if not len(nums2) % 2:
            return (nums2[len(nums2) // 2] + nums2[len(nums2) // 2 - 1]) / 2
        else:
            return float(nums2[len(nums2) // 2])

    nums = []
    i, j = 0, 0
    while i < len(nums1) and j < len(nums2):
        if nums1[i] < nums2[j]:
            nums.append(nums1[i])
            i += 1
        elif nums1[i] > nums2[j]:
            nums.append(nums2[j])
            j += 1
        else:
            nums.append(nums1[i])
            nums.append(nums2[j])
            i += 1
            j += 1

    if i == len(nums1):
        while j < len(nums2):
            nums.append(nums2[j])
            j += 1

    if j == len(nums2):
        while i < len(nums1):
            nums.append(nums1[i])
            i += 1

    if not (len(nums1) + len(nums2)) % 2:
        return (nums[(len(nums1) + len(nums2)) // 2] + nums[(len(nums1) + len(nums2)) // 2 - 1]) / 2
    else:
        return float(nums[(len(nums1) + len(nums2)) // 2])
