from httplib2 import Http
import json
import sys

try:
	title=sys.argv[1]
except:
	title=0
	
#http://example.com/jsonapi/node/article?filter[article-title][path]=title&filter[article-title][value]={{title_filter}}&filter[article-title][operator]==

#http://survey.houseofkoffler.com/jsonapi/node/article

#http://survey.houseofkoffler.com/jsonapi/node/article?filter[article-title][path]=title&filter[article-title][value]={{title_filter}}&filter[article-title][operator]==

d=open('drupal_credentials.json','r')
t=d.read()
credentials=json.loads(t)
d.close()


def get_item(title):
	
	USER = credentials['USER']
	PASSWORD = credentials['PASSWORD']
	
	http = Http('.cache')
	http.add_credentials(USER, PASSWORD)
	url ='http://survey.houseofkoffler.com/jsonapi/node/article?filter[article-title][path]=title&filter[article-title][value]=%s&filter[article-title][operator]==' %title
	headers={'Content-type':'application/vnd.api+json', 'Accept':'application/vnd.api+json'}
	
	resp, content = http.request(
        uri=url,
        method='GET',
        headers=headers    )
	
	print(resp)



def create_item():
	
	USER = credentials['USER']
	PASSWORD = credentials['PASSWORD']
	
	http = Http('.cache')
	http.add_credentials(USER, PASSWORD)
	url ='http://survey.houseofkoffler.com/jsonapi/node/article'
	headers={'Content-type':'application/vnd.api+json', 'Accept':'application/vnd.api+json'}
	
	post_data ={
	"data": {
	"type": "node--article",
	"attributes": {
	"title": "My custom title",
	"body": {
	"value": "Custom value",
	"format": "plain_text"}}
	}
	}
	
	resp, content = http.request(
        uri=url,
        method='POST',
        headers=headers,
        body=json.dumps(post_data)
    )
	
	print(resp)
	
if __name__ == '__main__':
	
	if title ==0:
		create_item()
	else:
		get_item(title)
