from Utils.SetUp import *
from Utils.utility import *
from classes.Components.MulitpleDropdownComponentClass import *
try:
    setup = SetUp()
    multiDropDownInstance=MulitpleDropdownComponentClass()

    selection=multiDropDownInstance.domultipleSelectionWithIndex_MRX(getHandle(setup,"Dummy_Screen"),['1','2'],0,parent="Dummy_Multi",child="multiselect-dropdown",setup=False)

    selection1=multiDropDownInstance.getSelection_MRX(getHandle(setup,"Dummy_Screen"),0,parent="Dummy_Multi", child="multiselect-dropdown")
    multiDropDownInstance.setEqualOrNotEqualIcon(getHandle(setup,"Dummy_Screen"), ['E'], 0, parent="Dummy_Multi", child="multiselect-dropdown", setup=False,E_NE_index=0)
    toggle=multiDropDownInstance.getToggleStateInMultiDropDown(getHandle(setup,"Dummy_Screen"),0,parent="Dummy_Multi", child="multiselect-dropdown",setup=False,E_NE_index=0)
    search_Result=multiDropDownInstance.doSearch(getHandle(setup,"Dummy_Screen"),'a',0,parent="Dummy_Multi",child="multiselect-dropdown")

except Exception as e:
    r = "issue_" + str(random.randint(0, 9999999)) + ".png"
    setup.d.save_screenshot(r)
    logger.debug("Got Exception from Script Level try catch :: Screenshot with name = %s is saved", r)
    logger.debug("Got Exception from Script Level try catch :: Screenshot with name = %s is saved", r)
    setup.d.close()
