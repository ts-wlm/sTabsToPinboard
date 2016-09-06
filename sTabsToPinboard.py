import asyncio
import functools
import json
import requests
import subprocess
import urllib.parse

# create and start an event loop for submitting the data to pinboard
loop = asyncio.get_event_loop()
open_requests = 0

# the save_tab function is called asyncronously for each url/tab
def save_tab(tab):
    global open_requests, api_endpoint, shared, pinboard_token
    print('saving tab from {} with title {}'.format(tab['host'], tab['title']))
    payload = {
        'auth_token': pinboard_token,
        'url': tab['url'],
        'description': tab['title'],
        'tags': tab['tags'],
        'shared': shared
    }
    r = requests.get(api_endpoint, params = payload)
    print(r.url)
    open_requests -= 1
    if open_requests == 0:
        loop.call_later(3, loop.stop)
        with open('missing_domains.json', 'w') as outfile:
            json.dump(host_matching, outfile, indent = 4)

# read configuration
with open('sTabsToPinboard.json') as json_data_file:
    data = json.load(json_data_file)
    exclude_hosts = data["excludeHosts"]
    host_matching = data["hostMatching"]
    title_matching = data["titleMatching"]
    shared = data["shared"]
    always_tags = data["alwaysTags"]
    api_endpoint = data["apiEndpoint"]
    pinboard_token = data["pinboardToken"]

# run automation script and read data received
res=subprocess.run(['/usr/bin/osascript', './sTabsToPinboard.scpt'],
        universal_newlines=True, stderr=subprocess.PIPE)
tabs=json.loads(res.stderr)

# remove duplicates, local files and extract hosts from found tabs
# TODO: duplicates
tabs.sort(key=lambda tab: tab['url'])
prepared_tabs = [ {'url': tab['url'], 'title': tab['title'], 
    'host': urllib.parse.urlparse(tab['url']).netloc } 
    for tab in tabs if tab['url'][:4] != 'file' ]

# filter for excluded hosts (could also be done in prepared_tabs creation, but is
# more readable here
prepared_tabs = [ tab for tab in prepared_tabs if True not in 
    [ (hostname in tab['host']) for hostname in exclude_hosts ] ]

# enhance data with tags from configuration
for tab in prepared_tabs:
    matching_tags = []
    # host-specific tags
    matching_tags.extend([ element 
        for host in host_matching.keys() 
        for element in host_matching[host]
        if host in tab['host'] ])
    # title-specific tags
    matching_tags.extend([ element 
        for title in title_matching.keys() 
        for element in title_matching[title]
        if title in tab['title'].lower() ])
    # and put to tab (removing duplicates)
    tab['tags'] = list(set(matching_tags))

# now output 
for index, tab in enumerate(prepared_tabs):
    if len(tab['tags']) == 0:
        # ohne tags: leeren eintrag in hostsMatching anlegen, am ende dann konfig
        # speichern
        print('no tags for {}, {}'.format(tab['host'], tab['title']))
        host_matching[tab['host']] = []
    else:
        # auf pinboard speichern
        tab['tags'].extend(always_tags)
        tab['tags'] = ' '.join(tab['tags'])
        loop.call_later(index * 5, save_tab, tab)
        open_requests += 1

loop.run_forever()
