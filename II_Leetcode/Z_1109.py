"""
这里有 n 个航班，它们分别从 1 到 n 进行编号。
有一份航班预订表 bookings ，表中第 i 条预订记录 bookings[i] = [firsti, lasti, seatsi] 
意味着在从 firsti 到 lasti （包含 firsti 和 lasti ）的 每个航班 上预订了 seatsi 个座位。
请你返回一个长度为 n 的数组 answer，里面的元素是每个航班预定的座位总数。

"""

class Solution:
    def corpFlightBookings(self, bookings: list[list[int]], n: int) -> list[int]:
        # 长度设为 n + 2 的原因：
        # 1. 题目航班从 1 开始编号，我们加个 0 索引让下标直接对齐，省去换算的麻烦。
        # 2. 如果有人一直坐到最后一站（第 n 站），他的下车点就是 n + 1 站，长度 n + 2 能防止数组越界。
        diff = [0] * (n + 2)
        
        # 遍历预订记录，构建差分数组 (O(1) 复杂度完成区间更新)
        for first, last, seats in bookings:  # FIXME for循环里直接解包并取值
            diff[first] += seats             # first 站：seats 人上车
            diff[last + 1] -= seats          # last 的下一站：seats 人下车
            
        # 根据差分数组计算前缀和，还原每个航班的真实座位数
        answer = []
        current_seats = 0
        for i in range(1, n + 1):
            # 前缀和，这里我们只需要最终结果，所以把中间值优化掉了
            current_seats += diff[i]    # 累加当前站的变化量
            answer.append(current_seats)
            
        return answer





