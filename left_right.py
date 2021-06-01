from godot import exposed, export, Node2D, Vector2

@exposed
class left_right(Node2D):
	
	# translate node that many pixel each loop, variable exposed to editor.
	step = export(int, default=10)
	# initial position of the node
	init_pos = Vector2(0,0)
	# flag to switch from left to right
	direction = 1
	
	def _ready(self):
		"""
		Called every time the node is added to the scene.
		Initialization here.
		"""
		# save intial position
		self.init_pos = self.position

	def _process(self, delta):
		"""
		Called for each rendering. Main code here.
		"""
		# when the node goes to much on the left or on the right, revert direction
		if self.position.x > self.init_pos.x + 100:
			self.direction = -1
		elif self.position.x < self.init_pos.x - 100:
			self.direction = 1
		# apply translation change
		self.position += Vector2(self.step * self.direction, 0)
