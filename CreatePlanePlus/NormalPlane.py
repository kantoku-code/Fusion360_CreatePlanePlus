# FusionAPI_python 
# Author-kantoku

import adsk.core, adsk.fusion, traceback

from .Fusion360Utilities.Fusion360Utilities import AppObjects
from .Fusion360Utilities.Fusion360CommandBase import Fusion360CommandBase


# SelectionCommandInput用情報
_selInfo = ['dlgSel','参照面','面クリック']

# サポートスケッチ名
_supportSktName = 'Plane Support'


class NormalPlane(Fusion360CommandBase):
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
            global _clickPoint, _selInfo
            fact = PlaneFactry(input_values[_selInfo[0]][0], _clickPoint)
            fact.exec()

        except:
            if ao.ui:
                ao.ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

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
        selIpt = inputs.addSelectionInput(_selInfo[0], _selInfo[1], _selInfo[2])
        selIpt.addSelectionFilter('Faces')

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
    _surf = adsk.fusion.BRepFace.cast(None)

    def __init__(self, 
        surf :adsk.fusion.BRepFace, 
        pnt :adsk.core.Point3D):

        self._pnt = pnt
        self._surf = surf
    
    def exec(self):
        def initSketch(
            comp :adsk.fusion.Component,
            name :str) -> adsk.fusion.Sketch:

            skt :adsk.fusion.Sketch = comp.sketches.add(comp.xYConstructionPlane)
            skt.name = name

            return skt

        def initPlane(
            plns :adsk.fusion.ConstructionPlanes,
            surf :adsk.fusion.BRepFace,
            pnt :adsk.fusion.SketchPoint):

            plnInput = plns.createInput()
            if plnInput.setByTangentAtPoint(surf, pnt):
                plns.add(plnInput)

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
            baseFeat = baseFeats.add()

            baseFeat.startEdit()

        # create sketch
        global _supportSktName
        skt :adsk.fusion.Sketch = initSketch(comp, _supportSktName)
        skt.isLightBulbOn = False

        # supprt point
        pnt :adsk.fusion.SketchPoint = skt.sketchPoints.add(self._pnt)

        # plane
        planes:adsk.fusion.ConstructionPlanes = comp.constructionPlanes
        initPlane(planes, self._surf, pnt)

        # remove sketch
        skt.deleteMe()

        # Parametric
        if desTypeParam:
            baseFeat.finishEdit()
