from collections import deque

"""
给定一个整数数组 nums 和一个滑动窗口的大小 k。窗口从数组的最左端移动到最右端，每次向右滑动 1 个位置。
你的任务是：返回每一个滑动窗口中的最大值。

示例：
    输入: nums = [1, 3, -1, -3, 5, 3], k = 3
    输出: [3, 3, 5, 5]

单调队列
"""

def maxSlidingWindowCollection(nums: list[int], k: int) -> list[int]:
    q = deque()                               # 存放元素下标，队列内数值保持单调递减
    ans = []
    # for i, x in enumerate(nums):
    for i in range(len(nums)):                # 这个while当遇到大的元素是会逐个比较逐个pop直到到比它大的元素
        while q and nums[i] >= nums[q[-1]] :  # 队尾淘汰：新来的数比队尾大（或相等），队尾永远没机会了，直接弹出
            q.pop()                           
        q.append(i)                           # q 里面只存当前有潜力的值，没潜力的直接就pop了
        if q[0] < i - k + 1:                  # 队首过期：当前窗口左边界是 i - k + 1，超出窗口的队首弹出
            q.popleft()
        if i >= k - 1:                        # 窗口达到 k 个元素后，才开始append最大值
            ans.append(nums[q[0]])            # 由于while会一次性全对比pop所以首位始终是当前最大的元素的索引
    return ans



def maxSlidingWindow(nums: list[int], k: int) -> list[int]:
    q = []                                         # q 里索引对应的元素一定是单调递减的
    ans = []
    head = 0                                       # 逻辑队首指针,用 list + head 指针模拟，避免 list.pop(0) 的内存搬迁
    for i, x in enumerate(nums):
        
        while len(q) > head and nums[q[-1]] <= x:  # 队尾操作不变
            q.pop()
        q.append(i) 
        if q[head] < i - k + 1:                    # 队首过期：不物理删除，直接将指针右移
            head += 1
        if i >= k - 1:                             # 这里需要等号（窗口刚凑齐，这里才开始append）
            ans.append(nums[q[head]])
    return ans


# 核心是怎么写代码，维护一个区间，做法是超过就丢弃，小于就pop，不是真要存k个在区间里
# 处理的其实是逻辑上的区间范围，数据pop光了都行，留着索引就可以；最容易混乱的就是这个q队列




if __name__ == "__main__":
    print(maxSlidingWindowCollection(nums = [1, 3, -1, -3, 5, 3], k = 3))
    print(maxSlidingWindow(nums = [1, 3, -1, -3, 5, 3], k = 3))
    print(max(nums = [1, 3, -1, -3, 5, 3], k = 3))
