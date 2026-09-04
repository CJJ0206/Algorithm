# Day 6 · 链表核心技巧

> **今日定位**：从「数组思维」切换到「指针思维」。
> 前五天我们操作的都是**数组**——下标即地址，随机访问 O(1)，脑子里的模型是"一排格子"。
> 今天开始操作**链表**——地址里存地址，只能顺着走，脑子里的模型是"一串钩子"。
> 链表本身不难，难的是**指针一旦乱掉就全盘皆输**。所以今天的核心不是"会不会"，而是**"每一步我手里握着谁"**。

---

## 〇、先跑一个最小例子，建立手感

在看任何理论之前，先把一条链搭起来、反转它，肉眼看见指针是怎么"掉头"的。

```python
from typing import Optional


class ListNode:
    def __init__(self, val: int = 0, next: Optional['ListNode'] = None):
        self.val = val
        self.next = next


def to_list(head):
    res = []
    while head:
        res.append(head.val)
        head = head.next
    return res


# 1) 手工搭一条链 1 -> 2 -> 3
n3 = ListNode(3)
n2 = ListNode(2, n3)
n1 = ListNode(1, n2)
head = n1
print("原始链表:", to_list(head))
print("n1.next.val =", n1.next.val, " n2.next.val =", n2.next.val)

# 2) 反转：三指针 pre / cur / nxt
pre, cur = None, head
step = 0
while cur:
    nxt = cur.next      # ① 先存后继，否则改完指针就找不到后面了
    cur.next = pre      # ② 掉头
    pre = cur           # ③ pre 前移
    cur = nxt           # ④ cur 前移
    step += 1
    print(f"  第{step}步: pre链={to_list(pre)}  剩余cur链={to_list(cur)}")
print("反转后:", to_list(pre))
```

<details>
<summary>运行结果</summary>

```
原始链表: [1, 2, 3]
n1.next.val = 2  n2.next.val = 3
  第1步: pre链=[1]  剩余cur链=[2, 3]
  第2步: pre链=[2, 1]  剩余cur链=[3]
  第3步: pre链=[3, 2, 1]  剩余cur链=[]
反转后: [3, 2, 1]
```

</details>

三件事请记住，它们会贯穿今天所有题目：

1. **没有全局变量 head 会变**——函数里的 `head` 只是一个局部指针变量，你改 `head` 不影响调用方，但改 `head.next` 会真实改链表。
2. **`cur.next = pre` 之前必须先存 `nxt`**——一旦箭头改了，原来的后继节点就永久丢失了。这是链表第一大坑。
3. 反转结束后，**新的头是 `pre`，不是 `cur`**（此时 `cur` 已经是 `None`）。

---

## 一、算法核心思想

### 1.1 链表的本质：拿「连续内存」换「O(1) 改结构」

| 维度 | 数组（Array） | 链表（Linked List） |
|------|--------------|-------------------|
| 内存布局 | 连续 | 离散，靠指针串起来 |
| 访问第 i 个 | **O(1)**（基址 + i×步长） | **O(n)**（必须从头走） |
| 已知位置时插入/删除 | O(n)（要搬移元素） | **O(1)**（改两个指针） |
| 查找某值 | O(n)（可二分则 O(log n)） | O(n)（**不能二分**） |
| 额外空间 | 无 | 每节点多一个指针域 |
| CPU 缓存 | 友好（预读连续内存） | 不友好（随机跳转） |

**一句话总结**：数组赢在"**查**"，链表赢在"**改**"。
所以链表题几乎全是"**结构调整题**"——反转、重排、合并、删除、判环；而"查找最值 / 统计频次"这类题，链表天生吃亏。

> **工程视角补充**：正因缓存不友好，现实中链表（尤其单向链表）用得比数组少得多。
> 但它是 LRU 缓存、邻接表、哈希桶拉链、内核任务队列、内存分配器 free list 的底层结构，
> 也是**二叉树、图**的"指针思维"前置训练。学它，一半是为了做题，一半是为了练手。

### 1.2 五件套武器库（今日全部技能点）

链表题看似千变万化，真正的核心武器只有这五件。**吃透这五个模板，95% 的链表题都是它们的组合。**

| # | 武器 | 解决什么问题 | 代表题 |
|---|------|------------|--------|
| 1 | **虚拟头节点 dummy** | 头节点可能被删/被改，导致无法统一处理 | LC 19、LC 21、LC 203 |
| 2 | **快慢指针** | 中点、倒数第 k、判环、找环入口 | LC 876、LC 19、LC 141/142 |
| 3 | **三指针原地反转** | 整体反转、局部反转、K 个一组 | LC 206、LC 92、LC 25 |
| 4 | **递归思维** | 把链表看成「一个头 + 一条更短的链表」 | LC 206、LC 21、LC 24 |
| 5 | **穿针引线（指针手术）** | 拆链、断链、重接、交叉合并 | LC 92、LC 143、LC 148 |

下面逐个展开。

#### ① 虚拟头节点 dummy —— 消灭「头节点特判」

**痛点**：删除节点需要拿到**前驱**。但头节点没有前驱，于是你不得不写：

```python
if head.val == target:      # 特判头节点
    return head.next
# 下面才是通用逻辑……
```

**解法**：在真正的头前面**钉一个假的头**。`dummy.next = head`，然后从头到尾用**同一套逻辑**遍历。
无论真正的头被删多少次，你返回的永远是 `dummy.next`，而 `dummy` 本身永不动。

```
dummy -> 1 -> 2 -> 3 -> None
  ↑
 永不移动，永远安全
```

**口诀**：**只要题目涉及"删除"或"头节点可能变化"，一律先上 dummy。**

#### ② 快慢指针 —— 用相对速度差量出距离

让两个指针**同时出发、速度不同**，它们的**间距**就会变成一把"尺子"。

- **速度 1 : 2** → 快指针到终点时，慢指针正好在**中点**。
- **固定间距 k** → 快指针到终点时，慢指针正好在**倒数第 k 个**。
- **速度 1 : 2 且有环** → 二者必然**相遇**（判环），且能反推**环入口**。

这是 Day 2「双指针」思想在链表上的**直接复用**——区别只在于，数组里指针靠下标移动，链表里靠 `.next` 移动。

#### ③ 三指针原地反转 —— `pre / cur / nxt`

就是第〇节那个例子。**循环不变量**：

> **每一轮循环开始前**：`pre` 是已反转部分的头，`cur` 是待反转部分的头，**`pre` 与 `cur` 之间的连接是断开的**。

四步曲顺序**不能乱**：`存 nxt → 改 cur.next → pre 前移 → cur 前移`。

#### ④ 递归思维 —— 「一个头 + 一条更短的链表」

链表的**递归定义**：一条链表 = 一个头节点 + 一条更短的链表。
于是"反转整条链"可以写成：

> 先把 `head.next` 之后的部分反转好（**假设子问题已解决**），
> 再把 `head` 接到反转后子链表的**尾部**。

这个"**先假设子问题已解决，再处理当前节点**"的套路，是明天 Day 7「二叉树与递归」的**完全同构**版本。
**今天把 LC 206 / LC 21 的递归写法想透，明天的树形递归会省力一半。**

#### ⑤ 穿针引线 —— 先拆后接，永远先存后继

复杂重排题（反转局部、K 个一组、重排链表）本质是"拆成几段 → 各自处理 → 按新顺序接回去"。
铁律三条：

1. **改任何指针前，先把会被覆盖的后继存进临时变量。**
2. **拆段时必须断链**（把段尾的 `.next` 置为 `None`），否则会形成环，遍历时死循环。
3. **接回去之前先在纸上画一遍**，确认每个节点的 `next` 都被赋过值（没赋值的会保持原指向，产生野指针）。

### 1.3 一条贯穿始终的心法

> **链表题不考智商，考的是"你有没有在脑子里/纸上维护住这张指针图"。**

具体做法（强烈建议初学者照做）：

- 在纸上画出**当前**的箭头状态，每改一次箭头就**重画一次**。
- 改指针前，问自己三个问题：
  1. **我现在握着哪个节点？**
  2. **改完这个 `.next` 之后，原来的后继还有没有别的引用能找到它？**
  3. **这条链会不会因此断掉 / 成环？**

---

## 二、复杂度分析与原因推导

### 2.1 基础操作复杂度总表

| 操作 | 时间复杂度 | 空间复杂度 | 原因 |
|------|-----------|-----------|------|
| 遍历一次 | O(n) | O(1) | 每个节点访问一次 |
| 按值查找 | O(n) | O(1) | 无法随机访问，必须顺序扫描 |
| 已知前驱，插入 / 删除 | **O(1)** | O(1) | 只改 2 个指针，不搬移数据 |
| 未知位置，删除第 i 个 | O(n) | O(1) | 时间花在**定位**上，不在删除上 |
| 迭代反转整链 | O(n) | **O(1)** | 每节点改一次 `next`，只用 3 个指针变量 |
| 递归反转整链 | O(n) | **O(n)** | 递归深度 = n，每层占用一个栈帧 |
| Floyd 判环 / 找入口 | O(n) | **O(1)** | 见 2.3 推导 |
| 快慢指针找中点 | O(n) | O(1) | 快指针走 n 步，慢指针走 n/2 步，合计 O(n) |
| 合并两条有序链 | O(m+n) | O(1)（原地重接） | 每次比较淘汰一个节点，共淘汰 m+n 个 |
| 链表归并排序（自顶向下） | O(n log n) | O(log n) | 递归深度 log n |
| 链表归并排序（自底向上） | O(n log n) | **O(1)** | 无递归，只有常数个指针 |

### 2.2 为什么反转是 O(n) 时间、O(1) 空间？

**时间 O(n)**：每个节点恰好被"掉头"一次（`cur` 从 `head` 一路走到 `None`，走 n 步），每步是常数操作 → O(n)。

**空间 O(1)**：我们**没有新建任何节点**，只是**修改已有节点的 `next` 指向**。全程只用了 `pre / cur / nxt` 三个指针变量，与 n 无关 → O(1)。

**对比递归版为什么是 O(n) 空间**：
递归调用 `reverseListRec(head.next)` 会一直压栈到链表尾部才返回，**栈深度 = 链表长度 n**，每层栈帧保存 `head` 和 `new_head` 两个局部变量 → O(n)。
**结论**：能迭代就迭代；递归版的价值在于**训练递归思维**（为明天做准备），不是性能更优。

**额外提醒**：Python 默认递归深度约 1000，链表长度超过 990 左右递归会抛 `RecursionError`。**生产代码请一律用迭代版。**

### 2.3 Floyd 判环：为什么一定相遇？为什么从头走能找到入口？

这是链表里**唯一需要真正推导**的算法，务必吃透，面试高频。

**设定**：
- 头节点到环入口的距离 = `a`
- 环的长度 = `b`
- slow 每次走 1 步，fast 每次走 2 步

**问题一：为什么一定会相遇？**

一旦 slow 进入环，fast 早已在环内（fast 更快）。此时把 slow 看作参照物，**fast 相对于 slow 每轮前进 1 步**。
两者的相对距离最大为 `b - 1`，且每轮减 1，所以**最多 b 轮必然追上**。
fast 不可能"跳过" slow——因为相对速度是 1，距离是逐个递减的整数。

**问题二：为什么相遇后，从头节点再走一个指针就能在入口相遇？**

设相遇时 slow 走了 `s` 步，则 fast 走了 `2s` 步。
fast 比 slow 多走的路程 = `2s - s = s`，而多走的这部分**恰好是环长的整数倍**（fast 在环里绕了若干圈才追上），所以：

$$s = k \cdot b \quad (k \text{ 为正整数})$$

slow 落在环内的位置（相对入口的偏移）为：

$$(s - a) \bmod b = (k \cdot b - a) \bmod b = (-a) \bmod b$$

也就是说：**从相遇点继续往前走 `a` 步（mod b 意义下），恰好回到环入口。**

而**从头节点走 `a` 步，也恰好是环入口**（这就是 `a` 的定义）。

所以：让一个指针 `p` 从**头节点**出发，另一个指针 `slow` 从**相遇点**出发，**两者同速（每次 1 步）**，它们必然在**环入口**相遇。

> **边界验证**：若 `a = 0`（整条链就是一个环），则第一次相遇点就是入口，此时 `p` 和 `slow` 一开始就重合，循环 0 次直接返回，逻辑依然自洽。

### 2.4 为什么链表排序用「归并」而数组用「快排」？

| | 归并排序 | 快速排序 |
|---|---------|---------|
| 核心操作 | 合并两个**有序**序列 | 按 pivot **分区** |
| 数组 | 需要 O(n) 辅助数组 | **原地分区，O(1) 额外空间** ✅ |
| 链表 | **只需改指针，O(1) 额外空间** ✅ | 需要双向遍历找 pivot，实现复杂，且退化为 O(n²) 风险高 |

**结论**：
- 数组：**快排**更省空间（原地分区）。
- 链表：**归并**更自然（合并 = 改指针，天生 O(1) 空间），且**稳定**、**最坏也是 O(n log n)**。
- 顺带一提：数组用归并需要 O(n) 辅助空间；链表用归并可以做到 O(1)（自底向上版）。

**为什么链表快排难做**：快排的 `partition` 依赖**首尾双向扫描 + 随机访问交换**，单链表既不能回退也不能 O(1) 定位，实现起来非常别扭。

### 2.5 一个容易被忽略的点：缓存局部性（Cache Locality）

数组元素在内存中**连续**，CPU 会把相邻的 64 字节（一个 cache line）**一次性预读**进缓存，所以遍历数组几乎是"免费"的连续访问。
链表节点是 `new` 出来的，**地址随机分布**，每访问一个节点都可能 **cache miss**，要从内存重新加载。

**实测经验**：在 n = 10⁵ 量级，同样的遍历，链表可能比数组慢 **2～5 倍**。
这也是为什么现代语言标准库（如 C++ `std::list`）在很多场景下反而打不过 `std::vector`。

> **做题启示**：如果一道题既可以用数组也可以用链表，且需要频繁按位置访问——**选数组**。链表只在"频繁在中间插入/删除"或"题目强制给链表"时才真正占优。

---

## 三、核心模板与边界细节

### 3.1 模板一：dummy 虚拟头节点（删除类通用骨架）

```python
def removeElements(head, val):        # LC 203：删除所有值等于 val 的节点
    dummy = ListNode(0, head)         # ① 造一个假头，钉在真头前面
    cur = dummy
    while cur.next:                   # ② 只看 cur.next，就能统一处理"删头"的情况
        if cur.next.val == val:
            cur.next = cur.next.next  # ③ 删除：跳过它
        else:
            cur = cur.next           # ④ 只有不删时才前进
    return dummy.next                 # ⑤ 返回假头的下一个，永远是"新真头"
```

**关键细节（初学者最常写错的一行）**：
`cur = cur.next` 必须放在 **`else` 分支**里。
如果写成 `if ...: cur.next = cur.next.next` 然后无条件 `cur = cur.next`，当连续出现两个待删节点时，第二个会被漏掉。

错误示范（会漏删连续目标）：

```python
while cur.next:
    if cur.next.val == val:
        cur.next = cur.next.next
    cur = cur.next      # ❌ 删除后立刻前进，会跳过新接上来的节点
```

### 3.2 模板二：反转（迭代 + 递归双版本）

**迭代版（工程首选，O(1) 空间）**

```python
def reverseList(head):
    pre, cur = None, head
    while cur:
        nxt = cur.next   # ① 存后继
        cur.next = pre   # ② 掉头
        pre = cur        # ③ pre 前移
        cur = nxt        # ④ cur 前移
    return pre           # ⑤ 注意返回 pre，不是 cur（cur 已是 None）
```

**递归版（思维训练，为 Day 7 铺垫）**

```python
def reverseListRec(head):
    if not head or not head.next:   # 递归基：空链或单节点，反转后还是自己
        return head
    new_head = reverseListRec(head.next)  # 假设：后面那段已经反转好了
    head.next.next = head                 # 让"后一段的尾节点"指回自己
    head.next = None                      # 自己变成新的尾，必须断链
    return new_head                       # 新头一路向上传递
```

**递归版最烧脑的一行是 `head.next.next = head`。** 拆开看：

- 进入这一行时，`head.next` 还是**原链表中 head 的后继**（它在下层递归里已经被反转到子链表的**尾部**了）。
- 所以 `head.next.next = head` 的含义是：**"让我的原后继，反过来指向我"**。
- 然后 `head.next = None` 是**必须的**：head 现在是整条链的尾巴，不清空就会形成环。

**循环不变量（迭代版）**：

> 每轮开始前，`pre` 指向"已反转段"的头，`cur` 指向"待反转段"的头，两段之间**连接断开**（`pre` 那条链的尾部 `next` 是原来的 `None` 或已改好）。

### 3.3 模板三：快慢指针四变体（一张表背下来）

这是**最容易记混**的地方，务必对照这张表：

| 目标 | 初始化 | 循环条件 | n=4（1,2,3,4）落点 | n=5 落点 |
|------|--------|---------|-------------------|---------|
| **后中点**（偏右，LC 876） | `slow = fast = head` | `while fast and fast.next` | 第 **3** 个 | 第 3 个 |
| **前中点**（偏左，切链用） | `slow = head; fast = head.next` | `while fast and fast.next` | 第 **2** 个 | 第 3 个 |
| **倒数第 k 个节点** | `slow = fast = head`；fast 先走 k 步 | `while fast` | k=2 → 节点 3 | — |
| **删除倒数第 n 个** | `slow = fast = dummy`；fast 先走 n+1 步 | `while fast` | slow 停在待删的**前一个** | — |

**为什么只改 `fast` 的初始化，中点就从"后"变成"前"了？**
因为循环结束的判定是"`fast` 走不动了"。把 `fast` 的起点往后挪一格，它就**提前一步**走不动，于是 `slow` 也**少走一步** → 落点前移一位。

**什么时候用前中点、什么时候用后中点？**

- **后中点**（LC 876 题目明确要求）：偶数长度时返回**靠右**那个。
- **前中点**：当你需要把链表**切成两半**时（归并排序、回文链表、重排链表）。切成两半需要拿到"前半段的尾"，而前中点正好就是它——切完直接 `slow.next = None` 就断了。

**倒数第 k 的距离推导**：fast 先走 k 步后，fast 与 slow 之间**相隔 k 个节点**。此后二者同速前进，当 fast 走到 `None`（越过尾节点）时，slow 距离尾节点恰好 k-1 个位置，即 slow 就是**倒数第 k 个**。

### 3.4 模板四：区间反转 [left, right]（头插法）

LC 92 要求只反转第 `left` 到 `right` 个节点。有两种写法：

**写法 A（推荐）：头插法 —— 一次遍历，O(1) 空间**

```python
def reverseBetween(head, left, right):
    dummy = ListNode(0, head)
    pre = dummy
    for _ in range(left - 1):
        pre = pre.next          # pre 停在"待反转段的前一个"，全程不动
    cur = pre.next              # cur 是"待反转段的头"，反转后会变成段尾，也全程不动
    for _ in range(right - left):
        nxt = cur.next          # 抓住 cur 后面的那个节点
        cur.next = nxt.next     # ① cur 跳过 nxt
        nxt.next = pre.next     # ② nxt 插到段首
        pre.next = nxt          # ③ pre 改指 nxt
    return dummy.next
```

**理解要点**：`pre` 和 `cur` **从头到尾不动**，每轮把 `cur` 后面的节点**摘下来插到 `pre` 后面**。
这叫**头插法**——循环 `right - left` 次，就把中间那段整个"翻"过来了。

**写法 B：穿针引线 —— 拆成三段再拼回去**

```
dummy -> [1] -> [2->3->4] -> [5] -> None
          ^      ^      ^      ^
         pre    cur    right   tail
```
四步：① 找到 `pre / leftNode / rightNode / tail` 四个关键点 → ② 断开 `pre.next = None` 和 `rightNode.next = None` → ③ 反转中间段 → ④ `pre.next = rightNode; leftNode.next = tail`。

写法 B 代码更长但**更不容易出错**，初学者建议先写 B，理解后再改用 A。

### 3.5 模板五：有序链表合并（迭代 + 递归）

**迭代版（dummy + 尾插）**

```python
def mergeTwoLists(l1, l2):
    dummy = cur = ListNode(0)
    while l1 and l2:
        if l1.val <= l2.val:
            cur.next = l1
            l1 = l1.next
        else:
            cur.next = l2
            l2 = l2.next
        cur = cur.next
    cur.next = l1 if l1 else l2   # 剩下的整段直接接上（已有序）
    return dummy.next
```

**递归版（极简，三行核心）**

```python
def mergeTwoListsRec(l1, l2):
    if not l1: return l2
    if not l2: return l1
    if l1.val <= l2.val:
        l1.next = mergeTwoListsRec(l1.next, l2)
        return l1
    l2.next = mergeTwoListsRec(l1, l2.next)
    return l2
```

**递归版的逻辑**："两条链的头，谁小谁当新头；新头的 `next` = 剩下那些节点的合并结果。"
注意这里**不需要 `dummy`**，因为递归天然处理了"某一方为空"的边界。

**细节提醒**：`cur.next = l1 if l1 else l2` 不能写成 `cur.next = l1 or l2`。
在 Python 里，`l1 or l2` 依赖对象的布尔值——`ListNode` 默认 truthy，**恰好能work**，
但如果给 `ListNode` 定义了 `__bool__` 或 `__len__`（比如 LeetCode 某些变体），就会出诡异 bug。**用 `if...else` 显式判断更稳。**

### 3.6 模板六：自底向上归并排序（O(1) 空间排链表）

LC 148 要求 O(n log n) 时间、**O(1) 额外空间**。思路：**不要递归切分，改成"先 1 个 1 个合并，再 2 个 2 个合并，再 4 个 4 个……"**

```python
def cut(head, n):        # 切下前 n 个节点，返回剩余部分的头
    p = head
    while p and n > 1:
        p = p.next
        n -= 1
    if not p:
        return None     # 不够 n 个，说明后面没了
    nxt = p.next
    p.next = None       # ⚠️ 必须断链！否则段与段之间还连着，会死循环
    return nxt


def sortList(head):
    n, p = 0, head
    while p:                       # ① 先数长度
        n += 1
        p = p.next
    dummy = ListNode(0, head)
    step = 1
    while step < n:                # ② 段长倍增：1, 2, 4, 8, ...
        cur, tail = dummy.next, dummy
        while cur:                 # ③ 每轮扫描全链，两两合并
            left = cur
            right = cut(left, step)             # 切左段
            cur = cut(right, step) if right else None   # 切右段
            tail.next = mergeTwoLists(left, right)
            while tail.next:       # ④ tail 移到合并后段的末尾
                tail = tail.next
        step <<= 1
    return dummy.next
```

**三个致命细节**：
1. `cut` 里**必须 `p.next = None`** 断链，否则合并时会顺着旧指针绕回去。
2. `cut(right, step) if right else None` —— **不能对 `None` 调 `cut`**，会 `AttributeError`。
3. 每轮结束后 `tail` 必须走到**已合并段的末尾**，否则下一轮的 `tail.next = ...` 会把刚排好的段覆盖掉。

### 3.7 易错点清单（做题前扫一眼，能省 30 分钟调试）

| # | 易错点 | 后果 | 正确做法 |
|---|--------|------|---------|
| 1 | 改 `cur.next` 前没存后继 | 后继节点永久丢失 | 先 `nxt = cur.next` |
| 2 | 反转后返回 `cur` | 返回 `None` | 返回 `pre` |
| 3 | 递归反转忘了 `head.next = None` | 链表成环，遍历死循环 | 尾节点必须断链 |
| 4 | 删除节点后无条件前进 | 漏删连续目标节点 | 只在 `else` 里前进 |
| 5 | 该用 dummy 却没用 | 删头节点时崩溃或逻辑分叉 | 涉及删除/头节点变化，一律 dummy |
| 6 | 前后中点写混 | 切链位置错一位 | 对照 3.3 的表格 |
| 7 | `while fast.next` 漏了 `fast` | 无环时 `AttributeError` | 写 `while fast and fast.next` |
| 8 | 判断环用 `slow == fast` | 若节点定义了 `__eq__` 会出错 | 用 `is` 比较**身份** |
| 9 | Python 递归层数 > 1000 | `RecursionError` | 长链表用迭代版 |
| 10 | 段切分后不断链 | 新旧指针交织，死循环 | `p.next = None` |

---

## 四、经典实战例题

### 例题 1 · LC 206 反转链表（必做，基础中的基础）

**题目**：给你单链表的头节点 `head`，请你反转链表，并返回反转后的链表。

**样例**
- 输入：`head = [1,2,3,4,5]`
- 输出：`[5,4,3,2,1]`
- 进阶：链表可以选用迭代或递归完成。你能否用两种方法解决？

**思路**

迭代法已在第〇节演示。核心是三指针 `pre / cur / nxt`，每轮做四件事：存后继、掉头、pre 前移、cur 前移。

递归法的关键是**"先假设子问题已解决"**：

```
原链:  1 -> 2 -> 3 -> None
                └─ 假设这段已经反转成 3 -> 2

现在要让 1 接到 2 的后面：
  2.next = 1     （写作 head.next.next = head，因为此时 head.next 还是 2）
  1.next = None  （1 变成新尾，必须断链）

结果:  3 -> 2 -> 1 -> None
```

**复杂度**：时间 O(n)（每节点处理一次）；迭代空间 O(1)，递归空间 O(n)（递归栈）。

---

### 例题 2 · LC 876 链表的中间结点（快慢指针入门）

**题目**：给你单链表的头结点 `head`，请你找出并返回链表的中间结点。
如果有两个中间结点，则返回**第二个**中间结点。

**样例**
- 输入：`head = [1,2,3,4,5]` → 输出：`[3,4,5]`
- 输入：`head = [1,2,3,4,5,6]` → 输出：`[4,5,6]`

**思路**

让 `fast` 每次走 2 步、`slow` 每次走 1 步。`fast` 到终点时，`slow` 走的路程恰好是 `fast` 的一半 → 落在中点。

- **初始化 `slow = fast = head`** → `fast` 走不动时 `slow` 落在**后中点**（偶数长度时偏右），符合本题要求。
- 若需要**前中点**（切链用），改成 `slow = head; fast = head.next`。

对照 3.3 表格即可，一分钟写完。

**复杂度**：时间 O(n)（两指针合计走 1.5n 步）；空间 O(1)。

---

### 例题 3 · LC 19 删除链表的倒数第 N 个结点（dummy + 固定间距）

**题目**：给你一个链表，删除链表的倒数第 `n` 个结点，并且返回链表的头结点。
**进阶**：你能尝试使用一次扫描实现吗？

**样例**
- 输入：`head = [1,2,3,4,5], n = 2` → 输出：`[1,2,3,5]`
- 输入：`head = [1,2], n = 1` → 输出：`[1]`

**思路**

用 `dummy` 打底，`fast` 从 dummy 出发**先走 `n+1` 步**，使 `fast` 与 `slow` 之间**隔着 n 个节点**。
之后二者同速前进，当 `fast` 变成 `None` 时，`slow` 恰好停在**待删节点的前一个**。

```
dummy -> 1 -> 2 -> 3 -> 4 -> 5 -> None
  ↑slow             ↑fast        （n=2，fast 领先 3 步）
         └─ 中间隔着 3、4、5 三个节点 ─┘
```

同步前进两轮后：

```
dummy -> 1 -> 2 -> 3 -> 4 -> 5 -> None
              ↑slow             ↑fast is None
```

执行 `slow.next = slow.next.next` 删掉 4。

**为什么是 n+1 步而不是 n 步？**
因为我们要停在**待删节点的前一个**（需要前驱才能删）。fast 领先 n+1 步，fast 走到 None 时，slow 后面还隔着 n 个节点中的最后一个 —— 即 slow 是第 n+1 个的前驱。

**复杂度**：时间 O(n)（一次扫描）；空间 O(1)。

**边界**：`n` 等于链表长度时删除的是头节点 —— 有 `dummy` 就完全不用特判。

---

### 例题 4 · LC 141 环形链表 + LC 142 环形链表 II（Floyd 算法）

**题目（141）**：给你一个链表的头节点 `head`，判断链表中是否有环。

**题目（142）**：给定一个链表的头节点 `head`，返回链表开始入环的第一个节点。如果链表无环，则返回 `null`。

**样例（142）**
- 输入：`head = [3,2,0,-4], pos = 1`（尾节点连接到第 2 个节点）
- 输出：返回索引为 1 的链表节点（值为 2）

**思路**

**第一步（141，判环）**：快慢指针，快走 2 步慢走 1 步。**有环必相遇，无环则 fast 先撞到 `None`。**

**第二步（142，找入口）**：相遇后，把一个指针 `p` 放回**头节点**，另一个留在**相遇点**，**二者同速（各走 1 步）**，再次相遇处就是**环入口**。

推导见 §2.3。核心结论：

$$s = k \cdot b \quad\Rightarrow\quad \text{从相遇点走 } a \text{ 步} = \text{从头走 } a \text{ 步} = \text{环入口}$$

**复杂度**：时间 O(n)（判环最多 b 轮相遇，找入口最多 a 步）；空间 O(1)。

**边界**：
- 整条链是环（`a = 0`）：第一次相遇点就是入口，第二个 `while` 循环 0 次直接返回。
- 自环（单节点指向自己）：同样成立。
- 无环：`fast` 撞 `None` 退出，返回 `False` / `None`。

**⚠️ Python 特有坑**：比较节点是否相同**必须用 `is`（身份比较），不能用 `==`（值比较）**。
若两个不同节点恰好 `val` 相同，`==` 会误判为相遇。

---

### 例题 5 · LC 21 合并两个有序链表（递归与迭代的必修课）

**题目**：将两个升序链表合并为一个新的**升序**链表并返回。新链表是通过拼接给定的两个链表的所有节点组成的。

**样例**
- 输入：`l1 = [1,2,4], l2 = [1,3,4]` → 输出：`[1,1,2,3,4,4]`
- 输入：`l1 = [], l2 = [0]` → 输出：`[0]`

**思路**

**迭代版**：`dummy` + 尾插。每次取两条链头中**较小**的那个接到尾部，被取的那条前进一格。
当某条链耗尽，**把另一条的剩余部分整段接上**（它本身已有序，无需再比较）。

**递归版**：三行核心逻辑 —— 谁的头小，谁当新头；新头的 `next` = **剩余部分的合并结果**。

```
merge(1->2->4, 1->3->4)
  → 1（左边）<= 1（右边），左边当头
  → merge(2->4, 1->3->4) 的结果接在 1 后面
      → 右边 1 更小，右边当头
      → merge(2->4, 3->4) 的结果接在 1 后面
          → ...
```

**递归基**：`if not l1: return l2` / `if not l2: return l1` —— 一方为空，直接返回另一方。

**复杂度**：时间 O(m+n)（每轮淘汰一个节点）；迭代空间 O(1)，递归空间 O(m+n)（递归栈）。

> **今日最重要的思维迁移**：这个递归版的写法 —— **"处理当前节点 + 递归处理剩余部分"** ——
> 明天会原封不动地搬到二叉树上，变成 **"处理根节点 + 递归处理左右子树"**。请务必在这里想透。

---

### 例题 6 · LC 92 反转链表 II（局部反转，穿针引线）

**题目**：给你单链表的头指针 `head` 和两个整数 `left` 和 `right`，其中 `left <= right`。
请你反转从位置 `left` 到位置 `right` 的链表节点，返回**反转后的链表**。

**样例**
- 输入：`head = [1,2,3,4,5], left = 2, right = 4` → 输出：`[1,4,3,2,5]`
- 输入：`head = [5], left = 1, right = 1` → 输出：`[5]`

**思路（头插法，见模板 3.4）**

```
初始:  dummy -> 1 -> 2 -> 3 -> 4 -> 5
                ↑pre   ↑cur
                       (pre 走 left-1 = 1 步，停在 1；cur = pre.next = 2)

第1轮: 抓 nxt=3;
       2.next = 4      (cur 跳过 3)
       3.next = 2      (3 插到 2 前面)
       1.next = 3      (pre 改指 3)
       结果: dummy -> 1 -> 3 -> 2 -> 4 -> 5

第2轮: 抓 nxt=4;
       2.next = 5
       4.next = 3
       1.next = 4
       结果: dummy -> 1 -> 4 -> 3 -> 2 -> 5   ✅
```

注意：`pre` 和 `cur` **全程不动**，动的只有被摘下来插到段首的 `nxt`。循环次数 = `right - left`。

**复杂度**：时间 O(n)（`pre` 最多走 n 步，反转最多 n 步）；空间 O(1)。

**边界**：`left == right` 时循环 0 次，原样返回；`left == 1` 时 `pre` 就是 `dummy`，无需特判 —— 这就是 dummy 的价值。

---

## 五、代码实现（Python）

> 全部代码已在 Python 3.13 实测通过样例。
> **建议先自己写一遍，再展开对照。**
> 共用部分（节点定义与工具函数）不折叠，先复制到你的编辑器里。

```python
from typing import Optional, List


class ListNode:
    """单链表节点。val 存值，next 指向后继节点。"""
    def __init__(self, val: int = 0, next: Optional['ListNode'] = None):
        self.val = val
        self.next = next


def build(vals: List[int]) -> Optional[ListNode]:
    """测试辅助：由列表构造链表，如 [1,2,3] -> 1->2->3"""
    dummy = cur = ListNode(0)
    for v in vals:
        cur.next = ListNode(v)
        cur = cur.next
    return dummy.next


def to_list(head: Optional[ListNode]) -> List[int]:
    """测试辅助：链表转列表，便于打印断言。有环链表请勿调用！"""
    res = []
    while head:
        res.append(head.val)
        head = head.next
    return res
```

### 5.1 反转链表（LC 206）

<details>
<summary>例题 1 · LC206 反转链表 — 解答（迭代 + 递归）</summary>

```python
def reverseList(head: Optional[ListNode]) -> Optional[ListNode]:
    """迭代版：时间 O(n)，空间 O(1)。工程首选。"""
    pre, cur = None, head
    while cur:
        nxt = cur.next   # ① 先存后继，否则改完指针就丢了
        cur.next = pre   # ② 掉头
        pre = cur        # ③ pre 前移
        cur = nxt        # ④ cur 前移
    return pre           # ⑤ 新头是 pre（cur 已是 None）


def reverseListRec(head: Optional[ListNode]) -> Optional[ListNode]:
    """递归版：时间 O(n)，空间 O(n)（递归栈）。用于训练递归思维。"""
    if not head or not head.next:          # 递归基：空链或单节点
        return head
    new_head = reverseListRec(head.next)   # 假设后面那段已反转
    head.next.next = head                  # 让原后继反向指回自己
    head.next = None                       # 自己成为新尾，必须断链
    return new_head                        # 新头逐层向上传递
```

</details>

### 5.2 链表的中间结点（LC 876）

<details>
<summary>例题 2 · LC876 链表的中间结点 — 解答（后中点 + 前中点）</summary>

```python
def middleNode(head: Optional[ListNode]) -> Optional[ListNode]:
    """后中点：偶数长度返回靠右那个。LC 876 要求。"""
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    return slow


def middleNodeFirst(head: Optional[ListNode]) -> Optional[ListNode]:
    """前中点：偶数长度返回靠左那个。切链（归并/回文/重排）时用。"""
    if not head:
        return None
    slow, fast = head, head.next
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    return slow
```

</details>

### 5.3 删除链表的倒数第 N 个结点（LC 19）

<details>
<summary>例题 3 · LC19 删除链表的倒数第 N 个结点 — 解答</summary>

```python
def removeNthFromEnd(head: Optional[ListNode], n: int) -> Optional[ListNode]:
    """dummy + 固定间距：fast 领先 slow 恰好 n+1 步。一次扫描，O(n)/O(1)。"""
    dummy = ListNode(0, head)
    fast = slow = dummy
    for _ in range(n + 1):     # fast 先走 n+1 步
        fast = fast.next
    while fast:                # 同步前进，直到 fast 为 None
        fast = fast.next
        slow = slow.next
    slow.next = slow.next.next  # slow 停在待删节点的前一个
    return dummy.next
```

</details>

### 5.4 环形链表 / 环形链表 II（LC 141 / LC 142）

<details>
<summary>例题 4 · LC141+LC142 环形链表与环入口 — 解答</summary>

```python
def hasCycle(head: Optional[ListNode]) -> bool:
    """Floyd 判环：快走 2 步、慢走 1 步，有环必相遇。O(n)/O(1)。"""
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:      # ⚠️ 必须用 is（身份），不能用 ==（值）
            return True
    return False


def detectCycle(head: Optional[ListNode]) -> Optional[ListNode]:
    """找环入口：相遇后，一个指针从头出发、一个留在相遇点，同速再走，相遇处即入口。"""
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:                 # 先确认相遇
            p = head                     # p 从头节点出发
            while p is not slow:         # 与 slow 同速前进
                p = p.next
                slow = slow.next
            return p                     # 再次相遇处 = 环入口
    return None                          # fast 撞 None，无环
```

</details>

### 5.5 合并两个有序链表（LC 21）

<details>
<summary>例题 5 · LC21 合并两个有序链表 — 解答（迭代 + 递归）</summary>

```python
def mergeTwoLists(l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
    """迭代版：dummy + 尾插。时间 O(m+n)，空间 O(1)。"""
    dummy = cur = ListNode(0)
    while l1 and l2:
        if l1.val <= l2.val:
            cur.next = l1
            l1 = l1.next
        else:
            cur.next = l2
            l2 = l2.next
        cur = cur.next
    cur.next = l1 if l1 else l2   # 剩余整段直接接上（已有序）
    return dummy.next


def mergeTwoListsRec(l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
    """递归版：谁的头小谁当新头，新头的 next = 剩余部分的合并结果。"""
    if not l1:
        return l2
    if not l2:
        return l1
    if l1.val <= l2.val:
        l1.next = mergeTwoListsRec(l1.next, l2)
        return l1
    l2.next = mergeTwoListsRec(l1, l2.next)
    return l2
```

</details>

### 5.6 反转链表 II（LC 92）

<details>
<summary>例题 6 · LC92 反转链表 II — 解答（头插法）</summary>

```python
def reverseBetween(head: Optional[ListNode], left: int, right: int) -> Optional[ListNode]:
    """头插法：pre 与 cur 全程不动，每轮把 cur 后的节点摘下插到段首。"""
    dummy = ListNode(0, head)
    pre = dummy
    for _ in range(left - 1):
        pre = pre.next          # pre 停在待反转段的前一个
    cur = pre.next              # cur 是待反转段的头，反转后成为段尾
    for _ in range(right - left):
        nxt = cur.next          # 抓住 cur 后面的节点
        cur.next = nxt.next     # ① cur 跳过 nxt
        nxt.next = pre.next     # ② nxt 插到段首
        pre.next = nxt          # ③ pre 改指 nxt
    return dummy.next
```

</details>

### 5.7 样例验证输出

> 6 道例题 + 边界用例共 **25 项断言全部通过**（含思考题的完整脚本为 36 项）。

<details>
<summary>样例输出（点击展开）</summary>

```
--- LC206 反转链表 ---
[PASS] 206 iter: got=[5, 4, 3, 2, 1] want=[5, 4, 3, 2, 1]
[PASS] 206 rec: got=[5, 4, 3, 2, 1] want=[5, 4, 3, 2, 1]
[PASS] 206 empty: got=[] want=[]
[PASS] 206 single: got=[1] want=[1]

--- LC876 中间结点 ---
[PASS] 876 odd: got=[3, 4, 5] want=[3, 4, 5]
[PASS] 876 even: got=[4, 5, 6] want=[4, 5, 6]
[PASS] 876 first-mid even: got=2 want=2
[PASS] 876 first-mid odd: got=3 want=3

--- LC19 删除倒数第 N 个 ---
[PASS] 19 n=2: got=[1, 2, 3, 5] want=[1, 2, 3, 5]
[PASS] 19 del head: got=[2] want=[2]
[PASS] 19 del tail: got=[1] want=[1]
[PASS] 19 single: got=[] want=[]

--- LC141/142 环形链表 ---
[PASS] 141 hasCycle: got=True want=True
[PASS] 142 detectCycle: got=2 want=2
[PASS] 141 no cycle: got=False want=False
[PASS] 142 no cycle: got=None want=None
[PASS] 142 self loop: got=1 want=1

--- LC21 合并两个有序链表 ---
[PASS] 21 iter: got=[1, 1, 2, 3, 4, 4] want=[1, 1, 2, 3, 4, 4]
[PASS] 21 rec: got=[1, 1, 2, 3, 4, 4] want=[1, 1, 2, 3, 4, 4]
[PASS] 21 empty1: got=[0] want=[0]
[PASS] 21 both empty: got=[] want=[]

--- LC92 反转链表 II ---
[PASS] 92 2-4: got=[1, 4, 3, 2, 5] want=[1, 4, 3, 2, 5]
[PASS] 92 whole: got=[5, 4, 3, 2, 1] want=[5, 4, 3, 2, 1]
[PASS] 92 single: got=[5] want=[5]
[PASS] 92 1-2: got=[2, 1, 3] want=[2, 1, 3]
```

</details>

---

## 六、课后进阶思考与方法延伸

### 6.1 思考题一 · LC 234 回文链表（难度：中等）

**题目**：给你一个单链表的头节点 `head`，请你判断该链表是否为回文链表。如果是，返回 `true`；否则，返回 `false`。

**进阶要求**：用 O(n) 时间复杂度和 **O(1) 空间复杂度**解决此题。

**提示**：

1. 用**前中点**快慢指针把链表切成两半（为什么不能用后中点？因为后半段会比前半段少一个节点）。
2. 反转**后半段**。
3. 双指针逐值比对（`p1` 从头、`p2` 从后半段头）。
4. **比对完把后半段再反转回去**，恢复原链表（这是个好习惯，面试官会加分）。

> 关键一问：为什么循环条件写成 `while p2`，而不是 `while p1 and p2`？
> 答：奇数长度时前半段比后半段多一个（正中间那个），用 `p2` 做终止条件正好跳过它。

<details>
<summary>思考题 1 · LC234 回文链表 — 解答</summary>

```python
def isPalindrome(head: Optional[ListNode]) -> bool:
    if not head or not head.next:
        return True

    # ① 前中点：slow 停在"前半段的尾"
    slow, fast = head, head.next
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next

    # ② 反转后半段
    second = reverseList(slow.next)

    # ③ 逐值比对（以 p2 为终止条件，奇数长度自动跳过正中间节点）
    p1, p2, ok = head, second, True
    while p2:
        if p1.val != p2.val:
            ok = False
            break
        p1 = p1.next
        p2 = p2.next

    # ④ 恢复原链表（原地修改类题目的职业习惯）
    slow.next = reverseList(second)
    return ok
```

</details>

### 6.2 思考题二 · LC 143 重排链表（难度：中等）

**题目**：给定一个单链表 `L` 的头节点 `head`，单链表 `L` 表示为 `L0 → L1 → … → Ln-1 → Ln`。
请将其重新排列后变为 `L0 → Ln → L1 → Ln-1 → L2 → Ln-2 → …`。
不能只是单纯的改变节点内部的值，而是需要**实际的进行节点交换**。

**提示**：这是 LC 876 + LC 206 + LC 21 的**三合一**组合题。
顺序：前中点切两半 → **反转后半段** → **断链**（`slow.next = None`，否则会成环）→ 交叉合并。
合并时同样要**先存 `t1 / t2` 两个后继**再改指针。

<details>
<summary>思考题 2 · LC143 重排链表 — 解答</summary>

```python
def reorderList(head: Optional[ListNode]) -> None:
    if not head:
        return

    # ① 前中点切分
    slow, fast = head, head.next
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next

    # ② 反转后半段，并把前半段尾部断开（不断链会成环！）
    second = reverseList(slow.next)
    slow.next = None

    # ③ 交叉合并：L0 -> Ln -> L1 -> Ln-1 -> ...
    first = head
    while second:
        t1, t2 = first.next, second.next   # 先存两个后继
        first.next = second                # 前半节点指向后半节点
        second.next = t1                   # 后半节点指回前半的下一个
        first, second = t1, t2             # 双双前移
```

</details>

### 6.3 思考题三 · LC 148 排序链表（难度：中等，压轴）

**题目**：给你链表的头结点 `head`，请将其按**升序**排列并返回**排序后的链表**。
**进阶**：你可以在 O(n log n) 时间复杂度和 **常数级空间复杂度**下，对链表进行排序吗？

**提示**：见模板 3.6 的**自底向上归并**。
三个必须做对的点：`cut` 里要断链、`cut(None)` 要提前判空、每轮 `tail` 要走到合并段末尾。

<details>
<summary>思考题 3 · LC148 排序链表 — 解答</summary>

```python
def cut(head: Optional[ListNode], n: int) -> Optional[ListNode]:
    """切下前 n 个节点，返回剩余部分的头。不足 n 个返回 None。"""
    p = head
    while p and n > 1:
        p = p.next
        n -= 1
    if not p:
        return None
    nxt = p.next
    p.next = None      # ⚠️ 必须断链，否则段间还连着会死循环
    return nxt


def sortList(head: Optional[ListNode]) -> Optional[ListNode]:
    """自底向上归并：时间 O(n log n)，空间 O(1)。"""
    if not head or not head.next:
        return head

    n, p = 0, head
    while p:                      # ① 数长度
        n += 1
        p = p.next

    dummy = ListNode(0, head)
    step = 1
    while step < n:               # ② 段长倍增 1,2,4,8,...
        cur, tail = dummy.next, dummy
        while cur:                # ③ 扫描全链，两两合并
            left = cur
            right = cut(left, step)
            cur = cut(right, step) if right else None   # ⚠️ 不能对 None 调 cut
            tail.next = mergeTwoLists(left, right)
            while tail.next:      # ④ tail 走到合并段末尾
                tail = tail.next
        step <<= 1
    return dummy.next
```

</details>

### 6.4 更多延伸方向（学有余力）

| 方向 | 代表题 | 用到今天的什么 |
|------|--------|--------------|
| K 个一组翻转 | LC 25 | 局部反转 + 穿针引线 + 递归（**强烈推荐，难度正好**） |
| 两两交换节点 | LC 24 | 递归 + 指针重接 |
| 相交链表 | LC 160 | 双指针走"两条路拼接"（浪漫的 A+B = B+A 思想） |
| 删除排序链表中的重复元素 | LC 83 / LC 82 | dummy + 遍历 |
| 旋转链表 | LC 61 | 成环 + 找新头 + 断链 |
| 复制带随机指针的链表 | LC 138 | 哈希映射 / 原地穿插复制 |
| LRU 缓存 | LC 146 | 哈希表 + **双向链表**（今天的单向链表是它的基础） |

### 6.5 Day 6 自测清单

在合上这份笔记之前，请逐条自问。任何一条答不上来，回到对应章节再看一遍。

- [ ] 能否**不看模板**，默写反转链表的迭代版和递归版？能否说清 `head.next.next = head` 在做什么？
- [ ] 能否说出**前中点**和**后中点**的初始化差异，以及各自的使用场景？
- [ ] 能否推导 Floyd 算法中「**相遇点 + 头节点同速前进 = 环入口**」的证明？
- [ ] 能否解释「**删除倒数第 N 个**」中，为什么 `fast` 要领先 `n+1` 步而不是 `n` 步？
- [ ] 能否说清 dummy 节点解决了什么问题？哪些场景**必须**用它？
- [ ] 能否独立写出 `reverseBetween` 的头插法，并说明 `pre` 和 `cur` 为什么全程不动？
- [ ] 能否说出**为什么链表排序用归并而不用快排**？
- [ ] 能否列出至少 5 条链表易错点（对照 3.7 的表格）？

### 6.6 与 Day 7「二叉树与递归」的衔接

明天的主题是**二叉树与递归**。今天的内容有三条**直接的知识依赖**，请务必带走：

**① 递归范式完全同构**
今天的递归版反转链表：

```python
new_head = reverseListRec(head.next)   # 先递归处理"剩余部分"
head.next.next = head                  # 再处理"当前节点"
```

明天的前序遍历：

```python
res.append(root.val)              # 先处理"当前节点"
dfs(root.left); dfs(root.right)   # 再递归处理"左右子树"
```

结构一模一样：**把一个结构拆成「一个元素 + 一个更小的同构结构」，递归处理后者。**
区别只在于链表是**一条**分支（递归一次），二叉树是**两条**分支（递归两次）。
**今天把「假设子问题已解决」这句话想透，明天的树形递归会顺畅非常多。**

**② 递归三要素的迁移**
今天在递归版里看到的「递归基（`if not head`）→ 递归调用 → 当前层处理 → 返回」，明天会变成
「递归基（`if not root`）→ 递归左右子树 → 当前层处理 → 返回」。
**递归空间复杂度 = 递归深度**：链表是 O(n)，平衡二叉树是 O(h) = O(log n)，退化成链则是 O(n)。

**③ 指针思维的延续**
二叉树节点 `TreeNode(val, left, right)` 本质就是**两个 next 指针的节点**。
今天练的「改指针前先存后继」「断链避免成环」，明天在**翻转二叉树、展平链表（LC 114）、Morris 遍历**中会原样复用。

**另外预告一个彩蛋**：Day 5 学的**单调栈**、Day 2 学的**双指针**，在树里会演化成**中序遍历（BST 有序性）**和**最近公共祖先的双指针走法**。这些算法并不是孤立的，它们是一条连续的思路链。

---

> **今日一句**：链表题的正确率，**取决于你在纸上画了多少张指针图，而不是你记了多少模板。**

---

*文档生成：2026-09-03 · Day 6｜代码环境：Python 3.13.12（36 项断言全部通过）｜例题来源：LeetCode*
