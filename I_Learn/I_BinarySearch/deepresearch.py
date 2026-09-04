import math
"""
(LeetCode 34 题前半部分）给定按照非递减顺序(就是允许重复的升序)整数数组 nums，和目标值 target。
请找出给定目标值在数组中的第一个出现位置。如果数组中不存在目标值 target，返回 -1。


(LeetCode 875. 爱吃香蕉的珂珂）珂珂喜欢吃香蕉。这里有 n 堆香蕉，
第 i 堆中有 piles[i] 根香蕉。警卫将在 h 小时后回来。珂珂可以决定她吃香蕉的速度 k（根/小时）。
每个小时，她将会选择一堆香蕉，从中吃掉 k 根。
如果这堆香蕉少于k 根，她将吃掉这堆的所有香蕉，且这一小时内不会再吃更多的香蕉。
返回她可以在 h 小时内吃掉所有香蕉的最小速度 k。
"""


def TaskOne(nums:list[int],target:int) -> int :
    left,right = 0 , len(nums) - 1
    while left <= right: # 循环，到达条件会自己退出
        mid = (left + right) // 2 # 更新写在里面
        if nums[mid] == target:
            right = mid - 1  # 找到目标不返回，而把右边界压过来，继续往左逼近
        elif nums[mid] > target:
            right = mid - 1
        else:
            left = mid + 1
    # 循环结束后，left 就是第一个目标值的位置
    # 但要检查一下有没有越界，及对应位置到底是不是 target
    if left < len(nums) and nums[left] == target:
        return left
    return -1


def TaskTwo(piles: list[int], h: int) -> int:
    def get_hours(speed: int) -> int: # 计算吃完时间的辅助函数
        hours = 0
        for pile in piles:
            hours += math.ceil(pile / speed) # 向上取整函数
        return hours
    left, right = 1, max(piles) # FIXME 在所有可能速度中做二分
    while left <= right:
        mid = left + (right - left) // 2
        if get_hours(mid) <= h: # 通过辅助函数计算时间来判断
            right = mid - 1 # 速度达标，尝试找更小的速度逼近边界
        else:
            left = mid + 1  # 速度太慢导致超时，必须提速
    return left # 最终的 left 就是满足条件的最小速度


if __name__ == "__main__":
    num1 = [2,3,3,4,5,6,6,8]
    # piles = [3, 6, 7, 11], h = 8
    # piles = [30, 11, 23, 4, 20], h = 5
    # piles = [30, 11, 23, 4, 20], h = 6

    print(TaskOne(num1,6))
    print(TaskTwo(piles = [3, 6, 7, 11], h = 8))
    print(TaskTwo(piles = [30, 11, 23, 4, 20], h = 6))
   
