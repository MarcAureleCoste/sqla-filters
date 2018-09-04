"""base module of filter package.

These class are used to represent the filters to apply to a query.
"""
import abc
import datetime
from typing import (
    Any,
    List,
    Dict,
    Tuple,
    Optional,
    Iterator,
    Callable
)
from sqlalchemy import (
    Date,
    Time,
    DateTime
)
from sqlalchemy import or_
from sqlalchemy.orm.query import Query



class TreeNode(metaclass=abc.ABCMeta):
    def __init__(self) -> None:
        self._childs: List['TreeNode'] = []

    @abc.abstractmethod
    def filter(self, query, entity):
        raise NotImplementedError('You must implement this.')

    @property
    def childs(self) -> List['TreeNode']:
        return self._childs


class BaseOperatorNode(TreeNode):
    def __init__(
        self, 
        attribute: str, 
        value: Any, 
        attr_sep: str='.',
        # date_format: str='%Y-%m-%d',
        # time_format: str='%H:%M:%S',
        # datetime_format: str='%Y-%m-%d %H:%M:%S.%f'
    ) -> None:
        super(BaseOperatorNode, self).__init__()
        self._attribute = attribute
        self._value = value
        self._attr_sep = attr_sep
        # self._date_format = date_format
        # self._time_format = time_format
        # self._datetime_format = datetime_format

    @property
    def attribute(self) -> str:
        return self._attribute

    @property
    def value(self) -> Any:
        return self._value

    def _extract_relations(self, attribute: str) -> Tuple[List[str], str]:
        """Split and return the list of relation(s) and the attribute"""
        # splitted = attribute.split(self._relation_delimiter)
        splitted = attribute.split(self._attr_sep)
        return (splitted[:-1], splitted[-1])

    def _get_relation(self, related_model: type, relations: List[str]) -> Tuple[Optional[List[type]], Optional[type]]:
        relations_list, last_relation = [], related_model
        for relation in relations:
            relationship = getattr(last_relation, relation, None)
            if relationship is None:
                return (None, None)
            last_relation = relationship.mapper.class_
            relations_list.append(last_relation)
        return (relations_list, last_relation)

    def _join_tables(self, query: Query, join_models: Optional[List[type]]):
        """Method to make the join when relation is found."""
        joined_query = query
        # Create the list of already joined entities
        joined_tables = [mapper.class_ for mapper in query._join_entities]
        if join_models:
            for j_model in join_models:
                if not j_model in joined_tables:
                    # /!\ join return a new query /!\
                    joined_query = joined_query.join(j_model)
        return joined_query

    # def _value_to_date(self, value: str) -> datetime.datetime:
    #     return datetime.datetime.strptime(value, self._date_format)

    # def _value_to_time(self, value: str) -> datetime.datetime:
    #     return datetime.datetime.strptime(value, self._time_format)

    # def _value_to_datetime(self, value: str) -> datetime.datetime:
    #     return datetime.datetime.strptime(value, self._time_format)

    # def _get_field_value(self, field, value):
    #     f_type = field.property.columns[0].type  # Get field type
    #     if isinstance(f_type, DateTime) or isinstance(f_type, Date) or isinstance(f_type, Time):
    #         return self._value_to_date(value)
    #     return value

    def filter(self, query: Query, entity: type):
        raise NotImplementedError('You must implement this.')


class BaseLogicalNode(TreeNode):
    def __init__(self) -> None:
        super(BaseLogicalNode, self).__init__()
        self._method = or_

    def filter(self, query: Query, entity: type):
        new_query = query
        c_filter_list = []
        for child in self._childs:
            new_query, f_list = child.filter(new_query, entity)
            c_filter_list.append(f_list)
        return (
            new_query,
            self._method(*c_filter_list)
        )