# coding: utf-8

import os

from django.views.generic import TemplateView
from django.shortcuts import render_to_response
from django.http import HttpResponse
from eco_map.forms import AddPointForm

import httplib2
from apiclient.discovery import build

from oauth2client.client import SignedJwtAssertionCredentials
from oauth2client.file import Storage


class HomeView(TemplateView):
    template_name = "base.html"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(HomeView, self).get_context_data(**kwargs)
        # Add in whatever variable you want to use in the view
        context['addPointForm'] = AddPointForm()
        return context


'''
    Google Maps:
    Key for browser apps (with referers)
    API key: ****

    GFT:
    Name:    recycle-map
    Numeric ID:    4302955
    Encrypted ID:    1gvB3SedL89vG5r1128nUN5ICyyw7Wio5g1w1mbk

    SQL example:
    INSERT INTO 1e7y6mtqv892222222222_bbbbbbbbb_CvWhg9gc (Product, Inventory) VALUES ('Red Shoes', 25)
'''


def addPointView(request):

    if request.method == 'POST':  # If the form has been submitted...
        form = AddPointForm(request.POST)  # A form bound to the POST data
        if form.is_valid():  # All validation rules pass
            
            # Check what waste types have been checked by user
            checked_waste_types = form.cleaned_data['waste_types']
            Paper, Metall, Glass, Cloth, Danger, Plastic, Other = [0, 0, 0, 0, 0, 0, 0]
            if ('Paper' in checked_waste_types): Paper = 1
            if ('Metall' in checked_waste_types): Metall = 1
            if ('Glass' in checked_waste_types): Glass = 1
            if ('Cloth' in checked_waste_types): Cloth = 1
            if ('Danger' in checked_waste_types): Danger = 1
            if ('Plastic' in checked_waste_types): Plastic = 1
            if ('Other' in checked_waste_types): Other = 1

            
            table_id = '1gvB3SedL89vG5r1128nUN5ICyyw7Wio5g1w1mbk'
            sqlQuery = ('INSERT INTO {0} ' +
                        '(Title, Location, Phone, \'Work time\', Comment, ' +
                        'Paper, Metall, Glass, Cloth, Danger, Plastic, Other) ' +
                        'VALUES ' +
                        '(\'{1}\', \'{2}\', \'{3}\', \'{4}\', \'{5}\', \'{6}\', ' +
                        '\'{7}\', \'{8}\', \'{9}\', \'{10}\', \'{11}\', ' +
                        '\'{12}\')').format(
                        table_id, form.cleaned_data['name'].encode('utf-8'), form.cleaned_data['adress'].encode('utf-8'),
                        form.cleaned_data['phone'], form.cleaned_data['work_time'],
                        form.cleaned_data['comment'].encode('utf-8'),
                        Paper, Metall, Glass, Cloth, Danger, Plastic, Other)
            # @todo: add correct waste_types ^^^^^^^^^^^^^^^^
            
            
            f = file(os.path.dirname(os.path.abspath(__file__)) + '/../data/d7509b5300823ddbc6a9d3a709a6804bf912d355-privatekey.p12', 'rb')
            key = f.read()
            f.close()

            credentials = SignedJwtAssertionCredentials(
                '185198787335-vup5osvu3bgni0k20gdajlp3ofmb2dno@developer.gserviceaccount.com',
                key,
                scope='https://www.googleapis.com/auth/fusiontables')
            storage = Storage(os.path.dirname(os.path.abspath(__file__)) + '/../data/fusion.dat')
            credentials.set_store(storage)

            http = httplib2.Http()
            http = credentials.authorize(http)
            
            service = build("fusiontables", "v1", http=http)
            response = service.query().sql(sql=sqlQuery).execute(http)
            
            answer = 'not_ok'
            if (response['kind'] == 'fusiontables#sqlresponse'):
                answer = 'ok'
            
            return HttpResponse(answer)
    else:
        form = AddPointForm()  # else show only form

    return render_to_response('addPointForm.html', {'form': form})
