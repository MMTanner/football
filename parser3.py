import sys, re, os

year = sys.argv[1]

output_data, new_data = [], []

input_file_name = 'data/{0}-schedule.html'.format(year)

team_wins, team_losses, team_ties = [], [], []
total_teams = []
football_data = open(input_file_name).readlines()
season_output = open('results/{0}-results.tsv'.format(year),'a+')
team_records = open('results/{0}-results.tsv'.format(year),'a+')

def date_parse(d):
	mo,da,ye = d.split(' ')[0],d.split(' ')[1],d.split(' ')[2]
	da = da.split(',')[0]
	if len(da) < 2:
		da = '0{0}'.format(da)
	if 'jan' in mo.lower():
		mo = '01'
	elif 'feb' in mo.lower():
		mo = '02'
	elif 'mar' in mo.lower():
		mo = '03'
	elif 'apr' in mo.lower():
		mo = '04'
	elif 'may' in mo.lower():
		mo = '05'
	elif 'jun' in mo.lower():
		mo = '06'
	elif 'jul' in mo.lower():
		mo = '07'
	elif 'aug' in mo.lower():
		mo = '08'
	elif 'sep' in mo.lower():
		mo = '09'
	elif 'oct' in mo.lower():
		mo = '10'
	elif 'nov' in mo.lower():
		mo = '11'
	elif 'dec' in mo.lower():
		mo = '12'
	new_d = '{0}/{1}/{2}'.format(mo,da,ye)
	return new_d

for line in football_data:
	if '<td align' in line or '<tr' in line or '</tr' in line:
		line = ' '.join(line.strip().split())
		line = re.sub(r'<tr class="no_ranker thead">','(DELETE)',line)
		line = re.sub(r'<tr class=.*">','(START)',line)
		line = re.sub(r'</tr>','(END)',line)
		line = re.sub(r'<td align="left" csk="ZZZ"></td>','(BLANK)',line)
		line = re.sub(r'<td align="left" ></td>','VS',line)
		line = re.sub(r'<.* csk=".*">','',line)
		line = re.sub(r'<td align=".*" >','',line)
		line = re.sub(r'</.*>','',line)
#		print line.strip().rstrip()
		if 'AM' not in line and 'PM' not in line:
			if 'START' in line:
				next
			elif 'END' not in line:
				output_data.append(line.strip().rstrip())
			elif 'END' in line:
				new_data.append('\t'.join(str(x).strip().rstrip() for x in output_data))
				output_data = []

for i in new_data:
	if i == "":
		next
	elif 'DELETE' in i:
		next
	else:
		game_n = int(i.split('\t')[0])
		week_n = i.split('\t')[1]
		game_date = date_parse(i.split('\t')[2])
		game_day = i.split('\t')[3]
		t_a = i.split('\t')[4]
		s_a = int(i.split('\t')[5])
		loc = i.split('\t')[6]
		t_b = i.split('\t')[7]
		s_b = int(i.split('\t')[8])
		site = i.split('\t')[9]
		if s_a > s_b:
			team_a, score_a = t_a, s_a
			team_b, score_b = t_b, s_b
			team_wins.append(team_a)
			team_losses.append(team_b)
		elif s_a < s_b:
			team_a, score_a = t_b, s_b
			team_b, score_b = t_a, s_a
			team_wins.append(team_a)
			team_losses.append(team_b)
			if loc == '@':
				loc == 'VS'
			elif loc == 'VS':
				loc == '@'
		elif s_a == s_b:
			team_ties.append(team_a)
			team_ties.append(team_b)
		if 'bowl' in site.lower():
			week_n = 'B'

		total_teams.append(team_a)
		total_teams.append(team_b)

		print '{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}\t{8}\t{9}'\
			.format(week_n,game_n,game_date,game_day,team_a,score_a,loc,team_b,score_b,site)
