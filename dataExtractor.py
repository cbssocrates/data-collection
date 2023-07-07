import os
import json
import subprocess
import base64
import shutil
import re

itemsPerLanguage = {"Bengali":0,
                    "Malayalam":0,
                    "Tamil":0,
                    "Marathi":0,
                    "Hindi":0,
                    "Kannada":0}

if os.path.exists(os.path.join(os.getcwd(),"data")):
    shutil.rmtree(os.path.join(os.getcwd(),"data"))
os.mkdir(os.path.join(os.getcwd(),"data"))
for language in itemsPerLanguage:
    os.mkdir(os.path.join(os.getcwd(),"data",language))

with open(os.path.join(os.getcwd(),"jatos_results_data_20230707060405.txt"), encoding='utf8') as file:
    data = list(map(json.loads, file.readlines()))
    for item in data:
        language = item[1]["response"]["language"]
        itemsPerLanguage[language] += 1
        os.mkdir(os.path.join(os.getcwd(),"data",language,str(itemsPerLanguage[language])))
        count = 0
        for audioResponses in item[4:-2]:
            audioFileName = str(count)+"_"+re.findall(">.+<", audioResponses["stimulus"])[0][1:-1]
            audioFileName = os.path.join(os.getcwd(),"data", language,str(itemsPerLanguage[language]), audioFileName)
            with open(audioFileName+".webm", 'wb') as audioFile:
                audioFile.write(base64.b64decode(audioResponses["response"]))
            subprocess.run(["ffmpeg","-i",audioFileName+".webm",audioFileName+".wav"])
            subprocess.run(["rm", audioFileName+".webm"])
            count += 1
        print(item[-2]["response"])

