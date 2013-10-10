from connections import connector
from globals import globals
from lib import *
import datetime
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse

def index(request):
    '''
    Handler for the accounts
    '''
    
    # add a list of pages in the view
    globals['sections'] = getSiteSections('accounts')
    
    accounts = getAccountsWithNames(connector)
    page_title = "View accounts"
    context = {'globals': globals, 'page_title': page_title, 'accounts': accounts}
    return render(request, 'accounts/index.html', context)

def add(request):
    '''
    Handler for the account create form
    '''
    context = getAddAccountFormContext()
    return render(request, 'accounts/add.html', context)

def getAddAccountFormContext(account_name='', currency='btc', error=None):
    
    # get available currencies
    currencies_available = []
    currencies = connector.services.keys()
    for curr in currencies:
        currencies_available.append({'name': curr, 'title': connector.config[curr]['currency_name']})
        
    page_title = "Create account"
    context = {'globals': globals, 'page_title': page_title, 'currencies': currencies_available, 'account_name': account_name, 'currency': currency, 'selected_currency': currency, 'error_message': error}
    return context

def create(request):
    try:
        account_name = request.POST['account_name']
        currency = request.POST['currency']
        if not account_name:
            raise Exception('Account name not provided')
    except (Exception, KeyError) as e:
        context = getAddAccountFormContext(account_name=account_name, currency=currency, error=e)
        return render(request, 'accounts/add.html', context)
    else:
        # all ok, create account
        new_address = connector.getnewaddress(currency, account_name)
        return HttpResponseRedirect(reverse('accounts:index'))
    
    