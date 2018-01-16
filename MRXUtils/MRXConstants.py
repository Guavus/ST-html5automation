from Utils.Constants import *
class MRXConstants(Constants):

    WEBDRIVERTIMEOUT = 12

    TIMEZONEOFFSET = 0
    TIMEPATTERN = '%d %b %Y %H:%M'
    UMTIMEPATTERN='%d-%m-%Y %H:%M'

    NumberOfSelectionOnAtAnyLevel = 2
    NumberOfElementToBeExpandOnAtAnyLevel = 3

    SEGMENTSCREEN = "segment_Screen"
    REPORTSCREEN = "report_Screen"
    DATAEXTRACTIONSCREEN="de_Screen"
    SEGMENTFILTERSCREEN="filter_Screen"
    UDSCREEN= "ud_Screen"
    COMPARATIVESCREEN="comparative_Screen"
    WFSTARTSCREEN = "workflowstart_Screen"
    UDPPOPUP= "udp_popup"
    DEPOPUP="de_popup"
    POPUPSCREEN="popUp_Screen"
    TMSCREEN="tm_Screen"
    EDITHEADERINEDITPOPUP = 'Edit Segment'
    CREATESEGMENT='Create Segment'
    IMPORTSEGMENT= 'Import Segment'
    INFOHEADERINPOPUP='Segment Info'
    FILTERSCREEN="filter_Screen"
    Apply_Filter='Apply Filters'
    Clear_All='Clear All'
    LFPOPUP='loadfilter_popup'
    PIVOTPOPUP = "pivotfilter_popup"
    SNFPOPUP='saveNewfilter_popup'
    ExploreScreen="explore_Screen"
    AvailableFilterList='availableFilterList'
    Logout='Logout'
    NO_FILTER='Filters'
    NO_FILTER_ON_POPUP='No filters'
    SearchValue='h'

    BREADCRUMB_SCREEN="breadCrumb_Screen"

    MRXUMSCREEN='mrxUserManagement_Screen'
    MRXUMPOPUP='mrxUserPopUp_Screen'
    ChangePasswordScreen = "changepassword_screen"
    MRX_SAME_USER_ERROR_MSG='Username already exists.'
    TimeRangeSpliter='-'
    NUMBEROFFILTERSCENARIO = 3
    NUMBEROFFILTERSCENARIOFORDE=2

    NUMBEROFFILTERSCENARIOFORCB=6
    NUMBEROFFILTERSCENARIOFORTM = 2

    SleepForComparativeScreen=60
    SleepForTNMScreen = 20

    ChangePassword ='Change Password'
    UMHeader="User Management"

    SEGMENT_TABLE_AT_BACKEND='campaign'
    DE_PGSQL_TABLE="de_last_extraction"
    DATAEXTRACTIONSCREENLABLE='Data Extraction'
    WFSCREEN="workflowstart_Screen"
    AvailableClassesOnDE=['Device','Network','Content','Usage']

    MinimumUserConfig=15
    Source_User_Distribution='User Distribution'
    ExpectedFilterOption = ['Segmentation Filters','Device Filters','Network Filters','Content Filters','Usage Filters']
    ExpectedFilterOptionForDE = ['Time Range', 'Measure', 'Top Rows (leave blank for All)', 'Segmentation Filters', 'Device Filters', 'Network Filters','Content Filters', 'Usage Filters']
    ExpectedQuickLinkList= ['Last 6 Months', 'Last Month', 'Last 7 days', 'Yesterday', 'Today', 'Calender']
    #ExpectedMeasure=['Volume (Upload)','Volume (Download)','Volume','# Session']
    ExpectedMeasure = ['Volume (Upload)', 'Volume (Download)', 'Volume', '# Network Session','# Web Domain Session','# IAB Session','# Contextual Session']
    ExpectedMeasureForDE = ['Volume (Upload)', 'Volume (Download)', 'Volume', '# Network Session', '# Web Domain Session','# IAB Session', '# Contextual Session', '# User']
    ListOfFilterContainingTree=['Content Interest','Operator Data Services','Location']
    SegmentScreenTableHeaderList= ['Segment Name','User Count','Status','Source','Owner','Access','Created on','Edit/Info','Delete']
    ReportScreenTableHeaderList = ['Id', 'Name', 'Type', 'Delivered on', 'Report Period', 'Download', 'Delete']
    UMScreenTableHeaderList=['Name', 'Username', 'Email', 'Application Role', 'Application Privileges','Network Role','Device Role', 'Last Modified', 'Status', 'Edit', 'Delete']
    ALL='ALL'
    REFRESH='Refresh'
    ALLLINKS = "alllinks"
    ALLTITLES="alltitles"
    ADMIN='admin'
    NODATAMSG='No Rows To Show'
    NewUser="New User"
    ColumnHeadeForRole_UM="Application Role"
    ExpectedUser_MRX=['Admin,AppUser,SegmentManager']
    MONTHLIST=['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    MSGFORSAMESEGMENT='Segment with same name already exists.'
    DE_TABLE_HEADER=['Method','Description','Last Extraction Date']
    Button_On_DEPOPUP=['Extract Data Set','Cancel']
    MaximumValueForTopRowInput=1000
    DefaultSelectionOnCBScreen=['Last 7 days','__','Volume','__','__ by Volume','__: Volume for All','Select data to compare','Select data to breakdown']
    ExpectedCompareValue=['__', 'Segment','Category', 'Manufacturer', 'OS', 'Model', 'Serving Node', 'Packet GW','Level 1', 'Level 2', 'Level 3', 'APN']
    ExpectedMeasureOnCB=['Volume (Upload)', 'Volume (Download)', 'Volume', '# Network Session', '# Web Domain Session', '# IAB Session', '# Contextual Session', '# User']
    AggreagableMeasureOnCB=['Volume (Upload)', 'Volume (Download)', 'Volume']
    ExpectedBrokenDownValue=['__','Radio Access Type', 'Roaming', 'Tier 1', 'Tier 2','Level 1', 'Level 2', 'Level 3','Category', 'Name', 'Web Domain', 'Global Data Service']
    ExpectedOptionForWorkFlow=['User Distribution','Behavior Trending','Comparative Breakdown']
    ExpectedOptionForNewUser=['Username*', 'First Name*', 'Last Name*', 'Email*', 'Password*', 'Confirm Password*', 'User Image', 'Role*','Network Data Privileges','Device Data Privileges','Timezone*']
    #Disabled_User_Login_Msg="Invalid credentials, please enter correct username and password."
    Passoword_Not_Matched='Passwords do not match.'
    Invalid_Current_Password='Invalid credentials, please enter correct current password.'
    #Accese_Denied_Msg="Access denied, please contact administrator."
    Accese_Denied_Msg="Invalid credentials, please enter correct username and password."
    BarChartIndex = 0
    LineChartIndex = 1
    TableViewIndex = 2

    # dimensionListForHover=['Radio Access Type', 'Roaming', 'Tier 1', 'Tier 2','Level 1', 'Level 2', 'Level 3','Category', 'Name', 'Web Domain', 'Global Data Service']
    # measureListForHover=['Volume (Upload)', 'Volume (Download)', 'Volume', '# Network Session', '# Web Domain Session', '# IAB Session', '# Contextual Session', '# User']
    # quickLinkListForHover=['Last 6 Months', 'Last Month', 'Last 7 days', 'Yesterday', 'Today','CustomClick_0']

    dimensionListForHover = ['Radio Access Type']
    measureListForHover = ['Volume']
    quickLinkListForHover = ['Last 7 days','CustomClick_0']

    ExpectedDefaultValueOnTM=[[0],'Last 7 days','Volume',1]
    ExpectedDrillDownOptionOnTM=['Create Segment','Apply as filter and pivot','Export data']
    AvailableOptionOnPivotPopup=['Workflow / Comparative Breakdown','Workflow / User Distribution']
    BaselinePath=['#000000']
    PivotPopupHeader="Apply as Filter and Pivot"
    TrendsScreen="Behavior Trending"
