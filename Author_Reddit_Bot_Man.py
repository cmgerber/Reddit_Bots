#!/Users/colingerber/anaconda/bin/python

import sys
sys.path.append('/Users/colingerber/Documents/Programming/Personal/Reddit_Bots')
sys.path.append('/Users/colingerber/Documents/Programming/Personal/Python_modules')
import praw
from pyUtil import easyPickle as pickle
import time
import Send_Email


def remove_old_posts(post_dict):
    '''if the submission is over a week old delete it'''
    for key, value in post_dict.items():
        if (time.time() - value[2])/(60*60) > 168:
            del post_dict[key]
    return post_dict


def get_posts(post_text, subreddit):
    #read submissions

    #list of new posts to email
    new_post_list = []

    for submission in subreddit.get_new():
        #if the submission is over a day old don't include it
        if (time.time() - submission.created_utc)/(60*60) > 24:
            continue
        if submission.short_link not in post_text:
            new_post_list.append(submission.short_link)
        post_text[(submission.short_link)] = [(submission.title + submission.selftext),
                                              submission.title, submission.created_utc]
    return post_text, new_post_list


def create_email_text(keyterms, post_text, new_post_list):
    email_text = ''
    for post in new_post_list:
        for term in keyterms:
            if term in post_text[post][0]:
                email_text += (post_text[post][1] + ' \n' + post + ' \n')
                break
    email_text = remove_ascii(email_text)
    return email_text


def remove_ascii(text):
    for letter in text:
        if ord(letter) > 128:
            text = text.replace(letter, '')
    return text


def main():
    '''This bot checks the printsf subreddit for mentions
    of a set of authors and then emails links to
    posts with the mentions in them'''

    #create user agent for reddit api
    user_agent = ("BookFinder Bot 0.1")

    r = praw.Reddit(user_agent = user_agent)

    #add a subreddit to look at
    subreddit1 = r.get_subreddit("printsf")
    subreddit2 = r.get_subreddit("scifi")
    subreddit3 = r.get_subreddit("books")

    #subreddit list
    sub_list = [subreddit1, subreddit2, subreddit3]

    #load previous post text
    post_text = pickle.open_object('/Users/colingerber/Documents/Programming/Personal/Reddit_Bots/post_text.pkl')

    #if the submission is over a week old delete it
    post_text = remove_old_posts(post_text)

    #create a variable to store all new posts
    tot_new_post_list = []
    #loop through subreddits
    for sub in sub_list:

        #update the post_text dict with new posts
        post_text, new_post_list = get_posts(post_text, sub)

        #add new posts to tot list
        tot_new_post_list += new_post_list

    #keyterms to look for
    keyterms = ['Bujold', 'Asimov', 'Hamilton', 'Gibson',
                'Reynolds', 'Stephenson', 'Scalzi', 'Simmons']

    #create email text
    email_text = create_email_text(keyterms, post_text, tot_new_post_list)

    #send the email
    if len(email_text) == 0:
        print 'Nothing new :('
    else:
        Send_Email.main(email_text, ['colin.gerber@gmail.com'])
        print 'Email Sent'

    #save the newly updated post dict
    pickle.save_object(post_text, '/Users/colingerber/Documents/Programming/Personal/Reddit_Bots/post_text.pkl')

    print 'Bot complete'


if __name__ == '__main__':
    main()
