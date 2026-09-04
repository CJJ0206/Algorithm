"""
给你一个链表，删除链表的倒数第 n 个结点，并且返回链表的头结点。

示例 1:
输入：head = [1,2,3,4,5], n = 2   输出：[1,2,3,5]

实例2：
输入：head = [1]   输出：n = 1
"""
from typing import Optional

# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
class Solution:
    # def removeNthFromEnd(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:
    #     cur = head
    #     length = 0

    #     while cur and cur.next:
    #         if length == n - 1:
    #             cur.next = cur.next.next
    #         cur = cur.next
    #         length += 1
    #     return head                         # 把头返回去就行，会自己遍历



    def removeNthFromEnd2(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:
        dummy = ListNode(0, head)         # 构造一个虚拟头节点
        length = 0                        # 由于节点的删除必须知道它前面的节点，否则就是使用if返回head.next
        cur = head
        while cur:
            length += 1                   # 第一个循环计算长度
            cur = cur.next
            
        cur = dummy                       # 把上面遍历的list重置回开头
        for _ in range(length - n):       # 遍历到len-n的位置跳出来处理一下
            cur = cur.next
            
        cur.next = cur.next.next
        return dummy.next                 # 跳过虚拟头输出处理后结果



    # 快慢指针完成（一次遍历：时间复杂度最低）
    def removeNthFromEnd3(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:
        dummy = ListNode(0, head)
        fast = slow = dummy
        
        for _ in range(n + 1):            # fast 先走 n + 1 步，拉开距离
            fast = fast.next              # 快指针先走n步，等他到终点了，慢指针正好到倒数第n个
            
        while fast:                       # 两个指针同速前进，直到 fast 出界
            fast = fast.next
            slow = slow.next
            
        slow.next = slow.next.next        # 此时 slow 刚好在目标节点的前一位
        return dummy.next





