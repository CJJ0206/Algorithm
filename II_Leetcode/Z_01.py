"""
给定一个整数数组 nums 和一个整数目标值 target，请你在该数组中找出和为目标值 target 的那两个整数，
并返回它们的数组下标。你可以假设每种输入只会对应一个答案，并且你不能使用两次相同的元素。
你可以按任意顺序返回答案。

示例 1：
输入：nums = [2,7,11,15], target = 9
输出：[0,1]
解释：因为 nums[0] + nums[1] == 9 ，返回 [0, 1] 。
"""

# FIXME 最优解，使用字典求解：时间复杂度O(n)
# 用时：3ms
class Solution:
    def twoSum(self, nums: list[int], target: int) -> list[int]:
        # 创建一个字典，用来“记住路过的人”:格式为 {数字: 对应的索引}
        seen = {} 
        
        for i, num in enumerate(nums): # (2) 遍历每个人
            complement = target - num # 计算当前数字需要的另一半
            
            # 多年后，才发现原来你早就在这里：检查另一半是否已经被我们记在字典里了
            if complement in seen:
                return [seen[complement], i] 
                # 把nums的值作为key，因为字典的遍历只有在查找key时能做到O(1)瞬时完成
            
            # 如果另一半不在，就把当前这个人和他的位置“记住”，存入字典，留给后面的人来找
            seen[num] = i 
        return []


# ----------------------------------------------------------------------------------------
# 暴力枚举：双循环解法
# 用时：4571ms
class Solution:
    def twoSum(self, nums: list[int], target: int) -> list[int]:
        for i in range(len(nums)):
            for j in range(len(nums)):
                if i != j and nums[i] + nums[j] == target:
                    return [i,j]

