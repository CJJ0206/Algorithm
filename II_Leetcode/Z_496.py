"""
题目描述：nums1 是 nums2 的子集。对 nums1 中每个元素 x，找出它在 nums2 中 x 右侧第一个比 x 大的元素；不存在则 -1。

样例：
输入：nums1 = [4,1,2], nums2 = [1,3,4,2]
输出：[-1,3,-1]
解释：4 在 nums2 中右侧没有更大的 → -1
     1 右侧第一个更大的是 3 → 3
     2 右侧没有更大的 → -1
"""

class Solution():
     def nextmax(self,nums1:list[int],nums2:list[int]) -> int:
          res_dict = {}
          stack = []  # 存具体的数值即可，保持单调递减

          for x in nums2:
               while stack and x > stack[-1]:
                    smaller = stack.pop()         # pop 出来的是小的元素的值
                    res_dict[smaller] = x         # 直接把这个值作为key，x作为找到的比它大的值存进字典
               stack.append(x)
          return [res_dict.get(num, -1) for num in nums1]

                         
if __name__ == "__main__":
     nums1 = [4,1,2]
     nums2 = [1,3,4,2]
     so = Solution()
     print(so.nextmax(nums1,nums2))
            


