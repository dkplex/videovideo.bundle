TITLE = 'videovideo.dk'
SHOWS_URL = 'http://www.videovideo.dk/shows/json'
ART = 'art-default.jpg'
ICON = 'icon-default.png'

###################################################################################################
def Start():

	# Plugin setup
	Plugin.AddViewGroup("InfoList", viewMode="InfoList", mediaType="items")
	Plugin.AddViewGroup("List", viewMode="List", mediaType="items")

	# Object / Directory / VideoClip setup
	ObjectContainer.title1 = TITLE
	ObjectContainer.view_group = 'InfoList'
	ObjectContainer.art = R(ART)
	DirectoryObject.thumb = R(ICON)
	DirectoryObject.art = R(ART)
	VideoClipObject.thumb = R(ICON)
	VideoClipObject.art = R(ART)

	# HTTP setup
	HTTP.CacheTime = CACHE_1HOUR
	HTTP.Headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:16.0) Gecko/20100101 Firefox/16.0'

###################################################################################################
@handler('/video/videovideo', TITLE, thumb=ICON, art=ART)
def MainMenu():

	oc = ObjectContainer()
	shows = JSON.ObjectFromURL(SHOWS_URL)

	for show in shows:
		oc.add(DirectoryObject(
			key = Callback(BrowseShow,
				title = show.get('title'),
				url = show.get('url')),
			title = show.get('title'),
			thumb = Resource.ContentsOfURLWithFallback(url=show.get('image'), fallback=ICON),
			summary = show.get('description')
		))

	return oc

###################################################################################################
@route('/video/videovideo/show')
def BrowseShow(title, url):

	oc = ObjectContainer(view_group="List", title2=title)
	episodes = JSON.ObjectFromURL(url)

	for episode in episodes:
		oc.add(VideoClipObject(
			url = video.get('url'),
			title = video.get('title'),
			summary = video.get('shownotes'),
			thumb = Resource.ContentsOfURLWithFallback(url=video.get('image'), fallback=ICON),
			duration = TimeToMs(video.get('duration')),
			originally_available_at = Datetime.ParseDate(video.get('timestamp')).date()
		))

	return oc

###################################################################################################
def TimeToMs(timecode):

	seconds  = 0
	duration = timecode.split(':')
	duration.reverse()

	for i in range(0, len(duration)):
		seconds += int(duration[i]) * (60**i)

	return seconds * 1000
