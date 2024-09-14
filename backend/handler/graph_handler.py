from graphviz import Digraph


class GraphvizHandler:
    """
    Graphvizを扱うハンドラー
    """

    def __init__(self, graph_format: str) -> None:
        self.__graph: Digraph = Digraph(strict=True, format=graph_format)
        self.__graph.clear(keep_attrs=False)
        self.__graph.attr(
            'node',
            color='lightblue2',
            style='filled',
            shape='record',
            fontname='MS Gothic'
        )
        self.__max_label_len: int = 65

    def add_node(self, node: str, formula: str ="") -> None:
        """
        グラフにノードを追加する
        """
        label = "{" + f"{self.__escape_char(node)}|{self.__escape_char(formula)}" + "}"
        self.__graph.node(
            self.__escape(node),
            label=label
        )

    def add_edge(self, start: str, target: str) -> None:
        """
        グラフにエッジを追加する
        """
        self.__graph.edge(
            self.__escape(start),
            self.__escape(target)
        )

    def has_node(self, node: str) -> bool:
        """
        ノードが存在するかどうかを調べる
        """
        return self.__escape(node) in self.__graph.body

    def get_graph(self) -> Digraph:
        """
        グラフを取得する
        """
        return self.__graph

    def __escape(self, txt: str) -> str:
        return txt.replace(':', '')

    def __escape_char(self, txt: str) -> str:
        if len(txt) > self.__max_label_len:
            txt = txt[:self.__max_label_len] + "..."

        return txt.replace("<", "\\<").replace(">", "\\>").\
            replace("\"", "\\\"").replace("{", "\\{").replace("}", "\\}")
