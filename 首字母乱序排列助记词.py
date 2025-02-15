
# 2025年2月15日04:51:15 owl
# 为了简单的存放助记词，或者泄露了明文被黑客利用，所以把助记词打乱存放，
# 跑脚本的时候根据规则还原乱序助记词。

# BIP39 助记词乱序, 要求:
# 1.在加密助记词前，明文也乱序一次，
# 2.乱序只依靠自身单词组合，不另存放编码规则。
# 3.12个单词排列组合为12的阶乘4.79亿次，其实也足够了，我这里取24词，反正天文数字，看到也排不出来。
# 4.试想黑客拿到你的助记词了，第一时间是干什么，不是继续控制你电脑，而可能是清理环境，清理痕迹赶紧走人，但结果全部无法导入。。。

# 1. **首字母编码**：将单词的首字母（a-z，排除X）映射为数值（a=0, b=1, ..., z=24）。
# 2. **固定锚点**：保持第一个单词位置不变，仅对剩余单词操作乱序。
# 3. **再首单词跟其他位置单词做一次交换，避免掉这个固定规则，这样只需要自己工具封装好两个函数即可。

import random
# 首字母到数值的映射（a=0, b=1, ..., z=24，排除x）
letters = [chr(97 + i) for i in range(26) if chr(97 + i) != 'x']
letter_to_num = {c: i for i, c in enumerate(letters)}
# 乱序函数
def shuffle_words(words):
    if not words:
        return []
    first = [words[0]]
    rest = words[1:]
    # 计算种子：所有首字母数值之和
    seed = sum(letter_to_num[w[0].lower()] for w in rest)
    random.seed(seed*400)
    indices = list(range(len(rest)))
    random.shuffle(indices)
    shuffled_rest = [rest[i] for i in indices]
    print(shuffled_rest)
    ret=first+shuffled_rest
    ret[0], ret[-1] = ret[-1], ret[0]#首尾交换下
    return ret
# 还原函数
def restore_words(shuffled):
    if not shuffled:
        return []
    shuffled[0], shuffled[-1] = shuffled[-1], shuffled[0]#首尾交换下
    first = [shuffled[0]]
    rest = shuffled[1:]
    # 重新计算种子（与乱序时相同）
    seed = sum(letter_to_num[w[0].lower()] for w in rest)
    random.seed(seed*400)
    indices = list(range(len(rest)))
    random.shuffle(indices)
    # 构建逆排列以恢复原始顺序
    inverse = [0] * len(indices)
    for i, pos in enumerate(indices):
        inverse[pos] = i
    restored_rest = [rest[pos] for pos in inverse]
    return first + restored_rest


# 示例单词列表（首字母为a-w, y, z）,注意只是示例测试，不是BIP39的单词 ...
original_words = [
    "Owl", "is", "very", "handsome", "are","Banana", "Cat", "Dog", "Eagle", "Fox", "Giraffe",  "Jaguar", "Kangaroo",
    "Lion", "Monkey", "Nightingale", "Penguin", "Quail", "Rabbit", "Snake","The", "Unicorn", "Yak", "Zebra"
]

print("原始词:", original_words)
# 乱序操作
shuffled = shuffle_words(original_words)
print("乱序后:", shuffled)

# 还原操作
restored = restore_words(shuffled)
print("还原后:", restored)


if restored == original_words:
    print("乱序还原验证成功！")
