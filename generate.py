from radarplot.CIKM import *
from jinja2 import Environment, FileSystemLoader


TEMPLATE_DIR = 'templates'
ITEMS_PER_PAGE = 60
ANCHOR_PAG = 9
WEB_DIR = 'web'
IMG_DIR = WEB_DIR + '/img'
VID_DIR = WEB_DIR + '/vid'
PAGE_NAME = 'index'

template = Environment(
    autoescape=False,
    loader=FileSystemLoader(TEMPLATE_DIR),
    trim_blocks=False)
cikm = CIKM('train.txt', 'train.index')
radar_data = []
pagesn = int(cikm.getSize() / ITEMS_PER_PAGE) # number of pages

def pagination (n, anchor, size):
    """Returns a list with the pagination numbers.
    n is the current page, anchor is the number of pages in
    the pagination bar and size is the total number of pages to
    be paginated. Page list start at 1 and ends at size."""
    padding = int(anchor / 2)
    if (n > padding and n <= (size - padding)):
        a = n - padding
        b = n + padding
    elif (n <= padding):
        a = 1
        b = anchor
    elif (n > (size - padding)):
        a = size - anchor + 1
        b = size
    return range(a, b + 1)

for i, radar in enumerate(cikm.getAllRadars(sorted=True, reversed=True)):
    print("Reading radar {}".format(radar.getID()))
    posinpage = i % ITEMS_PER_PAGE     # postion of the image in the page
    page = int(i / ITEMS_PER_PAGE)
    
    meta = {}
    meta["thumbnail"] = "img/{}.png".format(radar.getID())
    meta["id"] = radar.getID()
    meta["label"] = radar.getLabel()
    meta["video"] = "vid/{}.mp4".format(radar.getID())
    radar_data.append(meta)
    
    radar.plotThumbnail('{}/{}'.format(IMG_DIR, radar.getID()))
    radar.plot('{}/{}.mp4'.format(VID_DIR, radar.getID()))
               
    # if we are in the last element of the page we render the current page
    if (posinpage == ITEMS_PER_PAGE - 1):
        print('Rendering page {}'.format(page + 1))
        with open('{}/{}{}.html'.format(WEB_DIR, PAGE_NAME, str(page)), 'w') as f:
            tpl = template.get_template('index-basic.html')
            html = tpl.render(radars = radar_data,
                              pagination = pagination(page + 1, ANCHOR_PAG, pagesn),
                              current = page + 1,
                              last = pagesn - 1)
            f.write(html)
        radar_data = []
