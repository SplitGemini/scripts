from telethon import TelegramClient,sync
from telethon.tl.types import InputMessagesFilterPhotos
import sys
import os
proxy = None
# =============需要被替换的值=================
'''
api_id 你的api id
api_hash 你的api hash
channel_link 要下载图片的频道链接
proxy 将localhost改成代理地址,12345改成代理端口
picture_storage_path 图片下载到的路径
'''
api_id = 
api_hash = ""
channel_link = "https://t.me/Clashclient"
proxy =("socks5","localhost",2222) #不需要代理的话删掉该行
if len(sys.argv) == 2:
    channel_link = sys.argv[1]
picture_storage_path = os.path.join(os.getcwd(),channel_link.replace("https://t.me/",""))

client = TelegramClient(os.path.join(sys.path[0],'my_session'),api_id=api_id,api_hash=api_hash,proxy=proxy).start()
    
photos = client.get_messages(channel_link, None, filter=InputMessagesFilterPhotos)
    
total = len(photos)
index = 0
for photo in photos:
    filename = picture_storage_path + "/" +str(photo.id) + ".jpg"
    index = index + 1
    print("downloading:", index, "/", total, " : ", filename)
    client.download_media(photo, filename)
    
client.disconnect()
print("Done.")
