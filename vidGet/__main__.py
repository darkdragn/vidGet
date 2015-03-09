#!/usr/bin/python
import argparse
import os
import socket 
import subprocess
import sys
import time

if sys.version_info.major >= 3:
    import urllib.request as urllib2
    import http.cookiejar as cookielib
else:
    import urllib2
    import cookielib

try:
    import vidGet.sites as sites
    from vidGet.util import timeIt
    importClass = lambda i: getattr(__import__('vidGet.sites.{}'.format(i), 
                                               fromlist=[i]), i)
except ImportError:
    import sites
    from util import timeIt
    importClass = lambda i: getattr(__import__('sites.{}'.format(i), 
                                               fromlist=[i]), i)

def currentSave(link, name):
    currentPath = '/'.join([name.split('/')[0], '.current'])
    if os.path.exists(currentPath):
        with open(currentPath, 'rb') as f:
            hold = f.read()
            if name == hold.split('\t')[0]:
                return hold.split('\t')[1]
            else:
                return None
    else:
        with open(currentPath, 'wb') as f:
            f.write('\t'.join([name, link]))
        return None
    
def currentRemove(name):
    currentPath = '/'.join([name.split('/')[0], '.current'])
    os.remove(currentPath)
    
def display(message, level=0, clrLine=False):
    if level <= results.verb:
        if clrLine:
            global l
            if not 'l' in globals():
                try:
                    l = int(subprocess.check_output(['tput', 'cols']))
                except:
                    l = 50
            sys.stdout.write('\r{: ^{i}}'.format('', i=l))
        sys.stdout.write(message)
        sys.stdout.flush()

def downEpisode(link, name):
    if not link:
        return
    cur, curSize, fileMode = 0, None, 'wb'
    #linkAlt = currentSave(link, name)
    req = urllib2.Request(link)
    req.headers['User-agent'] = ''.join(['Mozilla/5.0 (X11; U; Linux i686; ',
                                'en-US) AppleWebKit/534.3 (KHTML,like Gecko) ',
                                'Chrome/6.0.472.14 Safari/534.3'])
    display('Beginning on {}\n'.format(name.split('/')[-1]), 2)
    if os.path.exists(name):
        curSize = os.path.getsize(name)
        req.headers['Range'] = 'bytes=%s-' % (curSize)
    if not 'downUrl' in locals().keys() or not downUrl:
        downUrl = openUrl(req)
    try:
        total = int(downUrl.info().get('content-length'))
    except:
        return
    if downUrl.getcode() == 200:
        if total == curSize:
            display('File already complete!\n', 1)
            return
    elif downUrl.getcode() == 206:
        total = total+curSize if curSize else total
        cur   = curSize if curSize else 0
        fileMode = 'ab'
    speedCheck = timeIt(name, cur)
    with open(name, fileMode) as f:
        lenTo = 1024
        while True:
            buffer = downUrl.read(lenTo)
            if cur == total:
                break
            elif len(buffer) == 0:
                raise socket.timeout
            f.write(buffer)
            cur += len(buffer)
            speed = speedCheck.speed(cur)
            lenTo = speedCheck.adj(speed)
            display('\r{cur}Kb/{total}Kb[{:-<20}]{speed: >5}KB/s'.format(('+' *
                    int((cur)*20/total)), cur=cur/1024, total=int(total/1024), 
                    speed=speed), 2, 1)
        f.flush()
        f.close()
    display('  Finished!!! \n', 2)
    #currentRemove(name)

def listAll():
    print('{: <20}{}\n{: <20}{}'.format('Sites', 'Tags', '-----', '----'))
    for num, i in enumerate(site):
        print('{: <20}{}'.format(''.join([sites.__all__[num], ':']), 
                                 ', '.join(i.tags)))
    sys.exit()
    
def loadCookie(fileName):
    cookies = cookielib.MozillaCookieJar(filename=fileName)
    cookies.load()
    #handler = urllib2.HTTPHandler(debuglevel=1)
    return [urllib2.HTTPCookieProcessor(cookies)]

def main(testIt, cookie=None):
    dirIt = testIt.title
    #Test to see if we need to make the folder.
    if not os.path.exists(dirIt) and not results.noDir:
        os.makedirs(dirIt)
    total = len(testIt.pages)
    display('Model {name} contains {num} episodes.\n'.format(name=testIt.title, 
                                                              num=len(testIt.pages)), 2)
    # Main loop, does the downloading/saving
    if results.noDir:
        nameIt = lambda x: '{}_{:0>2}.mp4'.format(testIt.title, x)
    else:
        nameIt = lambda x: '/'.join([testIt.title, '{}_{:0>2}.mp4'.format(testIt.title, x)])
    if results.epi:
        page = testIt.pages[results.epi-1]
        name = page.name if hasattr(page, 'name') else nameIt(resulte.epi)
        downEpisode(page.video, name)
    else:
        pages = testIt.pages[results.startEpi-1:]
        for num, page in enumerate(pages, results.startEpi):
            while True:
                try:
                    if not num == results.epiSkip:
                        if page.name:
                            downEpisode(page.video, '/'.join([testIt.title, page.name]))
                        else:
                            downEpisode(page.video, nameIt(num))
                        break
                except AttributeError:
                    print('Unable to download {}.'.format(nameIt(num)))
                    raise
                except (urllib2.httplib.ssl.SSLError, socket.timeout):
                    #testIt.cleanup()
                    display(' Timeout Error! Cleaning up...\n', 1)
                    #sys.exit()
                except urllib2.URLError:
                    display('Unable to download due to timeout.\n', 1)
    if hasattr(testIt, 'cleanup'):
        testIt.cleanup()
    display('Complete!!!\n', 1)
    
def openUrl(req):
    try:
        return urllib2.urlopen(req, timeout=20.0)
    except urllib2.HTTPError:
        display('File already complete!\n', 1)
        #display(''.join([req.get_full_url(), '\n']), 1)
        return None

if __name__ == '__main__':
    site = [importClass(i) for i in sites.__all__]
    
    parser=argparse.ArgumentParser('animeGet Cli')
    parser.add_argument('ser', action='store', metavar='series', nargs='?',
                        help='Unique identifier for the series to rip.')
    parser.add_argument('-c', action='store', dest='cookie', default=None, 
                        metavar='cookie', help='Specify a cookie file.')
    parser.add_argument('-e', action='store', dest='epi', default=None, type=int,
                        metavar='epi', help='Specify a episode number.')
    parser.add_argument('-es', action='store', dest='epiSkip', default=None, type=int,
                        metavar='epiSkip', help='Specify a episode number to skip.')
    parser.add_argument('-ex', action='store', dest='extras', default=None,
                        metavar='extras', help='Extra options, site specific.')
    parser.add_argument('-nd', action='store_true', dest='noDir', 
                        help='Save the resulting file in the current directory.')
    parser.add_argument('-se', action='store', dest='startEpi', default=1, type=int,
                        metavar='startEpi', help='Specify a episode number to start with.')
    parser.add_argument('-s', action='store', dest='site', default='bb', 
                        metavar='site', help='Specify a site.')
    parser.add_argument('-sl', action='store_true', dest='list', 
                        help='List all supported sites.')
    parser.add_argument('-v', action='store', dest='verb', default=4, type=int,
                        metavar='verb', help='Specify a verbosity level.')
    
    results = parser.parse_args()
    if results.list:
        listAll()
    if not results.list and not results.ser:
        parser.print_help()
        sys.exit()
    for i in site:
        for tag in i.tags:
            if results.site == tag:
                main(i(results.ser, results.extras, results.cookie))
            
    # ### For future expansion ###
    # cookie=None
    # if results.cookie:
    #     cookie=loadCookie(results.cookie)
    
