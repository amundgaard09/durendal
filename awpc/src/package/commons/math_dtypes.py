
from commons.exceptions import InvalidInput

def _Pythagoras(A: float, B: float) -> float:
    return (A*A + B*B) ** 0.5
def _validateFloat(n: float) -> float:
    try:
        toReturn = float(n)
    except (ValueError, TypeError):
        raise InvalidInput(float, type(n))
    else:
        return toReturn

class D3Vector:
    """`AWPC` Dataclass for 3-dimensional vectors."""
    def __init__(self, x: float, y: float, z: float):
        self._x = _validateFloat(x)
        self._y = _validateFloat(y)
        self._z = _validateFloat(z)

    @property
    def x(self):
        return self._x
    @property
    def y(self):
        return self._y
    @property
    def z(self):
        return self._z
    
    @property
    def magnitude(self):
        return _Pythagoras(self._x, _Pythagoras(self._y, self._z))
    
    def toOppositeVec(self):
        return D3Vector(-self._x, -self._y, -self._z)
    
    def toUnitVec(self):
        return D3Vector(self._x / self.magnitude, self._y / self.magnitude, self._z / self.magnitude) if self.magnitude != 0 else D3Vector(0, 0, 0)
     
    def __str__(self):
        return f"<{self._x}, {self._y}, {self._z}>"
    def __repr__(self) -> str:
        return f"Vector({self._x!r}, {self._y!r}, {self._z!r})"
    def __eq__(self, other):
        return isinstance(other, D3Vector) and self._x == other._x and self._y == other._y and self._z == other._z
    def __hash__(self):
        return hash((self._x, self._y, self._z))
    
    def __bool__(self):
        return self.magnitude != 0
    
    def __add__(self, other):
        if isinstance(other, D3Vector):
            return D3Vector(self._x + other._x, self._y + other._y, self._z + other._z)
        elif isinstance(other, (float, int)):
            return D3Vector(self._x + other, self._y + other, self._z + other)
        else: 
            return NotImplemented
    def __radd__(self, other):
        return self.__add__(other)
    def __sub__(self, other):
        if isinstance(other, D3Vector):
            return D3Vector(self._x - other._x, self._y - other._y, self._z - other._z)
        elif isinstance(other, (float, int)):
            return D3Vector(self._x - other, self._y - other, self._z - other)
        else: 
            return NotImplemented
    def __rsub__(self, other):
        if isinstance(other, D3Vector):
            return D3Vector(other._x - self._x, other._y - self._y, other._z - self._z)
        return NotImplemented
    
    # Scalar Multiplication
    def __mul__(self, other):
        if isinstance(other, (float, int)):
            return D3Vector(self._x * other, self._y * other, self._z * other)
        return NotImplemented
    def __rmul__(self, other):
        if isinstance(other, (float, int)):
            return D3Vector(self._x * other, self._y * other, self._z * other)
        return NotImplemented
        
    def __matmul__(self, other):
        if isinstance(other, D3Vector):
            return (
                self._x * other._x +
                self._y * other._y +
                self._z * other._z
            )
        return NotImplemented
    def __rmatmul__(self, other):
        return self.__matmul__(other)
    
class SquareMatrix:
    """`AWPC` Dataclass for Square Matrices"""
    def __init__(self, array: list[list[float]]):
        if any(len(row) != len(array) for row in array):
            raise ValueError("Matrix must be square")

        self._data = array
        self._dim = len(array)

    def __getitem__(self, idx):
        return self._data[idx]

    def __matmul__(self, other):
        if isinstance(other, SquareMatrix):

            result = [[0 for _ in range(self._dim)] for _ in range(self._dim)]

            for i in range(self._dim):
                for j in range(self._dim):
                    for k in range(self._dim):
                        result[i][j] += (self[i][k] * other[k][j])

            return SquareMatrix(result)

        elif isinstance(other, D3Vector):
            values = [0, 0, 0]
            vec = [other.x, other.y, other.z]

            for i in range(3):
                for k in range(3):
                    values[i] += self[i][k] * vec[k]

            return D3Vector(*values)
        return NotImplemented
    
class NDimTensor:
    def __init__(self, array: list[list[list]]):
        pass
class Vectorfield:
    def __init__(self):
        pass