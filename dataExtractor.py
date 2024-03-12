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
'''retroflexwords = {
      "Malayalam": ['ആട്ടാ', 'ഇട്ടി', 'ഉട്ടു', 'എട്ടെ', 'ഒട്ടൊ'],
      "Kannada": ['ಆಟ್ಟಾ', 'ಇಟ್ಟಿ', 'ಉಟ್ಟು', 'ಎಟ್ಟೆ', 'ಒಟ್ಟೊ'],
      "Hindi": ['आट्टा','इट्टि','उट्टु','एट्टे','ओट्टो'],
      "Marathi": ['आट्टा','इट्टि','उट्टु','एट्टे','ओट्टो'],
      "Tamil": ['ஆட்டா','இட்டி','உட்டு','எட்டெ','ஒட்டொ'],
      "Bengali": ['আট্টা','ইট্টি','উট্টু','এট্টে','ওট্টো'],
      "Roman"  : ['aTTa', 'iTTi', 'uTTu', 'eTTe', 'oTTo']
    }
    
dentalwords = {
      "Malayalam": ['ആത്താ', 'ഇത്തി', 'ഉത്തു', 'എത്തെ', 'ഒത്തൊ'],
      "Kannada": ['ಆತ್ತಾ', 'ಇತ್ತಿ', 'ಉತ್ತು', 'ಎತ್ತೆ', 'ಒತ್ತೊ'],
      "Hindi": ['आत्ता','इत्ति','उत्तु','एत्ते','ओत्तो'],
      "Marathi": ['आत्ता','इत्ति','उत्तु','एत्ते','ओत्तो'],
      "Tamil": ['ஆத்தா','இத்தி','உத்து','எத்தெ','ஒத்தொ'],
      "Bengali": ['আত্তা','ইত্তি','উত্তু','এত্তে','ওত্তে'],
      "Roman"  : ['atta', 'itti', 'uttu', 'ette', 'otto']
    }
    
labialwords = {
      "Malayalam": ['ആപ്പാ', 'ഇപ്പി', 'ഉപ്പു', 'എപ്പെ', 'ഒപ്പൊ'],
      "Kannada": ['ಆಪ್ಪಾ', 'ಇಪ್ಪಿ', 'ಉಪ್ಪು', 'ಎಪ್ಪೆ', 'ಒಪ್ಪೊ'],
      "Hindi": ['आप्पा', 'इप्पि', 'उप्पु', 'एप्पे', 'ओप्पो'],
      "Marathi": ['आप्पा', 'इप्पि', 'उप्पु', 'एप्पे', 'ओप्पो'],
      "Tamil": ['ஆப்பா', 'இப்பி', 'உப்பு', 'எப்பெ', 'ஒப்பொ'],
      "Bengali": ['আপ্পা', 'ইপ্পি', 'উপ্পু', 'এপ্পে', 'ওপ্পো'],
      "Roman"  : ['appa', 'ippi', 'uppu', 'eppe', 'oppo']
    }'''

wordDictionary = dict(zip(['ആട്ടാ', 'ഇട്ടി', 'ഉട്ടു', 'എട്ടെ', 'ഒട്ടൊ']+
                          ['ಆಟ್ಟಾ', 'ಇಟ್ಟಿ', 'ಉಟ್ಟು', 'ಎಟ್ಟೆ', 'ಒಟ್ಟೊ']+
                          ['आट्टा','इट्टि','उट्टु','एट्टे','ओट्टो']+
                          ['ஆட்டா','இட்டி','உட்டு','எட்டெ','ஒட்டொ']+
                          ['আট্টা','ইট্টি','উট্টু','এট্টে','ওট্টো']+
                          ['ആത്താ', 'ഇത്തി', 'ഉത്തു', 'എത്തെ', 'ഒത്തൊ']+
                          ['ಆತ್ತಾ', 'ಇತ್ತಿ', 'ಉತ್ತು', 'ಎತ್ತೆ', 'ಒತ್ತೊ']+
                          ['आत्ता','इत्ति','उत्तु','एत्ते','ओत्तो']+
                          ['ஆத்தா','இத்தி','உத்து','எத்தெ','ஒத்தொ']+
                          ['আত্তা','ইত্তি','উত্তু','এত্তে','ওত্তে']+
                          ['ആപ്പാ', 'ഇപ്പി', 'ഉപ്പു', 'എപ്പെ', 'ഒപ്പൊ']+
                          ['ಆಪ್ಪಾ', 'ಇಪ್ಪಿ', 'ಉಪ್ಪು', 'ಎಪ್ಪೆ', 'ಒಪ್ಪೊ']+
                          ['आप्पा', 'इप्पि', 'उप्पु', 'एप्पे', 'ओप्पो']+
                          ['ஆப்பா', 'இப்பி', 'உப்பு', 'எப்பெ', 'ஒப்பொ']+
                          ['আপ্পা', 'ইপ্পি', 'উপ্পু', 'এপ্পে', 'ওপ্পো'],
                          5*['aTTa', 'iTTi', 'uTTu', 'eTTe', 'oTTo']+
                          5*['atta', 'itti', 'uttu', 'ette', 'otto']+
                          5*['appa', 'ippi', 'uppu', 'eppe', 'oppo']))

if os.path.exists(os.path.join(os.getcwd(),"data")):
    shutil.rmtree(os.path.join(os.getcwd(),"data"))
os.mkdir(os.path.join(os.getcwd(),"data"))
for language in itemsPerLanguage:
    os.mkdir(os.path.join(os.getcwd(),"data",language))

with open(os.path.join(os.getcwd(),"jatos_results_data_20230823032947.txt"), encoding='utf8') as file:
    data = list(map(json.loads, file.readlines()))
    for item in data:
        language = item[1]["response"]["language"]
        itemsPerLanguage[language] += 1
        os.mkdir(os.path.join(os.getcwd(),"data",language,str(itemsPerLanguage[language])))
        count = 0
        for audioResponses in item[4:-2]:
            audioFileName = str(count)+"_"+wordDictionary[re.findall(">.+<", audioResponses["stimulus"])[0][1:-1]]
            audioFileName = os.path.join(os.getcwd(),"data", language,str(itemsPerLanguage[language]), audioFileName)
            with open(audioFileName+".webm", 'wb') as audioFile:
                audioFile.write(base64.b64decode(audioResponses["response"]))
            subprocess.run(["ffmpeg","-i",audioFileName+".webm",audioFileName+".wav"])
            subprocess.run(["rm", audioFileName+".webm"])
            count += 1
        print(item[-2]["response"])

