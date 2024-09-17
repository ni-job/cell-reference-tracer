from collections import deque
from collections.abc import Iterator
from itertools import tee
from typing import Any

from backend.domain.formula_analyzer import FormulaAnalyzer
from backend.handler.graph_handler import GraphvizHandler
from backend.handler.excel_handler import ExcelHandler, ArrayFormula, CellRichText


class CellTracer:
    """
    セルの参照元をたどるクラス
    """

    def __init__(
            self, excel_handler: ExcelHandler, graph_handler: GraphvizHandler, max_trace_size: int
        ):
        self.__cell_dq: deque[tuple[str, str | None, str | None]]
        self.__excel_hdl: ExcelHandler = excel_handler
        self.__graph_hdl: GraphvizHandler = graph_handler

        self.dq_maxsize = 50000
        self.__max_trace_size = max_trace_size

    def make_graph(self, sheet_name: str, row: int, clm: int) -> None:
        """
        指定したセルの参照元をたどってGraphvizのグラフを作成する

        params:
            sheet_name: シート名
            row: セルの行番号
            clm: セルの列番号
        """

        self.__cell_dq = deque()

        # dequeに最初のセルを追加する
        cell_address: str = f"{sheet_name}!{self.__excel_hdl.get_column_letter(clm)}{row}"
        cell_formula: str | None = self.__formula(sheet_name, row, clm)
        self.__cell_dq.append((cell_address, cell_formula, None))

        while len(self.__cell_dq) > 0:
            if len(self.__cell_dq) > self.dq_maxsize:
                Exception(f"参照元の数が{self.dq_maxsize}を超えたため中断しました")

            (cell_address, cell_formula, parent_cell_address) = self.__cell_dq.popleft()

            # グラフにノードとエッジを追加する
            self.__add_graph(cell_address, cell_formula, parent_cell_address)

            if cell_formula is None:
                continue

            # 参照元を取得する
            formula_analyzer: FormulaAnalyzer = FormulaAnalyzer(
                cell_formula, cell_address.split('!')[0], self.__excel_hdl
            )
            references = formula_analyzer.get_cells_from_tokenized()

            # 各参照元をdequeに追加する
            for reference_cell in references:
                self.__add_deque(reference_cell, cell_address)

                if self.__is_range(reference_cell):
                    self.__add_range_cell(reference_cell)

    def __add_range_cell(self, range_cell_address: str) -> None:
        sheet_name, cell_coor = range_cell_address.split('!')
        range_cells: Iterator = self.__excel_hdl.cells_from_range(cell_coor)
        range_cells, copy_range_cells = tee(range_cells)
        range_cells_size: int = sum(1 for _ in copy_range_cells)

        # アンパック最大数以下なら参照元の各セルのノードを追加する
        if range_cells_size <= self.__max_trace_size:
            for c in range_cells:
                self.__add_deque(f"{sheet_name}!{c}", range_cell_address)

    def __is_range(self, cell: str) -> bool:
        _, cell_coor = cell.split('!')
        return ':' in cell_coor

    def __add_deque(self, cell_address: str, parent_cell_address: str) -> None:
        sheet_name, cell_coor = cell_address.split('!')

        if self.__is_range(cell_address):
            cell_formula = ""
        else:
            row, clm = self.__excel_hdl.coordinate_to_tuple(cell_coor)
            cell_formula = self.__formula(sheet_name, row, clm)

        if not self.__graph_hdl.has_node(cell_address, cell_formula):
            self.__cell_dq.append((cell_address, cell_formula, parent_cell_address))

    def __add_graph(
            self, added_cell_address: str, formula: str | None, from_node: str | None
        ) -> None:
        if formula is None:
            formula = ""

        self.__graph_hdl.add_node(added_cell_address, formula)

        if from_node is not None:
            self.__graph_hdl.add_edge(from_node, added_cell_address)

    def __formula(self, sheet_name: str, row: int, clm: int) -> str:
        val: (Any | str | CellRichText | None) = self.__excel_hdl.get(sheet_name, row, clm)

        if val is None:
            val = ""

        if isinstance(val, ArrayFormula):
            val = val.text

        return str(val)
