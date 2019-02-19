import requests
import re
from bs4 import BeautifulSoup

regexp = '(http|https)://([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?'
init_site = 'https://tproger.ru/'
init_domain = 'tproger.ru'
sites_poll = []
completed_poll = []
domain_block = True
i = 0
sites_poll.append(init_site)
for site in sites_poll:
    if site in completed_poll: continue
    try:
        req = requests.get(site,allow_redirects=False)
    except BaseException as e:
        print('Site: {} cause exception {}'.format(site,str(e)))
        continue
    completed_poll.append(site)
    text = BeautifulSoup(req.text,'html.parser')
    text = text.findAll('p')
    finaltext = ''

    if text != []:
        for part in text:
            finaltext += part.text
        if re.search(r'[^\W]', finaltext) == None:
            continue
        i += 1
        print(site)
        file = open('pages/{}.txt'.format(str(i)),'w',encoding='utf-8')
        file.write(finaltext)
        file.close()
    else:
        continue

    index = open('index.txt', 'a')
    index.write('{}. {}\n'.format(i,site))
    index.close()

    for each in re.findall(regexp,req.text):
        if domain_block:
            if each[1].__contains__(init_domain):
                url = each[0] + '://' + each[1] + each[2]
                if not url in sites_poll:
                    if not url.__contains__('wp-content'):
                        sites_poll.append(url)
        else:
            url = each[0] + '://' + each[1] + each[2]
            if not url in sites_poll:
                sites_poll.append(url)
    print('Completed {}/{}'.format(len(completed_poll),len(sites_poll)))