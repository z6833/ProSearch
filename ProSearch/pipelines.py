# -*- coding: utf-8 -*-
from openpyxl import Workbook

class ProsearchPipeline(object):

    def __init__(self):
        # 创建excel表格保存数据
        self.workbook = Workbook()
        self.booksheet = self.workbook.active
        self.booksheet.append(['关键词', '项目编号', '项目类别', '学科类别', '项目名称', '立项时间', '负责人', '工作单位', '单位类别', '所在省市', '所属系统'])

    def process_item(self, item, spider):

        DATA = [
            item['keyword'], item['pronums'], item['protype'], item['subtype'], item['proname'], item['protime'], item['leaders'], item['workloc'], item['orgtype'], item['provloc'], item['systloc']
        ]

        self.booksheet.append(DATA)
        self.workbook.save('./data/ProSearch.xls')
        return item
