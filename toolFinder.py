# encoding: utf-8

import gvsig
from gvsig import geom
from gvsig.libs.formpanel import FormPanel
from org.gvsig.andami import PluginsLocator
from org.gvsig.tools.util import LabeledValueImpl
from org.gvsig.tools.swing.api import ToolsSwingLocator
from org.gvsig.tools import ToolsLocator
from java.awt.event import MouseAdapter

class MyMouseListener(MouseAdapter):
  def __init__(self,panel):
    self.panel = panel
    
  def mouseClicked(self, evt):
        mylist = evt.getSource()
        index = None
        if (evt.getClickCount() == 2):
            index = mylist.locationToIndex(evt.getPoint())
        elif (evt.getClickCount() == 3):
            index = mylist.locationToIndex(evt.getPoint())
        value = mylist.getSelectedValue().getValue()
        if value.isVisible() and value.isEnabled():
          self.panel.lblMessage.setText("")
          value.execute()
        else:
          self.panel.lblMessage.setText("Herramienta no activa")
        
        
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
      self.lstActions.addMouseListener(MyMouseListener(self))
      self.lblMessage.setText("")
      
    def updateControls(self):
      i18n = ToolsLocator.getI18nManager();
      indexAttributes = self.lstActions.getSelectedIndex()
      toolsSwingManager = ToolsSwingLocator.getToolsSwingManager()
      model = toolsSwingManager.createFilteredListModel()
      actions = PluginsLocator.getActionInfoManager().getActions()
      
      for action in actions:
        #print action.getName(), action.getLabel()
        if action.getLabel()==None:
          label = action.getName()
        else: 
          label = "%s (%s)" %(i18n.getTranslation(action.getLabel()),action.getName())
        if label.startswith("_"):
          label = label.replace("_"," ").strip()
        labeled = LabeledValueImpl(label, action)
        model.addElement(labeled)
      model.setFilter(self.txtFilter.getText())
      model.sort(True)
      self.lstActions.setModel(model);
      self.lstActions.setSelectedIndex(indexAttributes);

def main(*args):
    l = ToolFinderPanel()
    l.showTool("_Tool_Finder")
    pass