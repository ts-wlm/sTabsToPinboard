# Safari Tabs to Pinboard

Save all open Safari-Tabs to Pinboard and close them. Predefined Tags for
RegExp-matched URLs can be used (ie. set tag 'article' for all Urls matching
.*newyorker\.com*.).

## Plan

1. Read URLs and titles from all open Safari windows and tabs and save them in one huge
   array of objects {url: , title: } ;)
1. Request each url, convert to text and use the first n characters as
   descriptions.
1. Match urls with tag-adders and extend each url with the respective tags.
1. Submit URLs to pinboard in a timeouted loop to respect pinboard api limits.
