#!/usr/bin/python3.2

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

header={'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
		'Accept-Encoding':'gzip, deflate',
		'Accept-Language':'en-US,en;q=0.5',
		'Connection':'keep-alive',
		#'Cookie':'csrftoken=dcPrgAPsQ9zu4cve3zwHoFO6biwmz7O3; sessionid=hmdv5lku624a22cry176fj02ibkkddfs',
		'Cookie':'csrftoken=y0Uqs99XBpAgtGuOAKnDQTPfSv9AXKnQ; sessionid=uzjq61qhak2azmwxzoir2yb7ka2wwees',
		'Host':'127.0.0.1:8000',
		'Referer':'http://127.0.0.1:8000/login_check/',
		'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:17.0) Gecko/20131029 Firefox/17.0'
		}

zhihu_header={'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
			'Accept-Encoding':'gzip, deflate',
			'Accept-Language':'en-US,en;q=0.5',
			'Connection':'keep-alive',
			#'Cookie':'q_c1=57681b9fbe224c31818184ff40670fde|1407650158000|1407650158000; __utma=51854390.1419926283.1398591919.1407650000.1407742900.5; __utmz=51854390.1401992705.2.2.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); __utmv=51854390.100-2|2=registration_date=20110807=1^3=entry_date=20110807=1; q_c0="ZjZlYzhkYTBlMWJkN2MyM2M5MDViZTY1ZGJjMzZjNmR8czBRT2oyREM3ZkZlaE9jQw==|1407650768|c343217df856a0c88ab082a82ff91bbf9960a1b1"; _xsrf=4cd633a027fdd1f73090db71803a15d5; __utmb=51854390.2.10.1407742900; __utmc=51854390',
			'Cookie': 'randomSeed=722599; cpu_performance=17; __Q_w_s_hat_seed=1; __Q_w_s__QZN_TodoMsgCnt=1; __Q_w_s__appDataSeed=1; ac=1,019,008; pgv_pvid=1806123856; pt2gguin=o0329661289; ptcz=e60b2803dd717077f156ee61f0ecc8ac24f7dca83119ce0e639015b366d0861d; o_cookie=329661289; uin_cookie=329661289; euin_cookie=FD32CD92D758C606D2E050CE7E228146AE2B80B3836DFB6A; qz_screen=1366x768; pgv_r_cookie=1342180642730; SHKL_KANGSHIFUMOLI_130515_QQ_AIO_R0100_b_3=1@UV; hot_feeds_key=1094d319519f4a8a|143525a951bb3f25|; cpu_performance_v8=52; QZ_FE_WEBP_SUPPORT=0; uin=o0329661289; skey=@EWfzuAEM9; ptisp=ctc; qm_username=329661289; qm_sid=4eb698d094eaae718a354bf2c1efa959,qZW42RTNlcHB4NlNsclR3OExwNGswOWdIZ25wSHBzS2NvNSpNWHB0MnZtOF8.; blabla=dynamic; Loading=Yes; p_skey=j-1uWYvxOCWfj7iEyTXmDgTkHeUIeOuRm6bLDX7*2UM_; pt4_token=z8jFnTfuorsacsCelOnf2A__; pgv_info=ssid¯ºìSY',
			'Host':'www.zhihu.com',
			'Referer':'http://www.zhihu.com/',
			'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:17.0) Gecko/20131029 Firefox/17.0'
			}

qzone_header={'Host':'user.qzone.qq.com',
			'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0',
			'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
			'Accept-Language':'zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3',
			'Accept-Encoding':'gzip, deflate',
			#'X-Real-Url':'http://ic2.s8.qzone.qq.com/cgi-bin/feeds/cgi_get_feeds_count.cgi?uin=329661289&rd=0.34431276409970235&g_tk=2068035649',
			'Referer':'http://user.qzone.qq.com/329661289/myhome',
			#'Cookie':'randomSeed=722599; cpu_performance=17; __Q_w_s_hat_seed=1; __Q_w_s__QZN_TodoMsgCnt=1; __Q_w_s__appDataSeed=1; ac=1,019,008; pgv_pvid=1806123856; pt2gguin=o0329661289; ptcz=e60b2803dd717077f156ee61f0ecc8ac24f7dca83119ce0e639015b366d0861d; o_cookie=329661289; uin_cookie=329661289; euin_cookie=FD32CD92D758C606D2E050CE7E228146AE2B80B3836DFB6A; qz_screen=1366x768; pgv_r_cookie=1342180642730; SHKL_KANGSHIFUMOLI_130515_QQ_AIO_R0100_b_3=1@UV; hot_feeds_key=1094d319519f4a8a|143525a951bb3f25|; cpu_performance_v8=52; QZ_FE_WEBP_SUPPORT=0; uin=o0329661289; skey=@EWfzuAEM9; ptisp=ctc; qm_username=329661289; qm_sid=4eb698d094eaae718a354bf2c1efa959,qZW42RTNlcHB4NlNsclR3OExwNGswOWdIZ25wSHBzS2NvNSpNWHB0MnZtOF8.; blabla=dynamic; Loading=Yes;',
			'Cookie': 'randomSeed=722599; cpu_performance=17; __Q_w_s_hat_seed=1; __Q_w_s__QZN_TodoMsgCnt=1; __Q_w_s__appDataSeed=1; ac=1,019,008; pgv_pvid=1806123856; pt2gguin=o0329661289; ptcz=e60b2803dd717077f156ee61f0ecc8ac24f7dca83119ce0e639015b366d0861d; o_cookie=329661289; uin_cookie=329661289; euin_cookie=FD32CD92D758C606D2E050CE7E228146AE2B80B3836DFB6A; qz_screen=1366x768; pgv_r_cookie=1342180642730; SHKL_KANGSHIFUMOLI_130515_QQ_AIO_R0100_b_3=1@UV; hot_feeds_key=1094d319519f4a8a|143525a951bb3f25|; cpu_performance_v8=52; QZ_FE_WEBP_SUPPORT=0; uin=o0329661289; skey=@EWfzuAEM9; ptisp=ctc; qm_username=329661289; qm_sid=4eb698d094eaae718a354bf2c1efa959,qZW42RTNlcHB4NlNsclR3OExwNGswOWdIZ25wSHBzS2NvNSpNWHB0MnZtOF8.; blabla=dynamic; Loading=Yes; p_skey=j-1uWYvxOCWfj7iEyTXmDgTkHeUIeOuRm6bLDX7*2UM_; pt4_token=z8jFnTfuorsacsCelOnf2A__; pgv_info=ssid¯ºìSY',
			'Connection':'keep-alive'
			}
#url = "http://127.0.0.1:8000/show_password1/"
#url = "http://www.zhihu.com/settings/account"
#url = "http://www.zhihu.com"
url = "http://user.qzone.qq.com/329661289/main"
http = httplib2.Http(cache=None, timeout = 10)
response, move_content = http.request(url, headers=qzone_header)
soup = BeautifulSoup(move_content) 
print (soup)
