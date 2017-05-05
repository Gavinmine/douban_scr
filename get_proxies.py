# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import httplib2
import socket


def getHtmlContent(url):
    http = httplib2.Http(cache=None, timeout=10)
    try:
        response, content = http.request(url)
    except socket.timeout:
        print("Can not access %s" % url)
        return None

    content = content.decode('utf-8')
    soup = BeautifulSoup(content, "lxml")
    return soup


def getProxies(soup):
    proxyList = []
    proxies = soup.find_all('tr')[1:]
    for proxy in proxies:
        ip = proxy.find_all('td')[0].get_text()
        port = proxy.find_all('td')[1].get_text()
        ip_port = "%s:%s" % (ip, port)
        proxyList.append(ip_port)

    return proxyList

if __name__ == "__main__":
    PROXIES = []
    url = "http://www.kuaidaili.com/free/"
    soup = getHtmlContent(url)
    PROXIES.extend(getProxies(soup))

    print(PROXIES)
        
