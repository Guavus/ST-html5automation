from MuralUtils.ContentHelper import *
from MRXUtils import MRX_UMHelper
from classes.Pages.MuralScreens.UserMangementScreen import *
from classes.Pages.ExplorePageClass import *
from MRXUtils.MRXConstants import *


try:
    setup = SetUp()
    login(setup, Constants.USERNAME, Constants.PASSWORD)
    wfstart = WorkflowStartComponentClass()
    exploreScreenInstance = ExplorePageClass(setup.d)
    exploreHandle = getHandle(setup, "explore_Screen")
    exploreScreenInstance.exploreList.switchApp(exploreHandle)
    userScreenInstance = UserManagementScreenClass(setup.d)
    result = exploreScreenInstance.exploreList.launchapp(getHandle(setup, "explore_Screen"), 1)
    isError(setup)
    setup.d.switch_to.window(setup.d.window_handles[1])

    usersDetails = setup.cM.getNodeElements("userdetail", "edituser")

    for k, usersDetail in usersDetails.iteritems():

        ##################################### Validating Search ########################################################

        h = getHandle(setup,MRXConstants.MRXUMSCREEN,'allinputs')
        checkEqualAssert(True,len(h['allinputs']['input'])>0,message="Verify presence of Search Box",testcase_id="MKR-3478")
        userScreenInstance.cm.sendkeys_input(usersDetail['username'], h, 0)

        tableHandle = getHandle(setup,MRXConstants.MRXUMSCREEN, 'table')
        data2 = userScreenInstance.table.getTableData1(tableHandle)

        searchFlag,searchList=validateSearchForTable(data2,usersDetail['username'],columnIndex=1)
        checkEqualAssert(True,searchFlag,message="Verify Searching for username= "+str(usersDetail['username'])+" Search Result= "+str(searchList),testcase_id="MKR-3490")

        ################################################################################################################

        index=userScreenInstance.table.getRowIndexFromTable(1,tableHandle,usersDetail['username'])
        userDetailFromTable=[]
        for value in data2['rows'][index]:
            userDetailFromTable.append(value)

        logger.debug("Going to Click Edit Button for user =%s",usersDetail['username'])
        resultlogger.debug("Going to Click Edit Button for user =%s",usersDetail['username'])

        ############################### Click on Edit icon #############################################################
        try:
            userScreenInstance.table.clickIconOnTable(tableHandle, setup.d, index=index)
        except Exception as e:
            logger.debug("Not able to click on edit for user = %s ", usersDetail['username'])
            resultlogger.debug("Not able to click on edit for user = %s ", usersDetail['username'])
            continue

        ################################################################################################################

        userDetailFromUIPopup=MRX_UMHelper.getUserDetailFromUI(setup,userScreenInstance,MRXConstants.MRXUMPOPUP)
        userDetailFromTable.pop()
        userDetailFromTable.pop()
        checkEqualAssert(userDetailFromTable,userDetailFromUIPopup,message="Verify User detail on edit popup from table",testcase_id="MKR-3484")
        try:
            updatedUserDetailFromUIPopup = MRX_UMHelper.editUserDetail(setup, userScreenInstance,MRXConstants.MRXUMPOPUP,usersDetail,button=usersDetail['button'])
        except:
            r = "issue_" + str(random.randint(0, 9999999)) + ".png"
            setup.d.save_screenshot(r)
            logger.debug("Got Exception because of invalid entry for New User:: Screenshot with name = %s is saved", r)
            resultlogger.debug("Got Exception because of invalid entry for New User:: Screenshot with name = %s is saved <br>", r)
            userScreenInstance.clickIcon(getHandle(setup, MRXConstants.MRXUMPOPUP,'icons'),setup.d)
            continue

        ############################### Verify Detail After Edit #######################################################

        tableHandle = getHandle(setup, MRXConstants.MRXUMSCREEN, 'table')
        data2 = userScreenInstance.table.getTableData1(tableHandle)

        index = userScreenInstance.table.getRowIndexFromTable(1, tableHandle, usersDetail['username'])
        updatedUserDetailFromTable = []
        if index != -1:
            for value in data2['rows'][index]:
                updatedUserDetailFromTable.append(value)

        updatedUserDetailFromTable.pop()
        updatedUserDetailFromTable.pop()

        if len(updatedUserDetailFromUIPopup) == 0:
            checkEqualAssert(userDetailFromTable,updatedUserDetailFromTable,message="Verify that if we click on Cancel button than User's Detail remains same",testcase_id=' MKR-3488')

        else:
            checkEqualAssert(updatedUserDetailFromUIPopup,updatedUserDetailFromTable,message="Verify Updated User's Detail From table",testcase_id="MKR-3487")

    setup.d.close()
    setup.d.switch_to.window(setup.d.window_handles[0])
    setup.d.close()

except Exception as e:
    isError(setup)
    r = "issue_" + str(random.randint(0, 9999999)) + ".png"
    setup.d.save_screenshot(r)
    logger.debug("Got Exception from Script Level try catch :: Screenshot with name = %s is saved", r)
    setup.d.close()