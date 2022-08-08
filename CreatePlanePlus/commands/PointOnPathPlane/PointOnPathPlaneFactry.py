# FusionAPI_python 
# Author-kantoku

import traceback
import adsk.fusion
import adsk.core

DESIGN_TYPES = adsk.fusion.DesignTypes

class PointOnPathPlaneFactry():
    def __init__(self, ):
        pass

    def _getGeo(
        self,
        entity):

        geo = None
        if hasattr(entity, 'worldGeometry'):
            geo = entity.worldGeometry
        elif hasattr(entity, 'geometry'):
            geo = entity.geometry

        return geo

    def isOnCurve(
        self, 
        crvEntity,
        pntEntity) -> bool:

        crvGeo: adsk.core.Curve3D = self._getGeo(crvEntity)
        pntGeo: adsk.core.Point3D = self._getGeo(pntEntity)

        if not all([crvGeo, pntGeo]):
            return False

        eva: adsk.core.CurveEvaluator3D = crvGeo.evaluator
        _, prm = eva.getParameterAtPoint(pntGeo)
        _, prmPnt = eva.getPointAtParameter(prm)

        return pntGeo.isEqualTo(prmPnt)


    def _getCurveOnPointRatio(
        self,
        crvEntity,
        pntEntity) -> float:

        crvGeo: adsk.core.Curve3D = self._getGeo(crvEntity)
        pntGeo: adsk.core.Point3D = self._getGeo(pntEntity)

        eva: adsk.core.CurveEvaluator3D = crvGeo.evaluator
        _, prm = eva.getParameterAtPoint(pntGeo)
        _, sPrm, _ = eva.getParameterExtents()
        _, length = eva.getLengthAtParameter(sPrm, prm)

        retio = length / crvEntity.length
        if retio < 0:
            retio = 0
        elif retio > 1:
            retio = 1

        return retio


    def initPlane(
        self,
        crvEntity,
        pntEntity) -> adsk.fusion.ConstructionPlane:

        def initConstPlane(
            plns: adsk.fusion.ConstructionPlanes,
            crvEntity,
            ratio: float) -> adsk.fusion.ConstructionPlane:

            dist: adsk.core.ValueInput = adsk.core.ValueInput.createByReal(ratio)

            plnInput: adsk.fusion.ConstructionPlaneInput = plns.createInput()
            if plnInput.setByDistanceOnPath(crvEntity, dist):
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

        comp: adsk.fusion.Component = getComp(crvEntity)
        des: adsk.fusion.Design = comp.parentDesign

        # direct mode
        returnDesignType = False
        if des.designType == DESIGN_TYPES.DirectDesignType:
            returnDesignType = True
            crvToken = crvEntity.entityToken
            pntToken = pntEntity.entityToken
            des.designType = DESIGN_TYPES.ParametricDesignType
            crvEntity = des.findEntityByToken(crvToken)[0]
            pntEntity = des.findEntityByToken(pntToken)[0]

        ratio = self._getCurveOnPointRatio(crvEntity, pntEntity)

        # plane
        constPlanes: adsk.fusion.ConstructionPlanes = comp.constructionPlanes
        constPlane: adsk.fusion.ConstructionPlane = initConstPlane(
            constPlanes,
            crvEntity,
            ratio
        )

        # direct mode
        if returnDesignType:
            des.designType = DESIGN_TYPES.DirectDesignType

        return constPlane