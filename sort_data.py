from prettytable import PrettyTable
import pymysql
from collect_data import auto_get
#模式0代表重新一天的数据
#模式1代表本地缓存操作
#模式2代表更新比赛的数据
def show_exploit():
	pass
def auto_sort(mode = 0):
	recev_data = auto_get()
	clear_database()
	if mode == 0:
		write_database(recev_data)
	else:
		write_database(recev_data,1)
def clear_database():
	db = pymysql.connect(host = '127.0.0.1',user = 'root',password = 'mysql',db = 'lottery',charset = 'utf8')
	cur = db.cursor()
	cur.execute('truncate table home_match')
	cur.execute('truncate table guest_match')
	cur.execute('truncate table home_guest_match')
	cur.execute('truncate table odds_match')
	cur.execute('set foreign_key_checks=0')
	cur.execute('truncate table today_match')
	cur.execute('set foreign_key_checks=1')
	db.close()

def write_database(total_data,mode=0):
	db  = pymysql.connect(host = "127.0.0.1",user = "root",password = "mysql",db = "lottery",charset = "utf8")
	cur = db.cursor()
	for num in range(1,len(total_data)+1):
		data = total_data[num][0]
		odds_data = total_data[num][2]
		re_data = total_data[num][1]
		home_match = re_data[0]
		guest_match = re_data[1]
		comp_match = re_data[2]

		if data['resultXspf'] == '3':
			result  = '胜'
		elif data['resultXspf'] == '1':
			result = '平'
		elif data['resultXspf'] == '0':
			result = '负'
		else:
			result = '**'

		if mode == 0:
			sql = """insert into today_match values(%d,"%s","%s","%s","%s","%s","%s","%s")"""%(num,data['matchName'],data['homeTeam'],data['guestTeam'],data['endTime'],result,'**',data['fixId'])
			try:
				cur.execute(sql)
				db.commit()
				print ('今日比赛写入数据库成功')
			except:
				db.close()
				print ('今日比赛写入数据库错误')
				exit(1)
		else:
			sql = """update today_match set match_result="%s" """%(result)
			try:
				cur.execute(sql)
				db.commit()
				print ('今日比赛更新数据库成功')
			except:
				db.close()
				print ('今日比赛更新数据库错误')
				exit(1)
			

		eu_odds_list = odds_data[0]['europOddsList']
		for item in eu_odds_list:
			a = item['createTime']
			create_time = "%s-%s %s:%s"%(str(a['month']+1),
						     str(a['date']) if a['date'] >= 10 else '0'+str(a['date']),
						     str(a['hours']) if a['hours'] >= 10 else '0'+str(a['hours']),
						     str(a['minutes'] if a['minutes']>=10 else '0'+str(a['minutes'])))
			b = item['lastUpdateTime']
			update_time = "%s-%s %s:%s"%(str(b['month']+1),
						     str(b['date']) if b['date'] >= 10 else '0'+str(b['date']),
						     str(b['hours']) if b['hours'] >= 10 else '0'+str(b['hours']),
						     str(b['minutes'] if b['minutes']>=10 else '0'+str(b['minutes'])))
			sql = """insert into odds_match values(%d,"%s","%s","%s","%s","%s","%s","%s","%s")"""%(num,item['companyName'],
						      str(item['firstWinOdds']/10000),
						      str(item['firstDrowOdds']/10000),
						      str(item['firstLoseOdds']/10000),
						      str(item['firstWinRate']/100)+'%',
						      str(item['firstDrowRate']/100)+'%',
						      str(item['firstLoseRate']/100)+'%',
						      create_time)
			cur.execute(sql)
			try:
				cur.execute(sql)
				db.commit()
				print ('第一次odds数据库写入成功')
			except:
				print ('第一次odds数据库写入错误')
				db.close()
				exit()
			sql = """insert into odds_match values("%d","%s","%s","%s","%s","%s","%s","%s","%s")"""%(num,'',
						      str(item['winOdds']/10000),
						      str(item['drowOdds']/10000),
						      str(item['loseOdds']/10000),
						      str(item['winRate']/100)+'%',
						      str(item['drowRate']/100)+'%',
						      str(item['loseRate']/100)+'%',
						      update_time)
			try:
				cur.execute(sql)
				db.commit()
				print ('第二次odds数据库写入成功')
			except:
				print ('第二次odds数据库写入错误')
				db.close()
				exit()

		table_home = PrettyTable(['赛事','时间','主队','客队','半场比分','全场比分','比赛结果','亚盘'],horizontal_char = '*')
		table_guest = PrettyTable(['赛事','时间','主队','客队','半场比分','全场比分','比赛结果','亚盘'],horizontal_char = '*')
		for item in home_match:
			sql = """insert into home_match values("%d","%s","%s","%s","%s","%s","%s","%s","%s")"""%(num,item['matchName'],
									       item['date'],
									       item['hometeam'],
									       item['guestteam'],
									       item['hostHalfScore']+' : '+
									       item['awayHalfScore'],
									       item['hostScore']+' : '+
									       item['awayScore'],
									       item['matchResult'],
									       item['asiaTapZh'])
			try:
				cur.execute(sql)
				db.commit()
				print ('主队数据库写入成功')
			except:
				print ('主队数据库写入错误')
				db.close()
				exit()
		for item in guest_match:
			sql = """insert into guest_match values("%d","%s","%s","%s","%s","%s","%s","%s","%s")"""%(num,item['matchName'],
									       item['date'],
									       item['hometeam'],
									       item['guestteam'],
									       item['hostHalfScore']+' : '+
									       item['awayHalfScore'],
									       item['hostScore']+' : '+
									       item['awayScore'],
									       item['matchResult'],
									       item['asiaTapZh'])
			try:
				cur.execute(sql)
				db.commit()
				print ('客队数据库写入成功')
			except:
				print ('客队数据库写入错误')
				db.close()
				exit()

		for item in comp_match:
			sql = """insert into home_guest_match values("%d","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")"""%(num,item['matchName'],
								       item['date'],
								       data['homeTeam'],
								       data['guestTeam'],
								       item['hostScore']+' : '+
								       item['awayScore'],
								       item['matchResult'],
								       str(int(item['winOdds'])/10000),
								       str(int(item['drawOdds'])/10000),
								       str(int(item['loseOdds'])/10000),
								       item['asiaTapZh'])
			try:
				cur.execute(sql)
				db.commit()
				print ('数据库写入成功')
			except:
				print ('数据库写入错误')
				db.close()
				exit()
	db.close()
def select_func():
	db  = pymysql.connect(host = "127.0.0.1",user = "root",password = "mysql",db = "lottery",charset = "utf8")
	cur = db.cursor()
	while True:
		cur.execute('select * from today_match')
		today_match = list(cur.fetchall())
		today_match_table = PrettyTable(['序号','赛事','主队','客队','比赛时间','赛果','你的预测','fixid'],padding_width = 2)
		for item in today_match:
			tmp = []
			for ele in item:
				tmp.append(ele)		
			today_match_table.add_row(tmp)
		print (today_match_table)
		match_num = int(input('请选择需要查看的比赛序号:\n'))
		if match_num == -1:
			exit()
		print ('\n\n')
		while True:
			print ('1.查看主队近期比赛\n2.查看客队近期比赛\n3.查看两队近期比赛\n4.查看赔率情况\n5.预测赛果\n6.退出')
			mode = int(input('请输入功能序号:\n'))
			print ('\n\n')
			if mode == 5:
				prediction = int(input('输入你的预测结果(3/1/0):\n'))
				if prediction == 3:
					prediction = "胜"
				elif prediction == 1:
					prediction = "平"
				elif prediction == 0:
					prediction = "负"
				sql = 'update today_match set my_prediction="%s" where id = %d'%(prediction,match_num)
				cur.execute(sql)
				db.commit()

				cur.execute('select match_name,home_team,guest_team,match_time,match_result,my_prediction,fixId from today_match where my_prediction <> "**"') 
				prediction_match = list(cur.fetchall()) 
				for item in prediction_match:
					tmp = []
					for ele in item:
						tmp.append(ele)
					if tmp[4] == "**":
						isright = "**"
					else:
						if tmp[4] == tmp[5]:
							isright = "正确"
						else:
							isright = "错误"
						
					cur.execute('select max(id) from my_prediction')
					id_count = cur.fetchall()
					try:
						id_count = id_count[0][0]+1
					except:
						id_count = 1

					sql = 'insert into my_prediction values(%d,"%s","%s","%s","%s","%s","%s","%s","%s")'%(id_count,tmp[0],tmp[1],tmp[2],tmp[3],tmp[4],tmp[5],isright,tmp[6])

					try:
						cur.execute(sql)
						db.commit()
					except:
						sql = 'update my_prediction set prediction="%s",isright="%s" where fixid="%s"'%(tmp[5],isright,tmp[6])
						cur.execute(sql)
						db.commit()
			if mode == 6:
				break
			if mode==1:
				cur.execute('select match_name,match_time,home_team,guest_team,half_score,final_score,result,asia_handicap from home_match where id = %d'%match_num)
				home_match = list(cur.fetchall())
				home_match_table = PrettyTable(['赛事','比赛时间','主队','客队','半场比分','全场比分','赛果','亚盘'],padding_width = 2)
				for item in home_match:
					tmp = []
					for ele in item:
						tmp.append(ele)
					home_match_table.add_row(tmp)
				print (home_match_table)
			if mode==2:
				cur.execute('select match_name,match_time,home_team,guest_team,half_score,final_score,result,asia_handicap from guest_match where id = %d'%match_num)
				guest_match = list(cur.fetchall())
				guest_match_table = PrettyTable(['赛事','比赛时间','主队','客队','半场比分','全场比分','赛果','亚盘'],padding_width = 2)
				for item in guest_match:
					tmp = []
					for ele in item:
						tmp.append(ele)
					guest_match_table.add_row(tmp)
				print (guest_match_table)
			if mode==3:
				cur.execute('select match_name,match_time,home_team,guest_team,final_score,result,win_odds,draw_odds,lose_odds,asia_handicap from home_guest_match where id = %d'%match_num)
				home_guest_match = list(cur.fetchall())
				home_guest_match_table = PrettyTable(['赛事','比赛时间','主队','客队','全场比分','赛果','胜赔','平赔','负赔','亚盘'],padding_width = 2)
				for item in home_guest_match:
					tmp = []
					for ele in item:
						tmp.append(ele)
					home_guest_match_table.add_row(tmp)
				print (home_guest_match_table)
			if mode==4:
				cur.execute('select company,winodds,drawodds,loseodds,winrate,drawrate,lose,update_time from odds_match where id = %d'%match_num)
				odds_match = list(cur.fetchall())
				odds_match_table = PrettyTable(['公司','胜赔','平赔','负赔','胜率','平率','负率','更新时间'],padding_width = 2)
				i = 1
				for item in odds_match:
					tmp = []
					for ele in item:
						tmp.append(ele)
					odds_match_table.add_row(tmp)
					if i%2 == 0:
						odds_match_table.add_row(['*'*10,'*'*10,'*'*10,'*'*10,'*'*10,'*'*10,'*'*10,'*'*10])
					i+=1
				print (odds_match_table)
	db.close()

