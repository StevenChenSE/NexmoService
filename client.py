import urllib,json
from django.conf import settings
from django.utils.encoding import smart_str
from keys import API_SECRET,API_KEY

NEXMO_REQUEST_URL='https://api.nexmo.com/verify/json?'
NEXMO_CHECK_URL='https://api.nexmo.com/verify/check/json?'
NEXMO_CONTROL_URL='https://api.nexmo.com/verify/control/json?'
# account settings here
WAIT_TIME=300
BRAND='TESTNEXMO'

class CheckResponce(object):
    def __init__(self, status, error_text=None):
    	self.status=int(status)
    	self.error_text=error_text
    def __str__(self):
    	return "status=%d error_text=%d" % (self.status,self.error_text)
class RequestResponce(object):
	"""docstring for RequestResponce"""
	def __init__(self, request_id,status,error_text=None):
		self.request_id=(request_id)
		self.status=int(status)
		self.error_text=error_text
	def __str__(self):
		return "request_id=%s status=%d error_text=%s"%(self.request_id,self.status,self.error_text)
		
		
def make_request(phoneNumber):
	'make a request,return a RequestResponce'
	params = {
	    'api_key': API_KEY,
	    'api_secret': API_SECRET,
	    'number': phoneNumber,
	    'brand': BRAND,
	    'next_event_wait':WAIT_TIME,
	}
	url = NEXMO_REQUEST_URL + urllib.urlencode(params) 
	response = urllib.urlopen(url)
	status=json.loads(smart_str(response.read()))
	if 'error_text' not in status:
		status['error_text']=None
	if 'request_id' not in status:
		status['request_id']='no_id'
	return RequestResponce(status['request_id'],status['status'],status['error_text'])
	
def cancel(request_id):
	'return an integer,0 for success'
	params = {
	    'api_key': API_KEY,
	    'api_secret': API_SECRET,
	    'request_id': request_id,
	    'cmd':'cancel'
	}
	url=NEXMO_CONTROL_URL+urllib.urlencode(params)
	response=urllib.urlopen(url)
	status=int(json.loads(smart_str(response.read()))['status'])
	return status


def submit(request_id,code,ip=None):
	'check code,return a CheckResponce'
	params = {
    'api_key': API_KEY,
    'api_secret': API_SECRET,
    'request_id': request_id,
    'code': code
	}
	if ip:
		params['ip_address']=ip
	url = NEXMO_CHECK_URL + urllib.urlencode(params)
	response = urllib.urlopen(url)
	status=json.loads(smart_str(response.read()))
	if 'error_text' not in status:
		status['error_text']=None
	return CheckResponce(status['status'],status['error_text'])
if __name__ == '__main__':
	c=make_request('PHONE NUMBER')
	print c
	cancel(c.request_id)

