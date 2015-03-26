#!/usr/bin/env python

###
# XPify - An application to gamify learning.
# Version: DEV
# Timestamp: NULL
#
# Written by Ethan Guo
# Using Google App Engine
#
###

### IMPORTS ###

import time
import uuid
import os

import cgi
import webapp2
import jinja2

from google.appengine.ext.webapp import util
from google.appengine.ext import db, ndb
from google.appengine.api import users


### HELPER FUNCTIONS ###

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

	# def getScores(self):
	# 	scores = None
	# 	if self.usertype == "Student":
	# 		scores = {}
	# 		if self.classes:
	# 			for classKey in self.classes:
	# 				class_ = classKey.get()
	# 				scores[class_.classid] = class_.scores[self.userid]
	# 	return scores

	usertype =	ndb.StringProperty(required=True,	# FINAL; Role of user
							choices=["Student", "Teacher", "Administrator", "Undefined"] )
	userobj =	ndb.UserProperty(required=True)	# FINAL; User object
	userid =	ndb.StringProperty(required=True)	# FINAL, UNIQUE; Generated from user object at creation
	fullname =	ndb.StringProperty(default="")	# Used to compute $username
	username =	ndb.ComputedProperty(getUsername)# TYPE: String
	classes =	ndb.ComputedProperty(getClasses)	# UPLOOK; TYPE: Keys(EntryClass)
	# scores =	ndb.ComputedProperty(getScores)	# UPLOOK; FORMAT: {<classId>: <score>}

class EntryClass(ndb.Model):
	classname =ndb.StringProperty(required=True)	# Descriptive Name
	classid =	ndb.StringProperty(required=True)	# FINAL, UNIQUE; Generated at creation
	levels =	ndb.JsonProperty()			# FORMAT: [(<minXP>, <name>, <description>), ...]
	teachers =	ndb.KeyProperty(repeated=True,	# DEFINE; TYPE: Keys(EntryUser)[Teacher]
							kind="EntryUser")
	students =	ndb.KeyProperty(repeated=True,	# DEFINE; TYPE: Keys(EntryUser)[Student]
							kind="EntryUser")
	scores =	ndb.JsonProperty(default={})		# FORMAT: {<studentId>: <score>}


### PAGES ###

class PageLanding(webapp2.RequestHandler):
	def get(self):
		gUser = users.get_current_user()
		if gUser:
			self.redirect("/my/home/")
		else:
			loginURL = users.create_login_url("/postlogin/")

			template = jinja_env.get_template('landing.template')
			self.response.out.write(template.render(loginURL=loginURL))

class PageMyHome(webapp2.RequestHandler):
	def get(self):
		gUser = users.get_current_user()
		if not gUser:
			self.redirect("/login/")
		else:
			user = getUserEntry(gUser).get()

			template = jinja_env.get_template('myhome.template')
			self.response.out.write(template.render(user=user))

class PageProfile(webapp2.RequestHandler):
	def get(self):
		gUser = users.get_current_user()
		if not gUser:
			self.redirect("/login/")
		else:
			user = getUserEntry(gUser).get()

			tUserId = self.request.get("user")

			tSelf = False
			if not tUserId:
				tUserId = gUser.user_id()
				tSelf = True

			tUser = ndb.gql("SELECT * FROM EntryUser WHERE userid = :1", tUserId).get()

			template = jinja_env.get_template('profile.template')
			self.response.out.write(template.render(
					user=user,
					tUser=tUser,
					tSelf=tSelf
					))

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

			query = self.request.get("query")
			results = None
			if query:
				classid = None
				try:
					classid = query # TODO: Determine purpose of try
				except ValueError:
					results = ndb.gql("SELECT * FROM EntryClass WHERE classname = :1", classid).fetch(200)
				else:
					results = ndb.gql("SELECT * FROM EntryClass WHERE classid = :1", classid).fetch(200)

			template = jinja_env.get_template('classsearch.template')
			self.response.out.write(template.render(
					user=user,
					query=query,
					results=results
					))

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
							entry.scores[user.userid] = 0
						elif user.usertype in ["Teacher", "Administrator"]:
							entry.teachers.append(userKey)

						entry.put()

						self.redirect("/class/challenges?class=%s" %(classget) )

class PageClassCreate(webapp2.RequestHandler):
	def get(self):
		gUser = users.get_current_user()
		user = getUserEntry(gUser).get()
		if not gUser:
			self.redirect("/login/")
		elif not user.usertype == "Teacher":
			self.redirect("/class/search/")
		else:
			template = jinja_env.get_template('classcreate.template')
			self.response.out.write(template.render(user=user))

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

class PageClassChallenges(webapp2.RequestHandler):
	def get(self):
		gUser = users.get_current_user()
		if not gUser:
			self.redirect("/login/")
		else:
			classid = self.request.get("class")
			user = getUserEntry(gUser).get()
			class_ = ndb.gql("SELECT * FROM EntryClass WHERE classid = :1", classid).get()

			template = jinja_env.get_template('classchallenges.template')
			self.response.out.write(template.render(
					user=user,
					class_=class_
					))

class PageClassManage(webapp2.RequestHandler): ##HERE## Convert to template
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
			#subvalues["studentsHTML"] = "".join([studentKey.get().username for studentKey in class_.students])

			subvalues["studentsHTML"] = ""
			for studentKey in class_.students:
				student = studentKey.get()
				score = class_.scores[student.userid] ##HERE##
				subvalues["studentsHTML"] += '''
					<tr><td>
						<a href="/profile?user=%(userid)s">%(username)s</a>
					</td><td>
						<input type="number" class="table-score-editable" name="score%(userid)s" value="%(score)s" />
					</td></tr>
					''' %{"userid": student.userid, "username": student.username, "score": score}

			contentHTML = '''
<form id="table-form" action="/class/manage?class=%(classid)s" method="POST">
	<table id="class-info-table">
		<tr>
			<th class="table-name">Class Name</td>
			<td class="table-value-editable">
				<input type="text" name="classname" value="%(classname)s" />
			</td>
		</tr> <tr>
			<th class="table-name">Class ID</td>
			<td class="table-value">%(classid)s</td>
		</tr> <tr>
			<th class="table-name">Teachers</td>
			<td class="table-value">%(teachersHTML)s</td>
		</tr>
	</table>
	<table id="class-student-table">
		<tr>
			<th colspan="2">Students</th>
		</tr>
		%(studentsHTML)s
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
			template = jinja_env.get_template('postlogin.template') ##TODO: User Creation includes optional Fullname entry
			self.response.out.write(template.render())
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

jinja_env = jinja2.Environment(
		loader=jinja2.FileSystemLoader("templates")
		#extensions=['jinja2.ext.autoescape'],
		#line_statement_prefix="#",
		#line_comment_prefix="##"
		)

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
		], debug=True
		)
