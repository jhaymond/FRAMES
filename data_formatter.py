from authorization import *
from json import *
from shutil import *
from time import *
import os

def format_article_data(article_data, api_client):
    articles = []
    for article in article_data:
        articles.append({'id': article['id'], 'media_source': article['origin']['title'], 'title': article['title'], 'url': article['canonical'][0]['href'], 'author': article['author']})
        
        confidence_request = api_client.get_confidence(articles[-1]['url'])
        if confidence_request['status'] != '200':
            return "Readability returned " + confidence_request['status']
        else:
            articles[-1]['confidence'] = confidence_request.content['confidence']
            article_content_request = api_client.get_article_content(articles[-1]['url'])
            if article_content_request['status'] != '200':
                articles[-1]['content'] = "Unavailable"
            else:
                articles[-1]['content'] = article_content_request.content['content']
    
    return articles

def main(data_file = None):
    readability_client = auth_readability()
    
    if not data_file is None:
        data_file = open(data_file, 'r')
    else:
        raw_data_dir = os.getenv("HOME") + "/Data_Scrapes/unformatted/"
        archive_dir = os.getenv("HOME") + "/Data_Scrapes/archive/"
        clean_data_dir = os.getenv("HOME") + "/Data_Scrapes/formatted/"
        while True:
            if os.path.isfile(raw_data_dir + 'articles_' + strftime("%m-%d-%y_%H:%M") + '.txt'):
                data_filename = 'articles_' + strftime("%m-%d-%y_%H:%M") + '.txt'
                
                data_file = open(raw_data_dir + data_filename, 'r')
                article_data = loads(data_file.read())
                data_file.close()
                
                articles = format_article_data(article_data, readability_client)
                
                move(raw_data_dir + data_filename, archive_dir)
                
                data_file = open(clean_data_dir + data_filename, 'w')
                data_file.write(dumps(articles))
                data_file.close()

if __name__ == "__main__":
    main()
