# Change Log

## [0.4] - 2020-09-02

- Added support for more types:
  - Box Types - TBox and STBox (https://github.com/adonmo/mobilitydb-sqlalchemy/issues/4)
  - Time Types - Period, PeriodSet and TimestampSet (https://github.com/adonmo/mobilitydb-sqlalchemy/issues/2)
  - Range Types - RangeInt and RangeFloat (https://github.com/adonmo/mobilitydb-sqlalchemy/issues/3)

## [0.3] - 2020-07-28

- The library now works on top of [PyMEOS](https://github.com/adonmo/meos)

## [0.2.1] - 2020-03-06

- Add support for TGeogPoint

## [0.2.0] - 2019-12-25

- Add optional support for movingpandas when using TGeomPoint
- Tests using GitHub Actions as the CI
- Add this changelog

## [0.1.1] - 2019-12-23

- Proper public release on PyPI and readthedocs

## [0.1.0] - 2019-12-23

- Initial release with TGeomPoint, TFloat, TInt and TBool
- Support bindings for MobilityDB operators
