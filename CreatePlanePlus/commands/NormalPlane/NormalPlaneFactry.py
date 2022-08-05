# FusionAPI_python 
# Author-kantoku

import traceback
import adsk.fusion
import adsk.core

SUPPORT_SKETCH_NAME = 'SupportPlaneRef'

class NormalPlaneFactry():
    def __init__(self, ):
        pass


    def isOnFace(
        self, 
        face: adsk.fusion.BRepFace, 
        pnt: adsk.core.Point3D):

        eva: adsk.core.SurfaceEvaluator = face.evaluator
        _, prm = eva.getParameterAtPoint(pnt)
        return eva.isParameterOnFace(prm)


    def initPlane(
        self,
        face: adsk.fusion.BRepFace, 
        pnt: adsk.core.Point3D) -> adsk.fusion.ConstructionPlane:

        def initSketch(
            comp: adsk.fusion.Component,
            name: str) -> adsk.fusion.Sketch:

            skt: adsk.fusion.Sketch = comp.sketches.add(comp.xYConstructionPlane)
            skt.name = name

            return skt

        def initConstPlane(
            plns: adsk.fusion.ConstructionPlanes,
            surf: adsk.fusion.BRepFace,
            pnt: adsk.fusion.SketchPoint) -> adsk.fusion.ConstructionPlane:

            plnInput: adsk.fusion.ConstructionPlaneInput = plns.createInput()
            if plnInput.setByTangentAtPoint(surf, pnt):
                return plns.add(plnInput)

            return None

        # ****
        if not self.isOnFace(face, pnt):
            return

        comp: adsk.fusion.Component = face.body.parentComponent
        des: adsk.fusion.Design = comp.parentDesign


        baseFeat: adsk.fusion.BaseFeature = None
        if des.designType == adsk.fusion.DesignTypes.ParametricDesignType:
            baseFeat = comp.features.baseFeatures.add()

        if baseFeat:
            baseFeat.startEdit()

        # create sketch
        skt: adsk.fusion.Sketch = initSketch(comp, SUPPORT_SKETCH_NAME)
        skt.isLightBulbOn = False

        # supprt point
        sktPnt: adsk.fusion.SketchPoint = skt.sketchPoints.add(pnt)

        # plane
        constPlanes: adsk.fusion.ConstructionPlanes = comp.constructionPlanes
        constPlane: adsk.fusion.ConstructionPlane = initConstPlane(
            constPlanes,
            face,
            sktPnt
        )

        # remove sketch
        skt.deleteMe()

        if baseFeat:
            baseFeat.finishEdit()

        return constPlane