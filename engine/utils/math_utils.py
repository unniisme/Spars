import math

class Vector:
    fp_precision = 10**(-13)

    #Overrides

    #Constructors
    def __init__(self, *args):
        
        if hasattr(args[0], '__iter__'):
            self.elements = tuple(args[0])
        else:
            self.elements = tuple(args)
        self.dimensions = len(self.elements)
        self.magnitude = self.Magnitude()

    def asTuple(self) -> tuple:
        """Returns the vector as a tuple"""
        return self.elements


    #Shell representation
    def __repr__(self):
        return f"Vector{self.elements}"

    #Print function
    def __str__(self):
        return str(self.elements)

    #indexing
    def __getitem__(self, index):
        return self.elements[index]

    #Writing index
    def __setitem__(self, index, item):
        self.elements[index] = item      


    # +
    def __add__(self, other) -> 'Vector':
        if self.dimensions != other.dimensions:
            raise ValueError("Dimension mismatch")
        return Vector(x+y for x,y in zip(self.elements, other.elements))
        
    # additive inverse
    def __neg__(self) -> 'Vector':
        return Vector((-x) for x in self.elements)

    # -
    def __sub__(self, other) -> 'Vector':
        return self + (-other)

    # *
    def __mul__(self, scalar) -> 'Vector':
        if type(scalar) != int and type(scalar) != float:
            raise TypeError("scalar has to be an int or a float")
        return Vector(x*scalar for x in self.elements)

    # * but from the left
    def __rmul__(self, scalar) -> 'Vector':
        if type(scalar) != int and type(scalar) != float:
            raise TypeError("scalar has to be an int or a float")
        return Vector(x*scalar for x in self.elements)

    # /
    def __truediv__(self, scalar) -> 'Vector':
        if type(scalar) != int and type(scalar) != float:
            raise TypeError("scalar has to be an int or a float")
        return self * (1/scalar)

    #compare if 2 floats are as close as to be considered equal
    def PrecisionEquality(a,b):
        return abs(a-b)<Vector.fp_precision

    def PrecisionClamp(a):
        return 0 if Vector3.PrecisionEquality(a, 0) else a

    # ==
    def __eq__(self, o:'Vector') -> bool:
        if o==None:
            return False
        if self.dimensions != o.dimensions:
            return False
        return all([Vector.PrecisionEquality(x, y) for x,y in zip(self.elements, o.elemnts)])


    #Other operators
    
    def Magnitude(self):
        """Returns the magnitude of the vector"""
        return math.sqrt(sum([pow(x,2) for x in self.elements]))

    def Dot(a:'Vector', b:'Vector'):
        """
        Returns the dot product a.b
        Usage: Dot(a,b) or a.Dot(b)
        """
        if a.dimensions != b.dimensions:
            raise ValueError("Dimension mismatch")

        return sum([x*y for x,y in zip(a.elements, b.elements)])

    
    def Normalized(self):
        """Returns the unit vector in the direction of the input vector"""
        return self/self.magnitude

    def IntClamp(self):
        """Round the vector to the nearest integer vector"""
        return Vector(*map(int, self.elements))


    #Vector operators
    def lerp(start, end, t):
        """
        Linear Interpolation.
        Returns the vector at t fraction from start to end
        """
        return start + t*(end-start)

    def slerp(start, end, t : float, omega=90):
        """
        Spherical interpolation.
        """
        omega = math.radians(omega)

        return ((math.sin((1-t)*omega)/math.sin(omega)) * start) + ((math.sin((t)*omega)/math.sin(omega))*end)

    def Components(a, b):
        """
        Split a into parallel and perpendicular components wrt b 
        returns (parellel, perpendicular)
        """
        parallel = (a.Dot(b)/(b.magnitude**2)) * b
        perpendicular = a - parallel
        return (parallel, perpendicular)


    #global constants
    def ZERO(n):
        return Vector(*(0 for i in range(n)))



class Vector2(Vector):

    #Overrides

    #Constructors
    def __init__(self, x, y=None):
        """A Tuple/list/iterable can be used as inputs as well"""
        if y == None:
            try:
                y = x[1]
            except:
                y=0
            x = x[0]
        self.x = Vector.PrecisionClamp(x)
        self.y = Vector.PrecisionClamp(y)
        self.magnitude = self.Magnitude()

    def PolarConstructor(r, t):
        """Constructs a vector with given magnitude and direction(angle in radians)"""
        return Vector2(r*math.cos(t), r*math.sin(t))

    def PolarConstructorDeg(r, t):
        """Constructs a vector with given magnitude and direction(angle in degrees)"""
        t = math.radians(t)
        return Vector2(r*math.cos(t), r*math.sin(t))
    
    def asTuple(self) -> tuple:
        """Returns the vector as a tuple"""
        return (self[0], self[1])


    #Shell representation
    def __repr__(self):
        return f"Vector2({self.x}, {self.y})"

    #Print function
    def __str__(self):
        return str((self.x, self.y))

    #indexing
    def __getitem__(self, index):
        if index == 0 or index == 'x':
            return self.x
        elif index == 1 or index == 'y':
            return self.y
        else:
            raise IndexError("Enter a valid index (0/x or 1/y)")

    #Writing index
    def __setitem__(self, index, item):
        if index == 0 or index == 'x':
            self.x = item
        elif index == 1 or index == 'y':
            self.y = item
        else:
            raise IndexError("Enter a valid index (0/x or 1/y)")        



    # +
    def __add__(self, other) -> 'Vector2':
        return Vector2(self[0] + other[0], self[1] + other[1])
    # additive inverse
    def __neg__(self) -> 'Vector2':
        return Vector2(-self[0], -self[1])

    # -
    def __sub__(self, other) -> 'Vector2':
        return self + (-Vector2(other))

    # *
    def __mul__(self, scalar) -> 'Vector2':
        if type(scalar) != int and type(scalar) != float:
            raise TypeError("scalar has to be an int or a float")
        return Vector2(self[0]*scalar, self[1]*scalar)

    # * but from the left
    def __rmul__(self, scalar) -> 'Vector2':
        if type(scalar) != int and type(scalar) != float:
            raise TypeError("scalar has to be an int or a float")
        return Vector2(self[0]*scalar, self[1]*scalar)

    # /
    def __truediv__(self, scalar) -> 'Vector2':
        if type(scalar) != int and type(scalar) != float:
            raise TypeError("scalar has to be an int or a float")
        return self * (1/scalar)

    # ==
    def __eq__(self, o:'Vector2'):
        if o==None:
            return False
        return Vector.PrecisionEquality(self[0], o[0]) and Vector.PrecisionEquality(self[1], o[1])


    #Other operators
    
    def Magnitude(self):
        """Returns the magnitude of the vector"""
        return math.sqrt(self[0]**2 + self[1]**2)

    def Dot(self, b):
        """
        Returns the dot product a.b
        Usage: Dot(a,b) or a.Dot(b)
        """
        return self[0]*b[0] + self[1]*b[1]

    
    def Normalized(self):
        """Returns the unit vector in the direction of the input vector"""
        return self/self.magnitude

    def Cross(self, b:'Vector2'):
        """
        Returns the cross product axb (in this order)
        Usage: Dot(a,b) or a.Dot(b)
        """
        return self[0]*b[1] - self[1]*b[0]

    def Direction(a:'Vector2', b:'Vector2') -> 'Vector2':
        return b-a

    def Angle(self, other:'Vector2' = None):
        """returns the angle in radians between 2 vectors"""
        if other == None:
            return math.atan2(self[1], self[0])
            

        return self.Angle() - Vector2.Angle(other)


    def AngleDeg(self, other:'Vector2' = None):
        """returns the angle in degrees between 2 vectors"""
        return math.degrees(self.Angle(other))

    def Rotate(self, angle):
        """returns a vector rotated by angle in radians"""
        return Vector2.PolarConstructor(self.magnitude, self.Angle()+angle)

    def RotateDeg(self, angle):
        """returns a vector rotated by angle in degrees"""
        angle = math.radians(angle)
        return Vector2.PolarConstructor(self.magnitude, self.Angle()+angle)

    def IntClamp(self):
        """Round the vector to the nearest integer vector"""
        return Vector2(round(self[0]), round(self[1]))


    #Vector operators
    def lerp(start, end, t):
        """
        Linear Interpolation.
        Returns the vector at t fraction from start to end
        """
        return start + t*(end-start)

    def slerp(start, end, t : float, omega=90):
        """
        Spherical interpolation.
        """
        omega = math.radians(omega)

        return ((math.sin((1-t)*omega)/math.sin(omega)) * start) + ((math.sin((t)*omega)/math.sin(omega))*end)


    #global constants
    def UP():
        return Vector2(0, 1)
    def DOWN():
        return Vector2(0, -1)
    def LEFT():
        return Vector2(-1,0)
    def RIGHT():
        return Vector2(1,0)
    def ZERO():
        return Vector2(0,0)

class Vector3(Vector):

    #Overrides

    #Constructors
    def __init__(self, x, y=None, z=None):
        """A Tuple/list/iterable can be used as inputs as well"""
        if y == None:
            try:
                z = x[2]
            except:
                z = 0
            try:
                y = x[1]
            except:
                y = 0
            x = x[0]
        self.x = Vector.PrecisionClamp(x)
        self.y = Vector.PrecisionClamp(y)
        self.z = Vector.PrecisionClamp(z)
        self.magnitude = self.Magnitude()

    def SphericalConstructor(r, theta, phi):
        """
        theta is about y axis, phi is from y axis
        """
        return Vector3(r * math.sin(theta) * math.cos(phi), r * math.cos(theta), r * math.sin(theta) * math.sin(phi))

    def SphericalConstructorDeg(r, theta, phi):
        return Vector3.SphericalConstructor(r, math.radians(theta), math.radians(phi))

    def CylinderConstructor(r, h, theta):
        """
        Cylinder axis is y
        """
        return Vector3(r*math.cos(theta), h, r*math.sin(theta))

    def CylinderConstructorDeg(r, h, theta):
        return Vector3.CylinderConstructor(r, h, math.radians(theta))
    
    def asTuple(self) -> tuple:
        """Returns the vector as a tuple"""
        return (self[0], self[1], self[2])


    #Shell representation
    def __repr__(self):
        return f"Vector3{self.asTuple()}"

    #Print function
    def __str__(self):
        return str(self.asTuple())

    #indexing
    def __getitem__(self, index):
        if index == 0 or index == 'x':
            return self.x
        elif index == 1 or index == 'y':
            return self.y
        elif index == 2 or index == 'z':
            return self.z
        else:
            raise IndexError("Enter a valid index (0/x, 1/y or 2/z)")

    #Writing index
    def __setitem__(self, index, item):
        if index == 0 or index == 'x':
            self.x = item
        elif index == 1 or index == 'y':
            self.y = item
        elif index == 2 or index == 'z':
            self.z = item
        else:
            raise IndexError("Enter a valid index (0/x, 1/y or 2/z)")



    # +
    def __add__(self, other) -> 'Vector3':
        return Vector3(self[0] + other[0], self[1] + other[1], self[2] + other[2])
    # additive inverse
    def __neg__(self) -> 'Vector3':
        return Vector3(-self[0], -self[1], -self[2])

    # -
    def __sub__(self, other) -> 'Vector3':
        return self + (-Vector3(other))

    # *
    def __mul__(self, scalar) -> 'Vector3':
        if type(scalar) != int and type(scalar) != float:
            raise TypeError("scalar has to be an int or a float")
        return Vector3(self[0]*scalar, self[1]*scalar, self[2]*scalar)

    # * but from the left
    def __rmul__(self, scalar) -> 'Vector3':
        if type(scalar) != int and type(scalar) != float:
            raise TypeError("scalar has to be an int or a float")
        return Vector3(self[0]*scalar, self[1]*scalar, self[2]*scalar)

    # /
    def __truediv__(self, scalar) -> 'Vector3':
        if type(scalar) != int and type(scalar) != float:
            raise TypeError("scalar has to be an int or a float")
        return self * (1/scalar)

    # ==
    def __eq__(self, o:'Vector3'):
        if o==None:
            return False
        return Vector.PrecisionEquality(self[0], o[0]) and Vector.PrecisionEquality(self[1], o[1]) and Vector.PrecisionEquality(self[2], o[2])


    #Other operators
    
    def Magnitude(self):
        """Returns the magnitude of the vector"""
        return math.sqrt(self[0]**2 + self[1]**2 + self[2]**2)

    def Dot(a, b):
        """
        Returns the dot product a.b
        Usage: Dot(a,b) or a.Dot(b)
        """
        return a[0]*b[0] + a[1]*b[1] + a[2]*b[2]

    
    def Normalized(self):
        """Returns the unit vector in the direction of the input vector"""
        return self/self.magnitude

    def Cross(a:'Vector3', b:'Vector3') -> 'Vector3':
        """
        Returns the cross product axb (in this order)
        Usage: Dot(a,b) or a.Dot(b)
        """
        return Vector3( a[1]*b[2] - a[2]*b[1], 
                        a[2]*b[0] - a[0]*b[2], 
                        a[0]*b[1] - a[1]*b[0])

    def Direction(a:'Vector3', b:'Vector3') -> 'Vector3':
        return b-a

    def Angle(self, other:'Vector3'):
        """returns the angle in radians between 2 vectors"""
        return math.acos(self.Dot(other)/(self.magnitude * other.magnitude))

    def AngleDeg(self, other:'Vector3'):
        """returns the angle in degrees between 2 vectors"""
        return math.degrees(self.Angle(other))

    def Rotate(self, angle, axis):
        """returns a vector rotated by angle in radians"""
        pl, ppx = self.Components(axis)
        ppy = ppx.Cross(axis)/axis.magnitude

        return pl+ppx*math.cos(angle)+ppy*math.sin(angle)
        


    def RotateDeg(self, angle, axis):
        """returns a vector rotated by angle in degrees"""
        return self.Rotate(math.radians(angle), axis)

    def IntClamp(self):
        """Round the vector to the nearest integer vector"""
        return Vector3(round(self[0]), round(self[1]), round(self[2]))


    #global constants
    def UP():
        return Vector3(0, 1, 0)
    def X():
        return Vector3(1, 0, 0)
    def Z():
        return Vector3(0, 0, 1)
    def ZERO():
        return Vector3(0, 0, 0)
