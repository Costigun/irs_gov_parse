"""
Emphasoft developer challenge
    1.Taking a list of tax form names (ex: "Form W-2", "Form 1095-C"), search the website and
return some informational results. Specifically, you must return the "Product Number", the
"Title", and the maximum and minimum years the form is available for download.
    2.Taking a tax form name (ex: "Form W-2") and a range of years (inclusive, 2018-2020 should
fetch three years), download all PDFs available within that range.
"""
import json
import os
import sys
import requests
from bs4 import BeautifulSoup

URL = 'https://apps.irs.gov/app/picklist/list/priorFormPublication.html'


def get_forms(list_tax_form: list):
    """
    function to get response from iris.gov with all forms content
    :param list_tax_form: list of form names that we want to get info about
    :return: dict with form name,form title
    """
    response_list = []  # list for all responses of form names
    with requests.session() as session:
        for param in list_tax_form:
            request_params = {'value': param,
                              'criteria': 'formNumber',
                              'submit_search': 'Find'
                              }
            res = session.get(URL, params=request_params).content
            response_list.append(res)
        return response_list


def parse_responses(list_tax_form: list):
    """
    function to get all form names,titles years from previous func return
    :param list_tax_form: list of form names that we want to get info about
    :return: list of form names,titles,years
    """
    responses = get_forms(list_tax_form)
    # empty lists to fill them with the received information for all names, years, and titles
    td_form_name, td_form_title, td_form_rev_year = [], [], []
    for response in responses:
        soup = BeautifulSoup(response, 'lxml')
        td_name = soup.find_all('td', {'class': 'LeftCellSpacer'})
        td_title = soup.find_all('td', {'class': 'MiddleCellSpacer'})
        td_rev_year = soup.find_all('td', {'class': 'EndCellSpacer'})
        td_form_name.extend(td_name)
        td_form_title.extend(td_title)
        td_form_rev_year.extend(td_rev_year)
    return td_form_name, td_form_title, td_form_rev_year


def format_responses(list_tax_form: list):
    """
    function to formate all responses for all forms we got!
    1 Task
    :param list_tax_form: list of form names that we want to get info about
    :return: formated names,links,years
    """
    td_names, td_titles, td_years = parse_responses(list_tax_form)
    names = [name.text.strip() for name in td_names]
    links = [link.find('a')['href'] for link in td_names]
    titles = [title.text.strip() for title in td_titles]
    years = [int(year.text.strip()) for year in td_years]
    set_names = set(names)
    final_dict = []
    # loop to create dictionary of result information with years of tax form available to download
    for name in set_names:
        max_year = 0
        min_year = max(years)
        dict1 = {'form_number': name}
        for index, p_name in enumerate(names):
            if p_name == name:
                if years[index] > max_year:
                    max_year = years[index]
                elif years[index] < min_year:
                    min_year = years[index]
                dict1['form_title'] = titles[index]
                dict1['max_year'] = max_year
                dict1['min_year'] = min_year
        final_dict.append(dict1)
    print(json.dumps(final_dict, indent=2))
    return names, links, years


def download_files(list_tax_form):
    """
    2 Task
    Module to download pdf files of form_name that input from user.
    :param list_tax_form: list of form names that we want to get info about
    :return: message to user of successful create file or either
    """
    names, links, years = format_responses(list_tax_form)
    form_name = input('enter form name: ')
    if form_name in names:
        print('form exists. enter years range')
        form_year1 = int(input('start year to analysis: '))
        form_year2 = int(input('end year to analysis: '))
        try:
            os.mkdir(form_name)
        except FileExistsError:
            pass
        r_index = names.index(form_name)
        l_index = names.index(form_name)
        for name in names:
            if name == form_name:
                r_index += 1
        years = years[l_index:r_index]
        if form_year1 < form_year2:
            range_years = range(form_year1, form_year2 + 1)
            for year in range_years:
                if year in years:
                    link = links[years.index(year)]
                    form_file = requests.get(link, allow_redirects=True)
                    open(f'{form_name}/{form_name}_{str(year)}.pdf', 'wb').write(form_file.content)
            print(f'files saved to {form_name}/ directory!')
    else:
        print('input correct form name!')


if __name__ == '__main__':
    tax_list = sys.argv[1:]  # form names
    download_files(tax_list)
