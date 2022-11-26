from .utils.math_utils import *
from .utils.time_utils import *
from .GameErrors import ObjectError

class Behaviour:
	"""
	Class abstraction representing arbitrary scripts that can be attached to GameObjects
	Has to be worked on, to implement a script system.
	"""
	def __init__(self, name : str):
		self.name = name

	def Update(self):
		pass

	def Ready(self):
		pass

class Transform:
	"""
	Abstract class that saves any data pertaining to position, rotation etc.
	"""
	def __init__(self, position : Vector, rotation : Vector, label = None):
		self.position = position
		self.rotation = rotation
		self.label = label

	def __eq__(self, other):
		if other == None:
			return False
		return self.position == other.position and self.rotation == other.rotation and self.label == other.label

class Transform2D(Transform):
	"""
	Transform in 2D space
	"""
	def __init__(self, position : tuple, rotation : float, label = None):
		self.position = Vector2(position)
		self.rotation = rotation
		self.label = label
		# TODO: Implement scale as well

	def Null(label = None):
		return Transform(Vector2(0,0), 0, label)

class GameObject:
	"""
	Abstract class to represent any object on a grid
	All information pertaining to grid and position, rotation etc is stored in the transform class declared below
	Used to implement any function and property over it

	This version of the class is initialized using a pre define transform
	"""
	gameObjects = {}

	uid = 0
	def AssignUID():
		GameObject.uid += 1
		return GameObject.uid-1

	def __init__(self, transform : Transform):
		self.transform = transform
		if transform == None:
			self.label = None
			return

		self.type = self.GetType()
		
		self.label = transform.label
		self.scripts = {}
		self.children = []
		self.parent = None

		if GameObject.uid == 0:
			if self.type != GameObjectTypes.Scene2D:
				raise ObjectError(ObjectError.no_scene)
		else:
			GameObject.gameObjects[0].AttachChild(self)

		self.uid = GameObject.AssignUID()
		GameObject.gameObjects[self.uid] = self	# TODO: update in __del__


	def __repr__(self):
		return str(self.label)

	def __str__(self):
		return str(self.label)

	def __eq__(self, other):
		if other == None:
			return False
		return self.uid == other.uid

	def __del__(self):
		"""
		Delete object and all children. Also delete transform and entry in dictionary of gameobjects
		"""
		del GameObject.gameObjects[self.uid]
		for child in self.children:
			del child
		del self.transform


	# Setters

	def AttachChild(self, child : "GameObject"):
		self.children.append(child)

		if child.parent != None:
			child.parent.RemoveChild(child)

		child.parent = self

	def AttachScript(self, script : Behaviour):
		self.scripts[script.name] = script

	def RemoveChild(self, child : "GameObject"):
		self.children.remove(child)
		child.parent = None


	def Update(self, dt):
		"""
		Anything to be done in every frame
		"""
		pass

	def doUpdate(self, dt):
		self.Update(dt)
		for child in self.GetChildren():
			child.doUpdate(dt)


	# Getters

	def GetChildren(self):
		return self.children

	def GetChild(self, index : int):
		return self.children[index]

	def GetScript(self, name : str):
		return self.scripts[name]

	def GetParent(self):
		return self.parent


	# Debug
	def GetType(self):
		s = str(type(self))
		return s.split(".")[-1][:-2]

	
	def ToTreeString(self,  depth : int = 0, delim : str = "\t", showType : bool = True) -> str:
		s = delim * depth
		s += str(self)
		if showType:
			s += " : " 
			s += '<' + self.type + '>'
		s += "\n"
		for child in self.GetChildren():
			s += child.ToTreeString(depth+1, delim, showType)

		return s



class GameObject2D(GameObject):

	def __init__(self, transform : Transform2D):
		super().__init__(transform)

	def ToWorldSpace(self, v) -> Vector2:
		"""
		Convert the vector from local(transform) space to world space
		"""
		v = Vector2(v)
		return Vector2.Rotate(v, self.transform.rotation) + self.transform.position  # Rotation is not busted. TODO: Fix it
		
	def ToTransformSpace(self, v) -> Vector2:
		"""
		Convert the vector from transform space to world space
		"""
		v = Vector2(v)
		return Vector2.Rotate(v, -self.transform.rotation) - self.transform.position  # Rotation is not busted. TODO: Fix it
	
	# Setters
	def SetPosition(self, pos : Vector2):
		self.UpdatePosition(pos - self.transform.position)

	def UpdatePosition(self, offset : Vector2):
		self.transform.position += offset
		for child in self.children:
			child.UpdatePosition(offset)


	def SetRotation(self, rot : float):
		self.UpdateRotation(rot - self.transform.rotation)

	def UpdateRotation(self, offset : float):
		self.transform.rotation += offset
		for child in self.children:
			child.UpdateRotation(offset)


class GameObjectTypes:
	"""
	Just a list of types of gameobjects
	They're all strings.
	"""
	#.Objects
	GameObject = 'GameObject'
	GameObject2D = 'GameObject2D'	#(GameObject)

	# .Objects_2D.Shapes
	Shape2D = 'Shape2D'				#(GameObject2D)
	Rectangle = 'Rectangle'			#(Shape2D)
	Polygon = 'Polygon'				#(Shape2D)
	Circle = 'Circle'				#(Shape2D)

	# .Renderer.Renderer
	Camera2D = 'Camera2D'			#(GameObject2D)
	Renderer2D = 'Renderer2D'		#(GameObject2D)
	GridRenderer = 'GridRenderer'	#(Renderer2D)
	# .Renderer.ShapeRenderer
	ShapeRenderer2D = 'ShapeRenderer2D'	#(Renderer2D)
	# .Renderer.TileMapRenderer
	GenerativeTileMapRenderer = 'GenerativeTileMapRenderer'	#(GridRenderer)

	#.Physics_2D

	#.Scene
	Scene2D = 'Scene2D'				#(GameObject2D)