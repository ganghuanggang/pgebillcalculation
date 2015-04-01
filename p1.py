import re
import datetime
s="Electric usage,2014-03-01,00:00,00:59,0.45,kWh,$0.07,"
f='test.csv'
f="pge_electric_interval_data_9598747157_2014-03-01_to_2015-02-28.csv"
s=open(f).read()
totalhours=0
totaldollars=0
hourbill=[];
for s in open(f).read().split('\n'):
	m=re.match('Electric usage,(\d+)-(\d+)-(\d+),(\d+):00,(\d+):59,([\.\d]+),kWh,\$([\.\d]+)',s)
	if m:
		totalhours+=1
		ymdhhpd=m.groups()
		year=int(ymdhhpd[0])
		month=int(ymdhhpd[1])
		day=int(ymdhhpd[2])
		hour=int(ymdhhpd[3])
		power=float(ymdhhpd[5])
		dollar=float(ymdhhpd[6])
		weekday=datetime.date(year,month,day).weekday()
		holiday=[(1,1),(2,16),(5,26),(7,4),(9,1),(11,11),(11,27),(12,25)]
		totaldollars+=dollar
		newline={'year':year,'month':month,'day':day,'hour':hour,'power':power,'dollar':dollar,'weekday':weekday,'holiday':(month,day) in holiday}
		hourbill.append(newline)

def calEVA(hourbill):	
	nohomehours=0
	nohomepowers=0
	peaksummer=0
	peakwinter=0
	offpeaksummer=0
	offpeakwinter=0
	partialpeaksummer=0
	partialpeakwinter=0
	hpeaksummer=0
	hpeakwinter=0
	hoffpeaksummer=0
	hoffpeakwinter=0
	hpartialpeaksummer=0
	hpartialpeakwinter=0
	print '####  EVA ####'
	for line in hourbill:
			if line['holiday'] or line['weekday'] >=6:
				if line['month']>=5 and line['month'] <=10:
					if line['hour']>=15 and line['hour'] <19:
						peaksummer+=line['power']
						hpeaksummer+=1
					else:
						hoffpeaksummer+=1
						offpeaksummer+=line['power']
				else:
					if line['hour']>=15 and line['hour'] <19:
						hpeakwinter+=1
						peakwinter+=line['power']
					else:
						hoffpeakwinter+=1
						offpeakwinter+=line['power']
			else:
				if line['month']>=5 and line['month'] <=10:
					if line['hour']>=14 and line['hour'] <21:
						hpeaksummer+=1
						peaksummer+=line['power']
					elif (line['hour']>=7 and line['hour'] <14) or (line['hour'] >=21 and line['hour'] < 23):
						partialpeaksummer+=line['power']
						hpartialpeaksummer+=1
					else:
						hoffpeaksummer+=1
						offpeaksummer+=line['power']
				else:
					if line['hour']>=14 and line['hour'] <21:
						hpeakwinter+=1
						peakwinter+=line['power']
					elif (line['hour']>=7 and line['hour'] <14) or (line['hour'] >=21 and line['hour'] < 23):
						partialpeakwinter+=line['power']
						hpartialpeakwinter+=1
					else:
						hoffpeakwinter+=1
						offpeakwinter+=line['power']
		
				if line['month']==2 and (line['hour']<=18 or line['hour'] >=22):
					nohomehours+=1;
					nohomepowers+=line['power'];
	print totalhours,totaldollars,nohomehours,nohomepowers,nohomepowers*1.0/nohomehours
	print [peaksummer,partialpeaksummer,offpeaksummer,peakwinter,partialpeakwinter,offpeakwinter]
	print [hpeaksummer,hpartialpeaksummer,hoffpeaksummer,hpeakwinter,hpartialpeakwinter,hoffpeakwinter]
	totalcost=peaksummer*0.42225+partialpeaksummer*0.22276+offpeaksummer*0.09952+peakwinter*0.28781+partialpeakwinter*0.17062+offpeakwinter*0.10238
	totalcost1=peaksummer*0.42225+partialpeaksummer*0.22276+(offpeaksummer+250*12)*0.09952+peakwinter*0.28781+partialpeakwinter*0.17062+offpeakwinter*0.10238
	print 'yeartotal:',totalcost, totalcost1


class bill:
	def __init__(self,startdate,enddate):
		self.power=0
		self.price=0
		self.baseline=0
	def belonghere(self,date):
		pass

	
print '########    E6      #########'
def calE6(hourbill):
	billingdate=[datetime.date(2014,2,1),datetime.date(2014,3,1),datetime.date(2014,4,1),datetime.date(2014,5,1),datetime.date(2014,6,1),datetime.date(2014,7,1),datetime.date(2014,8,1),datetime.date(2014,9,1),datetime.date(2014,10,1),datetime.date(2014,11,1),datetime.date(2014,12,1),datetime.date(2015,1,1),datetime.date(2015,2,1)]
	if datetime.date(2014,5,1) not in billingdate:
		billingdate.append(datetime.date(2014,5,1))
	if datetime.date(2014,11,1) not in billingdate:
		billingdate.append(datetime.date(2014,11,1))
	date0=datetime.date(hourbill[0]['year'],hourbill[0]['month'],hourbill[0]['day'])
	date1=datetime.date(hourbill[-1]['year'],hourbill[-1]['month'],hourbill[-1]['day'])
	print len(billingdate)
	if date0 not in billingdate:
		billingdate.append(date0)
	if date1 not in billingdate:
		billingdate.append(date1)
	billingdate.sort()
	powerusage=(len(billingdate)-1)*[{}]
	for imon in range(len(billingdate)-1):
		powerusage[imon]={'sp':0,'spp':0,'so':0,'wp':0,'wpp':0,'wo':250};
	for line in hourbill:
		date=datetime.date(line['year'],line['month'],line['day'])
		hour=line['hour']
		power=line['power']
		for imon in range(len(billingdate)-1):
			if billingdate[-1] < date:
				powerusage[-1][calE6pptype(date,hour)]+=power;
			elif billingdate[imon] <=date <billingdate[imon+1]:
				powerusage[imon][calE6pptype(date,hour)]+=power;
			elif billingdate[0] > date:
				powerusage[0][calE6pptype(date,hour)]+=power;
	print 'here',date0,date1,len(billingdate)
	totalcost=0
	for imon in range(len(powerusage)-1):
		totalusage=1.0*sum(powerusage[imon].values())
		sppercent=0 if powerusage[imon]['sp']==0 else (powerusage[imon]['sp'])/totalusage
		spppercent=0 if powerusage[imon]['spp']==0 else (powerusage[imon]['spp'])/totalusage
		sopercent=0 if powerusage[imon]['so']==0 else (powerusage[imon]['so'])/totalusage
		wppercent=0 if powerusage[imon]['wp']==0 else (powerusage[imon]['wp'])/totalusage
		wpppercent=0 if powerusage[imon]['wpp']==0  else (powerusage[imon]['wpp'])/totalusage
		wopercent=0 if powerusage[imon]['wo']==0  else(powerusage[imon]['wo'])/totalusage
		totalbaseline=calbaseline(billingdate[imon],billingdate[imon+1])
		if totalusage/totalbaseline<=1.0:
			totalcost+=powerusage[imon]['sp']*0.32306+powerusage[imon]['spp']*0.20779+powerusage[imon]['so']*0.13101+powerusage[imon]['wp']*0.0+powerusage[imon]['wpp']*0.15218+powerusage[imon]['wo']*0.13535
		elif totalusage/totalbaseline<=1.3:
			totalcost+=(totalbaseline*sppercent*0.32306+totalbaseline*spppercent*0.20779+totalbaseline*sopercent*0.13101
		+totalbaseline*wppercent*0.0+totalbaseline*wpppercent*0.15218+totalbaseline*wopercent*0.13535
		+(powerusage[imon]['sp']-totalbaseline*sppercent)*0.34627
		+(powerusage[imon]['spp']-totalbaseline*spppercent)*0.23100
		+(powerusage[imon]['so']-totalbaseline*sopercent)*0.15423
		+(powerusage[imon]['wp']-totalbaseline*wppercent)*0.0
		+(powerusage[imon]['wpp']-totalbaseline*wpppercent)*0.17539
		+(powerusage[imon]['wo']-totalbaseline*wopercent)*0.15856)
		elif totalusage/totalbaseline<=2.0: 
			totalcost+=(totalbaseline*sppercent*0.32306+totalbaseline*spppercent*0.20779+totalbaseline*sopercent*0.13101
		+totalbaseline*wppercent*0.0+totalbaseline*wpppercent*0.15218+totalbaseline*wopercent*0.13535
		+(totalbaseline*sppercent*0.3)*0.34627
		+(totalbaseline*spppercent*0.3)*0.23100
		+(totalbaseline*sopercent*0.3)*0.15423
		+(totalbaseline*wppercent*0.3)*0.0
		+(totalbaseline*wpppercent*0.3)*0.17539
		+(totalbaseline*wopercent*0.3)*0.15856
		+(powerusage[imon]['sp']-totalbaseline*sppercent*1.3)*0.43368
		+(powerusage[imon]['spp']-totalbaseline*spppercent*1.3)*0.31841
		+(powerusage[imon]['so']-totalbaseline*sopercent*1.3)*0.24163
		+(powerusage[imon]['wp']-totalbaseline*wppercent*1.3)*0.0
		+(powerusage[imon]['wpp']-totalbaseline*wpppercent*1.3)*0.26280
		+(powerusage[imon]['wo']-totalbaseline*wopercent*1.3)*0.24597)
		elif totalusage/totalbaseline<=3.0:
			totalcost+=(totalbaseline*sppercent*0.32306+totalbaseline*spppercent*0.20779+totalbaseline*sopercent*0.13101
		+totalbaseline*wppercent*0.0+totalbaseline*wpppercent*0.15218+totalbaseline*wopercent*0.13535
		+(totalbaseline*sppercent*0.3)*0.34627
		+(totalbaseline*spppercent*0.3)*0.23100
		+(totalbaseline*sopercent*0.3)*0.15423
		+(totalbaseline*wppercent*0.3)*0.0
		+(totalbaseline*wpppercent*0.3)*0.17539
		+(totalbaseline*wopercent*0.3)*0.15856
		+(totalbaseline*sppercent*0.7)*0.43368
		+(totalbaseline*spppercent*0.7)*0.31841
		+(totalbaseline*sopercent*0.7)*0.24163
		+(totalbaseline*wppercent*0.7)*0.0
		+(totalbaseline*wpppercent*0.7)*0.26280
		+(totalbaseline*wopercent*0.7)*0.24597
		+(powerusage[imon]['sp']-totalbaseline*sppercent*2.0)*0.49368
		+(powerusage[imon]['spp']-totalbaseline*spppercent*2.0)*0.37841
		+(powerusage[imon]['so']-totalbaseline*sopercent*2.0)*0.30163
		+(powerusage[imon]['wp']-totalbaseline*wppercent*2.0)*0.0
		+(powerusage[imon]['wpp']-totalbaseline*wpppercent*2.0)*0.32280
		+(powerusage[imon]['wo']-totalbaseline*wopercent*2.0)*0.30597)
		else:
			totalcost+=(totalbaseline*sppercent*0.32306+totalbaseline*spppercent*0.20779+totalbaseline*sopercent*0.13101
		+totalbaseline*wppercent*0.0+totalbaseline*wpppercent*0.15218+totalbaseline*wopercent*0.13535
		+(totalbaseline*sppercent*0.3)*0.34627
		+(totalbaseline*spppercent*0.3)*0.23100
		+(totalbaseline*sopercent*0.3)*0.15423
		+(totalbaseline*wppercent*0.3)*0.0
		+(totalbaseline*wpppercent*0.3)*0.17539
		+(totalbaseline*wopercent*0.3)*0.15856
		+(totalbaseline*sppercent*0.7)*0.43368
		+(totalbaseline*spppercent*0.7)*0.31841
		+(totalbaseline*sopercent*0.7)*0.24163
		+(totalbaseline*wppercent*0.7)*0.0
		+(totalbaseline*wpppercent*0.7)*0.26280
		+(totalbaseline*wopercent*0.7)*0.24597
		+(totalbaseline*sppercent*1.0)*0.49368
		+(totalbaseline*spppercent*1.0)*0.37841
		+(totalbaseline*sopercent*1.0)*0.30163
		+(totalbaseline*wppercent*1.0)*0.0
		+(totalbaseline*wpppercent*1.0)*0.32280
		+(totalbaseline*wopercent*1.0)*0.30597
		+(powerusage[imon]['sp']-totalbaseline*sppercent*2.0)*0.49368
		+(powerusage[imon]['spp']-totalbaseline*spppercent*2.0)*0.37841
		+(powerusage[imon]['so']-totalbaseline*sopercent*2.0)*0.30163
		+(powerusage[imon]['wp']-totalbaseline*wppercent*2.0)*0.0
		+(powerusage[imon]['wpp']-totalbaseline*wpppercent*2.0)*0.32280
		+(powerusage[imon]['wo']-totalbaseline*wopercent*2.0)*0.30597)
	print 'total cost:',totalcost
	return totalcost
def calbaseline(startdate,enddate):
	startsummer=datetime.date(enddate.year,5,1)
	endsummer=datetime.date(enddate.year,11,1)
	if startdate<enddate<startsummer:
		baseline=(enddate-startdate).days*10.1
	elif startdate<=startsummer<= enddate<endsummer:
		baseline=(enddate-startsummer).days*10.9+(startsummer-startdate).days*10.1
	elif startdate<=endsummer<= enddate:
		baseline=(enddate-endsummer).days*10.1+(endsummer-startdate).days*10.9
	elif endsummer<=startdate< enddate:
		baseline=(enddate-startdate).days*10.9
	elif startsummer<=startdate< enddate<endsummer:
		baseline=(enddate-startdate).days*10.1
	else:
		baseline=0
		print 'calbaseline ??',startdate,enddate
	return baseline

def isholiday(date):
	holiday=[(1,1),(2,16),(5,26),(7,4),(9,1),(11,11),(11,27),(12,25)]
	return (date.month,date.day) in holiday
def issummer(date):
	return datetime.date(date.year,5,1) <= date < datetime.date(date.year,11,1)
def isweekday(date):
	return date.weekday()<=5
def calE6pptype(date,time):
	if issummer(date): 
		if isholiday(date):
			pptype='so'
		elif (13<=time<20 and isweekday(date)):
			pptype='sp'
		elif (((10 <= time < 13) or (19<=time<21)) and isweekday(date)) or (17 <=time <20 and not isweekday(date)):
			pptype='spp'
		else:
			pptype='so'
	else:
		if (17 <= time <20 and isweekday(date)):
			pptype='wpp'
		else:
			pptype='wo'
	return pptype
calE6(hourbill)
calEVA(hourbill)
