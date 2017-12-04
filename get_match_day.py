from sort_data import auto_sort,select_func
def init_func():
	mode = int(input('1.开始新的比赛\n2.更新昨日的预测\n3.查看今日比赛\n4.查看我的战绩\n'))
	if mode == 1:
		auto_sort()
	if mode == 2:
		auto_sort(1)
	if mode == 3:
		pass
	select_func()
def main():
	init_func()
if __name__ == '__main__':
	main()
	
