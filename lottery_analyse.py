import requests
import os
import re
from threading import Thread
from bs4 import BeautifulSoup
ua_agent = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'}
xua_agent = {'Referer':'http://zx.500.com/openplatform/n_1/2017/1127/a62aade1e0954398c32f6f090f50ee1b.shtml','User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'}
article_list = []
def write_article():
	if not os.path.exists('/Users/xiejunjie/py-exam/lottery/lottery_analyse.ini'):
		with open('/Users/xiejunjie/py-exam/lottery/lottery_analyse.ini','w') as f:
			with open('/Users/xiejunjie/py-exam/lottery/lottery_analyse.txt','w') as g:
				for article in article_list:
					f.write(article[2]+'\n')
					g.write(article[0]+'\n')
					g.write(article[1]+'\n')
					g.write(article[2]+'\n')
					g.write(article[4]+'\n')
					g.write('\n\n\n\n')
	else:
		with open('/Users/xiejunjie/py-exam/lottery/lottery_analyse.ini','r+') as f:
			with open('/Users/xiejunjie/py-exam/lottery/lottery_analyse.txt','a') as g:
				read_list = f.read().split('\n')[0:-1]
				existed = -1
				for article in article_list:
					for read_item in read_list:
						if article[2] == read_item:
							existed = 0
							continue
					if existed != 0:
						g.write(article[0]+'\n')
						g.write(article[1]+'\n')
						g.write(article[2]+'\n')
						g.write(article[4]+'\n')
						g.write('\n\n\n\n')
						f.write(article[2]+'\n')
					existed = -1
			
def down_analyse(url):
	try:
		data = requests.get(url = url, headers = ua_agent).content.decode('GBK')
		data = eval(data)['data']
	except:
		return -1
	for item in data:
		if item['paytype'] == '0':
			tmp = [ item['publishtime'] or item['expiretime'],
				item['nickname'],
				item['title'],
				item['aid']	]
			article_list.append(tmp)
	for article in article_list:	
		page = get_detail(article[3])
		if page == -1:
			page = get_detail(article[3])
			if page == -1:
				return -1
		article.append(page)
def sort_article():
	global article_list
	reg = re.compile(r'[:\s-]+')
	article_list =  sorted(article_list,key = lambda x:int(reg.sub('',x[0])))
def get_detail(fid):
	url = 'http://zx.500.com/openplatform/getinfo.php'
	data = {'tmpid':'a62aade1e0954398c32f6f090f50ee1b','fid':fid}
	try:
		respon= requests.post(url,headers = ua_agent,data=data)
		detail = respon.content.decode('GBK')
		detail = eval(detail)['detail']['freecontent']
	except:
		return -1
	Soup = BeautifulSoup(detail,'lxml')
	p_tags = Soup.find_all('p')
	contents =str() 
	for p in p_tags:
		text = p.text.replace('\n','').strip()
		if text!='':
			contents+=text
	return contents
def main():
	threads = []
	for i in range(10):
		url = "http://zx.500.com/ajax.php?pageCount=%d&sortid=1&type=news"%(i)
		threads.append(Thread(target = down_analyse,args=(url,)))
	for th in threads:
		th.start()
	for th in threads:
		th.join()

	sort_article()	
	write_article()
main()	
