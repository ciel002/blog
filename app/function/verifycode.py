import random


def yzm(n):
    code = ''  # 拼接随机生成的数字或字母
    for i in range(0, n):
        '''循环4次生成4个字母或数字'''
        # 生成数字
        # 注意：将数字转换成字符串
        num = str(random.randint(0, 9))
        # 生成字母  ASC码A:65~z:90
        zm = chr(random.randint(65, 90))
        # 随机产生一个内容
        ret = random.choice([num, zm])
        code += ret  # 把code和ret用空字符串拼接
    return code
