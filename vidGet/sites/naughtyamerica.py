import re
try:
    from vidGet.vidsite import vidSeries
    from vidGet.util import memorize, webpage, initMech
except ImportError:
    from vidsite import vidSeries
    from util import memorize, webpage, initMech

class naughtyamerica(vidSeries):
    pageCheck      = False
    siteTemplate   = 'http://members.naughtyamerica.com{}'
    seriesTemplate = siteTemplate.format('/pornstar/{}/?')
    tags, type_    = ['na'], 'Model'
    
    def __init__(self, series, extras=None, cookie=None):
        self.name = series
        self.br = initMech(self.siteTemplate.format(''), cookie)
        if extras:
            self.extras = extras.split(',')
            self.runExtras()
    
    def runExtras(self):
        for i in self.extras:
            if 'site' in i:
                if '=' in i:
                    self.last = i.split('=')[-1]
                    self.serType = 'sites'
                self.type_ = 'Site'
                self.seriesTemplate = self.siteTemplate.format('/sites/{}/?')
            elif 'title' in i:
                self.title = i.split('=')[-1]
            elif 'pref' in i:
                self.pref = i.split('=')[-1]

    @property
    def title(self):
        return self.soup.find(
            'p', 
            class_='pornstar-name'
            ).text.replace(u'\xa0', '_')
    @property
    @memorize
    def pages(self):
        pages =  [self.page(i.a['href'], self) 
                 for i in self.soup.findAll('p', class_='pornstar-name') ]
        if hasattr(self, 'last'):
            base = '/'.join(['/{}'.format(self.serType), self.name, '?&p={}'])
            otherPages = [base.format(i) for i in xrange(1, 5)]
        else:
            try:
                otherPages = [i['href'] for i in self.soup.find('div', id="pagination_more_porn_videos").findAll('a') 
                              if not i.has_attr("class")]
            except AttributeError:
                return pages
        for i in otherPages:
            hold = webpage(self.siteTemplate.format(i), self.br)
            pages = pages + [self.page(i.a['href'], self) 
                    for i in hold.soup.findAll('p', class_='pornstar-name')]
        return pages

    #@property
    #def preview(self):
    #    return [self.soup.find('div', class_='picture-container').img['src'],
    #            self.soup.find('div', class_='right-banner-background')['style'].split('\'')[1]]
    class page(vidSeries.page):
        @property
        @memorize
        def name(self):
            return self.video.split('?')[0].split('/')[-1]
        @property
        @memorize
        def video(self):
            pref = ['480p'] #, 'MPEG4']
            url = next(i['href'] for i in self.soup.find('div', id='video_download').findAll('a')
                       if any('480p' in s for s in i['rel']))
            return url #self.series.br.open(url)
