## StudentVue App API Docs

Documentation and research of the API routes from the Official StudentVue App.

The app uses [SOAP](https://en.wikipedia.org/wiki/SOAP), and the authentication scheme for the main web service (`ProcessWebServiceRequest`) is through the `userID` and  `password` fields.

### Related Projects

[StudentVue-Community/StudentVue](https://github.com/StudentVue-Community/StudentVue) - unofficial Python implementation of the web and SOAP APIs

[StudentVue-Community/StudentVueDistrictFinder](https://github.com/StudentVue-Community/StudentVueDistrictFinder) - implements zip code finding and a dump of brute forced districts

[loganMD/StudentVuePlus](https://studentvue.plus) - minimalist third-party StudentVue client

### TOC
[Getting Zip Codes](#getting-zip-codes)

[Getting Messages](#getting-messages)

[Getting Calendar](#getting-calendar)

[Getting Attendance](#getting-attendance)

[Getting Gradebook](#getting-gradebook)

[Getting Class Notes](#getting-class-notes)

[Getting Student Mail](#getting-student-mail)

[Composing/Sending Student Mail](#composingsending-student-mail)

[Getting Student Info](#getting-student-info)

[Getting Class Schedule](#getting-class-schedule)

[Getting School Info](#getting-school-info)

[Getting Class Websites](#getting-class-websites)

[Listing Report Cards](#listing-report-cards)

[Getting a Specific Report Card](#getting-a-specific-report-card)

[Listing Documents](#listing-documents)

[Getting a Specific Document](#getting-a-specific-document)

### Getting Zip Codes
[Top](#TOC)

**Example Request:**
```xml
POST /Service/HDInfoCommunication.asmx HTTP/1.1
Host: support.edupoint.com
Accept: */*
Content-Type: text/xml; charset=utf-8
SOAPAction: http://edupoint.com/webservices/ProcessWebServiceRequest
Connection: close
Cookie: /* REDACTED */
Accept-Language: en-us
Content-Length: 736
Accept-Encoding: gzip, deflate
User-Agent: StudentVUE/8.0.26 CFNetwork/1121.2.2 Darwin/19.3.0

<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"><soap:Body><ProcessWebServiceRequest xmlns="http://edupoint.com/webservices/"><userID>EdupointDistrictInfo</userID><password>Edup01nt</password><skipLoginLog>1</skipLoginLog><parent>0</parent><webServiceHandleName>HDInfoServices</webServiceHandleName><methodName>GetMatchingDistrictList</methodName><paramStr>&lt;Parms&gt;&lt;Key&gt;5E4B7859-B805-474B-A833-FDB15D205D40&lt;/Key&gt;&lt;MatchToDistrictZipCode&gt;94127&lt;/MatchToDistrictZipCode&gt;&lt;/Parms&gt;</paramStr></ProcessWebServiceRequest></soap:Body></soap:Envelope>
```

**Example Response:**
```xml
HTTP/1.1 200 OK
Cache-Control: private, max-age=0
Content-Type: text/xml; charset=utf-8
Server: Microsoft-IIS/8.0
X-AspNet-Version: 4.0.30319
X-Powered-By: ASP.NET
Date: Sun, 16 Feb 2020 04:36:22 GMT
Connection: close
Content-Length: 1417

<?xml version="1.0" encoding="utf-8"?><soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema"><soap:Body><ProcessWebServiceRequestResponse xmlns="http://edupoint.com/webservices/"><ProcessWebServiceRequestResult>&lt;DistrictLists xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"&gt;
     &lt;DistrictInfos&gt;
          &lt;DistrictInfo DistrictID="" Name="Jefferson Elementary School District" Address="Daly City CA 94015" PvueURL="https://portal.jsd.k12.ca.us/" /&gt;
          &lt;DistrictInfo DistrictID="" Name="Jefferson Union High School District" Address="Daly City CA 94015" PvueURL="https://genesis.juhsd.net/pxp" /&gt;
          &lt;DistrictInfo DistrictID="" Name="Millbrae School District" Address="Millbrae CA 94030" PvueURL="https://mesdparentvue.millbraesd.org" /&gt;
          &lt;DistrictInfo DistrictID="" Name="Newark Unified School District" Address="Newark CA 94560" PvueURL="https://vue.newarkunified.org/PXP" /&gt;
          &lt;DistrictInfo DistrictID="" Name="San Francisco Unified School District" Address="San Francisco CA 94102" PvueURL="https://portal.sfusd.edu/" /&gt;
     &lt;/DistrictInfos&gt;
&lt;/DistrictLists&gt;</ProcessWebServiceRequestResult></ProcessWebServiceRequestResponse></soap:Body></soap:Envelope>
```

**Notes:**

Uses `<methodName>GetMatchingDistrictList</methodName>`, a system account(`<userID>EdupointDistrictInfo</userID><password>Edup01nt</password>`) and a provided zip code (`&lt;MatchToDistrictZipCode&gt;94127&lt;/MatchToDistrictZipCode&gt;`) and returns nearby schools. The system account could have interesting privileges.

### Getting Messages
[Top](#TOC)

**Example Request:**
```xml
POST //Service/PXPCommunication.asmx HTTP/1.1
Host: portal.sfusd.edu
Accept: */*
Content-Type: text/xml; charset=utf-8
SOAPAction: http://edupoint.com/webservices/ProcessWebServiceRequest
Connection: close
Cookie: /* REDACTED */
Accept-Language: en-us
Content-Length: 630
Accept-Encoding: gzip, deflate
User-Agent: StudentVUE/8.0.26 CFNetwork/1121.2.2 Darwin/19.3.0

<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"><soap:Body><ProcessWebServiceRequest xmlns="http://edupoint.com/webservices/"><userID>/* REDACTED */</userID><password>/* REDACTED */</password><skipLoginLog>1</skipLoginLog><parent>0</parent><webServiceHandleName>PXPWebServices</webServiceHandleName><methodName>GetPXPMessages</methodName><paramStr>&lt;Parms&gt;&lt;childIntID&gt;0&lt;/childIntID&gt;&lt;/Parms&gt;</paramStr></ProcessWebServiceRequest></soap:Body></soap:Envelope>
```

**Example Response:**
```xml
HTTP/1.1 200 OK
Cache-Control: private, max-age=0
Content-Type: text/xml; charset=utf-8
Date: Sun, 16 Feb 2020 04:49:30 GMT
Content-Length: 99973
Connection: close
Vary: Accept-Encoding

<?xml version="1.0" encoding="utf-8"?><soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema"><soap:Body><ProcessWebServiceRequestResponse xmlns="http://edupoint.com/webservices/"><ProcessWebServiceRequestResult>&lt;PXPMessagesData xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"&gt;
     &lt;MessageListings&gt;
          &lt;MessageListing IconURL="images/PXP/TchComment_S.gif" ID="D9CD897E-E50F-44F9-92B5-A19CE021BB1E" BeginDate="02/07/2020 08:06:00" Type="StudentActivity" Subject="Kai - AP Physics 1B: Week 6 Assignment -- 40 HW Points (2/7/2020)" Content="&amp;lt;p&amp;gt;The assignment for this week is...&amp;lt;/p&amp;gt;&amp;#xD;&amp;#xA;&amp;#xD;&amp;#xA;&amp;lt;p&amp;gt;Chapter 13 (p. 423-429):&amp;lt;br /&amp;gt;&amp;#xD;&amp;#xA;Conceptual Exercises 3, 7, 10, 14&amp;lt;br /&amp;gt;&amp;#xD;&amp;#xA;Problems 2, 6, 9, 12, 18, 20, 31, 34, 41, 47, 51, 52, 58, 64, 67, 74&amp;lt;/p&amp;gt;&amp;#xD;&amp;#xA;&amp;#xD;&amp;#xA;&amp;lt;p&amp;gt;The relevant reading is most of Chapter 13 (except sections 13-7 and 13-8).&amp;lt;/p&amp;gt;" Read="false" Deletable="true" From="Scott Dickerman" SubjectNoHTML="Kai - AP Physics 1B: Week 6 Assignment -- 40 HW Points (2/7/2020)" /&gt;
          <!-- Continued... -->
     &lt;/MessageListings&gt;
&lt;/PXPMessagesData&gt;</ProcessWebServiceRequestResult></ProcessWebServiceRequestResponse></soap:Body></soap:Envelope>
```

**Notes:**

Uses `<methodName>GetPXPMessages</methodName>` and user credentials.

### Getting Calendar
[Top](#TOC)

**Example Request:**
```xml
POST //Service/PXPCommunication.asmx HTTP/1.1
Host: portal.sfusd.edu
Accept: */*
Content-Type: text/xml; charset=utf-8
SOAPAction: http://edupoint.com/webservices/ProcessWebServiceRequest
Connection: close
Cookie: /* REDACTED */
Accept-Language: en-us
Content-Length: 684
Accept-Encoding: gzip, deflate
User-Agent: StudentVUE/8.0.26 CFNetwork/1121.2.2 Darwin/19.3.0

<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"><soap:Body><ProcessWebServiceRequest xmlns="http://edupoint.com/webservices/"><userID>/* REDACTED */</userID><password>/* REDACTED */</password><skipLoginLog>1</skipLoginLog><parent>0</parent><webServiceHandleName>PXPWebServices</webServiceHandleName><methodName>StudentCalendar</methodName><paramStr>&lt;Parms&gt; &lt;childIntID&gt;0&lt;/childIntID&gt; &lt;RequestDate&gt;02/15/2020&lt;/RequestDate&gt;  &lt;/Parms&gt;</paramStr></ProcessWebServiceRequest></soap:Body></soap:Envelope>
```

**Example Response:**
```xml
HTTP/1.1 200 OK
Cache-Control: private, max-age=0
Content-Type: text/xml; charset=utf-8
Date: Sun, 16 Feb 2020 05:00:03 GMT
Content-Length: 9004
Connection: close
Vary: Accept-Encoding

<?xml version="1.0" encoding="utf-8"?><soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema"><soap:Body><ProcessWebServiceRequestResponse xmlns="http://edupoint.com/webservices/"><ProcessWebServiceRequestResult>&lt;CalendarListing xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" SchoolBegDate="08/19/2019" SchoolEndDate="06/02/2020" MonthBegDate="01/26/2020" MonthEndDate="02/29/2020"&gt;
     &lt;EventLists&gt;
          &lt;EventList Date="01/26/2020" Title="Watters, C  AP US History B(5) : Chapter 18 SAQ  - Score: 80.00" Icon="assignment.png" AGU="0" DayType="Assignment" StartTime="" Link="ASSIGNMENTS" DGU="1592243" ViewType="2" AddLinkData="F9F118EC-276A-4CD9-A69C-524BA16456CD" /&gt;
          <!-- Continued... -->
     &lt;/EventLists&gt;
&lt;/CalendarListing&gt;</ProcessWebServiceRequestResult></ProcessWebServiceRequestResponse></soap:Body></soap:Envelope>
```

**Notes:**

Uses `<methodName>StudentCalendar</methodName>` and user credentials.

### Getting Attendance
[Top](#TOC)

**Example Request:**
```xml
POST //Service/PXPCommunication.asmx HTTP/1.1
Host: portal.sfusd.edu
Accept: */*
Content-Type: text/xml; charset=utf-8
SOAPAction: http://edupoint.com/webservices/ProcessWebServiceRequest
Connection: close
Cookie: /* REDACTED */
Accept-Language: en-us
Content-Length: 626
Accept-Encoding: gzip, deflate
User-Agent: StudentVUE/8.0.26 CFNetwork/1121.2.2 Darwin/19.3.0

<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"><soap:Body><ProcessWebServiceRequest xmlns="http://edupoint.com/webservices/"><userID>/* REDACTED */</userID><password>/* REDACTED */</password><skipLoginLog>1</skipLoginLog><parent>0</parent><webServiceHandleName>PXPWebServices</webServiceHandleName><methodName>Attendance</methodName><paramStr>&lt;Parms&gt;&lt;ChildIntID&gt;0&lt;/ChildIntID&gt;&lt;/Parms&gt;</paramStr></ProcessWebServiceRequest></soap:Body></soap:Envelope>
```

**Example Response:**
```xml
HTTP/1.1 200 OK
Cache-Control: private, max-age=0
Content-Type: text/xml; charset=utf-8
Date: Sun, 16 Feb 2020 05:18:45 GMT
Content-Length: 21374
Connection: close
Set-Cookie: /* REDACTED */
Vary: Accept-Encoding

<?xml version="1.0" encoding="utf-8"?><soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema"><soap:Body><ProcessWebServiceRequestResponse xmlns="http://edupoint.com/webservices/"><ProcessWebServiceRequestResult>&lt;Attendance xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" Type="Period" StartPeriod="0" EndPeriod="14" PeriodCount="15"&gt;
     &lt;Absences&gt;
          &lt;Absence AbsenceDate="01/28/2020" Reason="N/S" Note="" DailyIconName="icon_unexcused.gif"&gt;
               &lt;Periods&gt;
                    &lt;Period Number="2" Name="Unexcused" Reason="A" Course="AP Comp Sci A B" Staff="Arthur Simon" StaffEMail="SIMONA1@sfusd.edu" IconName="icon_unexcused.gif" SchoolName="Lowell HS" StaffGU="37E8254B-CFC0-4DEC-926C-CDCAEB238444" OrgYearGU="3EF9E4C8-35BA-48AE-810F-586E0B12E09E" /&gt;
               &lt;/Periods&gt;
          &lt;/Absence&gt;
          &lt;Absence AbsenceDate="01/16/2020" Reason="N/S" Note="" DailyIconName="icon_excused.gif"&gt;
               &lt;Periods&gt;
                    &lt;Period Number="2" Name="Excused" Reason="E" Course="AP Comp Sci A B" Staff="Arthur Simon" StaffEMail="SIMONA1@sfusd.edu" IconName="icon_excused.gif" SchoolName="Lowell HS" StaffGU="37E8254B-CFC0-4DEC-926C-CDCAEB238444" OrgYearGU="3EF9E4C8-35BA-48AE-810F-586E0B12E09E" /&gt;
                    &lt;Period Number="3" Name="Excused" Reason="E" Course="AP Physics 1B" Staff="Scott Dickerman" StaffEMail="DickermanS@sfusd.edu" IconName="icon_excused.gif" SchoolName="Lowell HS" StaffGU="51C4CDC4-6DB8-41E4-B9AB-CD91D15931EC" OrgYearGU="3EF9E4C8-35BA-48AE-810F-586E0B12E09E" /&gt;
                    &lt;Period Number="4" Name="Excused" Reason="E" Course="AP Environ Sci B" Staff="Katherine Melvin" StaffEMail="MelvinK@sfusd.edu" IconName="icon_excused.gif" SchoolName="Lowell HS" StaffGU="E4020707-0794-42F6-A6A4-C5C9E6745891" OrgYearGU="3EF9E4C8-35BA-48AE-810F-586E0B12E09E" /&gt;
                    &lt;Period Number="5" Name="Excused" Reason="E" Course="AP US History B" Staff="Christopher Watters" StaffEMail="WattersC@sfusd.edu" IconName="icon_excused.gif" SchoolName="Lowell HS" StaffGU="1FB15260-A238-405F-BF47-41C250E5899D" OrgYearGU="3EF9E4C8-35BA-48AE-810F-586E0B12E09E" /&gt;
                    &lt;Period Number="7" Name="Excused" Reason="E" Course="AP EngLngComp72 A" Staff="Lael Bajet" StaffEMail="BajetL@sfusd.edu" IconName="icon_excused.gif" SchoolName="Lowell HS" StaffGU="379C7799-3331-4C75-A3A7-35B22CBE4C3F" OrgYearGU="3EF9E4C8-35BA-48AE-810F-586E0B12E09E" /&gt;
                    &lt;Period Number="8" Name="Excused" Reason="E" Course="Pre-Calc B H" Staff="Wilson Sinn" StaffEMail="SinnW@sfusd.edu" IconName="icon_excused.gif" SchoolName="Lowell HS" StaffGU="615F1330-4138-4ED8-9EE3-F3AF18985B7C" OrgYearGU="3EF9E4C8-35BA-48AE-810F-586E0B12E09E" /&gt;
                    &lt;Period Number="9" Name="Excused" Reason="E" Course="Homeroom" Staff="Carole Cadoppi" StaffEMail="CadoppiC@sfusd.edu" IconName="icon_excused.gif" SchoolName="Lowell HS" StaffGU="80A53656-ABDB-4208-9753-C012AF2C96D7" OrgYearGU="3EF9E4C8-35BA-48AE-810F-586E0B12E09E" /&gt;
               &lt;/Periods&gt;
          &lt;/Absence&gt;
          <!-- Continued... -->
     &lt;/Absences&gt;
     &lt;TotalExcused&gt;
          &lt;PeriodTotal Number="0" Total="0" /&gt;
          <!-- Continued... -->
     &lt;/TotalExcused&gt;
     &lt;TotalTardies&gt;
          &lt;PeriodTotal Number="0" Total="0" /&gt;
          <!-- Continued... -->
     &lt;/TotalTardies&gt;
     &lt;TotalUnexcused&gt;
          &lt;PeriodTotal Number="0" Total="0" /&gt;
          <!-- Continued... -->
     &lt;/TotalUnexcused&gt;
     &lt;TotalActivities&gt;
          &lt;PeriodTotal Number="0" Total="0" /&gt;
          <!-- Continued... -->
     &lt;/TotalActivities&gt;
     &lt;TotalUnexcusedTardies&gt;
          &lt;PeriodTotal Number="0" Total="0" /&gt;
          <!-- Continued... -->
     &lt;/TotalUnexcusedTardies&gt;
&lt;/Attendance&gt;</ProcessWebServiceRequestResult></ProcessWebServiceRequestResponse></soap:Body></soap:Envelope>
```

**Notes:**

Uses `<methodName>Attendance</methodName>` and user credentials.

### Getting Gradebook
[Top](#TOC)

**Example Request:**
```xml
POST //Service/PXPCommunication.asmx HTTP/1.1
Host: portal.sfusd.edu
Accept: */*
Content-Type: text/xml; charset=utf-8
SOAPAction: http://edupoint.com/webservices/ProcessWebServiceRequest
Connection: close
Cookie: /* REDACTED */
Accept-Language: en-us
Content-Length: 625
Accept-Encoding: gzip, deflate
User-Agent: StudentVUE/8.0.26 CFNetwork/1121.2.2 Darwin/19.3.0

<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"><soap:Body><ProcessWebServiceRequest xmlns="http://edupoint.com/webservices/"><userID>/* REDACTED */</userID><password>/* REDACTED */</password><skipLoginLog>1</skipLoginLog><parent>0</parent><webServiceHandleName>PXPWebServices</webServiceHandleName><methodName>Gradebook</methodName><paramStr>&lt;Parms&gt;&lt;ChildIntID&gt;0&lt;/ChildIntID&gt;&lt;/Parms&gt;</paramStr></ProcessWebServiceRequest></soap:Body></soap:Envelope>
```

**Example Response:**
```xml
HTTP/1.1 200 OK
Cache-Control: private, max-age=0
Content-Type: text/xml; charset=utf-8
Date: Sun, 16 Feb 2020 05:41:23 GMT
Content-Length: 27681
Connection: close
Set-Cookie: /* REDACTED */
Vary: Accept-Encoding

<?xml version="1.0" encoding="utf-8"?><soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema"><soap:Body><ProcessWebServiceRequestResponse xmlns="http://edupoint.com/webservices/"><ProcessWebServiceRequestResult>&lt;Gradebook xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" Type="Traditional" ErrorMessage="" HideStandardGraphInd="false" HideMarksColumnElementary="true" HidePointsColumnElementary="false" HidePercentSecondary="false" DisplayStandardsData="false" GBStandardsTabDefault="false"&gt;
     &lt;ReportingPeriods&gt;
          &lt;ReportPeriod Index="0" GradePeriod="P1" StartDate="8/19/2019" EndDate="9/27/2019" /&gt;
          &lt;ReportPeriod Index="1" GradePeriod="P2" StartDate="9/28/2019" EndDate="11/8/2019" /&gt;
          &lt;ReportPeriod Index="2" GradePeriod="P3/Fall" StartDate="11/9/2019" EndDate="12/20/2019" /&gt;
          &lt;ReportPeriod Index="3" GradePeriod="P4" StartDate="12/21/2019" EndDate="2/21/2020" /&gt;
          &lt;ReportPeriod Index="4" GradePeriod="P5" StartDate="2/22/2020" EndDate="4/17/2020" /&gt;
          &lt;ReportPeriod Index="5" GradePeriod="P6/Spring" StartDate="4/18/2020" EndDate="6/2/2020" /&gt;
     &lt;/ReportingPeriods&gt;
     &lt;ReportingPeriod GradePeriod="P4" StartDate="12/21/2019" EndDate="2/21/2020" /&gt;
     &lt;Courses&gt;
          &lt;Course Period="7" Title="AP EngLngComp72 A (ELAC302A)" Room="135" Staff="Lael Bajet" StaffEMail="BajetL@sfusd.edu" StaffGU="379C7799-3331-4C75-A3A7-35B22CBE4C3F" HighlightPercentageCutOffForProgressBar="50"&gt;
               &lt;Marks&gt;
                    &lt;Mark MarkName="P4" CalculatedScoreString="A" CalculatedScoreRaw="90.5"&gt;
                         &lt;StandardViews /&gt;
                         &lt;GradeCalculationSummary /&gt;
                         &lt;Assignments&gt;
                              &lt;Assignment GradebookID="1637597" Measure="Inferno PPE: 3-8" Type="Essays and Projects" Date="2/14/2020" DueDate="2/24/2020" Score="A" ScoreType="Letter Grade" Points="50.00 / 50.0000" Notes="" TeacherID="273733" StudentID="312711" MeasureDescription="See GC" HasDropBox="false" DropStartDate="2/14/2020" DropEndDate="2/15/2020"&gt;
                                   &lt;Resources /&gt;
                                   &lt;Standards /&gt;
                              &lt;/Assignment&gt;
                              <!-- Continued -->
                         &lt;/Assignments&gt;
                    &lt;/Mark&gt;
               &lt;/Marks&gt;
          &lt;/Course&gt;
          <!-- Continued -->
     &lt;/Courses&gt;
&lt;/Gradebook&gt;</ProcessWebServiceRequestResult></ProcessWebServiceRequestResponse></soap:Body></soap:Envelope>
```

**Notes:**

Uses `<methodName>Gradebook</methodName>` and user credentials.

Optionally you can use the `ReportPeriod` parameter with the index of the desired reporting period in the `<ReportingPeriods>...</ReportingPeriods>` field to get the gradebook for a reporting period.

### Getting Class Notes
[Top](#TOC)

**Example Request:**
```xml
POST //Service/PXPCommunication.asmx HTTP/1.1
Host: portal.sfusd.edu
Accept: */*
Content-Type: text/xml; charset=utf-8
SOAPAction: http://edupoint.com/webservices/ProcessWebServiceRequest
Connection: close
Cookie: /* REDACTED */
Accept-Language: en-us
Content-Length: 631
Accept-Encoding: gzip, deflate
User-Agent: StudentVUE/8.0.26 CFNetwork/1121.2.2 Darwin/19.3.0

<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"><soap:Body><ProcessWebServiceRequest xmlns="http://edupoint.com/webservices/"><userID>/* REDACTED */</userID><password>/* REDACTED */</password><skipLoginLog>1</skipLoginLog><parent>0</parent><webServiceHandleName>PXPWebServices</webServiceHandleName><methodName>StudentHWNotes</methodName><paramStr>&lt;Parms&gt;&lt;childIntID&gt;0&lt;/childIntID&gt; &lt;/Parms&gt;</paramStr></ProcessWebServiceRequest></soap:Body></soap:Envelope>
```

**Example Response:**
```xml
HTTP/1.1 200 OK
Cache-Control: private, max-age=0
Content-Type: text/xml; charset=utf-8
Date: Sun, 16 Feb 2020 06:20:43 GMT
Content-Length: 726
Connection: close
Vary: Accept-Encoding

<?xml version="1.0" encoding="utf-8"?><soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema"><soap:Body><ProcessWebServiceRequestResponse xmlns="http://edupoint.com/webservices/"><ProcessWebServiceRequestResult>&lt;GBHWNotesDatas xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" StudentGU="F24B3988-C7F1-4FBC-AF8F-D8D376C54B97" sisNumber="20118247" StudentSSY="EDDE12BB-599F-4C17-AC54-E6A0064C7B02"&gt;
     &lt;GBHomeWorkNotesRecords /&gt;
&lt;/GBHWNotesDatas&gt;</ProcessWebServiceRequestResult></ProcessWebServiceRequestResponse></soap:Body></soap:Envelope>
```

**Notes:**

Uses `<methodName>StudentHWNotes</methodName>` and user credentials.

My teachers don't use this feature, so I don't have a helpful example response.

### Composing/Sending Student Mail
[Top](#TOC)

**Example Request:**
```xml
TBD
```

**Example Response:**
```xml
TBD
```

**Notes:**
COMING SOON

Not all school districts use this feature.

### Getting Student Mail
[Top](#TOC)

**Example Request:**
```xml
TBD
```

**Example Response:**
```xml
TBD
```

**Notes:**
COMING SOON

Not all school districts use this feature.

### Getting Student Info
[Top](#TOC)

**Example Request:**
```xml
POST //Service/PXPCommunication.asmx HTTP/1.1
Host: portal.sfusd.edu
Accept: */*
Content-Type: text/xml; charset=utf-8
SOAPAction: http://edupoint.com/webservices/ProcessWebServiceRequest
Connection: close
Cookie: /* REDACTED */
Accept-Language: en-us
Content-Length: 627
Accept-Encoding: gzip, deflate
User-Agent: StudentVUE/8.0.26 CFNetwork/1121.2.2 Darwin/19.3.0

<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"><soap:Body><ProcessWebServiceRequest xmlns="http://edupoint.com/webservices/"><userID>/* REDACTED */</userID><password>/* REDACTED */</password><skipLoginLog>1</skipLoginLog><parent>0</parent><webServiceHandleName>PXPWebServices</webServiceHandleName><methodName>StudentInfo</methodName><paramStr>&lt;Parms&gt;&lt;ChildIntID&gt;0&lt;/ChildIntID&gt;&lt;/Parms&gt;</paramStr></ProcessWebServiceRequest></soap:Body></soap:Envelope>
```

**Example Response:**
```xml
HTTP/1.1 200 OK
Cache-Control: private, max-age=0
Content-Type: text/xml; charset=utf-8
Date: Sun, 16 Feb 2020 06:23:14 GMT
Content-Length: 58162
Connection: close
Set-Cookie: /* REDACTED */
Vary: Accept-Encoding

<?xml version="1.0" encoding="utf-8"?><soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema"><soap:Body><ProcessWebServiceRequestResponse xmlns="http://edupoint.com/webservices/"><ProcessWebServiceRequestResult>&lt;StudentInfo xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" Type="Detail"&gt;
     &lt;LockerInfoRecords /&gt;
     &lt;FormattedName&gt;/* REDACTED */&lt;/FormattedName&gt;
     &lt;PermID&gt;/* REDACTED */&lt;/PermID&gt;
     &lt;Gender&gt;/* REDACTED */&lt;/Gender&gt;
     &lt;Grade&gt;/* REDACTED */&lt;/Grade&gt;
     &lt;Address&gt;/* REDACTED */&lt;/Address&gt;
     &lt;LastNameGoesBy /&gt;
     &lt;NickName /&gt;
     &lt;BirthDate&gt;/* REDACTED */&lt;/BirthDate&gt;
     &lt;EMail&gt;/* REDACTED */&lt;/EMail&gt;
     &lt;Phone&gt;/* REDACTED */&lt;/Phone&gt;
     &lt;HomeLanguage /&gt;
     &lt;CurrentSchool&gt;Lowell HS&lt;/CurrentSchool&gt;
     &lt;Track /&gt;
     &lt;HomeRoomTch&gt;Carole Cadoppi&lt;/HomeRoomTch&gt;
     &lt;HomeRoomTchEMail&gt;CadoppiC@sfusd.edu&lt;/HomeRoomTchEMail&gt;
     &lt;HomeRoomTchStaffGU&gt;80A53656-ABDB-4208-9753-C012AF2C96D7&lt;/HomeRoomTchStaffGU&gt;
     &lt;OrgYearGU&gt;3EF9E4C8-35BA-48AE-810F-586E0B12E09E&lt;/OrgYearGU&gt;
     &lt;HomeRoom&gt;2103&lt;/HomeRoom&gt;
     &lt;CounselorName&gt;Wilson, Amber&lt;/CounselorName&gt;
     &lt;Photo&gt;&lt;/Photo&gt;
     &lt;EmergencyContacts /&gt;
     &lt;Physician Name="" Hospital="" Phone="" Extn="" /&gt;
     &lt;Dentist Name="" Office="" Phone="" Extn="" /&gt;
     &lt;UserDefinedGroupBoxes&gt;
          &lt;UserDefinedGroupBox GroupBoxLabel="Other Data"&gt;
               &lt;UserDefinedItems&gt;
                    &lt;UserDefinedItem ItemLabel="Counselor Name" ItemType="REV_EDIT_TEXT" Rev_Text="" SourceObject="0AFBF98B-3A86-4173-9BCC-E43C032ABEC4" SourceElement="CounselorFormattedName" VCID="211C518E-F1A8-4FBF-8C3D-3792541E4FE9" Value="Wilson, Amber" /&gt;
               &lt;/UserDefinedItems&gt;
          &lt;/UserDefinedGroupBox&gt;
     &lt;/UserDefinedGroupBoxes&gt;
&lt;/StudentInfo&gt;</ProcessWebServiceRequestResult></ProcessWebServiceRequestResponse></soap:Body></soap:Envelope>
```

**Notes:**

Uses `<methodName>StudentInfo</methodName>` and user credentials.

### Getting Class Schedule
[Top](#TOC)

**Example Request:**
```xml
POST //Service/PXPCommunication.asmx HTTP/1.1
Host: portal.sfusd.edu
Accept: */*
Content-Type: text/xml; charset=utf-8
SOAPAction: http://edupoint.com/webservices/ProcessWebServiceRequest
Connection: close
Cookie: /* REDACTED */
Accept-Language: en-us
Content-Length: 670
Accept-Encoding: gzip, deflate
User-Agent: StudentVUE/8.0.26 CFNetwork/1121.2.2 Darwin/19.3.0

<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"><soap:Body><ProcessWebServiceRequest xmlns="http://edupoint.com/webservices/"><userID>/* REDACTED */</userID><password>/* REDACTED */</password><skipLoginLog>1</skipLoginLog><parent>0</parent><webServiceHandleName>PXPWebServices</webServiceHandleName><methodName>StudentClassList</methodName><paramStr>&lt;Parms&gt;&lt;childIntID&gt;0&lt;/childIntID&gt; &lt;TermIndex&gt;1&lt;/TermIndex&gt; &lt;/Parms&gt;</paramStr></ProcessWebServiceRequest></soap:Body></soap:Envelope>
```

**Example Response:**
```xml
HTTP/1.1 200 OK
Cache-Control: private, max-age=0
Content-Type: text/xml; charset=utf-8
Date: Sun, 22 Mar 2020 17:19:04 GMT
Content-Length: 3963
Connection: close
Vary: Accept-Encoding

<?xml version="1.0" encoding="utf-8"?><soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema"><soap:Body><ProcessWebServiceRequestResponse xmlns="http://edupoint.com/webservices/"><ProcessWebServiceRequestResult>&lt;StudentClassSchedule xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" TermIndex="1" TermIndexName="Spring" ErrorMessage=""&gt;
     &lt;ClassLists&gt;
          &lt;ClassListing Period="2" CourseTitle="AP Comp Sci A B" RoomName="334" Teacher="Arthur Simon" TeacherEmail="SIMONA1@sfusd.edu" SectionGU="2549B62B-A20A-4A0C-A203-ECDE3EB0C8BE" TeacherStaffGU="37E8254B-CFC0-4DEC-926C-CDCAEB238444"&gt;
               &lt;AdditionalStaffInformationXMLs /&gt;
          &lt;/ClassListing&gt;
          <!-- Continued -->
     &lt;/ClassLists&gt;
     &lt;TermLists&gt;
          &lt;TermListing TermIndex="0" TermCode="1" TermName="Fall" BeginDate="08/19/2019" EndDate="12/20/2019" SchoolYearTrmCodeGU="7E09DC1F-D40F-4284-9F7F-8C226827AEF1"&gt;
               &lt;TermDefCodes&gt;
                    &lt;TermDefCode TermDefName="S1" /&gt;
                    &lt;TermDefCode TermDefName="FY" /&gt;
               &lt;/TermDefCodes&gt;
          &lt;/TermListing&gt;
          <!-- Continued -->
     &lt;/TermLists&gt;
     &lt;ConcurrentSchoolStudentClassSchedules /&gt;
&lt;/StudentClassSchedule&gt;</ProcessWebServiceRequestResult></ProcessWebServiceRequestResponse></soap:Body></soap:Envelope>
```

**Notes:**

Uses `<methodName>StudentClassList</methodName>` and user credentials.

Optionally you can use the `TermIndex` parameter with the index of the desired term in the `<TermLists>...</TermLists>` field to get the schedule for a specific term.

### Getting School Info
[Top](#TOC)

**Example Request:**
```xml
POST //Service/PXPCommunication.asmx HTTP/1.1
Host: portal.sfusd.edu
Accept: */*
Content-Type: text/xml; charset=utf-8
SOAPAction: http://edupoint.com/webservices/ProcessWebServiceRequest
Connection: close
Cookie: /* REDACTED */
Accept-Language: en-us
Content-Length: 633
Accept-Encoding: gzip, deflate
User-Agent: StudentVUE/8.0.26 CFNetwork/1121.2.2 Darwin/19.3.0

<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"><soap:Body><ProcessWebServiceRequest xmlns="http://edupoint.com/webservices/"><userID>/* REDACTED */</userID><password>/* REDACTED */</password><skipLoginLog>1</skipLoginLog><parent>0</parent><webServiceHandleName>PXPWebServices</webServiceHandleName><methodName>StudentSchoolInfo</methodName><paramStr>&lt;Parms&gt;&lt;childIntID&gt;0&lt;/childIntID&gt;&lt;/Parms&gt;</paramStr></ProcessWebServiceRequest></soap:Body></soap:Envelope>
```

**Example Response:**
```xml
HTTP/1.1 200 OK
Cache-Control: private, max-age=0
Content-Type: text/xml; charset=utf-8
Date: Sun, 22 Mar 2020 17:23:11 GMT
Content-Length: 3303
Connection: close
Set-Cookie: /* REDACTED */
Vary: Accept-Encoding

<?xml version="1.0" encoding="utf-8"?><soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema"><soap:Body><ProcessWebServiceRequestResponse xmlns="http://edupoint.com/webservices/"><ProcessWebServiceRequestResult>&lt;StudentSchoolInfoListing xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" School="Lowell HS" Principal="Dacotah Swett" SchoolAddress="1101 Eucalyptus Dr" SchoolAddress2="" SchoolCity="San Francisco" SchoolState="CA" SchoolZip="94132" Phone="415-759-2730" Phone2="415-759-2742" URL="http://lhs.sfusd.edu"&gt;
     &lt;StaffLists&gt;
          &lt;StaffList Name="Aguirre, Maria" EMail="AguirreM1@sfusd.edu" Title="0923-Counselor" Phone="" Extn="" StaffGU="9C7EF45E-2C8F-4A70-822B-D5EE466653F5" /&gt;
					<!-- Continued -->
     &lt;/StaffLists&gt;
&lt;/StudentSchoolInfoListing&gt;</ProcessWebServiceRequestResult></ProcessWebServiceRequestResponse></soap:Body></soap:Envelope>
```

**Notes:**

Uses `<methodName>StudentSchoolInfo</methodName>` and user credentials.

### Getting Class Websites
[Top](#TOC)

**Example Request:**
```xml
```

**Example Response:**
```xml
```

**Notes:**

TODO

### Listing Report Cards
[Top](#TOC)

**Example Request:**
```xml
POST //Service/PXPCommunication.asmx HTTP/1.1
Host: portal.sfusd.edu
Accept: */*
Content-Type: text/xml; charset=utf-8
SOAPAction: http://edupoint.com/webservices/ProcessWebServiceRequest
Connection: close
Cookie: /* REDACTED */
Accept-Language: en-us
Content-Length: 640
Accept-Encoding: gzip, deflate
User-Agent: StudentVUE/8.0.26 CFNetwork/1121.2.2 Darwin/19.3.0

<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"><soap:Body><ProcessWebServiceRequest xmlns="http://edupoint.com/webservices/"><userID>/* REDACTED */</userID><password>/* REDACTED */</password><skipLoginLog>1</skipLoginLog><parent>0</parent><webServiceHandleName>PXPWebServices</webServiceHandleName><methodName>GetReportCardInitialData</methodName><paramStr>&lt;Parms&gt;&lt;childIntID&gt;0&lt;/childIntID&gt;&lt;/Parms&gt;</paramStr></ProcessWebServiceRequest></soap:Body></soap:Envelope>
```

**Example Response:**
```xml
HTTP/1.1 200 OK
Cache-Control: private, max-age=0
Content-Type: text/xml; charset=utf-8
Date: Sun, 22 Mar 2020 17:26:03 GMT
Content-Length: 1622
Connection: close
Vary: Accept-Encoding

<?xml version="1.0" encoding="utf-8"?><soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema"><soap:Body><ProcessWebServiceRequestResponse xmlns="http://edupoint.com/webservices/"><ProcessWebServiceRequestResult>&lt;RCReportingPeriodData xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"&gt;
     &lt;RCReportingPeriods&gt;
          &lt;RCReportingPeriod ReportingPeriodGU="0F5168E9-67CE-4481-BD60-980AD910D5FB" ReportingPeriodName="P1" EndDate="09/27/2019" Message="Click here to view report card for  P1" DocumentGU="/* REDACTED */" /&gt;
          <!-- Continued -->
     &lt;/RCReportingPeriods&gt;
&lt;/RCReportingPeriodData&gt;</ProcessWebServiceRequestResult></ProcessWebServiceRequestResponse></soap:Body></soap:Envelope>
```

**Notes:**

Uses `<methodName>GetReportCardInitialData</methodName>` and user credentials.

### Getting a Specific Report Card
[Top](#TOC)

**Example Request:**
```xml
POST //Service/PXPCommunication.asmx HTTP/1.1
Host: portal.sfusd.edu
Accept: */*
Content-Type: text/xml; charset=utf-8
SOAPAction: http://edupoint.com/webservices/ProcessWebServiceRequest
Connection: close
Cookie: /* REDACTED */
Accept-Language: en-us
Content-Length: 676
Accept-Encoding: gzip, deflate
User-Agent: StudentVUE/8.0.26 CFNetwork/1121.2.2 Darwin/19.3.0

<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"><soap:Body><ProcessWebServiceRequest xmlns="http://edupoint.com/webservices/"><userID>/* REDACTED */</userID><password>/* REDACTED */</password><skipLoginLog>1</skipLoginLog><parent>0</parent><webServiceHandleName>PXPWebServices</webServiceHandleName><methodName>GetReportCardDocumentData</methodName><paramStr>&lt;Parms&gt;&lt;DocumentGU&gt;/* REDACTED */&lt;/DocumentGU&gt;&lt;/Parms&gt;</paramStr></ProcessWebServiceRequest></soap:Body></soap:Envelope>
```

**Example Response:**
```xml
HTTP/1.1 200 OK
Cache-Control: private, max-age=0
Content-Type: text/xml; charset=utf-8
Date: Sun, 22 Mar 2020 17:27:06 GMT
Content-Length: 10182
Connection: close
Vary: Accept-Encoding

<?xml version="1.0" encoding="utf-8"?><soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema"><soap:Body><ProcessWebServiceRequestResponse xmlns="http://edupoint.com/webservices/"><ProcessWebServiceRequestResult>&lt;DocumentData xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" DocumentGU="/* REDACTED */" FileName="/* REDACTED */" DocFileName="/* REDACTED */" DocType="PDF"&gt;
     &lt;Base64Code&gt;/* REDACTED */&lt;/Base64Code&gt;
&lt;/DocumentData&gt;</ProcessWebServiceRequestResult></ProcessWebServiceRequestResponse></soap:Body></soap:Envelope>
```

**Notes:**

Uses `<methodName>GetReportCardDocumentData</methodName>` and user credentials.

Use the `DocumentGU` parameter to specify the document that you want.

### Listing Documents
[Top](#TOC)

**Example Request:**
```xml
POST //Service/PXPCommunication.asmx HTTP/1.1
Host: portal.sfusd.edu
Accept: */*
Content-Type: text/xml; charset=utf-8
SOAPAction: http://edupoint.com/webservices/ProcessWebServiceRequest
Connection: close
Cookie: /* REDACTED */
Accept-Language: en-us
Content-Length: 645
Accept-Encoding: gzip, deflate
User-Agent: StudentVUE/8.0.26 CFNetwork/1121.2.2 Darwin/19.3.0

<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"><soap:Body><ProcessWebServiceRequest xmlns="http://edupoint.com/webservices/"><userID>/* REDACTED */</userID><password>/* REDACTED */</password><skipLoginLog>1</skipLoginLog><parent>0</parent><webServiceHandleName>PXPWebServices</webServiceHandleName><methodName>GetStudentDocumentInitialData</methodName><paramStr>&lt;Parms&gt;&lt;childIntID&gt;0&lt;/childIntID&gt;&lt;/Parms&gt;</paramStr></ProcessWebServiceRequest></soap:Body></soap:Envelope>
```

**Example Response:**
```xml
HTTP/1.1 200 OK
Cache-Control: private, max-age=0
Content-Type: text/xml; charset=utf-8
Date: Sun, 22 Mar 2020 17:29:05 GMT
Content-Length: 3661
Connection: close
Set-Cookie: /* REDACTED */
Vary: Accept-Encoding

<?xml version="1.0" encoding="utf-8"?><soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema"><soap:Body><ProcessWebServiceRequestResponse xmlns="http://edupoint.com/webservices/"><ProcessWebServiceRequestResult>&lt;StudentDocuments xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" showDateColumn="true" showDocNameColumn="true" showDocCatColumn="true" StudentGU="F24B3988-C7F1-4FBC-AF8F-D8D376C54B97" StudentSSY="EDDE12BB-599F-4C17-AC54-E6A0064C7B02"&gt;
     &lt;StudentDocumentDatas&gt;
          &lt;StudentDocumentData DocumentGU="/* REDACTED */" DocumentFileName="/* REDACTED */" DocumentDate="02/27/2020" DocumentType="Report Card" StudentGU="F24B3988-C7F1-4FBC-AF8F-D8D376C54B97" DocumentComment="2019-2020 P4" /&gt;
          <!-- Continued -->
     &lt;/StudentDocumentDatas&gt;
&lt;/StudentDocuments&gt;</ProcessWebServiceRequestResult></ProcessWebServiceRequestResponse></soap:Body></soap:Envelope>
```

**Notes:**

Uses `<methodName>GetStudentDocumentInitialData</methodName>` and user credentials.

### Getting a Specific Document
[Top](#TOC)

**Example Request:**
```xml
POST //Service/PXPCommunication.asmx HTTP/1.1
Host: portal.sfusd.edu
Accept: */*
Content-Type: text/xml; charset=utf-8
SOAPAction: http://edupoint.com/webservices/ProcessWebServiceRequest
Connection: close
Cookie: /* REDACTED */
Accept-Language: en-us
Content-Length: 674
Accept-Encoding: gzip, deflate
User-Agent: StudentVUE/8.0.26 CFNetwork/1121.2.2 Darwin/19.3.0

<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"><soap:Body><ProcessWebServiceRequest xmlns="http://edupoint.com/webservices/"><userID>/* REDACTED */</userID><password>/* REDACTED */</password><skipLoginLog>1</skipLoginLog><parent>0</parent><webServiceHandleName>PXPWebServices</webServiceHandleName><methodName>GetContentOfAttachedDoc</methodName><paramStr>&lt;Parms&gt;&lt;DocumentGU&gt;/* REDACTED */&lt;/DocumentGU&gt;&lt;/Parms&gt;</paramStr></ProcessWebServiceRequest></soap:Body></soap:Envelope>
```

**Example Response:**
```xml
HTTP/1.1 200 OK
Cache-Control: private, max-age=0
Content-Type: text/xml; charset=utf-8
Date: Sun, 22 Mar 2020 17:29:19 GMT
Content-Length: 10438
Connection: close
Vary: Accept-Encoding

<?xml version="1.0" encoding="utf-8"?><soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema"><soap:Body><ProcessWebServiceRequestResponse xmlns="http://edupoint.com/webservices/"><ProcessWebServiceRequestResult>&lt;StudentAttachedDocumentData xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"&gt;
     &lt;DocumentCategoryLookups /&gt;
     &lt;DocumentDatas&gt;
          &lt;DocumentData DocumentGU="/* REDACTED */" StudentGU="F24B3988-C7F1-4FBC-AF8F-D8D376C54B97" DocDate="02/27/2020" FileName="/* REDACTED */" Category="04" Notes="2019-2020 P4" DocType="PDF"&gt;
               &lt;Base64Code&gt;/* REDACTED */&lt;/Base64Code&gt;
          &lt;/DocumentData&gt;
     &lt;/DocumentDatas&gt;
&lt;/StudentAttachedDocumentData&gt;</ProcessWebServiceRequestResult></ProcessWebServiceRequestResponse></soap:Body></soap:Envelope>
```

**Notes:**

Uses `<methodName>GetContentOfAttachedDoc</methodName>` and user credentials.

Use the `DocumentGU` parameter to specify the document that you want.
