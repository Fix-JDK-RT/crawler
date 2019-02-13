import requests
import re
from bs4 import BeautifulSoup

regexp = '(http|https)://([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?'
init_site = 'https://stackoverflow.com/'
init_domain = 'stackoverflow.com'
sites_poll = []
completed_poll = []
domain_block = True
i = 0
sites_poll.append(init_site)
for site in sites_poll:
    if site in completed_poll: continue
    try:
        req = requests.get(site)
    except BaseException as e:
        print('Site: {} cause exception {}'.format(site,str(e)))
        continue
    completed_poll.append(site)
    text = BeautifulSoup(req.text,'html.parser')
    text = text.find('body')
    if text == None:
        print('Can\'t find body element')
        continue
    i += 1
    index = open('index.txt', 'a')
    index.write('{}. {}\n'.format(i,site))
    index.close()
    file = open('{}.txt'.format(str(i)),'w',encoding='utf-8')
    text_without_empty_lines = '\n'.join(filter(None,text.text.split('\n')))
    file.write(text_without_empty_lines)
    file.close()
    for each in re.findall(regexp,req.text):
        if domain_block:
            if each[1].__contains__(init_domain):
                url = each[0] + '://' + each[1] + each[2]
                if not url in sites_poll:
                    sites_poll.append(url)
        else:
            url = each[0] + '://' + each[1] + each[2]
            if not url in sites_poll:
                sites_poll.append(url)
    print('Completed {}'.format(len(completed_poll)))