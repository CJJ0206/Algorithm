"""
将两个升序链表合并为一个新的 升序 链表并返回。新链表是通过拼接给定的两个链表的所有节点组成的。

输入：l1 = [1,2,4], l2 = [1,3,4]
输出：[1,1,2,3,4,4]
"""

from typing import Optional

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def mergeTwoLists(self, list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
        dummy = ListNode(0)                   # 这个dummy是个孤立的新节点，不是接在谁头上
        cur = dummy                           # cur 是个全新的链表
        
        while list1 and list2:                # 两个链表都没走到头时，比较大小并穿针引线
            if list1.val <= list2.val:
                cur.next = list1
                list1 = list1.next            # 对比过后仅仅把取用过的list右移一位，没有取用的不右移
            else:
                cur.next = list2
                list2 = list2.next
            cur = cur.next
                                        
        cur.next = list1 if list1 else list2  # 拼接剩余部分
        return dummy.next                     # 返回新链表的真实头节点


        
