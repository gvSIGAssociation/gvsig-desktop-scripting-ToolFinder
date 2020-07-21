# encoding: utf-8

import gvsig
from gvsig import geom
from gvsig.libs.formpanel import FormPanel
from org.gvsig.andami import PluginsLocator
from org.gvsig.tools.util import LabeledValueImpl
from org.gvsig.tools.swing.api import ToolsSwingLocator
from java.awt.event import MouseAdapter

class MyMouseListener(MouseAdapter):
  def mouseClicked(self, evt):
        mylist = evt.getSource()
        index = None
        if (evt.getClickCount() == 2):
            index = mylist.locationToIndex(evt.getPoint())
        elif (evt.getClickCount() == 3):
            index = mylist.locationToIndex(evt.getPoint())
        value = mylist.getSelectedValue().getValue()
        value.execute()
        
class ToolFinderPanel(FormPanel):
    def __init__(self):
        FormPanel.__init__(self,gvsig.getResource(__file__, "toolFinder.xml"))
        self.listController = None
        self.initUI()
        self.updateControls()
    def initUI(self):
      toolsSwingManager = ToolsSwingLocator.getToolsSwingManager()
      self.listController = toolsSwingManager.createFilteredListController(
              self.lstActions,
              self.txtFilter,
              self.btnFilter
      )
      self.lstActions.addMouseListener(MyMouseListener())
      
    def updateControls(self):
      indexAttributes = self.lstActions.getSelectedIndex()
      toolsSwingManager = ToolsSwingLocator.getToolsSwingManager()
      model = toolsSwingManager.createFilteredListModel()
      actions = PluginsLocator.getActionInfoManager().getActions()
      
      for action in actions:
        labeled = LabeledValueImpl(action.getName(), action)
        if (action.isEnabled()):
          model.addElement(labeled)
      model.setFilter(self.txtFilter.getText())
      model.sort(True)
      self.lstActions.setModel(model);
      self.lstActions.setSelectedIndex(indexAttributes);

def main(*args):
    l = ToolFinderPanel()
    l.showTool("_Tool_Finder")
    pass