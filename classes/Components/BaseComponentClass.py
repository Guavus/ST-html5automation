# from classes.DriverHelpers.DriverHelper import DriverHelper
# from selenium import webdriver
# webdriver.Firefox().find_element_by_xpath().send_keys()
from Utils.UnitSystem import UnitSystem
from Utils.ConfigManager import ConfigManager
from selenium.common.exceptions import *
import time
from Utils.logger import *
from selenium.webdriver.common.keys import *

class BaseComponentClass:
    def click(self, elHandle):

        try:
            elHandle.click()
            return True
        except Exception:
            return Exception


    def send_keys(self, elHandle, value):
        return elHandle.send_keys(value)

    def customClick(self, elHandle):
        try:
            elHandle[len(elHandle)-1].click()
            time.sleep(2)
            return True
        except IndexError or Exception as e:
            elHandle.click()
            return e
        # return elHandle[len(elHandle)-1].click()
    def customSendkeys(self, elHandle, value):
        return elHandle[len(elHandle)-1].send_keys(value)
    def customText(self,elHandle):
        return elHandle[len(elHandle)-1].text


    def text(self,elHandle):
        return elHandle.text

    def getSelection(self):
        '''
        Base method for getSelection that can be used across all components for uniformity
        :return: Selection
        '''
        selection = []
        return selection

    def getSpecificLocators(self,locatorClass):
        '''
        Can be overridden at ComponentClass
        :param locatorClass: Locator Class of Component
        :return: component child as Key and its locators as Value
        '''
        return self.dictionary_ele_locators(locatorClass)

    def dictionary_ele_locators(self, locatorClass):
        dic = {}
        for method in dir(locatorClass):
            if type(getattr(locatorClass,method)) == tuple:
                dic[method]= getattr(locatorClass,method)
        return dic

    def validateToolTipData(self,dataCollection):
        result = {}
        return result

    def compare(self,v1,v2):
        if v1 == v2:
            return True
        else:
            return False

    def __init__(self):
        self.unitSystem = UnitSystem()
        self.configmanager = ConfigManager()


    def compHandlers(self,comp,handlers):
        return handlers[comp]
        # newHandlers = {}
        # for k,v in handlers.iteritems():
        #     if k in self.configmanager.componentChildRelations[comp]:
        #         newHandlers[k] = v
        # return newHandlers


    def selectDropDownByText(self,handler,text,text2="HAHA"):
        for ele in handler.find_elements_by_xpath(".//*"):
            if ele.text == text or ele.text == text2:
                ele.click()
                return ele.text

    def doSelection(self,h,parentLocator,measure):
        handlers = self.compHandlers('measureselectors',h)
        measureArr=measure.split("_")
        measureName=measureArr[0]
        downUpTotal=measureArr[1]
        absPerc=measureArr[2]
        self.setMeasureName(measureName,handlers['primaryMeasure'])
        self.select(handlers[downUpTotal])
        self.select(handlers[absPerc])
        try:
            avgPeak=measureArr[3]
            self.select(handlers[avgPeak])
        except:
            print "Got Measure without Peak/Average %s",measureName

    def getAllActiveElements(self, childHandles):
        activeElements = []
        for ele in childHandles:
            # 'disabled' not in ele.get_attribute("class") and
            if ele.is_displayed():
                activeElements.append(ele)
            else:
                pass
        return activeElements

    def clickCheckBox(self,h,index,parent="allcheckboxes",child="checkbox"):
        try:
            logger.debug("Going to Click Checkbox %d parent %s and child %s ",index,parent,child)
            h[parent][child][index].click()
            return True
        except Exception as e:
            logger.error("Exception found while clicking Checkbox %d",index)
            return e

    def sendkeys_input(self,value,h,index,clear=True,parent="allinputs",child="input"):
        try:
            if clear:
                logger.debug("Clearing the text at input %d parent %s and child %s ",index,parent,child)
                h[parent][child][index].send_keys(len(str(h[parent][child][index].get_attribute("value")))*Keys.BACKSPACE)
            logger.debug("Going to send keys to input %d parent %s and child %s ",index,parent,child)

            h[parent][child][index].send_keys(value)
            return h[parent][child][index].get_attribute("value")
        except Exception as e:
            logger.error("Exception found while entering keys to input %d",index)
            return e


    def selectRadioButton(self, value, h, childDiv="span", parent="radios", child="radio"):
        childs = ".//" + childDiv

        for el in h[parent][child]:
            if value == el.find_elements_by_xpath(childs)[0].text.strip().strip(':').strip():
                try:
                    el.click()
                    el.find_elements_by_xpath(".//input")[0].click()
                    time.sleep(2)
                    break
                except ElementNotVisibleException or ElementNotSelectableException or Exception as e:
                    return e



    def clickButton(self,value,h,parent="allbuttons",child="button"):
        for el in h[parent][child]:
            try:
                if value == el.text:
                    try:
                        el.click()
                        time.sleep(2)
                        return True
                        break
                    except ElementNotVisibleException or ElementNotSelectableException or Exception as e:
                        return e
            except Exception as e:
                return e

    def runtimeValue(self,prop,ele):
        if prop == "text":
            return ele.text
        elif prop == "title":
            return ele.get_attribute("title")
        elif prop == "value":
            return ele.get_attribute("style")
        elif prop == "style":
            return ele.get_attribute("style")
        elif prop == "class":
            return ele.get_attribute("class")
        elif prop == "id":
            return ele.get_attribute("id")


    def validateData(self,dataCollection,csvData):
        result = {}
        # for key,value in csvData.iteritems():
        for key in dataCollection['btvData']['dimension']:
            if "All " in key or "Others" in key:
                pass
            else:
                UIData = 0.0
                convertedData = float(dataCollection['btvData']['value'][dataCollection['btvData']['dimension'].index(key)].split(" ")[0])
                unitString = dataCollection['btvData']['value'][dataCollection['btvData']['dimension'].index(key)].split(" ")[1]
                UIData = self.unitSystem.getRawValue(convertedData,unitString)

                if csvData[key]['AGGR_totalByteBuffer'] == UIData:
                    result[key] = "Data Validation PASSED"
                else:
                    result[key] = "Data Validation FAILED --> Actual : "+str(UIData)+" and Expected : "+str(csvData[key]['AGGR_totalByteBuffer'])

        return result