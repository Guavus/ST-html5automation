from Utils.SetUp import *
from Utils.utility import *
from classes.Components.MulitpleDropdownComponentClass import *
'''
This script cover testing of below method
1. Set Multiple Selection on DropDown
2. Get Selection from DropDown
3. Set toggle button
4. Get state of toggle button
5. Get search result from drop down
'''
try:
    setup = SetUp()
    multiDropDownInstance=MulitpleDropdownComponentClass()

    selection=multiDropDownInstance.domultipleSelectionWithIndex_MRX(getHandle(setup,Constants.DUMMY_SCREEN),['1','2'],0,parent="Dummy_Multi",child="multiselect-dropdown",setup=False)
    selection1=multiDropDownInstance.getSelection_MRX(getHandle(setup,Constants.DUMMY_SCREEN),0,parent="Dummy_Multi", child="multiselect-dropdown")

    multiDropDownInstance.setEqualOrNotEqualIcon(getHandle(setup,Constants.DUMMY_SCREEN), ['E'], 0, parent="Dummy_Multi", child="multiselect-dropdown", setup=False,E_NE_index=0)
    toggle=multiDropDownInstance.getToggleStateInMultiDropDown(getHandle(setup,Constants.DUMMY_SCREEN),0,parent="Dummy_Multi", child="multiselect-dropdown",setup=False,E_NE_index=0)

    search_Result=multiDropDownInstance.doSearch(getHandle(setup,Constants.DUMMY_SCREEN),'a',0,parent="Dummy_Multi",child="multiselect-dropdown")

except Exception as e:
    r = "issue_" + str(random.randint(0, 9999999)) + ".png"
    setup.d.save_screenshot(r)
    logger.debug("Got Exception from Script Level try catch :: Screenshot with name = %s is saved", r)
    logger.debug("Got Exception from Script Level try catch :: Screenshot with name = %s is saved", r)
    setup.d.close()
