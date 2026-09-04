"""
给你一个整数数组 nums 和一个整数 k ，请你统计并返回该数组中和为 k 的子数组的个数 。
子数组是数组中元素的连续非空序列。

示例 1：
输入：nums = [1,1,1], k = 2
输出：2
"""

class Solution:
    def subarraySum_One(self, nums: list[int], k: int) -> int:
        # 前缀和求出来，一个个往前减呗
        prefix = [0]*(len(nums) + 1)
        for i in range(len(nums)):
            prefix[i+1] = prefix[i] + nums[i]
        num = 0
        for j in range(len(nums) , -1 , -1):  # 把右值改为-1就可以运行到了
            for m in range(j-1, -1 ,-1):      # 日他爹左闭右开，0在开区间直接跳过了
                res = prefix[j] - prefix[m]
                if res == k:
                    num += 1
        return num 


    def subarraySum_Two(self, nums: list[int], k: int) -> int:
        count = 0        
        prefix_sum = 0   # 记录当前的前缀和
        
        # 核心：字典记录 {前缀和: 出现次数}
        # 初始化 {0: 1} 非常重要！它的意思是：在数组最开始、什么都没加的时候，前缀和 0 出现了 1 次。
        # 这样如果刚好 prefix_sum 本身就等于 k，(prefix_sum - k == 0) 就能被正确记录到。
        prefix_dict = {0: 1} 
        
        for num in nums:
            prefix_sum += num  
            target = prefix_sum - k # 通过target去计算这个差值
            if target in prefix_dict:
                count += prefix_dict[target]
            # FIXME 这行是核心逻辑，每一次的前缀和先到字典里找有没有记录，没有则返回0，有则次数加1
            prefix_dict[prefix_sum] = prefix_dict.get(prefix_sum, 0) + 1
            
        return count


if __name__ == "__main__":
    so = Solution()
    print(so.subarraySum_Two(nums = [1,2,3], k = 3))
    # nums 超长时会超时


    