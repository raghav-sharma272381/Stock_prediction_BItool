from typing import List


def twoSum( nums: List[int], target: int) -> List[int]:
        head = 0
        tail = len(nums) - 1
        while tail > head:
            summ = nums[head] + nums[tail]
            if summ > target:
                tail -= 1
            elif summ < target:
                head += 1
            elif summ == target:
                return [head , tail ]

print(twoSum([3,2,4],6))