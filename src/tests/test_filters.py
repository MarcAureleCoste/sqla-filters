import os
import json

import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
import pytest

from sqla_filters.nodes.logical import AndNode
from sqla_filters.nodes.operational import (
    EqNode,
    NotEqNode,
    GtNode,
    GteNode,
    LtNode,
    LteNode,
    ContainsNode,
    LikeNode,
    InNode,
    NotInNode,
    NullNode,
    NotNullNode
)
from sqla_filters.tree import SqlaFilterTree
from .db import Base
from .loader import load_models
from .models import (
    Simple,
    Person,
    Author,
    Post
)


def removeTestDb():
    os.remove('test.db')

@pytest.fixture(scope='session', autouse=True)
def load_test_models(request):
    engine = sa.create_engine('sqlite:///test.db')
    DBSession = sessionmaker(bind=engine)
    Base.metadata.create_all(engine)
    session = DBSession()
    load_models(session)
    # Run callback 'removeTestDb' when all tests are finished
    request.addfinalizer(removeTestDb)


class TestBasicRequest(object):
    def setup_class(self):
        self._engine = sa.create_engine('sqlite:///test.db')
        self._DBSession = sessionmaker(bind=self._engine)
        self._session = self._DBSession()

    def teardown_class(self):
        self._session.close()

    def test_1_count(self):
        count = self._session \
            .query(Simple) \
            .count()
        assert count == 4

    def test_2_simple_request(self):
        entity = self._session \
            .query(Simple) \
            .filter_by(name='Toto') \
            .first()
        assert entity.name == 'Toto'
        assert entity.age == 20


class TestFilterEquality(object):
    def setup_class(self):
        self._engine = sa.create_engine('sqlite:///test.db')
        self._DBSession = sessionmaker(bind=self._engine)
        self._session = self._DBSession()

    def teardown_class(self):
        self._session.close()

    def test_1_eq(self):
        and_node = AndNode()
        eq_node = EqNode('name', 'Toto')
        and_node.childs.append(eq_node)
        tree = SqlaFilterTree(and_node)

        query = self._session \
            .query(Simple)
        result = tree.filter(query).first()
        assert result.name == 'Toto'
        assert result.age == 20
        assert result.average == 10

    def test_2_not_eq(self):
        and_node = AndNode()
        not_eq_node = NotEqNode('name', 'Toto')
        and_node.childs.append(not_eq_node)
        tree = SqlaFilterTree(and_node)

        query = self._session \
            .query(Simple)
        results = tree.filter(query).all()
        assert len(results) == 3

    def test_3_eq_relation(self):
        and_node = AndNode()
        eq_node = EqNode('author.person.name', 'Person_1')
        and_node.childs.append(eq_node)
        tree = SqlaFilterTree(and_node)

        query = self._session \
            .query(Post)
        results = tree.filter(query).first()
        assert results.title == 'post_1'
        assert results.content == 'content_1'

    def test_4_not_eq_relation(self):
        and_node = AndNode()
        not_eq_node = NotEqNode('author.person.name', 'Person_1')
        and_node.childs.append(not_eq_node)
        tree = SqlaFilterTree(and_node)

        query = self._session \
            .query(Post)
        results = tree.filter(query).all()
        assert len(results) == 4
        assert results[0].title == 'post_2'
        assert results[0].content == 'content_2'
        assert results[1].title == 'post_3'
        assert results[1].content == 'content_3'
        assert results[2].title == 'post_5'
        assert results[2].content == 'content_5'
        assert results[3].title == 'post_6'
        assert results[3].content == 'content_6'


class TestFilterGreater(object):
    def setup_class(self):
        self._engine = sa.create_engine('sqlite:///test.db')
        self._DBSession = sessionmaker(bind=self._engine)
        self._session = self._DBSession()

    def teardown_class(self):
        self._session.close()

    def test_1_gt(self):
        and_node = AndNode()
        gt_node = GtNode('age', 21)
        and_node.childs.append(gt_node)
        tree = SqlaFilterTree(and_node)

        query = self._session \
            .query(Simple)
        results = tree.filter(query).all()
        assert len(results) == 2

    def test_2_gte(self):
        and_node = AndNode()
        gte_node = GteNode('age', 21)
        and_node.childs.append(gte_node)
        tree = SqlaFilterTree(and_node)

        query = self._session \
            .query(Simple)
        results = tree.filter(query).all()
        assert len(results) == 3

    def test_3_gt_relation(self):
        and_node = AndNode()
        gt_node = GtNode('author.posts.pages', 7)
        and_node.childs.append(gt_node)
        tree = SqlaFilterTree(and_node)

        query = self._session \
            .query(Person)
        results = tree.filter(query).all()
        assert len(results) == 1
        assert results[0].name == 'Person_3'

    def test_4_gte_relation(self):
        and_node = AndNode()
        gte_node = GteNode('author.posts.pages', 7)
        and_node.childs.append(gte_node)
        tree = SqlaFilterTree(and_node)

        query = self._session \
            .query(Person)
        results = tree.filter(query).all()
        assert len(results) == 2
        assert results[0].name == 'Person_1'
        assert results[1].name == 'Person_3'


class TestFilterLower(object):
    def setup_class(self):
        self._engine = sa.create_engine('sqlite:///test.db')
        self._DBSession = sessionmaker(bind=self._engine)
        self._session = self._DBSession()

    def teardown_class(self):
        self._session.close()

    def test_1_lt(self):
        and_node = AndNode()
        lt_node = LtNode('age', 23)
        and_node.childs.append(lt_node)
        tree = SqlaFilterTree(and_node)

        query = self._session \
            .query(Simple)
        results = tree.filter(query).all()
        assert len(results) == 3

    def test_2_lte(self):
        and_node = AndNode()
        lte_node = LteNode('age', 23)
        and_node.childs.append(lte_node)
        tree = SqlaFilterTree(and_node)

        query = self._session \
            .query(Simple)
        results = tree.filter(query).all()
        assert len(results) == 4

    def test_3_lt_relation(self):
        and_node = AndNode()
        lt_node = LtNode('author.posts.pages', 4)
        and_node.childs.append(lt_node)
        tree = SqlaFilterTree(and_node)

        query = self._session \
            .query(Person)
        results = tree.filter(query).all()
        assert len(results) == 2
        assert results[0].name == 'Person_1'
        assert results[1].name == 'Person_3'

    def test_4_lte_relation(self):
        and_node = AndNode()
        lte_node = LteNode('author.posts.pages', 4)
        and_node.childs.append(lte_node)
        tree = SqlaFilterTree(and_node)

        query = self._session \
            .query(Person)
        results = tree.filter(query).all()
        assert len(results) == 3
        assert results[0].name == 'Person_1'
        assert results[1].name == 'Person_3'
        assert results[2].name == 'Person_2'

class TestFilterContains(object):
    def setup_class(self):
        self._engine = sa.create_engine('sqlite:///test.db')
        self._DBSession = sessionmaker(bind=self._engine)
        self._session = self._DBSession()

    def teardown_class(self):
        self._session.close()

    def test_1_contains(self):
        and_node = AndNode()
        contains_node = ContainsNode('name', 'to')
        and_node.childs.append(contains_node)
        tree = SqlaFilterTree(and_node)

        query = self._session \
            .query(Simple)
        results = tree.filter(query).all()
        assert len(results) == 1
        assert results[0].name == 'Toto'
        assert results[0].age == 20
        assert results[0].average == 10


class TestFilterLike(object):
    def setup_class(self):
        self._engine = sa.create_engine('sqlite:///test.db')
        self._DBSession = sessionmaker(bind=self._engine)
        self._session = self._DBSession()

    def teardown_class(self):
        self._session.close()

    def test_1_like(self):
        and_node = AndNode()
        like_node = LikeNode('name', 'Pers%')
        and_node.childs.append(like_node)
        tree = SqlaFilterTree(and_node)

        query = self._session \
            .query(Person)
        results = tree.filter(query).all()
        assert len(results) == 3

    def test_2_like(self):
        and_node = AndNode()
        like_node = LikeNode('name', '%_1')
        and_node.childs.append(like_node)
        tree = SqlaFilterTree(and_node)

        query = self._session \
            .query(Person)
        results = tree.filter(query).all()
        assert len(results) == 1

    def test_3_like(self):
        and_node = AndNode()
        like_node = LikeNode('name', '%son_%')
        and_node.childs.append(like_node)
        tree = SqlaFilterTree(and_node)

        query = self._session \
            .query(Person)
        results = tree.filter(query).all()
        assert len(results) == 3


class TestFilterIn(object):
    def setup_class(self):
        self._engine = sa.create_engine('sqlite:///test.db')
        self._DBSession = sessionmaker(bind=self._engine)
        self._session = self._DBSession()

    def teardown_class(self):
        self._session.close()

    def test_1_in(self):
        and_node = AndNode()
        in_node = InNode('name',  ['Toto', 'Titi'])
        and_node.childs.append(in_node)
        tree = SqlaFilterTree(and_node)

        query = self._session \
            .query(Simple)
        results = tree.filter(query).all()
        assert len(results) == 2
        assert results[0].name == 'Toto'
        assert results[0].age == 20
        assert results[0].average == 10
        assert results[1].name == 'Titi'
        assert results[1].age == 21
        assert results[1].average == 12.3

    def test_2_not_in(self):
        and_node = AndNode()
        not_in_node = NotInNode('name', ['Toto', 'Titi'])
        and_node.childs.append(not_in_node)
        tree = SqlaFilterTree(and_node)

        query = self._session \
            .query(Simple)
        results = tree.filter(query).all()
        assert len(results) == 2
        assert results[0].name == 'Tutu'
        assert results[0].age == 22
        assert results[0].average == 9.6
        assert results[1].name == 'Tata'
        assert results[1].age == 23
        assert results[1].average == None

    def test_3_in_relation(self):
        and_node = AndNode()
        in_node = InNode('author.person.name', ['Person_1', 'Person_3'])
        and_node.childs.append(in_node)
        tree = SqlaFilterTree(and_node)

        query = self._session \
            .query(Post)
        results = tree.filter(query).all()
        assert len(results) == 4
        assert results[0].title == 'post_1'
        assert results[0].content == 'content_1'
        assert results[1].title == 'post_3'
        assert results[1].content == 'content_3'
        assert results[2].title == 'post_4'
        assert results[2].content == 'content_4'
        assert results[3].title == 'post_6'
        assert results[3].content == 'content_6'

    def test_4_not_in_relation(self):
        and_node = AndNode()
        not_in_node = NotInNode('author.person.name', ['Person_1', 'Person_3'])
        and_node.childs.append(not_in_node)
        tree = SqlaFilterTree(and_node)

        query = self._session \
            .query(Post)
        results = tree.filter(query).all()
        assert len(results) == 2
        assert results[0].title == 'post_2'
        assert results[0].content == 'content_2'
        assert results[1].title == 'post_5'
        assert results[1].content == 'content_5'


class TestFilterNull(object):
    def setup_class(self):
        self._engine = sa.create_engine('sqlite:///test.db')
        self._DBSession = sessionmaker(bind=self._engine)
        self._session = self._DBSession()

    def teardown_class(self):
        self._session.close()

    def test_1_null(self):
        and_node = AndNode()
        null_node = NullNode('average')
        and_node.childs.append(null_node)
        tree = SqlaFilterTree(and_node)

        query = self._session \
            .query(Simple)
        result = tree.filter(query).first()
        assert result.name == 'Tata'
        assert result.age == 23
        assert result.average == None

    def test_2_not_null(self):
        and_node = AndNode()
        not_null_node = NotNullNode('average')
        and_node.childs.append(not_null_node)
        tree = SqlaFilterTree(and_node)

        query = self._session \
            .query(Simple)
        results = tree.filter(query).all()
        assert len(results) == 3


class TestFilterDatetime(object):
    def setup_class(self):
        self._engine = sa.create_engine('sqlite:///test.db')
        self._DBSession = sessionmaker(bind=self._engine)
        self._session = self._DBSession()

    def teardown_class(self):
        self._session.close()

    def test_1_datetime(self):
        and_node = AndNode()
        gt_node = GtNode('pub_date', '2018-04-01 10:45:23')
        and_node.childs.append(gt_node)
        tree = SqlaFilterTree(and_node)

        query = self._session \
            .query(Post)
        results = tree.filter(query).all()
        assert len(results) == 2
        assert results[0].title == 'post_5'
        assert results[1].title == 'post_6'

    def test_2_datetime_relation(self):
        and_node = AndNode()
        gt_node = GtNode('posts.pub_date', '2018-05-01 10:45:23')
        and_node.childs.append(gt_node)
        tree = SqlaFilterTree(and_node)

        query = self._session \
            .query(Author)
        results = tree.filter(query).all()
        assert len(results) == 1
        assert results[0].author_name == 'author_3'


class TestFilterDate(object):
    def setup_class(self):
        self._engine = sa.create_engine('sqlite:///test.db')
        self._DBSession = sessionmaker(bind=self._engine)
        self._session = self._DBSession()

    def teardown_class(self):
        self._session.close()

    def test_1_date(self):
        and_node = AndNode()
        gt_node = GtNode('pub_date', '2018-04-01')
        and_node.childs.append(gt_node)
        tree = SqlaFilterTree(and_node)

        query = self._session \
            .query(Post)
        results = tree.filter(query).all()
        assert len(results) == 3
        assert results[0].title == 'post_4'
        assert results[1].title == 'post_5'
        assert results[2].title == 'post_6'

    def test_2_date(self):
        and_node = AndNode()
        gt_node = GtNode('posts.pub_date', '2018-05-01')
        and_node.childs.append(gt_node)
        tree = SqlaFilterTree(and_node)

        query = self._session \
            .query(Author)
        results = tree.filter(query).all()
        assert len(results) == 2
        assert results[0].author_name == 'author_2'
        assert results[1].author_name == 'author_3'
