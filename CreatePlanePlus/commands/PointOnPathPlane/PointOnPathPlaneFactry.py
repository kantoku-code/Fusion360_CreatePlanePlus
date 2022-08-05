# FusionAPI_python 
# Author-kantoku

import traceback
import adsk.fusion
import adsk.core

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

    # def _getCurveOnPointDistance(
    #     self,
    #     crvEntity,
    #     pntEntity) -> float:

    #     crvGeo: adsk.core.Curve3D = self._getGeo(crvEntity)
    #     pntGeo: adsk.core.Point3D = self._getGeo(pntEntity)

    #     eva: adsk.core.CurveEvaluator3D = crvGeo.evaluator
    #     _, prm = eva.getParameterAtPoint(pntGeo)
    #     _, sPrm, _ = eva.getParameterExtents()

    #     _, length = eva.getLengthAtParameter(sPrm, prm)

    #     return length


    def _getCurveOnPointRatio(
        self,
        crvEntity,
        pntEntity) -> float:

        crvGeo: adsk.core.Curve3D = self._getGeo(crvEntity)
        pntGeo: adsk.core.Point3D = self._getGeo(pntEntity)

        eva: adsk.core.CurveEvaluator3D = crvGeo.evaluator
        _, prm = eva.getParameterAtPoint(pntGeo)
        _, sPrm, ePrm = eva.getParameterExtents()
        _, length = eva.getLengthAtParameter(sPrm, prm)

        return length / crvEntity.length


    def initPlane(
        self,
        crvEntity,
        pntEntity) -> adsk.fusion.ConstructionPlane:

        def initConstPlane(
            plns: adsk.fusion.ConstructionPlanes,
            crvEntity,
            ratio: float) -> adsk.fusion.ConstructionPlane:

            dist: adsk.core.ValueInput = adsk.core.ValueInput.createByReal(ratio)

            # unitMgr: adsk.core.UnitsManager = plns.component.parentDesign.unitsManager
            
            # dist: adsk.core.ValueInput = adsk.core.ValueInput.createByString(
            #     unitMgr.formatInternalValue(length)
            # )

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
        # des: adsk.fusion.Design = comp.parentDesign

        # length = self._getCurveOnPointDistance(crvEntity, pntEntity)
        ratio = self._getCurveOnPointRatio(crvEntity, pntEntity)

        # baseFeat: adsk.fusion.BaseFeature = None
        # if des.designType == adsk.fusion.DesignTypes.ParametricDesignType:
        #     baseFeat = comp.features.baseFeatures.add()

        # if baseFeat:
        #     baseFeat.startEdit()

        # plane
        constPlanes: adsk.fusion.ConstructionPlanes = comp.constructionPlanes
        constPlane: adsk.fusion.ConstructionPlane = initConstPlane(
            constPlanes,
            crvEntity,
            ratio
        )

        # if baseFeat:
        #     baseFeat.finishEdit()

        return constPlane