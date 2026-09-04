"""
给定一个整数数组 temperatures ，表示每天的温度，返回一个数组 answer ，其中 answer[i] 是指对于第 i 天
下一个更高温度出现在几天后。如果气温在这之后都不会升高，请在该位置用 0 来代替。

示例 1:
    输入: temperatures = [73,74,75,71,69,72,76,73]
    输出: [1,1,4,2,1,1,0,0]
"""

class Solution:
    def dailyTemperatures(self, temperatures: list[int]) -> list[int]:
        n = len(temperatures)
        res = [0] * n
        stack= []

        """
        其实只要想到使用栈来实现就能想到大致的代码写法了

        逻辑是每进来一个数字都要与栈顶进行一次对比，然后才决定进或出
        所以代码的stack.append要在while这个对比过程外部外部的
        """
        for i in range(n):

            # ⭐ while 是单调栈的灵魂，不可或缺
            while stack and temperatures[i] > temperatures[stack[-1]]:
                top_index = stack.pop()
                res[top_index] = i - top_index

            stack.append(i) # 这个是在while外的
        return res


if __name__ == "__main__":
    so = Solution()
    print(so.dailyTemperatures([73,74,75,71,69,72,76,73]))


