< !DOCTYPE
html >
< html
lang = "en" >
< head >
< meta
charset = "UTF-8" >
< meta
name = "viewport"
content = "width=device-width, initial-scale=1.0" >
< title > Query
Management
System < / title >
< link
rel = "stylesheet"
href = "style.css" >
< script
src = "https://cdn.jsdelivr.net/npm/chart.js" > < / script >
< / head >
< body >
< div


class ="container" >

< header >
< h1 >📧 Query
Management
System < / h1 >
< p > Unified
Inbox
for All Customer Queries < / p >
< / header >

< nav


class ="navbar" >

< button


class ="nav-btn active" onclick="showSection('dashboard')" > Dashboard < / button >

< button


class ="nav-btn" onclick="showSection('queries')" > All Queries < / button >

< button


class ="nav-btn" onclick="showSection('analytics')" > Analytics < / button >

< button


class ="nav-btn" onclick="showSection('new-query')" > New Query < / button >

< / nav >

< !-- Dashboard
Section -->
< section
id = "dashboard"


class ="section active" >

< div


class ="stats-grid" >

< div


class ="stat-card" >

< h3 >📥 Total
Queries < / h3 >
< div
id = "total-queries"


class ="stat-number" > 0 < / div >

< / div >
< div


class ="stat-card" >

< h3 >⏰ Avg
Response
Time < / h3 >
< div
id = "avg-response"


class ="stat-number" > 0h < / div >

< / div >
< div


class ="stat-card" >

< h3 >✅ Resolved < / h3 >
< div
id = "resolved-queries"


class ="stat-number" > 0 < / div >

< / div >
< div


class ="stat-card" >

< h3 >🚨 High
Priority < / h3 >
< div
id = "high-priority"


class ="stat-number" > 0 < / div >

< / div >
< / div >

< div


class ="charts-grid" >

< div


class ="chart-card" >

< h3 >📊 Queries
by
Category < / h3 >
< canvas
id = "categoryChart" > < / canvas >
< / div >
< div


class ="chart-card" >

< h3 >🔄 Queries
by
Status < / h3 >
< canvas
id = "statusChart" > < / canvas >
< / div >
< / div >

< div


class ="recent-queries" >

< h3 >🕒 Recent
Queries < / h3 >
< div
id = "recent-queries-list" > < / div >
< / div >
< / section >

< !-- All
Queries
Section -->
< section
id = "queries"


class ="section" >

< h2 >📋 All
Customer
Queries < / h2 >
< div


class ="filters" >

< select
id = "status-filter"
onchange = "loadQueries()" >
< option
value = "all" > All
Status < / option >
< option
value = "new" > New < / option >
< option
value = "in-progress" > In
Progress < / option >
< option
value = "resolved" > Resolved < / option >
< / select >
< select
id = "priority-filter"
onchange = "loadQueries()" >
< option
value = "all" > All
Priority < / option >
< option
value = "3" > High < / option >
< option
value = "2" > Medium < / option >
< option
value = "1" > Low < / option >
< / select >
< select
id = "category-filter"
onchange = "loadQueries()" >
< option
value = "all" > All
Categories < / option >
< / select >
< / div >
< div
id = "all-queries-list"


class ="queries-list" > < / div >

< / section >

< !-- Analytics
Section -->
< section
id = "analytics"


class ="section" >

< h2 >📈 Performance
Analytics < / h2 >
< div


class ="analytics-grid" >

< div


class ="analytics-card" >

< h3 > Team
Performance < / h3 >
< div
id = "team-performance" > < / div >
< / div >
< div


class ="analytics-card" >

< h3 > Response
Times < / h3 >
< div
id = "response-times" > < / div >
< / div >
< / div >
< / section >

< !-- New
Query
Section -->
< section
id = "new-query"


class ="section" >

< h2 >➕ Add
New
Query < / h2 >
< form
id = "new-query-form"


class ="query-form" >

< div


class ="form-group" >

< label > Source: < / label >
< select
id = "query-source"
required >
< option
value = "email" > Email < / option >
< option
value = "social" > Social
Media < / option >
< option
value = "chat" > Live
Chat < / option >
< option
value = "web" > Web
Form < / option >
< / select >
< / div >

< div


class ="form-group" >

< label > Customer
Email: < / label >
< input
type = "email"
id = "customer-email"
required >
< / div >

< div


class ="form-group" >

< label > Subject: < / label >
< input
type = "text"
id = "query-subject"
required >
< / div >

< div


class ="form-group" >

< label > Message: < / label >
< textarea
id = "query-content"
rows = "6"
required > < / textarea >
< / div >

< button
type = "submit"


class ="btn-primary" > Submit Query < / button >

< / form >
< / section >
< / div >

< script
src = "script.js" > < / script >
< / body >
< / html >