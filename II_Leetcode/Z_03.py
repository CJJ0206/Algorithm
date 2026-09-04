"""
给定一个字符串 s ，请你找出其中不含有重复字符的最长子串的长度。

示例 1:
输入: s = "abcabcbb"
输出: 3 
解释: 因为无重复字符的最长子串是 "abc"，所以其长度为 3。注意 "bca" 和 "cab" 也是正确答案。
"""

class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        char_index = {} # 这个字典只记录不重复的字符的相应索引
        left , right = 0 , 0
        ans = 0 
        # 从右界往左边测试，一个个放进字典，如果出现重复呢怎么办
        # 出现重复：把左界移到这个位置，并更新这个元素新的位置
        # 最后的长度怎么返回呢
        # for right in range(len(s)):
        #     char = s[right]
        #     if char in char_index and char_index[char] >= left:
        #         left = char_index[char] + 1
        #     char_index[char] = right 
        #    
        #     ans = max(ans, right - left + 1)
        # return ans

        for idx , val in enumerate(s): # 向后遍历s
            # 如果值在字典中并且这个值的索引大于left
            if val in char_index and char_index[val] >= left:
                # 说明这个重复值出现在left的右边，直接更新left
                left = char_index[val] + 1 # 这里做的是在原始的这个重复元素的位置加一把他去除
            char_index[val] = idx # 更新对应val的index
            # 这个确实只能写后面，如果按照正常想法写在前面的话，每一次进来的时候就直接覆盖位置了
            ans = max(ans, idx - left + 1)
            # 每次循环最后都要和ans对比下再保存最长值
            # 加一是因为：a b d 长度为三但是索引相减（2-0）结果是2不对，所以加一
        return ans

