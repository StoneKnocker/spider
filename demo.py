import re

date_pattern = r'(\d{5})年(\d{1,2})月(\d{1,2})日'
date_regex = re.compile(date_pattern)

str = '2023年2月21日新建商品房网签备案统计情况'

alls = re.search(date_pattern, str)
print(alls)
nums = alls.groups()
date = '{:0>4s}{:0>2s}{:0>2s}'.format(nums[0], nums[1], nums[2])
print(date)