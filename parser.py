import sys, re, os

year = 1900
#year = 2012

while year < 2014:
	football_data = open('{0}-schedule.html'.format(year)).readlines()
	year_results = open('{0}-results.csv'.format(year),'a+')
	output_data, new_data = [], []
	winners, losers, ties, teams_list = [], [], [], []
	season_wk = {}
	season_weeks = []

	for line in football_data:
		if '<tr' in line or '</tr' in line or 'td align' in line:
			line = re.sub(r'<tr.*>','(START)',line)
			line = re.sub(r'</tr>','(END)',line)
			line = re.sub(r'<.*csk=','',line)
			line = re.sub(r'<a href=.*">','',line)
			line = re.sub(r'".*">','',line)
			line = re.sub(r'<td ali.* >','',line)
			line = re.sub(r'.*&nbsp;','',line)
			line = re.sub(r'></td>','',line)
			line = re.sub(r'</a','',line)
			line = re.sub(r'</td>','',line)
			if 'START' in line:
				next
			elif 'END' not in line:
				line = re.sub(r'^\s*$','VS', line)
				output_data.append(line)
			elif 'END' in line:
				if not line == "":
					new_data.append('_'.join(str(x).strip() for x in output_data))
					output_data = []

	year_results.write('\n'.join(str(x).strip() for x in new_data))
	year += 1

	for line in new_data:
		line = re.sub(r',VS$','',line)
		if not line == "":
			if 'AM' in line or 'PM' in line:
				next
			else:
				gameNum = int(line.split('_')[0])
				weekNum = int(line.split('_')[1])
				gameDate = re.sub(r' ','-',line.split('_')[2])
				gameDate = re.sub(r',','',gameDate)
				gameDay = line.split('_')[3]
				team_a = line.split('_')[4]
				teams_list.append(team_a)
				score_a = int(line.split('_')[5])
				loc = line.split('_')[6]
				team_b = line.split('_')[7]
				teams_list.append(team_b)
				score_b = int(line.split('_')[8])
				if score_a > score_b:
					winners.append(team_a)
					losers.append(team_b)
				elif score_a < score_b:
					winners.append(team_b)
					losers.append(team_a)
				elif score_a == score_b:
					ties.append(team_a)
					ties.append(team_b)
				site = line.split('_')[9]
				if weekNum in season_wk.keys():
					season_wk[weekNum][gameNum] = {
						'gameDate':gameDate,
						'team_a':team_a,
						'score_a':score_a,
						'loc':loc,
						'team_b':team_b,
						'score_b':score_b,
						'site':site
						}
				elif weekNum not in season_wk.keys():
					season_wk[weekNum] = {
						'gameNum':gameNum,
							}
					season_wk[weekNum][gameNum] = {
						'gameDate':gameDate,
						'team_a':team_a,
						'score_a':score_a,
						'loc':loc,
						'team_b':team_b,
						'score_b':score_b,
						'site':site
						}

#print season_wk[1][1]
print winners.count('Oregon State')
for team in sorted(set(teams_list)):
	t_wins = winners.count(team)
	t_losses = losers.count(team)
	t_ties = ties.count(team)
	print '{0} {1}-{2}-{3}'.format(team,t_wins,t_losses,t_ties)
