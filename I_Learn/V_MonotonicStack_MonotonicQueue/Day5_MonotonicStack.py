import time 
import random

"""
先来一个最小例子（建立直觉）
问题：数组 a = [73, 74, 75, 71, 69, 72, 76, 73]，对每个位置回答：右边第一个比我大的数离我多远？
    myA: 暴力枚举
"""

class Solution():
    def HowFar_One(self,nums:list[int]) -> list[int]:
        length = len(nums)
        distance = []
        for i in range(length + 1):
            tag = True
            for j in range(i,length):
                if nums[j] > nums[i] and tag is True:
                    tag = False
                    distance.append(j-i)
                    break
                elif j == length-1:                     # 如果j到了最后还是一直没找到就返回0
                    distance.append(0)
        return distance


    # 用单调栈的方式做
    def HowFar_Two(self, nums: list[int]) -> list[int]:
        n = len(nums)
        res = [0] * n
        stack = []
        for i in range(n):
                                                        # ‼️在while里，i是不变的，但是pop_index会在while里一直出栈变化
            while stack and nums[i] > nums[stack[-1]]:  # 🟡 while stack不为空且当前元素大于栈顶元素
                top_index = stack.pop()                 # 🔴 pop 是有返回值的，返回的是被提出的元素的值
                res[top_index] = i - top_index          # 一定是对top索引对应位置算距离，不是往后append
                                                        # 🟣 栈里装的是索引
            stack.append(i)                             # FIXME append 插入数据是在已有的后面的，所以上面可以用-1
        return res
    """
    nums : head |4|3|2|6| tail
    stack: |4|||| -> |4|3||| -> |4|3|2|| -> |4|3|2||  6 -> 此时i=3,top_index依次为 2 1 0 
    """



if __name__ == "__main__":
    a = [random.randint(1,100) for _ in range(10000)]
    so = Solution()

    starttime = time.perf_counter()
    so.HowFar_One(a)
    endtime = time.perf_counter()
    usedtime = endtime - starttime
    print(usedtime)                                     # 0.04712130001280457  暴力枚举速度问题

    starttime = time.perf_counter()
    so = Solution()
    so.HowFar_Two(a)
    endtime = time.perf_counter()
    usedtime = endtime - starttime
    print(usedtime)                                     # 0.00238309998530894  一万个数字时，速度已经是20倍了

    b = [4,3,2,1,15,22,16]
    b.append(5)
    print(b)                                            # 🤡 可与看到b是插在后面的而不是在前面
    last = b.pop()                                      # POP 函数返回的是被剔除的元素值
    print(last)

    so = Solution()
    print(so.myself(b))



