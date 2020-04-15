# FusionAPI_python 
# Author-kantoku

import adsk.core, adsk.fusion, traceback

from .Fusion360Utilities.Fusion360Utilities import AppObjects
from .Fusion360Utilities.Fusion360CommandBase import Fusion360CommandBase


# SelectionCommandInput用情報
_selInfo = ['dlgSel','平面位置','平面位置クリック']

# サポートスケッチ名
_supportSktName = 'Plane Support'


class ViewPlane(Fusion360CommandBase):
    _handlers = []
    _clickPoint = adsk.core.Point3D.cast(None)

    def __init__(self, cmd_def, debug):
        super().__init__(cmd_def, debug)
        pass

    def on_preview(self, command: adsk.core.Command, inputs: adsk.core.CommandInputs, args, input_values):
        pass

    def on_destroy(self, command: adsk.core.Command, inputs: adsk.core.CommandInputs, reason, input_values):
        pass

    def on_input_changed(self, command: adsk.core.Command, inputs: adsk.core.CommandInputs, changed_input, input_values):
        pass

    def on_execute(self, command: adsk.core.Command, inputs: adsk.core.CommandInputs, args, input_values):
        ao = AppObjects()
        try:
            global _clickPoint
            fact = PlaneFactry(_clickPoint)
            fact.exec()

        except:
            if ao.ui:
                ao.ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
            pass

    def on_create(self, command: adsk.core.Command, inputs: adsk.core.CommandInputs):
        ao = AppObjects()

        # comp Position check
        command.isPositionDependent=True

        # event
        onSelect = self.SelectHandler()
        command.select.add(onSelect)
        self._handlers.append(onSelect)

        onUnselect = self.UnselectHandler()
        command.unselect.add(onUnselect)
        self._handlers.append(onUnselect)

        # Dialog
        inputs.command.setDialogInitialSize(500,1000)

        global _selInfo
        inputs.addSelectionInput(_selInfo[0], _selInfo[1], _selInfo[2])

    # -- Support functions --
    def isPositionUndetermined(self) -> bool:
        ao = AppObjects()
        pnl = ao.ui.allToolbarPanels.itemById('SnapshotPanel')
        return pnl.isVisible

    # -- Support class --
    class SelectHandler(adsk.core.SelectionEventHandler):
        def __init__(self):
            super().__init__()

        def notify(self, args):
            args = adsk.core.SelectionEventArgs.cast(args)

            global _clickPoint
            _clickPoint = args.selection.point

    class UnselectHandler(adsk.core.SelectionEventHandler):
        def __init__(self):
            super().__init__()

        def notify(self, args):
            args = adsk.core.SelectionEventArgs.cast(args)

            global _clickPoint
            _clickPoint = None

class PlaneFactry():

    _pnt = adsk.core.Point3D.cast(None)

    def __init__(self,
        pnt :adsk.core.Point3D):

        self._pnt = pnt
    
    def exec(self):
        def initSupportLine(
            skt :adsk.fusion.Sketch,
            pnt :adsk.core.Point3D) -> adsk.fusion.SketchLine:

            ao = AppObjects()

            cam :adsk.core.Camera = ao.app.activeViewport.camera
            vec :adsk.core.Vector3D = cam.eye.vectorTo(cam.target)
            vec.scaleBy(0.1)

            tmpPnt :adsk.core.Point3D = pnt.copy()
            tmpPnt.translateBy(vec)

            lines :adsk.fusion.SketchLines = skt.sketchCurves.sketchLines
            return lines.addByTwoPoints(pnt, tmpPnt)

        def initSketch(
            comp :adsk.fusion.Component,
            name :str) -> adsk.fusion.Sketch:

            skt :adsk.fusion.Sketch = comp.sketches.add(comp.xYConstructionPlane)
            skt.name = name

            return skt

        def initPlane(
            plns :adsk.fusion.ConstructionPlanes,
            lne :adsk.fusion.SketchLine) -> adsk.fusion.ConstructionPlane:

            plnInput = plns.createInput()
            dist = adsk.core.ValueInput.createByReal(0)
            pln :adsk.fusion.ConstructionPlane = None
            if plnInput.setByDistanceOnPath(lne, dist):
                pln = plns.add(plnInput)

            return pln

        # def GetRootMatrix(
        #     comp :adsk.fusion.Component) -> adsk.core.Matrix3D:
            
        #     des = adsk.fusion.Design.cast(comp.parentDesign)
        #     root = des.rootComponent

        #     mat = adsk.core.Matrix3D.create()
        
        #     if comp == root:
        #         return mat

        #     occs = root.allOccurrencesByComponent(comp)
        #     if len(occs) < 1:
        #         return mat

        #     occ = occs[0]
        #     occ_names = occ.fullPathName.split('+')
        #     occs = [root.allOccurrences.itemByName(name) 
        #                 for name in occ_names]
        #     mat3ds = [occ.transform for occ in occs]
        #     # mat3ds.reverse() #important!!
        #     for mat3d in mat3ds:
        #         mat.transformBy(mat3d)

        #     return mat

        # start
        ao = AppObjects()
        comp :adsk.fusion.Component = ao.design.activeComponent

        # DesignType check
        desTypes = adsk.fusion.DesignTypes
        desTypeParam = ao.design.designType == desTypes.ParametricDesignType

        # Parametric
        baseFeat = adsk.fusion.BaseFeature.cast(None)
        if desTypeParam:
            baseFeats = comp.features.baseFeatures
            baseFeat :adsk.fusion.BaseFeature = baseFeats.add()

            baseFeat.startEdit()

        # create sketch
        global _supportSktName
        skt :adsk.fusion.Sketch = initSketch(comp, _supportSktName)
        skt.isLightBulbOn = False

        # supprt line
        line :adsk.fusion.SketchLine = initSupportLine(skt, self._pnt)

        # plane
        planes :adsk.fusion.ConstructionPlanes = comp.constructionPlanes
        plane :adsk.fusion.ConstructionPlane = initPlane(planes, line)

        # mat
        # mat :adsk.core.Matrix3D = GetRootMatrix(comp)
        # plane.transform = mat

        # remove sketch
        skt.deleteMe()

        # Parametric
        if desTypeParam:
            baseFeat.finishEdit()