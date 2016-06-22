import os
import sys
import socket

from django import forms
from django.conf import settings
try:
    from django.utils.encoding import smart_unicode
except ImportError:
    from django.utils.encoding import smart_text as smart_unicode

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

import client


class NexmoField(forms.CharField):

    def __init__(self,*args, **kwargs):
        """
        """
        super(NexmoField, self).__init__(*args, **kwargs)

    def clean(self,values):
        '''
        values[0]= requestID
        values[1]= codefromuser
        '''
        super(NexmoField, self).clean(values[1])
        nexmo_challenge_value = smart_unicode(values[1])
        request_id=smart_unicode(values[0])

        try:
            responce = client.submit(
                request_id,
                nexmo_challenge_value)
            
        except socket.error: # Catch timeouts, etc
            raise ValidationError(
                'network error'
            )

        if responce.status!=0:
            raise ValidationError(
                responce.error_text
            )
        return values[1]

if __name__ == '__main__':
    responce=client.make_request('YOUR PHONE NUMBER')
    if responce.status==0:
        request_id=responce.request_id
        n=NexmoField()
        print n.clean([responce.request_id,input('input code:')])
    else:
        print responce.error_text
