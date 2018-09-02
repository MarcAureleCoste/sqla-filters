import json
import ast
from abc import (
    ABC,
    abstractmethod
)
from typing import Any

from ..filter import (
    TreeNode,
    OrNode,
    AndNode,
    SqlaFilterTree,
    OPERATOR_NODES,
    LOGICAL_NODES
)
from .exceptions import FiltersParserTypeError


def validate_element(e_type, e_value) -> bool:
    if not e_type or not e_value:
        return False
    if (e_type == 'and' or e_type == 'or') and not isinstance(e_value, list):
        return False
    return True


class JSONFiltersParser(object):
    def __init__(self, json_str: str, attr_sep: str = '.') -> None:
        self._raw_data = json_str
        self._attr_sep = attr_sep  # Global attr_sep
        self._filters_tree = self._generate_filters_tree()

    @property
    def raw_data(self) -> str:
        return self._raw_data

    @property
    def attr_sep(self) -> str:
        """Return the current attriute separator."""
        return self._attr_sep

    @attr_sep.setter
    def attr_sep(self, new_sep: str) -> None:
        """Set the new value for the attribute separator.
        
        When the new value is assigned a new tree is generated.
        """
        self._attr_sep = new_sep
        self._filters_tree = self._generate_filters_tree()

    @property
    def tree(self) -> SqlaFilterTree:
        return self._filters_tree

    def _create_node(self, key: str, data: Any) -> TreeNode:
        # TODO: Correct the mypy error
        if key == 'and' or key == 'or':
            return LOGICAL_NODES[key]()
        elif key == 'operator':
            operator = data.get('operator')
            attr_sep = data.get('attr_sep', None)  # Per node attr_sep
            return OPERATOR_NODES[operator](
                data.get('attribute', ''),
                data.get('value', None),
                attr_sep=attr_sep if attr_sep else self._attr_sep
            )
        else:
            raise FiltersParserTypeError('Unknown key.')

    def _generate_nodes(self, key: str, data: Any) -> TreeNode:
        node = self._create_node(key, data)
        if isinstance(node, AndNode) or isinstance(node, OrNode):
            for element in data:
                e_type = element.get('type', None)
                e_data = element.get('data', None)
                node.childs.append(self._generate_nodes(e_type, e_data))
        return node

    def _generate_filters_tree(self) -> SqlaFilterTree:
        json_dict = json.loads(self._raw_data)
        r_type = json_dict.get('type', None)
        r_data = json_dict.get('data', None)
        if not validate_element(r_type, r_data):
            raise FiltersParserTypeError('Invalid json')
        return SqlaFilterTree(self._generate_nodes(r_type, r_data))
