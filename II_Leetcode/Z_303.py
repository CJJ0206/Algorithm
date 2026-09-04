"""
LeetCode 303. 区域和检索 - 数组不可变（前缀和入门必做题）
题目：
    给定一个整数数组 nums，处理以下类型的多个查询:
    计算索引 left 和 right （包含 left 和 right）之间的 nums 元素和 ，其中 left <= right
    实现 NumArray 类：
        NumArray(int[] nums) 使用数组 nums 初始化对象
        int sumRange(int left, int right) 返回数组 nums 中索引 left 和 right 之间的元素的总和
        包含 left 和 right 两点（也就是 nums[left] + nums[left + 1] + ... + nums[right] )
样例：
    输入：["NumArray","sumRange","sumRange","sumRange"]
        [[[-2,0,3,-5,2,-1]],[0,2],[2,5],[0,5]]
    输出：[null, 1, -1, -3]
"""

class NumArray:
    def __init__(self, nums: list[int]):
        self.pre = [0]*(len(nums) + 1)
        for i in range(len(nums)):
            self.pre[i+1] = self.pre[i] + nums[i]

    def sumRange(self, left: int, right: int) -> int:
        return self.pre[right + 1] - self.pre[left]
        # FIXME 有哨兵0时，这里右边界要加一
        # 没有哨兵时：left - 1



if __name__ == "__main__":
    num = NumArray([-2, 0, 3, -5, 2, -1])
    print(num.sumRange(0,2))


