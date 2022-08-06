import adsk.core
import adsk.fusion
import os
from ...lib import fusion360utils as futil
from ... import config
app = adsk.core.Application.get()
ui = app.userInterface

from .PolarPlaneFactry import PolarPlaneFactry

# TODO *** Specify the command identity information. ***
CMD_ID = f'{config.COMPANY_NAME}_{config.ADDIN_NAME}_polarPlane'
CMD_NAME = '極平面'
CMD_Description = 'ボディと方向を指定し、極平面を作成します'

# Specify that the command will be promoted to the panel.
IS_PROMOTED = False

# TODO *** Define the location where the command button will be created. ***
# This is done by specifying the workspace, the tab, and the panel, and the 
# command it will be inserted beside. Not providing the command to position it
# will insert it at the end.
WORKSPACE_ID = 'FusionSolidEnvironment'
PANEL_ID = 'ConstructionPanel'
COMMAND_BESIDE_ID = 'WorkPlaneAlongPathCommand'

# Resource location for command icons, here we assume a sub folder in this directory named "resources".
ICON_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'resources', '')

# Local list of event handlers used to maintain a reference so
# they are not released and garbage collected.
local_handlers = []


_bodyIpt: adsk.core.SelectionCommandInput = None
_directionIpt: adsk.core.SelectionCommandInput = None
_fact: 'PolarPlaneFactry' = None


# Executed when add-in is run.
def start():
    # Create a command Definition.
    cmd_def = ui.commandDefinitions.addButtonDefinition(CMD_ID, CMD_NAME, CMD_Description, ICON_FOLDER)

    # Define an event handler for the command created event. It will be called when the button is clicked.
    futil.add_handler(cmd_def.commandCreated, command_created)

    # ******** Add a button into the UI so the user can run the command. ********
    # Get the target workspace the button will be created in.
    workspace = ui.workspaces.itemById(WORKSPACE_ID)

    # Get the panel the button will be created in.
    panel = workspace.toolbarPanels.itemById(PANEL_ID)

    # Create the button command control in the UI after the specified existing command.
    control = panel.controls.addCommand(cmd_def, COMMAND_BESIDE_ID, False)

    # Specify if the command is promoted to the main toolbar. 
    control.isPromoted = IS_PROMOTED


# Executed when add-in is stopped.
def stop():
    # Get the various UI elements for this command
    workspace = ui.workspaces.itemById(WORKSPACE_ID)
    panel = workspace.toolbarPanels.itemById(PANEL_ID)
    command_control = panel.controls.itemById(CMD_ID)
    command_definition = ui.commandDefinitions.itemById(CMD_ID)

    # Delete the button command control
    if command_control:
        command_control.deleteMe()

    # Delete the command definition
    if command_definition:
        command_definition.deleteMe()


def command_created(args: adsk.core.CommandCreatedEventArgs):
    futil.log(f'{CMD_NAME} {args.firingEvent.name}')

    args.command.isPositionDependent = True

    # inputs
    inputs = args.command.commandInputs

    global _bodyIpt, _directionIpt
    _bodyIpt = inputs.addSelectionInput(
        'bodyIpt',
        'ボディ',
        'ボディを選択して下さい'
    )
    _bodyIpt.addSelectionFilter('Bodies')
    _bodyIpt.setSelectionLimits(0)

    _directionIpt = inputs.addSelectionInput(
        'directionIpt',
        '方向',
        '方向となる要素を選択して下さい'
    )
    _directionIpt.addSelectionFilter('SketchLines')
    _directionIpt.addSelectionFilter('ConstructionLines')
    _directionIpt.addSelectionFilter('ConstructionPlanes')
    _directionIpt.addSelectionFilter('LinearEdges')
    _directionIpt.addSelectionFilter('PlanarFaces')
    _directionIpt.setSelectionLimits(0)

    # events
    # futil.add_handler(args.command.execute, command_execute, local_handlers=local_handlers)
    futil.add_handler(args.command.inputChanged, command_input_changed, local_handlers=local_handlers)
    futil.add_handler(args.command.executePreview, command_preview, local_handlers=local_handlers)
    futil.add_handler(args.command.validateInputs, command_validate_input, local_handlers=local_handlers)
    futil.add_handler(args.command.destroy, command_destroy, local_handlers=local_handlers)
    futil.add_handler(args.command.preSelect, command_preSelect, local_handlers=local_handlers)

    global _fact
    _fact = PolarPlaneFactry()


def command_preSelect(args: adsk.core.SelectionEventArgs):
    futil.log(f'{CMD_NAME} {args.firingEvent.name}')

    selIpt: adsk.core.SelectionCommandInput = args.activeInput

    if selIpt.selectionCount > 0:
        args.isSelectable = False


def command_execute(args: adsk.core.CommandEventArgs):
    futil.log(f'{CMD_NAME} {args.firingEvent.name}')

def command_preview(args: adsk.core.CommandEventArgs):
    futil.log(f'{CMD_NAME} {args.firingEvent.name}')

    global _fact, _bodyIpt, _directionIpt
    _fact.initPlane(
        _bodyIpt.selection(0).entity,
        _directionIpt.selection(0).entity,
    )

    args.isValidResult = True


def command_input_changed(args: adsk.core.InputChangedEventArgs):
    futil.log(f'{CMD_NAME} {args.firingEvent.name}')

    if args.input.classType() != adsk.core.SelectionCommandInput.classType():
        return

    global _bodyIpt
    if _bodyIpt.selectionCount < 1:
        _bodyIpt.hasFocus = True
        return

    global _directionIpt
    if _directionIpt.selectionCount < 1:
        _directionIpt.hasFocus = True


def command_validate_input(args: adsk.core.ValidateInputsEventArgs):
    futil.log(f'{CMD_NAME} {args.firingEvent.name}')

    global _bodyIpt, _directionIpt
    if _bodyIpt.selectionCount < 1 or _directionIpt.selectionCount < 1:
        args.areInputsValid = False


def command_destroy(args: adsk.core.CommandEventArgs):
    futil.log(f'{CMD_NAME} {args.firingEvent.name}')

    global local_handlers
    local_handlers = []