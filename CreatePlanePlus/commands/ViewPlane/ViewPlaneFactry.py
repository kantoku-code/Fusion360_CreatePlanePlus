# FusionAPI_python 
# Author-kantoku

import traceback
import adsk.fusion
import adsk.core

SUPPORT_SKETCH_NAME = 'SupportPlaneRef'

class ViewPlaneFactry():
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
        entity,
        pnt: adsk.core.Point3D) -> adsk.fusion.ConstructionPlane:

        def initSupportLine(
            skt: adsk.fusion.Sketch,
            pnt: adsk.core.Point3D) -> adsk.fusion.SketchLine:

            app: adsk.core.Application = adsk.core.Application.get()

            cam: adsk.core.Camera = app.activeViewport.camera
            vec: adsk.core.Vector3D = cam.eye.vectorTo(cam.target)
            vec.scaleBy(0.1)

            tmpPnt: adsk.core.Point3D = pnt.copy()
            tmpPnt.translateBy(vec)

            lines: adsk.fusion.SketchLines = skt.sketchCurves.sketchLines
            return lines.addByTwoPoints(pnt, tmpPnt)

        def initSketch(
            comp: adsk.fusion.Component,
            name: str) -> adsk.fusion.Sketch:

            skt: adsk.fusion.Sketch = comp.sketches.add(comp.xYConstructionPlane)
            skt.name = name

            return skt

        def initConstPlane(
            plns: adsk.fusion.ConstructionPlanes,
            line: adsk.fusion.SketchLine) -> adsk.fusion.ConstructionPlane:

            plnInput: adsk.fusion.ConstructionPlaneInput = plns.createInput()
            dist: adsk.core.ValueInput = adsk.core.ValueInput.createByReal(0)
            if plnInput.setByDistanceOnPath(line, dist):
                return plns.add(plnInput)

            return None

        def getComp(
            ent) -> adsk.fusion.Component:

            if hasattr(ent, 'parent'):
                if ent.parent.objectType == adsk.fusion.Component.objectType:
                    return ent.parent

            if hasattr(ent, 'body'):
                return ent.body.parentComponent

            app: adsk.core.Application = adsk.core.Application.get()
            des: adsk.fusion.Design = app.activeProduct
            return des.activeComponent

        # ****
        comp: adsk.fusion.Component = getComp(entity)
        des: adsk.fusion.Design = comp.parentDesign

        baseFeat: adsk.fusion.BaseFeature = None
        if des.designType == adsk.fusion.DesignTypes.ParametricDesignType:
            baseFeat = comp.features.baseFeatures.add()

        if baseFeat:
            baseFeat.startEdit()

        # create sketch
        skt: adsk.fusion.Sketch = initSketch(comp, SUPPORT_SKETCH_NAME)
        skt.isLightBulbOn = False

        # supprt line
        line: adsk.fusion.SketchLine = initSupportLine(skt, pnt)

        # plane
        constPlanes: adsk.fusion.ConstructionPlanes = comp.constructionPlanes
        constPlane: adsk.fusion.ConstructionPlane = initConstPlane(
            constPlanes,
            line
        )

        # remove sketch
        skt.deleteMe()

        if baseFeat:
            baseFeat.finishEdit()

        return constPlane