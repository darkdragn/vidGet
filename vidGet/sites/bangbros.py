import re

try:
    from vidGet.vidsite import vidSeries
    from vidGet.util import memorize
except ImportError:
    from vidsite import vidSeries
    from util import memorize

class bangbros(vidSeries):
    siteTemplate = 'http://beta.members.bangbros.com{}'
    seriesTemplate = siteTemplate.format('/product/1/girl/{}')
    tags = ['bb', 'bangbros']
    pageList = lambda self: self.soup.findAll('span', class_='echThumbLnk-desc')
    
    def runExtras(self):
        for i in self.extras.split(','):
            if 'site' in i:
                self.pageList = lambda self: self.soup.findAll('div', 
                                             class_='vdoThumbHolder')[-1].findAll('span', class_='echThumbLnk-desc')
                self.seriesTemplate = self.siteTemplate
                self.siteLoad()
            elif 'title' in i:
                self.title = i.split('=')[-1]
    @property 
    @memorize
    def pages(self):
        return [self.page(self.siteTemplate.format(i.a['href']), self) 
                for i in self.pageList(self)]
    def siteLoad(self):
        self.br.open(self.url)
        self.br.click_link(link=self.br.find_link(text_regex=re.compile('Latest.*')))
        self.source = self.br.response().read()
    @property
    @memorize
    def title(self):
        return self.soup.h1.text.replace(' ', '')
    class page(vidSeries.page):
        
        @property
        @memorize
        def name(self):
            return self.video.split('&')[1].split('=')[1]
        @property
        @memorize
        def video(self):
            for i in ['720', '480']:
                for t in self.soup.findAll('div', class_='wtm-btnHolder clearfix'):
                    for b in t.findAll('a'):
                        if '720' in b['href'] and 'mp4' in b['href']:
                            return b['href']
