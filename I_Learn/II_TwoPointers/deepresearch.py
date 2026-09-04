"""
FIXME 核心思路（排序 + 固定一数 + 对撞双指针）
    思路是最重要的，代码其实都很简单
"""

def ThreeSum(nums:list[int],target:int) -> int:
    nums.sort() # 需要先排序不然后面不好做
    print(nums)
    for i in range(len(nums)-1):
        start , left , right = i , i + 1 , len(nums) - 1 
        while left <= right:
            res = nums[start] + nums[left] + nums[right]
            if res == target:
                return i , left ,right
            elif res < target:
                left += 1
            else:
                right += 1


# FIXME 这里可以把python看作是go的struct，里面的self就是struct里的属性和方法
class ListNode: # 需要自定义一下链表class
    def __init__(self, x):
        self.val = x 
        self.next = None # 同样的属性通过后续的实例调用

class Solution:
    def hasCycle(self, head: ListNode | None) -> bool:
        if not head or not head.next:
            return False
            
        slow = head
        fast = head

        # 主要思路就是快慢指针，步长间隔为1，如果是环，一定会相遇
        while fast and fast.next:     # 有一个为假则结束（允许这种写法）
            slow = slow.next          # 慢指针走 1 步
            fast = fast.next.next     # 快指针走 2 步
            
            if slow == fast:
                return True
        return False


if __name__ == "__main__":
    print(ThreeSum([3,6,7,2,1,8,4,14],17))

    sol = Solution()

    # 测试用例 1：构造有环链表 3 -> 2 -> 0 -> -4 -> 2（回到节点 2）
    node1 = ListNode(3)              # 相当于go创建实例并直接赋值
    node2 = ListNode(2)
    node3 = ListNode(0)
    node4 = ListNode(-4)
    # next属性class定义为None，是通过手动指定指向位置赋值的
    node1.next = node2
    node2.next = node3
    node3.next = node4
    node4.next = node2  # 形成环
    print("测试 1（有环）：", sol.hasCycle(node1))  # 预期输出: True

    # 测试用例 2：构造无环链表 1 -> 2 -> None
    a = ListNode(1)
    b = ListNode(2)
    a.next = b
    print("测试 2（无环）：", sol.hasCycle(a))      # 预期输出: False

            