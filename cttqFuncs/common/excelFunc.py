'''
Author: Logic
Date: 2022-09-08 11:03:51
LastEditTime: 2022-09-26 19:33:23
Description: 
'''
from typing import Any, List, Dict
import xlwt
import xlrd2
import openpyxl
from cttqFuncs.basic.exClass import CommonException


class XlsWriter():

    def __init__(self, path: str) -> None:
        self.path = path

        if path.endswith('.xlsx'):
            self.isXlsx = True
            self.workbook = openpyxl.Workbook(write_only=True)
        elif path.endswith('.xls'):
            self.isXlsx = False
            self.workbook = xlwt.Workbook(encoding="utf-8")
        else:
            raise CommonException('文件类型不正确')

    

    def save(self):
        self.workbook.save(self.path)

    def createSheet(self, headers: List[str], datas: List[List[Any]],
                    sheetName: str):
        # 生成sheet
        if self.isXlsx:
           
            sheet = self.workbook.create_sheet(sheetName)
            # 写入标题
            sheet.append(headers)

            # 写入每一行
            for data in datas:
                sheet.append(data)
        else:

            sheet = self.workbook.add_sheet(sheetName)
            # 写入标题
            for col, column in enumerate(headers):
                sheet.write(0, col, column)

            # 写入每一行
            for row, data in enumerate(datas):
                for col, col_data in enumerate(data):
                    sheet.write(row + 1, col, col_data)

    def createSheetWithDict(self, dataList: List[Dict[str, Any]],
                            sheetName: str):
        headers = list(dataList[0].keys())
        datas = []
        for bill in dataList:
            tmp = []
            for t in headers:
                if t in bill and bill[t]:
                    tmp.append(bill[t])
                else:
                    tmp.append('')
            datas.append(tmp)
        self.createSheet(headers, datas, sheetName)


class XlsReader():

    def __init__(self, path) -> None:
        self.workbook = xlrd2.open_workbook(path)

    def sheetNames(self):
        return self.workbook.sheet_names()

    def readSheetByName(self, sheetName: str) -> List[Dict[str, Any]]:
        sh = self.workbook.sheet_by_name(sheetName)
        re = []
        headers = sh.row_values(0)
        for i in range(1, sh.nrows):
            d = dict(zip(headers, sh.row_values(i)))
            re.append(d)
        return re

    def readSheetByIndex(self, sheetIndex: int) -> List[Dict[str, Any]]:
        sh = self.workbook.sheet_by_index(sheetIndex)
        re = []
        headers = sh.row_values(0)
        for i in range(1, sh.nrows):
            d = dict(zip(headers, sh.row_values(i)))
            re.append(d)
        return re

    def readSheetAsMatrixByName(self, sheetName: str) -> List[Dict[str, Any]]:
        sh = self.workbook.sheet_by_name(sheetName)
        re = []
        for i in range(0, sh.nrows):
            re.append(sh.row_values(i))
        return re
