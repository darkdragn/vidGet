import os
import re

from util import memorize, webpage, initMech

class vidSeries(webpage):
    pageComp       = NotImplemented
    siteTemplate   = NotImplemented
    seriesTemplate = NotImplemented
    type_ = 'Series'
    
    def __init__(self, series, extras=None, cookie=None):
        if extras:
            self.extras = extras.split(',')
            self.runExtras()
        self.name = series
        self.br = initMech(self.siteTemplate.format(''), cookie)

    @property
    @memorize
    def pages(self):
        pages = []
        if hasattr(self, pageList):
            for i in pageList:
                hold = webpage(self.siteTemplate.format(pageList))
                [pages.append(self.page(i)) for i in self.pageIt(self.soup)]
        else:
            [pages.append(self.page(i)) for i in self.pageIt(self.soup)]
        return pages
    @property
    @memorize
    def title(self):
        return self.name
    
    class page(webpage):
        linkComp = NotImplemented
        vidComp  = NotImplemented
        vidName  = None
	
        def __init__(self, episode, series=None):
            self.episode = episode
            self.series = series
            if series:
                self.br = series.br
        @property
        @memorize
        def url(self):
            return self.episode
        @property
        @memorize
        def video(self):
            if hasattr(self, 'compSearch'):
                setCompile(self)
            return self.vidComp.search(self.embed.source).group('vid')
