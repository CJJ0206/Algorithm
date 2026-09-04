from typing import Optional

"""
链表

先跑一个最小例子，建立手感

在看任何理论之前，先把一条链搭起来、反转它，肉眼看见指针是怎么"掉头"的。

"""

class ListNode:
    def __init__(self, val: int = 0, next = None):
        self.val = val
        self.next = next

def to_list(head):
    res = []
    while head:
        res.append(head.val)
        head = head.next  # 传递下去
    return res

if __name__ == "__main__":
    # 手工搭一条链 1 -> 2 -> 3
    n4 = ListNode(4)
    n3 = ListNode(3, n4)
    n2 = ListNode(2, n3)
    n1 = ListNode(1, n2)
    head = n1
    print("原始链表:", to_list(head))
    print("n1.next.val =", n1.next.val, " n2.next.val =", n2.next.val)

    # 反转：三指针 pre / cur / nxt  （previous\current\next）
    pre, cur = None, head
    step = 0            
    while cur:              # 从head开始处理，每处理完一位就右移继续，直到next为None的那个
        nxt = cur.next      # ① 先存原来的后继，否则改完指针就找不到后面了
        cur.next = pre      # ② 掉头(把cur的next指向pre)
                            # 处理完一对右移完后继续处理
        # ‼️‼️ 我逻辑有问题，这里的赋值操作pre = cur意思是把cur赋值到pre，相当于把pre右移到cur位置（不是左移），这相当于在挪指针位置
        pre = cur           # ③ pre 右移
        cur = nxt           # ④ cur 右移
        
        step += 1
        print(f"  第{step}步: pre链={to_list(pre)}  剩余cur链={to_list(cur)}")
    print("反转后:", to_list(pre))



"""
|val1|next| -> |val2|next| ...
反转要做的就是把 所有next反转指向前面


None        1  ------>  2  ------>  3
 ↑          ↑           ↑
pre        cur         nxt


None <----- 1           2  ------>  3
 ↑          ↑           ↑
pre        cur         nxt


None <----- 1           2  ------>  3
            ↑           ↑
           pre         cur
"""

