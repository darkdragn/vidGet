from util import memorize, webpage, initMech


class vidSeries(webpage):
    pageCheck = False
    siteTemplate = NotImplemented
    seriesTemplate = NotImplemented
    type_ = 'Series'

    def __init__(self, series, extras=None, cookie=None):
        if extras:
            self.extras = extras.split(',')
            self.runExtras()
        self.cookie, self.name = cookie, series
        self.br = initMech(self.siteTemplate.format(''), cookie)

    @property
    @memorize
    def pages(self):
        return [self.page(self.formatPage(i), self)
                for i in self.pageList()]

    @property
    @memorize
    def title(self):
        return self.name

    class page(webpage):
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
            return self.vidComp.search(self.embed.source).group('vid')
