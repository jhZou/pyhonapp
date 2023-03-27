import pandas as pd
import datetime


# 加载汉字笔画对照文件，参考同级目录下的 chinese_unicode_table.txt 文件格式
def init_list(file):
    allwords_list = []
    with open(file, 'r', encoding='UTF-8') as f:
        lines = f.readlines()
        for line in lines:
            line_info = line.strip().split(' ')
            allwords_list.extend(line_info)
    return allwords_list

def word_dict():
    #1.初始化笔画的字典
    chinese_char_map = {}
    with open('./chinese_unicode_table.txt', 'r', encoding='UTF-8') as f:
        lines = f.readlines()
        for line in lines[6:]:  # 前6行是表头，去掉
            line_info = line.strip().split()
            # 处理后的数组第一个是文字，第7个是笔画数量
            chinese_char_map[line_info[0]] = line_info[6]
    return chinese_char_map


def count_word(dict,list1,list2):
        allnamemerge=[]
        dictname1 = {}
        toexcelist = []
        #1.遍历第一个列表
        counlistlen=0
        for jw in list1:
            # 1.遍历第二个列表，做计算笔画和判断
            for tw in list2:
                #print(jw,tw)
                #笔画总数初始化为0
                count = 0
                #遍历字典拿到笔画数
                for k,v in dict.items():
                    #int v
                    #判断组合的两个字是否在字典，获取笔画数
                    if k == jw or k == tw:
                        #print(k,v)
                        #两个字的笔画数累加
                        count +=int(v)
                #如果笔画数在大吉的列表里面，则加入导出excel的字典中
                if count in [5,8,9,10,11,14,16,17,18,22,24,25,28,30,32,34]:
                    #for times in (0,2):])
                    dictname = {}
                    dictname['name'] = jw+tw
                    dictname['countline'] = count
                    toexcelist.append(dictname)
                    dictname = {}
                    dictname['name'] = tw+jw
                    dictname['countline'] = count
                    toexcelist.append(dictname)

                    allnamemerge.append(jw + tw)
                    dictname1[jw+tw] = count
                    dictname1[tw+jw] = count
                    print(allnamemerge)
        return toexcelist

def export_excel(export):
    ctime = datetime.datetime.now().strftime('%Y%m%d%H%M')
    excelname = str('组合名字') + ctime +  str('xlsx')
    # 将字典列表转换为DataFrame
    pf = pd.DataFrame(list(export))
    # 指定字段顺序
    order = ['name', 'countline']
    pf = pf[order]
    # 将列名替换为中文
    columns_map = {
            'name': '名字组合',
            'countline': '笔画数'
    }
    pf.rename(columns=columns_map, inplace=True)
    # 指定生成的Excel表格名称
    file_path = pd.ExcelWriter('名字组合' + ctime + '.xlsx')
    # 替换空单元格
    pf.fillna(' ', inplace=True)
    # 输出
    pf.to_excel(file_path, encoding='utf-8', index=False)
    # 保存表格
    file_path.save()

if __name__ == '__main__':
    dictword = word_dict()
    firstlist = init_list('tuword.txt')
    seconflist = init_list('jinword.txt')
    dict2excel = count_word(dictword,firstlist,seconflist)
    export_excel(dict2excel)