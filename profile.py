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
import cProfile

nationality = "indian"
destinationcountry = "denmark"
def wikipedia_search(nationality, destinationcountry):
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
    if "Srilanka" in destinationcountry:
        destinationcountry = "Sri Lanka"
    elif "Uae" in destinationcountry:
        destinationcountry = "United Arab Emirates"
    elif "Usa" in destinationcountry or "Us" in destinationcountry or "America" in destinationcountry and "Russia" not in destinationcountry and "Mauritius" not in destinationcountry and "Cyprus" not in destinationcountry and "Australia" not in destinationcountry and "Austria" not in destinationcountry and "Belarus" not in destinationcountry:
        destinationcountry = "United States"
    elif "Uk" in destinationcountry or "England" in  destinationcountry: #and "Ukraine" not in destinationcountry:
        if "Ukraine" not in destinationcountry:
            destinationcountry =  "United Kingdom"
        else:
            destinationcountry =  "Ukraine"
            
    
    # Loading Nationality List into Array to validate against the destination country input
    file_path = '/app/country_name_JSON.txt'
    with open(file_path) as f:
       data = json.loads(f.read())
       # print("First Element from Nationality_List -->" + data[0]['nationality'])

    # Loading the COUNTRY list to validate DESTINATION COUNTRY input:
    for data_item in data:
        str_destinationcountry = str(data_item['country_name'])
        if str_destinationcountry == destinationcountry:
           correct_str_destinationcountry = destinationcountry
           print ("This is the CORRECT destinationcountry--->" + correct_str_destinationcountry)
           break
        
    # if not correct_str_destinationcountry:
        # print ("Destinationcountry is wrong!!!")
        # speech = "It seems the destination country name is not exactly correct. Please try once more."
    
    print ("wikipedia_search Method nationality --> " + nationality)
    
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
           "contextOut": [
                     {
                         "name": "wikipediasearch",
                         "lifespan": 1,
                         "parameters": {
                            "param": "$countryname"
                          }
                     }
           ],
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

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print("Starting APPLICATION on port %d" % port)
    context.run(debug=True, port=port, host='0.0.0.0')
    pr = cProfile.Profile()
    pr.enable()
    wikipedia_search(indian, denmark)
    pr.disable()
    pr.print_stats()