#!/usr/bin/env python2
from vidGet import sites
from vidGet.util import timeIt, timing
import argparse
import os
import signal
import socket
import subprocess
import sys

##########################################
#        Version Specific Imports        #
if sys.version_info.major >= 3:
    import urllib.request as urllib2
else:
    import urllib2


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


def downEpisode(link, name):
    if not link:
        return
    cur, curSize, fileMode = 0, None, 'wb'
    req = urllib2.Request(link)
    user_agent = ''.join(['Mozilla/5.0 (X11; U; Linux i686; ',
                          'en-US) AppleWebKit/534.3 (KHTML,like Gecko) ',
                          'Chrome/6.0.472.14 Safari/534.3'])
    req.headers['User-Agent'] = user_agent
    display('Beginning on {}\n'.format(name.split('/')[-1]), 2)
    if os.path.exists(name):
        curSize = os.path.getsize(name)
        req.headers['Range'] = 'bytes=%s-' % (curSize)
    if 'downUrl' not in locals().keys():
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
        total = total + curSize if curSize else total
        cur = curSize if curSize else 0
        fileMode = 'ab'
    speedCheck = timeIt(name, cur)
    check = timing()
    with open(name, fileMode) as f:
        lenTo = 1024
        while True:
            buffer = downUrl.read(lenTo)
            cur += len(buffer)
            speed = speedCheck.speed(cur)
            lenTo = speedCheck.adj(speed)
            try:
                remain = (total-cur)/(1024*speed)
                remainMsg = '\tRemaining: {min:02}:{sec:02}'.format(
                        min=remain/60,
                        sec=remain % 60
                )
            except ZeroDivisionError:
                remainMsg = '\tStandby...'
            tickerMsg = '\r{cur}Kb/{total}Kb[{:-<20}]'.format(
                        ('+' * int((cur)*21/total)), cur=cur/1024,
                        total=int(total/1024))
            speedMsg = '{speed: >5}KB/s'.format(speed=speed)
            disPas = [' '.join([tickerMsg, speedMsg, remainMsg]), 2, 1]
            check.tryRun(display, disPas)
            if cur == total:
                display(*disPas)
                break
            elif len(buffer) == 0:
                display(*disPas)
                raise socket.timeout
            f.write(buffer)
            f.flush()
    display('  Finished!!! \n', 2)


def downPreview(imgs, dirIt):
    for num, img in enumerate(imgs):
        outName = ''.join(['preview_', str(num), '.jpg'])
        urlObj = urllib2.urlopen(img)
        with open('/'.join([dirIt, outName]), 'wb') as f:
            f.write(urlObj.read())


def listAll():
    print('{: <20}{}\n{: <20}{}'.format('Sites', 'Tags', '-----', '----'))
    for num, i in enumerate(site):
        print('{: <20}{}'.format(''.join([sites.__all__[num], ':']),
                                 ', '.join(i.tags)))
    sys.exit()


def main(testIt, cookie=None):
    dirIt = testIt.title
    # Test to see if we need to make the folder.
    if not os.path.exists(dirIt) and not results.noDir:
        os.makedirs(dirIt)
        writeStats(testIt)
    display('{type} {name} contains {num} episodes.\n'.format(
        type=testIt.type_,
        name=testIt.title,
        num=len(testIt.pages)), 2)
    # Main loop, does the downloading/saving
    name = '{}'
    if not results.noDir:
        dir_string = '/'.join([testIt.title, '{}'])
        name = name.format(dir_string)
    name_gen = name.format('{}_{}.mp4'.format(testIt.title, '{:03}'))
    if results.epi:
        page = testIt.pages[results.epi-1]
        name = name.format(page.name) if hasattr(page, 'name')\
            else name_gen.format(results.epi)
        downEpisode(page.video, name)
    else:
        pages = testIt.pages[results.startEpi-1:]
        if testIt.pageCheck:
            for i in pages:
                try:
                    i.video
                except StopIteration:
                    print("Missing a video here.")
        if hasattr(testIt, 'preview'):
            downPreview(testIt.preview, dirIt)
        for num, page in enumerate(pages, results.startEpi):
            while True:
                try:
                    if num == results.epiSkip:
                        break
                    if hasattr(page, 'name'):
                        out_name = page.name.format(num)
                    else:
                        out_name = name_gen.format(num)
                    link = page.video
                    if type(link) is tuple:
                        link[0](link[1], out_name)
                        break
                    else:
                        downEpisode(link.replace(' ', '%20'), out_name)
                        break
                except AttributeError:
                    print('Unable to download {}.'.format(out_name))
                except StopIteration:
                    print "Missing a video here."
                except urllib2.HTTPError as e:
                    display('HTTP error. Please check the url:\n', 1)
                    display(page.video)
                    break
                except (urllib2.httplib.ssl.SSLError,
                        socket.error, socket.timeout):
                    display(' Timeout Error! Cleaning up...\n', 1)
    if hasattr(testIt, 'cleanup'):
        testIt.cleanup()
    display('Complete!!!\n', 1)


def openUrl(req):
    try:
        return urllib2.urlopen(req, timeout=20.0)
    except urllib2.HTTPError as err:
        if err.code == 416:
            display('File already complete!\n', 1)
        else:
            raise


def sigIntHandler(signal, frame):
    # Catch all the CTRL+C
    sys.stdout.write('\nSigInt Caught, Terminating...\n')
    sys.exit(0)


def writeStats(series):
    with open('/'.join([series.title, '.stats']), 'w') as f:
        f.write('Link: {}\n'.format(series.name))
        f.write('Total: {}'.format(len(series.pages)))


if __name__ == '__main__':
    site = [getattr(sites, name) for name in sites.__all__]

    parser = argparse.ArgumentParser('vidGet Cli')
    parser.add_argument('ser', action='store', metavar='series', nargs='?',
                        help='Unique identifier for the series to rip.')
    parser.add_argument('-c', action='store', dest='cookie', default=None,
                        metavar='cookie', help='Specify a cookie file.')
    parser.add_argument('-e', action='store', dest='epi', default=None,
                        type=int, metavar='epi',
                        help='Specify a episode number.')
    parser.add_argument('-es', action='store', dest='epiSkip', default=None,
                        type=int, metavar='epiSkip',
                        help='Specify a episode number to skip.')
    parser.add_argument('-x', action='store', dest='extras', default=None,
                        metavar='extras', help='Extra options, site specific.')
    parser.add_argument('-nd', action='store_true', dest='noDir',
                        help=''.join(['Save the resulting file in the current',
                                      'directory.']))
    parser.add_argument('-se', action='store', dest='startEpi', default=1,
                        help='Specify a episode number to start with.',
                        type=int, metavar='startEpi')
    parser.add_argument('-s', action='store', dest='site', default='bb',
                        metavar='site', help='Specify a site.')
    parser.add_argument('-sl', action='store_true', dest='list',
                        help='List all supported sites.')
    parser.add_argument('-v', action='store', dest='verb', default=4, type=int,
                        metavar='verb', help='Specify a verbosity level.')

    results = parser.parse_args()
    signal.signal(signal.SIGINT, sigIntHandler)
    args = {'cookie': results.cookie, 'extras': results.extras,
            'series': results.ser}
    if results.list:
        listAll()
    if not results.list and not results.ser:
        parser.print_help()
        sys.exit()
    next(main(i.Series(**args)) for i in site
         for tag in i.tags if results.site == tag)
