#!/usr/bin/env python

import urllib.parse
import http.client
import re
import time

username = 'USERNAME'
password = 'PASSWORD'

login_domain = 'secure.zyctd.com'
login_url = '/Ajax/AjaxHandle.ashx?CommandName=UserSignService/SignIn'
header_cookies = 'FromsAuthByDbCookie_zytd_Edwin.PrvGuest=1c1uuuuuuuuuuaIRVd9dRU61V69418cTb1Rc481V8T9Ua6SbWTb0o5qqnc78ca99o698qac9nadmoll5moad015; UM_distinctid=15c4427ea4c1-064a42ff17d2bf-396c7804-100200-15c4427ea4d6d1; ASP.NET_SessionId=a0eggxcymzs2zyjjwqdbstda; activePlatforms=https%3A//secure.zyccst.com/Ajax/AjaxHandle.ashx%2Chttps%3A//msecure.zyccst.com/Ajax/AjaxHandle.ashx%2Chttps%3A//securecs.zyccst.com/Ajax/AjaxHandle.ashx; lnXedStgli=; Hm_lvt_ba57c22d7489f31017e84ef9304f89ec=1495792086; Hm_lpvt_ba57c22d7489f31017e84ef9304f89ec=1495807881;'

headers = {
    'Content-type':'application/x-www-form-urlencoded',
    'Accept':'application/json, text/javascript, */*',
    'X-Requested-With':'XMLHttpRequest',
    'Cookie':header_cookies,
    'Referer':'https://secure.zyctd.com/signin/login?returnurl=%20http%3A//www.zyctd.com/'
}

params = urllib.parse.urlencode({'Data': {
    'LoginName':username,
    'Password':password,
    'IsNeedCheckCode':'false',
    'CheckCode':'',
    'AppID':2
}})
conn = http.client.HTTPSConnection(login_domain)
conn.request('POST', login_url, params, headers)
res = conn.getresponse()
response_headers = res.getheaders()
response_headers = ''.join([str(header) for header in response_headers])
#print('headers = ')
#print(response_headers)

cookies = re.findall('\'Set-Cookie\',\s+\'FromsAuthByDbCookie_zytd_Edwin=[\w%.-]+', response_headers)
for cookie in cookies:
    split_cookie = cookie.split(', ')
    header_cookies += split_cookie[1].replace('\'', '')
    header_cookies += '; '
header_cookies = header_cookies.strip()
print('header cookies =', header_cookies)
conn.close()

supplier_info_regex = r'<tr><td title="(?P<name>.*?)">.*?<div>.*?</div></td><td title="(?P<type>.*?)">.*?</td><td class="price">(?P<price>.*?)</td><td title="(?P<produced_at>.*?)">.*?</td><td title="(?P<stored_at>.*?)">.*?</td><td>(?P<contact>.*?)</td><td>(?P<phone>.*?)</td><td class="check"><a target="_blank" href=".*?">.*?</a></td></tr>'
http_header = {
    'Accept':'text/html,*/*',
    'Cookie':header_cookies,
    'Upgrade-Insecure-Requests':1
}
http_domain = 'www.zyctd.com'
conn = http.client.HTTPConnection(http_domain)

for i in range(1, 4):
    http_url = '/gqgy-p{}.html'.format(i)
    print('Getting supplier data from', http_url)
    conn.request('GET', http_url, headers=http_header)
    res = conn.getresponse()
    page_data = res.read().decode().replace('\r\n', '')
    page_data = re.sub('\s\s+', '', page_data)
    #print('data = ', page_data)

    # Parse data and save to CSV format
    supplier_data = re.findall('\<tr\>.+?\<\/tr\>', page_data)
    supplier_info_output = ''
    for supplier_info in supplier_data:
        # print(supplier_info)
        # print('===============')
        supplier_match = re.search(supplier_info_regex, supplier_info)
        result = '{},{},{},{},{},{},{}\n'.format(
            supplier_match.group('name'),
            supplier_match.group('type'),
            supplier_match.group('price'),
            supplier_match.group('produced_at'),
            supplier_match.group('stored_at'),
            supplier_match.group('contact'),
            supplier_match.group('phone')
        )
        supplier_info_output += result

    # print('output = ')
    # print(supplier_info_output)
    with open('supplier_contact.csv', 'a') as fh:
        fh.write(supplier_info_output)

    time.sleep(2)
