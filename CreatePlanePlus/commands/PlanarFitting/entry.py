import adsk.core as core
import adsk.fusion as fusion
import os
from ...lib import fusion360utils as futil
from ... import config
app = core.Application.get()
ui = app.userInterface

from .PlanarFittingFactry import NormalPlaneFactry

# TODO *** Specify the command identity information. ***
CMD_ID = f'{config.COMPANY_NAME}_{config.ADDIN_NAME}_planarFitting'
CMD_NAME = 'フィッティング平面'
CMD_Description = '点群から平面を作成します'

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


_selIpt: core.SelectionCommandInput = None
_selCountMin: int = 3
_fact: 'NormalPlaneFactry' = None


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


def command_created(args: core.CommandCreatedEventArgs):
    futil.log(f'{CMD_NAME} {args.firingEvent.name}')

    args.command.isPositionDependent = True
    args.command.isAutoExecute = False

    # inputs
    inputs = args.command.commandInputs

    global _selIpt, _selCountMin
    _selIpt = inputs.addSelectionInput(
        'dlgSel',
        '点',
        '3個以上の点を選択'
    )
    _selIpt.setSelectionLimits(_selCountMin)
    _selIpt.addSelectionFilter("SketchPoints")
    _selIpt.addSelectionFilter("Vertices")
    _selIpt.addSelectionFilter("ConstructionPoints")

    # events
    futil.add_handler(args.command.executePreview, command_preview, local_handlers=local_handlers)
    futil.add_handler(args.command.destroy, command_destroy, local_handlers=local_handlers)

    global _fact
    _fact = NormalPlaneFactry()


def command_preview(args: core.CommandEventArgs):
    futil.log(f'{CMD_NAME} {args.firingEvent.name}')

    global _selIpt, _selCountMin
    ents = [_selIpt.selection(idx).entity for idx in range(_selIpt.selectionCount)]

    global _fact
    points = list(
        filter(
            None,
            [_fact.get_point3d(e) for e in ents]
        )
    )
    if len(points) < _selCountMin: return

    _fact.create_fit_plane(points)

    args.isValidResult = True


def command_destroy(args: core.CommandEventArgs):
    futil.log(f'{CMD_NAME} {args.firingEvent.name}')

    global local_handlers
    local_handlers = []