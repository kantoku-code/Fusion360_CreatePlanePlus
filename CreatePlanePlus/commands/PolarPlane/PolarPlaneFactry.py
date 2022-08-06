# FusionAPI_python 
# Author-kantoku

import traceback
import adsk.fusion
import adsk.core

SUPPORT_SKETCH_NAME = 'SupportPlaneRef'

class PolarPlaneFactry():
    def __init__(self, ):
        pass

    def initPlane(
        self,
        body: adsk.fusion.BRepBody,
        linerEntity: adsk.core.Base) -> list:

        # *******
        def getNormalVec(
            entity) -> adsk.core.Vector3D:

            def getMat(
                entity) -> adsk.core.Matrix3D:

                occ: adsk.fusion.Occurrence = entity.assemblyContext
                if occ:
                    return occ.transform2

            # *****
            mat: adsk.core.Matrix3D = getMat(entity)

            geo = entity.geometry
            if mat:
                geo.transformBy(mat)

            if hasattr(entity, 'worldGeometry'):
                geo = entity.worldGeometry

            if hasattr(geo, 'normal'):
                return geo.normal
            elif hasattr(geo, 'direction'):
                return geo.direction
            elif hasattr(geo, 'asInfiniteLine'):
                inf: adsk.core.InfiniteLine3D = geo.asInfiniteLine()
                return inf.direction

            raise Exception

        def initVerticalPlanes(
            comp: adsk.fusion.Component,
            bBox: adsk.core.OrientedBoundingBox3D,
            vec: adsk.core.Vector3D,) -> list:

            # ******
            def getVerticalPlanes(body, vec):
                constPlanes: adsk.fusion.ConstructionPlanes = comp.constructionPlanes

                planes = []
                face: adsk.fusion.BRepFace = None
                for face in body.faces:
                    if not direction.isParallelTo(getNormalVec(face)):
                        continue
                    plnIpt: adsk.fusion.ConstructionPlaneInput = constPlanes.createInput()
                    plnIpt.setByOffset(
                        face,
                        adsk.core.ValueInput.createByReal(0)
                    )
                    # constPlane: adsk.fusion.ConstructionPlane = constPlanes.add(plnIpt)
                    # planes.append(constPlane.geometry.copy())
                    # constPlane.deleteMe()
                    planes.append(constPlanes.add(plnIpt))
                return planes

            def getPlanes(comp, bBox, vec) -> list:
                tmpMgr: adsk.fusion.TemporaryBRepManager = adsk.fusion.TemporaryBRepManager.get()
                box: adsk.fusion.BRepBody = tmpMgr.createBox(bBox)

                baseFeat: adsk.fusion.BaseFeature = None
                if des.designType == adsk.fusion.DesignTypes.ParametricDesignType:
                    baseFeat = comp.features.baseFeatures.add()

                brepBodies: adsk.fusion.BRepBodies = comp.bRepBodies

                planes = []
                boxBody: adsk.fusion.BRepBody = None
                if baseFeat:
                    baseFeat.startEdit()
                    boxBody = brepBodies.add(box, baseFeat)
                    planes = getVerticalPlanes(boxBody, vec)
                    boxBody.deleteMe()
                    baseFeat.finishEdit()
                else:
                    boxBody = brepBodies.add(box, baseFeat)
                    planes = getVerticalPlanes(boxBody, vec)
                    boxBody.deleteMe()

                return planes

            # ******
            return getPlanes(comp, bBox, vec)

        def getBoundingBox(
            body: adsk.fusion.BRepBody,
            direction: adsk.core.Vector3D) -> adsk.core.OrientedBoundingBox3D:

            plane = adsk.core.Plane = adsk.core.Plane.create(
                adsk.core.Point3D.create(0,0,0),
                direction
            )

            app: adsk.core.Application = adsk.core.Application.get()
            measMgr: adsk.core.MeasureManager = app.measureManager
            return measMgr.getOrientedBoundingBox(
                body,
                plane.vDirection,
                plane.uDirection
            )

        # ****************

        app: adsk.core.Application = adsk.core.Application.get()
        des: adsk.fusion.Design = app.activeProduct
        comp: adsk.fusion.Component = body.parentComponent

        # get vector
        direction: adsk.core.Vector3D = getNormalVec(linerEntity)

        # get OrientedBoundingBox
        bBox: adsk.core.OrientedBoundingBox3D = getBoundingBox(
            body,
            direction
        )

        # get Vertical Planes
        return initVerticalPlanes(comp, bBox, direction)