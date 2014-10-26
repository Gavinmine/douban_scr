#!/usr/bin/python3.4

from bs4 import BeautifulSoup 
import urllib.request
from urllib.request import Request, urlopen
from time import sleep
import httplib2
import socket 
import os 
import re
import threading
from queue import Queue
from time import sleep

book_lock = threading.Lock()
movie_lock = threading.Lock()
music_lock = threading.Lock()
error_lock = threading.Lock()
#firstmove = "http://book.douban.com/subject/1000001/"
#filename = "firstmove"

nameerror_type = -3
timeout_type = -2
not_exist_type = -1
unknow_type = 0
move_type = 1
music_type = 2
book_type = 3

move_http = "http://movie.douban.com"
music_http = "http://music.douban.com"
book_http = "http://book.douban.com"
type_dict = {move_http:move_type, music_http:music_type, book_http:book_type}

move_file = "move.txt"
music_file = "music.txt"
book_file = "book.txt"
error_file = "error.txt"
MOVE = open(move_file, 'a')
MUSIC = open(music_file, 'a')
BOOK = open(book_file, 'a')
ERROR = open(error_file, 'a')

not_exist_str = "条目不存在"

def get_IP_PORT():
	url = "http://cn-proxy.com/"
	http = httplib2.Http(cache=None, timeout = 10)
	try:
		response, move_content = http.request(url)
	except socket.timeout:
		print("can't access %s"%url)
		return None
	soup = BeautifulSoup(move_content)
	match = soup.findAll('td')
	pat=re.compile('\d+\.\d+\.\d+\.\d+')
	index = 0
	IP_PORT_DICT = {}
	for line in match:
		index+=1
		new_str = line.string
		if new_str == None:
			continue
		match2=pat.search(new_str)
		if match2:
			port=match[index].get_text()
			ip=match2.group(0)
			IP_PORT_DICT.setdefault(ip,port)

	return IP_PORT_DICT

IP_PORT_DICT = get_IP_PORT()
print(IP_PORT_DICT)
#IP_PORT_DICT={'122.96.59.102':82,'211.138.121.36':81,'211.151.50.179':81,'211.138.121.35':83,'211.138.121.38':81,
#		'111.1.36.12':80,'116.228.55.217':80,'183.129.198.231':80,'122.96.59.99':82,'114.80.136.220':7780,
#		'111.1.36.133':80,'61.174.9.96':8080,'120.198.230.31':80,'114.112.69.21':81,'114.80.136.112':7780,
#		'116.228.55.217':8000,'114.80.91.166':7780,'111.1.36.26':80,'210.14.138.102':8080,'111.1.36.25':80,
#		'111.1.36.27':83,'114.80.136.22':7780,'111.1.36.21':80,'221.130.162.77':84,'122.96.59.106':82,
#		'222.89.155.62':9000}
#
http_list = []
for host,port in IP_PORT_DICT.items():
	proxy_info = httplib2.ProxyInfo(
			proxy_type = 3,
			proxy_host = host,
			proxy_port = int(port),
			proxy_rdns = True
			)
	http = httplib2.Http(cache=None, timeout = 10, proxy_info = proxy_info)
	http_list.append(http)

#proxy_info15 = httplib2.ProxyInfo(
#		proxy_type = 3,
#		proxy_host = '120.203.214.187',
#		proxy_port = 80,
#		proxy_rdns = True
#		)

http_len = len(http_list)

COOKIE_LIST = [
		'bid="zCz8LjpyvG4"; ll="118201"; viewed="1000208_6025284_6886607"; __utma=30149280.2104381519.1362022077.1392470437.1392474034.46; __utmb=30149280.1.10.1392474034; __utmc=30149280; __utmz=30149280.1392470437.45.26.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utmv=30149280.4684; __utma=81379588.2005357480.1365138966.1377528892.1392474034.7; __utmb=81379588.1.10.1392474034; __utmc=81379588; __utmz=81379588.1377528892.6.6.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided)',
		'll="118201"; bid="Cr3fRkvJ34o"; ct=y; push_noty_num=1; push_doumail_num=0; viewed="1052930_1000001_1000720_1000355_1000354_1000208_6025284_6886607"; __utma=30149280.2104381519.1362022077.1393594981.1394023674.55; __utmb=30149280.2.10.1394023674; __utmc=30149280; __utmz=30149280.1392477830.48.27.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=%E8%B1%86%E7%93%A3%E9%AA%8C%E8%AF%81%E7%A0%81%20%E7%A0%B4%E8%A7%A3; __utmv=30149280.4684; __utma=81379588.2005357480.1365138966.1393159782.1394023674.13; __utmb=81379588.2.10.1394023674; __utmc=81379588; __utmz=81379588.1392476887.8.7.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/misc/sorry',
		'll="118200"; viewed="10618793_1444353"; bid="3MLO5FmMHGM"; push_noty_num=1; push_doumail_num=0; __utma=30149280.1693857919.1376618405.1393054900.1394024815.42; __utmb=30149280.0.10.1394024815; __utmc=30149280; __utmz=30149280.1394024815.42.34.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utmv=30149280.4684; __utma=223695111.280055576.1381931958.1393054900.1394024815.18; __utmb=223695111.2.10.1394024815; __utmc=223695111; __utmz=223695111.1394024815.18.17.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/',
		'bid="Tkaub3tBxek"; ll="118201"; __utma=30149280.2143334902.1394026238.1394026238.1394026238.1; __utmb=30149280.1.10.1394026238; __utmc=30149280; __utmz=30149280.1394026238.1.1.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utma=223695111.1724793445.1394026238.1394026238.1394026238.1; __utmb=223695111.1.10.1394026238; __utmc=223695111; __utmz=223695111.1394026238.1.1.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; report=ref=%2F&from=mv_a_pst',
		'bid="eJQ9xkaNlJs"; ll="118201"; __utma=30149280.1084672605.1394026330.1394026330.1394026330.1; __utmb=30149280.2.10.1394026330; __utmc=30149280; __utmz=30149280.1394026330.1.1.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utma=223695111.198367812.1394026330.1394026330.1394026330.1; __utmb=223695111.0.10.1394026330; __utmc=223695111; __utmz=223695111.1394026330.1.1.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/',
		'bid="CsZlyDIaR1s"; ll="118201"; __utma=30149280.2047060055.1394294384.1394294384.1394294384.1; __utmb=30149280.1.10.1394294384; __utmc=30149280; __utmz=30149280.1394294384.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utma=223695111.1348122756.1394294384.1394294384.1394294384.1; __utmb=223695111.1.10.1394294384; __utmc=223695111; __utmz=223695111.1394294384.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)',
		'bid="F266s1sMX+o"; ll="118201"; __utma=30149280.1269307237.1394294694.1394294694.1394294694.1; __utmb=30149280.0.10.1394294694; __utmc=30149280; __utmz=30149280.1394294694.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utma=223695111.1735782203.1394294694.1394294694.1394294694.1; __utmb=223695111.1.10.1394294694; __utmc=223695111; __utmz=223695111.1394294694.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)',
		'bid="K1mNPeSNedM"; ll="118201"; __utma=30149280.704009222.1394294815.1394294815.1394294815.1; __utmb=30149280.0.10.1394294815; __utmc=30149280; __utmz=30149280.1394294815.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utma=223695111.114950008.1394294815.1394294815.1394294815.1; __utmb=223695111.1.10.1394294815; __utmc=223695111; __utmz=223695111.1394294815.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)',
		'bid="HqjDimmULvw"; ll="118201"; __utma=30149280.648891368.1394294911.1394294911.1394294911.1; __utmb=30149280.1.10.1394294911; __utmc=30149280; __utmz=30149280.1394294911.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utma=223695111.1556016097.1394294911.1394294911.1394294911.1; __utmb=223695111.0.10.1394294911; __utmc=223695111; __utmz=223695111.1394294911.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)',
		'bid="Id/iXXQgxZw"; ll="118201"; __utma=30149280.1338717495.1394295012.1394295012.1394295012.1; __utmb=30149280.0.10.1394295012; __utmc=30149280; __utmz=30149280.1394295012.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utma=223695111.1307109127.1394295012.1394295012.1394295012.1; __utmb=223695111.0.10.1394295012; __utmc=223695111; __utmz=223695111.1394295012.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)',
		'bid="bN8fy9HbujI"; ll="118201"; __utma=30149280.1739073242.1394295135.1394295135.1394295135.1; __utmb=30149280.1.10.1394295135; __utmc=30149280; __utmz=30149280.1394295135.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utma=223695111.1071819040.1394295135.1394295135.1394295135.1; __utmb=223695111.0.10.1394295135; __utmc=223695111; __utmz=223695111.1394295135.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)',
		'bid="4Wj2BRZoYQ4"; ll="118201"; __utma=30149280.1791382088.1394295276.1394295276.1394295276.1; __utmb=30149280.1.10.1394295276; __utmc=30149280; __utmz=30149280.1394295276.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utma=223695111.899222939.1394295276.1394295276.1394295276.1; __utmb=223695111.1.10.1394295276; __utmc=223695111; __utmz=223695111.1394295276.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)',
		'bid="xmCn1TxDAMc"; ll="118201"; __utma=30149280.416461866.1394295369.1394295369.1394295369.1; __utmb=30149280.1.10.1394295369; __utmc=30149280; __utmz=30149280.1394295369.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utma=223695111.595062404.1394295370.1394295370.1394295370.1; __utmb=223695111.1.10.1394295370; __utmc=223695111; __utmz=223695111.1394295370.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)',
		'bid="gH6EoAVYoOA"; ll="118201"; __utma=30149280.1518653905.1394295426.1394295426.1394295426.1; __utmb=30149280.2.10.1394295426; __utmc=30149280; __utmz=30149280.1394295426.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utma=223695111.2123450746.1394295426.1394295426.1394295426.1; __utmb=223695111.2.10.1394295426; __utmc=223695111; __utmz=223695111.1394295426.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)',
		'bid="TMt7UC8EKY8"; ll="118201"; __utma=30149280.1812931489.1394295503.1394295503.1394295503.1; __utmb=30149280.1.10.1394295503; __utmc=30149280; __utmz=30149280.1394295503.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utma=223695111.1686323383.1394295503.1394295503.1394295503.1; __utmb=223695111.1.10.1394295503; __utmc=223695111; __utmz=223695111.1394295503.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)',
		'bid="p/pHVKhA+54"; __utma=30149280.307115621.1388152439.1394343515.1394346213.32; __utmz=30149280.1392477863.17.11.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=%E8%B1%86%E7%93%A3%E9%AA%8C%E8%AF%81%E7%A0%81%20%E7%A0%B4%E8%A7%A3; ll="118201"; __utma=223695111.25818725.1388834193.1392651799.1394346226.6; __utmz=223695111.1392651799.5.4.utmcsr=book.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/subject/7964416/; push_noty_num=1; push_doumail_num=0; __utmv=30149280.4684; ct=y; viewed="2056210_2055369_1796484_2055157_2042131_2010197_2006771_2006770_2006056_1043972"; __utmc=30149280; __utmb=30149280.2.10.1394346213; __utmb=223695111.0.10.1394346226; __utmc=223695111',
		'bid="WzfeXU2r9Bw"; viewed="2998826_2167741"; __utma=30149280.1442858129.1412687575.1414308898.1414314601.6; __utmz=30149280.1414154877.4.2.utmcsr=baidu|utmccn=(organic)|utmcmd=organic|utmctr=%E6%9C%89%E8%B6%A3%E7%9A%84%E7%BD%91%E7%AB%99; ll="118201"; __utma=223695111.1871680365.1413105365.1413105365.1414314605.2; __utmz=223695111.1414314605.2.2.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1414314605%2C%22http%3A%2F%2Fwww.douban.com%2F%22%5D; _pk_id.100001.4cf6=fd720ca80024096e.1413105365.2.1414314614.1413105371.; __utmc=30149280; __utmb=30149280.1.10.1414314601; __utmt=1; __utmb=223695111.2.10.1414314605; __utmc=223695111; _pk_ses.100001.4cf6=*'
		]

headers_list = []
for cookies in COOKIE_LIST:
	header = {'Accept':'text/html;q=0.9,*/*;q=0.8',
			'Accept-Encoding':'gzip,deflate,sdch',
			#'Accept-Encoding':'gzip',
			'Accept-Language':'zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4',
			'Cache-Control':'max-age=0',
			'Connection':'close',
			#'Connection':'keep-alive',
			'Cookie':cookies,
			#'Host':'book.douban.com',
			#'Referer':'http://www.douban.com/',
			#'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.107 Safari/537.36'
			'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:33.0) Gecko/20100101 Firefox/33.0'
			}
	headers_list.append(header)

headers_len = len(headers_list)

#header15 = {'Accept':'text/html;q=0.9,*/*;q=0.8',
#		'Accept-Encoding':'gzip,deflate,sdch',
#		#'Accept-Encoding':'gzip',
#		'Accept-Language':'zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4',
#		'Cache-Control':'max-age=0',
#		'Connection':'close',
#		#'Connection':'keep-alive',
#		'Cookie':'bid="TMt7UC8EKY8"; ll="118201"; __utma=30149280.1812931489.1394295503.1394295503.1394295503.1; __utmb=30149280.1.10.1394295503; __utmc=30149280; __utmz=30149280.1394295503.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utma=223695111.1686323383.1394295503.1394295503.1394295503.1; __utmb=223695111.1.10.1394295503; __utmc=223695111; __utmz=223695111.1394295503.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)',
#		#'Host':'book.douban.com',
#		#'Referer':'http://www.douban.com/',
#		'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.107 Safari/537.36'
#		}
#headers_list = [header1,header2,header3,header4,header5,header6,header7,header8,header9,header10,header11,header12,header13,header14,header15]

#if(os.path.exists(filename)):
#	os.remove(filename)
#	print ("clean file\n")

#soup = BeautifulSoup(open(move_content))

def get_move_values(url, http_info, header):
	match_type = unknow_type 
	h = http_info
	headers = header
	is_get = True
	average = '0'
	try_times = 0;
	#h = httplib2.Http(cache=None, timeout = 10)
	while is_get:
		try:
			is_get = False
			response, move_content = h.request(url, headers = headers)
		except socket.timeout:
			print ("timeout:retyr")
			sleep(5)
			is_get = True
			try_times = try_times + 1
			if try_times > 10:
				return (timeout_type, '0', '0', '0')
		#except NameError:
		#	print ("NameError:retry")
		#	sleep(5)
		#	is_get = True
		#	try_times = try_times + 1
		#	if try_times > 10:
		#		return (nameerror_type, '0', '0', '0')

	#req = Request(url, headers = headers)
	#move_content = urlopen(req).read()
	#move_content = urllib.request.urlopen(url).read()
	soup = BeautifulSoup(move_content)
	for key in type_dict.keys():
		match = soup.findAll('a', attrs={'href' : key})
		if not match == []:
			match_type = type_dict.get(key)
			break

	if match_type == unknow_type:
		print ("not match item\n");
		return (match_type, '0', '0', '0')
	#match = soup.findAll('a', attrs={'href' : move_http})
	#if match == []:
	#	return (False,'0','0','0')

	
	title = soup.title
	pat = re.compile(not_exist_str)
	if pat.search(title.string):
		return (not_exist_type, '0', '0', '0')

	strong = soup.findAll('strong')
	pat1 = re.compile('\d\.\d')
	for line in strong:
		#print (type(line.string))
		#print (line.string)
		if line.string == None:
			average = '0'
			break
		match = pat1.search(line.string)
		if match:
			average = match.group(0)
		else:
			average = '0'
	
	votes = soup.findAll('a', attrs={'href' : 'collections'}); #votes是个列表
	try:
		vote = votes[0]()[0].get_text()
	except IndexError:
		vote = '0'
	
	#bs4.element.Tag 能用get_text() bs4.element.ResultSet不能用
	
	#print (title)
	#print ("%s	%s	%s"% (title.string, average, vote))
	return (match_type, title.string.strip('\n'), average, vote)




def write_file(value_str, file_open):
	file_open.write(value_str+"\n")

def worker():
	while True:
		arguments = work_queue.get()
		istype, title, average, vote = get_move_values(arguments[0], arguments[1], arguments[2])
		value_str = "%s     %s  %s  %s"%(title, average, vote, arguments[0])
		if istype == move_type:
			if not movie_lock.acquire(timeout=3):
				movie_lock.release()
				movie_lock.acquire()
			write_file(value_str, MOVE)
			movie_lock.release()
		elif istype == music_type:
			if not music_lock.acquire(timeout=3):
				music_lock.release()
				music_lock.acquire()
			write_file(value_str, MUSIC)
			music_lock.release()
		elif istype == book_type:
			if not book_lock.acquire(timeout=3):
				book_lock.release()
				book_lock.acquire()
			write_file(value_str, BOOK)
			book_lock.release()
		elif istype == timeout_type or istype == nameerror_type:
			if not error_lock.acquire(timeout=3):
				error_lock.release()
				error_lock.acquire()
			value_str = "%s"%(arguments[0])
			write_file(value_str, ERROR)
			error_lock.release()
		elif istype == not_exist_type:
			print ("not exist item:", arguments[0])
		else:
			print ("unknow type:", arguments[0])
		print (value_str)

work_queue = Queue()
for i in range(5):
	t = threading.Thread(target=worker)
	t.daemon = True
	t.start()

def main():
	IP_PORT_DICT = {}
	url = "http://book.douban.com/subject/"
	first = 3000001
	#first = 4202001
	#first = 4202900
	count = 2000000
	i = 27159
	#IP_PORT_DICT = get_IP_PORT()
	#print (IP_PORT_DICT)
	#for i in range(count):
	while i < count:
		tmp_count = i + first
		tmp_url = url + str(tmp_count)
		http_info = http_list[tmp_count%http_len]
		headers = headers_list[tmp_count%headers_len]
		work_queue.put((tmp_url, http_info, headers))
		i = i + 1

	work_queue.join()
	MOVE.close()
	MUSIC.close()
	BOOK.close()
	ERROR.close()
	
if __name__=='__main__':
	main()
