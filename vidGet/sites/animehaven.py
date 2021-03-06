import re
from multiprocessing import Pool
from bs4 import BeautifulSoup, SoupStrainer
try:
    from vidGet.vidsite import vidSeries
    from vidGet.util import memorize, runRepl, unescape, webpage
except ImportError:
    from vidsite import vidSeries
    from util import memorize, runRepl, unescape, webpage

bs4 = BeautifulSoup

def getSet(inVars):
    url, page = inVars
    curUrl = '/'.join([url, 'page', str(page)])
    intUrlObj = webpage(curUrl)
    so = SoupStrainer('article')
    soup = BeautifulSoup(intUrlObj.urlObj.read(), 'html.parser',
                                                  parse_only=so)
    return [ i.a['href'] for i in soup.findAll('h2')]

class animehaven(vidSeries):
    siteTemplate   = 'http://animehaven.org/{}'
    seriesTemplate = siteTemplate
    tags  = ['ah', 'animehaven']
    matchIt = re.compile('Episodes.*')
    
    def runExtras(self):
        for i in self.extras:
            if 'dub' in i:
                #self.matchIt = re.compile('Episodes.*Dub.*')
                self.matchIt = re.compile('English.*Dub.*')
            elif 'pref' in i:
                self.pref = i.split('=')[-1]
    def listPages(self, url):
        curUrl = url 
        intUrlObj = webpage(curUrl, self.br)
        try:
            lpSoup = BeautifulSoup(intUrlObj.source, 'html.parser', 
                                   parse_only=SoupStrainer('nav'))
            lp = int(lpSoup.find('nav', class_='pagination').findAll('a')[-1]['href'].split('/')[-1])
        except AttributeError:
            lp = 1
        pool = Pool(processes=4)
        pages = pool.map(getSet, [(url, x) for x in range(1, lp+1)])
        pool.close()
        ret = []
        for i in pages[::-1]:
                ret.extend(self.page(p, self) for p in i[::-1])
        return ret
    
    @property
    @memorize
    def pages(self):
        try:
            return self.listPages(self.soup.find('a', text=self.matchIt)['href'])
        except:
            return self.listPages('/'.join([self.seriesTemplate.format('episodes/subbed'),self.name]))
        
    class page(vidSeries.page):
        
        @property
        @memorize
        def video(self):
            pref, self.strainOnly = ['720', '480'], 'a'
            if hasattr(self.series, 'pref'):
                next(pref.insert(0, pref.pop(pref.index(i)))
                     for i in pref if self.series.pref in i)
            try: 
                return next(dlink['href'] for qual in pref
                            for dlink in self.soup.findAll('a', class_='btn') 
                            if qual in dlink.text)
            except:
                urlTemp = 'http://{}.tiwi.kiwi/{}/v.mp4'
                grouping = (480, 720, 1080)
                
                while True:
                    try:
                        embedLink = self.soup.find('div', 
                                         class_='download_feed_link').a['href']
                        break
                    except AttributeError:
                        self.soup = bs4(self.source)
                
                embed = webpage(embedLink)
                matchIt  = re.search("init\|(.*)\|updateSrc", embed.source)
                group    = matchIt.group(1).split('|')
                try:
                    firstHit = re.search("img src=\"http://(.*)\.tiwi.kiwi", 
                                         embed.source).group(1)
                except AttributeError as e:
                    urlTemp = 'http://{}/{}/v.mp4'
                    firstHit = re.search("img src=\"http://([^/]*)/", 
                                         embed.source).group(1)

                return next(urlTemp.format(firstHit, group[num])               
                            for qual in pref for num, i in enumerate(grouping)
                            if qual in str(i))
