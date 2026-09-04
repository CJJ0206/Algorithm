# Day 2：双指针算法（Two Pointers）

---

### 一、算法核心思想

双指针是指在遍历对象的过程中，使用两个移动方向或移动速度不同的指针协同完成任务。双指针的核心优势在于能够**利用数据的有序性或结构特征，避免不必要的嵌套循环，将时间复杂度从 $\mathcal{O}(n^2)$ 优化至 $\mathcal{O}(n)$**。

常见模式主要分为两类：

1. **对撞指针（左右指针 / 相向指针）**：指针分别置于两端，根据条件向中间靠拢（常用于有序数组求和、二分衍生、反转/回文判断）。
2. **快慢指针（同向指针 / 读写指针）**：指针同向移动但步长或触发条件不同（常用于原地修改数组、链表检测环、寻找链表中点）。

---

### 二、复杂度分析与原因推导

* **时间复杂度：$\mathcal{O}(n)$**
* **原因推导**：
* **对撞指针**：左指针从最左向右移动，右指针从最右向左移动，每次循环至少有一个指针移动一步，两指针相遇即结束。整个过程中每个元素最多被访问一次，总操作次数与数组长度 $n$ 呈线性关系。
* **快慢指针**：快指针负责无条件遍历数组（最多 $n$ 步），慢指针仅在满足特定条件时前移（最多 $n$ 步）。两指针各自走完全程的步数上限均为 $n$，总时间为 $2n$ 级别的常数开销，即 $\mathcal{O}(n)$。




* **空间复杂度：$\mathcal{O}(1)$**
* **原因推导**：算法全程仅需维护常数个指针变量（如 `left`、`right`、`slow`、`fast` 等数值索引或节点引用），所有的比较、交换或覆盖均直接在原始数据结构上原地（In-place）完成，不需要申请任何与输入规模 $n$ 成正比的额外内存空间。



---

### 三、经典模式与实战例题

#### 模式 1：对撞指针 —— LeetCode 167. 两数之和 II - 输入有序数组

##### 题目描述

给你一个下标从 `1` 开始的整数数组 `numbers` ，该数组已按**非递减顺序排列**，请你从数组中找出满足相加之和等于目标数 `target` 的两个数。

**示例：**

> **输入:** `numbers =`, `target = 9`
> **输出:** `  **解释:** 2 与 7 之和等于目标数 9 。因此 index1 = 1, index2 = 2 。返回` 。

##### 核心思路

<details>

<summary> 点击展开答案 </summary>

1. 定义左指针 `left = 0`，右指针 `right = len(numbers) - 1`。
2. 计算 `curr_sum = numbers[left] + numbers[right]`：
* 若 `curr_sum == target`，找到答案，返回对应下标（题目要求从 1 开始，需加 1）；
* 若 `curr_sum < target`，因为数组有序，增大总和的唯一方式是让左指针右移：`left += 1`；
* 若 `curr_sum > target`，减小总和的唯一方式是让右指针左移：`right -= 1`。



##### 代码实现 (Python)

```python
def two_sum(numbers: list[int], target: int) -> list[int]:
    left, right = 0, len(numbers) - 1
    
    while left < right:
        curr_sum = numbers[left] + numbers[right]
        if curr_sum == target:
            return [left + 1, right + 1]
        elif curr_sum < target:
            left += 1
        else:
            right -= 1
            
    return [-1, -1]

```

</details>

---

#### 模式 2：快慢指针 —— LeetCode 26. 删除有序数组中的重复项

##### 题目描述

给你一个**非严格递增排列**的数组 `nums` ，请你**原地**删除重复出现的元素，使每个元素只出现一次 ，返回删除后数组的新长度。元素的相对顺序应该保持一致。

**示例：**

> **输入:** `nums =`
> **输出:** `5`, `nums =`
> **解释:** 函数应该返回新的长度 5，并且原数组 nums 的前五个元素被修改为 0, 1, 2, 3, 4 。

##### 核心思路

<details>

<summary> 点击展开答案 </summary>

1. 定义慢指针 `slow = 0`（指向有效不重复区间的末尾），快指针 `fast = 1`（负责向后探索新元素）。
2. 当 `nums[fast] != nums[slow]` 时，说明探索到了新的不重复元素：
* 慢指针前进一步：`slow += 1`
* 将新元素赋值到慢指针位置：`nums[slow] = nums[fast]`


3. 最终 `[0, slow]` 区间即为去重后的有效数组，长度为 `slow + 1`。

##### 代码实现 (Python)

```python
def remove_duplicates(nums: list[int]) -> int:
    if not nums:
        return 0
        
    slow = 0
    for fast in range(1, len(nums)):
        if nums[fast] != nums[slow]:
            slow += 1
            nums[slow] = nums[fast]
            
    return slow + 1

```

</details>

---

### 四、课后进阶思考与实战

#### 进阶思考 1：快慢指针在链表中的应用 —— LeetCode 141. 环形链表

##### 题目描述

给你一个链表的头节点 `head` ，判断链表中是否有环。如果链表中有某个节点，可以通过连续跟踪 `next` 指针再次到达，则链表中存在环。如果链表中存在环，则返回 `true` ；否则，返回 `false` 。

**示例：**

> **输入:** `head =`, `pos = 1`（表示尾节点连到索引 1 的节点）

> **输出:** `true`

> **解释:** 链表中有一个环，其尾部连接到第二个节点。

##### 核心思路（Floyd 判圈算法 / 龟兔赛跑）

<details>

<summary> 点击展开答案 </summary>

1. 定义慢指针 `slow`（每次前进一步）和快指针 `fast`（每次前进两步），初始均指向 `head`。
2. 若链表无环，快指针必定率先遇到 `None`，循环结束；
3. 若链表有环，快指针进入环后，相对于慢指针每次以 1 步的相对速度拉近距离，最终必然在环内“套圈”与慢指针相遇（`slow == fast`）。

##### 复杂度分析

* **时间复杂度**：$\mathcal{O}(n)$，无环时遍历 $n/2$ 次；有环时快指针最多多跑一圈即可追上慢指针。
* **空间复杂度**：$\mathcal{O}(1)$，仅使用两个指针变量。

##### 代码实现 (Python)

```python
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None

def has_cycle(head: ListNode | None) -> bool:
    if not head or not head.next:
        return False
        
    slow, fast = head, head
    while fast and fast.next:
        slow = slow.next          # 走一步
        fast = fast.next.next     # 走两步
        if slow == fast:
            return True
            
    return False

```

</details>

---

#### 进阶思考 2：三指针拓展 —— LeetCode 15. 三数之和

##### 题目描述

给你一个整数数组 `nums` ，判断是否存在三元组 `[nums[i], nums[j], nums[k]]` 满足 `i != j`、`i != k` 且 `j != k` ，同时还满足 `nums[i] + nums[j] + nums[k] == 0` 。请你返回所有和为 0 且**不重复**的三元组。

**示例：**

> **输入:** `nums =`

> **输出:** `i j k`

> **解释:** 答案中不包含重复的三元组。

##### 核心思路（排序 + 固定一数 + 对撞双指针）

<details>

<summary> 点击展开答案 </summary>

1. **排序**：先对数组进行升序排序，时间复杂度 $\mathcal{O}(n \log n)$。
2. **遍历固定首数**：遍历数组，固定第一个数 `nums[i]`，问题转化为在 `[i + 1, len - 1]` 区间内寻找两数之和等于 `-nums[i]`。
3. **对撞双指针搜索**：
* 设置 `left = i + 1`, `right = len(nums) - 1`。
* 计算 `curr_sum = nums[i] + nums[left] + nums[right]`。
* 根据 `curr_sum` 与 0 的大小关系收缩 `left` 或 `right`。


4. **关键去重逻辑**：
* 固定元素去重：若 `i > 0 and nums[i] == nums[i - 1]`，跳过当前循环。
* 左右指针去重：找到合法三元组后，若左右指针移动后的相邻元素相同，需持续跳过重复项。



##### 复杂度分析

* **时间复杂度**：$\mathcal{O}(n^2)$，外层遍历 $n$ 次，内层双指针搜索最多 $n$ 次。
* **空间复杂度**：$\mathcal{O}(1)$（除返回值和排序本身占用的栈空间外）。

##### 代码实现 (Python)

```python
def three_sum(nums: list[int]) -> list[list[int]]:
    nums.sort()
    res = []
    n = len(nums)
    
    for i in range(n - 2):
        # 优化剪枝：如果当前最小正数大于 0，三数之和不可能为 0
        if nums[i] > 0:
            break
            
        # 对固定元素去重
        if i > 0 and nums[i] == nums[i - 1]:
            continue
            
        left, right = i + 1, n - 1
        while left < right:
            total = nums[i] + nums[left] + nums[right]
            if total == 0:
                res.append([nums[i], nums[left], nums[right]])
                # 对 left 和 right 去重
                while left < right and nums[left] == nums[left + 1]:
                    left += 1
                while left < right and nums[right] == nums[right - 1]:
                    right -= 1
                left += 1
                right -= 1
            elif total < 0:
                left += 1
            else:
                right -= 1
                
    return res

```

</details>

---

### 五、方法延伸

如果快慢指针维护的是一个“动态扩展与收缩的有效区间”，它就演变为了接下来的核心进阶算法 —— **滑动窗口（Sliding Window）**。