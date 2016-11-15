
## PERFORMATRIX ###

#########################################################################
## FIRST CONTROLLER TO GET CALLED
## SHOWS THE index.html , FIRST PAGE TO BE DISPLAYED
########################################################################


de index():
	'''Login Form generated here and passed to the index page '''
	form=FORM(LABEL('Username:'), 
			INPUT(_name='username', _value = '', _class = 'text-input',_required = 'on', requires=IS_NOT_EMPTY()), 
			BR (_style='clear: both;'),
			LABEL('Password:'), 
			INPUT(_name='password' ,_type='password', _value = '', _class = 'text-input',_required = 'on', requires=IS_NOT_EMPTY()),
			BR (_style='clear: both;'),
			BR (_style='clear: both;'),
			INPUT(_type='submit', _class = 'button', _value = 'Sign In'),
			_action = 'setUserPref',
			_method = 'post')
	'''Shows error message on the wrong login'''
	a = 'Please login to continue'
	if request.vars.a == "Invalid_Login":
		a = "Wrong Username/Password"
	elif request.vars.a == "Session_over":
		a = "Session timeout"
	elif request.vars.a == "logged_out":
		a = "User logged out"
	else:
		a = 'Please login to continue'
		
	return dict(form=form,
				a = a)

def setUserPref():
	flag = 0
	for row in db(db.login_tab).select():
		if row.username == request.vars.username and row.password == request.vars.password:
			session.empid = row.username
			session.roleid = row.role_id
			flag = 1
	
	if flag == 0:
		redirect(URL('index',vars=dict(a='Invalid_Login')))
	
	print "Session role id : ", session.roleid
	print "Session empid : ", session.empid
	if session.roleid == '0':
		redirect(URL('aDashboard'))
	else:
		redirect(URL('eDashboard'))
	return dict()


def checkSession():
	sval = 0;
	if session.empid == '' or session.roleid == '':
		sval = 1;
	return sval

def aDashboard():
	print "inAdashboard"
	sval = checkSession()
	if sval == 1:
		redirect(URL('index',vars=dict(a='Session_over')))

	return dict()	


def addEmployee():
	sval = checkSession()
	if sval == 1:
		redirect(URL('index',vars=dict(a='Session_over')))

	return dict()

def addEmpProcess():
	sval = checkSession()
	if sval == 1:
		redirect(URL('index',vars=dict(a='Session_over')))
	
	try:
		input_empid = request.vars.new_emp_id
		epassword = request.vars.epass
		nrole =  request.vars.role
	except:
		session.flash = "Data Not Inserted"
		redirect(URL('addEmployee', vars=dict(a = 'value not submitted')))
	else:
		db.login_tab.update_or_insert((db.login_tab.username == input_empid),
		username = input_empid,
		password = epassword,
		role_id = nrole)
		session.flash = "Data Inserted"
		redirect(URL('addEmployee', vars=dict(a = 'value submittted')))
	
	return dict()

def removeEmployee():
	sval = checkSession()
	if sval == 1:
		redirect(URL('index',vars=dict(a='Session_over')))

	return dict()

def removeEmpProcess():
	sval = checkSession()
	if sval == 1:
		redirect(URL('index',vars=dict(a='Session_over')))
	
	rem_id = request.vars.remEmp

	try:	
		db(db.login_tab.username == rem_id).delete()
		db(db.self_eval_tab.EmployeeId == rem_id).delete()
		db(db.emp_skill.EmployeeId == rem_id).delete()
		db(db.team_eval_tab.EmployeeId == rem_id).delete()
		db(db.emp_details_tab.EmployeeId == rem_id).delete()
	except:
		session.flash = "Data Not Removed"
		redirect(URL('removeEmployee',vars=dict(a='Employee Not removed')))
	else:
		session.flash = "Data Removed"
		redirect(URL('removeEmployee',vars=dict(a='Employee removed')))
	return dict()

def addSkill():
	sval = checkSession()
	if sval == 1:
		redirect(URL('index',vars=dict(a='Session_over')))

	return dict()

def addSkillProcess():
	sval = checkSession()
	if sval == 1:
		redirect(URL('index',vars=dict(a='Session_over')))

	sk = request.vars.nskill
	try:
		db.skill_table.insert(skill_desc = sk)
	except:
		session.flash = "Skill Not Added"
		redirect(URL('addSkill',vars=dict(a='skill not added')))
	else:
		session.flash = "Skill Added"
		redirect(URL('addSkill',vars=dict(a='skill added')))
	return dict()

def iReport():
	genId = request.vars.iEmp
	sval = checkSession()
	if sval == 1:
		redirect(URL('index',vars=dict(a='Session_over')))
	
	logged_first_username = 'Please Select '
	logged_last_username = ''
	import pygal
	from pygal.style import LightStyle
	pie_chart = pygal.Pie(
				width=500,
				height=300,
				explicit_size=True)
	
	if genId == 'None':
		return dict(fname = logged_first_username,
				lname = logged_last_username,
				pchart = pie_chart.render())
		
	
	self_v = 0
	team_v = 0
	final = 0
	
	for firstrow in db(db.emp_details_tab.EmployeeId == genId).select():
		logged_first_username = firstrow.FirstName
		logged_last_username = firstrow.LastName
	
	for sw in db(db.self_eval_tab.EmployeeId == genId).select():
		self_v = sw.Overall
	
	for rw in db(db.team_eval_tab.EmployeeId == genId).select():
		team_v = rw.toverall
		
	if self_v == 0 or team_v == 0:
		final = self_v + team_v
	else:
		final = 0.4 * self_v + 0.6 * team_v
	
	
	pie_chart.title = 'Overall Suitability (in %)'
	pie_chart.add('Suitable', final)
	pie_chart.add('Not Suitable', 100 - final)
	
	return dict(fname = logged_first_username,
				lname = logged_last_username,
				pchart = pie_chart.render())

def tCapacity():
	
	if request.vars.iCap == 'None':
		cId = 0
	else:
		cId = int(request.vars.iCap or 0)
		
	sval = checkSession()
	if sval == 1:
		redirect(URL('index',vars=dict(a='Session_over')))
	cName = ''
	import pygal
	from pygal.style import LightStyle
	pie_chart = pygal.Pie(
				width=500,
				height=300,
				explicit_size=True)
	
	print "cid :",cId
	if cId == 0:
		return dict(cName = cName,
				pchart = pie_chart.render())
		
	pCount = 0
	sCount = 0
	eCount = 0
	lCount = 0
	count = 0
	for firstrow in db(db.skill_table.id == cId).select():
		cName = firstrow.skill_desc
	
	print "cid : ",cId
	for srow in db(db.emp_skill).select():
		count += 1
		if srow.priskill == cId:
			pCount += 1
		if srow.secskill == cId:
			sCount += 1
		if srow.expskill == cId:
			eCount += 1
		if srow.learnskill == cId:
			lCount += 1
	
	p =  ( (pCount * 100 )/ count ) 
	s =  ( (sCount * 100 )/ count ) 
	e =  ( (eCount * 100 )/ count ) 
	l =  ( (lCount * 100 )/ count ) 
	
	
	pie_chart.title = 'Capbility  (in %)'
	pie_chart.add('Proficient Skill', p)
	pie_chart.add('Intermediate Skill ', s)
	pie_chart.add('Expert Skill', e)
	pie_chart.add('In Learning ', l)
	pie_chart.add('Non -'+cName, 100 - p - s - e - l)
	
	return dict(cName = cName,
				pchart = pie_chart.render())


def eDashboard():
	print "inEdashboard"
	sval = checkSession()
	if sval == 1:
		redirect(URL('index',vars=dict(a='Session_over')))
	active_role = ''
	logged_first_username = ' Please refer to the '
	logged_last_username = 'Add Details Page and Fill your details .'
	'''Brings out the Role Description '''
	for newrow in db(db.role_table.role_id == session.roleid).select():
		active_role = newrow.role_desc
	'''Brings out the Employee Name '''
	for firstrow in db(db.emp_details_tab.EmployeeId == session.empid).select():
		logged_first_username = firstrow.FirstName
		logged_last_username = firstrow.LastName
	flag = 0
	'''Display certain option based on the role of the logged in user'''
	if int(float(session.roleid)) > 1:
		flag = 1
	return locals()
	

def temp():
	return dict()

def logout():
	session.empid = ''
	session.roleid = ''
	redirect(URL('index',vars=dict(a='logged_out')))

def addDetails():
	sval = checkSession()
	if sval == 1:
		redirect(URL('index',vars=dict(a='Session_over')))
	
	record = db.emp_details_tab(db.emp_details_tab.EmployeeId == session.empid)
	form = SQLFORM(db.emp_details_tab, record, submit_button = 'Insert/Update Data')
	form.custom.submit['_class'] = 'button'
	form.custom.widget.EmployeeId['_value'] = session.empid
	form.custom.widget.EmployeeId['_readonly'] = 'ON'
	form.custom.widget.DOB['autocomplete'] = 'OFF'
	form.custom.widget.FirstName['_required'] = 'ON'
	form.custom.widget.LastName['_required'] = 'ON'
	form.custom.widget.DOB['_required'] = 'ON'
	form.custom.widget.CurrentPosition['_required'] = 'ON'
	form.custom.widget.ProficientSkill['_required'] = 'ON'
	form.custom.widget.IntermediateSkill['_required'] = 'ON'
	form.custom.widget.BasicSkill['_required'] = 'ON'
	form.custom.widget.ManagerId['_required'] = 'ON'
	flag = 0
	'''Display certain option based on the role of the logged in user'''
	if int(float(session.roleid)) > 1:
		flag = 1
	
	if form.process(keepvalues=True).accepted:
		response.flash = T("Form accepted")
	elif form.errors:
		response.flash = T("Form has errors")
	else:
		response.flash = T("Please fill out the form")
	return dict(form=form,
				flag = flag)

def selfEvaluate():
	sval = checkSession()
	if sval == 1:
		redirect(URL('index',vars=dict(a='Session_over')))
	
	flag = 0
	'''Display certain option based on the role of the logged in user'''
	if int(float(session.roleid)) > 1:
		flag = 1
	
	return dict(flag = flag)

'''Best value = 80
	   Worst value = 0'''
def selfEvaluate_process():
	
	sval = checkSession()
	if sval == 1:
		redirect(URL('index',vars=dict(a='Session_over')))
		
	try:
		empid = session.empid
		competency = 2 * int(float(request.vars.Competency))
		focussed =  2 * int(float(request.vars.Focussed))
		adaptable = 2 * int(float(request.vars.Adaptable))
		consistent = 2 * int(float(request.vars.Consistent))
		proactive = 2 * int(float(request.vars.Proactive))
		obthinker = 2 * int(float(request.vars.OutOfBoxthinker))
		absentmind = 2 * int(float(request.vars.AbsentMinded))
		optimistic = 2 * int(float(request.vars.Optimistic))
		uncomp = 2 * int(float(request.vars.Uncompromising))
		strat = 2 * int(float(request.vars.Strategist))
		overall = competency + focussed + adaptable + consistent + proactive + obthinker - absentmind + optimistic - uncomp + strat + 4
	except:
		session.flash = "Data Not Inserted"
		redirect(URL('selfEvaluate', vars=dict(a = 'value not submitted')))
	else:
		db.self_eval_tab.update_or_insert((db.self_eval_tab.EmployeeId== session.empid),
		EmployeeId = empid,
		Competency = competency,
		Focussed = focussed,
		Adaptable = adaptable,
		Consistent = consistent,
		Proactive = proactive,
		OutOfBoxthinker = obthinker,
		AbsentMinded = absentmind,
		Optimistic = optimistic,
		Uncompromising = uncomp,
		Strategist = strat,
		Overall = overall)
		session.flash = "Data Inserted"
		redirect(URL('selfEvaluate', vars=dict(a = 'value submittted')))
			
	return dict()
	
def myperformance():
	sval = checkSession()
	if sval == 1:
		redirect(URL('index',vars=dict(a='Session_over')))
	
	logged_id = session.empid
	logged_first_username = ''
	logged_last_username = ''
	nlist = []
	svalue = 0
	for firstrow in db(db.emp_details_tab.EmployeeId == logged_id).select():
		logged_first_username = firstrow.FirstName
		logged_last_username = firstrow.LastName
	
	flag = 0
	'''Display certain option based on the role of the logged in user'''
	if int(float(session.roleid)) > 1:
		flag = 1
		
	for frow in db(db.self_eval_tab.EmployeeId == logged_id).select():
		svalue = frow.Overall * 1.25
		nlist.append(frow.Competency)
		nlist.append(frow.Focussed)
		nlist.append(frow.Adaptable)
		nlist.append(frow.Consistent)
		nlist.append(frow.Proactive)
		nlist.append(frow.OutOfBoxthinker)
		nlist.append(frow.AbsentMinded)
		nlist.append(frow.Optimistic)
		nlist.append(frow.Uncompromising)
		nlist.append(frow.Strategist)
		nlist.append((frow.Overall * 1.25) / 10)
	
	plist = []
	pvalue = 0
	for trow in db(db.team_eval_tab.EmployeeId == logged_id).select():
		pvalue = trow.toverall
		plist.append(trow.HumanCharacter)
		plist.append(trow.Interpersonal)
		plist.append(trow.BuildingTalent)
		plist.append(trow.Leadership)
		plist.append(trow.Communication)
		plist.append(trow.JobPerformance)
		plist.append(trow.MutualUnderstanding)
		plist.append(trow.Knowledge)
		plist.append(trow.toverall)
	
	emp_hist = []
	hist_date = []
	for mrow in db(db.emp_hist_tab.EmployeeId == logged_id).select():	
		emp_hist.append( 0.4 * mrow.self_overall + 0.6 * mrow.team_overall)
		hist_date.append(str(mrow.edate))
	
	print emp_hist, hist_date
	
	import pygal
	from pygal.style import LightStyle
	bar_chart = pygal.Bar( 
				width=600,
	            height=300,
				explicit_size=True,
				x_label_rotation=-340) # Then create a bar graph object
	bar_chart.title = 'Self Rated Performance (in %)'
	'''values = [0,2,4,6,8,10]
	bar_chart.y_labels = map(str, values)'''
	bar_chart.add('Ratings', nlist)
	bar_chart.x_labels = ['Competency', 'Focussed', 'Adaptable', 'Consistent', 'Proactive', 'Out of Box thinker', 'Absent Minded', 'Optimistic', 'Uncompromising', 'Strategist','Overall']
	
	pie_chart = pygal.Pie(
				width=500,
				height=300,
				explicit_size=True)
	pie_chart.title = 'Self Suitability (in %)'
	pie_chart.add('Suitable', svalue);
	pie_chart.add('Not Suitable', 100 - svalue)
	
	rbar_chart = pygal.Bar( 
				width=600,
	            height=300,
				explicit_size=True,
				x_label_rotation=-340) # Then create a bar graph object
	rbar_chart.title = 'Recommended Rated Performance (in %)'
	rbar_chart.add('Ratings', plist)
	rbar_chart.x_labels = ['Human Character', 'Interpersonal', 'Building Talent', 'Leadership', 'Communication', 'Job Performance', 'Mutual Understanding', 'Knowledge', 'Overall']
	
	rpie_chart = pygal.Pie(
				width=500,
				height=300,
				explicit_size=True)
	rpie_chart.title = 'Recommended Suitability (in %)'
	rpie_chart.add('Suitable', pvalue);
	rpie_chart.add('Not Suitable', 100 - pvalue)
	
	
	line_chart = pygal.Line(
				width=600,
				height=300,
				explicit_size=True)
	line_chart.title = 'Employee Performance history (in %)'
	line_chart.x_labels = hist_date
	line_chart.add("Performance", emp_hist);
	return dict(
			fname = logged_first_username,
			lname = logged_last_username,
			chart = bar_chart.render(),
			pchart = pie_chart.render(),
			rchart = rbar_chart.render(),
			rpchart = rpie_chart.render(),
			lchart = line_chart.render(),
			flag = flag
			)
	
def overallRating():
	flag = 0
	'''Display certain option based on the role of the logged in user'''
	if int(float(session.roleid)) > 1:
		flag = 1
	sval = checkSession()
	if sval == 1:
		redirect(URL('index',vars=dict(a='Session_over')))
	import pygal
	from pygal.style import LightStyle
	self_v = 0
	team_v = 0
	final = 0
	logged_first_username = ''
	logged_last_username = ''
	
	for firstrow in db(db.emp_details_tab.EmployeeId == session.empid).select():
		logged_first_username = firstrow.FirstName
		logged_last_username = firstrow.LastName
	
	for sw in db(db.self_eval_tab.EmployeeId == session.empid).select():
		self_v = sw.Overall
	
	for rw in db(db.team_eval_tab.EmployeeId == session.empid).select():
		team_v = rw.toverall
		
	if self_v == 0 or team_v == 0:
		final = self_v + team_v
	else:
		final = 0.4 * self_v + 0.6 * team_v
	
	pie_chart = pygal.Pie(
				width=500,
				height=300,
				explicit_size=True)
	pie_chart.title = 'Overall Suitability (in %)'
	pie_chart.add('Suitable', final)
	pie_chart.add('Not Suitable', 100 - final)
	
	return dict(flag = flag,
				fname = logged_first_username,
				lname = logged_last_username,
				pchart = pie_chart.render())
	
def rateTeam():
	sval = checkSession()
	if sval == 1:
		redirect(URL('index',vars=dict(a='Session_over')))
		
	logged_id = session.empid
	flag = 0
	'''Display certain option based on the role of the logged in user'''
	if int(float(session.roleid)) > 1:
		flag = 1
	
	return dict(flag = flag)

def rateTeam_process():
	sval = checkSession()
	if sval == 1:
		redirect(URL('index',vars=dict(a='Session_over')))
	
	logged_id = session.empid
	
	from datetime import datetime
	i = datetime.now().date()
	
	print i
	try:
		input_emp_id = request.vars.select_emp
		c1 = 2 * int (float(request.vars.c1))
		c2 = 2 * int (float(request.vars.c2))
		c3 = 2 * int (float(request.vars.c3))
		c4 = 2 * int (float(request.vars.c4))
		c5 = 2 * int (float(request.vars.c5))
		c6 = 2 * int (float(request.vars.c6))
		character = ( ( c1 + c2 + c3 + c4 + c5 + c6 - 12 ) * 100 ) / 48 
		'''
			formula = ( (total - lower_bound) * 100 ) / higher_bound - lower_bound
		'''
	
		i1 = 2 * int (float(request.vars.i1))
		i2 = 2 * int (float(request.vars.i2))
		i3 = 2 * int (float(request.vars.i3))
		i4 = 2 * int (float(request.vars.i4))
		i5 = 2 * int (float(request.vars.i5))
		interpersonal = ( (i1 + i2 + i3 + i4 + i5 - 10 ) * 100 ) / 40 
		
		b1 = 2 * int (float(request.vars.b1))
		b2 = 2 * int (float(request.vars.b2))
		b3 = 2 * int (float(request.vars.b3))
		b4 = 2 * int (float(request.vars.b4))
		b5 = 2 * int (float(request.vars.b5))
		btalent = ( (b1 + b2 + b3 + b4 + b5 - 10) * 100 ) / 40
		
		l1 = 2 * int (float(request.vars.l1))
		l2 = 2 * int (float(request.vars.l2))
		l3 = 2 * int (float(request.vars.l3))
		l4 = 2 * int (float(request.vars.l4))
		l5 = 2 * int (float(request.vars.l5))
		l6 = 2 * int (float(request.vars.l5))
		leadership = ( (l1 + l2 + l3 + l4 + l5 + l6 - 12 ) * 100 ) / 48
		
		co1 = 2 * int (float(request.vars.co1))
		co2 = 2 * int (float(request.vars.co2))
		co3 = 2 * int (float(request.vars.co3))
		co4 = 2 * int (float(request.vars.co4))
		co5 = 2 * int (float(request.vars.co5))
		comm = ( ( co1 + co2 + co3 + co4 + co5 - 10 ) * 100 ) / 40 
		
		j1 = 2 * int (float(request.vars.j1))
		j2 = 2 * int (float(request.vars.j2))
		j3 = 2 * int (float(request.vars.j3))
		j4 = 2 * int (float(request.vars.j4))
		j5 = 2 * int (float(request.vars.j5))
		j6 = 2 * int (float(request.vars.j6))
		j7 = 2 * int (float(request.vars.j7))
		j8 = 2 * int (float(request.vars.j8))
		j9 = 2 * int (float(request.vars.j9))
		jobPer = ( ( j1 + j2 + j3 + j4 + j5 + j6 + j7 + j8 + j9 - 18 ) * 100 ) / 72
		
		
		m1 = 2 * int (float(request.vars.m1))
		m2 = 2 * int (float(request.vars.m2))
		m3 = 2 * int (float(request.vars.m3))
		m4 = 2 * int (float(request.vars.m4))
		m5 = 2 * int (float(request.vars.m5))
		m6 = 2 * int (float(request.vars.m6))
		m7 = 2 * int (float(request.vars.m7))
		m8 = 2 * int (float(request.vars.m8))
		m9 = 2 * int (float(request.vars.m9))
		mutualUn = ( (m1 + m2 + m3 + m4 + m5 + m6 + m7 + m8 + m9 - 18 ) * 100 ) / 72


		k1 = 2 * int (float(request.vars.k1))
		k2 = 2 * int (float(request.vars.k2))
		k3 = 2 * int (float(request.vars.k3))
		k4 = 2 * int (float(request.vars.k4))
		k5 = 2 * int (float(request.vars.k5))
		k6 = 2 * int (float(request.vars.k6))
		k7 = 2 * int (float(request.vars.k7))
		knowledge = ( ( k1 + k2 + k3 + k4 + k5 + k6 + k7 - 14 ) * 100 ) / 56
		
		toverall = ( character + interpersonal + btalent + leadership + comm + jobPer + mutualUn + knowledge ) / 8
		
		suggest = request.vars.suggest
		
		so = 0
		for sw in db(db.self_eval_tab).select():
			if sw.EmployeeId == input_emp_id:
				so = sw.Overall
		
		'''print so'''
		
	except:
		session.flash = "Data Not Inserted"
		redirect(URL('rateTeam', vars=dict(a = 'value not submitted')))
	else:
		db.team_eval_tab.update_or_insert((db.team_eval_tab.EmployeeId == input_emp_id),
		EmployeeId = input_emp_id,
		HumanCharacter = character,
		Interpersonal = interpersonal,
		BuildingTalent = btalent,
		Leadership = leadership,
		Communication = comm,
		JobPerformance = jobPer,
		MutualUnderstanding = mutualUn,
		Knowledge = knowledge,
		toverall = toverall,
		suggested = suggest)
		
		db.emp_hist_tab.insert(EmployeeId = input_emp_id,
		edate = i,
		self_overall = so,
		team_overall = toverall)
		session.flash = "Data Inserted"
		redirect(URL('rateTeam', vars=dict(a = 'value submittted')))
			
	return dict()

def suggestions():
	logged_id = session.empid
	flag = 0
	'''Display certain option based on the role of the logged in user'''
	if int(float(session.roleid)) > 1:
		flag = 1
		
	sval = checkSession()
	if sval == 1:
		redirect(URL('index',vars=dict(a='Session_over')))
		
	fname = ''
	lname = ''
	suggest = ''
	for firstrow in db(db.emp_details_tab.EmployeeId == session.empid).select():
		fname= firstrow.FirstName
		lname = firstrow.LastName
	
	for trow in db(db.team_eval_tab.EmployeeId == session.empid).select():
		suggest = trow.suggested
	
	return dict(flag = flag,
				fname = fname,
				lname = lname,
				suggest = suggest)

def mySkill():
	sval = checkSession()
	if sval == 1:
		redirect(URL('index',vars=dict(a='Session_over')))
		
	logged_id = session.empid
	flag = 0
	'''Display certain option based on the role of the logged in user'''
	if int(float(session.roleid)) > 1:
		flag = 1
	
	return dict(flag = flag)
	
def mySkillProcess():
	sval = checkSession()
	if sval == 1:
		redirect(URL('index',vars=dict(a='Session_over')))
	
	try:
		empid = session.empid
		pskill = request.vars.pskill
		sskill =  request.vars.sskill
		eskill = request.vars.eskill
		lskill = request.vars.lskill
	except:
		session.flash = "Data Not Inserted"
		redirect(URL('mySkill', vars=dict(a = 'not submitted')))
	else:
		db.emp_skill.update_or_insert((db.emp_skill.EmployeeId== session.empid),
		EmployeeId = empid,
		priskill = pskill,
		secskill = sskill,
		expskill = eskill,
		learnskill = lskill)
		session.flash = "Data Inserted"
		redirect(URL('mySkill', vars=dict(a = 'value submittted')))
	return dict()







def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())

@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_signature()
def data():
    """
    http://..../[app]/default/data/tables
    http://..../[app]/default/data/create/[table]
    http://..../[app]/default/data/read/[table]/[id]
    http://..../[app]/default/data/update/[table]/[id]
    http://..../[app]/default/data/delete/[table]/[id]
    http://..../[app]/default/data/select/[table]
    http://..../[app]/default/data/search/[table]
    but URLs must be signed, i.e. linked with
      A('table',_href=URL('data/tables',user_signature=True))
    or with the signed load operator
      LOAD('default','data.load',args='tables',ajax=True,user_signature=True)
    """
    return dict(form=crud())
