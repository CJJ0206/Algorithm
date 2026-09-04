"""
例题 2：LeetCode 209 — 长度最小的子数组
题目描述：给定仅含正整数的数组nums与目标值target，找出和 ≥ target 的最短连续子数组长度；不存在则返回 0。
样例：
nums = [2,3,1,2,4,3], target = 7 → 输出 2（子数组 [4,3]）
nums = [1,4,4], target = 4 → 输出 1
nums = [1,1,1,1,1,1,1,1], target = 11 → 输出 0
"""

class Solution():
    def shortestLength(self,nums:list[int],target:int) -> int:
        left = 0
        len_arr = []
        if sum(nums) < target:
            return 0
        # # 最短肯定从最大开始搜索吧，先排序
        # # 一直优先最大的呗
        # nums.sort(reverse=True) # 这里做的倒序
        # # 现在问题是如果第一轮找到了，一定是最小的吗，只能说大多数是，但是如果两层循环又跟暴力枚举没区别了O(n^2)
        # for start in range(len(nums)):
        #     for left in range(start,len(nums)):
        #         arr.append(nums[left])
        #         if sum(arr) >= target:
        #             min = len(arr)
        #             return len(arr)
        # return 0

        # for right in range(left,len(nums)):
        #     res = sum(nums[left:right+1])
        #     if res >= target:
        #         len_arr.append(right-left)
        #         left += 1
        # res = min(len_arr,default=0)
        # return res


        # ---------------------------------------------------------------------------------
        # FIXME 这个时间复杂度其实是O(n)，while其实没有做什么动作，只是根据索引拿数据，左右一直是单向的
        left = 0
        current_sum = 0
        min_len = float('inf')                            # 初始化为一个无限大的数
        for right in range(len(nums)):
            current_sum += nums[right]                    # 就是在已经满足的情况下左界收缩，右界不动
            while current_sum >= target:                  # 通过一个while收缩窗口：如果当前和满足条件，尝试不断缩小左边界
                min_len = min(min_len, right - left + 1)  # 更新最小长度
                current_sum -= nums[left]                 # 左指针指向的元素移出窗口，并更新和
                left += 1                                 # 左界不能再收缩之后再出去右移右界重复此操作
        return min_len if min_len != float('inf') else 0  # 如果min_len没变过，说明没有找到符合条件的子数组，返回 0
            
                

if __name__ == "__main__":
    so = Solution()
    print(so.shortestLength([2,3,1,2,4,3], 7))
    print(so.shortestLength([1,4,4], 4))
    print(so.shortestLength([1,1,1,1,1,1,1,1], 11))
    print(so.shortestLength([1,2,3,4,5], 12))
    print(so.shortestLength([2,16,14,15], 20))


