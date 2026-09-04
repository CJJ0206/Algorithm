"""
给你单链表的头节点 head ，请你反转链表，并返回反转后的链表。

输入：head = [1,2,3,4,5]
输出：[5,4,3,2,1]

这题leetcode底层帮我们构建好了链表了，所以这个输入输出可能看着有点不习惯
"""

from typing import Optional

# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
class Solution:
    def reverseList(self, head:Optional[ListNode]) -> Optional[ListNode]:
        pre , cur = None , head
        while cur:
            nxt = cur.next
            cur.next = pre

            pre = cur
            cur = nxt
        return pre

    def reverseList2(self, head:Optional[ListNode]) -> Optional[ListNode]:
        if not head or not head.next:           # 递归基：空链或单节点，反转后还是自己
            return head
        new_head = self.reverseList2(head.next) # ⭐ new_head 是全程不变的，只是保存这个新表头
        head.next.next = head                   # 让"后一段的尾节点"指回自己
        head.next = None                        # 自己变成新的尾，必须断链
        return new_head    

    """
    [1,2,3,4,5]
    节点5时触发ifz,返回节点5给new_head,只是作为找到新头的记录 和 给后面返回用
    然后回溯执行节点4,此时new_head = revertlist(4.next) 也就是5
    head.next.next = head  🔴也就是 5.next = 4 （这里就实现了反转了）
    head.next = None 然后要把原来的尾部置空，防止形成环
    """


