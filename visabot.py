#!/usr/bin/env python

from __future__ import print_function
from future import standard_library
#from lxml import html
import requests
standard_library.install_aliases()
import urllib.request, urllib.parse, urllib.error
import json
import os
import sys
#import urlparse
from urllib.parse import urljoin
import emoji
import pprint

from flask import Flask
from flask import request, render_template
from flask import make_response
import gspread
from oauth2client.service_account import ServiceAccountCredentials


# Flask should start in global layout
context = Flask(__name__)
# Facbook Access Token
ACCESS_TOKEN = "EAADSsDjm6gIBALq0KNMZBdmwRKe2G2w4sLN1o27c22Hl4hhN2zmyRZCnSONlqA8ZAgB3toVrNtjSheJ7lzdZCTFXy4i3RPs5wAbOKNkDtGWLHofDQfZBvy2gbrNsdbaY8Ud2wjILm5X5bAU4ievEDmZA6yyKK6TFnSdMeHNZBmOZCAZDZD"
# Google Sheet Credentials
#CLIENT_ID = "107898040430223609451"
#LIENT_SECRET = '<Client secret from Google API Console>'
#************************************************************************************#
#                                                                                    #
#    All Webhook requests lands within the method --webhook                          #
#                                                                                    #
#************************************************************************************#
reqContext = None
# Webhook requests are coming to this method
@context.route('/webhook', methods=['POST'])
def webhook():
    #global reqContext
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
    elif reqContext.get("result").get("action") == "nothanks":
       return noThanks()
    elif reqContext.get("result").get("action") == "listen.help":
       return help()
    elif reqContext.get("result").get("action") == "morebots":
       return moreBots()
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
       #fb_info = "https://graph.facebook.com/v2.6/" + id + "?fields=first_name,last_name,profile_pic,locale,timezone,gender&access_token=" + ACCESS_TOKEN
       fb_info = "https://graph.facebook.com/v2.6/" + id + "?fields=first_name,last_name&access_token=" + ACCESS_TOKEN
       print (fb_info)
       result = urllib.request.urlopen(fb_info).read()
       print (result)
       data = json.loads(result)
       first_name = data.get('first_name')
       print ("FACEBOOK: First Name -->" + first_name)

       #####################################################################
       # Opening Google Drive Excel to read and write userbase             #
       # https://www.youtube.com/watch?v=vISRn5qFrkM                       #
       #####################################################################

       scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
       creds = ServiceAccountCredentials.from_json_keyfile_name("client_secret.json", scope)
       client = gspread.authorize(creds)
       
       sheet = client.open("Visa CheckBot Global User Database").worksheet("user_table")
       user_table = sheet.get_all_records()
       pp = pprint.PrettyPrinter()
       #print (sheet.row_count)
       pp.pprint (user_table)

       # INSERT USER DETAILS FROM FACEBOOK API
       row = [str(data.get('first_name')), str(data.get('last_name')), str(data.get('gender')), str(data.get('id'))]
       print (row)
       
       # STOP DUPLICACY OF USER DATA
       if str(data.get('id')) in sheet.col_values(4):
          print ("Nothing to print")
       elif str(data.get('id')) not in sheet.col_values(4):
          sheet.insert_row(row)
       
    elif platform == "telegram":
       first_name = data.get('originalRequest').get('data').get('message').get('chat').get('first_name')
       print ("TELEGRAM: First Name -->" + first_name)
    elif platform == "skype":
       first_name = "to Visa CheckBot"
       print ("SKYPE: Within Python")
    elif platform == "slack":
       first_name = "to Visa CheckBot"
       print ("SKYPE: Within Python")
    elif platform == "kik":
       first_name = data.get('originalRequest').get('data').get('from')
       print ("KiK: Within Python")
       
    speech1 = "This is your one stop solution for visa related enquiry. "
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
                                   "image_url" : "http://gdurl.com/eDd3J",
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
                 "parse_mode": "markdown",
                 "text": "[​​​​​​​​​​​](http://gdurl.com/eDd3J) Welcome " + first_name + "! " + speech1 + "So let's start, shall we?",
                 "reply_markup": { 
                   "inline_keyboard": [ 
                        [{ "callback_data": "Yeah Sure", "text": "Yeah Sure" }], 
                        [{ "callback_data": "No Thanks", "text": "No Thanks" }] 
                       ] 
                   }
                },
           "slack": {
                 "text": speech1,
                 "attachments": [
                   {
                    "fallback": "You are unable to proceed",
                    "callback_id": "intro_block",
                    "color": "#3AA3E3",
                    "image_url": "http://gdurl.com/eDd3J",
                    "text": "So, let's start. Shall we?",
                    "attachment_type": "default",
                    "actions": [
                         {
                            "name": "Yeah Sure",
                            "text": "Yeah Sure",
                            "type": "button",
                            "value": "Yeah Sure"
                         },
                         {
                            "name": "No Thanks",
                            "text": "No Thanks",
                            "type": "button",
                            "value": "No Thanks"
                         }
                     ]
                  }
                ]
              },
           "kik": {
                 "type": "text",
                 "body": "Welcome " + first_name + "! " + speech1 + "So let's start, shall we?",
                 "keyboards": [
                        {
                    "type": "suggested",
                    "responses": [
                        {
                            "type": "text",
                            "body": "Yeah Sure"
                        },
                        {
                            "type": "text",
                            "body": "No Thanks"
                        }
                      ]
                    }
                 ]
              }
          },
        "messages": [
        {
          "type": 4,
          "platform": "skype",
          "payload": {
            "skype": {
              "type": "message",
              "text": "Hi",
              "attachments": [
                {
                  "contentType": "application/vnd.microsoft.card.hero",
                  "content": {
                    "title": "Welcome to Visa CheckBot",
                    "subtitle": "Your one stop solution for Visa check",
                    "images": [
                      {
                        "url": "http://gdurl.com/eDd3J"
                      }
                    ],
                   "buttons": [{
                            "type":"postBack",
                            "title": "Yeah Sure",
                            "value": "Yeah Sure"
                    },
                    {
                            "type":"postBack",
                            "title": "No Thanks",
                            "value": "No Thanks"
                    }]
                  }
                }
              ]
            }
          }
        }
       ],
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
    otherplatformstatement = "Great! I'll ask two questions only. Then only I can precisely tell whether you need a VISA or NOT to travel your destination country."
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
                  },
                 {
                  "content_type": "text",
                  "title": "Help",
                  "payload": "Help",
                  }
                  ]
                 }
             ],
        "telegram": {
                 "text": otherplatformstatement,
                 "reply_markup": { 
                   "inline_keyboard": [ 
                        [{ "callback_data": "I'm Ready", "text": "I'm Ready" }], 
                        [{ "callback_data": "No Thanks", "text": "No Thanks" }],
                        [{ "callback_data": "Help", "text": "Help" }]
                       ] 
                },
              },
        "slack": {
                 "text": otherplatformstatement,
                 "attachments": [
                   {
                    "fallback": "You are unable to proceed",
                    "callback_id": "intro_block",
                    "color": "#3AA3E3",
                    "attachment_type": "default",
                    "actions": [
                         {
                            "name": "I'm Ready",
                            "text": "I'm Ready",
                            "type": "button",
                            "value": "I'm Ready"
                         },
                         {
                            "name": "No Thanks",
                            "text": "No Thanks",
                            "type": "button",
                            "value": "No Thanks"
                         },
                         {
                            "name": "Help",
                            "text": "Help",
                            "type": "button",
                            "value": "Help"
                         }
                     ]
                  }
                ]
              },
         "kik": {
                 "type": "text",
                 "body": otherplatformstatement,
                 "keyboards": [
                        {
                    "type": "suggested",
                    "responses": [
                        {
                            "type": "text",
                            "body": "I'm Ready"
                        },
                        {
                            "type": "text",
                            "body": "No Thanks"
                        },
                        {
                            "type": "text",
                            "body": "Help"
                        }
                      ]
                    }
                 ]
              }
           }, 
        "messages": [
        {
          "type": 4,
          "platform": "skype",
          "payload": {
            "skype": {
              "text": "Great! I'll ask two questions only. Then only I can precisely tell whether you need a VISA or NOT to travel your destination country.",
              "attachments": [
                {
                  "contentType": "application/vnd.microsoft.card.hero",
                  "content": {
                    "buttons": [{
                            "type":"postBack",
                            "title": "I'm Ready",
                            "value": "I'm Ready"
                    },
                    {
                            "type":"postBack",
                            "title": "No Thanks",
                            "value": "No Thanks"
                    },
                    {
                            "type":"postBack",
                            "title": "Help",
                            "value": "Help"
                    }]
                  }
                }
              ]
            }
          }
        }
       ]
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
    whatisyournationality = "What is your nationality?"
    print (reqContext.get("result").get("action"))
    res = {
        "speech": whatisyournationality,
        "displayText": whatisyournationality,
        "data" : {
        "facebook" : [
              {
                 "text": whatisyournationality
              }
             ],
        "telegram": {
                 "text": whatisyournationality
             },
        "slack": {
                 "text": whatisyournationality
             },
        "kik": {
                 "type": "text",
                 "body": whatisyournationality
             }
           },
        "messages": [
        {
          "type": 4,
          "platform": "skype",
          "payload": {
            "skype": {
              "text": whatisyournationality
            }
          }
        }
       ]   
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
    whatisyournationality = "What is your nationality?"
    res = {
        "speech": whatisyournationality,
        "displayText": whatisyournationality,
        "data" : {
        "facebook" : [
              {
                 "text": whatisyournationality
              }
             ],
        "telegram": {
                 "text": whatisyournationality
             },
        "slack": {
                 "text": whatisyournationality
             },
        "kik": {
                 "type": "text",
                 "body": whatisyournationality
             }
           },
        "messages": [
        {
          "type": 4,
          "platform": "skype",
          "payload": {
            "skype": {
              "text": whatisyournationality
            }
          }
        }
       ]   
      };
    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

###   Start Over        ###
def startOver():
    print ("*********startOver*************")
    global nationality
    global destinationcountry
    nationality = ""
    destinationcountry = ""
    whatisyournationality = "What is your nationality?"
    res = {
        "speech": whatisyournationality,
        "displayText": whatisyournationality,
        "data" : {
        "facebook" : [
              {
                 "text": whatisyournationality
              }
             ],
        "telegram": {
                 "text": whatisyournationality
             },
        "slack": {
                 "text": whatisyournationality
             },
        "kik": {
                 "type": "text",
                 "body": whatisyournationality
             }
           },
        "messages": [
        {
          "type": 4,
          "platform": "skype",
          "payload": {
            "skype": {
              "text": whatisyournationality
            }
          }
        }
       ]   
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
       #print("First Element from Nationality_List -->" + data[0]['nationality'])

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
             },
        "slack": {
                 "text": speech
             },
        "kik": {
                 "type": "text",
                 "body": speech
             }
           },
        "messages": [
        {
          "type": 4,
          "platform": "skype",
          "payload": {
            "skype": {
              "text": speech
            }
          }
        }
       ]    
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
    visa_status = ""
    resolvedQuery_wiki = reqContext.get("result").get("resolvedQuery")
    global nationalityNEW
    #To capitalize the first letter
    global destinationcountry
    destinationcountry = ""
    destinationcountry = str(resolvedQuery_wiki).title() 
    
    if destinationcountry == nationality:
        destinationcountry = ""
        print ("destinationcountry: " + destinationcountry)
    else:
        print ("destinationcountry: " + destinationcountry) 

    
    # Check if the country name is abbreviated, put the correct names:
    if "Uae" in destinationcountry:
        destinationcountry = "United Arab Emirates"
    elif "Usa" in destinationcountry or "Us" in destinationcountry and "Russia" not in destinationcountry and "Mauritius" not in destinationcountry and "Cyprus" not in destinationcountry and "Australia" not in destinationcountry and "Austria" not in destinationcountry and "Belarus" not in destinationcountry:
        destinationcountry = "United States"
    elif "Uk" in destinationcountry or "England" in  destinationcountry: #and "Ukraine" not in destinationcountry:
        if "Ukraine" not in destinationcountry:
            destinationcountry =  "United Kingdom"
        else:
            destinationcountry =  "Ukraine"
            
    
    # Loading Nationality List into Array to validate against the user nationality input
    file_path = '/app/country_name_JSON.txt'
    with open(file_path) as f:
       data = json.loads(f.read())
       # print("First Element from Nationality_List -->" + data[0]['nationality'])

    # Loading the Nationality list to validate nationality input:
    for data_item in data:
        str_destinationcountry = str(data_item['country_name'])
        if str_destinationcountry == destinationcountry:
           correct_str_destinationcountry = destinationcountry
           print ("This is the CORRECT destinationcountry--->" + destinationcountry)
           break
        

    print ("wikipedia_search Method nationality --> " + nationality)
    # Check if the nationality is abbreviated, put the correct names:
    if "Uae" in destinationcountry:
        destinationcountry = "United Arab Emirates"

    nationalityNEW = nationality
    if " " in nationality:
        nationalityNEW = nationality.replace(" ", "%20")
        print ("Nationality with SPACE--------->" + nationalityNEW)
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
    if google_query:
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
           print ("Exception handling for Peru, Belgium and Costa Rica-->" + info)
           #Peru|state<!--Use state flag-->}}\n| {{yes|Visa not required}}<ref>{{Timatic|nationality=CA|destination=PE|accessdate=26 November 2013}}</ref>\n| 183 days\n|\n|- \n| 
           #print ("Visa Status-->" + info.split("<ref>")[0].split("{{")[1].split("}}")[0].split("|")[1])
           infotoStringFinal = info.split("<ref>")[0].split("{{")[1].split("}}")[0].split("|")[1]
           visa_status = infotoStringFinal 
           print ("Country name: -->" + infotoStringFinal)
        else:
           continue
    print ("NECESSARY STRING -->")
    # Check all artifacts which are to be removed to get the VISA INFORMATION
    print (infotoStringFinal)
    #print ("Section splitlines -->" + infotoStringFinal.splitlines()

    if "Visa" in infotoStringFinal or "movement" in infotoStringFinal and visa_status != infotoStringFinal:
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
    elif visa_status == infotoStringFinal:
        visa_status = infotoStringFinal 
        print ("No change in VISA Status -->" + visa_status)
        # 4th CATEGORY like, Australia}}\n| {{yes|[[eVisitor]]}}<ref>{{Timatic|nationality=DK|destination=AU}}
        if "]]" in infotoStringFinal:
            print ("Check 4th Category-->" + infotoStringFinal.split("]]")[0].split("[[")[1])
            visa_status = infotoStringFinal.split("]]")[0].split("[[")[1]

    #########################################################################

    subtitle = visa_status + " for " + nationality + " citizen to travel in " + destinationcountry

    #########################################################################
    if visa_status == "Visa required":
        image_url_final = str("https://gdurl.com/tPqr")  # https://goo.gl/D4H5ZZ
    elif visa_status == "Visa not required" or visa_status == "Freedom of movement":
        image_url_final = str("https://gdurl.com/YMBa")  # https://goo.gl/NM7yGE
    elif visa_status == "e-Visa required" or visa_status == "eVisa" or visa_status == "Visa on arrival" or visa_status == "eVisa / Visa on arrival":
        image_url_final = str("https://gdurl.com/JyLG")   # https://goo.gl/hh1ypL
    elif visa_status == "0":
        image_url_final = "https://gdurl.com/Xn4F"
        visa_status = "Hmm, No VISA details found"
        subtitle = "Please check the spelling or see if it's a valid country name"
    elif infotoStringFinal == "0":
        image_url_final = "https://gdurl.com/Xn4F"
        visa_status = "Hmm, No VISA details found"
        subtitle = "Please check the spelling or see if it's a valid country name"
    else:
        image_url_final = str("https://gdurl.com/JyLG")

    print ("image_url_final---->" + image_url_final)
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
                 "parse_mode": "markdown",
                 "text": "[​​​​​​​​​​​](" + image_url_final + ") Visa Status: " + subtitle + ". Write another country name to continue checking VISA requirement",
                 "reply_markup": { 
                   "inline_keyboard": [ 
                        [{ "url": "https://en.wikipedia.org/wiki/Visa_requirements_for_" + nationality + "_citizens", "text": "More Info" }],
                        [{ "callback_data": "startover", "text": "Restart" }], 
                        [{ "callback_data": "morebots", "text": "More Bots" }],
                        [{ "callback_data": "Help", "text": "Help" }]
                   ] 
                },
             },
           "slack": {
                 "text": "Visa Status: " + subtitle + ". Write another country name to continue checking VISA requirement",
                 "attachments": [
                   {
                    "fallback": "You are unable to proceed",
                    "callback_id": "visa_block",
                    "color": "#3AA3E3",
                    "image_url": image_url_final,
                    "attachment_type": "default",
                    "actions": [
                         {
                            "name": "Restart",
                            "text": "Restart",
                            "type": "button",
                            "value": "Restart"
                         },
                         {
                            "name": "No",
                            "text": "No",
                            "type": "button",
                            "value": "No"
                         }
                     ]
                  }
                ]
              },
           "kik": {
                 "type": "text",
                 "body": "Visa Status: " + subtitle + ". Write another country name to continue checking VISA requirement",
                 "keyboards": [
                        {
                    "type": "suggested",
                    "responses": [
                        {
                            "type": "text",
                            "body": "Restart"
                        },
                        {
                            "type": "text",
                            "body": "No"
                        }
                      ]
                    }
                 ]
              }
           },
         "messages": [
        {
          "type": 4,
          "platform": "skype",
          "payload": {
            "skype": {
              "text": subtitle + ". Write another country name to continue checking VISA requirement",
              "attachments": [
                {
                  "contentType": "application/vnd.microsoft.card.hero",
                  "content": {
                    "title": subtitle,
                    "subtitle": "Write another country name to continue checking VISA requirement",
                    "images": [
                      {
                        "url": image_url_final
                      }
                    ],
                   "buttons": [{
                            "type":"postBack",
                            "title": "Restart",
                            "value": "Restart"
                    },
                    {
                            "type":"postBack",
                            "title": "No",
                            "value": "No"
                    },
                    {
                            "type":"postBack",
                            "title": "Help",
                            "value": "Help"
                    }]
                  }
                }
              ]
            }
          }
        }
       ]   
      };
    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


###   No Thanks        ###
def noThanks():
    print ("*********No Thanks*************")
    statement = "I'm sorry to hear that. But you can always say Hi to start again."
    res = {
        "speech": statement,
        "displayText": statement,
        "data" : {
        "facebook" : [
              {
                 "text": statement
              }
             ],
        "telegram": {
                 "text": statement
             },
        "slack": {
                 "text": statement
             },
        "kik": {
                 "type": "text",
                 "body": statement
             }
           },
        "messages": [
        {
          "type": 4,
          "platform": "skype",
          "payload": {
            "skype": {
              "text": statement
            }
          }
        }
       ]   
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
def help():
    speech = "Write Hi to start again."
    res = {
        "speech": speech,
        "displayText": speech,
        "data" : {
        "facebook" : [
               {
                "text": "Write Hi to start or you can choose option from menu."
               }
             ],
        "telegram": {
                 "text": speech
             },
        "slack": {
                 "text": speech
             },
        "kik": {
                 "type": "text",
                 "body": speech
             }
           },
        "messages": [
        {
          "type": 4,
          "platform": "skype",
          "payload": {
            "skype": {
              "text": speech
            }
          }
        }
       ] 
         };
    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r
#************************************************************************************#
#                                                                                    #
#   Displaying ALL CHATBOTS - For Sale                                               #
#                                                                                    #
#************************************************************************************#
def moreBots():
    print ("Within forsale method")
    speech = "This bot is been created by marvin.ai. \nDo you like it?"
    res = {
        "speech": speech,
        "displayText": speech,
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
                                   "title" : "You like VISA CheckBot?",
                                   "image_url" : "http://gdurl.com/qYXU",
                                   "subtitle" : "This is one stop solution for all your VISA requirements",
                                   "buttons": [{
                                        "type": "web_url",
                                        "url": "https://marvinai.live",
                                        "title": "View Website"
                                    },
                                    {
                                        "type": "web_url",
                                        "url": "https://www.facebook.com/visacheckbot/",
                                        "title": "Facebook Page"
                                    },
                                    {
                                        "type": "element_share"
                                   }]
                                 }
                           ]
                       } 
                   }
                }
           ],
        "telegram": {
                "parse_mode": "Markdown",
                "text": "[​​​​​​​​​​​](http://famousdestinations.in/wp-content/uploads/2016/03/howtogetthere.png) You like VISA CheckBot?",
                "reply_markup": { 
                   "inline_keyboard": [ 
                        [{ "callback_data": "https://marvinai.live", "text": "View Website" }], 
                        [{ "callback_data": "https://www.facebook.com/visacheckbot", "text": "Facebook Page" }] 
                       ] 
                   }
             }
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