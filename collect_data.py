import requests
import json
import time
from lxml import etree
ua_agent = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'}
total_data = dict()
now_date = time.localtime()
year = str(now_date.tm_year)[2:]
month =	now_date.tm_mon 
if month >10:
	month = str(month)
else:
	month = '0'+str(month)
day = now_date.tm_mday 
if day >10:
	day = str(day)
else:
	day = '0'+str(day)
today = year+month+day


def get_odds(fixid):
	eu_url = 'http://live.aicai.com/xiyaou/odds!getOuzhi.htm?betId=%s&propId=1&start=0&size=50'%fixid
	as_url = 'http://live.aicai.com/xiyaou/odds!getyazhi.htm?betId=%s&propId=0&start=0&size=50&selectedType=yazhi'%fixid
	ball_url = 'http://live.aicai.com/xiyaou/odds!getyazhi.htm?betId=%s&propId=0&start=0&size=50&selectedType=dxzhi'%fixid
	try:
		eu_odds_data  = requests.get(url = eu_url,headers = ua_agent).content.decode('utf-8')
		as_odds_data  = requests.get(url = as_url,headers = ua_agent).content.decode('utf-8')
		ball_odds_data  = requests.get(url = ball_url,headers = ua_agent).content.decode('utf-8')
		eu_odds_data= json.loads(eu_odds_data)['result']
		as_odds_data= json.loads(as_odds_data)['result']
		ball_odds_data= json.loads(ball_odds_data)['result']
		return (eu_odds_data,as_odds_data,ball_odds_data)
	except:	
		print ('获取赔率出问题')
		return -1
def get_recently(team_id):
	home_url = 'http://live.aicai.com/xiyaou/datan!queryLateMatchs.htm?leagueType=0&teamId=%s&matchDate=20%s-%s-%s%%2014:40&hostType=all&count=15'%(team_id[0],year,month,day)
	guest_url = 'http://live.aicai.com/xiyaou/datan!queryLateMatchs.htm?leagueType=0&teamId=%s&matchDate=20%s-%s-%s%%2014:40&hostType=all&count=15'%(team_id[1],year,month,day)

	bet_url = 'http://live.aicai.com/xiyaou/datan!getHisDatan.htm?leagueType=0&hostTeamId=%s&awayTeamId=%s&matchDate=20%s-%s-%s%%2014:40&hostType=all'%(team_id[0],team_id[1],year,month,day)

	try:
		home_data = json.loads(requests.get(url = home_url, headers = ua_agent).content.decode('utf-8'))['result']['teams']
		guest_data = json.loads(requests.get(url = guest_url, headers = ua_agent).content.decode('utf-8'))['result']['teams']
		bet_data = json.loads(requests.get(url = bet_url, headers = ua_agent).content.decode('utf-8'))['result']['dates']
		return (home_data,guest_data,bet_data)
	except:
		print ('获取战绩出问题')
		return -1

def get_team_id(url):
	respon = requests.get(url = url, headers = ua_agent)
	html = respon.content.decode('utf-8')
	try:
		selector = etree.HTML(html)
		hometeam_id = selector.xpath('//span[@id="jq_hometeamd_id"]/text()')[0]
		guestteam_id = selector.xpath('//span[@id="jq_guestteamd_id"]/text()')[0]
		return (hometeam_id,guestteam_id)
	except:
		print ('获取teamId出错')
		return -1

def get_match_data():
	url = 'http://www.aicai.com/lotnew/jc/getMatchByDate.htm?lotteryType=jczq&cate=gd&dataStr='
	url = url+year+month+day
	respon = requests.get(url = url, headers = ua_agent)
	data = respon.content.decode('utf-8')
	try:
		data = eval(data)
	except:
		return -1

	matchs_data = data['raceList']
	count  = 1
	for match_number in matchs_data:
		
		tmp = []
		match_data = matchs_data[match_number]
		match_analyse_url = 'http://live.aicai.com/zc/xyo_%s.html'%(match_data['fixId'])
		team_id = get_team_id(match_analyse_url)
		all_match_data = get_recently(team_id)
		all_odds_data = get_odds(match_data['fixId'])
		tmp.append(match_data)
		tmp.append(all_match_data)
		tmp.append(all_odds_data)
		total_data.update({count:tmp})
		print ('第%d个已经完成数据更新'%count)
		count +=1
def auto_get():
	get_match_data()
	return total_data
