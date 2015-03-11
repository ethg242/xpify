#!/usr/bin/env python

###
# XPify - An application to gamify learning.
# Version: DEV
# Timestamp: NULL
# 
# Written by Ethan Guo
# Using Google App Engine and the webapp2 framework
# 
###

### IMPORTS ###

import time
import uuid

import cgi
import webapp2

from google.appengine.ext.webapp import util
from google.appengine.ext import db
from google.appengine.ext import ndb
from google.appengine.api import users


### HELPER FUNCTIONS ###

contentHTML = '''
	<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Mauris et arcu congue, placerat 
	massa ut, vestibulum enim. Cras id tempus erat. Ut enim leo, fermentum eu elementum vel, 
	varius in nisl. Suspendisse dapibus suscipit mauris, eget ornare justo congue at. Fusce 
	hendrerit ante ut dictum tincidunt. Morbi nec metus sit amet odio elementum consectetur in eu 
	mi. Proin sed velit sapien. Proin auctor feugiat leo vel gravida. Nullam neque enim, hendrerit 
	fringilla velit non, fermentum pretium tortor. Sed id congue felis. Vestibulum laoreet a eros 
	a porttitor.</p>
	<p>Sed fringilla, ipsum a congue tincidunt, odio purus lobortis lacus, mollis dictum turpis 
	nisi quis quam. Fusce in interdum diam. Mauris tempus dolor ut viverra pellentesque. Sed id 
	condimentum ligula, et venenatis augue. Sed gravida scelerisque metus, ut cursus enim 
	elementum nec. Mauris euismod tincidunt felis, ut auctor erat malesuada in. Sed aliquam turpis 
	sit amet velit malesuada vehicula. Nulla fermentum nibh sapien, et convallis erat eleifend at. 
	Phasellus accumsan mattis libero eu porttitor.</p>
	<p>Duis ac egestas nulla, egestas tincidunt enim. Nulla ultrices cursus ipsum vitae vehicula. 
	Donec ac libero bibendum, semper magna vitae, vestibulum tellus. Suspendisse adipiscing tellus 
	ut tempor luctus. Praesent accumsan, mi vel scelerisque mattis, purus nisi ultricies ante, sit 
	amet malesuada nisl sapien eu erat. Ut iaculis mauris eget diam viverra, quis lacinia urna 
	elementum. Donec non ultrices nunc. Etiam quis adipiscing nunc. Proin luctus tellus in nulla 
	pellentesque, vel placerat nisi volutpat. Nullam at urna diam. Praesent congue tortor ut nisi 
	lacinia ornare. Proin tristique tincidunt posuere. Morbi ut elit porttitor, convallis nisl in, 
	posuere augue. Nullam fermentum urna odio, sagittis dapibus lorem elementum et. Pellentesque 
	habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Phasellus 
	semper feugiat erat nec semper.</p>
	<p>In ut laoreet orci. Curabitur varius dui id lorem dignissim sagittis. Mauris imperdiet 
	libero nec orci gravida, a vulputate massa adipiscing. Nullam auctor nulla lorem, sit amet 
	rhoncus risus scelerisque sed. Duis nisl elit, consectetur in dictum a, varius ac elit. Nunc 
	ut tempus sapien. Sed sollicitudin, eros in semper ultricies, est sem facilisis urna, a 
	eleifend erat lorem sed orci. Proin pretium dolor ac tellus imperdiet, in mattis libero 
	porttitor. Nullam lorem velit, semper at lobortis sed, vestibulum sed nulla. Morbi lacinia, 
	nunc non luctus lacinia, sem elit laoreet elit, at dapibus nisi nisl ut purus. Maecenas vitae 
	imperdiet arcu, eget suscipit nunc. Class aptent taciti sociosqu ad litora torquent per 
	conubia nostra, per inceptos himenaeos. Maecenas sollicitudin, tellus nec blandit pharetra, 
	felis arcu dignissim nibh, vel pellentesque mi sem a odio. Proin luctus blandit venenatis. 
	Suspendisse ac gravida diam. Fusce blandit volutpat urna in laoreet.</p>
	<p>Praesent ac tortor non est accumsan vehicula. Morbi mi felis, vulputate consequat viverra 
	sit amet, vehicula ac turpis. Aenean mattis blandit risus gravida gravida. Etiam hendrerit 
	ipsum arcu, et facilisis elit pharetra in. Sed cursus lobortis elit, ac imperdiet risus 
	vehicula id. Quisque ac dui id libero sagittis viverra. Praesent semper dictum venenatis. 
	Donec sed diam et velit sodales semper. Phasellus sed lacinia est. Nam sit amet dolor urna. 
	Nunc sagittis vitae sem eu posuere. Vestibulum in sodales lectus. Praesent rhoncus sit amet 
	risus non interdum.</p>
	<p>Praesent ullamcorper et metus sed hendrerit. Etiam vitae sem nunc. Cras consequat in tortor 
	in sollicitudin. Aliquam quam enim, vestibulum a ultricies in, commodo et lectus. Suspendisse 
	potenti. Maecenas posuere vitae libero sed molestie. In et ligula quis lectus viverra cursus 
	eu quis turpis. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere 
	cubilia Curae; Nullam in purus dolor. Morbi sit amet sagittis dolor. Integer purus dolor, 
	hendrerit ac nisi blandit, tempor aliquam nunc. Nunc malesuada pharetra mollis. Morbi ultrices 
	velit sagittis semper semper. Pellentesque habitant morbi tristique senectus et netus et 
	malesuada fames ac turpis egestas. Maecenas nisi est, varius ac est vitae, hendrerit mattis 
	magna. Praesent libero augue, consectetur eu accumsan vulputate, feugiat at nunc.</p>
	<p>Donec vel dolor vel lorem laoreet consequat. Integer volutpat neque interdum neque 
	fringilla, a tincidunt eros varius. Vivamus eu auctor orci, ac tempus sem. Donec libero ipsum, 
	varius vitae libero et, porta euismod dui. Mauris non diam id nisl blandit dignissim a quis 
	tellus. Etiam semper pellentesque felis, non tincidunt augue mollis vel. Vivamus tincidunt 
	elit lacus, eget congue ante placerat nec. Ut vel enim sit amet odio gravida rhoncus. 
	Vestibulum fermentum sed nibh adipiscing placerat. Proin eu urna nulla. Quisque eleifend 
	tristique justo, consectetur accumsan purus imperdiet id. Duis vehicula enim tellus, non 
	dapibus augue elementum id. Aenean ut aliquet nibh, in pellentesque elit. Pellentesque vitae 
	molestie quam. Maecenas quis ultrices quam, eget sodales est. Nunc porttitor orci vitae 
	bibendum venenatis.</p>
	<p>Maecenas molestie eros nisl, sed dictum lectus consectetur et. Phasellus auctor libero sed 
	tristique mattis. Ut adipiscing libero quis rutrum ullamcorper. Mauris eget nisl vitae diam 
	fringilla posuere. Quisque sed mi tristique, fringilla odio eget, sollicitudin magna. Sed 
	viverra libero congue nisi iaculis, vitae hendrerit velit aliquet. Aliquam sit amet faucibus 
	lectus. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis 
	egestas. Mauris iaculis neque ornare mauris suscipit, at tincidunt dui ornare. Sed id 
	vestibulum quam. Praesent at lacus ut tortor accumsan rutrum. Nulla vulputate sit amet eros ac 
	commodo. Morbi sit amet nibh ligula. Nunc quis mi vel tortor hendrerit tempus. Cras quis 
	vehicula metus.</p>
'''

def composePage(content, style=0):
	return '''
<!DOCTYPE html>
<html>
	<head>
		<title>XPify - BETA</title>
		
		<link rel="stylesheet" type="text/css" href="/static/css/theme/jquery-ui-1.10.4.custom.min.css" />
		<link rel="stylesheet" type="text/css" href="/static/css/styles-global.css" />
		<link rel="stylesheet" type="text/css" href="/static/css/styles%d.css" />
		
		<link rel="shortcut icon" href="/static/images/favicon.ico" />
		<link rel="apple-touch-icon" sizes="57x57" href="/static/images/apple-touch-icon-57x57.png" />
		<link rel="apple-touch-icon" sizes="114x114" href="/static/images/apple-touch-icon-114x114.png" />
		<link rel="apple-touch-icon" sizes="72x72" href="/static/images/apple-touch-icon-72x72.png" />
		<link rel="apple-touch-icon" sizes="144x144" href="/static/images/apple-touch-icon-144x144.png" />
		<link rel="apple-touch-icon" sizes="60x60" href="/static/images/apple-touch-icon-60x60.png" />
		<link rel="apple-touch-icon" sizes="120x120" href="/static/images/apple-touch-icon-120x120.png" />
		<link rel="apple-touch-icon" sizes="76x76" href="/static/images/apple-touch-icon-76x76.png" />
		<link rel="apple-touch-icon" sizes="152x152" href="/static/images/apple-touch-icon-152x152.png" />
		<link rel="icon" type="image/png" href="/static/images/favicon-196x196.png" sizes="196x196" />
		<link rel="icon" type="image/png" href="/static/images/favicon-160x160.png" sizes="160x160" />
		<link rel="icon" type="image/png" href="/static/images/favicon-96x96.png" sizes="96x96" />
		<link rel="icon" type="image/png" href="/static/images/favicon-16x16.png" sizes="16x16" />
		<link rel="icon" type="image/png" href="/static/images/favicon-32x32.png" sizes="32x32" />
		<meta name="msapplication-TileColor" content="#603cba" />
		<meta name="msapplication-TileImage" content="/static/images/mstile-144x144.png" />
		<meta name="msapplication-square70x70logo" content="/static/images/mstile-70x70.png" />
		<meta name="msapplication-square144x144logo" content="/static/images/mstile-144x144.png" />
		<meta name="msapplication-square150x150logo" content="/static/images/mstile-150x150.png" />
		<meta name="msapplication-square310x310logo" content="/static/images/mstile-310x310.png" />
		<meta name="msapplication-wide310x150logo" content="/static/images/mstile-310x150.png" />
		
		<script type="text/javascript" src="/static/js/jquery-1.10.2.min.js"></script>
		<script type="text/javascript" src="/static/js/jquery-ui-1.10.4.custom.min.js"></script>
		<script type="text/javascript" src="/static/js/portlets.js"></script>
	</head>
%s
</html>
''' %(style, content)

def getUserEntry(gUser):
	result = ndb.gql("SELECT __key__ FROM EntryUser "
							"WHERE userid = :1", gUser.user_id()).get()
	return result

def getNextUUID():
	longid = uuid.uuid4()
	id = str(int(longid))[:8]
	return id


### DATABASE ###

class EntryUser(ndb.Model):
	def getUsername(self):
		return self.fullname or self.userobj.nickname() or "Anonymous"
	
	def getClasses(self):
		usertypepl = "students"
		if self.usertype in ["Teacher", "Administrator"]:
			usertypepl = "teachers"
		allClasses = ndb.gql("SELECT " + usertypepl + ", classid FROM EntryClass").fetch(200)
		classids = []
		for class_ in allClasses:
			if self.key in class_.to_dict()[usertypepl]:
				classids.append(class_.classid)
		try:
			return ndb.gql("SELECT __key__ FROM EntryClass "
								"WHERE classid IN :1",
								classids).fetch(20)
		except db.BadQueryError:
			return None
	
	usertype =	ndb.StringProperty(required=True,   # FINAL; Role of user
							choices=["Student", "Teacher", "Administrator", "Undefined"] )
	userobj =	ndb.UserProperty(required=True)		# User object
	userid =	ndb.StringProperty(required=True)	# FINAL, UNIQUE; Generated from user object at creation
	fullname = 	ndb.StringProperty(default="")		# Used to compute $username
	username = 	ndb.ComputedProperty(getUsername)	# TYPE: String 
	classes =	ndb.ComputedProperty(getClasses)	# UPLOOK; TYPE: Keys(EntryClass)

class EntryClass(ndb.Model):
	classname =	ndb.StringProperty(required=True)	# Descriptive Name
	classid =	ndb.StringProperty(required=True)	# FINAL, UNIQUE; Generated at creation
	levels =	ndb.JsonProperty()					# FORMAT: [(<minXP>, <name>, <description>), ...]
	
	teachers =	ndb.KeyProperty(repeated=True,		# DEFINE; TYPE: Keys(EntryUser)[Teacher]
							kind="EntryUser")
	students =	ndb.KeyProperty(repeated=True,		# DEFINE; TYPE: Keys(EntryUser)[Student]
							kind="EntryUser")
	scores =	ndb.JsonProperty(default={})		# FORMAT: {<studentKey>: <score>}


### PAGES ###

class PageLanding(webapp2.RequestHandler):
	def get(self):
		gUser = users.get_current_user()
		if gUser:
			self.redirect("/my/home/")
		else:
			self.response.write(composePage('''
<body>
	<header>
		<div id="logo-wrapper"><img src="/static/images/favicon-196x196.png"
				height="196" width="196" alt="[XPify]" /></div>
	</header>
	<div id="login-wrapper">
		<a href="%s">Login</a>
	</div>
</body>
''' %(users.create_login_url("/postlogin/")), style=1 ))



class PageMyHome(webapp2.RequestHandler):
	def get(self):
		gUser = users.get_current_user()
		if not gUser:
			self.redirect("/login/")
		else:
			user = getUserEntry(gUser).get()
			userClasses = user.classes
			classesHTML = ""
			if userClasses:
				for classKey in userClasses:
					class_ = classKey.get()
					classesHTML += '<li><a href="/class/challenges?class=%s">%s</a></li>\n' %(
							class_.classid, class_.classname)
				classesHTML += '<li class="join-class-plus"><a href="/class/search/"><div>+</div></a></li>'
			else:
				if user.usertype in ["Teacher", "Administrator"]:
					classesHTML = '''
<div id="no-classes">
	<span id="no-classes-banner">You have no classes!</span>
	<li><a href="/class/create/">
		Create one!
	</a></li>
</div>
'''
				else:
					classesHTML = '''
<div id="no-classes">
	<span id="no-classes-banner">You have no classes!</span>
	<li><a href="/class/search/">
		Join one!
	</a></li>
</div>
'''
			
			contentHTML = '''
<div class="column">
	<div class="portlet">
		<div class="portlet-header">Header 1</div>
		<div class="portlet-content">Lorem ipsum dolor sit amet, consectetur adipiscing elit. Mauris et arcu congue, placerat 
		massa ut, vestibulum enim. Cras id tempus erat.</div>
	</div>
	
	<div class="portlet">
		<div class="portlet-header">Header 3</div>
		<div class="portlet-content">Sed fringilla, ipsum a congue tincidunt, odio purus lobortis lacus, mollis dictum turpis 
	nisi quis quam. Fusce in interdum diam. Mauris tempus dolor ut viverra pellentesque.</div>
	</div>
</div>
<div class="column">
	<div class="portlet">
		<div class="portlet-header">Header 2</div>
		<div class="portlet-content">Duis ac egestas nulla, egestas tincidunt enim. Nulla ultrices cursus ipsum vitae vehicula. 
	Donec ac libero bibendum, semper magna vitae, vestibulum tellus.</div>
	</div>
</div>
'''

			self.response.out.write(composePage('''
<body>
	<aside>
		<div id="logo-wrapper"><img src="/static/images/favicon-96x96.png"
				height="96" width="96" alt="[XPify]" /></div>
		<nav id="vert-navbar">
			<ul id="vert-navbar-main">
				<li id="current"><a href="/my/home/">Home</a></li>
				<li><a href="/profile/">Profile</a></li>
				<li><a href="/logout/">Log out</a></li>
			</ul>
			<span id="vert-navbar-classes-header">Classes</span>
			<ul id="vert-navbar-classes-list">
				%s
			</ul>
		</nav>
	</aside>
	<main>
		<div id="content">
			%s
		</div>
	</main>
</body>
''' %(classesHTML, contentHTML) ))

class PageProfile(webapp2.RequestHandler):
	def get(self):
		gUser = users.get_current_user()
		if not gUser:
			self.redirect("/login/")
		else:
			user = getUserEntry(gUser).get()
			userClasses = user.classes
			classesHTML = ""
			if userClasses:
				for classKey in userClasses:
					class_ = classKey.get()
					classesHTML += '<li><a href="/class/challenges?class=%s">%s</a></li>\n' %(
							class_.classid, class_.classname)
				classesHTML += '<li class="join-class-plus"><a href="/class/search/"><div>+</div></a></li>'
			else:
				if user.usertype in ["Teacher", "Administrator"]:
					classesHTML = '''
<div id="no-classes">
	<span id="no-classes-banner">You have no classes!</span>
	<li><a href="/class/create/">
		Create one!
	</a></li>
</div>
'''
				else:
					classesHTML = '''
<div id="no-classes">
	<span id="no-classes-banner">You have no classes!</span>
	<li><a href="/class/search/">
		Join one!
	</a></li>
</div>
'''
		
			# Generate Content
			tUserId = self.request.get("user")
			tSelf = False
			
			if not tUserId:
				tUserId = gUser.user_id()
				tSelf = True
			tUser = ndb.gql("SELECT * FROM EntryUser WHERE userid = :1", tUserId).get()
			
			subvalues = tUser.to_dict()
			
			if tSelf:
				fullnameHTML = '''
<td class="table-name">Full Name</td>
<td class="table-value-editable">
	<input type="text" name="fullname" value="%s" />
</td>
''' %(subvalues["fullname"])
			else:
				fullnameHTML = '''
<td class="table-name">Full Name</td>
<td class="table-value">%s</td>
''' %(subvalues["fullname"])
			
			subvalues["fullnameHTML"] = fullnameHTML
			contentHTML = '''
<button id="profile-change-picture" onclick="changePicture()">
	<img id="profile-picture" src="/static/images/favicon-196x196.png"
			height="196" width="196" alt="Profile Picture" />
</button>
<form id="table-form" action="/profile/" method="POST">
	<table id="usertable">
		<tr>
			%(fullnameHTML)s
		</tr> <tr>
			<td class="table-name">User Type</td>
			<td class="table-value">%(usertype)s</td>
		</tr> <tr>
			<td class="table-name">User ID</td>
			<td class="table-value">%(userid)s</td>
		</tr> <tr>
			<td class="table-name">Classes</td>
			<td class="table-value">%(classes)s</td>
		</tr>
	</table>
	<br />
	<input type="submit" value="Save"/>
</form>
''' %(subvalues)
			
			self.response.out.write(composePage('''
<body>
	<aside>
		<div id="logo-wrapper"><img src="/static/images/favicon-96x96.png"
				height="96" width="96" alt="[XPify]" /></div>
		<nav id="vert-navbar">
			<ul id="vert-navbar-main">
				<li><a href="/my/home/">Home</a></li>
				<li id="current"><a href="/profile/">Profile</a></li>
				<li><a href="/logout/">Log out</a></li>
			</ul>
			<span id="vert-navbar-classes-header">Classes</span>
			<ul id="vert-navbar-classes-list">
				%s
			</ul>
		</nav>
	</aside>
	<main>
		<div id="content">
			%s
		</div>
	</main>
</body>
''' %(classesHTML, contentHTML) ))

	def post(self):
		gUser = users.get_current_user()
		if not gUser:
			self.redirect("/login/")
		else:
			fullname = self.request.get("fullname", "")
			
			user = getUserEntry(gUser)
			entry = user.get()
			entry.fullname = fullname
			entry.put()
			
			self.redirect("/profile/")

class PageClassSearch(webapp2.RequestHandler):
	def get(self):
		gUser = users.get_current_user()
		if not gUser:
			self.redirect("/login/")
		else:
			user = getUserEntry(gUser).get()
			userClasses = user.classes
			classesHTML = ""
			if userClasses:
				for classKey in userClasses:
					class_ = classKey.get()
					classesHTML += '<li><a href="/class/challenges?class=%s">%s</a></li>\n' %(
							class_.classid, class_.classname)
				classesHTML += '<li class="join-class-plus"><a href="/class/search/"><div>+</div></a></li>'
			else:
				if user.usertype in ["Teacher", "Administrator"]:
					classesHTML = '''
<div id="no-classes">
	<span id="no-classes-banner">You have no classes!</span>
	<li><a href="/class/create/">
		Create one!
	</a></li>
</div>
'''
				else:
					classesHTML = '''
<div id="no-classes">
	<span id="no-classes-banner">You have no classes!</span>
	<li><a href="/class/search/">
		Join one!
	</a></li>
</div>
'''
			
			# Generate Content
			contentHTML = '''
<form action="/class/search" method="GET">
	<input type="text" name="query" placeholder="Class name (Coming soon)" disabled="true" size="30"/> OR
	<input type="text" name="query" placeholder="Class code" pattern="[0-9]+" />
	<input type="submit" value="Search" />
</form>
'''
			
			query = self.request.get("query")
			if query:
				classid = None
				try:
					classid = query
				except ValueError:
					results = ndb.gql("SELECT * FROM EntryClass WHERE classname = :1", classid).fetch(200)
				else:
					results = ndb.gql("SELECT * FROM EntryClass WHERE classid = :1", classid).fetch(200)
				resultsHTML = ""
				for result in results:
					resultsHTML += '''
<label class="label-class">
	<input type="radio" name="classid" value="%(classid)s" />
	%(classname)s (%(classid)s)
</label>
					''' %result.to_dict()
					#TODO: Check if student already in class
				contentHTML = '''
<form id="search-form" action="/class/search" method="GET">
	<input type="text" name="query" placeholder="Class name (Coming soon)" disabled="true" size="30"/> OR
	<input type="text" name="query" value="%s" placeholder="Class code" />
	<input type="submit" value="Search" />
</form>
<hr />
<form id="joinclass-form" action="/class/search" method="POST">
	<ul>
		%s
	</ul>
	<input type="submit" value="Go!" />
</form>
''' %(query, resultsHTML)
			
			self.response.out.write(composePage('''
<body>
	<aside>
		<div id="logo-wrapper"><img src="/static/images/favicon-96x96.png"
				height="96" width="96" alt="[XPify]" /></div>
		<nav id="vert-navbar">
			<ul id="vert-navbar-main">
				<li><a href="/my/home/">Home</a></li>
				<li><a href="/profile/">Profile</a></li>
				<li><a href="/logout/">Log out</a></li>
			</ul>
			<span id="vert-navbar-classes-header">Classes</span>
			<ul id="vert-navbar-classes-list">
				%s
			</ul>
		</nav>
	</aside>
	<main>
		<div id="content">
			%s
		</div>
	</main>
</body>
''' %(classesHTML, contentHTML) ))

	def post(self):
		gUser = users.get_current_user()
		if not gUser:
			self.redirect("/login/")
		else:
			classget = self.request.get("classid")
			if classget:
				classKey = ndb.gql("SELECT __key__ FROM EntryClass "
										"WHERE classid = :1",
										classget).get()
				if classKey:
					entry = classKey.get()
					userKey = getUserEntry(gUser)
					if userKey in entry.students or userKey in entry.teachers:
						self.response.out.write('You are already in that class! <br /><a href="/class/challenges?class=%s">Go to class home</a>' %(classget))
					else:
						user = userKey.get()
						if user.usertype == "Student":
							entry.students.append(userKey)
							entry.scores[userKey] ##HERE##
						elif user.usertype in ["Teacher", "Administrator"]:
							entry.teachers.append(userKey)
						
						entry.put()
						
						self.redirect("/class/challenges?class=%s" %(classget) )

class PageClassChallenges(webapp2.RequestHandler):
	def get(self):
		gUser = users.get_current_user()
		if not gUser:
			self.redirect("/login/")
		else:
			classid = self.request.get("class")
			user = getUserEntry(gUser).get()
			userClasses = user.classes
			classesHTML = ""
			if userClasses:
				for classKey in userClasses:
					class_ = classKey.get()
					if str(class_.classid) == classid:
						classesHTML += '<li id="current"><a href="/class/challenges?class=%s">%s</a></li>\n' %(
								class_.classid, class_.classname)
					else:
						classesHTML += '<li><a href="/class/challenges?class=%s">%s</a></li>\n' %(
								class_.classid, class_.classname)
				classesHTML += '<li class="join-class-plus"><a href="/class/search/"><div>+</div></a></li>'
			else:
				if user.usertype in ["Teacher", "Administrator"]:
					classesHTML = '''
<div id="no-classes">
	<span id="no-classes-banner">You have no classes!</span>
	<li><a href="/class/create/">
		Create one!
	</a></li>
</div>
'''
				else:
					classesHTML = '''
<div id="no-classes">
	<span id="no-classes-banner">You have no classes!</span>
	<li><a href="/class/search/">
		Join one!
	</a></li>
</div>
'''
			manageHTML = ""
			if user.usertype == "Teacher":
				manageHTML = '<li><a href="/class/manage/?class=%s">Manage</a></li>' %(classid)
			
			self.response.out.write(composePage('''
<body>
	<aside>
		<div id="logo-wrapper"><img src="/static/images/favicon-96x96.png"
				height="96" width="96" alt="[XPify]" /></div>
		<nav id="vert-navbar">
			<ul id="vert-navbar-main">
				<li><a href="/my/home/">Home</a></li>
				<li><a href="/profile/">Profile</a></li>
				<li><a href="/logout/">Log out</a></li>
			</ul>
			<span id="vert-navbar-classes-header">Classes</span>
			<ul id="vert-navbar-classes-list">
				%(classes)s
			</ul>
		</nav>
	</aside>
	<main>
		<nav id="span-navbar">
			<ul>
				<li id="current"><a href="/class/challenges?class=%(classid)s">Challenges</a></li>
				<li><a href="/class/leaderboards?class=%(classid)s">Leaderboards</a></li>
				<li><div class="unimplemented">Coming Soon</div></li>
				%(manage)s
			</ul>
		</nav>
		<div id="content">
			%(content)s
		</div>
	</main>
</body>
''' %{"classes":classesHTML, "classid":classid, "manage":manageHTML, "content":contentHTML} ))

class PageClassCreate(webapp2.RequestHandler):
	def get(self):
		gUser = users.get_current_user()
		user = getUserEntry(gUser).get()
		if not (gUser and user.usertype == "Teacher"):
			self.redirect("/login/")
		else:
			classid = self.request.get("class")
			userClasses = user.classes
			classesHTML = ""
			if userClasses:
				for classKey in userClasses:
					class_ = classKey.get()
					if str(class_.classid) == classid:
						classesHTML += '<li id="current"><a href="/class/home?class=%s">%s</a></li>\n' %(
								class_.classid, class_.classname)
					else:
						classesHTML += '<li><a href="/class/home?class=%s">%s</a></li>\n' %(
								class_.classid, class_.classname)
				classesHTML += '<li class="join-class-plus" id="current"><a href="/class/search/"><div>+</div></a></li>'
			else:
				if user.usertype in ["Teacher", "Administrator"]:
					classesHTML = '''
<div id="no-classes">
	<span id="no-classes-banner">You have no classes!</span>
	<li id="current"><a href="/class/create/">
		Create one!
	</a></li>
</div>
'''
				else:
					classesHTML = '''
<div id="no-classes">
	<span id="no-classes-banner">You have no classes!</span>
	<li><a href="/class/search/">
		Join one!
	</a></li>
</div>
'''

			self.response.out.write(composePage('''
<body>
	<aside>
		<div id="logo-wrapper"><img src="/static/images/favicon-96x96.png"
				height="96" width="96" alt="[XPify]" /></div>
		<nav id="vert-navbar">
			<ul id="vert-navbar-main">
				<li><a href="/my/home/">Home</a></li>
				<li><a href="/profile/">Profile</a></li>
				<li><a href="/logout/">Log out</a></li>
			</ul>
			<span id="vert-navbar-classes-header">Classes</span>
			<ul id="vert-navbar-classes-list">
				%(classes)s
			</ul>
		</nav>
	</aside>
	<main>
		<div id="content">
			<form action="/class/create/" method="POST">
				<input type="hidden" name="teacher" value="">
				<label>
					Class Name: <input type="text" name="classname">
				</label>
				<input type="submit" value="Create">
			</form>
		</div>
	</main>
</body>
''' %{"classes":classesHTML, "classid":classid, "content":contentHTML} ))
	
	def post(self):
		classname = self.request.get("classname")
		
		gUser = users.get_current_user()
		user = getUserEntry(gUser).get()
		if classname and gUser and user.usertype == "Teacher":
			classid = getNextUUID()
			
			entry = EntryClass()
			entry.classname = classname
			entry.classid = classid
			entry.teachers = [user.key,]
			
			entry.put()
			
			time.sleep(1)
			
			self.redirect("/class/manage?class=%s" %(classid) )
		else:
			self.redirect("/class/create/")

class PageClassManage(webapp2.RequestHandler):
	def get(self):
		gUser = users.get_current_user()
		user = getUserEntry(gUser).get()
		if not (gUser and user.usertype == "Teacher"):
			self.redirect("/login/")
		else:
			classid = self.request.get("class")
			userClasses = user.classes
			classesHTML = ""
			if userClasses:
				for classKey in userClasses:
					class_ = classKey.get()
					if str(class_.classid) == classid:
						classesHTML += '<li id="current"><a href="/class/home?class=%s">%s</a></li>\n' %(
								class_.classid, class_.classname)
					else:
						classesHTML += '<li><a href="/class/home?class=%s">%s</a></li>\n' %(
								class_.classid, class_.classname)
				classesHTML += '<li class="join-class-plus"><a href="/class/search/"><div>+</div></a></li>'
			else:
				if user.usertype in ["Teacher", "Administrator"]:
					classesHTML = '''
<div id="no-classes">
	<span id="no-classes-banner">You have no classes!</span>
	<li><a href="/class/create/">
		Create one!
	</a></li>
</div>
'''
				else:
					classesHTML = '''
<div id="no-classes">
	<span id="no-classes-banner">You have no classes!</span>
	<li><a href="/class/search/">
		Join one!
	</a></li>
</div>
'''

			class_ = ndb.gql("SELECT * FROM EntryClass WHERE classid = :1", classid).get()
			
			subvalues = class_.to_dict()
			
			subvalues["teachersHTML"] = ", ".join([teacherKey.get().username for teacherKey in class_.teachers])
			subvalues["studentsHTML"] = ", ".join([studentKey.get().username for studentKey in class_.students])
			
			contentHTML = '''
<form id="table-form" action="/class/manage?class=%(classid)s" method="POST">
	<table id="classtable">
		<tr>
			<td class="table-name">Class Name</td>
			<td class="table-value-editable">
				<input type="text" name="classname" value="%(classname)s" />
			</td>
		</tr> <tr>
			<td class="table-name">Class ID</td>
			<td class="table-value">%(classid)s</td>
		</tr> <tr>
			<td class="table-name">Teachers</td>
			<td class="table-value">%(teachersHTML)s</td>
		</tr> <tr>
			<td class="table-name">Students</td>
			<td class="table-value">%(studentsHTML)s</td>
		</tr>
	</table>
	<br />
	<input type="submit" value="Save"/>
</form>
''' %(subvalues)
			
			self.response.out.write(composePage('''
<body>
	<aside>
		<div id="logo-wrapper"><img src="/static/images/favicon-96x96.png"
				height="96" width="96" alt="[XPify]" /></div>
		<nav id="vert-navbar">
			<ul id="vert-navbar-main">
				<li><a href="/my/home/">Home</a></li>
				<li><a href="/profile/">Profile</a></li>
				<li><a href="/logout/">Log out</a></li>
			</ul>
			<span id="vert-navbar-classes-header">Classes</span>
			<ul id="vert-navbar-classes-list">
				%(classes)s
			</ul>
		</nav>
	</aside>
	<main>
		<nav id="span-navbar">
			<ul>
				<li><a href="/class/challenges?=%(classid)s">Challenges</a></li>
				<li><a href="/class/leaderboards?=%(classid)s">Leaderboards</a></li>
				<li><div class="unimplemented">Coming Soon</div></li>
				<li id="current"><a href="/class/manage/?class=%(classid)s">Manage</a></li>
			</ul>
		</nav>
		<div id="content">
			%(content)s
		</div>
	</main>
</body>
''' %{"classes":classesHTML, "classid":classid, "content":contentHTML} ))


class PagePostlogin(webapp2.RequestHandler):
	def get(self):
		gUser = users.get_current_user()
		continueURL = self.request.get("continue", "/my/home/")
		tUser = ndb.gql("SELECT __key__ FROM EntryUser WHERE userid = :1",
				gUser.user_id()).get()
		if not tUser:
			# Show User Creation
			self.response.out.write(composePage('''
<body>
	<main>
		<form id="user-form" action="/postlogin/" method="POST">
			<span id="header-usertype">User Type:</span>
			<br />
			<label class="label-usertype">
				<input type="radio" name="usertype" value="Student" checked="true"/> Student
			</label><br />
			<label class="label-usertype">
				<input type="radio" name="usertype" value="Teacher" /> Teacher
			</label><br />
			<label class="label-usertype">
				<input type="radio" name="usertype" value="Administrator" /> Administrator
			</label>
			<br />
			<input type="submit" />
		</form>
	</main>
</body>
''', style=1))
		else:
			self.redirect(continueURL)
	
	def post(self):
		usertype = self.request.get("usertype")
		
		if usertype:
		
			gUser = users.get_current_user()
			entry = EntryUser()
			entry.usertype = usertype
			entry.userobj = gUser
			entry.userid = gUser.user_id()
			entry.put()
		else:
			self.redirect("/postlogin/")
		
		# Continue
		self.redirect("/d/my/home/")

### REDIRECTS ###

class RedirectLogin(webapp2.RequestHandler):
	def get(self):
		target = cgi.escape(self.request.get("continue", "/my/home/"))
		self.redirect(users.create_login_url("/postlogin/?continue=" + target))

class RedirectLogout(webapp2.RequestHandler):
	def get(self):
		target = cgi.escape(self.request.get("continue", "/"))
		self.redirect(users.create_logout_url(target))

class RedirectRestrictedPage(webapp2.RequestHandler):
	target = "/"
	def get(self):
		gUser = users.get_current_user()
		if gUser:
			self.redirect(self.target)
		else:
			self.redirect(users.create_login_url("/postlogin/?continue=" + self.target))

class RedirectMyHome(RedirectRestrictedPage):
	target = "/my/home/"

class RedirectClassSearch(RedirectRestrictedPage):
	target = "/class/search/"

class RedirectClassChallenges(RedirectRestrictedPage):
	target = "/class/challenges/"

class RedirectDelayMyHome(webapp2.RequestHandler):
	def get(self):
		gUser = users.get_current_user()
		if gUser:
			time.sleep(1)
			self.redirect("/my/home/")
		else:
			self.redirect(users.create_login_url("/postlogin/?continue=/my/home"))
	

#:DEV:
class PageDev(webapp2.RequestHandler):
	def post(self):
		entry = EntryClass()
		
	def get(self):
		if self.request.get("make")=="class":
			entry = EntryClass()
			entry.classname = self.request.get("classname", "Demo Class")
			entry.classid = 000001
			
			entry.put()
			self.response.out.write("Success!")


### APPLICATION ###

app = webapp2.WSGIApplication([
		("^(?:/landing)?/?$", PageLanding),
		("^/login/?$", RedirectLogin),
		("^/logout/?$", RedirectLogout),
		("^/postlogin/?$", PagePostlogin),
		("^/my/home/?$", PageMyHome),
			("^/my/?$|^/home/?$", RedirectMyHome),
			("^/d/my/home/?$", RedirectDelayMyHome),
		("^/profile/?$", PageProfile),
		("^/class/challenges/?$", PageClassChallenges),
			("^/class/?$", RedirectClassChallenges),
		("^/class/create/?$", PageClassCreate),
		("^/class/manage/?$", PageClassManage),
		("^/class/search/?$", PageClassSearch),
			("^/class/join/?$", RedirectClassSearch),
		("^/dev/?$", PageDev)
		], debug=True)
