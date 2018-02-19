from MuralUtils.ContentHelper import *
from MRXUtils import MRX_UMHelper
from classes.Pages.MuralScreens.RoleManagementScreen import *
from classes.Pages.ExplorePageClass import *
#from MRXUtils.MRXConstants import *
from Utils.UMConstants import *
from classes.Pages.MuralScreens.UserMangementScreen import UserManagementScreenClass

try:
    setup = SetUp()
    login(setup,Constants.USERNAME,Constants.PASSWORD)
    isError(setup)
    wfstart = WorkflowStartComponentClass()
    userScreenInstance = UserManagementScreenClass(setup.d)
    handle = getHandle(setup, "explore_Screen","alllabels")
    roleScreenInstance=RoleManagementScreenClass(setup.d)
    roleScreenInstance.click(handle['alllabels']['label'][1])



    ################### Verify New Role label on UM Role Management screen
    tableHandle = getHandle(setup, UMConstants.UMSCREEN_MANAGEROLES, 'table')
    actualHeader=roleScreenInstance.table.getIterfaceHeaders(tableHandle['table'])
    checkEqualAssert(UMConstants.UMScreenTableHeaderList_ManageRoles,actualHeader,message="Verify table header on UM Screen for Manage roles",testcase_id="Reflex-UM-188")
    newRoleLabel=roleScreenInstance.getScreenNameFromUI(getHandle(setup,UMConstants.UMSCREEN_MANAGEROLES,'alllabels'))
    checkEqualAssert(UMConstants.NewRole,newRoleLabel,message="Verify New Role label on UM Role Management screen",testcase_id="Reflex-UM-189")




    ############# Verify that table on manage roles screen can be sorted on columns rolename and default privileges
    MRX_UMHelper.verifySortingOnTable(setup, roleScreenInstance, screenName=UMConstants.UMSCREEN_MANAGEROLES, parent='table', sortTableColumnTag='rolesorttablecolumn',sortTableColumnInnerTag='column',testcase_id="Reflex-UM-181")




    ################# Verify the requiredFields label , help/close icon, field options ,roleAlredayExists label , create role, edit role delete role opertaions
    rolesDetailsDict=setup.cM.getNodeElements("roleDetails","role")
    rolesDetailsDictOnlyRoles = dict((k, roleDetail) for k, roleDetail in rolesDetailsDict.iteritems() if 'role' in k)
    checkRequiredFieldsTextFlag = True
    checkHelpCloseIconFlag = True
    checkRoleAlreadyExistsFlag = True
    editRoleFlag = True
    deleteRoleFlag = True
    createUserWithNewRoleCreatedFlag = True
    loginWithNewUserNewRole = True

    for k, roleDetail in rolesDetailsDictOnlyRoles.iteritems():
        tableHandle = getHandle(setup, UMConstants.UMSCREEN_MANAGEROLES, 'table')
        tableData_beforeCreateRole = roleScreenInstance.table.getTableData1(tableHandle)
        handle = getHandle(setup, UMConstants.UMSCREEN_MANAGEROLES, 'newRoleIcon')
        MRX_UMHelper.clickOnPopupIcon(setup, h=handle, screen=UMConstants.UMSCREEN_MANAGEROLES,parent='newRoleIcon', child='icon')





        ### Verify the required Fields label
        if checkRequiredFieldsTextFlag:
            handle = getHandle(setup, UMConstants.UMPOPUP_ADDROLE, 'content')
            reqiredLabelFromUI = ""
            if len(handle['content']['requiredFieldLabel']) > 0:
                reqiredLabelFromUI = str(handle['content']['requiredFieldLabel'][0].text)
            else:
                logger.debug("Required fields label could not be fetched from UI")
            checkEqualAssert(UMConstants.RequiredFieldsLabel, reqiredLabelFromUI,message="Verify requiredFields label on UM add role popup", testcase_id="Reflex-UM-154")
            checkRequiredFieldsTextFlag = False





        ### Verify field options given in add role popup
        fieldsOnAddRolePopup=roleScreenInstance.getAllTitle(getHandle(setup,UMConstants.UMPOPUP_ADDROLE,'alllabels'),parent='alllabels',child='label')
        actualFieldsOnAddRolePopup = fieldsOnAddRolePopup[:2]
        checkEqualAssert(UMConstants.ExpectedOptionForNewRole,actualFieldsOnAddRolePopup[:2],message='Verify the field options given in the new role dialog box',testcase_id='Reflex-UM-193')




        ### Verify Creating a new role
        expectedRoleName, expectedCheckedCheckBoxesList, createBtnStatus = MRX_UMHelper.setRoleDetails(roleScreenInstance, setup, str(k),screen=UMConstants.UMPOPUP_ADDROLE,values=roleDetail)
        roleNameFromUI, checkedCheckBoxesListFromUI = MRX_UMHelper.getRoleDetails(screenInstance=roleScreenInstance, setup=setup,screen=UMConstants.UMPOPUP_ADDROLE)
        checkEqualAssert(expectedRoleName, roleNameFromUI, message="Verify Entered Role Name",testcase_id='Reflex-UM-194')
        checkEqualAssert(expectedCheckedCheckBoxesList, checkedCheckBoxesListFromUI, message="Verify Selected privileges",testcase_id='Reflex-UM-194')
        if tableData_beforeCreateRole['rows'] != Constants.NODATA:
            numberOfRows_beforeCreateRole = len(tableData_beforeCreateRole['rows'])
        else:
            numberOfRows_beforeCreateRole = 0
        expected_RoleEntry_forTable = [expectedRoleName] + expectedCheckedCheckBoxesList + ['', '']
        handle = getHandle(setup, UMConstants.UMPOPUP_ADDROLE, 'allbuttons')
        if createBtnStatus:
            logger.debug("Going to click on 'Create' buttton on add role popup ")
            roleScreenInstance.hoverAndClickButton(setup, "Create", handle)
        else:
            logger.debug(" 'Create' button on add role popup is not enabled. Hence exiting from popup screen through Cancel' button ")
            roleScreenInstance.hoverAndClickButton(setup, "Cancel", handle)
        logger.debug("Getting table handle after Creating a new role")
        tableHandle = getHandle(setup, UMConstants.UMSCREEN_MANAGEROLES, 'table')
        tableData_afterCreateRole = roleScreenInstance.table.getTableData1(tableHandle)
        if tableData_afterCreateRole['rows'] != Constants.NODATA:
            numberOfRows_afterCreateRole = len(tableData_afterCreateRole['rows'])
            roleEntry_forTableFromUI = []
            rolenameFoundFlag = False
            for row in tableData_afterCreateRole['rows']:
                if str(row[0]) == expectedRoleName:
                    logger.debug("Rolename for newly created role found in the first column of the table")
                    roleEntry_forTableFromUI = [str(row[0])] + row[1].replace(', ',',').split(',') + [row[2]] + [row[3]]
                    rolenameFoundFlag = True
                    break
            if not rolenameFoundFlag:
                logger.debug("Rolename for newly created role not found in the first column of the table")
        else:
            numberOfRows_afterCreateRole = 0
            roleEntry_forTableFromUI = []
        checkEqualAssert(sorted(expected_RoleEntry_forTable),sorted(roleEntry_forTableFromUI),message="Verify a row for newly created role is successfully inserted in manage roles table",testcase_id='Reflex-UM-1')
        checkEqualAssert(numberOfRows_beforeCreateRole+1, numberOfRows_afterCreateRole,message="Verify the count of rows after insertion of a new role in manage roles table",testcase_id='Reflex-UM-1')




        '''
        ### Verify a user can be assigned a new role
        if createUserWithNewRoleCreatedFlag:
            handle = getHandle(setup, "explore_Screen", "alllabels")
            roleScreenInstance = RoleManagementScreenClass(setup.d)
            roleScreenInstance.click(handle['alllabels']['label'][0])
            usersDetails = setup.cM.getNodeElements("userdetail", "user")
            usersDetail = usersDetails['kriti']
            userDetailFromUIPopup = MRX_UMHelper.setUserDetail(setup, userScreenInstance, UMConstants.UMPOPUP_ADDUSER,usersDetail, button=usersDetail['button'])
            createUserWithNewRoleCreatedFlag = False


            ### Verify that user created with a new role is able to login
            if loginWithNewUserNewRole:
                handle = getHandle(setup, "explore_Screen", "alllinks")['alllinks']['a'][0]
                roleScreenInstance.click(handle)
                handle = getHandle(setup, "explore_Screen", "alllinks")['alllinks']['a'][2]
                roleScreenInstance.click(handle)
                username = "cmatheiu"
                password = "a"
                # username = usersDetails['kriti']['autokriti']
                # password = usersDetails['kriti']['password']
                login(setup,username,password)
                loginWithNewUserNewRole = False

        '''



        ###  Verfiy another role cannot be created with same  role name
        if checkRoleAlreadyExistsFlag:
            handle = getHandle(setup, UMConstants.UMSCREEN_MANAGEROLES, 'newRoleIcon')
            MRX_UMHelper.clickOnPopupIcon(setup, h=handle, screen=UMConstants.UMSCREEN_MANAGEROLES, parent='newRoleIcon',child='icon')
            logger.debug("Setting an existing rolename and privileges on add role popup")
            expectedRoleName, expectedCheckedCheckBoxesList, createBtnStatus = MRX_UMHelper.setRoleDetails(roleScreenInstance,setup, str(k),screen=UMConstants.UMPOPUP_ADDROLE,values=roleDetail)
            handle = getHandle(setup, UMConstants.UMPOPUP_ADDROLE, 'allbuttons')
            logger.debug("Going to click on 'Create' buttton on add role popup ")
            roleScreenInstance.hoverAndClickButton(setup, "Create", handle)
            logger.debug("Fetching Role already exists label from add role popup ")
            handle = getHandle(setup, UMConstants.UMPOPUP_ADDROLE, 'errorMsgRolePopup')
            roleExistsLabelFromUI = ""
            if len(handle['errorMsgRolePopup']['errorMsg']) > 0:
                roleExistsLabelFromUI = str(handle['errorMsgRolePopup']['errorMsg'][0].text)
            else:
                logger.debug("Role already exists label cound not be fetched from UI")
            checkEqualAssert(UMConstants.RoleExistsLabel,roleExistsLabelFromUI, message = "Verify that admin user can not create role with a role name that already exists.",testcase_id='Reflex-UM-184')
            logger.debug("Exiting from popup screen through Cancel' button ")
            handle = getHandle(setup, UMConstants.UMPOPUP_ADDROLE, 'allbuttons')
            roleScreenInstance.hoverAndClickButton(setup, "Cancel", handle)
            checkRoleAlreadyExistsFlag = False






        ###  Verfiy a role can be updated by the admin user
        if editRoleFlag:
            tableHandle = getHandle(setup, UMConstants.UMSCREEN_MANAGEROLES, 'table')
            tableData_beforeUpdateRole = roleScreenInstance.table.getTableData1(tableHandle)
            if tableData_beforeUpdateRole['rows'] != Constants.NODATA:
                numberOfRows_beforeUpdateRole = len(tableData_beforeUpdateRole['rows'])
                roleDetail = rolesDetailsDict['edit1']
                columnValueInRowToBeEdited = rolesDetailsDict[k]['rolename']
                expectedRoleName, expectedCheckedCheckBoxesList, createBtnStatus = MRX_UMHelper.editRole(setup=setup,tableHandle=tableHandle,screenInstance=roleScreenInstance,screen=UMConstants.UMSCREEN_MANAGEROLES,columnValueInRowToBeEdited=columnValueInRowToBeEdited,k=str(k),roleDetail=roleDetail,colIndex=0)
                handle = getHandle(setup, UMConstants.UMPOPUP_ADDROLE, 'allbuttons')
                logger.debug("Going to click on 'Update' buttton on add role popup ")
                roleScreenInstance.hoverAndClickButton(setup, "Update", handle)
                expected_RoleEntry_forTable = [expectedRoleName] + expectedCheckedCheckBoxesList + ['', '']
                logger.debug("Getting table handle after Updating an existing role")
                tableHandle = getHandle(setup, UMConstants.UMSCREEN_MANAGEROLES, 'table')
                tableData_afterUpdateRole = roleScreenInstance.table.getTableData1(tableHandle)
                if tableData_afterUpdateRole['rows'] != Constants.NODATA:
                    numberOfRows_afterUpdateRole = len(tableData_afterUpdateRole['rows'])
                    roleEntry_forTableFromUI = []
                    rolenameFoundFlag = False
                    for row in tableData_afterUpdateRole['rows']:
                        if str(row[0]) == expectedRoleName:
                            logger.debug("Updated Rolename found in the first column of the table")
                            roleEntry_forTableFromUI = [str(row[0])] + row[1].replace(', ', ',').split(',') + [row[2]] + [row[3]]
                            rolenameFoundFlag = True
                            break

                    if not rolenameFoundFlag:
                        logger.debug(" Updated Rolename could not be found in the first column of the table")
                else:
                    numberOfRows_afterUpdateRole = 0
                    roleEntry_forTableFromUI = []
            else:
                numberOfRows_beforeUpdateRole = -1
                expected_RoleEntry_forTable =[]

            checkEqualAssert(sorted(expected_RoleEntry_forTable), sorted(roleEntry_forTableFromUI),message="Verify an existing row is successfully updated in manage roles table",testcase_id='Reflex-UM-4')
            checkEqualAssert(numberOfRows_beforeUpdateRole, numberOfRows_afterUpdateRole,message="Verify the count of rows after updating an existing role in manage roles table",testcase_id='Reflex-UM-4')
            editRoleFlag = False





        ###  Verfiy a role can be deleted by the admin user
        if deleteRoleFlag:
            tableHandle = getHandle(setup, UMConstants.UMSCREEN_MANAGEROLES, 'table')
            tableData_beforeDeleteRole = roleScreenInstance.table.getTableData1(tableHandle)
            if tableData_beforeDeleteRole['rows'] != Constants.NODATA:
                numberOfRows_beforeDeleteRole = len(tableData_beforeDeleteRole['rows'])
                columnValueInRowToBeDeleted = rolesDetailsDict['edit1']['rolename']
                MRX_UMHelper.deleteRole(setup=setup,tableHandle=tableHandle,screenInstance=roleScreenInstance,parentScreen=UMConstants.UMSCREEN_MANAGEROLES,screen=UMConstants.UMPOPUP_DELETEROLE,columnValueInRowToBeDeleted=columnValueInRowToBeDeleted,colIndex=0)
                tableHandle = getHandle(setup, UMConstants.UMSCREEN_MANAGEROLES, 'table')
                tableData_afterDeleteRole = roleScreenInstance.table.getTableData1(tableHandle)
                if tableData_afterDeleteRole['rows'] != Constants.NODATA:
                    numberOfRows_afterDeleteRole = len(tableData_afterDeleteRole['rows'])
                else:
                    numberOfRows_afterDeleteRole = 0
            else:
                numberOfRows_beforeDeleteRole = -1
            checkEqualAssert(numberOfRows_beforeDeleteRole-1, numberOfRows_afterDeleteRole,message="Verify the count of rows after deleting a role from manage roles table",testcase_id='Reflex-UM-5')
            deleteRoleFlag = False





        ### Verify help/close icon
        if checkHelpCloseIconFlag:
            handle = getHandle(setup, UMConstants.UMSCREEN_MANAGEROLES, 'newRoleIcon')
            MRX_UMHelper.clickOnPopupIcon(setup, h=handle, screen=UMConstants.UMSCREEN_MANAGEROLES,parent='newRoleIcon', child='icon')
            click_status = MRX_UMHelper.clickOnPopupIcon(setup, h=handle, screen=UMConstants.UMPOPUP_ADDROLE,parent='popupIcons', child='closeIcon')
            checkEqualAssert(True, click_status, message='Verify Close icon on Add Role Popup is clickable',testcase_id="Reflex-UM-190")

            handle = getHandle(setup, UMConstants.UMSCREEN_MANAGEROLES, 'newRoleIcon')
            MRX_UMHelper.clickOnPopupIcon(setup, h=handle, screen=UMConstants.UMSCREEN_MANAGEROLES,parent='newRoleIcon', child='icon')
            handle = getHandle(setup, UMConstants.UMPOPUP_ADDROLE, 'popupIcons')
            click_status = MRX_UMHelper.clickOnPopupIcon(setup, h=handle, screen=UMConstants.UMPOPUP_ADDROLE,parent='popupIcons', child='helpIcon')
            checkEqualAssert(True, click_status, message='Verify Help icon on Add Role Popup is clickable',testcase_id="Reflex-UM-191")
            checkHelpCloseIconFlag = False





    setup.d.close()


except Exception as e:
    logger.debug("Exception Occurred: "+ str(e))
    isError(setup)
    r = "issue_" + str(random.randint(0, 9999999)) + ".png"
    setup.d.save_screenshot(r)
    logger.debug("Got Exception from Script Level try catch :: Screenshot with name = %s is saved", r)
    setup.d.close()


