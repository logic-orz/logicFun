import warnings
from decimal import Decimal
import re


def moneyNum2Char(value, capital=True, prefix=False, classical=None):
    '''
    人民币数字转大写汉字,参数:
    capital:    True   大写汉字金额
                False  一般汉字金额
    classical:  True   元
                False  圆
    prefix:     True   以'人民币'开头
                False, 无开头
    '''
    if not isinstance(value, (Decimal, str, int)):
        msg = '''由于浮点数精度问题，请考虑使用字符串，或者 decimal.Decimal 类。'''
        warnings.warn(msg, UserWarning)
    # 默认大写金额用圆，一般汉字金额用元
    if classical is None:
        classical = True if capital else False

    # 汉字金额前缀
    if prefix is True:
        prefix = '人民币'
    else:
        prefix = ''

    # 汉字金额字符定义
    dunit = ('角', '分')
    if capital:
        num = ('零', '壹', '贰', '叁', '肆', '伍', '陆', '柒', '捌', '玖')
        iunit = [None, '拾', '佰', '仟', '万', '拾', '佰',
                 '仟', '亿', '拾', '佰', '仟', '万', '拾', '佰', '仟']
    else:
        num = ('〇', '一', '二', '三', '四', '五', '六', '七', '八', '九')
        iunit = [None, '十', '百', '千', '万', '十', '百',
                 '千', '亿', '十', '百', '千', '万', '十', '百', '千']
    if classical:
        iunit[0] = '元' if classical else '圆'
    # 转换为Decimal，并截断多余小数

    if not isinstance(value, Decimal):
        value = Decimal(value).quantize(Decimal('0.01'))

    # 处理负数
    if value < 0:
        prefix += '负'  # 输出前缀，加负
        value = - value  # 取正数部分，无须过多考虑正负数舍入
        # assert - value + value == 0
    # 转化为字符串
    s = str(value)
    if len(s) > 19:
        raise ValueError('金额太大了，不知道该怎么表达。')
    istr, dstr = s.split('.')  # 小数部分和整数部分分别处理
    istr = istr[::-1]  # 翻转数部分字符串
    so = []  # 用于记录转换结果

    # 零
    if value == 0:
        return prefix + num[0] + iunit[0]
    haszero = False  # 用于标记零的使用
    if dstr == '0':  # 数字精度不够，补0
        dstr = '00'
    if dstr == '00':
        haszero = True  # 如果无小数部分，则标记加过零，避免出现“圆零整”

    # 处理小数部分
    # 分
    if dstr[1] != '0':
        so.append(dunit[1])
        so.append(num[int(dstr[1])])
    else:
        so.append('整')  # 无分，则加“整”
    # 角
    if dstr[0] != '0':
        so.append(dunit[0])
        so.append(num[int(dstr[0])])
    elif dstr[1] != '0':
        so.append(num[0])  # 无角有分，添加“零”
        haszero = True  # 标记加过零了

    # 无整数部分
    if istr == '0':
        if haszero:  # 既然无整数部分，那么去掉角位置上的零
            so.pop()
        so.append(prefix)  # 加前缀
        so.reverse()  # 翻转
        return ''.join(so)

    # 处理整数部分
    for i, n in enumerate(istr):
        n = int(n)
        if i % 4 == 0:  # 在圆、万、亿等位上，即使是零，也必须有单位
            if i == 8 and so[-1] == iunit[4]:  # 亿和万之间全部为零的情况
                so.pop()  # 去掉万
            so.append(iunit[i])
            if n == 0:  # 处理这些位上为零的情况
                if not haszero:  # 如果以前没有加过零
                    so.insert(-1, num[0])  # 则在单位后面加零
                    haszero = True  # 标记加过零了
            else:  # 处理不为零的情况
                so.append(num[n])
                haszero = False  # 重新开始标记加零的情况
        else:  # 在其他位置上
            if n != 0:  # 不为零的情况
                so.append(iunit[i])
                so.append(num[n])
                haszero = False  # 重新开始标记加零的情况
            else:  # 处理为零的情况
                if not haszero:  # 如果以前没有加过零
                    so.append(num[0])
                    haszero = True

    # 最终结果
    so.append(prefix)
    so.reverse()
    return ''.join(so)


def moneyChar2Num(amount: str):
    chinese_num = {'零': 0, '壹': 1, '贰': 2, '叁': 3,
                   '肆': 4, '伍': 5, '陆': 6, '柒': 7, '捌': 8, '玖': 9}
    chinese_amount = {'分': 0.01, '角': 0.1, '元': 1,
                      '拾': 10, '佰': 100, '仟': 1000, '圆': 1}
    amount_float = 0
    if '亿' in amount:
        yi = re.match(r'(.+)亿.*', amount).group(1)
        amount_yi = 0
        for i in chinese_amount:
            if i in yi:
                amount_yi += chinese_num[yi[yi.index(i) - 1]] * \
                    chinese_amount[i]
        if yi[-1] in chinese_num.keys():
            amount_yi += chinese_num[yi[-1]]
        amount_float += amount_yi * 100000000
        amount = re.sub(r'.+亿', '', amount, count=1)
    if '万' in amount:
        wan = re.match(r'(.+)万.*', amount).group(1)
        amount_wan = 0
        for i in chinese_amount:
            if i in wan:
                amount_wan += chinese_num[wan[wan.index(i) - 1]] * \
                    chinese_amount[i]
        if wan[-1] in chinese_num.keys():
            amount_wan += chinese_num[wan[-1]]
        amount_float += amount_wan * 10000
        amount = re.sub(r'.+万', '', amount, count=1)

    amount_yuan = 0
    for i in chinese_amount:
        if i in amount:
            if amount[amount.index(i) - 1] in chinese_num.keys():
                amount_yuan += chinese_num[amount[amount.index(
                    i) - 1]] * chinese_amount[i]
    amount_float += amount_yuan

    return amount_float


def isNumberStr(s: str) -> bool:
    try:
        float(s)
        return True
    except ValueError:
        pass
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False


def isIdCard(idStr) -> bool:
    """
    判断是否为身份证
    """
    if len(idStr) == 18:  # 校验省份证长度是否是18位
        num17 = idStr[0:17]
        if not isNumberStr(num17):
            return False
        last_num = idStr[-1]  # 截取前17位和最后一位
        moduls = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
        num17 = map(int, num17)
        num_tuple = zip(num17, moduls)  # [(1, 4), (2, 5), (3, 6)]
        num = map(lambda x: x[0]*x[1], num_tuple)
        mod = sum(num) % 11
        yushu1 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        yushu2 = [1, 0, 'X', 9, 8, 7, 6, 5, 4, 3, 2]
        last_yushu = dict(zip(yushu1, yushu2))
        if last_num == str(last_yushu[mod]):
            return True
        else:
            return False
    else:
        return False


def toCamel(name: str) -> str:
    """下划线转驼峰命名"""
    return re.sub('_([a-zA-Z])', lambda m: (m.group(1).upper()), name.lower())


def toSnake(name: str) -> str:
    """驼峰转下划线命名"""
    if '_' not in name:
        name = re.sub(r'([a-z])([A-Z])', r'\1_\2', name)
    else:
        raise ValueError(f'{name}字符中包含下划线，无法转换')
    return name.lower()
