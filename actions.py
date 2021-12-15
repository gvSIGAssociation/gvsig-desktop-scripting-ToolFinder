# encoding: utf-8

import gvsig

from org.gvsig.app import ApplicationLocator
from org.gvsig.andami import PluginsLocator
from org.gvsig.scripting.app.extension import ScriptingExtension
from org.gvsig.tools.swing.api import ToolsSwingLocator
from org.gvsig.tools import ToolsLocator
from java.io import File

from toolFinder import ToolFinderPanel

class ToolFinderExtension(ScriptingExtension):
  def __init__(self):
    pass
    
  def canQueryByAction(self):
      return True
  
  def isVisible(self, action):
    if gvsig.currentView()!=None:
      return True
    return False

  def isLayerValid(self, layer):
    return True
    
  def isEnabled(self, action):
    #if not self.isLayerValid(layer):
    #  return False
    if gvsig.currentView()!=None:
      return True
    return False

  def execute(self,actionCommand, *args):
    actionCommand = actionCommand.lower()
    if actionCommand == "settool-toolfinder":
      viewPanel = gvsig.currentView().getWindowOfView()
      mapControl = viewPanel.getMapControl()
      mytool = ToolFinderPanel()
      i18n = ToolsLocator.getI18nManager()
      mytool.showTool(i18n.getTranslation("_Tool_finder"))
      
def selfRegisterI18n():
  i18nManager = ToolsLocator.getI18nManager()
  i18nManager.addResourceFamily("text",File(gvsig.getResource(__file__,"i18n")))
  
def selfRegister():
  selfRegisterI18n()
  i18n = ToolsLocator.getI18nManager()
  application = ApplicationLocator.getManager()
  actionManager = PluginsLocator.getActionInfoManager()
  iconTheme = ToolsSwingLocator.getIconThemeManager().getCurrent()

  toolfinder_icon = File(gvsig.getResource(__file__,"images","toolFinder.png")).toURI().toURL()
  iconTheme.registerDefault("scripting.toolfinder", "action", "tools-toolfinder", None, toolfinder_icon) #quickinfo_icon)

  mytool_extension = ToolFinderExtension()
  mytool_action = actionManager.createAction(
    mytool_extension,
    "tools-toolfinder",   # Action name
    "Tool finder",   # Text
    "settool-toolfinder", # Action command
    "tools-toolfinder",   # Icon name
    None,                # Accelerator
    1009000000,          # Position
    i18n.getTranslation("_Tool_finder")    # Tooltip
  )
  mytool_action = actionManager.registerAction(mytool_action)

  # Añadimos la entrada en el menu herramientas
  application.addMenu(mytool_action, "tools/"+i18n.getTranslation("_Tool_finder"))
  application.addTool(mytool_action, "ToolFinder")

def main(*args):

    selfRegister()
