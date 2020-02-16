## StudentVue App API Docs

Documentation and research of the API routes from the Official StudentVue App.

### Related Projects

[kajchang/StudentVue](https://github.com/kajchang/StudentVue) - unofficial Python implementation of the web API

[kajchang/StudentVueDistrictFinder](https://github.com/kajchang/StudentVueDistrictFinder) - implements zip code finding and a dump of brute forced districts

### TOC
[Getting Zip Codes](#getting-zip-codes)

### Getting Zip Codes
[Top](#TOC)

Example Request:
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

Example Response:
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

Description:

Uses a system account (`<userID>EdupointDistrictInfo</userID><password>Edup01nt</password>`) and a provided zip code (`&lt;MatchToDistrictZipCode&gt;94127&lt;/MatchToDistrictZipCode&gt;`) and returns nearby schools. The system account could have interesting privileges.
