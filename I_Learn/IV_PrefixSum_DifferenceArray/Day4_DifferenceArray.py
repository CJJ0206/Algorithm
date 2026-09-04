import random
import time 

"""
差分数组

最小例子（建立直觉）：
假设你是一所学校的教务，手头有一份 10 万个学生的成绩单数组 a。
现在校长发话了，要进行 10 万次瞎折腾的操作，比如：
    第 1 次：把学号 100 到 50000 的学生，每人加 5 分。
    第 2 次：把学号 2000 到 80000 的学生，每人扣 3 分。
    ……执行 10 万次。

"""

class Solution():
    def BruteForce (self, nums: list[int]) -> float:
        starttime = time.perf_counter()
        # 将外层循环缩小到 10000 次，总计算量大约 6.3 亿次
        for _ in range(10000): 
            for j in range(101, 25001):
                nums[j] += 5              
            for j in range(2000, 40000):
                nums[j] -= 3
        endtime = time.perf_counter()
        return endtime - starttime

    def DifferenceArray(self, nums: list[int]) -> float:
        n = len(nums)
        diff = [0] * (n + 1)  # 初始化差分数组，全是 0。长度多 1 为了防止右边界出界
        
        starttime = time.perf_counter()
        # 模拟 10 万次瞎折腾，注意这里只有 O(1) 的复杂度！
        for _ in range(100000):
            # 这里意思只动开头结尾，通过开头结尾影响后面
            diff[101] += 5          # [101] 加一，这样只要往后累加，后面的所有数字就都加5了
            diff[50001] -= 5        # 由于只到50000，所以后面要再减5
            
            diff[2000] -= 3
            diff[80000] -= (-3) 
            
        for k in range(1, n):
            diff[k] += diff[k - 1]  # 核心就是这一次前缀和，把数字像多米诺骨牌传递，获得每一个位置的改变值

        for k in range(n):
            nums[k] += diff[k]      # 把计算好的修改量，一次性加回原数组 (这一步只需要遍历1次！)
            
        endtime = time.perf_counter()
        return endtime - starttime


if __name__ == "__main__":
    nums = [random.randint(1, 100) for _ in range(50000)]
    so = Solution()
    cost_time = so.BruteForce(nums)
    print(f"暴力破解耗时: {cost_time:.4f} 秒")  # 暴力破解耗时: 42.8359 秒

    # -------------------------------------------------------------------------------

    nums = [random.randint(1,100) for _ in range(100000)]
    so = Solution()
    print("差分数组耗时:", so.DifferenceArray(nums))  # 差分数组耗时: 0.0402341 秒

