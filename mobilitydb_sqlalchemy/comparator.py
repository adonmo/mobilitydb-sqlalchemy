from sqlalchemy import types as sqltypes
from sqlalchemy.types import UserDefinedType
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION
from sqlalchemy.sql import operators

try:
    from sqlalchemy.sql.functions import _FunctionGenerator
except ImportError:  # SQLA < 0.9  # pragma: no cover
    from sqlalchemy.sql.expression import _FunctionGenerator

EVER_EQUAL_TO = operators.custom_op("?=")
ALWAYS_EQUAL_TO = operators.custom_op("%=")
EVER_DIFFERENT_FROM = operators.custom_op("?<>")
ALWAYS_DIFFERENT_FROM = operators.custom_op("@<>")
EVER_LESS_THAN = operators.custom_op("?<")
EVER_GREATER_THAN = operators.custom_op("?>")
EVER_LESS_THAN_OR_EQUAL_TO = operators.custom_op("?<=")
EVER_GREATER_THAN_OR_EQUAL_TO = operators.custom_op("?>=")
ALWAYS_LESS_THAN = operators.custom_op("%<")
ALWAYS_GREATER_THAN = operators.custom_op("%>")
ALWAYS_LESS_THAN_OR_EQUAL_TO = operators.custom_op("%<=")
ALWAYS_GREATER_THAN_OR_EQUAL_TO = operators.custom_op("%>=")

TEMPORAL_EQUAL = operators.custom_op("#=")
TEMPORAL_NOT_EQUAL = operators.custom_op("#<>")
TEMPORAL_LESS_THAN = operators.custom_op("#<")
TEMPORAL_GREATER_THAN = operators.custom_op("#>")
TEMPORAL_LESS_THAN_OR_EQUAL_TO = operators.custom_op("#<=")
TEMPORAL_GREATER_THAN_OR_EQUAL_TO = operators.custom_op("#>=")

BBOX_ALWAYS_STRICTLY_LESS_THAN = operators.custom_op("<<")
BBOX_ALWAYS_STRICTLY_GREATER_THAN = operators.custom_op(">>")
BBOX_NEVER_GREATER_THAN = operators.custom_op("&<")
BBOX_NEVER_LESS_THAN = operators.custom_op("&>")
BBOX_STRICTLY_TO_LEFT = operators.custom_op("<<")
BBOX_STRICTLY_TO_RIGHT = operators.custom_op(">>")
BBOX_STRICTLY_BELOW = operators.custom_op("<<|")
BBOX_STRICTLY_ABOVE = operators.custom_op("|>>")
BBOX_DOES_NOT_EXTEND_TO_LEFT = operators.custom_op("&>")
BBOX_DOES_NOT_EXTEND_TO_RIGHT = operators.custom_op("&<")
BBOX_DOES_NOT_EXTEND_BELOW = operators.custom_op("&<|")
BBOX_DOES_NOT_EXTEND_ABOVE = operators.custom_op("|&>")
BBOX_STRICTLY_IN_FRONT = operators.custom_op("<</")
BBOX_STRICTLY_IN_BACK = operators.custom_op("/>>")
BBOX_DOES_NOT_EXTEND_IN_FRONT = operators.custom_op("&</")
BBOX_DOES_NOT_EXTEND_IN_BACK = operators.custom_op("/&>")
BBOX_ALWAYS_BEFORE = operators.custom_op("<<#")
BBOX_ALWAYS_AFTER = operators.custom_op("<<#")
BBOX_NEVER_AFTER = operators.custom_op("&<#")
BBOX_NEVER_BEFORE = operators.custom_op("#&>")
BBOX_CONTAINS = operators.custom_op("@>")
BBOX_CONTAINED = operators.custom_op("<@")
BBOXES_OVERLAP = operators.custom_op("&&")
BBOXES_EQUAL = operators.custom_op("~=")

SMALLEST_DISTANCE_EVER_BETWEEN = operators.custom_op("|=|")
DISTANCE = operators.custom_op("<->")


class Comparator(UserDefinedType.Comparator):
    """
    A custom comparator base class. It adds the ability to call spatial and
    temporal functions on columns that use this kind of comparator. It also
    defines functions that map to operators supported by ``TBool``, ``TInt``,
    ``TFloat`` and ``TGeomPoint`` columns.
    """

    def __lshift__(self, other):
        return self.bbox_strictly_to_left(other)

    def __rshift__(self, other):
        return self.bbox_strictly_to_right(other)

    def ever_equal_to(self, other):
        """
        The "?=" operator.

        Is lhs ever equal to the rhs?

        The function does not take into account whether the bounds are inclusive or not.
        """
        return self.operate(EVER_EQUAL_TO, other, is_comparision=True)

    def always_equal_to(self, other):
        """
        The "%=" operator.

        Is lhs always equal to the rhs?

        The function does not take into account whether the bounds are inclusive or not.
        """
        return self.operate(ALWAYS_EQUAL_TO, other, is_comparision=True)

    def ever_different_from(self, other):
        """
        The "?<>" operator.
        """
        return self.operate(EVER_DIFFERENT_FROM, other, is_comparision=True)

    def always_different_from(self, other):
        """
        The "@<>" operator.
        """
        return self.operate(ALWAYS_DIFFERENT_FROM, other, is_comparision=True)

    def ever_less_than(self, other):
        """
        The "?<" operator.
        """
        return self.operate(EVER_LESS_THAN, other, is_comparision=True)

    def ever_greater_than(self, other):
        """
        The "?>" operator.
        """
        return self.operate(EVER_GREATER_THAN, other, is_comparision=True)

    def ever_less_than_or_equal_to(self, other):
        """
        The "?<=" operator.
        """
        return self.operate(EVER_LESS_THAN_OR_EQUAL_TO, other, is_comparision=True)

    def ever_greater_than_or_equal_to(self, other):
        """
        The "?>=" operator.
        """
        return self.operate(EVER_GREATER_THAN_OR_EQUAL_TO, other, is_comparision=True)

    def always_less_than(self, other):
        """
        The "%<" operator.
        """
        return self.operate(ALWAYS_LESS_THAN, other, is_comparision=True)

    def always_greater_than(self, other):
        """
        The "%>" operator.
        """
        return self.operate(ALWAYS_GREATER_THAN, other, is_comparision=True)

    def always_less_than_or_equal_to(self, other):
        """
        The "%<=" operator.
        """
        return self.operate(ALWAYS_LESS_THAN_OR_EQUAL_TO, other, is_comparision=True)

    def always_greater_than_or_equal_to(self, other):
        """
        The "%>=" operator.
        """
        return self.operate(ALWAYS_GREATER_THAN_OR_EQUAL_TO, other, is_comparision=True)

    def temporal_equal(self, other):
        """
        The "#=" operator.
        """
        from mobilitydb_sqlalchemy.types.TBool import TBool

        return self.operate(TEMPORAL_EQUAL, other, result_type=TBool)

    def temporal_not_equal(self, other):
        """
        The "#<>" operator.
        """
        from mobilitydb_sqlalchemy.types.TBool import TBool

        return self.operate(TEMPORAL_NOT_EQUAL, other, result_type=TBool)

    def temporal_less_than(self, other):
        """
        The "#<" operator.
        """
        from mobilitydb_sqlalchemy.types.TBool import TBool

        return self.operate(TEMPORAL_LESS_THAN, other, result_type=TBool)

    def temporal_greater_than(self, other):
        """
        The "#>" operator.
        """
        from mobilitydb_sqlalchemy.types.TBool import TBool

        return self.operate(TEMPORAL_GREATER_THAN, other, result_type=TBool)

    def temporal_less_than_or_equal_to(self, other):
        """
        The "#<=" operator.
        """
        from mobilitydb_sqlalchemy.types.TBool import TBool

        return self.operate(TEMPORAL_LESS_THAN_OR_EQUAL_TO, other, result_type=TBool)

    def temporal_greater_than_or_equal_to(self, other):
        """
        The "#>=" operator.
        """
        from mobilitydb_sqlalchemy.types.TBool import TBool

        return self.operate(TEMPORAL_GREATER_THAN_OR_EQUAL_TO, other, result_type=TBool)

    def bbox_always_strictly_less_than(self, other):
        """
        The "<<" operator.
        """
        return self.operate(BBOX_ALWAYS_STRICTLY_LESS_THAN, other, is_comparision=True)

    def bbox_always_strictly_greater_than(self, other):
        """
        The ">>" operator.
        """
        return self.operate(
            BBOX_ALWAYS_STRICTLY_GREATER_THAN, other, is_comparision=True
        )

    def bbox_never_greater_than(self, other):
        """
        The "&<" operator.
        """
        return self.operate(BBOX_NEVER_GREATER_THAN, other, is_comparision=True)

    def bbox_never_less_than(self, other):
        """
        The "&>" operator.
        """
        return self.operate(BBOX_NEVER_LESS_THAN, other, is_comparision=True)

    def bbox_strictly_to_left(self, other):
        """
        The "<<" operator.
        """
        return self.operate(BBOX_STRICTLY_TO_LEFT, other, is_comparision=True)

    def bbox_strictly_to_right(self, other):
        """
        The ">>" operator.
        """
        return self.operate(BBOX_STRICTLY_TO_RIGHT, other, is_comparision=True)

    def bbox_strictly_below(self, other):
        """
        The "<<|" operator.
        """
        return self.operate(BBOX_STRICTLY_BELOW, other, is_comparision=True)

    def bbox_strictly_above(self, other):
        """
        The "|>>" operator.
        """
        return self.operate(BBOX_STRICTLY_ABOVE, other, is_comparision=True)

    def bbox_does_not_extend_to_left(self, other):
        """
        The "&>" operator.
        """
        return self.operate(BBOX_DOES_NOT_EXTEND_TO_LEFT, other, is_comparision=True)

    def bbox_does_not_extend_to_right(self, other):
        """
        The "&<" operator.
        """
        return self.operate(BBOX_DOES_NOT_EXTEND_TO_RIGHT, other, is_comparision=True)

    def bbox_does_not_extend_below(self, other):
        """
        The "&<|" operator.
        """
        return self.operate(BBOX_DOES_NOT_EXTEND_BELOW, other, is_comparision=True)

    def bbox_does_not_extend_above(self, other):
        """
        The "|&>" operator.
        """
        return self.operate(BBOX_DOES_NOT_EXTEND_ABOVE, other, is_comparision=True)

    def bbox_strictly_in_front(self, other):
        """
        The "<</" operator.
        """
        return self.operate(BBOX_STRICTLY_IN_FRONT, other, is_comparision=True)

    def bbox_strictly_in_back(self, other):
        """
        The "/>>" operator.
        """
        return self.operate(BBOX_STRICTLY_IN_BACK, other, is_comparision=True)

    def bbox_does_not_extend_in_front(self, other):
        """
        The "&</" operator.
        """
        return self.operate(BBOX_DOES_NOT_EXTEND_IN_FRONT, other, is_comparision=True)

    def bbox_does_not_extend_in_back(self, other):
        """
        The "/&>" operator.
        """
        return self.operate(BBOX_DOES_NOT_EXTEND_IN_BACK, other, is_comparision=True)

    def bbox_always_before(self, other):
        """
        The "<<#" operator.
        """
        return self.operate(BBOX_ALWAYS_BEFORE, other, is_comparision=True)

    def bbox_always_after(self, other):
        """
        The "<<#" operator.
        """
        return self.operate(BBOX_ALWAYS_AFTER, other, is_comparision=True)

    def bbox_never_after(self, other):
        """
        The "&<#" operator.
        """
        return self.operate(BBOX_NEVER_AFTER, other, is_comparision=True)

    def bbox_never_before(self, other):
        """
        The "#&>" operator.
        """
        return self.operate(BBOX_NEVER_BEFORE, other, is_comparision=True)

    def bbox_contains(self, other):
        """
        The "@>" operator.
        """
        return self.operate(BBOX_CONTAINS, other, is_comparision=True)

    def bbox_contained(self, other):
        """
        The "<@" operator.
        """
        return self.operate(BBOX_CONTAINED, other, is_comparision=True)

    def bboxes_overlap(self, other):
        """
        The "&&" operator.
        """
        return self.operate(BBOXES_OVERLAP, other, is_comparision=True)

    def bboxes_equal(self, other):
        """
        The "~=" operator.
        """
        return self.operate(BBOXES_EQUAL, other, is_comparision=True)

    def smallest_distance_ever_between(self, other):
        """
        The "|=|" operator.
        """
        return self.operate(
            SMALLEST_DISTANCE_EVER_BETWEEN, other, result_type=sqltypes.Float
        )

    def distance(self, other):
        """
        The "<->" operator.
        """
        from mobilitydb_sqlalchemy.types.TFloat import TFloat

        return self.operate(DISTANCE, other, result_type=TFloat)
