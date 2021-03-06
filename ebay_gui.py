#!/usr/bin/env python
#
# Author: John Glatts
# This is a program for searching\scraping EBAY.
# Search for Products, and see when\how much they sold for.
#
#
import PySimpleGUI as sg
import requests
import string
from bs4 import BeautifulSoup


def bayscrap(products):
    """ Get some info from EBAY with requests and bs4.
        Add empty scrap check
    """

    url = 'https://www.ebay.com/sch/' + products
    # Add headers
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}
    source_code = requests.get(url, headers=headers)
    plain_text = source_code.text

    content = ''
    soup = BeautifulSoup(plain_text, "html.parser")
    for items in soup.find_all("div", {"class": "s-item__info clearfix"}):
        # filtering
        for char in items.get_text():
            if char in string.printable:
                content += char

        content += '\n\n\n'

    return content


def sold_menu(products):
    """ Scrap EBAY for sold items of the search product. """

    print('\nDisplaying Sold Items For:' + ' ' + products.title() + '\n')
    sold_url = 'https://www.ebay.com/sch/i.html?_from=R40&_nkw=' + products + '&_sacat=0&LH_Sold=1&_dmd=2'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}
    src_sold = requests.get(sold_url, headers=headers)
    bs4_text = src_sold.text

    sold_soup = BeautifulSoup(bs4_text, 'html.parser')
    filtered = ''
    for sold in sold_soup.find_all("li", {"class": "s-item"}):
        #print('\n' + sold.get_text())
        for char in sold.get_text():
            if char in string.printable:
                filtered += char
        filtered += '\n\n\n'

    return filtered


def sold_form(product):
    """ GUI for sold products """

    content = sold_menu(product)
    sg.ChangeLookAndFeel('GreenMono')
    sg.SetOptions(element_padding=(5, 0))
    heading = ("sold %s-products" % product)

    layout = [
            [sg.Text(heading.title(), size=(20, 1), justification='center', font=("Helvetica", 35), text_color="blue",
                relief=sg.RELIEF_RIDGE)],
            [sg.Multiline(content, size=(70, 12))],
            [sg.In('JDG', key='input', do_not_clear=True)],
            [sg.Button('HOME', button_color=('black', 'white')), sg.Button('Sold-Listings',
            button_color=('black', 'white')), sg.Button('Change URL', button_color=('black', 'white')),
             sg.Button('EXIT', button_color=('black', 'white'))]
        ]

    window = sg.Window("Ebay Feed", default_element_size=(12, 1), auto_size_text=False,
                           auto_size_buttons=True).Layout(layout)

    # read values from buttons and respond accordingly
    while True:
        event, value = window.Read()
        if event == 'HOME':
            begin_form()
        elif event == 'Sold-Listings':
            sold_form(product)
        elif event == 'Change URL':
            begin_form()
        else:
            return


def begin_form():
    """ Prompt the user what products to find """

    searches = []
    sg.ChangeLookAndFeel('LightGreen')
    layout = [
                [sg.Text('Search Ebay!', size=(21, 1), justification='center', font=("Helvetica", 35), text_color="blue",
                 relief=sg.RELIEF_RIDGE)],
                [sg.Text('Enter products to search for', pad=(210, 5))],
                [sg.InputText(focus=True, pad=(130, 5))],
                [sg.Button('Find Products', button_color=('black', 'red'), font=("Helvetica", 15), pad=(225, 5))]
             ]

    window = sg.Window('Find Products').Layout(layout)
    while True:
        button, value = window.Read()
        if button == 'Find Products':
            val_string = ''.join(value)
            #print(val_string)
            # keep track of the searches
            searches.append(val_string)
            test_menus(val_string)
        else:
            exit_dsply(searches)
            return



def test_menus(product):
    """ Initial GUI product page. Scraps ebay for products.
        TODO:
            - add links
            - more button options
            - format improvements
     """

    output = bayscrap(product)
    # work on filtering
    filtered = ''
    for char_two in output:
        if char_two in string.printable:
            filtered += char_two
    #print(filtered)
    sg.ChangeLookAndFeel('GreenMono')
    sg.SetOptions(element_padding=(5, 0))
    heading = ("%s-products" % product)

    layout = [
            [sg.Text(heading.title(), size=(20, 1), justification='center', font=("Helvetica", 35), text_color="blue",
                relief=sg.RELIEF_RIDGE)],
            [sg.Multiline(output, size=(70, 12))],
            [sg.In('JDG', key='input', do_not_clear=True)],
        [sg.Button('HOME', button_color=('black', 'white')),
         sg.Button('Sold-Listings', button_color=('black', 'white')), sg.Button('EXIT', button_color=('black', 'white'))]
    ]

    window = sg.Window("Ebay Feed", default_element_size=(12, 1), auto_size_text=False,
                           auto_size_buttons=True).Layout(layout)

    # read values from buttons and respond accordingly
    while True:
        event, value = window.Read()
        if event == 'HOME':
            begin_form()
        elif event == 'Sold-Listings':
            sold_form(product)
        # same functionality as HOME btn
        # upgrade this ish
        elif event == 'Change URL':
            begin_form()
        else:
            return


def exit_dsply(searches):
    """ Display console info about searches"""

    # count searches
    for idx in searches:
        # get rid of print statement
        add_idx += idx

    print("\nAmount of Searches: %d" % add_idx)

    # print all searches
    for search in searches:
        print("\n")
        print(search)

begin_form()
