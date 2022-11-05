from .utils.math_utils import *
from .utils.time_utils import *

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
	def __init__(self, position : Vector2, rotation : float, label = None):
		self.position = position
		self.rotation = rotation
		self.label = label

class GameObject:
	"""
	Abstract class to represent any object on a grid
	All information pertaining to grid and position, rotation etc is stored in the transform class declared below
	Used to implement any function and property over it

	This version of the class is initialized using a pre define transform
	"""

	uid = 0
	def AssignUID():
		GameObject.uid += 1
		return GameObject.uid-1

	def __init__(self, transform : Transform):
		self.transform = transform
		if transform == None:
			self.label = None
			return

		self.uid = GameObject.AssignUID()
		
		self.label = transform.label
		self.scripts = {}
		self.children = []
		self.parent = None

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
		Delete object and all children. Also delete transform
		"""
		for child in self.children:
			del child
		del self.transform


	# Setters

	def AttachChild(self, child : "GameObject"):
		self.children.append(child)
		child.parent = self

	def AttachScript(self, script : Behaviour):
		self.scripts[script.name] = script


	# Getters

	def GetChild(self, index : int):
		return self.children[index]

	def GetScript(self, name : str):
		return self.scripts[name]

	def GetParent(self):
		return self.parent