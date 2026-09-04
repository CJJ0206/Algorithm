


def TwoPointer(nums:list[int],target:int) -> int:
    # FIXME 对撞指针（同样这里要求非递减顺序数组）
    left ,right = 0, len(nums) - 1
    while left <= right:
        res = nums[left] + nums[right] 
        if res == target:
            return left , right
        elif res < target: # 因为输入是有序的所以可以做到根据结果操作，那肯定时间复杂度低啊
            left += 1
        else:
            right += 1


def remove_duplicates(nums: list[int]) -> int:
    # FIXME 快慢指针
    # 非严格递增数组 nums ，原地删除重复出现元素，使元素只出现一次 ，返回数组新长度。元素相对顺序保持一致。
    slow = 0
    for fast in range(1, len(nums)): # 快指针是全部遍历的
        # FIXME 只处理了不相同时
        if nums[fast] != nums[slow]: # 如果前后不相同则慢指针加一，如果相同的话则是快指针在一直往后
            slow += 1
            nums[slow] = nums[fast]  # 这里如果快指针不直接覆盖中间会别重复元素隔开
    print(nums[:slow + 1]) # 这种原地操作本来也不会删除最后多余的元素，就是重复就往前覆盖
    return slow + 1



if __name__ == "__main__":
    print(TwoPointer([2,2,3,5,6,9],12))
    print(remove_duplicates([2,2,3,5,6,9]))
    

