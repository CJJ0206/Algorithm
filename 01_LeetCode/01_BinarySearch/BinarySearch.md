# Day 1：二分查找（Binary Search）



## 一、算法核心思想



二分查找是一种在**有序数组**中查找特定元素的高效算法。其核心思想是**分治与减治（Decrease and Conquer）**：
每次通过将目标值与区间中点元素进行比较，直接排除掉一半不可能包含目标值的区间，从而将搜索规模减半。

## 二、适用前提与复杂度



* **前提条件**：数据必须具备**单调性**（通常为升序或降序排列），且支持**随机访问**（如数组）。


* **时间复杂度**：$\mathcal{O}(\log n)$。


* **原因**：每次查找都会将搜索规模减半。假设数组长度为 $n$，最坏情况下需要查找 $k$ 次，区间长度的变化过程为 $n \rightarrow n/2 \rightarrow n/4 \dots \rightarrow n/2^k$。当 $n/2^k = 1$ 时（即区间缩小到只剩最后一个元素），解得 $k = \log_2 n$。因此，时间复杂度呈现对数级别。




* **空间复杂度**：$\mathcal{O}(1)$（迭代实现）。


* **原因**：在迭代实现中，整个算法运行期间只需要额外开辟空间来维护 `left`、`right` 和 `mid` 等几个常数级别的指针变量。无论输入数组的数据规模 $n$ 有多大，这部分占用的内存都是恒定不变的。





## 三、关键细节与边界处理（左闭右闭区间）



实现二分查找时，定义好区间不变量（Loop Invariant）至关重要。最常用且不易出错的区间定义是左闭右闭 `[left, right]`：

* **初始边界**：`left = 0`, `right = len(nums) - 1`

* **循环条件**：`left <= right`（因为 `[left, right]` 在 `left == right` 时区间依然有效）


* **中点防溢出计算**：`mid = left + (right - left) / 2`

* **区间收缩**：


* 若 `nums[mid] > target`，说明目标在左侧，更新 `right = mid - 1`

* 若 `nums[mid] < target`，说明目标在右侧，更新 `left = mid + 1`

* 若 `nums[mid] == target`，直接返回下标 `mid`




## 四、课后进阶思考



标准二分查找用于查找确定的单值。在实际算法题中，二分查找更多用于寻找边界或满足某种单调条件的最优解：

1. **寻找左侧边界**：数组存在重复元素时，如何找到第一个等于 `target` 的位置？


2. **二分答案法**：当题目要求“求最大值的最小值”或“求最小值的最大值”时，如何将问题转化为二分查找？（如：LeetCode 875. 爱吃香蕉的珂珂）



---

## 五、进阶例题与解析

### 进阶思考 1：寻找左侧边界

**题目描述**：给定一个按照非递减顺序排列的整数数组 `nums`，和一个目标值 `target`。请找出给定目标值在数组中的第一个出现位置。如果数组中不存在目标值 `target`，返回 `-1`。（对应 LeetCode 34 题前半部分）

<details>

<summary>展开查看解析与代码实现</summary>

**解析**：
与标准二分查找不同，当遇到 `nums[mid] == target` 时，我们**不能立即返回**，因为当前位置可能不是第一个出现的 `target`。我们需要继续在左区间 `[left, mid - 1]` 中寻找，因此要更新 `right = mid - 1` 来锁定左侧边界。循环结束后，检查 `left` 是否越界以及是否命中目标即可。

**Python 实现**：

```python
def searchFirst(nums: list[int], target: int) -> int:
    left, right = 0, len(nums) - 1
    
    while left <= right:
        mid = left + (right - left) // 2
        if nums[mid] == target:
            right = mid - 1  # 重点：找到目标值不返回，而是收缩右边界向左逼近
        elif nums[mid] > target:
            right = mid - 1
        else:
            left = mid + 1
            
    # 检查 left 是否越界，以及对应位置是否真的是 target
    if left >= len(nums) or nums[left] != target:
        return -1
    return left

```

</details>



### 进阶思考 2：二分答案法


**题目描述**：（LeetCode 875. 爱吃香蕉的珂珂）
珂珂喜欢吃香蕉。这里有 $n$ 堆香蕉，第 $i$ 堆中有 `piles[i]` 根香蕉。警卫将在 $h$ 小时后回来。珂珂可以决定她吃香蕉的速度 $k$（单位：根/小时）。每个小时，她将会选择一堆香蕉，从中吃掉 $k$ 根。如果这堆香蕉少于 $k$ 根，她将吃掉这堆的所有香蕉，且这一小时内不会再吃更多的香蕉。返回她可以在 $h$ 小时内吃掉所有香蕉的**最小速度** $k$。

<details>

<summary>展开查看解析与代码实现</summary>

**解析**：
题目要求找出“最小速度 $k$”。速度 $k$ 与吃完所需的时间存在**单调关系**：速度越快，耗时越短。因此可以用二分查找直接“猜”答案。

1. **确定二分范围**：速度最慢是 `1`，最快是一次性吃完最大的一堆，即 `max(piles)`。区间为 `[1, max(piles)]`。
2. **判定条件**：针对猜出的速度 `mid`，计算总耗时。如果耗时 $\le h$，说明速度可行，但我们要找最小值，所以尝试更慢的速度（`right = mid - 1`）；如果耗时 $> h$，说明太慢了被抓了，必须加快速度（`left = mid + 1`）。

**Python 实现**：

```python
import math

def minEatingSpeed(piles: list[int], h: int) -> int:
    def get_hours(speed: int) -> int:
        hours = 0
        for pile in piles:
            hours += math.ceil(pile / speed) # 每堆向上取整耗时
        return hours

    left, right = 1, max(piles)
    
    while left <= right:
        mid = left + (right - left) // 2
        if get_hours(mid) <= h:
            right = mid - 1 # 速度达标，尝试找更小的速度逼近边界
        else:
            left = mid + 1  # 速度太慢导致超时，必须提速
            
    return left # 最终的 left 就是满足条件的最小速度

```


</details>