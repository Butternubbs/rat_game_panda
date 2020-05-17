from direct.showbase.ShowBase import ShowBase
from direct.showbase.Loader import Loader
from direct.task import Task
from direct.interval.IntervalGlobal import Sequence
from direct.gui.OnscreenImage import OnscreenImage
from panda3d.core import WindowProperties, Shader, PerspectiveLens
from panda3d.core import Point3, GeomTriangles, Geom, GeomNode
from panda3d.core import GeomVertexFormat, GeomVertexData, GeomVertexWriter
from panda3d.core import CollisionFloorMesh, CollisionNode, CollisionTraverser
from panda3d.core import CollisionHandlerQueue, CollisionSphere, Fog
from panda3d.core import CollisionHandlerPusher, Vec3, AntialiasAttrib
from panda3d.core import ConfigVariableString, LVector3f, TransparencyAttrib
from panda3d.bullet import *
from math import *
import generator
import sys

fbuffer = ConfigVariableString("framebuffer-multisample", "1")
msamples = ConfigVariableString("multisamples", "2")

class MyApp(ShowBase):

	def __init__(self):
		ShowBase.__init__(self)
		props = WindowProperties()
		props.setTitle("The Rat Cave")
		self.win.requestProperties(props)
		self.win.setClearColor((0.5,0.5,0.9,1.0))
		self.disableMouse()
		self.locked = False
		lens = PerspectiveLens()
		lens.set_fov(70)
		self.cam.node().setLens(lens)
		self.position = [30, 30, 30]
		self.velocity = [0, 0, 0]
		self.setFrameRateMeter(True)
		self.myFog = Fog("Fog Name")
		self.myFog.setColor(0.5,0.5,0.9)
		self.myFog.setExpDensity(0.005)
		render.setFog(self.myFog)
		#cool bg
		#b=OnscreenImage(parent=render2d, image="space.png")
		#base.cam.node().getDisplayRegion(0).setSort(20)

		render.setAntialias(AntialiasAttrib.MMultisample)

		debugNode = BulletDebugNode('Debug')
		debugNode.showWireframe(True)
		debugNode.showConstraints(True)
		debugNode.showBoundingBoxes(False)
		debugNode.showNormals(False)
		debugNP = render.attachNewNode(debugNode)
		debugNP.show()

		self.world = BulletWorld()
		self.world.setGravity(Vec3(0, 0, -80))
		#self.world.setDebugNode(debugNP.node())
		
		loader = Loader(self)
		myShader = Shader.load(Shader.SL_GLSL,
		               vertex="vertshader.vert",
		               fragment="fragshader.frag")
		floorMesh = BulletTriangleMesh()

		texs = [loader.loadTexture("flatstone.png"),
				loader.loadTexture("flatstone2.png"),
				loader.loadTexture("flatgrass.png"),
				loader.loadTexture("flatgrass2.png"),
				loader.loadTexture("flatrock.png"),
				loader.loadTexture("flatrock2.png"),
				loader.loadTexture("flatsnow.png"),
				loader.loadTexture("flatsand.png"),
				loader.loadTexture("flatsand2.png")]
		hmap = generator.generate(200, 200, 50, 0.01, 5)
		groundTypes = [[] for x in range(9)]
		for thing in hmap:
			groundTypes[thing[3]].append(thing[0:3])
		for i in range(len(groundTypes)):
			if len(groundTypes[i]) == 0:
				continue
			format = GeomVertexFormat.get_v3n3t2()
			format = GeomVertexFormat.registerFormat(format)
			vdata = GeomVertexData('name', format, Geom.UHStatic)
			vdata.setNumRows(3)
			vertex = GeomVertexWriter(vdata, 'vertex')
			normal = GeomVertexWriter(vdata, 'normal')
			texcoord = GeomVertexWriter(vdata, 'texcoord')
			prim = GeomTriangles(Geom.UHStatic)
			for grid in groundTypes[i]:
				v0 = (grid[0][0], grid[0][2], grid[0][1])
				vertex.addData3(v0)
				if grid[1][2] < 0:
					normal.addData3(grid[1][0], grid[1][2], grid[1][1])
				else:
					normal.addData3(-grid[1][0], -grid[1][2], -grid[1][1])
				texcoord.addData2(grid[2][0], grid[2][1])
				v1 = (grid[0][3], grid[0][5], grid[0][4])
				vertex.addData3(v1)
				if grid[1][5] < 0:
					normal.addData3(grid[1][3], grid[1][5], grid[1][4])
				else:
					normal.addData3(-grid[1][3], -grid[1][5], -grid[1][4])
				texcoord.addData2(grid[2][2], grid[2][3])
				v2 = (grid[0][6], grid[0][8], grid[0][7])
				vertex.addData3(v2)
				if grid[1][8] < 0:
					normal.addData3(grid[1][6], grid[1][8], grid[1][7])
				else:
					normal.addData3(-grid[1][6], -grid[1][8], -grid[1][7])
				texcoord.addData2(grid[2][4], grid[2][5])
				floorMesh.addTriangle(v0, v1, v2)
				prim.add_next_vertices(3)
			geom = Geom(vdata)
			geom.addPrimitive(prim)
			node = GeomNode('gnode')
			node.addGeom(geom)
			nodePath = render.attachNewNode(node)
			nodePath.setTexture(texs[i])
			nodePath.setShader(myShader)
		vdata2 = GeomVertexData('wata', format, Geom.UHStatic)
		vdata2.setNumRows(3)
		prim2 = GeomTriangles(Geom.UHStatic)
		vertex2 = GeomVertexWriter(vdata2, 'vertex')
		normal2 = GeomVertexWriter(vdata2, 'normal')
		texcoord2 = GeomVertexWriter(vdata2, 'texcoord')
		vertex2.addData3((0, 0, 0))
		vertex2.addData3((200, 0, 0))
		vertex2.addData3((0, 200, 0))
		normal2.addData3((0,0,1))
		normal2.addData3((0,0,1))
		normal2.addData3((0,0,1))
		texcoord2.addData2((0, 0))
		texcoord2.addData2((1, 0))
		texcoord2.addData2((0, 1))
		prim2.addNextVertices(3)
		vertex2.addData3((200, 200, 0))
		vertex2.addData3((0, 200, 0))
		vertex2.addData3((200, 0, 0))
		normal2.addData3((0,0,1))
		normal2.addData3((0,0,1))
		normal2.addData3((0,0,1))
		texcoord2.addData2((1, 1))
		texcoord2.addData2((0, 1))
		texcoord2.addData2((1, 0))
		prim2.addNextVertices(3)
		water = Geom(vdata2)
		water.addPrimitive(prim2)
		waterNode = GeomNode('water')
		waterNode.addGeom(water)
		waterNodePath = render.attachNewNode(waterNode)
		waterNodePath.setTransparency(True)
		waterNodePath.setTexture(loader.loadTexture("water.png"))
		floorMeshShape = BulletTriangleMeshShape(floorMesh, dynamic=False)
		fNode = BulletRigidBodyNode('floor')
		fNode.addShape(floorMeshShape)
		self.floorPhysNode = render.attachNewNode(fNode)
		self.world.attachRigidBody(fNode)
		for i in range(25):
			rat = loader.loadModel("deer.obj")
			rat.setScale((0.003, 0.003, 0.003))
			rat.setHpr((0, 90, 0))
			rat.setPos((0,0,-0.8))
			rat.setTexture(texs[5])
		
			shape = BulletSphereShape(1)
			node = BulletRigidBodyNode('ratBox')
			#node.setAngularFactor((0,0,1))
			node.setMass(10.0)
			node.addShape(shape)
			node.setActive(False)
			#node.friction = 1
			np = render.attachNewNode(node)
			np.setPos((i%5)*2+40, int(i/5)*2+40, 50)
			self.world.attachRigidBody(node)
			rat.flattenLight()
			rat.reparentTo(np)
			#posInterval1 = rat.hprInterval(0.1,
			#							 Point3(10, 90, 0),
			#							 startHpr=Point3(-10, 90, 0))
			#posInterval2 = rat.hprInterval(0.1,
			#							 Point3(-10, 90, 0),
			#							 startHpr=Point3(10,90,0))
			#pandaPace = Sequence(posInterval1, posInterval2,
			#						  name="pandaPace" + str(i))
			#pandaPace.loop()
			self.ratto = np
		self.deer = loader.loadModel("rat.obj")
		self.deer.setScale((0.15, 0.15, 0.15))
		self.deer.setHpr((0, 90, 0))
		self.deer.setPos((0, 0, -2))
		self.deerShape = BulletBoxShape((3, 1, 3))
		self.deerNode = BulletRigidBodyNode('deerBox')
		self.deerNode.setAngularFactor((0,0,1))
		self.deerNode.setMass(10.0)
		self.deerNode.setFriction(1)
		self.deerNode.addShape(self.deerShape)
		self.deerNodePath = render.attachNewNode(self.deerNode)
		self.deerNodePath.setPos((30, 30, 130))
		self.world.attachRigidBody(self.deerNode)
		self.deer.reparentTo(self.deerNodePath)


		self.keyMap = {"w" : False, "s" : False,
					   "a" : False, "d" : False,
					   "space" : False, "lshift" : False,
					   "p" : False, "o" : False}   
		self.accept("w", self.setKey, ["w", True])
		self.accept("s", self.setKey, ["s", True])	
		self.accept("a", self.setKey, ["a", True])	
		self.accept("d", self.setKey, ["d", True])
		self.accept("space", self.setKey, ["space", True])
		self.accept("lshift", self.setKey, ["lshift", True])
		self.accept("e", self.lockMouse)
		self.accept("p", self.setKey, ["p", True])
		self.accept("o", self.setKey, ["o", True])

		self.accept("w-up", self.setKey, ["w", False])
		self.accept("s-up", self.setKey, ["s", False])
		self.accept("a-up", self.setKey, ["a", False])
		self.accept("d-up", self.setKey, ["d", False])
		self.accept("space-up", self.setKey, ["space", False])
		self.accept("lshift-up", self.setKey, ["lshift", False])
		self.accept("e-up", self.setKey, ["e", False])
		self.accept('escape', sys.exit)
		self.accept("p-up", self.setKey, ["p", False])
		self.accept("o-up", self.setKey, ["o", False])

		# Add the spinCameraTask procedure to the task manager.
		self.taskMgr.add(self.cameraControl, "CameraControl")
		
		self.camera.setPos(tuple(self.position))
		#print(render.ls())
	def setKey(self, key, value):
		self.keyMap[key] = value
	def cameraControl(self, task):
		dt = globalClock.getDt()
		self.world.doPhysics(dt)
		depth = self.camera.getPos()[2]

		#Underwater appearance changes
		if depth < 0:
			self.win.setClearColor((0.4 + 0.01*depth,0.4 + 0.01*depth,0.7 + 0.01*depth,1.0))
			self.myFog.setColor((0.4 + 0.01*depth,0.4 + 0.01*depth,0.7 + 0.01*depth,1.0))
			self.myFog.setExpDensity(min(1, 0.01-depth/1000))
		else:
			self.win.setClearColor((0.5,0.5,0.9,1.0))
			self.myFog.setColor((0.5,0.5,0.9,1.0))
			self.myFog.setExpDensity(0.005)

		#Camera control
		if dt > .20:
			return task.cont
		if self.mouseWatcherNode.hasMouse() == True:
			mpos = self.mouseWatcherNode.getMouse()
			self.camera.setP(min(max(self.camera.getP() + (mpos.getY() * 30), -90), 90))
			self.camera.setH(self.camera.getH() + (mpos.getX() * -50))
			if mpos.getX() < 0.1 and mpos.getX() > -0.1:
				self.camera.setH((self.camera.getH())%360)
			else: 
				self.camera.setH((self.camera.getH() - mpos.getX())%360)
		h = radians(self.camera.getH())
		dh = radians(self.deerNodePath.getH())
		diff = (self.deerNodePath.getH() + 90 - self.camera.getH())%360 - 180
		diff = diff + 360 if diff<-180 else diff
		self.deerNode.setAngularVelocity((0, 0, 0.1*(-diff)))
		if self.locked:
			self.win.movePointer(0, int(self.win.getXSize() / 2), int(self.win.getYSize() / 2))

		#Player physics
		if self.world.contactTestPair(self.deerNode, self.floorPhysNode.node()).getNumContacts() > 0:
			self.deerNode.setGravity((0,0,0))
		else:
			self.deerNode.setGravity((0,0,-80))
		if self.keyMap["w"]:
			self.deerNode.applyCentralImpulse((-1500*dt*sin(h), 1500*dt*cos(h), 0))
		elif self.keyMap["s"]:
			self.deerNode.applyCentralImpulse((1500*dt*sin(h), -1500*dt*cos(h), 0))
		if self.keyMap["a"]:
			self.deerNode.applyCentralImpulse((-1000*dt*cos(h), -1000*dt*sin(h), 0))
		elif self.keyMap["d"]:
			self.deerNode.applyCentralImpulse((1000*dt*cos(h), 1000*dt*sin(h), 0))
		speed = sqrt((self.deerNode.getLinearVelocity()[0]*self.deerNode.getLinearVelocity()[0]) + (self.deerNode.getLinearVelocity()[1] * self.deerNode.getLinearVelocity()[1]))
		if speed > 20.0:
			self.deerNode.setLinearVelocity((self.deerNode.getLinearVelocity()[0]*0.85, self.deerNode.getLinearVelocity()[1]*0.85, self.deerNode.getLinearVelocity()[2]))
		if self.keyMap["space"]:
			if self.world.contactTestPair(self.deerNode, self.floorPhysNode.node()).getNumContacts() > 0:
				self.deerNode.setLinearVelocity((0,0,0))
				self.deerNode.applyCentralImpulse((0,0, 400))
		elif self.keyMap["lshift"]:
			None
		dp = self.deerNodePath.getPos()
		self.camera.setPos((dp[0], dp[1], dp[2] + 6))
		if not self.deerNode.active:
			self.deerNode.setActive(True)

		#Pushing and pulling models
		if self.keyMap["p"]:
			# Get to and from pos in camera coordinates
			pMouse = base.mouseWatcherNode.getMouse()
			pFrom = Point3()
			pTo = Point3()
			base.camLens.extrude(pMouse, pFrom, pTo)

			# Transform to global coordinates
			pFrom = render.getRelativePoint(base.cam, pFrom)
			pTo = render.getRelativePoint(base.cam, pTo)
			dif = (pFrom - pTo).normalized()

			result = self.world.rayTestClosest(pFrom, pTo)
			if result.hasHit():
				hit = result.getNode()
				hit.setActive(True)
				dist = (pFrom - result.getHitPos()).length()
				#print(dist)
				if dist < 5:
					hit.setLinearVelocity(0)
					hit.setGravity(0)
				else:
					hit.setLinearVelocity(dif * 80)
					hit.setGravity((0, 0, -30))
		if self.keyMap["o"]:
			# Get to and from pos in camera coordinates
			pMouse = base.mouseWatcherNode.getMouse()
			pFrom = Point3()
			pTo = Point3()
			base.camLens.extrude(pMouse, pFrom, pTo)

			# Transform to global coordinates
			pFrom = render.getRelativePoint(base.cam, pFrom)
			pTo = render.getRelativePoint(base.cam, pTo)
			dif = (pTo - pFrom).normalized()

			result = self.world.rayTestClosest(pFrom, pTo)
			if result.hasHit():
				hit = result.getNode()
				hit.setActive(True)
				hit.setLinearVelocity(dif * 120)
				hit.setGravity((0, 0, -30))
		return task.cont
	
	def lockMouse(self):
		wp = WindowProperties()
		if not self.locked:
			wp.setMouseMode(WindowProperties.MRelative)
			self.win.requestProperties(wp)
			self.locked = True
		else:
			wp.setMouseMode(WindowProperties.MAbsolute)
			self.win.requestProperties(wp)
			self.locked = False


app = MyApp()
app.run()