import cookielib
import functools
import httplib
import mechanize
import requests
import sys
import time
from bs4 import BeautifulSoup, SoupStrainer

bs4 = BeautifulSoup
strain = SoupStrainer

if sys.version_info.major >= 3:
    import urllib.request as urllib2
    from html.parser import HTMLParser as parser
else:
    import urllib2
    from HTMLParser import HTMLParser as parser


useragent = ('User-agent',
             ''.join(['Mozilla/5.0 (X11; U; Linux i686;',
                      'en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9',
                      ' Firefox/3.0.1'])
             )


def display(message, level=0, clrLine=False):
    if level <= results.verb:
        if clrLine:
            global l
            if 'l' not in globals():
                try:
                    l = int(subprocess.check_output(['tput', 'cols']))
                except:
                    l = 50
            sys.stdout.write('\r{: ^{i}}'.format('', i=l))
        sys.stdout.write(message)
        sys.stdout.flush()


def initMech(site, cookies=None):
    br = mechanize.Browser()

    br.set_handle_redirect(True)
    br.set_handle_referer(True)
    br.set_handle_robots(False)
    br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
    br.addheaders = [useragent]
    if cookies:
        cj = cookielib.MozillaCookieJar(filename=cookies)
        cj.load(ignore_expires=True)
        br.set_cookiejar(cj)
    hold = bs4(br.open(site), 'html.parser')
    try:
        if 'login' in hold.text:
            br.select_form(nr=0)
            hold = br.submit()
    except:
        pass
    return br


def memorize(obj):
    cache = obj.cache = {}

    @functools.wraps(obj)
    def memoizer(*args, **kwargs):
        key = str(args) + str(kwargs)
        if key not in cache:
            cache[key] = obj(*args, **kwargs)
        return cache[key]
    return memoizer


def openUrl(req):
    try:
        return urllib2.urlopen(req, timeout=20.0)
    except urllib2.HTTPError as err:
        if err.code == 416:
            display('File already complete!\n', 1)
        else:
            raise


def runRepl(startPnt):
    repl = {'%3A': ':', '%2F': '/', '%3F': '?', '%3D': '=', '%26': '&',
            '%2C': ','}
    for i in repl.items():
        startPnt = startPnt.replace(*i)
    return startPnt


def sigIntHandler(signal, frame):
    # Catch all the CTRL+C
    sys.stdout.write('\nSigInt Caught, Terminating...\n')
    sys.exit(0)


def unescape(in_data):
    repl = {'%3F': '?', '%26': '&', '%3D': '=', '%2F': '/', '%3A': ':'}
    for i in repl.items():
        in_data = in_data.replace(*i)
    return parser().unescape(in_data)


class timing():
    def __init__(self):
        self.updateTime()

    def tryRun(self, toRun, runOpts, gap=2):
        current = time.time()
        if (current - self.lastRun) > gap:
            self.updateTime()
            toRun(*runOpts)

    def updateTime(self):
        self.lastRun = time.time()


class timeIt():
    def __init__(self, name, current):
        self.fileName = name
        self.oldSize = current
        self.oldTime = int(time.time())
        self.spRange = [0]

    def speed(self, current):
        timeCheck = int(time.time())-self.oldTime
        if timeCheck > 2:
            self.oldTime = int(time.time())
            self.spRange.append(((current-self.oldSize)/timeCheck)/1024)
            self.oldSize = current
        return self.rangeIt()

    def rangeIt(self):
        avg = 0
        if len(self.spRange) < 5:
            rangeTo = self.spRange
            divisor = len(self.spRange)
        else:
            rangeTo = self.spRange[-5:]
            divisor = 5
        for i in rangeTo:
            avg += i
        return avg/divisor

    @staticmethod
    def adj(speed):
        if speed > (100*1024):
            return (50*1024)
        elif speed > (50*1024):
            return (20*1024)
        else:
            return 1024


class webpage():
    def __init__(self, url=None, br=None):
        if url:
            self.url = url
        if br:
            self.br = br

    @property
    @memorize
    def soup(self):
        if hasattr(self, 'strainOnly'):
            so = strain(self.strainOnly)
            return bs4(self.source, 'html.parser', parse_only=so)
        return bs4(self.source, 'html.parser')

    @property
    def source(self):
        while True:
            try:
                if hasattr(self, 'br'):
                    if 'phantom' in self.br.__str__():
                        return self.br.page_source
                return self.urlObj.content
                # return str(self.urlObj.read())
            except httplib.IncompleteRead:
                pass

    @property
    @memorize
    def url(self):
        return self.seriesTemplate.format(self.name)

    @property
    def urlObj(self):
        if hasattr(self, 'br'):
            if 'phantom' in self.br.__str__():
                return self.br.get(self.url)
            return self.br.open(self.url)
        else:
            return requests.get(self.url)
            #req = urllib2.build_opener()
            #req.addheaders = [useragent]
            #return req.open(self.url)
