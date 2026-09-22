## StudentVue JSON API Docs

Documentation of the API routes used by the current **StudentVUE (New)** app — Android `com.edupoint.studentvue`, iOS `studentvue-new/id6618112702` (researched against Android v1.9.16). The legacy **StudentVUE** app (`com.FreeLance.StudentVUE`, iOS `studentvue/id412050327`) is the one documented in [SOAP-API.md](SOAP-API.md).

The new app uses a JSON API for student data and keeps a subset of SOAP for configuration and account tasks. Authentication for the JSON API is HTTP Basic at login, then a Bearer token. GUIDs, tokens, and personal fields in the examples are placeholders; the district host is written as `https://<district>.edupoint.com`.

### TOC
[Transports](#transports)

[The JSON API](#the-json-api)

[Authentication](#authentication)

[Token refresh](#token-refresh)

[The edupointkeyversion header](#the-edupointkeyversion-header)

[Device attestation](#device-attestation)

[Errors](#errors)

[SOAP](#soap)

[Unauthenticated config methods](#unauthenticated-config-methods)

[Forgot password](#forgot-password)

[District lookup](#district-lookup)

[Method catalog](#method-catalog)

[Examples](#examples)

### Transports
[Top](#TOC)

| Endpoint | Used for |
|----------|----------|
| `POST https://<district>.edupoint.com/api/v1/mobile/PXPWebServices/<Method>` | all student data: schedule, gradebook, attendance, documents, mail, … |
| `POST https://<district>.edupoint.com/Service/PXPCommunication.asmx` | boot-time district config, activation, forgot password (SOAP) |
| `POST https://support.edupoint.com/Service/HDInfoCommunication.asmx` | district lookup by zip code (Edupoint-central) |

### The JSON API
[Top](#TOC)

**Example Request:**
```http
POST /api/v1/mobile/PXPWebServices/<Method> HTTP/1.1
Host: <district>.edupoint.com
Content-Type: application/json
User-Agent: ksoap
AppNameOSAndVersion: StudentVUE|Android|1.9.16
Authorization: Bearer <access_token>

{"arguments":{"request":"{\"childIntID\":0,\"languageCode\":\"en\"}"}}
```

**Example Response:**
```json
{"error": null, "data": {"studentDocuments": {}}}
```

**Notes:**

- The real parameters are a JSON object **serialized to a string** and placed at `arguments.request`. Not a nested object — a string. Some request fields (e.g. `UpdateNotificationPrefs`' `mobileUserSettings`) are JSON strings one level deeper still.
- Responses have exactly one method-specific key under `data` (see the [Method catalog](#method-catalog)). Field names ending in `XML` are usually JSON objects despite the name; a couple really are XML strings.
- `User-Agent: ksoap` is sent verbatim on JSON calls — a leftover from the SOAP days.
- `AppNameOSAndVersion` is `StudentVUE|Android|<appVersion>`.
- An optional `?DN=<districtDN>` query parameter is appended when the client knows a district number; omitting it works.
- ASP.NET session cookies are sent by the app but are not needed — bearer-only requests return full data. No certificate pinning was observed.

### Authentication
[Top](#TOC)

**Example Request:**
```http
POST /api/v1/mobile/PXPWebServices/AttemptLogin HTTP/1.1
Host: <district>.edupoint.com
Content-Type: application/json
User-Agent: ksoap
AppNameOSAndVersion: StudentVUE|Android|1.9.16
Authorization: Basic <base64(userID:password)>

{"arguments":{"request":"{\"userID\":null,\"password\":null,\"userType\":\"Student\"}"}}
```

**Example Response:**
```json
{
  "access_token": "<88 opaque characters>",
  "refresh_token": "<opaque>",
  "token_type": null,
  "expires_in": null,
  "scope": null
}
```

**Notes:**

- Credentials travel in the `Authorization: Basic` header only; the app nulls `userID`/`password` in the body. Both placements are accepted server-side, but header-only is what the app does.
- `userType` is `"Student"` for StudentVUE (`"parent"` on ParentVUE).
- `token`, `solu`, `decode` are only used for SAML/SSO re-entry; absent on a plain login.
- The login/refresh responses are a bare token object with **no `error` and no `data` key** — a different envelope than every other call. `expires_in`, `token_type`, `scope` were `null` on every observation; nothing about token expiry can be determined client-side.
- A failed login returns the ordinary error envelope, still with HTTP 200.

### Token refresh
[Top](#TOC)

**Example Request:**
```http
POST /api/v1/mobile/PXPWebServices/RefreshToken HTTP/1.1
Host: <district>.edupoint.com
Content-Type: application/json
User-Agent: ksoap
AppNameOSAndVersion: StudentVUE|Android|1.9.16
Authorization: Bearer <refresh_token>

{}
```

**Example Response:** the same bare token object as `AttemptLogin`, with a fresh pair.

**Notes:**

- Body is an empty JSON object — no `arguments` wrapper.
- The client does this automatically whenever a call returns HTTP **401** (the only non-200 status observed) and it holds a refresh token.

### The edupointkeyversion header
[Top](#TOC)

The app normally sends an `edupointkeyversion` header on every JSON call. Verified behaviour:

| request carries | result |
|---|---|
| header omitted | **accepted** (200) |
| header with a garbage value | **rejected** |
| header with a correctly computed value | accepted |

Clients can omit it today; the server-side check evidently exists behind a flag.

<details>
<summary>How the value is computed (reverse-engineered)</summary>

The app bundle contains CryptoJS-based helpers (`getGpaE`/`getGpaD`/`getGpaE2`/`getGpaES`/`getGpaDS`). The header uses `getGpaE2`, an AES-256-CBC encryption:

- **Plaintext:** `<MMDDYYYY>|<appVersion>|<MMDDYYYY>|android` — today's local date zero-padded, the app version, the date again, the literal platform. Verified in bytecode: exactly 7 concatenation parts.
- **Key:** a 32-byte ASCII constant embedded in the app's crypto helpers, trivially extractable from any APK. Its literal value is deliberately not published here — see the note below.
- **IV:** CryptoJS `Utf8.parse("AES")` — 3 bytes. CryptoJS XORs the IV word-per-32-bit-word and `x ^= undefined` coerces to `x ^= 0` in JS, so the effective 16-byte IV is `41 45 53 00 00 00 00 00 00 00 00 00 00 00 00 00`.
- **Padding/output:** PKCS#7, base64.

The same function encrypts the `<Parms>` XML of the forgot-password SOAP method (see [Forgot password](#forgot-password)).

Note: please don't paste live header values (or the extracted key) into issues, PRs, or pastes. If Edupoint rotates the key or starts enforcing the header, published values break things for everyone. Omitting the header works; prefer that.
</details>

### Device attestation
[Top](#TOC)

The client contains a device-key attestation flow that runs around login when a server-side `enableAttestation` flag is on: it fetches a signing challenge from `POST /api/v1/mobile/android-sign-challenge` (no auth; returns `challenge`, `challengeId`, `userGU`), signs it with a hardware-backed Keystore key, and submits `{keyAlias, publicKey, challenge, challengeId, attestationChain, packageName}` with the login. On a 403 "Key not registered" it wipes the local key and re-registers once.

As of v1.9.16 the flow is off in practice: the challenge endpoint returns 404 on districts observed, logins succeed with it skipped entirely, and there is a client kill switch. Nothing to implement today.

### Errors
[Top](#TOC)

Every call returns **HTTP 200, even on failure**. Check the body's `error` field:

**Example Response (gradebook at a school without gradebook):**
```json
{
  "error": {"code": "2100",
            "message": "Grade Book data not available for this school",
            "stackTrace": null},
  "data": null
}
```

**Example Response (module disabled district-wide):**
```json
{
  "error": {"code": "400",
            "message": "2100 - School District has not enabled access for the Fees Module.",
            "stackTrace": null},
  "data": null
}
```

**Example Response (server-side failure with a support ID):**
```json
{
  "error": {"code": "500",
            "message": "Error:  Please contact your school office for assistance. (ID: XXXXX)",
            "stackTrace": null},
  "data": null
}
```

**Notes:**

- `code "2100"` — the feature is not enabled at this school; treat as empty data, not as a failure.
- `code "400"` — e.g. past attendance not available for this school, or a module the district has disabled; the message often embeds a `2100 -` prefix even though the code is `400`.
- `code "500"` — generic server error. The `(ID: XXXXX)` suffix is a server-side event ID for the district's support desk; it varies per failure. Some `GetSynergyMail*` calls return this at districts even when `pxpMessagesData.supportingSynergyMail` is `true`.
- Don't treat unseen codes as benign; log them.
- This matters most for rarely-used areas (documents especially), where an empty result and an error look identical if you only check `data`.

### SOAP
[Top](#TOC)

The district SOAP endpoint is still `/Service/PXPCommunication.asmx`, but the wrapper element is now `ProcessWebServiceRequestMultiWeb` — the legacy `ProcessWebServiceRequest` from [SOAP-API.md](SOAP-API.md) plus a `webDBName` element. No `SOAPAction` header is sent.

**Example Request:**
```xml
POST /Service/PXPCommunication.asmx HTTP/1.1
Host: <district>.edupoint.com
Content-Type: text/xml; charset=utf-8

<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:web="http://edupoint.com/webservices/">
  <soapenv:Header/>
  <soapenv:Body>
    <web:ProcessWebServiceRequestMultiWeb>
      <web:userID></web:userID>
      <web:password></web:password>
      <web:skipLoginLog>1</web:skipLoginLog>
      <web:parent>0</web:parent>
      <web:webDBName></web:webDBName>
      <web:webServiceHandleName>PXPWebServices</web:webServiceHandleName>
      <web:methodName>GETSAMLSTATUS</web:methodName>
      <web:paramStr></web:paramStr>
    </web:ProcessWebServiceRequestMultiWeb>
  </soapenv:Body>
</soapenv:Envelope>
```

**Example Response:**
```xml
HTTP/1.1 200 OK
Content-Type: text/xml; charset=utf-8

<?xml version="1.0" encoding="utf-8"?><soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" ...><soap:Body><ProcessWebServiceRequestMultiWebResponse xmlns="http://edupoint.com/webservices/"><ProcessWebServiceRequestMultiWebResult>&lt;AllSAMLRecordData ... /&gt;</ProcessWebServiceRequestMultiWebResult></ProcessWebServiceRequestMultiWebResponse></soap:Body></soap:Envelope>
```

**Notes:**

- The inner result is HTML-escaped XML inside `ProcessWebServiceRequestMultiWebResult`, exactly like the legacy API — parse it twice.
- On failure the result contains `<RT_ERROR ERROR_MESSAGE="..." />` instead of a payload.
- Element order matters: `userID, password, skipLoginLog, parent, webDBName, webServiceHandleName, methodName, paramStr` (`parent` only in the `PXPWebServices` variant).
- Handle names by app: StudentVUE → `PXPWebServices`, TeacherVUE → `TXPWebServices`, AdminVUE → `AXPWebServices`, KioskVUE → `KXPWebServices`, HealthVUE → `HEALTHWEBSERVICES`, SEVUE → `SPECIALEDWEBSERVICES`, CounselVUE → `CounselorWebService`; help-desk lookups use `HDInfoServices` / `HDVueWebServices`.
- During the legacy API's deprecation the gate was per method: these config calls still work unauthenticated, while the student-data SOAP methods were the ones disabled.

### Unauthenticated config methods
[Top](#TOC)

Called by the app on cold start, before any login; all observed working with empty `userID`/`password`:

| `methodName` | `paramStr` | returns |
|---|---|---|
| `GetSupportedLanguages` | `&lt;Parms&gt;&lt;LanguageCode&gt;en&lt;/LanguageCode&gt;&lt;/Parms&gt;` | `<LanguageLists>` — `<Language Code="1" Name="English" EnglishDescription="English" />`, `Code="45"` Spanish, `Code="39"` Russian, … |
| `GETSAMLSTATUS` | *(empty)* | `<AllSAMLRecordData ShowLoginButtonForStudentVUE="false" ... />` — per-district SSO configuration |
| `GETACTIVATIONLINKSTATUS_PARENTVUE` | `&lt;Parms&gt;&lt;Parent&gt;0&lt;/Parent&gt;&lt;/Parms&gt;` | bare `true`/`false` — whether to show account activation |
| `SHOW_GET_FORGOT_PASSWORD_BUTTON_STATUS` | *(empty)* | bare `false`/`true` |
| `GETACKTEXT` | `&lt;Parms&gt;&lt;Parent&gt;0&lt;/Parent&gt;&lt;/Parms&gt;` (`1` for ParentVUE) | `<AckStatment PRIV_STMT="…">` — privacy acknowledgement text |

### Forgot password
[Top](#TOC)

`SHOW_GET_FORGOT_PASSWORD_UPDATE` (SOAP, unauthenticated, `skipLoginLog=1`) takes its `<Parms>` XML AES-encrypted through `getGpaE2` and base64-encoded into `paramStr`. Plaintext:

```xml
<Parms><UserName>…</UserName><Student>…</Student><Password>…</Password><Code>en</Code><LanguageCode>en</LanguageCode></Parms>
```

A bogus username returns `<RT_ERROR ERROR_MESSAGE="Error:  Please contact your school office for assistance." />` — no user-enumeration oracle. The JSON-side companion is `GetForgotPasswordEmailToken` (response key `twoFactorTokenData`).

### District lookup
[Top](#TOC)

Zip-code lookup against Edupoint central, as in [SOAP-API.md](SOAP-API.md) but wrapped in `ProcessWebServiceRequestMultiWeb` (handle `HDInfoServices`; `HDVueWebServices` for the help-desk variant):

```
paramStr = &lt;Parms&gt;&lt;Key&gt;5E4B7859-B805-474B-A833-FDB15D205D40&lt;/Key&gt;&lt;MatchToDistrictZipCode&gt;94127&lt;/MatchToDistrictZipCode&gt;&lt;/Parms&gt;
```

Returns `<DistrictLists><DistrictInfos><DistrictInfo DistrictID="" Name="…" Address="…" PvueURL="https://…/" /></DistrictInfos></DistrictLists>` (HTML-escaped in the result). `PvueURL` is the `<district>` host used everywhere else; `DistrictID` is the `DN` value the client can send as `?DN=`.

### Method catalog
[Top](#TOC)

All of these are JSON-API calls: `POST /api/v1/mobile/PXPWebServices/<Method>`. Request fields are the inner `request` object's fields, extracted from the app's generated typed client; defaults shown are the client's. **✅** = verified live against a district server; **◦** = from the client only.

| Method | Inner request fields | `data` key(s) | |
|--------|----------------------|---------------|--|
| `AttemptLogin` | `userID`, `password` (nulled in body), `userType`, `token`*, `solu`*, `decode`* | *(bare token object)* | ✅ |
| `RefreshToken` | *(none — empty body, Bearer refresh token)* | *(bare token object)* | ✅ |
| `GetChildListData` | `legacyAppRequest=false`, `secondaryLogin=false` | `children` | ✅ |
| `StudentClassList` | `childIntID`, `loadAllTerms`, `conSchOrgYearGU`, `conSchTermIndex`, `termIndex` (`"-1"` = all) | `studentClassSchedule`, `studentClassScheduleForAllTerms` | ✅ |
| `GetStudentClasesForGivenDay` | `childIntID`, `schDate` (`MM/DD/YYYY`), `dayType` | `todayScheduleInfo` | ✅ |
| `GetStudentClasesForGivenDayResponse` | same as above — the wire name really carries the `Response` suffix (and Edupoint's `Clases` typo) | `todayScheduleInfo` | ✅ |
| `GetStudentClassTime` | `childIntID` | `studentClassNow` | ✅ |
| `Gradebook` | `reportPeriod` (index from `reportingPeriods[].index`), `concurrentSchOrgYearGU` (from StudentClassList), `childIntID`, `languageCode` | `traditionalGradebook`, `standardsGradebook` | ✅ |
| `GetStudentAttendanceList` | `childIntID` | `dailyAttendance`, `periodAttendance` | ✅ |
| `GetStudentPastAttendanceData` | `childIntID` | `reportPastAtteendanceXML` *(sic)* | ✅ |
| `GetStudentInfoData` | `childIntID` | `studentInfoXML`, `studentInfoDetailXML` | ✅ |
| `GetCalendarData` | `childIntID`, optional date-window fields | `calendarListingData` | ✅ |
| `GetCalendarAssignmentDetails` | calendar event fields (`AGU`, `DGU`, `dguInternal`, `dgU2`, `viewType`, `addLinkData`, `dayType`) | `calendarAssignmentDetails` | ✅ |
| `GetStudentDocuments` | `childIntID`, `languageCode` | `studentDocuments` | ✅ |
| `GetStudentDocumentContent` | `childIntID`, `documentGU` | `studentAttachedDocumentData` (base64 PDF inline) | ◦ |
| `GetStudentHWNotes` | `childIntID`, `gu` | `gbhwNotesDatas` | ✅ |
| `UpdateStudentHWNotes` | `gbhwNotesUpdateData` | — | ◦ |
| `UpdateStudentGBLastCheckTime` | — | — | ◦ |
| `GetPXPContentMessage` | `childIntID` | `pxpMessagesData` | ✅ |
| `GetUserDefinedModule` | `childIntID`, `moduleIndex` | `allModuleRecordData` | ✅ |
| `GetFlexScheduleData` | `childIntID`, date fields | `studentFlexScheduleListingXML` | ◦ |
| `UpdateFlexSchedule` | `removeStudentFromSection=false`, section fields | — | ◦ |
| `GetSchoolInformationData` | `childIntID` | `studentSchoolInfoListing` | ✅ |
| `GetSchoolPayUrl` | — | payment-portal URL | ◦ |
| `GetSchoologoResponse` | *(none)* | `schoolAndDistrictLogo` (base64 images) | ✅ |
| `GetSoundFile` / `SaveSoundFile` | sound id / data | `soundFileData` | ◦ |
| `GenerateAuthToken` | *(session)* | `authToken` (SSO token for portal web-views) | ◦ |
| `GetAckData` | `processActivation=false` | `acctResult`, `ackStatmentData`, `parentOrStudentData` | ◦ |
| `GetAcknowledgementsData` | `childIntID` | `parentAcknowledgementMain` | ✅ |
| `GetAcknowledgementDetailsMobile` | acknowledgement id | `acknowledgement` | ◦ |
| `UpdateAckFromMyAccount` / `UpdateParentAcknowledgement` | `ackUpdateListing` | — | ◦ |
| `UpdateEmergencyResponse` | emergency contact answers | — | ◦ |
| `UpdateStudentAbsence` | `absenceReportListings`, `absenceReportPastList`, `reportingOption` | `requestResult` | ◦ |
| `UpdateAttachPhotoResponse` | `photoAttachDocumentData` | — | ◦ |
| `UpdateMyAccountData` | `pxpMobileUpdateMyAccountData` | — | ◦ |
| `GetContentMyAccountData` | `childIntID` | `pxpMyAccountData` | ✅ |
| `GetStudentDisciplineData` | `childIntID` | `studentDisciplineListing` | ◦ |
| `GetStudentFeeData` | `childIntID` | `studentFeeData` | ◦ |
| `GetStudentSpecialEdData` | `childIntID` | `specialEdData` | ◦ |
| `GetConferenceData` | `childIntID` | `studentConferenceData` | ◦ |
| `GetParentTeacherConferenceResponse` | conference fields | `conferenceDataList` | ◦ |
| `GetStudentsVideoMeeting` / `GetParentsVideoMeeting` | meeting fields | `meetingsForUserResponse`, `videoCallResponseModel` | ◦ |
| `GetHallPassData` | `getOnlyScheduedPases=false` *(sic)* | `studentHallPassXML` | ◦ |
| `GetHallPassHistory` | `onlyOverTimeLimit=false` | `passesData`, `statsData`, `summaryData` | ◦ |
| `GetHallPassSetup` | `childIntID` | `hallPassRoomSetupXML` | ✅ |
| `UpdateHallPass` | pass action fields | `studentHallPassXML` | ◦ |
| `GetHealthData` | `getDatahealthConditions=false`, `getDatahealthImmunizations=false`, `getDatahealthVisits=false` | `studentHealthData` | ◦ |
| `GetCounselorVisitBasicData` | `getPositionInLine=false` | `counselorVisiNthInLine` | ◦ |
| `GetLunchOrderInfoResponse` | `childIntID`, date | `lunchOrdersForStudent`, `lunchOrdersListForSchool`, `validSchoolDays` | ◦ |
| `UpdateLunchOrderInfoResponse` | `studentLunchOrder` | `result` | ◦ |
| `GetOLRInitialDataResponse` | `childIntID` | `olrInitialData` | ◦ |
| `GetOLRDocumentDownloadResponse` | `delete=false`, doc fields | `olrDocumentData` | ◦ |
| `UploadOLRDocumentUploadResponse` | `olrUploadDocumentData` | — | ◦ |
| `GetDownloadDocumentForSignatureResponse` | doc fields | `document` | ◦ |
| `UpdateDocumentSignatureResponse` | `docViewed=false`, `signPicDocumentData` | — | ◦ |
| `UploadDocumentForParentsResponse` | `studentDocumentUploadData` | — | ◦ |
| `UploadGBDocumentDataForStudentAssigment` | `gbDocumentDataObj` | — | ◦ |
| `UpdateDeviceToken` | push token, `reactNativeApp=false` | — (registers device for push) | ◦ |
| `UpdateNotificationPrefs` | `mobileUserSettings`, `notificationListing` | — | ◦ |
| `TestSystemCall` | *(none)* | connectivity smoke test (`data` is a bool) | ✅ |
| `GetSynergyMailGetConversations` | `pageToLoad=0` | `conversations`, `isLastPageLoaded`, `totalUnreadConversationMessages` | ◦ |
| `GetSynergyMailMessage` | message id fields | `synergyMailDataXML` | ◦ |
| `GetSynergyMailIGetMessageBody` | message id fields | `synergyMailMessageBodyXML` | ◦ |
| `GetSynergyMailGetAttachment` | attachment id fields | `attachmentXML` | ◦ |
| `GetSynergyMailInboxCount` | folder fields | `synergyMailInboxCountXML` | ◦ |
| `GetSynergyMailUnreadCount` | — | `messageCount` | ✅ |
| `GetSynergyMailGetContactList` | — | `contactGroupList` | ◦ |
| `GetSynergyMailGetSchoolList` | — | `organizationList` | ◦ |
| `GetSynergyMailGetStaffList` | — | `organizationStaffList` | ◦ |
| `GetSynergyMailGetStudentList` | — | `organizationStudentList` | ◦ |
| `GetSynergyMailGetTeacherList` | — | `studentClassScheduleForAllTerms` | ◦ |
| `GetSynergyMailRecipientSearch` | search fields | `studentCounselorInfo`, `studentGroupInfoDatas`, `studentInfoList` | ◦ |
| `GetSynergyMailRecipientAddressing` | `to`, `cc`, `bcc` | `to`, `cc`, `bcc`, `invalidRecipients` | ◦ |
| `GetSynergyMailSaveNewMessage` | `synergyEmailListing` | — | ◦ |
| `GetSynergyMailSaveReadOrDeleteMsg` | `synergyEmailMarkList` | — | ◦ |
| `GetSynergyMailMoveMessage` | message/folder fields | `synergyEmailSuccessMessage` | ◦ |
| `GetSynergyMailUpdateFolder` | `delete=false`, folder fields | `folderListViewXML` | ◦ |
| `GetSynergyMailUpdateSignatures` | `synergyMailSignatureXML` | — | ◦ |
| `GetForgotPasswordEmailToken` | account fields | `twoFactorTokenData` | ◦ |
| `ForceChangePassword` | `isStudent=false`, `oldApp=false`, credentials | `pxpForceChangePasswordResult` | ◦ |

\* SAML/SSO re-entry only.

### Examples
[Top](#TOC)

One section per method, in the order of the [method catalog](#method-catalog). Every request is `POST /api/v1/mobile/PXPWebServices/<Method>` with the bearer token; only the inner `request` object and the `data` payload are shown. Values are anonymized; `N`/`NN` stand for numbers and `H:MM` for clock times so district-specific schedules aren't leaked.

#### GetChildListData

```json
{"arguments":{"request":"{\"legacyAppRequest\":false,\"secondaryLogin\":false}"}}
```
→ `data.children` (trimmed):
```json
{
  "districtName": "<District Name>",
  "districtRootURL": "https://<district>.edupoint.com/api/v1/mobile/PXPWebServices/",
  "appVersion": "…", "mobileClientTimeout": NN,
  "showGradeBookModule": true, "showAttendanceModule": true,
  "showSynergyMailModule": true, "showDisciplineModule": false,
  "showHealthVisitModule": false, "…": "…",
  "acknowledgementsPresent": false,
  "childrenList": [
    {"childIntID": 0, "studentGU": "<GUID>", "studentSSY": "<GUID>",
     "childName": "<Student Name>", "childFirstName": "<First Name>",
     "childPermID": "<id>", "ID": "<id>", "orgYearGU": "<GUID>",
     "organizationName": "<School Name>", "grade": "NN",
     "accessGU": "<GUID>", "photo": "<base64>", "events": null,
     "concurrentSchools": [],
     "supportingFutureAttendance": false, "supportingPastAttendance": false,
     "showArriveLate": true, "showByClass": true, "showLeaveEarly": true,
     "daysInFutureToAcceptAttendance": NN, "daysInPastToAcceptAttendance": NN,
     "attendanceReasonForFutureAtt": [
       {"reasonGU": "<GUID>", "reasonType": 6, "description": "Illness",
        "reasonTypeIcon": "<i class=\"fa att-icon\" data-type=\"EXC\"></i>"}
     ],
     "attendanceInstText": "<instructions shown on the report-absence form>",
     "counselorName": null, "hallPassStatus": "", "hallPassCountToday": 0,
     "studentAttendanceType": 1,
     "allModules": [
       {"name": "Synergy Mail", "module": "21", "isEnabled": "Y",
        "iconUrl": "Images/PXP/ModuleIcons/icon_Messages.png",
        "moduleUrl": "PXP2_Messages.aspx", "moduleOrder": 0.0,
        "pxpModuleCfgGU": null, "organizationYearGU": null}
     ]}
  ]}
```

This is the app's boot call and doubles as the district configuration dump: dozens of `show*Module`/`supporting*` flags, per-student attendance-reporting settings, and the district's enabled modules in `children.allModules` (also copied per child) — useful for deciding which calls to attempt. The student entry key is **`childrenList`**. Child selection is a parameter (`childIntID`), not a stateful step — there is no "select child" call; `0` is the logged-in student on StudentVUE. Don't confuse `childIntID` (request ordinal) with `studentGU` (response GUID).

#### StudentClassList

```json
{"arguments":{"request":"{\"childIntID\":0,\"loadAllTerms\":true,\"conSchOrgYearGU\":\"\",\"conSchTermIndex\":\"-1\",\"termIndex\":\"-1\"}"}}
```
→ `data.studentClassScheduleForAllTerms` (trimmed):
```json
{
  "termIndex": 0,
  "termIndexName": "Semester 1",
  "termLists": [
    {"termIndex": 0, "termCode": 1, "termName": "Semester 1",
     "beginDate": "MM/DD/YYYY", "endDate": "MM/DD/YYYY",
     "schoolYearTrmCodeGU": "<GUID>", "schoolName": "<School Name>",
     "orgYearGU": "<GUID>", "termDefCodes": [{"termDefName": "S1"}, {"termDefName": "FY"}]}
  ],
  "studentClassScheduleForTerms": [
    {"thisTermIndex": 0, "beginDate": "MM/DD/YYYY", "endDate": "MM/DD/YYYY",
     "orgYearGU": "<GUID>",
     "classLists": [
       {"period": "N", "courseTitle": "<Course Title>", "roomName": "<Room>",
        "teacher": "<Teacher Name>", "teacherEmail": "<teacher@example.com>",
        "sectionGU": "<GUID>", "teacherStaffGU": "<GUID>",
        "meetingDays": null, "excludePVUE": false,
        "additionalStaffInformation": [], "additionalStaffInformationXMLs": []}
     ]}
  ],
  "concurrentSchoolStudentClassScheduleForAllTermss": []
}
```

With `loadAllTerms: true` classes live under `studentClassScheduleForAllTerms.studentClassScheduleForTerms[].classLists[]`. With `loadAllTerms: false` the same call returns `data.studentClassSchedule` — a flat `classLists` for the selected `termIndex` plus today's bell times:

```json
{"studentClassSchedule": {
  "termIndex": 0, "termIndexName": "Semester 1", "errorMessage": "",
  "includeAdditionalStaffWhenEmailingTeachers": false,
  "classLists": [
    {"period": "N", "courseTitle": "<Course Title>", "roomName": "<Room>",
     "teacher": "<Teacher Name>", "teacherEmail": "<teacher@example.com>",
     "sectionGU": "<GUID>", "teacherStaffGU": "<GUID>",
     "meetingDays": null, "excludePVUE": false,
     "additionalStaffInformation": [], "additionalStaffInformationXMLs": []}
  ],
  "termLists": ["…same term objects as above…"],
  "todayScheduleInfoData": {"date": "M/D/YYYY", "schoolInfos": [
    {"schoolName": "<School Name>", "bellSchedName": "",
     "classes": [
       {"period": "NN", "className": "<Course Title> - <Section ID>",
        "startTime": "H:MM AM", "endTime": "H:MM AM",
        "startDate": "MM/DD/YYYY H:MM:SS AM", "endDate": "MM/DD/YYYY H:MM:SS AM",
        "roomName": "<Room>",
        "teacherName": "<Teacher Name>", "teacherEmail": "<teacher@example.com>",
        "staffGU": "<GUID>", "sectionGU": "<GUID>",
        "emailSubject": "RE: Period NN, Section <Section ID>",
        "teacherURL": "<HTML snippet with SMApp.composeEx(...) mailto handlers>",
        "classURL": "", "attendanceCode": "", "hideClassStartEndTime": false}
     ]}]},
  "concurrentSchoolStudentClassSchedules": []}}
```

Handle both shapes. `orgYearGU` here is the value `Gradebook` wants as `concurrentSchOrgYearGU`. `todayScheduleInfoData` is the only reliable source of bell times — see the `GetStudentClasesForGivenDay` notes for why. `teacherURL` is an HTML fragment embedding JavaScript `SMApp.composeEx({to: [{RecipientList: 0, GU: "<GUID>"}], subject: "…", messageText: ""})` calls for Synergy Mail compose; `staffGU`/`emailSubject` carry the same data in usable form.

#### GetStudentClasesForGivenDay / GetStudentClasesForGivenDayResponse

Two names for the same dedicated "today's classes" call; the app uses the `Response`-suffixed one.

```json
{"arguments":{"request":"{\"childIntID\":0,\"schDate\":\"MM/DD/YYYY\",\"dayType\":0}"}}
```
→ `data.todayScheduleInfo`:
```json
{"date": "M/D/YYYY", "dateToLoad": "YYYY-MM-DDT00:00:00-07:00",
 "attendance": null, "schools": []}
```

Reproducibly `attendance: null, schools: []` mid-class on a regular school day — across both method names, both `dayType` values (normal/alternate flex schedules), and arbitrary `schDate` values; the response always echoes the current day, so `schDate` appears to be ignored. Treat empty `schools` as "no data", not "no school". The `date` fields use `M/D/YYYY` (no zero-padding), while `dateToLoad` is ISO-8601 with the local UTC offset. Get bell times from `StudentClassList`'s `todayScheduleInfoData` instead.

#### GetStudentClassTime

```json
{"arguments":{"request":"{\"childIntID\":0}"}}
```
→ `data.studentClassNow` (trimmed):
```json
{
  "period": "N", "courseTitle": "<Course Title>", "sectionID": "<Section ID>",
  "room": "<Room>", "staffName": "<Teacher Name>",
  "startTime": null, "endtime": null,
  "minutesRemainingToEndClass": "N", "minutesAfterClassStart": "NN",
  "resultCode": 1,
  "currentClass": "Period: N,  Course Title: <Course Title>,  Section ID: <Section ID>, Room: <Room>,  Staff Name: <Teacher Name>,  All Day Code: Present"
}
```

`currentClass` is a pre-rendered human-readable summary (it embeds today's attendance code); build your own UI from the individual fields, not by parsing it. `startTime`/`endtime` stay `null` even mid-class; the minute counters are strings. Outside school hours every class field is `null` and `resultCode` != 0 (4 = nothing found) with a message in `currentClass`, e.g. `"For the current day, no Schedule Information was found for the selected student."`

#### Gradebook

```json
{"arguments":{"request":"{\"reportPeriod\":\"\",\"concurrentSchOrgYearGU\":\"\",\"childIntID\":0,\"languageCode\":\"en\"}"}}
```
→ `data.traditionalGradebook` (trimmed):
```json
{
  "type": "Traditional",
  "errorMessage": null,
  "hideStandardGraphInd": false,
  "hideMarksColumnElementary": false,
  "hidePointsColumnElementary": false,
  "hidePercentSecondary": false,
  "displayStandardsData": false,
  "gbStandardsTabDefault": false,
  "reportingPeriods": [
    {"index": "0", "gradePeriod": "<Semester 1 Mid-Term>", "startDate": "M/D/YYYY", "endDate": "M/D/YYYY"},
    {"index": "1", "gradePeriod": "<Semester 1>", "startDate": "M/D/YYYY", "endDate": "M/D/YYYY"}
  ],
  "reportingPeriod": {"index": "0", "gradePeriod": "<Semester 1 Mid-Term>", "startDate": "M/D/YYYY", "endDate": "M/D/YYYY"},
  "courses": [
    {"period": "N", "title": "<Course Title> (<Section ID>)", "courseName": "<Course Title>", "courseID": "<Section ID>",
     "room": "<Room>", "staff": "<Teacher Name>", "staffEMail": "<teacher@example.com>",
     "staffGU": "<GUID>", "imageType": "social",
     "highlightPercentageCutOffForProgressBar": NN, "usesRichContent": false,
     "marks": [
       {"markName": "S1MT", "shortMarkName": "S1MT",
        "calculatedScoreString": "<grade>", "calculatedScoreRaw": "NN.N",
        "standardViews": [],
        "gradeCalculationSummary": [
          {"type": "Classwork", "weight": "NN%", "points": "NN.NN", "pointsPossible": "NN.NN",
           "weightedPct": "NN.NN%", "calculatedMark": "<grade>"},
          {"type": "Assessment", "weight": "NN%", "points": "0.00", "pointsPossible": "0.00",
           "weightedPct": "0.00%", "calculatedMark": "0"},
          {"type": "TOTAL", "weight": "100%", "points": "NN.NN", "pointsPossible": "NN.NN",
           "weightedPct": "100.00%", "calculatedMark": "<grade>"}
        ],
        "assignments": [
          {"gradebookID": NN, "measure": "<Assignment Title>", "type": "Classwork",
           "date": "M/D/YYYY", "dueDate": "M/D/YYYY",
           "score": "N", "displayScore": "N out of N", "scoreCalValue": "N", "scoreMaxValue": "N",
           "scoreType": "Raw Score", "points": "N / N", "point": "N", "pointPossible": "N",
           "timeSincePost": "Nd", "totalSecondsSincePost": NNNNNN.0,
           "notes": "", "measureDescription": "",
           "teacherID": NN, "studentID": NNNNN,
           "hasDropBox": false, "dropStartDate": "M/D/YYYY", "dropEndDate": "M/D/YYYY",
           "resources": [], "standards": []}
        ],
        "assignmentsSinceLastAccess": []}
     ]}
  ],
  "standardsGradebook": null
}
```

Assignments are inline in `courses[].marks[].assignments[]` — no second fetch. The quarter is a request parameter: valid `reportPeriod` values come from `reportingPeriods[].index`, so a full year takes one call per quarter. `standardsGradebook` is a second mode some districts use. `assignmentsSinceLastAccess` reflects per-account read state tracked by the server.

Field quirks: mark names can be mid-term markers (`S1MT`), not just final-term codes; `calculatedScoreRaw` is a string; `totalSecondsSincePost` is a float; all score fields are duplicated in several forms (`score`/`displayScore`/`points`/`point`…) with `scoreType` distinguishing `Raw Score` from letter/percent grades; `gradebookID` here is the same id the calendar uses as `DGU`. Numeric lookups (`gradebookID`, `teacherID`, `studentID`) are numbers, not strings. If a mark has no weighted categories `gradeCalculationSummary` is a list with just the `TOTAL` row.

#### GetStudentAttendanceList

```json
{"arguments":{"request":"{\"childIntID\":0}"}}
```
→ `data.dailyAttendance` can be `null`, with `data.periodAttendance` carrying everything:
```json
{
  "type": "Period", "startPeriod": 0, "endPeriod": NN, "periodCount": NN,
  "schoolName": "<School Name>",
  "absences": [
    {"absenceDate": "MM/DD/YYYY", "reason": "", "reason2": null,
     "note": "<Parent note text>", "dailyIconName": "",
     "codeAllDayReasonType": "", "codeAllDayDescription": "",
     "periods": []},
    {"absenceDate": "MM/DD/YYYY", "reason": "<Reason>", "reason2": null,
     "note": "<Parent note text>", "dailyIconName": "icon_excused.gif",
     "codeAllDayReasonType": "icon_excused.gif", "codeAllDayDescription": "<Reason>",
     "periods": [
       {"number": "N", "name": "", "note": "", "reason": "",
        "course": "<Course Title>", "staff": "<Teacher Name>",
        "staffEMail": "<teacher@example.com>", "iconName": "",
        "schoolName": "<School Name>", "staffGU": "<GUID>", "orgYearGU": "<GUID>"}
     ]}
  ],
  "totalExcused":   [{"number": N, "total": N}, {"number": N, "total": N}, {"...": "..."}],
  "totalTardies":   [{"number": N, "total": N}, {"...": "..."}],
  "totalUnexcused": [{"number": N, "total": N}, {"...": "..."}],
  "totalActivities": [{"number": N, "total": N}, {"...": "..."}],
  "totalUnexcusedTardies": [{"number": N, "total": N}, {"...": "..."}],
  "concurrentSchoolsLists": []
}
```

The `total*` arrays have one `{number, total}` entry per period. An absence with an empty `periods` array is a pending/not-yet-verified entry. Whole-year history is a separate call, `GetStudentPastAttendanceData` (response key `reportPastAtteendanceXML` — Edupoint's spelling); schools that don't expose it return an error:

#### GetStudentPastAttendanceData

```json
{"arguments":{"request":"{\"childIntID\":0}"}}
```
→
```json
{"error": {"code": "400",
           "message": "Attendance data not available for this school",
           "stackTrace": null},
 "data": null}
```

#### GetStudentInfoData

```json
{"arguments":{"request":"{\"childIntID\":0}"}}
```
→ `data.studentInfoXML` can be `null`; `data.studentInfoDetailXML` carries the demographics. All PII — key list only:
```json
{"type": "Detail", "formattedName": "<Student Name>", "permID": "<id>",
 "gender": "<…>", "grade": "<…>", "address": "<…>", "lastNameGoesBy": "…",
 "nickName": "…", "birthDate": "<…>", "eMail": "<…>", "phone": "<…>",
 "homeLanguage": "…", "currentSchool": "<School Name>", "track": "…",
 "homeRoomTch": "<Teacher Name>", "homeRoomTchEMail": "<teacher@example.com>",
 "homeRoomTchStaffGU": "<GUID>", "orgYearGU": "<GUID>", "homeRoom": "<Room>",
 "counselorName": "<Counselor Name>", "counselorEmail": "<counselor@example.edu>",
 "counselorStaffGU": "<GUID>", "photo": "<base64>",
 "emergencyContacts": ["…"], "physician": {"name": "…", "hospital": "…", "phone": "…", "extn": "…"},
 "dentist": {"name": "…", "office": "…", "phone": "…", "extn": "…"},
 "userDefinedGroupBoxes": ["…"], "lockerInfoRecords": [],
 "studentBusAssignments": ["…"],
 "showStudentBusAssignmentInfo": false, "showPhysicianAndDentistInfo": false,
 "showStudentInfo": true, "showFrontLineSpedURL": false,
 "showFrontLine504URL": false, "showFrontLineParentPortalURL": false}
```

Both keys are JSON objects despite the `XML` names. `userDefinedGroupBoxes` holds district-configured extra fields (`UserDefinedGroupBox.GroupBoxLabel` + `UserDefinedItems[].ItemLabel`/`Value`).

#### GetCalendarData

```json
{"arguments":{"request":"{\"childIntID\":0}"}}
```
→ `data.calendarListingData` (trimmed):
```json
{
  "schoolBegDate": "MM/DD/YYYY", "schoolEndDate": "MM/DD/YYYY",
  "monthBegDate": "MM/DD/YYYY", "monthEndDate": "MM/DD/YYYY",
  "eventLists": [
    {"date": "MM/DD/YYYY", "title": "First Day of the School", "icon": null,
     "AGU": null, "dayType": 0, "startTime": "", "link": null,
     "DGU": null, "dguInternal": null, "dgU2": null,
     "viewType": null, "addLinkData": null, "evtDescription": null},
    {"date": "MM/DD/YYYY", "title": "Holiday", "icon": null,
     "AGU": null, "dayType": 1, "startTime": "All Day", "link": null,
     "DGU": null, "dguInternal": null, "dgU2": null,
     "viewType": null, "addLinkData": null, "evtDescription": null},
    {"date": "MM/DD/YYYY",
     "title": "<Teacher Name>  <Course Title>(<period>) : <Assignment Title>  - Score: NN.NN",
     "icon": "assignment.png",
     "AGU": "0", "dayType": 2, "startTime": "", "link": "ASSIGNMENTS",
     "DGU": "NNNNNN", "dguInternal": "NNNNNN", "dgU2": null,
     "viewType": "2", "addLinkData": "<GUID>", "evtDescription": null}
  ]
}
```

Called with just `childIntID` the server returns the current month window. Mid-semester the list mixes three event kinds — school events, holidays, and gradebook assignments (`period` inside a title is the class period). `dayType` doubles as an event-kind discriminator here: `0` plain school event, `1` no-school day, `2` assignment. On assignment events `DGU`/`dguInternal` is the gradebook assignment id (equal to `Gradebook`'s `assignments[].gradebookID`) and `addLinkData` is the section `GUID` — the inputs for `GetCalendarAssignmentDetails`. Assignment `title`s already embed the score; there is no separate score field.

#### GetCalendarAssignmentDetails

Pass a calendar assignment event's fields through:

```json
{"arguments":{"request":"{\"childIntID\":0,\"AGU\":\"0\",\"DGU\":\"NNNNNN\",\"dguInternal\":\"NNNNNN\",\"dgU2\":null,\"viewType\":\"2\",\"addLinkData\":\"<GUID>\",\"dayType\":2}"}}
```
→ `data.calendarAssignmentDetails`:
```json
{
  "classGU": null, "assignment": null,
  "hideStandardGraphInd": false, "hideMarksColumnElementary": false,
  "hidePointsColumnElementary": false, "displayStandardsData": false,
  "assignmentEventDetailLists": []
}
```

The container comes back with `assignmentEventDetailLists: []` for past assignments; the exact input combination that populates it is still unknown.

#### GetStudentDocuments

```json
{"arguments":{"request":"{\"childIntID\":0,\"languageCode\":\"en\"}"}}
```
→ `data.studentDocuments` (trimmed):
```json
{
  "showDateColumn": true, "showDocNameColumn": true, "showDocCatColumn": true,
  "studentGU": "<GUID>", "studentSSY": "<GUID>",
  "changesPending": false, "pendingChangeDate": null, "pendingChangesMessage": null,
  "studentDocumentDatas": [
    {"documentGU": "<GUID>", "documentFileName": "<GUID>.pdf",
     "documentDate": "MM/DD/YYYY", "documentType": "Report Card",
     "studentGU": "<GUID>", "documentComment": "<School Year> Sem 1 Final Mark"},
    {"documentGU": "<GUID>", "documentFileName": "<GUID>.pdf",
     "documentDate": "MM/DD/YYYY", "documentType": "Unofficial Transcript",
     "studentGU": "<GUID>", "documentComment": "Transcript <School Year>"},
    {"documentGU": "<GUID>", "documentFileName": "<GUID>.pdf",
     "documentDate": "MM/DD/YYYY", "documentType": "Course History",
     "studentGU": "<GUID>", "documentComment": "Grad Profile <School Year>"}
  ],
  "documentSetupDatas": [],
  "documentsDiv": "…", "directions": "…"
}
```

`documentFileName` is a server-side GUID-named file, not the human title — the display name comes from `documentType`/`documentComment`. `documentType` values include: Report Card, Unofficial Transcript, Course History, Test Report, Parent Letter, attendance letters, surveys.

Fetch: `GetStudentDocumentContent` with `{"childIntID":0,"documentGU":"<GUID>"}` → `data.studentAttachedDocumentData.documentDatas[]`:

```json
{"documentGU": "<GUID>", "studentGU": "<GUID>", "docDate": "MM/DD/YYYY",
 "fileName": "<GUID>.pdf", "category": "<category code>", "notes": "<comment>",
 "docType": "PDF", "base64Code": "JVBERi0xLjQKJ…",
 "gbStudentID": null, "gbTeacherID": null, "gbGradeBookID": null}
```

The PDF is inline base64 in `base64Code` (decodes to `%PDF-…`) — no URL, no second host. The `gb*` fields suggest gradebook attachments ride the same envelope.

#### GetStudentHWNotes

```json
{"arguments":{"request":"{\"childIntID\":0,\"gu\":\"\"}"}}
```
→ `data.gbhwNotesDatas`:
```json
{"studentGU": "<GUID>", "sisNumber": "<id>", "studentSSY": "<GUID>", "gbHomeWorkNotesRecords": []}
```

`gu` selects a section (GUID from the schedule); empty returns the container only. Writing is `UpdateStudentHWNotes` with `gbhwNotesUpdateData`.

#### GetPXPContentMessage

```json
{"arguments":{"request":"{\"childIntID\":0}"}}
```
→ `data.pxpMessagesData` (trimmed):
```json
{
  "supportingSynergyMail": true,
  "messageListings": [],
  "synergyMailMessageListingByStudents": [
    {"studentGU": "<GUID>",
     "synergyMailMessageListings": [
       {"attachmentDatas": [], "iconURL": "images/PXP/", "ID": null,
        "beginDate": "MM/DD/YYYY 00:00:00", "type": 1,
        "subject": "Progress report period '<Term>' is ending on MM/DD/YYYY",
        "content": null, "endDate": null,
        "read": false, "deletable": true, "from": null,
        "subjectNoHTML": "Progress report period '<Term>' is ending on MM/DD/YYYY",
        "module": 7, "email": null, "staffGU": null, "smMsgPersonGU": null},
       {"attachmentDatas": [], "iconURL": "images/PXP/", "ID": null,
        "beginDate": "MM/DD/YYYY", "type": 1,
        "subject": "Attendance notes for MM/DD/YYYY",
        "content": null, "endDate": null,
        "read": false, "deletable": true, "from": null,
        "subjectNoHTML": "Attendance notes for MM/DD/YYYY",
        "module": 1, "email": null, "staffGU": null, "smMsgPersonGU": null}
     ]}]}
```

District/school alert messages. `messageListings` is the legacy shape (empty here); live messages arrive under `synergyMailMessageListingByStudents[]`, grouped per student. `module` identifies the emitting module (`7` = gradebook progress-report notices, `1` = attendance notes). `ID`/`from`/`content` can all be `null` for auto-generated notices. Replaces the SOAP `GetPXPMessages`; message attachments are fetched through the mail family below.

#### GetUserDefinedModule

```json
{"arguments":{"request":"{\"childIntID\":0,\"moduleIndex\":0}"}}
```
→ `data.allModuleRecordData`:
```json
{"moduleRecords": []}
```

Empty when the district has no user-defined module content configured.

#### GetSchoolInformationData

```json
{"arguments":{"request":"{\"childIntID\":0}"}}
```
→ `data.studentSchoolInfoListing` (trimmed):
```json
{
  "school": "<School Name>", "principal": "<Principal Name>",
  "schoolAddress": "<Street Address>", "schoolAddress2": "",
  "schoolCity": "<City>", "schoolState": "<ST>", "schoolZip": "<ZIP>",
  "phone": "<phone>", "phone2": "<phone>", "URL": "<school website>",
  "principalEmail": "<principal@example.edu>", "principalGu": "<GUID>",
  "staffLists": [
    {"name": "<Staff Name>", "eMail": "<staff@example.edu>",
     "title": "HS TEACHER", "phone": "", "extn": "", "staffGU": "<GUID>"},
    {"name": "<Staff Name>", "eMail": "<staff@example.edu>",
     "title": "HS SECRETARY OFFICE", "phone": "<phone>", "extn": "", "staffGU": "<GUID>"}
  ]}
```

A full staff directory — hundreds of entries at a large school, all teachers included with their `staffGU` (matching the schedule's `teacherStaffGU`). Titles are raw Synergy position codes (`HS TEACHER`, `HS SECRETARY OFFICE`, `HS SPED PARAEDUC`, …).

#### GetContentMyAccountData

```json
{"arguments":{"request":"{\"childIntID\":0}"}}
```
→ `data.pxpMyAccountData` (trimmed) — the account holder's contact/notification settings. Contains the student's name, address, phone and e-mail (all PII):
```json
{
  "formattedName": "<Student Name>",
  "userID": "<id>",
  "homeAddress": "<Street Address><br><City>, <ST> <ZIP>",
  "mailAddreess": "Same as Home Address",
  "phoneNumbers": "C: <phone><br>* <i>* Indicates primary contact phone</i>",
  "adultID": null,
  "canEditParentDemographicData": false,
  "enableParentEmployerUpdates": false,
  "enableParentPrimaryLanguageUpdates": false,
  "enableParentNameUpdates": false,
  "firstName": null, "lastName": null, "employer": null,
  "primaryLanguageCode": null, "primaryLanguage": null,
  "eMail": "<student e-mail>",
  "eMail1": null, "eMail2": null, "eMail3": null, "eMail4": null, "eMail5": null,
  "eMailEnabled": false, "eMailVisible": false,
  "hidePaperlessReportcard": true, "paperlessReportcardSetting": false,
  "supporting_Email_Notification_ForStudentVUE": true,
  "chkNotifyAttendance": false, "chkNotifyAttendanceEnabled": false,
  "chkNotifyGrade": false, "chkNotifyGradeEnabled": false,
  "chkNotifyGradebook": false, "chkNotifyGradebookEnabled": false,
  "chkNotifyDiscipline": false, "chkNotifyHealth": false,
  "showNotificationAttendance": false,
  "showNotificationAttendanceEmail": false, "showNotificationAttendanceSMS": false, "showNotificationAttendanceVoice": false,
  "showNotificationGrades": false,
  "showNotificationGradesEmail": false, "showNotificationGradesSMS": false, "showNotificationGradesVoice": false,
  "showNotificationAssignment": false,
  "showNotificationAssignmentEmail": false, "showNotificationAssignmentSMS": false, "showNotificationAssignmentVoice": false,
  "…": "…"
}
```

Field groups: `mailAddreess` is Edupoint's spelling; addresses/phones are `<br>`-separated HTML with a `*` primary marker; each `chkNotify*` toggle is paired with a `chkNotify*Enabled` flag and `showNotification*Email`/`SMS`/`Voice` variants; `eMail`…`eMail5` each have `Enabled`/`Visible` flags; the rest are self-edit permissions (`canEditParentDemographicData`, `*UpdatePermission`) and misc settings.

#### GetAcknowledgementsData

```json
{"arguments":{"request":"{\"childIntID\":0}"}}
```
→ `data.parentAcknowledgementMain`:
```json
{"parentAcknowledgementDatas": []}
```

Empty outside signature windows.

#### GetHallPassSetup

```json
{"arguments":{"request":"{\"childIntID\":0}"}}
```
→ `data.hallPassRoomSetupXML` (a JSON object despite the name):
```json
{"hallPassMaxDaysForFuturePass": "NN", "hallPassCountUp": false,
 "allowStudentsToEndHallPass": false, "hallPassRoomTypes": []}
```

Returned even where the pass calls fail (see below); empty `hallPassRoomTypes` means the feature has no rooms configured. The rest of the family — `GetHallPassData` (`getOnlyScheduedPases`, *sic*), `GetHallPassHistory` (`onlyOverTimeLimit`), `UpdateHallPass` — is district-dependent and often disabled.

#### GetHealthData

```json
{"arguments":{"request":"{\"getDatahealthConditions\":false,\"getDatahealthImmunizations\":false,\"getDatahealthVisits\":false}"}}
```
→
```json
{"error": {"code": "500",
           "message": "Error:  Please contact your school office for assistance. (ID: XXXXX)",
           "stackTrace": null},
 "data": null}
```

The three booleans select the sections of `studentHealthData`; districts gate this heavily, and the generic `500` is what closed gates look like.

#### GetStudentDisciplineData / GetStudentFeeData

```json
{"arguments":{"request":"{\"childIntID\":0}"}}
```
→ both return the module-disabled error with their own module name:
```json
{"error": {"code": "400",
           "message": "2100 - School District has not enabled access for the Discipline Module.",
           "stackTrace": null},
 "data": null}
```
```json
{"error": {"code": "400",
           "message": "2100 - School District has not enabled access for the Fees Module.",
           "stackTrace": null},
 "data": null}
```

#### GetSynergyMailUnreadCount

```json
{"arguments":{"request":"{}"}}
```
→ `data.messageCount`:
```json
{"error": null, "data": {"messageCount": 1}}
```

The whole mail stack is a `GetSynergyMail*` / `UpdateSynergyMail*` family (see the [method catalog](#method-catalog)): compose goes `GetSynergyMailRecipientSearch` / `GetSynergyMailRecipientAddressing` → `GetSynergyMailSaveNewMessage`; read/delete `GetSynergyMailSaveReadOrDeleteMsg`; move `GetSynergyMailMoveMessage`; folders `GetSynergyMailUpdateFolder`; signatures `GetSynergyMailUpdateSignatures`; inbox counters `GetSynergyMailInboxCount` and this method; address books `GetSynergyMailGetContactList`/`GetSchoolList`/`GetStaffList`/`GetStudentList`/`GetTeacherList` (teachers also come from the schedule — `GetSynergyMailGetTeacherList` returns `studentClassScheduleForAllTerms`). Don't assume the whole family works because one member does — see below.

#### GetSynergyMailGetConversations

```json
{"arguments":{"request":"{\"pageToLoad\":0}"}}
```
→
```json
{"error": {"code": "500",
           "message": "Error:  Please contact your school office for assistance. (ID: XXXXX)",
           "stackTrace": null},
 "data": null}
```

Even with mail enabled (`pxpMessagesData.supportingSynergyMail: true`, unread count above returning `1`), the conversations/address-book calls can fail with the generic `500` — including `GetSynergyMailInboxCount` and the `GetSynergyMailGet*List` family. The `(ID: XXXXX)` suffix is a server-side event ID for the district's support desk; it varies per failure.

#### TestSystemCall

```json
{"arguments":{"request":"{}"}}
```
→ `data` is a bare boolean:
```json
{"error": null, "data": true}
```

Connectivity smoke test; no payload beyond the boolean.
