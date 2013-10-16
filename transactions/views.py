from connections import connector
import config
import generic
from django.shortcuts import render
import math

current_section = 'transactions'

def index(request, page=0):
    '''
    handler for the transactions
    '''
    page = int(page)
    items_per_page = 10
    page_title = "Transactions"
    
    transactions = generic.getTransactions(connector = connector, sort_by = 'time', reverse_order = True)
    
    for transaction in transactions:
        transaction['currency_symbol'] = generic.getCurrencySymbol(transaction['currency'].lower())
        if transaction['category'] == 'receive':
            transaction['icon'] = 'glyphicon-circle-arrow-down'
        elif transaction['category'] == 'send':
            transaction['icon'] = 'glyphicon-circle-arrow-up'
        elif transaction['category'] == 'move':
            transaction['icon'] = 'glyphicon-circle-arrow-right'
    
    # pagify
    if page is 0:
        # pager off
        selected_transactions = transactions
        max_page = 0
        pages = []
        show_pager = False
        current_subsection = 'all'
        current_activesession = ''
    else:
        # pager on
        page_id = page-1
        selected_transactions = transactions[(page_id*items_per_page):((page_id*items_per_page)+items_per_page)]
        max_page = int(math.ceil(len(transactions)/items_per_page))+1
        pages = [i+1 for i in range(max_page)]
        show_pager = True
        current_subsection = 'pages'
        current_activesession = 'Page %s' % page
    
    # add a list of pages in the view
    sections = generic.getSiteSections(current_section)
    
    context = {'globals': config.MainConfig['globals'], 'breadcrumbs': generic.buildBreadcrumbs(current_section, '', current_activesession), 'page_title': page_title, 'page_sections': sections, 'transactions': selected_transactions, 'show_pager': show_pager, 'next_page': min((page+1), len(pages)), 'prev_page': max(1, page-1), 'pages': pages, 'current_page': page}
    return render(request, 'transactions/index.html', context)

