import telebot
from google.cloud import vision
import os
import requests

#here put path to your credentials file(.json)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="google_cloud.json"

#creating vision client
client=vision.ImageAnnotatorClient()

#paste your bot token here
token="YOUR TOKEN HERE"

bot=telebot.AsyncTeleBot(token)

#handle all photos sent
@bot.message_handler(content_types=["photo"])
def photo(msg):
    #download file
    file_info=bot.get_file(msg.photo[-1].file_id).wait()
    img=bot.download_file(file_info.file_path).wait()
    #get text from image, if error occured-stop
    try:
      text=client.annotate_image({
  "image": {"content":img},
  "features": [{"type": vision.enums.Feature.Type.DOCUMENT_TEXT_DETECTION}],
  "image_context":{"language_hints":["en"]}
}).full_text_annotation.text
    except Exception:
      return
    #send the text to http://0x0.st and send user the link
    hasted_url=requests.post("http://0x0.st",files={"file":text}).text.rstrip()
    bot.send_message(msg.chat.id,"*Here it is the information I could get from the picture:*\n"+hasted_url,parse_mode="markdown")
    #delete the photo
    bot.delete_message(msg.chat.id,msg.message_id)

bot.polling(none_stop=True) 