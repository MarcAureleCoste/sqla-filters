# Sqla-filters

![license](https://img.shields.io/pypi/l/sqla-filters.svg)
![wheel](https://img.shields.io/pypi/wheel/sqla-filters.svg)
![pyversions](https://img.shields.io/pypi/pyversions/sqla-filters.svg)

## Introduction 

Filter sqlalchemy query with json data.

This is an early stage version of the project a lot of change is coming.

## Installation

```bash
pip install sqla-filter
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

Fork the repository and run the following command to install the dependencies and the dev dependencies.

`pip install -e '.[dev]'`


### URLS
[github discution](https://github.com/pypa/pip/issues/3)
