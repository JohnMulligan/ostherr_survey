import csv
import sys
import re
import os
fname=sys.argv[1]

def clean(s):
	s=re.sub('^\s+','',s)
	s=re.sub('\s+$','',s)
	return s
	
print(fname)

def formatstring(s):
	s=re.sub('^\s+','',s)
	s=re.sub('\s+$','',s)
	s=re.sub('\s+','-',s)
	s=re.sub('/','-',s)
	s=s.lower()
	return(s)

q41={}
c=1
with open(fname) as csvfile:
	reader = csv.DictReader(csvfile)
	for row in reader:
		if c==1:
			unique_values={item:re.search("[^-]+-[^-]+$",row[item]).group(0) for item in row if 'Q41_' in item}
			
			disciplines_and_expertise={unique_values[v]:0 for v in unique_values}
			'''disciplines=[]
			expertise=[]
			for v in unique_values:
				d,e=unique_values[v].split(' - ')
				disciplines.append(d)
				expertise.append(e)
			
			disciplines=list(set(disciplines))
			expertise=list(set(expertise))
			
			print(disciplines)
			print(expertise)'''
		elif c>2:
			
			response_id = row['ResponseId']
			nonblanks = {item for item in row if 'Q41_' in item and row[item] != ''}
			if len(nonblanks)>0:
				q41[response_id]=[]
				for entry in nonblanks:
					q41[response_id].append(unique_values[entry])
					disciplines_and_expertise[unique_values[entry]]+=1
		c+=1

print(disciplines_and_expertise)



outputlines=[','.join(['discipline','expertise','value','url'])]
for k in disciplines_and_expertise:
	v=disciplines_and_expertise[k]
	d,e=k.split(' - ')
	urld=formatstring(d)
	urle=formatstring(e)
	url='http://survey.houseofkoffler.com/humanities-field-gained-exposure/'+urld+'-'+urle
	outputlines.append(','.join([d,e,str(v),url]))

print(outputlines)

h = open('heatmap_data.csv','w')
h.write('\n'.join(outputlines))
h.close()



###okay, we're going to have an endless csv here -- so I'm just going to dump these into a file, comma-delimited
###which means no commas allowed in any of the data!!
newfname='Q41PIVOT_'+fname
if os.path.exists(newfname):
	os.remove(newfname)
d=open(newfname,'a')
for response in q41:
	ResponseId = response
	rowlist = [ResponseId] + [clean(pair) for pair in q41[response]]
	output = ','.join(rowlist)+'\n'
	d.write(output)
d.close()