from direct.showbase.ShowBase import ShowBase
from direct.showbase.Loader import Loader
from direct.task import Task
from direct.interval.IntervalGlobal import Sequence
from direct.gui.OnscreenImage import OnscreenImage
from panda3d.core import WindowProperties, PerspectiveLens, Point3
from panda3d.core import ConfigVariableString, AntialiasAttrib
from panda3d.bullet import *
from math import *
import random
import generator
import sys

fbuffer = ConfigVariableString("framebuffer-multisample", "1")
msamples = ConfigVariableString("multisamples", "2")

class MyApp(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)
        props = WindowProperties()
        props.setTitle("Big Bang")
        self.win.requestProperties(props)
        self.win.setClearColor((0, 0, 0, 1))
        self.disableMouse()
        self.locked = False
        lens = PerspectiveLens()
        lens.set_fov(70)
        lens.setNear(0.01)
        self.cam.node().setLens(lens)    
        render.setAntialias(AntialiasAttrib.MMultisample)
        b=OnscreenImage(parent=render2d, image="space.png")
        base.cam.node().getDisplayRegion(0).setSort(20)

        loader = Loader(self)
        bang = loader.loadModel("sphere.obj")
        bang.setScale((0.15, 0.15, 0.15))
        pos = (0, 4, 0)
        bang.setPos(pos)
        bang.reparentTo(render)
        sizeInterval1 = bang.scaleInterval(3,
        							 Point3(5, 5, 5),
        							 startScale=Point3(0.001, 0.001, 0.001))
        sizeInterval2 = bang.scaleInterval(0.1,
        							 Point3(0.001, 0.001, 0.001),
        							 startScale=Point3(5,5,5))
        sizeInterval3 = bang.scaleInterval(1,
        							 Point3(0.001, 0.001, 0.001),
        							 startScale=Point3(0.001, 0.001, 0.001))
        sizeInterval4 = bang.scaleInterval(0.1,
        							 Point3(0.1, 0.1, 1),
        							 startScale=Point3(0.1, 0.1, 0.1))
        sizeInterval5 = bang.scaleInterval(0.1,
        							 Point3(1, 0.1, 0.1),
        							 startScale=Point3(0.1, 0.1, 0.1))
        #posInterval1 = bang.posInterval(3,
        #							 Point3(0, 8, 0),
        #							 startPos=Point3(pos))
        #posInterval2 = bang.posInterval(0.1,
        #							 Point3(pos),
        #							 startPos=Point3(0, 8, 0))
        #posInterval3 = bang.posInterval(1,
        #							 Point3(pos),
        #							 startPos=Point3(pos))
        #posInterval4 = bang.posInterval(0.1,
        #							 Point3(pos),
        #							 startPos=Point3(pos))
        grow = Sequence(sizeInterval1, sizeInterval2, sizeInterval3, sizeInterval4, sizeInterval5,
        						  name="grow")
        grow.loop()
        #move = Sequence(posInterval1, posInterval2, posInterval3, posInterval4, posInterval4,
        #						  name="move")
        #move.loop()

        self.accept("e", self.lockMouse)
        # Add the spinCameraTask procedure to the task manager.
        self.taskMgr.add(self.cameraControl, "CameraControl")

        #print(render.ls())
    def cameraControl(self, task):
        dt = globalClock.getDt()
        loopTime = task.time % 4.3
        if loopTime > 2.1 and loopTime < 3.01:
            self.win.setClearColor((1, 1, 1, 1))
        else:
            self.win.setClearColor((0, 0, 0, 1))
        #Camera control
        if dt > .20:
            return task.cont
        if self.mouseWatcherNode.hasMouse() == True:
            if self.locked:
                mpos = self.mouseWatcherNode.getMouse()
                self.camera.setP(self.camera.getP() + (mpos.getY() * 30))
                self.camera.setH(self.camera.getH() + (mpos.getX() * -50))
                if mpos.getX() < 0.1 and mpos.getX() > -0.1:
                    self.camera.setH((self.camera.getH())%360)
                else: 
                    print(mpos.getX())
                    self.camera.setH((self.camera.getH() - mpos.getX())%360)

                self.win.movePointer(0, int(self.win.getXSize() / 2), int(self.win.getYSize() / 2))
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