import json
import asyncio
import json
import time

import aiohttp
import async_timeout
import os
import requests

from mutagen.mp3 import MP3
from mutagen.id3 import ID3NoHeaderError
from mutagen.id3 import ID3, TIT2, TALB, TPE1, TPE2, COMM, USLT, TCOM, TCON, TDRC

# filename = "c:\\Users\\starc\\Downloads\\The Killers - Mr. Brightside.mp3"

# Example which shows how to automatically add tags to an MP3 using EasyID3

async def fetch(session, url):
    async with async_timeout.timeout(10):
        async with session.get(url) as response:
            return await response.text()

async def addTags(temp, i, filename):
    async with aiohttp.ClientSession() as session:
        artist, name = temp

        if ('(' in name):
            name = name[:name.rfind('(')]
        url = f"https://orion.apiseeds.com/api/music/lyric/{artist}/{name}?apikey=9qfmD9f5MagVEjzWJP7QFEbpS1PjUgYdwCxD91gr9tFHzl2X5kLxqb2IAnyb8imE"

        json_str = await fetch(session, url)
        try:
            dic = json.loads(json_str)
        except:
            dic = {}

        # url = f"https://orion.apiseeds.com/api/music/lyric/{artist}/{name}?apikey=9qfmD9f5MagVEjzWJP7QFEbpS1PjUgYdwCxD91gr9tFHzl2X5kLxqb2IAnyb8imE"
        # dic = json.loads(requests.get(url).text)


        # create ID3 tag if not present
        try:
            tags = ID3(filename)
        except ID3NoHeaderError:
            print("Adding ID3 header;")
            tags = ID3()

        print(i, '. ', artist, name, end="")
        i += 1
        tags["TIT2"] = TIT2(encoding=3, text=name)
        tags["TPE2"] = TPE2(encoding=3, text=artist)

        tags["COMM"] = COMM(encoding=3, lang=u'eng', desc='desc', text=u'mutagen comment')
        tags["TPE1"] = TPE1(encoding=3, text=artist)

        if "result" in dic:
            print(" -- add text", end='')
            tags[u"USLT::'eng'"] = (USLT(encoding=3, lang=u'eng', desc=u'desc', text=dic["result"]["track"]["text"]))

        tags.save(filename)

        print()

        
def main(start=0):
    i = 0
    loop = asyncio.get_event_loop()
    for root, dirs, files in os.walk("E:\сводная музяка"):
        for f in files:

            filename = os.path.join(root, f)
            i += 1
            if filename.endswith('.mp3') and i>=start:
                # print(filename)
                temp = f[:-4].split(' - ')
                if len(temp)==2:
                    loop.run_until_complete(addTags(temp, i, filename))


                    


# mp3file = MP3(filename, ID3=EasyID3)
#
# try:
#     mp3file.add_tags(ID3=EasyID3)
# except mutagen.id3.error:
#     print("has tags")
#
# mp3file['title'] = 'Mr. Brightside'
# mp3file['artist'] = 'The Killers'
# mp3file.save()
# print(mp3file.pprint())
if __name__ == "__main__":
    main(205)