#!/usr/bin/env python

from __future__ import print_function
from future import standard_library
standard_library.install_aliases()
import urllib.request, urllib.parse, urllib.error
import json
import os
import sys
import urlparse
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
# Webhook requests are coming to this method
@context.route('/webhook', methods=['POST'])
def webhook():
    reqContext = request.get_json(silent=True, force=True)
    #print(json.dumps(reqContext, indent=4))
    print(reqContext.get("result").get("action"))
    print ("webhook is been hit ONCE ONLY")
    if reqContext.get("result").get("action") == "input.welcome":
       return welcome()
    elif reqContext.get("result").get("action") == "input.asktheuser":
       return asktheuser(reqContext)
    elif reqContext.get("result").get("action") == "input.nationality":
       return userNationality(reqContext)
    elif reqContext.get("result").get("action") == "input.destinationcountry":
       return userDestinationCountry(reqContext)
    else:
       print("Good Bye")

 
#************************************************************************************#
#                                                                                    #
#   This method is to get the Facebook User Deatails via graph.facebook.com/v2.6     #
#                                                                                    #
#************************************************************************************#
user_name = None
def welcome():
    global user_name
    #print ("within welcome method")
    data = request.json
    print (data)
    if data is None:
        return {}
    entry = data.get('originalRequest')
    dataall = entry.get('data')
    sender = dataall.get('sender')
    id = sender.get('id')
    print ("id :" + id)
    fb_info = "https://graph.facebook.com/v2.6/" + id + "?fields=first_name,last_name,profile_pic,locale,timezone,gender&access_token=" + ACCESS_TOKEN
    print (fb_info)
    result = urllib.request.urlopen(fb_info).read()
    print (result)
    data = json.loads(result)
    first_name = data.get('first_name')
    print (first_name)
    user_name = data.get('first_name')
    speech1 = "I'm Visa CheckBot - your one stop solution for visa related enquiry"
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
                  "text": "So, shall we start looking for your visa enquiry?",
                  "quick_replies": [
                 {
                  "content_type": "text",
                  "title": "Yeah Sure",
                  "payload": "Yeah Sure",
                  "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQZLSAsTl9tNQAG72yb9P4YV4EMjsFYxZ6eJbD6JS1_wnfthxJP"
                 },
                 {
                  "content_type": "text",
                  "title": "No Thanks",
                  "payload": "No Thanks",
                  "image_url": "https://3.bp.blogspot.com/-2Q4mCe03fEg/VuOR92Jk6bI/AAAAAAAAMAw/YCY_ej--zEoSybT_PseTp6p0-G7Y-kGfw/s1600/Smiley-Red-rating.jpg"
                   }
                  ]
                 }
                ]
              }
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
                  "title": "Yes",
                  "payload": "Yes",
                 },
                 {
                  "content_type": "text",
                  "title": "No",
                  "payload": "No",
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

#************************************************************************************#
#                                                                                    #
#   Asking the USER the FIRST QUESTION - What's Your Nationality?                    #
#                                                                                    #
#************************************************************************************#
def userNationality(reqContext):
    print (reqContext.get("result").get("action"))
    option = reqContext.get("result").get("action")
    res = {
        "speech": "First Question",
        "displayText": "First Question",
        "data" : {
        "facebook" : [
              {
                 "text": "1. What is your nationality?"
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
#   Asking the USER the SECOND QUESTION - What's Your Destination Country?           #
#                                                                                    #
#************************************************************************************#
def userDestinationCountry(reqContext):
    print (reqContext.get("result").get("action"))
    option = reqContext.get("result").get("action")
    res = {
        "speech": "Second Question",
        "displayText": "Second Question",
        "data" : {
        "facebook" : [
              {
                 "text": "2. Which country do you want to travel?"
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
#   Below method is to get the Facebook Quick Reply Webhook Handling - Wikipedia     #
#                                                                                    #
#************************************************************************************#
def wikipedia_search(reqContext):
    #print (reqContext.get("result").get("action"))
    option = reqContext.get("result").get("action")
    res = {
        "speech": "Please provide the topic you want to search in Wikipedia",
        "displayText": "Please provide the topic you want to search in Wikipedia",
        "data" : {
        "facebook" : [
               {
                "text": "Please write the topic you want to search in Wikipedia"
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
#   This method is to get the Wikipedia Information via Google API                   #
#                                                                                    #
#************************************************************************************#
# Searchhook is for searching for Wkipedia information via Google API
def searchhook(reqContext):
    req = request.get_json(silent=True, force=True)
    print("Within Search function......!!")
    resolvedQuery = reqContext.get("result").get("resolvedQuery")
    print ("resolvedQuery: " + resolvedQuery)
    true_false = True
    baseurl = "https://www.googleapis.com/customsearch/v1?"
###########################################################
    result = req.get("result")
    parameters = result.get("parameters")
    search_list0 = parameters.get("any")
    #print ("search_list0" + search_list0)
    search_u_string_removed = [str(i) for i in search_list0]
    search_list1 = str(search_u_string_removed)
    #print ("search_list1" + search_list1)
    cumulative_string = search_list1.strip('[]')
    search_string = cumulative_string.replace(" ", "%20")
    print(search_string)
    search_string_ascii = search_string.encode('ascii')
    if search_string_ascii is None:
        return None
    google_query = "key=AIzaSyDNYsLn4JGIR4UaZMFTAgDB9gKN3rty2aM&cx=003066316917117435589%3Avcms6hy5lxs&q=" + search_string_ascii + "&num=1"
###########################################################
    if google_query is None:
        return {}
    #google_url = baseurl + urllib.parse.urlencode({google_query})
    google_url = baseurl + google_query
    print("google_url::::"+google_url)
    result = urllib.request.urlopen(google_url).read()
    #print (result)
    data = json.loads(result)
    print ("data = json.loads(result)")
############################################################
    speech = data['items'][0]['snippet'].encode('utf-8').strip()
    for data_item in data['items']:
        link = data_item['link'],

    for data_item in data['items']:
        pagemap = data_item['pagemap'],

    cse_thumbnail_u_string_removed = [str(i) for i in pagemap]
    cse_thumbnail_u_removed = str(cse_thumbnail_u_string_removed)
    cse_thumbnail_brace_removed_1 = cse_thumbnail_u_removed.strip('[')
    cse_thumbnail_brace_removed_2 = cse_thumbnail_brace_removed_1.strip(']')
    cse_thumbnail_brace_removed_final =  cse_thumbnail_brace_removed_2.strip("'")
    #print (cse_thumbnail_brace_removed_final)
    keys = ('cse_thumbnail', 'metatags', 'cse_image')
    for key in keys:
        # print(key in cse_thumbnail_brace_removed_final)
        #print ('cse_thumbnail' in cse_thumbnail_brace_removed_final)
        true_false = 'cse_thumbnail' in cse_thumbnail_brace_removed_final
        if true_false == True:
            #print ('Condition matched -- Within IF block')
            for key in pagemap:
                cse_thumbnail = key['cse_thumbnail']
                #print ('Within the For loop -- cse_thumbnail is been assigned')
                for image_data in cse_thumbnail:
                    raw_str = image_data['src']
                    
                    break
        else:
            raw_str = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTwdc3ra_4N2X5G06Rr5-L0QY8Gi6SuhUb3DiSN_M-C_nalZnVA"
            #print ('***FALSE***') 
    
    
    src_brace_removed_final = raw_str
    # Remove junk charaters from URL
    link_u_removal =  [str(i) for i in link]
    link_u_removed = str(link_u_removal)
    link_brace_removed_1 = link_u_removed.strip('[')
    link_brace_removed_2 = link_brace_removed_1.strip(']')
    link_final =  link_brace_removed_2.strip("'")
    # Remove junk character from search item
    search_string_final = cumulative_string.strip("'")
    
############################################################
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
                                   "title" : search_string_final,
                                   "image_url" : src_brace_removed_final,
                                   "subtitle" : "",
                                   "buttons": [{
                                        "type": "web_url",
                                        "url": link_final,
                                        "title": "More info"
                                    }]
                                 } 
                           ]
                       } 
                   }
                },
                 {
                 "text": speech
                  },
                 {
                  "text": "Click on the below options to start over again",
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
                  "payload": "weather",
                  "image_url": "https://www.mikeafford.com/store/store-images/ww01_example_light_rain_showers.png"
                   },
                  {
                  "content_type": "text",
                  "title": "Wikipedia",
                  "payload": "wikipedia",
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

#************************************************************************************#
#                                                                                    #
#   This method is to get the Wikipedia Information via Google API via Funnel        #
#                                                                                    #
#************************************************************************************#
# Searchhook is for searching for Wkipedia information via Google API
def wikipediaInformationSearch(reqContext):
    #req = request.get_json(silent=True, force=True)
    resolvedQuery = reqContext.get("result").get("resolvedQuery")
    #print ("resolvedQuery: " + resolvedQuery)
    true_false = True
    baseurl = "https://www.googleapis.com/customsearch/v1?"
    resolvedQueryFinal = resolvedQuery.replace(" ", "%20")
    search_string_ascii = resolvedQueryFinal.encode('ascii')
    if search_string_ascii is None:
        return None
    google_query = "key=AIzaSyDNYsLn4JGIR4UaZMFTAgDB9gKN3rty2aM&cx=003066316917117435589%3Avcms6hy5lxs&q=" + search_string_ascii + "&num=1"
###########################################################
    if google_query is None:
        return {}
    google_url = baseurl + google_query
    #print("google_url::::"+google_url)
    result = urllib.request.urlopen(google_url).read()
    data = json.loads(result)
    #print (data)
############################################################
    speech = data['items'][0]['snippet'].encode('utf-8').strip()
    for data_item in data['items']:
        link = data_item['link'],

    for data_item in data['items']:
        pagemap = data_item['pagemap'],

    cse_thumbnail_u_string_removed = [str(i) for i in pagemap]
    cse_thumbnail_u_removed = str(cse_thumbnail_u_string_removed)
    cse_thumbnail_brace_removed_1 = cse_thumbnail_u_removed.strip('[')
    cse_thumbnail_brace_removed_2 = cse_thumbnail_brace_removed_1.strip(']')
    cse_thumbnail_brace_removed_final =  cse_thumbnail_brace_removed_2.strip("'")
    keys = ('cse_thumbnail', 'metatags', 'cse_image')
    for key in keys:
        true_false = 'cse_thumbnail' in cse_thumbnail_brace_removed_final
        if true_false == True:
            for key in pagemap:
                cse_thumbnail = key['cse_thumbnail']
                for image_data in cse_thumbnail:
                    raw_str = image_data['src']
                    break
        else:
            raw_str = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTwdc3ra_4N2X5G06Rr5-L0QY8Gi6SuhUb3DiSN_M-C_nalZnVA"
           
    src_brace_removed_final = raw_str
    # Remove junk charaters from URL
    link_u_removal =  [str(i) for i in link]
    link_u_removed = str(link_u_removal)
    link_brace_removed_1 = link_u_removed.strip('[')
    link_brace_removed_2 = link_brace_removed_1.strip(']')
    link_final =  link_brace_removed_2.strip("'")
    # Remove junk character from search item
    search_string_final = resolvedQuery.strip("'")
    #print ("Image::::::::")
    #print (src_brace_removed_final)
    #print ("link_final....")
    #print (link_final)
    #print("Response:")
    #print(speech)
############################################################
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
                                   "title" : search_string_final,
                                   "image_url" : src_brace_removed_final,
                                   "subtitle" : "",
                                   "buttons": [{
                                        "type": "web_url",
                                        "url": link_final,
                                        "title": "More info"
                                    }]
                                 } 
                           ]
                       } 
                   }
                },
                 {
                 "text": speech
                  },
                 {
                  "text": "Click on the below options to start over again",
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