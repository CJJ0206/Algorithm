"""
给你单链表的头结点 head ，请你找出并返回链表的中间结点。
如果有两个中间结点，则返回第二个中间结点。

输入：head = [1,2,3,4,5]
输出：[3,4,5]
解释：链表只有一个中间结点，值为 3 。
"""
from typing import Optional

# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
class Solution:
    # 错误答案  
    # def middleNode(self, head: Optional[ListNode]) -> Optional[ListNode]:
    #     # 快慢指针，速度分别为1/2，当快指针到达时，慢指针一定是在中点
    #     cur = head
    #     slow_cur = head
    #     while cur and cur.next:
    #         if not cur.next.next:
    #             cur = cur.next
    #             slow = slow_cur.next.next
    #         else:
    #             cur = cur.next.next
    #             slow = slow_cur.next
    #     return slow


    def middleNode2(self, head: Optional[ListNode]) -> Optional[ListNode]:
        slow = fast = head
        # 只要快指针还能走 2 步，就继续走
        while fast and fast.next:     # 出界只会有差一步的情况，这种情况下，永远会再执行一次，
                                      # 执行完之后，fast出界，low多走一步，这样就是第二个中点的位置
            slow = slow.next          # 慢指针走 1 步
            fast = fast.next.next     # 快指针走 2 步
        return slow





