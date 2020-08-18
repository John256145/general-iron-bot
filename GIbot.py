import tweepy
import random
import time

CONSUMER_KEY = 'Woah there!'
CONSUMER_SECRET = 'These keys are private!'
ACCESS_KEY = 'But thank you for having an interest in looking into my code.'
ACCESS_SECRET = 'Have a great day :)'

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

#These are the random phrases that my bot will use to reply
phrases = ["Thank you for bringing up this important topic. Could you also look into denying the permits for the relocation of General Iron to the East Side? They pose a danger to our community.",
            "This is definitely worth talking about. Another thing worth talking about is the health risks associated with General Iron moving to the Southeast side. May you help us out?",
            "I respect your decisions Mrs. Lightfoot, but the East Side neighborhood has felt neglected recently because you haven't stopped a hazardous factory from moving into our community. If the North Side can get rid of them, why can't we?",
            "Thank you for all the help you have given to Chicago. All residents of the East Side would be grateful for your help in stopping General Iron's relocation to our area, as they are known for several violations. Thank you for showing us you care ❤️",
            "I agree, this is absolutely an important matter. However, I would also like to bring up the fact that General Iron is posing a health risk to the forgotten community of the East Side. We need your help in stopping them from poisoning our area."
            ]

#If a tweet mentions COVID-19, a random phrase from this list will be chosen instead.
covidPhrases = ["Thank you for your swift actions against COVID-19. Your fellow residents on the Southeast side will also face another health risk if you allow General Iron to move into our community, and we are worried.",
                "COVID-19 is absolutely a threat to our wellbeing. In addition to the pandemic, Southeast side residents will suffer further health risks if General Iron moves into our neighborhood. Please, step in and stop their relocation.",
                "Your dedication to slowing down coronavirus cases in Chicago is remarkable. Could you also share this dedication with your residents in the East Side by stopping General Iron from moving into our neighborhood? We're already plagued with other industries polluting the area."
                ]

#If my bot finds a tweet that mentions General Iron, this reply will be given
GIphrase = "Thank you for talking about General Iron!"

#Storing the most recently seen tweet ID prevents the bot from replying to the same tweet multiple times
FILE_NAME = 'lastSeenID.txt'

def getLastSeenID(filename):
    file = open(filename, 'r')
    ID = int(file.read().strip())
    file.close()
    return ID

def setLastSeenID(ID, filename):
    file = open(filename, 'w')
    file.write(str(ID))
    file.close()
    return

def reply():
    while True:
        lightfootRecentTweet = api.user_timeline("chicagosmayor", count = 1)[0] #obtain the latest tweet
        if getLastSeenID(FILE_NAME) != lightfootRecentTweet.id: #have i seen this tweet already?
            setLastSeenID(lightfootRecentTweet.id, FILE_NAME) #store the tweet id
            #i have not replied to the latest tweet
            if not "retweeted_status" in dir(lightfootRecentTweet): #if it is not a retweet
                if not lightfootRecentTweet.in_reply_to_user_id: #if tweet is not a reply
                    #valid tweet to reply to
                    tweetText = lightfootRecentTweet.text.lower()
                    if "general iron" in tweetText:
                        reply = GIphrase
                    elif "covid" in tweetText or "coronavirus" in tweetText:
                        #reply random covid phrase
                        reply = random.choice(covidPhrases)
                    else:
                        #reply random phrase
                        reply = random.choice(phrases)
                    print("Replying to {}".format(lightfootRecentTweet.text))
                    api.update_status('@' + lightfootRecentTweet.user.screen_name + " " + reply,lightfootRecentTweet.id) #send the tweet!
                else:
                    print("latest tweet is a reply!")
            else:
                print("lateset tweet is a retweet!")
        else:
                print("no new tweet...")

        #this code will repeat in 15 seconds
        time.sleep(15)
