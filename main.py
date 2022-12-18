import requests
import json
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from datetime import datetime
#from instapy_cli import client
from instabot import Bot
import os
from time import sleep

class image_generator():
    def __init__(self, width=1080, height=1350):                
        #1080px by 1080px (Square) 
        #1080px by 1350px (Portrait)
        #1080px by 608px (Landscape)

        self.image = Image.new("RGB", (width, height), (255, 255, 255))
        background_image = self.get_random_image(width, height)
        self.image.paste(background_image)
        self.draw = ImageDraw.Draw(self.image)
        quote = self.get_random_quote()
        self.main(quote)
    
    def main(self, quote):
        quote = self.modified_quote(quote)
        color = (255, 255, 255)

        font = ImageFont.truetype('arial.ttf', 48)
        (x, y) = (150, self.image.height/1.766)
        self.add_text_to_image(x,y, quote, font, color)
            
        (x, y) = (150, self.image.height-66)
        font = ImageFont.truetype('arial.ttf', size=45)
        self.add_text_to_image(x,y, '-ThefCraft', font, color)

        (x, y) = (self.image.width/1.7, self.image.height-56)
        font = ImageFont.truetype('arial.ttf', size=22)
        time = str(datetime.utcnow())
        self.add_text_to_image(x,y, f"UTC Time: {time[:time.find('.')]}", font, color, add_shadow=False)

    def save(self, filename): self.image.save(filename)
    def get_image(self): return self.image

    def get_random_image(self, width, height):
        background_image_url = f"https://source.unsplash.com/random/{width}x{height}"
        response = requests.get(background_image_url)
        background_image = Image.open(BytesIO(response.content))
        return background_image

    def add_text_to_image(self, pos_x, pos_y, text, font, color, add_shadow = True):
        self.draw.text((pos_x, pos_y), text, fill=color, font=font)
        if add_shadow:
            offset = (2, 2)
            shadow_color = (100, 100, 100)
            self.add_text_to_image(pos_x+offset[0], pos_y+offset[1], text, font, shadow_color , add_shadow=False)

    def get_random_quote(self):
        quotes_url = "https://zenquotes.io/api/random"
        response = requests.get(quotes_url)
        json_data = json.loads(response.text)
        quote = json_data[0]['q']
        return quote    

    def modified_quote(self, quote):
        message = quote
        i = 1
        message_with_returns=""
        temp_message = message
        final_message=""
        ch_count=0
        messageA = []
        strln=len(temp_message)

        #104/26 = 4
        theCut=26
        while strln>=0:
            if strln<=26:
                messageA.append(temp_message[0:])
                strln=0
                break
            else:
                #message_with_returns +=  temp_message + "\n"
                #print(message_with_returns)
                temp = temp_message[theCut:len(temp_message)]
                try: cut = theCut + temp.index(" ")
                except: cut=26
                messageA.append(temp_message[0:cut])
                temp_message= temp_message[cut:len(temp_message)]
                strln=len(temp_message)
                # print(str(strln)+"strln")
        message_final=""
        for o in messageA: message_final += o + "\n"
        return message_final

def instagram_uploder(username, password, image_path = 'main.jpg', text = 'Posted by a bot' + '\r\n' + '#ThefCraft #pythondeveloper'):
    
    time = str(datetime.utcnow())
    time = f"UTC Time: {time[:time.find('.')]}"

    #with client(username, password) as cli: 
        #cli.upload(image_path, time+'\n'+text)    
    bot = Bot()
    bot.login(username = username, password = password)
    bot.upload_photo(image_path, caption = time)#+'\n'+text)

def cleaner():
    filepath = "main.jpg.REMOVE_ME"
    if os.path.exists(filepath): os.remove(filepath)

while True:
    try:
        image = image_generator()
        image.save("main.jpg")
        cleaner()
        instagram_uploder(username='daily.quotes.bot', password='')
    except Exception as e:
        with open('main.log', 'a') as f:
            time = str(datetime.utcnow())
            time = f"UTC Time: {time}"
            f.write(f'{time}: A Error is occurred "{str(e)}"')
            f.write('\n')
    finally:
        break
        sleep(3600)
