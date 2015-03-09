import os
import re

from embedList import setCompile
from util import memorize, webpage, initMech

class vidSeries(webpage):
    pageComp       = NotImplemented
    siteTemplate   = NotImplemented
    seriesTemplate = NotImplemented
    
    def __init__(self, seriesName, extras=None, cookie=None):
        self.extras = extras
        self.name = seriesName
        self.br = initMech(self.siteTemplate.format(''), cookie)
        if extras:
            self.runExtras()

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
        def embed(self):
            return self.embedded(self.embedLink)
        @property
        @memorize
        def embedLink(self):
            if self.series:
                return self.series.siteTemplate.format(self.linkComp.search(self.source).group('link'))
            return self.linkComp.search(self.source).group('link')
        @property
        @memorize
        def video(self):
            if hasattr(self, 'compSearch'):
                setCompile(self)
            return self.vidComp.search(self.embed.source).group('vid')

        class embedded(webpage):
            def __init__(self, link):
                self.link  = link
            @property
            @memorize
            def url(self):
                return self.link
                
