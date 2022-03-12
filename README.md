# eve-bot
<img src="https://i.ytimg.com/vi/o-l269A9I38/maxresdefault.jpg">

## Introduction
A Discord bot I created in Python. Her name is Eve. I've been working on her since the summer of 2020, and I said that once I get a working chatbot feature up, I'd host her on Heroku for everyone to use full-time, along with posting the code on my Github. So, at long last, here she is. 

Disclaimer: The images are from an old MMORPG named <a href="https://elsword.koggames.com/">Elsword</a>. I take no credit.

If you would like more information on her different commands, please refer to my <a href="https://charles-yuan.netlify.app/eve.html">website</a>.

## Getting Started
To get started, you'll need to <a href="https://discord.com/developers/docs/intro">sign up</a> to become a Discord developer, create a bot (application), then get your token. 

### Deployment
Once you have your token, if you are deploying locally, go to line 231 in ```eve.py``` and replace TOKEN with your token:

```
self.client.run("YOUR TOKEN HERE")
```

Finally, you can run:
```
python eve.py
```

### Prerequisites
```
-f https://download.pytorch.org/whl/torch_stable.html
torch==1.10.2+cpu
torchvision==0.11.3+cpu
torchaudio===0.10.2+cpu
transformers==4.16.2
asyncio==3.4.3
nextcord==2.0.0a8
datetime==4.3
bs4==0.0.1
python-docx==0.8.11
requests==2.26.0
requests_html==0.10.0
urllib3==1.26.6
wikipedia==1.4.0
PyDictionary==2.0.1
mathparse==0.1.2
python-dateutil==2.7.5
sqlalchemy==1.3.0
pytz==2021.1
```

## Built With
### nextcord (previously discord.py)
An API wrapper for Discord written in Python. Migrated from the previous version (discord.py). Basically the backbone of this entire project.

### transformers (pytorch-transformers by Hugging Face)
Hugging Face's transformers library provides thousands of pretrained models to perform tasks on different modalities such as text, vision, and audio. I mainly used it for Eve's chatbot function, which worked very well but can't be deployed due to the RAM limitations of Heroku Dynos (max. 512 MB each). 

## Future Plans
### Update (Feb 21, 2022):
Eve has now been migrated to nextcord and is now the official bot of the EngSci Machine Intelligence 2T4 server!

### Update (Feb 23, 2022):
;-; I can't deploy the chatbot function. Is anyone willing to sponsor me $250/month for the Performance M Dyno package?

### Update (Mar 11, 2022):
Eve now has embeds! They're integrated into the help, define, and wiki commands.

<p float="left">
<img src="https://github.com/Chubbyman2/eve-bot/blob/main/docs/eve_embed_sample_2.PNG" width="412">
<img src="https://github.com/Chubbyman2/eve-bot/blob/main/docs/eve_embed_sample.png" width="412">
</p>

## License
This project is licensed under the MIT License - see the <a href="https://github.com/Chubbyman2/eve-bot/blob/main/LICENSE">LICENSE</a> file for details.
