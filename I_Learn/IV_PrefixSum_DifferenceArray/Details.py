"""
太棒了！把差分数组和前缀和结合在一起，正是很多大厂面试（比如美团、字节跳动）最喜欢考的“缝合怪”题型。

这种题目的标准流程是：先用“差分”进行多次极速的区间加减，然后通过一次“前缀和”还原出真实数据，
最后再对真实数据建立“前缀和”来应对无数次的区间求和查询。简而言之：差分操作 -> 求前缀和(还原真值) -> 
再次求前缀和(为了极速查询)。我们来虚构一道非常贴合实际的综合大题：《游乐园人流监控系统》。

🎢 示例题目：游乐园人流监控系统题目描述：游乐园有 N 个主题区域（编号 0 到 N-1）。
早晨开园时，每个区域已经有了一批初始游客，记录在 initial_crowd 中。在接下来的一小时内，
发生了 M 次旅行团的集体移动，每次记录为 [start, end, count]，表示从 start 到 end 区域，
每个区域都涌入了 count 名游客（如果为负，表示离开）。一小时后，移动结束，
园区主管开始不断向你提问：“第 L 个到第 R 个区域，现在总共有多少人？”
请你设计一个系统，极速处理所有的移动，并能瞬间回答主管的每一次查询。

"""

class ThemeParkSystem:
    def __init__(self, initial_crowd: list[int]):
        self.n = len(initial_crowd)
        
        # ========================================================
        # 阶段一：构建差分数组 (应对未来的区间加减)
        # ========================================================
        
        # 【🚨 差分易错点 1：忘记尾部哨兵】
        # FIXME 前缀和是头部哨兵，差分是尾部哨兵
        # 错误：self.diff = [0] * self.n 
        # 正确：必须是 n + 1，防末尾越界
        self.diff = [0] * (self.n + 1)
        
        self.diff[0] = initial_crowd[0]
        for i in range(1, self.n):
            self.diff[i] = initial_crowd[i] - initial_crowd[i - 1]
            
        self.prefix = []  # self.diff 准备就绪，self.prefix 稍后再建

    def update_crowd(self, start: int, end: int, val: int):
        """
        处理旅行团的区间移动 (时间复杂度 O(1))
        """
        self.diff[start] += val
        
        # 【🚨 差分易错点 2：下车点设错】
        # 错误：self.diff[end] -= val (把最后一站的人也给扣了)
        # 正确：影响在 end + 1 处才结束，哪怕 end = n-1，也有哨兵兜底！
        self.diff[end + 1] -= val  # 这就是哨兵的作用和前缀和的0是一样的

    def lock_and_build(self):
        """
        一小时后，停止移动。我们将差分还原为真实值，并马上建立前缀和用于查询。
        (时间复杂度 O(N))
        """
        # 1. 先用前缀和还原出真实的人数分布
        real_crowd = [0] * self.n
        
        # 【🚨 差分易错点 3：直接返回 diff 数组】
        # 错误：real_crowd = self.diff (差分只是相对变化量，必须求前缀和才是真值)
        real_crowd[0] = self.diff[0]
        for i in range(1, self.n):
            real_crowd[i] = real_crowd[i - 1] + self.diff[i]
            
        print(f"✅ 移动停止，当前各区域真实人数为: {real_crowd}")
        
        # ========================================================
        # 阶段二：针对真实数据，构建前缀和数组 (应对未来的区间查询)
        # ========================================================
        
        # 【🚨 前缀和易错点 1：忘记头部哨兵】
        # 错误：self.prefix = [0] * self.n
        # 正确：必须是 n + 1，第 0 位留个 0 当头部哨兵，防查开头时越界
        self.prefix = [0] * (self.n + 1)
        
        for i in range(self.n):
            # 注意下标错位：prefix[i+1] 存的是包含 real_crowd[i] 及之前的总和
            self.prefix[i + 1] = self.prefix[i] + real_crowd[i]
            
        print(f"✅ 前缀和构建完成 (带头部哨兵): {self.prefix}")

    def query_total(self, left: int, right: int) -> int:
        """
        回答主管的区间求和查询 (时间复杂度 O(1))
        """
        # 【🚨 前缀和易错点 2：查询时弄错哨兵偏移量】
        # 错误：return self.prefix[right] - self.prefix[left] 
        #      或者 return self.prefix[right+1] - self.prefix[left+1]
        # 正确：大面积(包含right) - 小面积(不包含left)，映射到加了哨兵的 prefix 就是 right+1 和 left
        return self.prefix[right + 1] - self.prefix[left]  # 因为有哨兵所以加一



if __name__ == "__main__":
    # 0 到 4 号区域，初始各有 100 人
    initial = [100, 100, 100, 100, 100]
    
    park = ThemeParkSystem(initial)
    
    # 发生多次区间人群移动 O(1)
    print("📢 旅行团开始移动...")
    park.update_crowd(0, 2, 50)   # 0,1,2 区域各进 50 人
    park.update_crowd(2, 4, -20)  # 2,3,4 区域各走 20 人 (尾部更新砸在哨兵上)
    
    # 主管要来查岗了，锁定数据，生成前缀和 O(N)
    park.lock_and_build()
    
    # 应对主管的无限次瞬间查询 O(1)
    print("📢 主管开始提问...")
    print(f"0 到 1 区域总人数: {park.query_total(0, 1)}")  # 应为 150+150 = 300
    print(f"2 到 4 区域总人数: {park.query_total(2, 4)}")  # 应为 130+80+80 = 290
    print(f"0 到 4 区域总人数: {park.query_total(0, 4)}")  # 应为 300+290 = 590

"""
算法时间线总结早晨初始化：通过 __init__ 花费 $O(N)$ 时间构建出差分数组。发生移动：无论多少次 update_crowd，
每次仅修改两个端点，花费 O(1) 时间。锁定结算：通过 lock_and_build 将差分还原并转化成前缀和，
花费 O(N) 时间。疯狂查询：通过 query_total 瞬间得到任何区间的总和，花费 $O(1)$ 时间。
如果没有这一套组合拳，遇到大量更新和大量查询时，普通的暴力循环会把时间复杂度拉长到可怕的 O(M x N)（M 是更新/查询次数，
N 是数组长度）。而现在，所有的操作被完美压榨到了物理极限。
"""
