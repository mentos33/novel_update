import re
import time
import asyncio
import aiohttp
from general_headers import headers
#server api 
#text : title
#desp : body

'''
SCKEY : input your key
    SCKEY = 'SCKEY'
'''
SCKEY = ''

server_url = 'https://sc.ftqq.com/{0}.send'.format(SCKEY)
target_url = 'https://www.xbiquge.cc/book/24276/'

async def fetch_html(session, url):
    '''
    if update time changed, send message.
    args:
        1:session
        2:target url
    return:
        2: update time
    ''' 
    async with session.get(url) as response:
        return await response.text()

async def get_update_time(url):
    '''
    args:
        1:url
    return:
        1:update_time
    '''
    async with aiohttp.ClientSession(headers= headers) as session:
        html = await fetch_html(session, target_url)
        #print html
    get_update_time = re.compile(r'更新时间.*?(\d{4}-\d{2}-\d{2}\s?\d{2}:\d{2})')
    result = re.findall(get_update_time, html)# result : 2019-06-23 21:38
    return result

async def send_message_via_wx(server_url, sec_time):
    title = 'novel update!!!'
    params = {'text':title, 'desp':sec_time}
    async with aiohttp.ClientSession(headers= headers) as session:
        async with session.get(server_url, params = params) as resp:
            #resp.url
            return await resp.text()

async def main():
    first_time = await get_update_time(target_url)
    while True:
        sec_time = await get_update_time(target_url)
        if first_time[0] != sec_time[0]:
            try:
                r = await send_message_via_wx(server_url, sec_time[0])
                #r
            except Exception as e:
                print ('error: ',e)
                print ('send again...')
                await asyncio.sleep(60)
                try:
                    r = await send_message_via_wx(server_url, sec_time[0])
                except Exception as e:
                    print ('sec_error: ',e)

            else:
                print ('send success!')
            finally:
                first_time ,sec_time= sec_time, []
        else:
            print ('no update')
            print ('still running...')
        await asyncio.sleep(3600)

if __name__ == "__main__":
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        loop.close()
        
    
    