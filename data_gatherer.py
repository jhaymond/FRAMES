from authorization import *
from time import *
from json import *
import os
from shutil import *

def get_new_articles(inoreader_auth):
    subscriptions_request = get('https://www.inoreader.com/reader/api/0/subscription/list', headers = inoreader_auth)
    if "200" not in str(subscriptions_request):
        return "Inoreader returned " + str(subscriptions_request)
    
    subscriptions = subscriptions_request.json()['subscriptions']
    article_data = []
    for sub in subscriptions:
        content_request = get('https://www.inoreader.com/reader/atom/' + sub['id'] + '?n=150&output=json', headers = inoreader_auth)
        if "200" not in str(content_request):
            article_data.append({'No response from ' + sub['id']})
        else:
            article_data.extend(content_request.json()['items'])

    return article_data

def main():
    inoreader_auth = auth_inoreader()
    data_dir = os.getenv("HOME") + "/Data_Scrapes/unformatted/"
    
    start_time = time()
    while True:
        new_data = get_new_articles(inoreader_auth)
        output_filename = 'articles_' + strftime("%m-%d-%y_%H:%M") + '.txt'
        output_file = open(output_filename, 'w')
        output_file.write(dumps(new_data))
        output_file.close()
        move(output_filename, data_dir)
        sleep(3600.0 - ((time() - start_time) % 3600.0))

if __name__ == "__main__":
    main()
