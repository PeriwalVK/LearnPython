# print("Try programiz.pro")
# import sys


# def prints(x):
#     print(f"for x {x}: number occupies {sys.getsizeof(1 << x)} bytes")
#     print(f"for x {x}: list occupies {sys.getsizeof([True for _ in range(x)])} bytes")
#     print("=========================================================")


# x = 1
# prints(x)

# x = 10
# prints(x)

# x = 100
# prints(x)

# x = 1000
# prints(x)

# x = 10000
# prints(x)

# x = 100000
# prints(x)


# from collections import defaultdict


# def count_unique_subarrays_with_sum(nums, target):

#     left = -1
#     left_sum = 0
#     right_sum = 0

#     seen = set()
#     sum_cnt = defaultdict(int)
#     sum_cnt[0] = 1

#     count = 0

#     for right in range(len(nums)):
#         # Remove duplicates
#         while nums[right] in seen:
#             sum_cnt[left_sum] -= 1
#             left += 1
#             seen.remove(nums[left])
#             left_sum += nums[left]

#         seen.add(nums[right])
#         right_sum += nums[right]

#         count += sum_cnt[right_sum - target]
#         sum_cnt[right_sum] += 1

#     return count


# assert(count_unique_subarrays_with_sum([1, 1, 1, 1, 1], 0) == 0)
# assert(count_unique_subarrays_with_sum([1, 1, 1, 1, 1], 1) == 5)
# assert(count_unique_subarrays_with_sum([1, 1, 1, 1, 1], 2) == 0)
# assert(count_unique_subarrays_with_sum([1, 2, 3], 0) == 0)
# assert(count_unique_subarrays_with_sum([1, 2, 3], 1) == 1)
# assert(count_unique_subarrays_with_sum([1, 2, 3], 2) == 1)
# assert(count_unique_subarrays_with_sum([1, 2, 3], 3) == 2)
# assert(count_unique_subarrays_with_sum([1, 2, 3], 4) == 0)
# assert(count_unique_subarrays_with_sum([1, 2, 3], 5) == 1)
# assert(count_unique_subarrays_with_sum([1, 2, 3], 6) == 1)
# assert(count_unique_subarrays_with_sum([1, 2, 3], 7) == 0)
# assert(count_unique_subarrays_with_sum([1, 2, 1, 2], 3) == 3)
# assert(count_unique_subarrays_with_sum([1, -1, 2, 3], 3) == 1)
# assert(count_unique_subarrays_with_sum([2, -2, 2, -2, 2], 0) == 4)
# assert(count_unique_subarrays_with_sum([0, 0, 0], 0) == 3)
# assert(count_unique_subarrays_with_sum([1, 2, 3, 4], 10) == 1)
# assert(count_unique_subarrays_with_sum([1, 2, 3], 100) == 0)
# assert(count_unique_subarrays_with_sum([5], 5) == 1)
# assert(count_unique_subarrays_with_sum([1, 2, 3, 2, 1], 3) == 3)
# assert(count_unique_subarrays_with_sum([3, 1, 2, 3, 4], 6) == 2)
# assert(count_unique_subarrays_with_sum([1, 2, -1, 2, -1, 2], 3) == 1)
# assert(count_unique_subarrays_with_sum([4, 2, -2, 2, 4], 4) == 4)

# print("All TEST CASES PASSED!")

# s = set()
# for i in range(19,11,-1):
#     s.add(i)

x = [[0, 1, 2, 3], [4, 5, 6, 7], (8, 9, 10, 11), {101, 400000000999900, 99, 23}]

for each in zip(*x):
    print(each)
# while True:
#     print(next(y))


def f(*args, **kwargs):
    print(type(args), type(kwargs))


f()

print("vikas".capitalize())  # Vikas
print("_kumar".capitalize())  # _kumar
print("Periwal".capitalize())  # Periwal


x = {}
print(type(x))
print(-10 // 3)







# Given a 15 digit number. Pick digits from it without sorting to make the biggest 3 digit number.
#
# Examples:
#
# 987654321111111 -> 987
# 811111111111119 -> 819
# 34234234234278 -> 478
# 818181911112111 -> 921





#
# Constraints:
#
# 1 <= digit <= 9
# no ZEROS



def ans0(num: str):

    ret = ''

    # l = 11
    # for _ in range(3):


    current_left = 0
    
    for k in range(3, 0, -1):
      curr_pos = 15-k
      for i in range(15-k,current_left-1, -1):
        # print(f"i: {i}")
        x = int(num[i])
        if x >= int(num[curr_pos]):
          curr_pos = i
      
          # print(curr_pos)
      ret += num[curr_pos]
      current_left = curr_pos + 1
    
    return int(ret)




def ans(num: str, k:int=3):
    
    from collections import defaultdict, deque
    m = defaultdict(lambda: deque())

    for i in range(len(num)-k):
        m[num[i]].append(i)

    ret = ""
    start_ = 0
    for j in range(len(num)-k, len(num)):
        m[num[j]].append(j)

        for d in "987654321":
            if m[d]:
                curr_pos = m[d].popleft()
                ret += d
                break
        
        for pos in range(start_, curr_pos):
            m[num[pos]].popleft()
        start_ = curr_pos + 1
    
    return ret






print(ans("987654321111111"))# -> 987
print(ans("811111111111119"))# -> 819
print(ans("134234234234278"))# -> 478
print(ans("818181911112111"))# -> 921











