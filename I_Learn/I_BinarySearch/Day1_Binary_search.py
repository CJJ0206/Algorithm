"""
例题

> 题目描述（LeetCode 704. 二分查找）
> 给定一个 n 个元素有序的（升序）整型数组 nums 和一个目标值 target，
> 写一个函数搜索 nums 中的 target，如果目标值存在返回下标，否则返回 -1。

    示例 1：
    输入: nums = [-1, 0, 3, 5, 9, 12], target = 9
    输出: 4
    解释: 9 出现在 nums 中并且下标为 4

    示例 2：
    输入: nums = [-1, 0, 3, 5, 9, 12], target = 2
    输出: -1
    解释: 2 不存在 nums 中因此返回 -1
"""

### Go / Python 
def BinarySearch(nums: list[int], target: int) -> int:
    left, right = 0, len(nums) - 1 # 记录左右初始坐标

    # while left >= right: # 这样就可以处理降序了
    while left <= right:
        mid = (right + left) // 2 # 算出中间位置(使用的向下取整除法)
        if nums[mid] == target:
            return mid
        elif nums[mid] > target:
            right = mid - 1
        else:
            left = mid + 1
    return -1

# FIXME 通过不断折半，利用中值不断对比最后靠近答案（主要问题是要求输入 升序）

if __name__ == "__main__":
    nums = [0, 2, 6, 10, 11, 12, 15] 
    res = BinarySearch(nums, 10)
    print(res)

    # nums2 = [15, 12, 11, 10, 6, 2, 0]
    # res2 = BinarySearch(nums2, 10)
    # print(res2)