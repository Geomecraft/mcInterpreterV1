from model.Syntax import isCoordinate


def isCoordinateTest():
    assert(isCoordinate("1 1 1"))
    assert(isCoordinate("0 -1 2"))
    assert(isCoordinate("-1 -123 145"))
    assert(isCoordinate("~ ~ ~"))
    assert(isCoordinate("~ ~5 ~"))
    assert (isCoordinate("~-1 ~1.5 ~"))
    assert(isCoordinate("~1 1 ~-1"))
    assert(isCoordinate("^ ^ ^"))
    assert(isCoordinate("^ ^-1 ^1"))
    assert(not isCoordinate("1  1"))
    assert(not isCoordinate("1"))
    assert(not isCoordinate("-5 ~"))
    assert(not isCoordinate("~~~"))
isCoordinateTest()
