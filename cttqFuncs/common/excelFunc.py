from typing import Any, List, Dict
import xlwt
import xlrd


class XlsWriter():

    def __init__(self) -> None:
        self.workbook = xlwt.Workbook(encoding="utf-8")

    def save(self, path):
        self.workbook.save(path)

    def createSheet(self, headers: List[str], datas: List[List[Any]],
                    sheetName: str):

        # 实例化book对象
        sheet = self.workbook.add_sheet(sheetName)  # 生成sheet

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
        self.workbook = xlrd.open_workbook(path)

    def sheetNames(self):
        return self.workbook.sheet_names()

    def readSheetByName(self, sheetName: str) -> List[Dict[str, Any]]:
        sh = self.workbook.sheet_by_name(sheetName)
        re = []
        for i in range(1, sh.nrows):
            d = dict(zip(sh.row_values(0), sh.row_values(i)))
            re.append(d)
        return re

    def readSheetByIndex(self, sheetIndex: int) -> List[Dict[str, Any]]:
        sh = self.workbook.sheet_by_index(sheetIndex)
        re = []
        for i in range(1, sh.nrows):
            d = dict(zip(sh.row_values(0), sh.row_values(i)))
            re.append(d)
        return re

