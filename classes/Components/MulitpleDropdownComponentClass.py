from DropdownComponentClass import DropdownComponentClass
from Utils.ConfigManager import ConfigManager
import time

class MulitpleDropdownComponentClass(DropdownComponentClass):

    def __init__(self):
        DropdownComponentClass.__init__(self)
        self.configmanager = ConfigManager()


    def getSelection(self,h,index,parent="filterPopup",child="multiselect-dropdown"):
        activeDropDowns = self.getAllActiveElements(h[parent][child])
        activeDropDowns[index].click()
        selections = []

        for el in activeDropDowns[index].find_elements_by_class_name("menuitem"):
            for e in  el.find_elements_by_tag_name("input"):
                if str(e[0].get_attribute("checked")).upper() == "TRUE":
                    selections.append(el.text)

        return selections

    def domultipleSelection(self,h,value,index,parent="filterPopup",child="multiselect-dropdown"):
        activeDropDowns = self.getAllActiveElements(h[parent][child])
        activeDropDowns[index].click()
        for el in activeDropDowns[index].find_elements_by_class_name("menuitem"):
            if el.text == value:
                el.click()

        return self.getSelection(h,index)

    def getOptionsAvailable(self,h,index,parent="filterPopup",child="multiselect-dropdown"):
        activeDropDowns = self.getAllActiveElements(h[parent][child])
        return [el.text for el in activeDropDowns[index].find_elements_by_class_name("menuitem")]


    def doSearch(self,h,value,index,parent="filterPopup",child="multiselect-dropdown"):
        activeDropDowns = self.getAllActiveElements(h[parent][child])
        activeDropDowns[index].click()
        for el in activeDropDowns[index].find_elements_by_class_name("input"):
            if el.get_attribute("type") == "text":
                el.send_keys(value)
        return self.getOptionsAvailable(h,index)

