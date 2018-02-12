from MuralUtils.ContentHelper import *
from MRXUtils import MRX_UMHelper
from classes.Pages.MuralScreens.UserMangementScreen import *
from classes.Pages.ExplorePageClass import *
from MRXUtils.MRXConstants import *
try:
    setup = SetUp()
    login(setup,Constants.USERNAME,Constants.PASSWORD)
    isError(setup)
    wfstart = WorkflowStartComponentClass()
    exploreScreenInstance = ExplorePageClass(setup.d)
    userScreenInstance=UserManagementScreenClass(setup.d)
    isError(setup)
    handleForHeader = getHandle(setup, Constants.VALIDATE_HEADER, 'leftHeader')
    UMHeader = str(handleForHeader['leftHeader']['project_Name'][0].text).strip()
    checkEqualAssert(MRXConstants.UMHeader, UMHeader, message="User management screen should be open in new tab",testcase_id="MKR-3475")

    tableHandle = getHandle(setup, MRXConstants.MRXUMSCREEN, 'table')
    actualHeader=userScreenInstance.table.getIterfaceHeaders(tableHandle['table'])
    checkEqualAssert(MRXConstants.UMScreenTableHeaderList,actualHeader,message="Verify table header on UM Screen",testcase_id="MKR-3479,MKR-3478")
    newUserLabel=userScreenInstance.getScreenNameFromUI(getHandle(setup,MRXConstants.MRXUMSCREEN,'alllabels'))
    checkEqualAssert(MRXConstants.NewUser,newUserLabel,message="Verify New User label on UM",testcase_id="MKR-3478")
    usersDetails=setup.cM.getNodeElements("userdetail","user")
    checkAllFieldsFlagForAddUser=True
    checkComplusoryFieldFlag=True

    for k, usersDetail in usersDetails.iteritems():
        wfstart.clickImage('icon', getHandle(setup, MRXConstants.MRXUMSCREEN,'newUserIcon'),parent='newUserIcon',child='icon')
        if checkAllFieldsFlagForAddUser:
            actualFieldsOnAddUserPopup=userScreenInstance.getAllTitle(getHandle(setup,MRXConstants.MRXUMPOPUP,'alllabels'),parent='alllabels',child='label')
            actualFieldsOnAddUserPopup.pop()
            checkEqualAssert(MRXConstants.ExpectedOptionForNewUser,actualFieldsOnAddUserPopup,message='Verify that parameters in the new user dialog box',testcase_id='MKR-3480')
            checkAllFieldsFlagForAddUser=False
        try:
            if checkComplusoryFieldFlag:
                MRX_UMHelper.setUserDetail(setup, userScreenInstance, MRXConstants.MRXUMPOPUP, usersDetail,button=usersDetail['button'],checkComplusoryFieldFlag=checkComplusoryFieldFlag)
                wfstart.clickImage('icon', getHandle(setup, MRXConstants.MRXUMSCREEN, 'newUserIcon'),parent='newUserIcon', child='icon')
                checkComplusoryFieldFlag=False
            userDetailFromUIPopup=MRX_UMHelper.setUserDetail(setup,userScreenInstance,MRXConstants.MRXUMPOPUP,usersDetail,button=usersDetail['button'])
        except Exception as e:
            r = "issue_" + str(random.randint(0, 9999999)) + ".png"
            setup.d.save_screenshot(r)
            logger.error("Got Exception because of invalid entry for New User:: Screenshot with name = %s is saved :: User Details= %s and ERROR: %s", r,str(usersDetail),str(e))
            resultlogger.error("Got Exception because of invalid entry for New User:: Screenshot with name = %s is saved :: User Details= %s <br>",r,str(usersDetail))
            userScreenInstance.clickIcon(getHandle(setup, MRXConstants.MRXUMPOPUP,'icons'),setup.d)
            continue

        tableHandle = getHandle(setup, MRXConstants.MRXUMSCREEN,'table')
        tableMap = userScreenInstance.table.getTableDataMap(tableHandle, driver=setup,colIndex=1)

        if usersDetail['button']=='Create' and len(userDetailFromUIPopup)>0:
            checkEqualAssert(True,tableMap['rows'].has_key(usersDetail['username']),message="Verify User added Successfully ")
            tableMap['rows'][usersDetail['username']].pop()
            tableMap['rows'][usersDetail['username']].pop()
            checkEqualAssert(userDetailFromUIPopup,tableMap['rows'][usersDetail['username']],message="Verify that admin can create a new user from the user management screen (Functional)",testcase_id="MKR-3483")

        elif usersDetail['button']=='Create' and len(userDetailFromUIPopup)==0:
            checkEqualAssert(True, tableMap['rows'].has_key(usersDetail['username']),message="User aleady exist in table hence not allow to add again")

        elif usersDetail['button']=='Cancel' or usersDetail['button']=='Cross':
            checkEqualAssert(False, tableMap['rows'].has_key(usersDetail['username']),message="Verify that cancel and X button should working fine in the new user dialog box",testcase_id="MKR-3482")


    # Verify basic table functionality (sorting)

    logger.debug("Verify Basic Table functionality")
    MRX_UMHelper.verifySortingOnTable(setup,userScreenInstance,MRXConstants.MRXUMSCREEN)

    usersDetailsNegativeScenario = setup.cM.getNodeElements("userdetail_NegativeScenario", "user")
    for k, usersDetail in usersDetailsNegativeScenario.iteritems():
        wfstart.clickImage('icon', getHandle(setup, MRXConstants.MRXUMSCREEN, 'newUserIcon'),parent='newUserIcon', child='icon')
        try:
            userDetailFromUIPopup = MRX_UMHelper.setUserDetail(setup, userScreenInstance,MRXConstants.MRXUMPOPUP, usersDetail,button=usersDetail['button'])
            if "incorrectpassword" in k:
                checkEqualAssert(False,True,message="Incorrect Password not allowed :: Enterd Password = " + str(usersDetail['password']), testcase_id="MKR-3493")
        except:
            r = "issue_" + str(random.randint(0, 9999999)) + ".png"
            setup.d.save_screenshot(r)
            logger.debug("Got Exception because of invalid entry for New User:: Screenshot with name = %s is saved", r)
            resultlogger.debug("Got Exception because of invalid entry for New User:: Screenshot with name = %s is saved <br>", r)
            userScreenInstance.clickIcon(getHandle(setup, MRXConstants.MRXUMPOPUP, 'icons'), setup.d)
            if "incorrectpassword" in k:
                checkEqualAssert(False,False,message="Incorrect Password not allowed :: Enterd Password = " + str(usersDetail['password']), testcase_id="MKR-3493")
            continue

        tableHandle = getHandle(setup, MRXConstants.MRXUMSCREEN, 'table')
        tableMap = userScreenInstance.table.getTableDataMap(tableHandle, driver=setup, colIndex=1)
        if usersDetail['button']=='Create' and len(userDetailFromUIPopup)==0:
            checkEqualAssert(True, tableMap['rows'].has_key(usersDetail['username']),message="User aleady exist in table hence not allow to add again")
        else:
            checkEqualAssert(False, tableMap['rows'].has_key(usersDetail['username']),message="New user having invalid entry should not be added")

    setup.d.close()
    setup.d.switch_to.window(setup.d.window_handles[0])
    setup.d.close()

    import MRX.Validate_NewUserloging
    import MRX.VisibleSegment_ForAdminAndSegmentManager
    import MRX.EditUser_MRX_UM
    import MRX.ChangePassword
    import MRX.ChangePassword_NegativeScenario


except Exception as e:
    isError(setup)
    r = "issue_" + str(random.randint(0, 9999999)) + ".png"
    setup.d.save_screenshot(r)
    logger.debug("Got Exception from Script Level try catch :: Screenshot with name = %s is saved", r)
    setup.d.close()


# PrivilegesFromTable=tableMap['rows'][usersDetail['username']].pop(4)
# listOfPrivilegesFromTable=PrivilegesFromTable.split(',')
# # neglecting User Management and System Monitoring from list of privileges in case of Admin
# if usersDetail['userrole']=='Admin':
#     listOfPrivileges.remove('User Management')
#     listOfPrivileges.remove('System Monitoring')
#
#
# for Privilege in listOfPrivileges:
#     listOfPrivilegesFromTable.remove(Privilege)
# checkEqualAssert(0, len(listOfPrivilegesFromTable), '', '', 'Verify Privileges From Table')
