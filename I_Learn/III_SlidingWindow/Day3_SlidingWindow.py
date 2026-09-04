import sys
import os
import time

# 1. 拿到当前文件的绝对路径，并向上推两级，找到 I_Learn 文件夹
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(os.path.dirname(current_dir))

# 2. 把 I_Learn 文件夹的路径强行塞给 Python 的搜索雷达
sys.path.append(parent_dir)

# 3. 雷达升级完毕，现在可以正常跨文件夹导入了！
from II_Leetcode.Z_03 import Solution as Solution03
from II_Leetcode.Z_209 import Solution as Solution209


"""
最小例子：固定窗口求最大子段和
问题：nums = [2, 1, 5, 1, 3, 2]，窗口长度 k = 3，求长度为 3 的连续子数组中元素和最大是多少？


# II_Leetcode.Z_03 在这里实现了 
例题 1：LeetCode 3 — 无重复字符的最长子串
题目描述：给定字符串 s，找出其中不含有重复字符的最长子串的长度。
样例：
输入 s = "abcabcbb" → 输出 3（子串 "abc"）
输入 s = "bbbbb" → 输出 1（子串 "b"）
输入 s = "pwwkew" → 输出 3（子串 "wke" 或 "kew"；注意 "pwke" 不是连续子串）


例题 2：LeetCode 209 — 长度最小的子数组
题目描述：给定仅含正整数的数组nums与目标值target，找出和 ≥ target 的最短连续子数组长度；不存在则返回 0。
样例：
nums = [2,3,1,2,4,3], target = 7 → 输出 2（子数组 [4,3]）
nums = [1,4,4], target = 4 → 输出 1
nums = [1,1,1,1,1,1,1,1], target = 11 → 输出 0
"""
class solution():
    # 时间复杂度：O(Kn) 其实是可以忽略成O(n)的，但实际运行K大时就是会有速度差距
    def Sd(self,nums:list[int]) -> int:
        sum = 0
        for i in range(len(nums)-2):        # 会发现其实很难用一个通用k来维护
            left ,right = i , i + 2
            res = nums[left] + nums[right] + nums[left + 1]
            if res > sum:
                sum = res
        return sum 

    # 优雅写法:时间复杂度：O(n)
    def max_sum_of_k_window(self,nums, k):
        window_sum = sum(nums[:k])           # 第一个窗口的和（内置函数sum()）
        ans = window_sum
        for right in range(k, len(nums)):
            window_sum += nums[right]        # 右端点加上
            window_sum -= nums[right - k]    # 左端点减掉
            ans = max(ans, window_sum)
        return ans



if __name__ == "__main__":
    start_time = time.perf_counter()
    so = solution()
    print(so.Sd([2, 1, 5, 1, 3, 2]))
    end_time = time.perf_counter()
    print(f"代码运行耗时: {end_time - start_time:.6f} 秒")

    start_time = time.perf_counter()
    so = solution()
    print(so.max_sum_of_k_window([2, 1, 5, 1, 3, 2],3))
    end_time = time.perf_counter()
    print(f"代码运行耗时: {end_time - start_time:.6f} 秒")

    so2 = Solution03()
    print(so2.lengthOfLongestSubstring("abdfadsffga"))

    so209 = Solution209()
    print(so209.shortestLength([2,3,1,2,4,3], 7))
