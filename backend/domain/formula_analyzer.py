import re

from backend.handler.excel_handler import ExcelHandler, Token, Tokenizer


class FormulaAnalyzer:
    """
    数式を解析するクラス
    """

    def __init__(self, formula: str, sheet_name: str, excel_hdl: ExcelHandler):
        self.__formula: str = formula
        self.__current_sheet_name: str = sheet_name
        self.__excel_hdl: ExcelHandler = excel_hdl

        # Excelブック全体に定義された名前
        self.__wb_defined_name = self.__excel_hdl.defined_name()
        # シートに定義された名前
        self.__ws_defined_name = self.__excel_hdl.defined_name(sheet_name)

        self.__tables = self.__excel_hdl.tables()

    def get_cells_from_tokenized(self) -> list:
        """
        数式に含まれる参照元を解析して取得する
        """

        # 数式でない場合、参照元なし
        if not self.__is_formula():
            return []

        references: set = set()
        for item in self.__parse_formula().items:
            if item.type != Token.OPERAND:
                continue

            if item.subtype != Token.RANGE:
                continue

            reference = self.__format_reference(item.value)
            if reference is not None:
                references.add(reference)

        return list(references)

    def __format_reference(self, range_val: str) -> str | None:
        cell_txt = self.__get_cell_range(range_val)
        if cell_txt is None:
            return None

        if '!' not in cell_txt:
            cell_txt = f"{self.__current_sheet_name}!{cell_txt}"

        return self.__format_cell_txt(cell_txt)

    def __get_cell_range(self, cell_txt: str) -> str | None:
        # 定義された名前
        if cell_txt in self.__wb_defined_name.keys():
            return self.__wb_defined_name[cell_txt].value
        if cell_txt in self.__ws_defined_name.keys():
            return self.__ws_defined_name[cell_txt].value

        # テーブル
        if '[' in cell_txt:
            table_name = cell_txt.split('[')[0]
            table = self.__tables[table_name]
            return f"{table['sheet_name']}!{table['ref']}"

        cell_txt = self.__format_cell_txt(cell_txt)

        if '!' in cell_txt:
            _, cell = cell_txt.split('!')
        else:
            cell = cell_txt

        if self.__is_cell_format(cell) or self.__is_range_format(cell):
            return cell_txt

        # 参照元なし
        return None

    def __parse_formula(self) -> Tokenizer:
        """
        数式を以下のようにパースする
        =IF($A$1,"then True",MAX(DEFAULT_VAL,'Sheet 2'!B1))
                value      type  subtype
                IF(        FUNC     OPEN
                $A$1    OPERAND    RANGE
                ,           SEP      ARG
        "then True"     OPERAND     TEXT
                ,           SEP      ARG
                MAX(       FUNC     OPEN
        DEFAULT_VAL     OPERAND    RANGE
                ,           SEP      ARG
        'Sheet 2'!B1    OPERAND    RANGE
                )          FUNC    CLOSE
                )          FUNC    CLOSE
        
        https://openpyxl.readthedocs.io/en/latest/formula.html
        """
        return Tokenizer(self.__formula)

    def __is_formula(self) -> bool:
        if not isinstance(self.__formula, str) or len(self.__formula) == 0:
            return False

        return self.__formula[0] == '='

    def __format_cell_txt(self, cell_txt: str) -> str:
        """
        "$A$1"を"A1"に変換する
        """
        cell_txt = cell_txt.replace('$', '')
        cell_txt = cell_txt.replace('\'', '')
        return cell_txt

    def __is_cell_format(self, txt):
        pattern = "[A-Z]+[0-9]+"
        return re.match(pattern, txt)

    def __is_range_format(self, txt):
        pattern = "[A-Z]+[0-9]+:[A-Z]+[0-9]+"
        return re.match(pattern, txt)
