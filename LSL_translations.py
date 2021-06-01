from godot import exposed, export, Node2D, Vector2
from pylsl import StreamInlet, resolve_bypred

@exposed
class LSL_translations(Node2D):
	
	# magnitude of the applied translation
	factor = export(int, default=100)
	# initial position of the node
	init_pos = Vector2(0,0)
	# flag to switch from left to right
	direction = 1
	# LSL input stream
	inlet = None
	
	def _ready(self):
		"""
		Called every time the node is added to the scene.
		Initialization here.
		"""
		# save intial position
		self.init_pos = self.position
		
	def check_stream(self):
		"""
		Try to find the LSL stream on the network. Change predicate depending on target.
		WARNING: due to timeout option will block execution for the whole Godot engine upon each request.
		TODO: use threads to prevent blocking calls.
		"""
		if self.inlet is None:
			print("looking for stream init")
			streams = resolve_bypred("type='EEG'", timeout=0.1)
			if len(streams) > 0:
				# create a new inlet to read from the stream
				self.inlet = StreamInlet(streams[0])
				print("got stream")
				
	def _process(self, delta):
		"""
		Called for each rendering. Main code here.
		"""
		self.check_stream()
		if self.inlet is not None:
			# fetch data from inlet
			data, _ = self.inlet.pull_sample(timeout=0)
			# To maximize responsiveness, pull until last value in the buffer
			# Note: input with very high bandwidth might block forever execution here.
			while data is not None and len(data) >= 2:
				# expect two channels, translation from the initial position for X and Y.
				self.position = self.init_pos + Vector2(data[0]*self.factor, data[1]*self.factor)
				#print("got value: %s" % str(data))
				data, _ = self.inlet.pull_sample(timeout=0)
