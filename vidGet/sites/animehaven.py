import re
from bs4 import BeautifulSoup, SoupStrainer
try:
    from vidGet.vidsite import vidSeries
    from vidGet.util import memorize, runRepl, unescape, webpage
except ImportError:
    from vidsite import vidSeries
    from util import memorize, runRepl, unescape, webpage

class animehaven(vidSeries):
    siteTemplate   = 'http://animehaven.org/{}'
    seriesTemplate = siteTemplate
    tags  = ['ah', 'animehaven']
    matchIt = re.compile('Episodes.*')
    
    def runExtras(self):
        for i in self.extras:
            if 'dub' in i:
                self.matchIt = re.compile('Episodes.*Dub.*')
    def listPages(self, url, cp=1, lp=None):
        curUrl = url if cp == 1 else '/'.join([url, 'page', str(cp)])
        intUrlObj = webpage(curUrl, self.br)
        if not lp:
            try:
                lpSoup = BeautifulSoup(intUrlObj.source, 'html.parser', parse_only=SoupStrainer('nav'))
                lp = int(lpSoup.find('nav', class_='pagination').findAll('a')[-1]['href'].split('/')[-1])
            except AttributeError:
                lp = 1
        intUrlObj.strainOnly = 'article'
        pages = [self.page(i.a['href'], self) for i in intUrlObj.soup.findAll('h2')]
        if cp < lp:
            pages.extend(self.listPages(url, cp+1, lp))
        return pages
    
    @property
    @memorize
    def pages(self):
        try:
            return self.listPages(self.soup.find('a', text=self.matchIt)['href'])[::-1]
        except:
            return self.listPages(self.url)[::-1]
        
    class page(vidSeries.page):
        
        @property
        @memorize
        def video(self):
                self.strainOnly = 'a'
                hold = self.soup
                return next(dlink['href'] for qual in ['720', '480']
                            for dlink in self.soup.findAll('a') if qual in dlink.text)
