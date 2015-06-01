import re
from bs4 import BeautifulSoup, SoupStrainer
try:
    from vidGet.vidsite import vidSeries
    from vidGet.util import memorize, runRepl, unescape, webpage
except ImportError:
    from vidsite import vidSeries
    from util import memorize, runRepl, unescape, webpage

class animeflavor(vidSeries):
    siteTemplate   = 'http://www.animeflavor.com{}'
    seriesTemplate = siteTemplate.format('/cartoon/{}')
    tags  = ['af', 'animeflavor']
    
    #def runExtras(self):
        #for i in self.extras:
            #if 'dub' in i:
                #self.matchIt = re.compile('Episodes.*Dub.*')
            #elif 'pref' in i:
                #self.pref = i.split('=')[-1]
    
    @property
    @memorize
    def pages(self):
        return [self.page(i.a['href'], self) for i in self.soup.findAll('ul', class_='menu')[1].findAll('li')]
        
    class page(vidSeries.page):
        vidComp = re.compile('file: \"(?P<vid>[^\"]*)\"')
        @property
        def embed(self):
            return webpage(self.embedLink)
        @property
        def embedLink(self):
            #try:
                #link = self.soup.find('div', class_='tab-body first ').iframe['src']
            #except:
                #link = self.soup.find('div', class_='node').find('div', 
                                             #class_='content').find('iframe')['src']
            return self.soup.find(src=re.compile('filehoot'))['src']
        @property
        def url(self):
            return self.series.siteTemplate.format(self.episode)
        
