TITLE       = 'VideoVideo.dk'
PREFIX      = '/video/videovideo'
PATH        = 'http://www.videovideo.dk/'
ART         = 'art-default.jpg'
ICON        = 'icon-default.png'

###################################################################################################

def Start():
    
    # Plugin setup
    Plugin.AddPrefixHandler(PREFIX, MainMenu, TITLE, ICON, ART)
    Plugin.AddViewGroup("InfoList", viewMode="InfoList", mediaType="items")
    Plugin.AddViewGroup("List", viewMode="List", mediaType="items")
    
    # Object / Directory / VideoClip setup
    ObjectContainer.title1      = TITLE
    ObjectContainer.view_group  = 'InfoList'
    ObjectContainer.art         = R(ART)
    DirectoryObject.thumb       = R(ICON)
    DirectoryObject.art         = R(ART)
    VideoClipObject.thumb       = R(ICON)
    VideoClipObject.art         = R(ART)
    
    # HTTP setup
    HTTP.CacheTime              = CACHE_1HOUR
    HTTP.Headers['User-Agent']  = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:12.0) Gecko/20100101 Firefox/12.0'

###################################################################################################

@route('/video/videovideo')
def MainMenu():
    
    # create container
    oc = ObjectContainer()
    
    try:
        
        shows = JSON.ObjectFromURL(PATH + 'shows/json')
        
        for show in shows:
            
            # add elements to container
            oc.add(DirectoryObject(
                                   key      = Callback(BrowseShow, 
                                                         title = show.get('title'),
                                                         url = show.get('url')),
                                   title    = show.get('title'),
                                   thumb    = Resource.ContentsOfURLWithFallback(url=show.get('image'), fallback=ICON),
                                   summary  = show.get('description')
                                   ))
        
    except :
        
        oc.header = "UPS!!!"
        oc.message = "Ingen forbindelse til VideoVideo"
    
    return oc

###################################################################################################

def BrowseShow(title = TITLE, url = ''):
    
    # create container
    oc = ObjectContainer(view_group="List", title1 = TITLE, title2 = title)
    
    try:
        
        episodes = JSON.ObjectFromURL(url)
    
    except :
    
        raise Ex.MediaNotAvailable
        
    for episode in episodes:
        
        # add elements to container
        oc.add(getVideoObj(episode))
    
    
    return oc

###################################################################################################

def getVideoObj(video = dict):
    
    # find video url
    if video.get('distributions').get('720'):
        url = video.get('distributions').get('720')
    elif video.get('distributions').get('480'): 
        url = video.get('distributions').get('720')
    
    # find duration
    duration = 0
    if video.get('duration'): 
        duration_dict = video.get('duration').split(':')
        duration += int(duration_dict[0])*60*60
        duration += int(duration_dict[1])*60
        duration += int(duration_dict[2])
        duration = duration * 1000
    
    return  VideoClipObject(url = url, 
                            title = video.get('title'), 
                            summary = video.get('shownotes'), 
                            thumb = Resource.ContentsOfURLWithFallback(url=show.get('image'), fallback=ICON),
                            duration = duration,
                            originally_available_at = Datetime.ParseDate(video.get('timestamp')))
    
