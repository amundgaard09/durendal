"""
Linear Algebra Type Library for the `DuraPy` package.

This module contains the base classes for the custom data types used in the `DuraPy` library, such as `D3Vector`, `NDVector`, `Matrix`, and `SquareMatrix`.
"""

from __future__ import annotations

import math, copy, typing, random
from durapy.src.commons.exceptions import MissingParameters, InvalidInput

EPSILON = 1e-9

def _validate_float(n: float) -> float:
    try:
        toReturn = float(n)
    except (ValueError, TypeError):
        raise InvalidInput(float, type(n))
    else:
        return toReturn

@typing.overload
def _isClose(a: float, b: float) -> bool: ...
@typing.overload
def _isClose(a: list[float], b: list[float]) -> bool: ...
@typing.overload
def _isClose(a: list[list[float]], b: list[list[float]]) -> bool: ...
def _isClose(a: float | list[float] | list[list[float]], b: float | list[float] | list[list[float]]) -> bool:
    """Overloaded function for checking if two floats / lists of floats are close"""
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        return math.isclose(a, b)
    
    if isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b):
            return False
        return all(_isClose(x, y) for x, y in zip(a, b))
        
    return False

class D3Vector:
    """`DuraPy` Dataclass for 3-dimensional vectors.
     
    This class is to be used for applications where 3 and only 3 dimensions in a vector is needed. 
    Use the `NDVector` class elsewhere.
    
    Args
    ----
    `x`, `y` & `z`: float - X, Y, and Z values for the vector.
    """
    def __init__(self, x: float, y: float, z: float):
        self._x = _validate_float(x)
        self._y = _validate_float(y)
        self._z = _validate_float(z)

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
        return math.hypot(self._x, math.hypot(self._y, self._z))

    def toOppositeVec(self):
        return D3Vector(-self._x, -self._y, -self._z)
    def toUnitVec(self):
        return D3Vector(self._x / self.magnitude, self._y / self.magnitude, self._z / self.magnitude) if self.magnitude != 0 else D3Vector(0, 0, 0)
    def rotate(self, x: float, y: float, z: float):
        """Rotates the vector V by angles x, y, and z around the x, y, and z axes respectively."""
        
        R = (Rz(z) @ (Ry(y) @ Rx(x)))
        newVec = R @ self
    
        return newVec
    
    def __str__(self):
        return f"<{self._x}, {self._y}, {self._z}>"
    def __repr__(self):
        return f"Vector({self._x!r}, {self._y!r}, {self._z!r})"
    def __eq__(self, other):
        return (
            isinstance(other, D3Vector) and
            _isClose(self._x, other._x) and
            _isClose(self._y, other._y) and
            _isClose(self._z, other._z)
        )
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
        elif isinstance(other, SquareMatrix):
            values = [0.0, 0.0, 0.0]
            vec = [self._x, self._y, self._z]

            for i in range(3):
                for k in range(3):
                    values[i] += other[i][k] * vec[k]

            return D3Vector(*values)
        else:
            return NotImplemented
    def __rmatmul__(self, other):
        return self.__matmul__(other)
class NDVector:
    """`DuraPy` Dataclass for N-dimensional vectors.
    
    This class is to be used for applications where more than 3 dimensions in a vector is needed. 
    Use the `D3Vector` class for 3-dimensional vectors.
    
    Args
    ----
    `components`: list[float] - The components of the vector, in order.
    """
    def __init__(self, components: list[float]):
        self._components = [ _validate_float(comp) for comp in components ]
    
    def __getitem__(self, idx: int) -> float:
        return self._components[idx]
    def __setitem__(self, key, value: float) -> None:
        self._components[key] = _validate_float(value)
    def __iter__(self):
        return iter(self._components)
    def __str__(self) -> str:
        return str(self._components)
    def __neg__(self) -> NDVector:
        return NDVector([-(component) for component in self._components])
    def __eq__(self, value) -> bool:
        if isinstance(value, NDVector):
            return (self._components == value._components)
        elif isinstance(value, list):
            return (self._components == value)
        return NotImplemented
    
    @property
    def components(self) -> list[float]:
        return self._components
    
    @property
    def magnitude(self) -> float:
        return math.hypot(*self._components)

class Matrix:
    """`DuraPy` Dataclass for Matrices.
    
    This class is to be used for applications where non-square matrices are needed. 
    Use the `SquareMatrix` class for square matrices.
    
    Args
    ----
    `array`: list[list[float]] - The data to create the matrix from, unless empty or random values are preferred.
    
    `rows` & `cols`: int - Create an empty matrix with dimensions `Rows` x `Cols`
    
    `random`: bool - Create a matrix filled with uniform values ranging from -1 and 1 unless otherwise specified with the `randrange` parameter.

    `randtype`: tuple - Specifies if the matrix should be filled with random integers or floats.
    
    `randrange`: tuple - Specifies the range for the `random`.`uniform` function.
    
    `fill`: float - Specifies what value to fill the matrix with, if not random.
    """
    def __init__(
        self, 
        array: list[list[float]]  | None = None, 
        rows:       int           | None = None, 
        cols:       int           | None = None, 
        randomfill: bool          | None = False,
        randtype:   type          | None = float,
        randrange:  tuple         | None = (-1, 1),
        fill:       float         | None = 0,
    ):
        if rows == 0 or cols == 0:
            raise ValueError("Matrix can't have 0 rows or columns!")
        
        if array is None and rows and cols:
            if randomfill:
                if randtype is float:
                    array = [[random.uniform(*randrange) for _ in range(cols)] for _ in range(rows)]
                elif randtype is int:
                    array = [[random.randint(*randrange) for _ in range(cols)] for _ in range(rows)]
                else: 
                    array = [[0 for _ in range(cols)] for _ in range(rows)]
                    
            else:
                array = [[fill for _ in range(cols)] for _ in range(rows)]
            
        if not rows and not cols and not array:
            raise MissingParameters("Missing array and size parameters! Matrix() needs atleast 1!")

        if array is not None:
            if len(array) == 0 or any(len(row) != len(array[0]) for row in array):
                raise ValueError("Matrix must be rectangular and non-empty")

        self._data = array
        self._rows = len(array)
        self._cols = len(array[0]) if self._rows > 0 else 0
    
    @property
    def dim(self) -> tuple[int, int]:
        """
        Returns the dimensions of the matrix in the format: (`Rows`,`Cols`)
        """
        return (self._rows, self._cols)
    
    @property
    def elements(self) -> int:
        """
        Returns the total number of elements in the matrix.
        """
        return self._rows * self._cols
    
    @property
    def zeros(self):
        """
        Returns the number of elements which are zero.
        """
        _zeros = 0
        for row in self._data:
            for element in row:
                _zeros += 1 if element == 0 else None
        return _zeros
    
    @property
    def nonzeros(self):
        """
        Returns the number of elements which are not zero.
        """
        _nonzeros = 0
        for row in self._data:
            for element in row:
                _nonzeros += 1 if element != 0 else None
        return _nonzeros
    
    def __getitem__(self, idx: int) -> list:
        return self._data[idx]
    def __setitem__(self, key: int, value: list[float]) -> None:
        self._data[key] = value
    def __format__(self, format_spec: str) -> str:
        match format_spec:
            case '':
                return str(self)
            case '_':
                return str(self)
        return str(self)

    def __bool__(self) -> bool:
        return any(any(cell != 0 for cell in row) for row in self._data)
    def __iter__(self):
        return iter(self._data)
    def __repr__(self) -> str:
        return f"Matrix({self._data!r})"
    def __str__(self) -> str:
        returnStr = ""
        for row in self:
            returnStr += str(row) + "\n"
            
        return returnStr
    def __neg__(self) -> Matrix:
        return Matrix([[(self[idx1][idx2] * -1) for idx2 in range(self._cols)] for idx1 in range(self._rows)])
    def __eq__(self, other) -> bool:
        if isinstance(other, Matrix):         return _isClose(self._data, other._data) and self._rows == other._rows and self._cols == other._cols
        elif isinstance(other, SquareMatrix): return _isClose(self._data, other._data)
        else:                                 return self._data == other
    
    def __add__(self, other) -> Matrix | SquareMatrix:
        if isinstance(other, Matrix):
            if self._rows != other._rows or self._cols != other._cols:
                raise ValueError("Matrix summation only takes same-size dimensions!")
            return SquareMatrix([[self[i][j] + other[i][j] for j in range(self._cols)] for i in range(self._rows)])
        elif isinstance(other, SquareMatrix):
            if self._rows != other._dim or self._cols != other._dim:
                raise ValueError("Matrix summation only takes same-size dimensions!")
            return SquareMatrix([[self[i][j] + other[i][j] for j in range(self._cols)] for i in range(self._rows)])
        elif isinstance(other, (int, float)):
            return SquareMatrix([[self[i][j] + other for j in range(self._cols)] for i in range(self._rows)])
        return NotImplemented
    def __radd__(self, other) -> Matrix | SquareMatrix:
        return self.__add__(other)
    def __sub__(self, other) -> Matrix | SquareMatrix:
        if isinstance(other, Matrix):
            if self._rows != other._rows or self._cols != other._cols:
                raise ValueError("Matrix subtraction only takes same-size dimensions!")
            return SquareMatrix([[self[i][j] - other[i][j] for j in range(self._cols)] for i in range(self._rows)])
        elif isinstance(other, SquareMatrix):
            if self._rows != other._dim or self._cols != other._dim:
                raise ValueError("Matrix subtraction only takes same-size dimensions!")
            return SquareMatrix([[self[i][j] - other[i][j] for j in range(self._cols)] for i in range(self._rows)])
        elif isinstance(other, (int, float)):
            return SquareMatrix([[self[i][j] - other for j in range(self._cols)] for i in range(self._rows)])
        return NotImplemented
    def __rsub__(self, other) -> Matrix | SquareMatrix:
        if isinstance(other, Matrix):
            if self._rows != other._rows or self._cols != other._cols:
                raise ValueError("Matrix subtraction only takes same-size dimensions!")
            return SquareMatrix([[other[i][j] - self[i][j] for j in range(self._cols)] for i in range(self._rows)])
        elif isinstance(other, SquareMatrix):
            if self._rows != other._dim or self._cols != other._dim:
                raise ValueError("Matrix subtraction only takes same-size dimensions!")
            return SquareMatrix([[other[i][j] - self[i][j] for j in range(self._cols)] for i in range(self._rows)])
        elif isinstance(other, (int, float)):
            return SquareMatrix([[other - self[i][j] for j in range(self._cols)] for i in range(self._rows)])
        return NotImplemented
    def __mul__(self, other) -> Matrix:
        if isinstance(other, (int, float)):
            return SquareMatrix([[self[i][j] * other for j in range(self._cols)] for i in range(self._rows)])
        return NotImplemented
    def __rmul__(self, other) -> Matrix:
        if isinstance(other, (int, float)):
            return SquareMatrix([[self[i][j] * other for j in range(self._cols)] for i in range(self._rows)])
        return NotImplemented
    def __matmul__(self, other) -> Matrix | SquareMatrix:
        if isinstance(other, Matrix):
            if self._cols != other._rows:
                raise ValueError("Matrix multiplication requires the number of columns in the first matrix to be equal to the number of rows in the second matrix!")
            result = [[0.0 for _ in range(other._cols)] for _ in range(self._rows)]
            for i in range(self._rows):
                for j in range(other._cols):
                    for k in range(self._cols):
                        result[i][j] += (self[i][k] * other[k][j])
            return SquareMatrix(array=result)
        elif isinstance(other, SquareMatrix):
            if self._cols != other._dim:
                raise ValueError("Matrix multiplication requires the number of columns in the first matrix to be equal to the number of rows in the second matrix!")
            result = [[0.0 for _ in range(other._dim)] for _ in range(self._rows)]
            for i in range(self._rows):
                for j in range(other._dim):
                    for k in range(self._cols):
                        result[i][j] += (self[i][k] * other[k][j])
            return SquareMatrix(array=result)
        return NotImplemented
    def __rmatmul__(self, other) -> Matrix | SquareMatrix:
        if isinstance(other, Matrix):
            if other._cols != self._rows:
                raise ValueError("Matrix multiplication requires the number of columns in the first matrix to be equal to the number of rows in the second matrix!")
            result = [[0.0 for _ in range(self._cols)] for _ in range(other._rows)]
            for i in range(other._rows):
                for j in range(self._cols):
                    for k in range(other._cols):
                        result[i][j] += (other[i][k] * self[k][j])
            return SquareMatrix(array=result)
        elif isinstance(other, SquareMatrix):
            if other._dim != self._rows:
                raise ValueError("Matrix multiplication requires the number of columns in the first matrix to be equal to the number of rows in the second matrix!")
            result = [[0.0 for _ in range(self._cols)] for _ in range(other._dim)]
            for i in range(other._dim):
                for j in range(self._cols):
                    for k in range(other._dim):
                        result[i][j] += (other[i][k] * self[k][j])
            return SquareMatrix(array=result)
        return NotImplemented

    def __len__(self) -> int:
        return self._rows

    def __abs__(self) -> float:
        return math.sqrt(sum(cell * cell for row in self._data for cell in row))

    def __truediv__(self, other) -> Matrix:
        if isinstance(other, (int, float)):
            return SquareMatrix([[self[i][j] / other for j in range(self._cols)] for i in range(self._rows)])
        return NotImplemented

    def __rtruediv__(self, other):
        return NotImplemented

    def set_row(self, idx: int, newrow: list) -> None:
        if len(newrow) != self._cols: raise ValueError("New row length doesn't match the dimensions of the matrix!")
        self[idx] = newrow
    def row(self, idx: int) -> list:
        return self[idx]
    def set_column(self, idx: int, newcolumn: list) -> None:
        if len(newcolumn) != self._rows: raise ValueError("New column length doesn't match the dimensions of the matrix!")
        for j in range(len(self._data)):
            self[j][idx] = newcolumn[j] 
    def column(self, idx: int) -> list:
        return [self[j][idx] for j in range(len(self[0]))]
class SquareMatrix:
    """
    `DuraPy` `UniMath` Dataclass for Square Matrices.
    
    Args
    ----
    - `array`:     list[list[float]] - The data to create the matrix from, unless empty or random values are preferred.
    
    - `size`:      int - Create an empty matrix with dimensions `Size` x `Size`
    
    - `random`:    bool - Create a matrix filled with values from within the `randrange` parameter, defaulted to -1 to 1.
    
    - `validate`:  bool - Bypasses square-shape validation in the constructor.
    
    - `fill`:      float - Specifies what value to fill the matrix with, if not random.
    
    - `randtype`:  tuple - Specifies if the matrix should be filled with random integers or floats.
    
    - `randrange`: tuple - Specifies the range for the `random`.`uniform` function.
    """
    def __init__(
        self, 
        array: list[list[float]]  | None = None, 
        size:       int           | None = None, 
        randomfill: bool          | None = False,
        validate:   bool          | None = True,  # Used for AugmentedMatrix building NOTE remove after Matrix is finished
        fill:       float         | None = 0,
        randtype:   type          | None = float,
        randrange:  tuple         | None = (-1, 1),
    ):
        if size == 0:
            raise ValueError("A matrix can't have a size of 0!")
        
        if array is None and size:
            if randomfill:
                if randtype is float:
                    array = [[random.uniform(*randrange) for _ in range(size)] for _ in range(size)]
                elif randtype is int:
                    array = [[random.randint(*randrange) for _ in range(size)] for _ in range(size)]
                else: 
                    array = [[0, 0], [0, 0]]
                    
            else:
                array = [[fill for _ in range(size)] for _ in range(size)]
            
        if not size and not array:
            raise MissingParameters("Missing both array and size parameters! SquareMatrix() needs atleast 1!")

        if any(len(row) != len(array) for row in array) and validate:
            raise ValueError("Matrix must be square")
        
        self._data = array
        self._dim = len(array)

    def __getitem__(self, idx: int) -> list:
        return self._data[idx]
    def __setitem__(self, key: int, value: list[float]) -> None:
        if isinstance(value, list):
            self._data[key] = [_validate_float(item) for item in value]
        else:
            self._data[key] = _validate_float(value)
    def __format__(self, format_spec: str) -> str:
        match format_spec:
            case '':
                return str(self)
            case '_':
                return str(self)
        return str(self)
    def __bool__(self) -> bool:
        return any(any(cell != 0 for cell in row) for row in self._data)
    def __iter__(self):
        return iter(self._data)
    def __len__(self) -> int:
        return self._dim
    def __abs__(self) -> float:
        return math.sqrt(sum(cell * cell for row in self._data for cell in row))
    def __str__(self) -> str:
        returnStr = ""
        for row in self:
            returnStr += str(row) + "\n"
            
        return returnStr
    def __neg__(self) -> SquareMatrix:
        return SquareMatrix([[-(self[idx1][idx2]) for idx2 in range(self._dim)] for idx1 in range(self._dim)])
    def __eq__(self, other) -> bool:
        if isinstance(other, SquareMatrix):
            return _isClose(self._data, other._data) and self._dim == other._dim
        elif isinstance(other, Matrix):
            return _isClose(self._data, other._data) and self._dim == other._rows and self._dim == other._cols
        else:
            return self._data == other
    
    def __add__(self, other) -> SquareMatrix:
        if isinstance(other, SquareMatrix):
            if self._dim != other._dim:
                raise ValueError("Matrix summation only takes same-size dimensions!")
            return SquareMatrix([[self[i][j] + other[i][j] for j in range(self._dim)] for i in range(self._dim)])
        elif isinstance(other, (int, float)):
            return SquareMatrix([[self[i][j] + other for j in range(self._dim)] for i in range(self._dim)])
        return NotImplemented
    def __radd__(self, other) -> SquareMatrix:
        if isinstance(other, SquareMatrix):
            if self._dim != other._dim:
                raise ValueError("Matrix summation only takes same-size dimensions!")
            return SquareMatrix([[other[i][j] + self[i][j] for j in range(self._dim)] for i in range(self._dim)])
        elif isinstance(other, (int, float)):
            return SquareMatrix([[other + self[i][j] for j in range(self._dim)] for i in range(self._dim)])
        return NotImplemented
    def __sub__(self, other) -> SquareMatrix:
        if isinstance(other, SquareMatrix):
            if self._dim != other._dim:
                raise ValueError("Matrix subtraction only takes same-size dimensions!")
            return SquareMatrix([[self[i][j] - other[i][j] for j in range(self._dim)] for i in range(self._dim)])
        elif isinstance(other, (int, float)):
            return SquareMatrix([[self[i][j] - other for j in range(self._dim)] for i in range(self._dim)])
        return NotImplemented
    def __rsub__(self, other) -> SquareMatrix:
        if isinstance(other, SquareMatrix):
            if self._dim != other._dim:
                raise ValueError("Matrix subtraction only takes same-size dimensions!")
            return SquareMatrix([[other[i][j] - self[i][j] for j in range(self._dim)] for i in range(self._dim)])
        elif isinstance(other, (int, float)):
            return SquareMatrix([[other - self[i][j] for j in range(self._dim)] for i in range(self._dim)])
        return NotImplemented
    def __truediv__(self, other: float | int) -> SquareMatrix:
        if isinstance(other, (int, float)):
            return SquareMatrix([[self[i][j] / other for j in range(self._dim)] for i in range(self._dim)])
        return NotImplemented
    def __rtruediv__(self, other: float | int):
        return NotImplemented
    def __pow__(self, power: int, modulo=None) -> SquareMatrix:
        if not isinstance(power, int):
            raise TypeError("SquareMatrix exponent must be an integer")
        if modulo is not None:
            raise ValueError("Modulo exponentiation is not supported for SquareMatrix")

        if power == 0:
            return self.to_identity()

        base = self
        if power < 0:
            inverse = self.inverse
            if inverse is None:
                raise ValueError("Negative power requires invertible matrix")
            base = inverse
            power = -power

        result = base.to_identity()
        for _ in range(power):
            result = result @ base
        return result
    def __rpow__(self, other):
        return NotImplemented
    
    def __matmul__(self, other: SquareMatrix | D3Vector | NDVector | float | int) -> SquareMatrix | D3Vector | NDVector:
        if isinstance(other, SquareMatrix):

            result = [[0.0 for _ in range(self._dim)] for _ in range(self._dim)]

            for i in range(self._dim):
                for j in range(self._dim):
                    for k in range(self._dim):
                        result[i][j] += (self[i][k] * other[k][j])

            return SquareMatrix(array=result)
        elif isinstance(other, D3Vector):
            if self._dim != 3:
                raise ValueError("Can only multiply a D3Vector by a 3x3 SquareMatrix")
            values = [0.0, 0.0, 0.0]
            vec = [other.x, other.y, other.z]

            for i in range(3):
                for k in range(3):
                    values[i] += self[i][k] * vec[k]

            return D3Vector(*values)
        elif isinstance(other, NDVector):
            if self._dim != len(other.components):
                raise ValueError("SquareMatrix and NDVector dimensions must match for matmul")
            result = [sum(self[i][k] * other[k] for k in range(self._dim)) for i in range(self._dim)]
            return NDVector(result)
        return NotImplemented
    def __rmatmul__(self, other: SquareMatrix | D3Vector | NDVector | float | int) -> SquareMatrix | D3Vector | NDVector:
        return self.__matmul__(other)

    def set_row(self, idx: int, newrow: list[float]) -> None:
        self[idx] = newrow
    def row(self, idx: int) -> list[float]:
        return self[idx]
    def set_column(self, idx: int, newcolumn: list[float]) -> None:
        for j in range(len(self._data)):
            self[j][idx] = newcolumn[j]
    def column(self, idx: int) -> list[float]:
        return [self[j][idx] for j in range(len(self[0]))]
    
    @staticmethod
    def __sign(expr: float, idx: int) -> float:
        return expr * (-1)**abs(idx)
    @staticmethod
    def __2x2_det(_array: list[list[float]]) -> float:
        if len(_array) == 2 and all(len(row) == 2 for row in _array):
            A, B, C, D = _array[0][0], _array[0][1], _array[1][0], _array[1][1]
            return (A * D) - (B * C)
        raise ValueError("Can't calculate a base case 2x2 determinant of a non-2x2 matrix!")
    @staticmethod
    def __minor_extract(_array: list[list[float]], rowIdx: int, colIdx: int) -> SquareMatrix:
        without_row = [_array[idx] for idx in range(len(_array)) if idx != rowIdx]
        without_col = [[without_row[idx1][idx2] for idx2 in range(len(without_row[idx1])) if idx2 != colIdx] for idx1 in range(len(without_row))]
        return SquareMatrix(without_col)
    @staticmethod
    def _det(M: SquareMatrix) -> float:
        if M.dim == 2: return M.__2x2_det(M._data)
        if M.dim == 1: return M._data[0][0]
        
        detsum = 0.0
        
        for idx1, _ in enumerate(M[0]):
            minor = M.__minor_extract(M._data, 0, idx1)
            detsum += M.__sign((M[0][idx1] * M._det(minor)), idx1)
            
        return detsum
    @property
    def det(self) -> float:
        """
        Returns the determinant of the matrix through Laplace Expansion.
        
        The determinant is used to determine if the Matrix is invertible or singular (collapses space).
        """
        return self._det(self)
    
    @staticmethod
    def _T(M: SquareMatrix) -> SquareMatrix:
        transpose = SquareMatrix(size=M._dim)
        for i in range(M._dim):
                for j in range(M._dim):
                    transpose[i][j] = M[j][i]
                    
        return transpose
    @property
    def T(self) -> SquareMatrix:
        """
        Returns the transposed matrix of itself. 
        
        A transposed matrix is the original matrix but with its rows and columns swapped, 
        so one element in the original matrix - `A[I][J]` becomes `A[J][I]` in the transpose.
        It is as if the matrix was rotated around its diagonal from the top-left to bottom right.
        """
        return self._T(self)   
    
    @staticmethod
    def __build_augmented(A: SquareMatrix) -> SquareMatrix:
        n = A.dim
        I = A.to_identity()

        aug = SquareMatrix([[0 for _ in range(2 * n)] for _ in range(n)], validate=False)

        for i in range(n):
            for j in range(n):
                aug[i][j] = A[i][j]
                aug[i][j + n] = I[i][j]

        return aug
    @staticmethod
    def _inverse(A: SquareMatrix) -> SquareMatrix | None:
        if A.det == 0:
            return None

        n = A.dim
        aug = SquareMatrix.__build_augmented(A)


        for i in range(n):
            pivot = aug[i][i]

            if pivot == 0:
                for j in range(i + 1, n):
                    if aug[j][i] != 0:
                        aug[i], aug[j] = aug[j], aug[i]
                        pivot = aug[i][i]
                        break

            if pivot == 0:
                return None

            aug[i] = [x / pivot for x in aug[i]]

            for j in range(n):
                if j != i:
                    factor = aug[j][i]
                    aug[j] = [aug[j][k] - factor * aug[i][k] for k in range(2 * n)]

        inverse = [row[n:] for row in aug]
        return SquareMatrix(inverse)    
    @property
    def inverse(self) -> SquareMatrix:
        """
        Returns the inverse of the matrix through Gauss-Jordan elimination.
        
        The inverse of a matrix `A`, `A^-1`, satisfies the following equation:
        
        `A` * `A^-1` = `A^-1` * `A` = `I`, 
        
        where `I` is the identity matrix of the same dimension.
        """
        return self._inverse(self)
    
    @staticmethod
    def _rank(A: SquareMatrix) -> int:
        A = copy.deepcopy(A._data)
        N = A._dim
        
        rank, row_idx = N, 0
        
        for col in range(N):
            pivot_row_idx = row_idx
            while pivot_row_idx < N and abs(A[pivot_row_idx][col]) < EPSILON:
                pivot_row_idx += 1
                
            if pivot_row_idx == N:
                rank -= 1
                continue
                
            if pivot_row_idx != row_idx:
                A[row_idx], A[pivot_row_idx] = A[pivot_row_idx], A[row_idx]
                
            for I in range(row_idx + 1, N):
                factor = (A[I][col] / A[row_idx][col])
                for J in range(col, N):
                    A[I][J] -= factor * A[row_idx][J]
                    
            row_idx += 1
            
            if row_idx == N:
                break
                
        return rank
    @property
    def rank(self) -> int:
        """
        Calculates matrix rank via Gaussian Elimination.
        Accounts for floating point errors using `EPSILON`.
        """
        return self._rank(self)
    
    @staticmethod
    def __QR_decomposition(A: SquareMatrix) -> tuple[SquareMatrix, SquareMatrix]:
        """Performs QR Decomposition via Modified Gram-Schmidt process."""
        N = A._dim  
        Q = SquareMatrix(size=N)
        R = SquareMatrix(size=N)
        
        for J in range(N):
            v = A.column(J)
            
            for I in range(J):
                QI = Q.column(I)
                R[I][J] = sum(x * y for x, y in zip(QI, A.column(J)))
                v = [(v[idx] - R[I][J] * QI[idx]) for idx in range(N)]
                
            norm = math.sqrt(sum(x**2 for x in v))
            R[J][J] = norm
            
            if norm > 1e-12:
                Q.set_column(J, [x / norm for x in v])
            else:
                Q.set_column(J, [0.0] * N)
                
        return Q, R
    @staticmethod
    def _eigen(A: SquareMatrix) -> tuple[list[float], SquareMatrix]:
        n = A._dim
        Ak = SquareMatrix([[A[r][c] for c in range(n)] for r in range(n)])
        I = SquareMatrix(size=n).to_identity()
        
        max_iterations = 150
        
        for _ in range(max_iterations):
            Q, R = SquareMatrix.__QR_decomposition(Ak)
            
            Ak = R @ Q
            I = I @ Q
            
            off_diagonal_sum = 0.0
            for r in range(n):
                for c in range(n):
                    if r != c:
                        off_diagonal_sum += abs(Ak[r][c])
                        
            if off_diagonal_sum < EPSILON:
                break
                
        eigenvalues = [Ak[i][i] for i in range(n)]
        return eigenvalues, I
    @property
    def eigen(self) -> tuple[list[float], SquareMatrix]:
        """
        Computes eigenvalues and eigenvectors using the iterative QR algorithm.
        
        Returns
        -------
        - list[float]: The eigenvalues
        - SquareMatrix: A matrix where columns represent the corresponding eigenvectors
        """
        return self._eigen(self) 
    
    @property
    def dim(self) -> int:
        """
        Returns the dimension of the matrix. 
        
        Since it's square, only one integer is needed, compared to a rectangular one.
        """
        return self._dim
    @property
    def trace(self) -> float:
        """
        Returns the trace of the matrix. 
        
        The trace is defined as the sum of all the elements on the diagonal, e. g. `A_00`, `A_11`, `A_22`, etc.
        """
        return sum(self[idx][idx] for idx in range(len(self._data)))
    @property
    def diagonal(self) -> list:
        """
        Returns the diagonal of the matrix as a list.
        """
        return [self[idx][idx] for idx in range(self._dim)]
    
    def to_identity(self) -> SquareMatrix:
        """
        Matrix constructor that returns the identity matrix of the given size.
        """
        matrix = SquareMatrix(size=self._dim)
        for idx in range(self._dim):    
            matrix[idx][idx] = 1
    
        return matrix
    
    def is_singular(self) -> bool:
        """
        Returns if the matrix is singular. 
        
        A singular matrix is a matrix with a determinant of 0.
        """
        return (self.det == 0)
    def is_identity(self) -> bool:
        """
        Returns if the matrix is equal to the identity matrix of the same dimension.
        """
        return self == SquareMatrix(size=self.dim).to_identity()
    def is_diagonal(self) -> bool:
        """
        Returns if the matrix is diagonal.
        
        A diagnoal matrix is a matrix where all the elements outside of the leading diagonal is 0. 
        The identity matrix is a common example.
        """
        for idx1 in range(self._dim):
            for idx2 in range(self._dim):
                if idx1 != idx2 and self[idx1][idx2] != 0:
                    return False
                else:
                    continue
        return True
    def is_symmetric(self) -> bool:
        """
        Returns if the matrix is symmetric

        A symmetric matrix is a matrix that is equal to its transpose.
        """
        return (self == self.T)
    def is_nilpotent(self) -> bool:
        """
        Returns True if the matrix raised to some power becomes a zero matrix.
        """
        return all(value == 0 for value in self.eigen[0]) and self.det == 0
    def is_idempotent(self) -> bool:
        """
        Returns True if the matrix multiplied by itself equals itself: `A^2` = `A`.
        """
        return (self == self @ self)
    def is_orthogonal(self) -> bool:
        """
        Returns if the matrix is orthogonal.
        
        An orthogonal matrix is a matrix whose transpose is equal to its inverse.
        """
        return (self.T == self.inverse)
    def is_invertible(self) -> bool:
        """
        Returns if the matrix is invertible.
        
        An invertible matrix has a determinant that is not 0.
        """
        return (self.det != 0)
    def is_skew_symmetric(self) -> bool:
        """
        Returns if the matrix is skew-symmetric.
        
        A skew-symmetric matrix is a matrix whose transpose is equal to its negative.
        """
        return (self.T == -(self))
    def is_upper_triangular(self) -> bool:
        """
        Returns if the matrix is upper triangular.
        
        An upper triangular matrix is a matrix whose elements below the leading diagonal are all 0.
        """
        for idx1 in range(1, self._dim):
            for idx2 in range(idx1):
                if self[idx1][idx2] != 0:
                    return False
        return True
    def is_lower_triangular(self) -> bool:
        """
        Returns if the matrix is lower triangular.
        
        An lower triangular matrix is a matrix whose elements above the leading diagonal are all 0.
        """
        for idx1 in range(self._dim):
            for idx2 in range(idx1 + 1, self._dim):
                if self[idx1][idx2] != 0:
                    return False
        return True
    def is_positive_definite(self) -> bool:
        """
        Returns True if all eigenvalues are strictly positive.
        """
        return all(value > 0 for value in self.eigen[0])
      
def Rx(θ: float) -> SquareMatrix:
    θ = math.radians(θ)
    return SquareMatrix([
        [1, 0,            0          ], 
        [0, math.cos(θ), -math.sin(θ)], 
        [0, math.sin(θ),  math.cos(θ)]
    ])
def Ry(θ: float) -> SquareMatrix:
    θ = math.radians(θ)
    return SquareMatrix([
        [math.cos(θ),  0,  math.sin(θ)], 
        [0,            1,  0          ], 
        [-math.sin(θ), 0,  math.cos(θ)]
    ])
def Rz(θ: float) -> SquareMatrix:
    θ = math.radians(θ)
    return SquareMatrix([
        [math.cos(θ), -math.sin(θ), 0], 
        [math.sin(θ),  math.cos(θ), 0], 
        [0,            0,           1]
    ])