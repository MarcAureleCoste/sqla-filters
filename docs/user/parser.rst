====================
sqla-filters: Parser
====================

JSON Parser
-----------

This parser is included in the sqla-filters package. This is the default
parser.

.. _sqla-filters-parser-usage:

Usage
-----

For the example we will take a simple entity like the following:

.. code-block:: python

    class Post(Base):
        p_id = sa.Column(sa.Integer, primary_key=True)
        title = sa.Column(sa.String(100))
        content = sa.Column(sa.String)

        def __str__(self):
            return '{} | {}'.format(self.title, self.content)

and your JSON looks like:

.. code-block:: json

    {
        "type": "or",
        "data": [
            {
                "type": "operator",
                "data": {
                    "attribute": "title",
                    "operator": "eq",
                    "value": "Post_01"
                }
            },
            {
                "type": "operator",
                "data": {
                    "attribute": "title",
                    "operator": "eq",
                    "value": "Post_03"
                }
            }
        ]
    }

you can now use sqla-filter to filter your query and get only post with title
equal to 'Post_01' or 'Post_02'.

.. code-block:: python

    # Create a JSON parser instance
    parser = JSONFiltersParser(raw_json_string)

    # A tree is generated with the JSON received.
    # If you set the JSON the tree is automatically updated.
    print(parser.tree)

    # Now you can filter a query
    query = session.query(Post)
    filtered_query = parser.tree.filter(query)

    # Get the results
    # you can also directly call the `all()` from previous step
    # results = filtered_query = parser.tree.filter(query).all()
    results = query.all()

Create your own parser
----------------------

If you want to support a special format you can create and add your own
parser to the sqla_filters package.