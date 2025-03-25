from flask import Flask, request, abort

from linebot.v3 import (
    WebhookHandler
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,  
    TextMessage,   
    LocationMessage,   
    ImageMessage

)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent,  
    FollowEvent  
)

import os

app = Flask(__name__)

configuration = Configuration(access_token=os.getenv('CHANNEL_ACCESS_TOKEN'))
line_handler = WebhookHandler(os.getenv('CHANNEL_SECRET'))


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        line_handler.handle(body, signature)
    except InvalidSignatureError:
        app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

# 加入好友事件
@line_handler.add(FollowEvent)
def handle_follow(event):
    print(f'Got {event.type} event')
    
# 文字訊息
@line_handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    text = event.message.text
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)

        if text == '產品':
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text="消費性中低壓MOSFET、工業用高壓高功率IGBT、Super Junction以及先進GaN/SiC原料製程產品")]
                )
            ) 
        elif text == '企業核心價值':
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text="1.創新:功率離散元件 (POWER DISCRETE DEVICE) 必須以不斷創新來支持日新月異之科技產品"),TextMessage(text="2.誠信:本公司以誠信為本，經營公司、服務客戶"),TextMessage(text="3.功率離散元件 (POWER DISCRETE DEVICE)為支援終端產品之螺絲釘，只有真誠不斷的服務，才能支持造就客戶之產品與市場")]
                )
            )
        elif text == '經營理念':
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text="1.成就客戶，共存共榮"),TextMessage(text="2.壯大公司營運，回饋股東，照顧員工，繁榮社會"),TextMessage(text="3.建立合作平台，融合跨界資源，擴大市場領域"),TextMessage(text="4.永續經營。遵循ESG的理念及運作，永續經營，保護地球")]
                )
            )
        elif text == '願景':
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text="1.壯大博盛為多角經營之世界級公司"),TextMessage(text="2.成為世界級一流之功率離散元件提供者"),TextMessage(text="3.不斷設計生產Enhancing everyday life的產品及相關的技術服務")]
                )
            )         
        elif text == '圖片':
            url="https://www.potens-semi.com/upload/2019/08/201908070850545306WZVV3WN2L.jpg"            
            app.logger.info("url=" + url)
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[
                        ImageMessage(original_content_url=url, preview_image_url=url)
                    ]
                )
            )             
        elif text == '位置':
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[
                        LocationMessage(title='博盛半導體股份有限公司', address="新竹", latitude=24.807418, longitude=121.036620)
                    ]
                )
            )
        else:
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text ="請輸入關鍵字:產品/企業核心價值/經營理念/圖片/願景/位置")]
                )
            )




if __name__ == "__main__":
    app.run()