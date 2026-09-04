import time
import random


"""
前缀和 

先来一个最小例子（建立直觉）
问题：数组 a = [2, 1, 5, 1, 3, 2]（下标 0~5）
回答两个问题：
    1. 区间 [1, 4]（即 1+5+1+3）的和是多少？  这里只做了四次取值和相加
    2. 区间 [2, 3]（即 5+1）的和是多少？      这里是两次
如果放到数据量大的情况下，这种求和是会很慢的（约等于全遍历）


直接全局做一次所有位置的和表pre
区间 [1,4] 的和 = pre[5] - pre[1] = 12 − 2 = 10 ✅
区间 [2,3] 的和 = pre[4] - pre[2] = 9 − 3 = 6 ✅
关键发现：一次 O(n) 预处理之后，任何区间求和都只是一次减法，O(1)。这张表就叫前缀和数组。    
"""


class Solution():
    def prefix(self, nums: list[int], start_idx: int, end_idx: int):
        starttime = time.perf_counter()
        n = len(nums)
        # pre = []
        # 这里就是在构建前缀和数组，首元素为0!!
        pre = [0] * (n + 1) # 正常使用append是不用初始化的，但是我们不知append
        for i in range(n):
            pre[i + 1] = pre[i] + nums[i] # 这里直接复用前面算出来的值做加法 复杂度O(n) 0.00466 
            # pre.append(sum(nums[:i]))   # 这里如果使用sum的话，复杂度就又是O(n^2)了  6.2203
        endtime = time.perf_counter()
        time1 = endtime - starttime 
        print(time1)

        print(f"--- 准备查询区间 [{start_idx}, {end_idx}) 10万次 ---")

        t1_start = time.perf_counter()
        for j in range(100000): # 切片不包含 end_idx
            res = sum(nums[start_idx:end_idx])
        t1_end = time.perf_counter()
        print(f"暴力切片耗时: {t1_end - t1_start:.6f} 秒")

        t2_start = time.perf_counter()
        for k in range(100000):
            # 注意：pre[end_idx] - pre[start_idx] 刚好对应 nums[start_idx:end_idx] 的和
            res2 = pre[end_idx] - pre[start_idx]
        t2_end = time.perf_counter()
        print(f"前缀和查询耗时: {t2_end - t2_start + time1 :.6f} 秒")


if __name__ == "__main__":
    so = Solution()
    print("正在生成 5 万长度的测试数组...")
    big_nums = [random.randint(1, 100) for _ in range(50000)]
    
    # 模拟极端情况：查询一个跨度接近 9 万的大区间
    so.prefix(big_nums, 100, 30000)

    """
    FIXME 可以看到效果是十分牛逼的
    暴力切片耗时: 15.207839 秒
    前缀和查询耗时: 0.006448 秒
    """