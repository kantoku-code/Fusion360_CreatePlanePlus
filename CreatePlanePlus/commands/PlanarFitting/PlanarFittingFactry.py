# FusionAPI_python 
# Author-kantoku

import traceback
import adsk.fusion as fusion
import adsk.core as core

import sys
import pathlib

THIS_DIR = pathlib.Path(__file__).resolve().parent
PACKAGE_PATH = str(THIS_DIR.parent.parent / "lib" / "site-packages")
if not PACKAGE_PATH in sys.path:
    sys.path.append(PACKAGE_PATH)

import numpy as np


class PlanarFittingFactry():
    def __init__(self, ):
        pass

    def get_point3d(
        self,
        entity,
    ) -> core.Point3D:

        if entity.objectType == fusion.SketchPoint.classType():
            return entity.worldGeometry
        elif entity.objectType == fusion.BRepVertex.classType():
            return entity.geometry
        elif entity.objectType == fusion.ConstructionPoint.classType():
            return entity.geometry
        else:
            return None


    def create_fit_plane(
        self,
        pointList: list[core.Point3D],
    ) -> fusion.ConstructionPlane:

        def fit_plane(pointList: list[core.Point3D]):
            point_cloud = np.array(pointList)

            com = np.sum(point_cloud, axis=0) / len(point_cloud)
            q = point_cloud - com
            Q = np.dot(q.T, q)
            la, vectors = np.linalg.eig(Q)
            plane_v = vectors.T[np.argmin(la)]

            return plane_v, com

        # *************

        normal, origin = fit_plane(
            [p.asArray() for p in pointList]
        )

        app: core.Application = core.Application.get()
        des: fusion.Design = app.activeProduct
        root: fusion.Component = des.rootComponent

        plane: core.Plane = core.Plane.create(
            core.Point3D.create(*origin.tolist()),
            core.Vector3D.create(*normal.tolist()),
        )

        baseFeat: fusion.BaseFeature = None
        if des.designType == fusion.DesignTypes.ParametricDesignType:
            baseFeat = root.features.baseFeatures.add()

        planes: fusion.ConstructionPlanes = root.constructionPlanes
        planeIpt: fusion.ConstructionPlaneInput = planes.createInput()
        constPlane: fusion.ConstructionPlane = None
        if baseFeat:
            try:
                baseFeat.startEdit()
                planeIpt.setByPlane(plane)
                constPlane = planes.add(planeIpt)
            except:
                pass
            finally:
                baseFeat.finishEdit()
        else:
            planeIpt.setByPlane(plane)
            constPlane = planes.add(planeIpt)
        constPlane.name = "Fit Plane"

        eva: core.SurfaceEvaluator = constPlane.geometry.evaluator
        _, prms = eva.getParametersAtPoints(pointList)

        mat: core.Matrix3D = constPlane.transform
        mat.invert()
        p: core.Point3D = None
        [p.transformBy(mat) for p in pointList]
        prms = [core.Point2D.create(p.x, p.y) for p in pointList]

        bBox: core.BoundingBox2D = constPlane.displayBounds.copy()
        [bBox.expand(p) for p in prms]

        constPlane.displayBounds = bBox

        return constPlane