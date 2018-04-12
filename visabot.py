#!/usr/bin/env python

from __future__ import print_function
from future import standard_library
from lxml import html
import requests
standard_library.install_aliases()
import urllib.request, urllib.parse, urllib.error
import json
import os
import sys
#import urlparse
from urllib.parse import urljoin
import emoji

from flask import Flask
from flask import request, render_template
from flask import make_response


# Flask should start in global layout
context = Flask(__name__)
# Facbook Access Token
ACCESS_TOKEN = "EAADSsDjm6gIBANlzUbBmbFLGpNvZBhnZCEw71BSMvwQZCK8n9KjaY5Pf8P5ZAZBlt9mKcLHe2AmU5hgq7XZAc4vedP5ISpyuRIBKuWMvYx6YI6976r5qpZBsI8vSoU4pmqvVqffjNVJuvCttk7EykTb9tUfHWCnjfivwKUZAA1S4WQZDZD"

#************************************************************************************#
#                                                                                    #
#    All Webhook requests lands within the method --webhook                          #
#                                                                                    #
#************************************************************************************#
reqContext = None
# Webhook requests are coming to this method
@context.route('/webhook', methods=['POST'])
def webhook():
    global reqContext
    reqContext = request.get_json(silent=True, force=True)
    #print(json.dumps(reqContext, indent=4))
    print("webhook---->" + reqContext.get("result").get("action"))
    print ("webhook is been hit ONCE ONLY")
    if reqContext.get("result").get("action") == "input.welcome":
       return welcome()
    elif reqContext.get("result").get("action") == "asktheuser":
       return asktheuser(reqContext)
    elif reqContext.get("result").get("action") == "nationality":
       return userNationality(reqContext)
    elif reqContext.get("result").get("action") == "nationalityrecheck":
       return userNationalityRecheck()
    elif reqContext.get("result").get("action") == "startover":
       return startOver()
    elif reqContext.get("result").get("action") == "destinationcountry":
       print ("User Input-->Citizenship -->" + reqContext.get("result").get("resolvedQuery"))
       return userDestinationCountry(reqContext)
    elif reqContext.get("result").get("action") == "wikipediasearch":
       print ("User Input-->Country Name -->" + reqContext.get("result").get("resolvedQuery"))
       return wikipedia_search(reqContext)
    else:
       print("Good Bye")

 
#************************************************************************************#
#                                                                                    #
#   This method is to get the Facebook User Deatails via graph.facebook.com/v2.6     #
#                                                                                    #
#************************************************************************************#
nationality = "False"
destinationcountry = "False"
def welcome():
    data = request.json
    print (data)
    if data is None:
        return {}
    #entry = data.get('originalRequest')
    platform = data.get('originalRequest').get('source')
    print ("PLATFORM -->" + platform)

    if platform == "facebook":
       id = data.get('originalRequest').get('data').get('sender').get('id')
       print ("id :" + id)
       fb_info = "https://graph.facebook.com/v2.6/" + id + "?fields=first_name,last_name,profile_pic,locale,timezone,gender&access_token=" + ACCESS_TOKEN
       print (fb_info)
       result = urllib.request.urlopen(fb_info).read()
       print (result)
       data = json.loads(result)
       first_name = data.get('first_name')
       print ("FACEBOOK: First Name -->" + first_name)
    elif platform == "telegram":
       first_name = data.get('originalRequest').get('data').get('message').get('chat').get('first_name')
       print ("TELEGRAM: First Name -->" + first_name)
    elif platform == "skype":
       first_name = "to Visa CheckBot"
       print ("SKYPE: Within Python")
       
    speech1 = "I'm Visa CheckBot - your one stop solution for visa related enquiry. "
    res = {
          "speech": speech1,
          "displayText": speech1,
           "data" : {
              "facebook" : [
                   {
                    "sender_action": "typing_on"
                  },
                  {
                 "attachment" : {
                   "type" : "template",
                     "payload" : {
                      "template_type" : "generic",
                       "elements" : [ 
                                 {
                                   "title" : "Welcome " + first_name + "! ",
                                   "image_url" : "http://kredist.ru/wp-content/uploads/2014/10/%D0%B2%D1%8B%D0%B5%D0%B7%D0%B4-%D0%B7%D0%B0-%D0%B3%D1%80%D0%B0%D0%BD%D0%B8%D1%86%D1%83-%D1%81-%D0%B4%D0%BE%D0%BB%D0%B3%D0%B0%D0%BC%D0%B8.jpg",
                                 } 
                           ]
                       } 
                   }
                },
                 {
                    "sender_action": "typing_on"
                  },
                 {
                 "text": speech1
                  },
                 {
                  "text": "So, let's start. Shall we?",
                  "quick_replies": [
                 {
                  "content_type": "text",
                  "title": "Yeah Sure",
                  "payload": "Yeah Sure",
                  "image_url": "http://gdurl.com/eNYq"
                 },
                 {
                  "content_type": "text",
                  "title": "No Thanks",
                  "payload": "No Thanks",
                  "image_url": "http://gdurl.com/uViQ"
                   }
                  ]
                 }
                ],
            "telegram": {
                 "photo": "http://kredist.ru/wp-content/uploads/2014/10/%D0%B2%D1%8B%D0%B5%D0%B7%D0%B4-%D0%B7%D0%B0-%D0%B3%D1%80%D0%B0%D0%BD%D0%B8%D1%86%D1%83-%D1%81-%D0%B4%D0%BE%D0%BB%D0%B3%D0%B0%D0%BC%D0%B8.jpg",
                 "text": "Welcome in Telegram -->" + first_name + "! " + speech1 + "So let's start, shall we?",
                 "reply_markup": { 
                   "inline_keyboard": [ 
                        [{ "callback_data": "Yeah Sure", "text": "Yeah Sure" }], 
                        [{ "callback_data": "No Thanks", "text": "No Thanks" }] 
                       ] 
                },
               }
             },
        "messages": [
        {
          "type": 4,
          "platform": "skype",
          "payload": {
            "skype": {
              "text": "Hier ist ein Video von Elie Saab",
              "attachments": [
                {
                  "contentType": "application/vnd.microsoft.card.hero",
                  "content": {
                    "title": "ELIE SAAB Bridal Spring 2018 | Backstage",
                    "subtitle": "von Elie Saab",
                    "images": [
                      {
                        "url": "https://i.ytimg.com/vi/DwTmaqoSlgs/default.jpg"
                      }
                    ],
                    "buttons": [
                      {
                        "type": "openUrl",
                        "title": "Auf Youtube ansehen",
                        "value": "https://youtu.be/DwTmaqoSlgs"
                      },
                      {
                        "type": "openUrl",
                        "title": "Elie Saab - Channel",
                        "value": "https://www.youtube.com/user/ElieSaabChannel"
                      }
                    ]
                  }
                }
              ]
            }
          }
        }
        ]
        };
    print (res)
    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    print (r)
    return r

def reply(user_id, msg):
    data = {
        "recipient": {"id": user_id},
        "message": {"text": msg}
    }
    print ("Data.........")
    print (data)
    resp = requests.post("https://graph.facebook.com/v2.6/me/messages?access_token=" + ACCESS_TOKEN, json=data)
    print(resp.content)

#************************************************************************************#
#                                                                                    #
#   Tell USER about Visa Check Bot - ASK TWO QUESTIONS                               #
#                                                                                    #
#************************************************************************************#
def asktheuser(reqContext):
    print (reqContext.get("result").get("action"))
    option = reqContext.get("result").get("action")
    res = {
        "speech": "Great! I'll ask two questions only",
        "displayText": "Great! I'll ask two questions only",
        "data" : {
        "facebook" : [
               {
                "text": "Great! I'll ask two questions only."
               },
              {
                    "sender_action": "typing_on"
              },
              {
                 "text": "Then only I can precisely tell whether you need a VISA or NOT to travel your destination country."
              },
              {
                    "sender_action": "typing_on"
              },
              {
                  "text": "Ready?",
                  "quick_replies": [
                 {
                  "content_type": "text",
                  "title": "I'm Ready",
                  "payload": "I'm Ready",
                 },
                 {
                  "content_type": "text",
                  "title": "No Thanks",
                  "payload": "No Thanks",
                  }
                  ]
                 }
             ],
        "telegram": {
                 "text": "Great! I'll ask two questions only. Then only I can precisely tell whether you need a VISA or NOT to travel your destination country.",
                 "reply_markup": { 
                   "inline_keyboard": [ 
                        [{ "callback_data": "I'm Ready", "text": "I'm Ready" }], 
                        [{ "callback_data": "No Thanks", "text": "No Thanks" }] 
                       ] 
                },
             }
           } 
         };
    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

#************************************************************************************#
#                                                                                    #
#   Asking the USER the FIRST QUESTION - What's Your Nationality?                    #
#                                                                                    #
#************************************************************************************#
data = None
def userNationality(reqContext):
    nationality = "False"
    destinationcountry = "False"
    print (reqContext.get("result").get("action"))
    res = {
        "speech": "What is your nationality?",
        "displayText": "What is your nationality?",
        "data" : {
        "facebook" : [
              {
                 "text": "What is your nationality?"
              }
             ],
        "telegram": {
                 "text": "What is your nationality?"
             }
           } 
         };
    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

###     START AGAIN       ###
def userNationalityRecheck():
    print ("******userNationalityRecheck********")
    nationality = ""
    destinationcountry = ""
    res = {
        "speech": "Which country do you want to travel?",
        "displayText": "Which country do you want to travel?",
        "data" : {
        "facebook" : [
              {
                 "text": "Which country do you want to travel?"
              }
             ],
        "telegram": {
                 "text": "Which country do you want to travel?"
             }
           } 
         };
    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

###   Start Over        ###
def startOver():
    print ("*********startOver*************")
    nationality = ""
    destinationcountry = ""
    res = {
        "speech": "What is your nationality?",
        "displayText": "What is your nationality?",
        "data" : {
        "facebook" : [
              {
                 "text": "What is your nationality?"
              }
             ],
        "telegram": {
                 "text": "What is your nationality?"
             }
           } 
         };
    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


#************************************************************************************#
#                                                                                    #
#   Asking the USER the SECOND QUESTION - What's Your Destination Country?           #
#                                                                                    #
#************************************************************************************#

def userDestinationCountry(reqContext):
    correct_nationality = ""
    print ("Within userDestinationCountry METHOD")
    resolvedQuery = reqContext.get("result").get("resolvedQuery")
    
    # Loading nationality input
    global nationality
    nationality = ""
    nationality = str(resolvedQuery).title()
    
    # Loading Nationality List into Array to validate against the user nationality input
    file_path = '/app/country_name_JSON.txt'
    with open(file_path) as f:
       data = json.loads(f.read())
       print("First Element from Nationality_List -->" + data[0]['nationality'])

    # Loading the Nationality list to validate nationality input:
    for data_item in data:
        str_nationality = str(data_item['nationality'])
        #print (str_nationality)
        if str_nationality == nationality:
           correct_nationality = nationality
           print ("This is the CORRECT nationality--->" + nationality)
           break
        
        
    if correct_nationality:
        print ("Which country do you want to travel?")
        speech = "Which country do you want to travel?"
        
    else:
        speech = "This is not a valid citizenship. Please enter a valid citizenship"
        print ("This is not a valid citizenship. Please enter a valid citizenship")
        userNationalityRecheck()
        

    print ("userDestinationCountry Method nationality --> " + nationality)
    res = {
        "speech": "Second Question",
        "displayText": speech,
        "data" : {
        "facebook" : [
              {
                 "text": speech
              }
             ],
        "telegram": {
                 "text": speech
             }
           } 
         };
    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

#************************************************************************************#
#                                                                                    #
#   This method is to get the Wikipedia Information via Google API                   #
#                                                                                    #
#************************************************************************************#

def wikipedia_search(reqContext):
    print ("***Nationality has the latest input-->" + nationality)
    resolvedQuery_wiki = reqContext.get("result").get("resolvedQuery")
    global nationalityNEW
    #To capitalize the first letter
    global destinationcountry
    destinationcountry = ""
    destinationcountry = str(resolvedQuery_wiki).title() 
    
    print ("destinationcountry: " + destinationcountry)
    
    # Check if the country name is abbreviated, put the correct names:
    if "Uae" in destinationcountry:
        destinationcountry = "United Arab Emirates"
    elif "Usa" in destinationcountry or "Us" in destinationcountry and "Russia" not in destinationcountry and "Mauritius" not in destinationcountry and "Cyprus" not in destinationcountry and "Australia" not in destinationcountry and "Austria" not in destinationcountry and "Belarus" not in destinationcountry:
        destinationcountry = "United States"
    elif "Uk" in destinationcountry or "England" in  destinationcountry and "Ukraine" not in destinationcountry:
        destinationcountry =  "United Kingdom"
            
    
    # Loading Nationality List into Array to validate against the user nationality input
    file_path = '/app/country_name_JSON.txt'
    with open(file_path) as f:
       data = json.loads(f.read())
       print("First Element from Nationality_List -->" + data[0]['nationality'])

    # Loading the Nationality list to validate nationality input:
    for data_item in data:
        str_destinationcountry = str(data_item['country_name'])
        if str_destinationcountry == destinationcountry:
           correct_str_destinationcountry = destinationcountry
           print ("This is the CORRECT destinationcountry--->" + destinationcountry)
           break
        

    print ("wikipedia_search Method nationality --> " + nationality)
    nationalityNEW = nationality
    jsoncountryappendage = "}}"
    destinationcountry1 = str(destinationcountry + jsoncountryappendage)
    print ("destinationcountry1--------->" + destinationcountry1)
    google_query = ''
    if nationalityNEW:
       google_query = str("https://en.wikipedia.org/w/api.php?action=query&prop=revisions&rvprop=content&format=json&&titles=Visa_requirements_for_" + nationalityNEW + "_citizens")
       nationalityNEW = ''
    else:   
       print ("Nationality value NULL, hence NO API Calling...!!!")
    ###########################################################

    if google_query is None:
        return {}
    print("google_query::::"+google_query)
    result = urllib.request.urlopen(google_query).read()
    #print (result)
    data1 = json.loads(result)
    infotoStringFinal = "0"
    #data1 = str(data1)
    wikidata = str(data1).split("{{flag|")
    for info in wikidata:
        #print ("info within FOR Loop--->" + info)
        if destinationcountry1 in info and "}}." not in info and "{{flagicon|" not in info:
           print ("I'm in IF loop, therefore I'm already in FOR loop")
           #infotoString = str(info)
           infotoStringFinal = str(info)
           print (infotoStringFinal)
           break
        elif destinationcountry in info and "|state<!" in info:
           print ("Exception handling for Peru, Belgium and Costa Rica")
           infotoStringFinal = info.split("|state<!")[0]
           print ("Country name: -->" + infotoStringFinal)
        else:
           continue
    print ("NECESSARY STRING -->")
    # Check all artifacts which are to be removed to get the VISA INFORMATION
    print (infotoStringFinal)
    #print ("Section splitlines -->" + infotoStringFinal.splitlines()

    if "Visa" in infotoStringFinal or "movement" in infotoStringFinal:
        #visa_status_primary = infotoStringFinal.split("\n| {{",1)[1]
        visa_status_primary = infotoStringFinal.split("}}<ref>")
        print ("After splitting }}<ref>, here is the 2nd part -->" + visa_status_primary[0])
        
        # Checking for the 1st && 3rd CATEGORY, like --> Denmark}} \n| {{no|Visa required OR Thailand}} \n| {{yes|Visa not required  Germany}}\n| {{free|{{sort|EU|Visa not required}}
        if "|{{" in visa_status_primary[0]:
           print ("3rd Category -> 1st clause of |{{ --> " + visa_status_primary[0])
           # Germany}}\n| {{free|{{sort|EU|Visa not required}}
           visa_status = visa_status_primary[0].split("{{")[2].split("}}")[0].split("|")[2].split("}}")[0]
           print ("3rd category: FINAL visa_status -->" + visa_status)
        
        elif "{{" in visa_status_primary[0]:
           visa_status_temp_1 = visa_status_primary[0].split("{{")
           print ("Splitting the {{ from the string and select LAST PART-->" + visa_status_temp_1[1])
           
           # Checking for the 1st CATEGORY, like --> Denmark}} \n| {{no|Visa required OR Thailand}} \n| {{yes|Visa not required
           if "|" in visa_status_temp_1[1]:
               visa_status_almst_fnl = visa_status_primary[0].split("{{")[1].split("|")[1]
               #visa_status = visa_status_temp_2[1]
               print ("1st category: FINAL visa_status -->" + visa_status_almst_fnl)
               if "}}" in visa_status_almst_fnl:
                   visa_status = visa_status_almst_fnl.split("}}")[0]
                   print ("If visa_status holds }} then split it -->" + visa_status)
               else:
                   visa_status = visa_status_almst_fnl
        
        # Checking for the 2nd CATEGORY, like --> Malaysia}} (e-Visa required)\n* 
        elif "(" in visa_status_primary[0]:
           visa_status_temp_1 = visa_status_primary[0].split("(")
           print ("Splitting the ( from the string and select LAST PART-->" + visa_status_temp_1[1])
           if ")" in visa_status_temp_1[1]:
               visa_status = visa_status_temp_1[1].split(")")[0]
               #visa_status = visa_status_temp_2[0]
               print ("2nd CATEGORY: FINAL visa_status -->" + visa_status_temp_1[1].split(")")[0])
        else:
           #visa_status = visa_status_primary[0]
           print ("ELSE: No exception found, so assigning same variable to visa_status_temp_1-->")
           
           # 5th CATEGORY like, Thailand}}\n| Visa on arrival\n| e-Visa for 60 Days\n|-\n|
           if "Visa" in visa_status_primary[0]:
               if "}}" in visa_status_primary[0]:
                   visa_status = visa_status_primary[0].split("|")[1].split("\n")[0]
                   print ("5th CATEGORY --->" + visa_status)
           elif "Visitor" in visa_status_primary[0]:
                if "}}" in visa_status_primary[0]:
                   visa_status = visa_status_primary[0].split("|")[1].splitlines()
                   print ("5th CATEGORY --->" + visa_status)
    else:
        visa_status = infotoStringFinal 
        print ("No change in VISA Status -->" + visa_status)
        # 4th CATEGORY like, Australia}}\n| {{yes|[[eVisitor]]}}<ref>{{Timatic|nationality=DK|destination=AU}}
        if "]]" in infotoStringFinal:
            print ("Check 4th Category-->" + infotoStringFinal.split("]]")[0].split("[[")[1])
            visa_status = infotoStringFinal.split("]]")[0].split("[[")[1]

    #########################################################################
    subtitle = "You need " + visa_status + " for " + destinationcountry
    #########################################################################
    if visa_status == "Visa required":
        image_url_final = str("https://www.iconsdb.com/icons/preview/red/visa-xxl.png")
    elif visa_status == "Visa not required" or visa_status == "Freedom of movement":
        image_url_final = str("https://www.iconsdb.com/icons/preview/green/visa-xxl.png")
    elif visa_status == "e-Visa required" or visa_status == "eVisa" or visa_status == "Visa on arrival" or visa_status == "eVisa / Visa on arrival":
        image_url_final = str("http://www.iconsplace.com/icons/preview/yellow/visa-256.png")
    elif visa_status == "0":
        image_url_final = "https://previews.123rf.com/images/lkeskinen/lkeskinen1707/lkeskinen170701095/81349455-no-information-rubber-stamp.jpg"
        visa_status = "Hmm, No VISA details found"
        subtitle = "Please check the spelling or see if it's a valid country name"
    else:
        image_url_final = str("http://www.iconsplace.com/icons/preview/yellow/visa-256.png")
############################################################
#    
############################################################
    res = {
          "speech": "Visa Status",
          "displayText": visa_status,
           "data" : {
              "facebook" : [
                  {
                    "sender_action": "typing_on"
                  },
                  {
                 "attachment" : {
                   "type" : "template",
                     "payload" : {
                      "template_type" : "generic",
                       "elements" : [ 
                                 {
                                   "title" : visa_status,
                                   "image_url" : image_url_final,
                                   "subtitle" : subtitle,
                                   "buttons": [{
                                        "type": "web_url",
                                        "url": "https://en.wikipedia.org/wiki/Visa_requirements_for_" + nationality + "_citizens",
                                        "title": "More info"
                                    },
                                    {
                                        "type": "element_share"
                                    }]
                                 } 
                           ]
                       } 
                   }
                },
                 {
                  "text": "Write another country name to continue checking VISA requirement",
                  "quick_replies": [
                 {
                  "content_type": "text",
                  "title": "Restart",
                  "payload": "startover",
                  },
                 {
                  "content_type": "text",
                  "title": "No",
                  "payload": "No",
                  }
                  ]
                 }
               ],
            "telegram": {
                 "text": subtitle + ". Write another country name to continue checking VISA requirement",
                 "reply_markup": { 
                   "inline_keyboard": [ 
                        [{ "callback_data": "startover", "text": "Restart" }], 
                        [{ "callback_data": "No", "text": "No" }] 
                       ] 
                },
             }
           } 
         };
    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


#************************************************************************************#
#                                                                                    #
#   Help Information Providing                                                       #
#                                                                                    #
#************************************************************************************#
def help(resolvedQuery):
    speech = "I'm sorry if I make you confused. Please select Quick Reply or Menu to chat with me. \n\n 1. Click on 'News' to read latest news from 33 globally leading newspapers \n 2. Click on 'Weather' and write a city name to get weather forecast \n 3. Click on 'Wikipedia' and write a topic you want to know about. No need to ask a full question. \n 4. Click on 'YouTube' and search for your favourite videos. \n 5. You can still chat directly with Marvin without the quick replies like before for - Weather, Wikipedia & Small Talk."
    res = {
        "speech": speech,
        "displayText": speech,
        "data" : {
        "facebook" : [
               {
                "text": speech
               }
             ]
           } 
         };
    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r
#************************************************************************************#
#                                                                                    #
#   Contact Information                                                              #
#                                                                                    #
#************************************************************************************#
def contact(resolvedQuery):
    print ("Within Contact Me method")
    speech = "Marvin.ai is now present from Denmark to help businesses all over the world. \nRequest for a free Demo now."
    res = {
        "speech": speech,
        "displayText": speech,
        "data" : {
        "facebook" : [
                {
                 "text": speech
                },
                {
                 "attachment" : {
                   "type" : "template",
                     "payload" : {
                      "template_type" : "generic",
                       "elements" : [ 
                                 {
                                   "title" : "Swapratim Roy",
                                   "image_url" : "https://marvinchatbot.files.wordpress.com/2017/06/swapratim-roy-founder-owner-of-marvin-ai.jpg?w=700&h=&crop=1",
                                   "subtitle" : "An innovative entrepreneur, founder at Marvin.ai \nAarhus, Denmark \nCall: +45-7182-5584",
                                   "buttons": [{
                                        "type": "web_url",
                                        "url": "https://www.messenger.com/t/swapratim.roy",
                                        "title": "Connect on Messenger"
                                    },
                                    {
                                        "type": "web_url",
                                        "url": "https://marvinai.live",
                                        "title": "View Website"
                                    }]
                                 }
                           ]
                       } 
                   }
                },
                {
                    "sender_action": "typing_on"
                },
                {
                  "text": "Start over again",
                  "quick_replies": [
                 {
                  "content_type": "text",
                  "title": "News",
                  "payload": "News",
                  "image_url": "http://www.freeiconspng.com/uploads/newspaper-icon-20.jpg"
                 },
                 {
                  "content_type": "text",
                  "title": "Weather",
                  "payload": "Weather",
                  "image_url": "https://www.mikeafford.com/store/store-images/ww01_example_light_rain_showers.png"
                   },
                  {
                  "content_type": "text",
                  "title": "Wikipedia",
                  "payload": "Wikipedia",
                  "image_url": "https://upload.wikimedia.org/wikipedia/en/thumb/8/80/Wikipedia-logo-v2.svg/1122px-Wikipedia-logo-v2.svg.png"
                   },
                  {
                  "content_type": "text",
                  "title": "YouTube",
                  "payload": "YouTube",
                  "image_url": "https://cdn1.iconfinder.com/data/icons/logotypes/32/youtube-512.png"
                   },
                  {
                  "content_type": "text",
                  "title": "Contact Me",
                  "payload": "contact",
                  "image_url": "https://cdn3.iconfinder.com/data/icons/communication-mass-media-news/512/phone_marketing-128.png"
                  }
                  ]
                 }
             ]
           } 
         };
    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def requestDemo(resolvedQuery):
    print ("Within requestDemo method")
    speech = "Marvin.ai is now present from Denmark to help businesses all over the world. \nRequest for a free Demo now."
    res = {
        "speech": speech,
        "displayText": speech,
        "data" : {
        "facebook" : [
               {
                    "sender_action": "typing_on"
               },
               {
                    "text": "Thank you " + user_name + " for requesting a Demo. Please say Hi to Swapratim on Messenger to get him notified. :-)"
               },
                {
                 "attachment" : {
                   "type" : "template",
                     "payload" : {
                      "template_type" : "generic",
                       "elements" : [ 
                                 {
                                   "title" : "Swapratim Roy",
                                   "image_url" : "https://marvinchatbot.files.wordpress.com/2017/06/swapratim-roy-founder-owner-of-marvin-ai.jpg?w=700&h=&crop=1",
                                   "subtitle" : "An innovative entrepreneur, founder at Marvin.ai \nAarhus, Denmark \nCall: +45-7182-5584",
                                   "buttons": [{
                                        "type": "web_url",
                                        "url": "https://www.messenger.com/t/swapratim.roy",
                                        "title": "Connect on Messenger"
                                    },
                                    {
                                        "type": "web_url",
                                        "url": "https://marvinai.live",
                                        "title": "View Website"
                                    }]
                                 }
                           ]
                       } 
                   }
                }
            ]
           } 
         };
    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print("Starting APPLICATION on port %d" % port)
    context.run(debug=True, port=port, host='0.0.0.0')