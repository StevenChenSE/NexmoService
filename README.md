#NexmoService
This is a simple django app that wrapps [Nexmo sevice API](https://docs.nexmo.com/).

client.py wrapps the Nexmo API.

fields.py implements a django forms.Charfield which cleans itself using the client API.
###How to set your keys(update)
Add a simple keys.py in the folder which contains:

	API_KEY='YOUR API_KEY'
	API_SECRET='YOUR API_SECRET'
###Usage
	if __name__ == '__main__':
    responce=client.make_request('YOUR PHONE NUMBER')
    if responce.status==0:
        request_id=responce.request_id
        n=NexmoField()
        print n.clean([responce.request_id,input('input code:')])
    else:
        print responce.error_text