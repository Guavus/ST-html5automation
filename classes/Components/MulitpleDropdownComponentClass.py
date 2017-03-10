from DropdownComponentClass import DropdownComponentClass
from Utils.ConfigManager import ConfigManager
import time
from Utils.logger import *

class MulitpleDropdownComponentClass(DropdownComponentClass):

    def __init__(self):
        DropdownComponentClass.__init__(self)
        self.configmanager = ConfigManager()


    def getSelection(self,h,index,parent="filterPopup",child="multiselect-dropdown"):
        activeDropDowns = self.getAllActiveElements(h[parent][child])
        time.sleep(1)
        activeDropDowns[index].click()
        selections = []

        # for el in activeDropDowns[index].find_elements_by_class_name("menuitem"):
        #     for e in  el.find_elements_by_tag_name("input"):
        #         if str(e[0].get_attribute("checked")).upper() == "TRUE" or str(e[0].get_attribute("ng-reflect-checked")).upper() == "TRUE":
        #             selections.append(el.text)
        try:
            for e in activeDropDowns[index].find_elements_by_css_selector('[ng-reflect-model="true"],[ng-reflect-checked="true"]'):

                # commenting below lines to get all selected values in dropdown
                if e.find_elements_by_xpath("..//div")[0].text.strip() == "Select All":
                    selections.append("ALL")
                    activeDropDowns[index].click()
                    return selections

                selections.append(e.find_elements_by_xpath("..//div")[0].text)
        except Exception as e:
            try:
                for e in activeDropDowns[index].find_elements_by_css_selector('[ng-reflect-model="true"],[checked="true"]'):
                    if e.find_elements_by_xpath("..//div")[0].text.strip() == "Select All":
                        selections.append("ALL")
                        activeDropDowns[index].click()
                        return selections
                    selections.append(e.find_elements_by_xpath("..//div")[0].text)
            except Exception as e:
                logger.error("Exception %s found while getting current selection, Component: MulitpleDropdownComponentClass",e)


        activeDropDowns[index].click()
        time.sleep(1)
        return selections

    def getSelectionWithIndex(self,h,index,parent="filterPopup",child="multiselect-dropdown"):
        activeDropDowns = self.getAllActiveElements(h[parent][child])
        activeDropDowns[index].click()
        selections = []

        # for el in activeDropDowns[index].find_elements_by_class_name("menuitem"):
        #     for e in  el.find_elements_by_tag_name("input"):
        #         if str(e[0].get_attribute("checked")).upper() == "TRUE" or str(e[0].get_attribute("ng-reflect-checked")).upper() == "TRUE":
        #             selections.append(el.text)
        try:

            for e in activeDropDowns[index].find_elements_by_css_selector('[ng-reflect-checked="true"]'):
                selections.append(e.find_elements_by_xpath("..//div")[0].text)
        except Exception as e:
            try:
                for e in activeDropDowns[index].find_elements_by_css_selector('[checked="true"]'):
                    selections.append(e.find_elements_by_xpath("..//div")[0].text)
            except Exception as e:
                logger.error("Exception %s found while getting current selection, Component: MulitpleDropdownComponentClass",e)



        return selections


    def domultipleSelection(self,h,value,index,parent="filterPopup",child="multiselect-dropdown"):
        activeDropDowns = self.getAllActiveElements(h[parent][child])
        activeDropDowns[index].click()
        time.sleep(2)
        for el in activeDropDowns[index].find_elements_by_class_name("menuitem"):
            if el.text == value:
                el.click()
        activeDropDowns[index].click()
        return self.getSelection(h,index)

    def domultipleSelectionWithIndex(self,h,value,index,parent="filterPopup",child="multiselect-dropdown"):
        activeDropDowns = self.getAllActiveElements(h[parent][child])
        activeDropDowns[index].click()
        time.sleep(2)
        elements = activeDropDowns[index].find_elements_by_css_selector('input[type="checkbox"]')
        for i in range(len(elements)):
            if i in value or str(i) in value:
                elements[i].click()

        activeDropDowns[index].click()
        return self.getSelection(h,index,parent,child)

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

    def getHeader(self,h,index,parent="picker",child="multiselect-dropdown"):
        return h[parent][child][index].find_elements_by_css_selector("[class*=PickerHeaderClass]")[0].text.strip().strip('\n').strip()


    def domultipleSelectionWithName(self,h,value,index,parent="filterPopup",child="multiselect-dropdown"):
        activeDropDowns = h[parent][child]
        activeDropDowns[index].click()
        time.sleep(2)

        for el in activeDropDowns[index].find_elements_by_class_name("menuitemDiv"):
            if str(el.text).strip() == value:
                el.click()
                return str(activeDropDowns[index].find_elements_by_xpath("./div/*")[0].text)


