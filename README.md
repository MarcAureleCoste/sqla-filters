# Sqla-filters

![license](https://img.shields.io/pypi/l/sqla-filters.svg)
![wheel](https://img.shields.io/pypi/wheel/sqla-filters.svg)
![pyversions](https://img.shields.io/pypi/pyversions/sqla-filters.svg)

## Introduction 

The purpose of this project is to set the basic class so that you can create a tree that will be then used to filter a request made with the SQLAlchemy ORM.

Currently, the elements provided are as Follows:
- the nodes (see: the table Below)
- the class SqlaFilterTree which contains the tree and allows to print it.
- the class BaseSqlaParser which serves as the basis if you create a parser that allows generating a tree.

This project is also for me a way to experience the namespace packages.

## Installation

```bash
pip install sqla-filters
```

## Operators

The following operators are or will be implemented:

| support | operators |          name         |        code        |
|:-------:|:----------|:---------------------:|-------------------:|
|   [x]   | like      | like                  | like()             |
|   [x]   | eq        | equal                 | operators.eq       |
|   [x]   | not_eq    | not equal             | operators.ne       |
|   [x]   | null      | null                  | is None            |
|   [x]   | not_null  | not null              | is not None        |
|   [x]   | gt        | greater than          | operators.gt       |
|   [x]   | gte       | greater than or equal | operators.ge       |
|   [x]   | lt        | lower than            | operators.lt       |
|   [x]   | lte       | lower than or equal   | operators.le       |
|   [x]   | in        | in                    | in_()              |
|   [x]   | not_in    | not in                | ~.in_()            |
|   [x]   | contains  | contains              | operators.contains |


## Tree

This is an example of what a tree looks like.

```
                                      +----------------------+
                                      |                      |
                                      |          and         |
                                      |                      |
                                      -----------------------+
                                                 ||
                                                 ||
                                                 ||
                    +----------------------+     ||     +----------------------+
                    |                      |     ||     |                      |
                    |          or          <------------>      age == 21       |
                    |                      |            |                      |
                    +----------------------+            +----------------------+
                               ||
                               ||
                               ||
+----------------------+       ||       +----------------------+
|                      |       ||       |                      |
|     name == toto     <---------------->     name == tata     |
|                      |                |                      |
+----------------------+                +----------------------+
```

## Contribute

You can contribute to the project using different ways.

### 1 | Classical

Fork the repository and run the following command to install the dependencies and the dev dependencies.

`pip install -e '.[dev]'`

Pipenv `Pipefile` is also available if needed.

### 2 | Using namespace features

If you want to contribute using the namespace features it's really simple.
First create your own project and use the following directories structure.

    ProjectFolder
        |______src
                |______sqla_filters
                            |______parser

This is an example to create new parser.

You can find example with the following repositories:

- [sqla-filters-json](https://github.com/MarcAureleCoste/sqla-filters-json)
- [sqla-filters-yaml](https://github.com/MarcAureleCoste/sqla-filters-yaml)
