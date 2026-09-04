"""
给你单链表的头指针 head 和两个整数 left 和 right ，其中 left <= right 。
请你反转从位置 left 到位置 right 的链表节点，返回反转后的链表。 
(这题是反转这个范围的内容不是换左右节点位置)
 
示例 1：
输入：head = [1,2,3,4,5], left = 2, right = 4
输出：[1,4,3,2,5]
"""
from typing import Optional

# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def reverseBetween(self, head: Optional[ListNode], left: int, right: int) -> Optional[ListNode]:
        dummy = ListNode(0,head)
        p0 = dummy

        # 走到待反转区间的前驱节点 (p0)
        for _ in range(left - 1):
            p0 = p0.next
            
        # 对区间内的节点进行反转（完全复用 206 题的双指针模板）
        pre = None
        cur = p0.next
        for _ in range(right - left + 1):
            nxt = cur.next
            cur.next = pre

            # 代码上看是左移，但是逻辑上是右移，pre右移到cur，cur右移到nxt
            pre = cur
            cur = nxt
            
        # 缝合两端
        p0.next.next = cur   # 区间原来的起点变成尾巴，连接后面的 cur
        p0.next = pre        # p0 连接反转后的新表头 pre
        
        return dummy.next


        
if __name__ == "__main__":
    so = Solution()
    so.reverseBetween()

