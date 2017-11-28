import requests
import time
from lxml import etree
ua_agent = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'}
now_date = time.localtime()

def write_database(data):
	pass

def check():
	pass



def get_recently(team_id):
	year = now_date.tm_year
	month = now_date.tm_mon
	day = now_date.tm_mday
	home_url = 'http://live.aicai.com/xiyaou/datan!queryLateMatchs.htm?leagueType=0&teamId=%s&matchDate=%s-%s-%s%%2014:40&hostType=all&count=15'%(team_id[0],year,month,day)
	guest_url = 'http://live.aicai.com/xiyaou/datan!queryLateMatchs.htm?leagueType=0&teamId=%s&matchDate=%s-%s-%s%%2014:40&hostType=all&count=15'%(team_id[1],year,month,day)

	bet_url = 'http://live.aicai.com/xiyaou/datan!getHisDatan.htm?leagueType=0&hostTeamId=%s&awayTeamId=%s&matchDate=&s-%s-%s%%2014:40&hostType=all'%(team_id[0],team_id[1],year,month,day)

	try:
		home_data = eval(requests.get(url = home_url, headers = ua_agent).content.decode('utf-8'))['result']['teams']
		guest_data = eval(requests.get(url = guest_url, headers = ua_agent).content.decode('utf-8'))['result']['teams']
		bet_data = eval(requests.get(url = bet_url, headers = ua_agent).content.decode('utf-8'))['result']['dates']
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
	year = now_date.tm_year[2:]
	month =	now_date.tm_mon 
	day = now_date.tm_mday 
	url = url+year+month+day

	respon = requests.get(url = url, headers = ua_agent)
	data = respon.content.decode('utf-8')
	try:
		data = eval(data)
	except:
		return -1
	match_date = data['weekDate']

	matchs_data = data['raceList']
	for match_number in matchs_data:
		match_data = matchs_data[match_number]
		match_analyse_url = 'http://live.aicai.com/zc/xyo_%s.html'%(match_data['fixId'])
		team_id = get_team_id(match_analyse_url)

		all_match_data = get_recently(team_id)
		all_odds_data = get_odds(match_data['fixId'])

		time.sleep(10)
		#print ('比赛场次:%s\t%s VS %s\n比赛时间: %s\n胜平负: %s\n半全场: %s\n总进球: %s\n比分: %s\n让球数: %s\n让胜平负: %s\n\n'%(match_number,home_team,guest_team,match_time,match_spfsp,match_bqcsp,match_zjqsp,match_bfsp,match_concede,match_concede_spfsp))
def get_odds(fixid):
	eu_url = 'http://live.aicai.com/xiyaou/odds!getOuzhi.htm?betId=%s&propId=1&start=0&size=50'%fixid
	as_url = 'http://live.aicai.com/xiyaou/odds!getyazhi.htm?betId=%s&propId=0&start=0&size=50&selectedType=yazhi'%fixid
	ball_url = 'http://live.aicai.com/xiyaou/odds!getyazhi.htm?betId=%s&propId=0&start=0&size=50&selectedType=dxzhi'%sfixid
	try:
		eu_odds_data  = eval(requests.get(url = eu_url,headers = ua_agent).content.decode('utf-8'))['result']
		as_odds_data  = eval(requests.get(url = as_url,headers = ua_agent).content.decode('utf-8'))['result']
		ball_odds_data  = eval(requests.get(url = ball_url,headers = ua_agent).content.decode('utf-8'))['result']
		return (eu_odds_data,as_odds_data,ball_odds_data)
	except:	
		print ('获取赔率出问题')
		return -1


def main():
	get_match_data()

if __name__ == '__main__':
	main()
	
