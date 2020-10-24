# FusionAPI_python Addin
# Author-kantoku

from .ViewPlane import ViewPlane
from .NormalPlane import NormalPlane

import adsk.core, adsk.fusion

commands = []
command_definitions = []
separator = adsk.core.SeparatorControl.cast(None)

# ViewPlane
cmd = {
    'cmd_name': '画面向きの平面',
    'cmd_description': 'コマンド実行時の向きに平面を作成します',
    'cmd_id': 'ViewPlane',
    'cmd_resources': './resources/viewplane',
    'workspace': 'FusionSolidEnvironment',
    'toolbar_panel_id': 'ConstructionPanel',
    'class': ViewPlane
}
command_definitions.append(cmd)

# NormalPlane
cmd = {
    'cmd_name': '法線方向の平面',
    'cmd_description': 'クリックした位置の面の法線の向きの平面を作成します',
    'cmd_id': 'NormalPlane',
    'cmd_resources': './resources/normalplane',
    'workspace': 'FusionSolidEnvironment',
    'toolbar_panel_id': 'ConstructionPanel',
    'class': NormalPlane
}
command_definitions.append(cmd)

# Set to True to display various useful messages when debugging your app
debug = False#True#
# Don't change anything below here:
for cmd_def in command_definitions:
    command = cmd_def['class'](cmd_def, debug)
    commands.append(command)


def run(context):
    separator = addSeparator('SolidTab', 'ConstructionPanel')

    for run_command in commands:
        run_command.on_run()

def stop(context):
    if separator:
        separator.deleteMe()

    for stop_command in commands:
        stop_command.on_stop()

# -- Support fanction --
def addSeparator(
    tabId :str,
    panelId :str):

    app = adsk.core.Application.get()
    ui = app.userInterface

    if not ui.isTabbedToolbarUI: return

    # 'デザイン' の全タブを取得
    desTabs = adsk.core.ToolbarTabs.cast(None)
    desTabs = ui.toolbarTabsByProductType('DesignProductType')
    if desTabs.count < 1: return

    # 目的のタブ取得
    targetTab :adsk.core.ToolbarTab = desTabs.itemById(tabId)
    if not targetTab: return

    # 目的のタブ内の全パネル取得
    panels :adsk.core.ToolbarPanels = targetTab.toolbarPanels
    if panels.count < 1: return

    # 目的のパネル取得
    targetpanel :adsk.core.ToolbarPanel = panels.itemById(panelId)

    # パネル内のコントロール取得
    controls :adsk.core.ToolbarControls = targetpanel.controls

    # セパレータ追加
    return controls.addSeparator()