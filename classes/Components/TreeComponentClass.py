# coding=utf-8
from BaseComponentClass import BaseComponentClass
from Utils.ConfigManager import ConfigManager
import time
from Utils.logger import *
from selenium.webdriver.common.keys import *
from selenium.webdriver import ActionChains
from MRXUtils.MRXConstants import *
import random
from copy import deepcopy

TreeElementDict = {}

class TreeComponentClass(BaseComponentClass):

    def __init__(self,driver):
        '''
        Constructor
        '''
        self.driver = driver
        self.utility = __import__("Utils.utility")
        BaseComponentClass.__init__(self)
        self.configmanager = ConfigManager()


    def expandTree(self,setup,treeHandle,parent='alltrees',child='tree',index=0):
        logger.info('Going to expand Tree')
        global TreeElementDict
        TreeElementDict = {}
        self.expandTree1(setup,treeHandle[parent][child][index])
        return TreeElementDict


    def expandTree1(self,setup,treeElementHandle,count=0):
        tree_nodes=treeElementHandle.find_elements_by_tag_name('tree-node')
        for ele in tree_nodes:
            self.set_attribute(setup, ele.find_element_by_tag_name('tree-node-content'), property='tree-level',value=count)
            path=self.set_PathOnTree(ele)
            if str(count) in TreeElementDict.keys():
                TreeElementDict[str(count)].append([str(ele.text), path.replace('\n', '/')])
            else:
                TreeElementDict[str(count)]=[]
                TreeElementDict[str(count)].append([str(ele.text), path.replace('\n', '/')])

        if len(tree_nodes)>5:
            nodeIndexList=random.sample(range(len(tree_nodes)),MRXConstants.NumberOfElementToBeExpandOnAtAnyLevel)
            nodeIndexList.sort()
            treenodes = [tree_nodes[index] for index in range(len(nodeIndexList))]
        else:
            treenodes = tree_nodes

        for ele in treenodes:
            if 'leaf' in ele.find_elements_by_xpath('.//*')[1].get_attribute('class'):
                continue
            else:
                count_1 = count
                ele.find_elements_by_class_name('toggle-children')[0].click()
                time.sleep(1)
                self.expandTree1(setup,ele,count_1+1)


    def doSelectionOnTree_Random(self, setup, elementDict, treeHandle, parent='alltrees', child='tree', index=0):
        elementToBeSelect={}
        for k in elementDict.keys():
            if len(elementDict[k])>MRXConstants.NumberOfSelectionOnAtAnyLevel:
                l=[elementDict[k][random.randrange(len(elementDict[k]))] for item in range(MRXConstants.NumberOfSelectionOnAtAnyLevel)]
                elementToBeSelect[k]=list(set(l))
            else:
                elementToBeSelect[k]=elementDict[k]

        expectedTextFormUIForSelectedTree=[]

        expected={}
        for k in elementToBeSelect.keys():
            expected[k]=self.selectTree(setup,treeHandle,elementToBeSelect[k],key=k,index=index)

        keysList=expected.keys()  ### for verify level 1>2>3...###
        keysList.sort()
        for k in keysList:
            expectedTextFormUIForSelectedTree+=expected[k]

        return expectedTextFormUIForSelectedTree,elementToBeSelect,self.getSelectionFromExpendedTree(treeHandle,index=index)


    def getSelectionFromExpendedTree(self,treeHandle,parent='alltrees',child='tree',index=0):
        selectedElements = {}
        for ele in treeHandle[parent][child][index].find_elements_by_tag_name('tree-node-content'):
            #key = str(ele.find_elements_by_xpath('../../../div')[0].get_attribute('class').split(' ')[1]).strip()
            key = str(ele.get_attribute('tree-level'))
            if not key in selectedElements.keys():
                selectedElements[key] = []

        for ele in treeHandle[parent][child][index].find_elements_by_tag_name('tree-node-content'):
            if 'active' in ele.find_elements_by_xpath('../../../../div')[0].get_attribute('class'):
                #selectedElements[str(ele.find_elements_by_xpath('../../../div')[0].get_attribute('class').split(' ')[1]).strip()].append(str(ele.text).strip())
                selectedElements[str(ele.get_attribute('tree-level'))].append(str(ele.text).strip())
        return selectedElements


    def selectTree(self,setup,treeHandle,listForSelection,parent='alltrees',child='tree',key='',index=0):
        List = []
        listForSelectionCopy=deepcopy(listForSelection)
        TreeElementListCopy=[]
        if key in TreeElementDict.keys():
            TreeElementListCopy = deepcopy(TreeElementDict[str(key)])

        for ele in treeHandle[parent][child][index].find_elements_by_tag_name('tree-node-content'):
            try:
                for element in listForSelectionCopy:
                    if str(ele.text).strip()==str(element).strip() and str(ele.get_attribute('tree-level')) == str(key):
                        try:
                            logger.info('Going to select %s on tree',str(ele.text))
                            ActionChains(setup.d).key_down(Keys.SHIFT).perform()
                            ele.click()
                            for node in TreeElementListCopy:
                                if node[0]==str(ele.text).strip():
                                    List+=[node[1]]
                                    TreeElementListCopy.remove(node)
                                    break

                            ActionChains(setup.d).key_down(Keys.SHIFT).perform()
                            listForSelectionCopy.remove(element)
                            break
                        except Exception as e:
                            logger.error('Got exception during selection on Tree:: Exception = %s',str(e))
            except:
                pass
        return List


    def seprateElementOfTreeByLevel(self,treeHandle,parent='alltrees',child='tree',index=0):
        classname = []
        element_list = []
        for ele in treeHandle[parent][child][index].find_elements_by_tag_name('tree-node-content'):
            try:
                element_list.append(str(ele.text).strip())
                #classname.append(str(ele.find_elements_by_xpath('../../../div')[0].get_attribute('class').split(' ')[1]).strip())
                classname.append(ele.get_attribute('tree-level'))
            except:
                # uncode char handling
                pass

        level_Dict = {}
        for level in classname:
            if not level in level_Dict.keys():
                level_Dict[level] = []

        for i in range(len(element_list)):
            level_Dict[classname[i]].append(element_list[i])
        return level_Dict

