import requests
import json
from bs4 import BeautifulSoup
URL = 'https://apps.irs.gov/app/picklist/list/priorFormPublication.html'


def get_forms(list_tax_form):
    """
    :param list_tax_form: list of form names that we want to get info about
    :return: dict with form name,form title
    """
    response_list = [] # list for all responses of form names
    with requests.session() as session:
        for param in list_tax_form:
            request_params = {'value': param,
                              'criteria': 'formNumber',
                              'submit_search': 'Find'
                              }
            res = session.get(URL,params=request_params).content
            response_list.append(res)
        return response_list

def parse_responses(list_tax_form):
    responses = get_forms(list_tax_form)
    td_form_name,td_form_title,td_form_rev_year = None,None,None
    for response in responses:
        soup = BeautifulSoup(response,'lxml')
        td_form_name = soup.find_all('td',{'class':'LeftCellSpacer'})
        td_form_title = soup.find_all('td',{'class':'MiddleCellSpacer'})
        td_form_rev_year = soup.find_all('td',{'class':'EndCellSpacer'})
    return td_form_name,td_form_title,td_form_rev_year



def format_responses(list_tax_form):
    td_names,td_titles,td_years = parse_responses(list_tax_form)
    names = [name.text.strip() for name in td_names]
    links = [link.find('a')['href'] for link in td_names]
    titles = [title.text.strip() for title in td_titles]
    years = [int(year.text.strip()) for year in td_years]
    set_names = set(names)
    final_dict = []

    for name in set_names:
        max_year = 0
        min_year = max(years)
        dict1 = {'form_number':name}
        for index,p_name in enumerate(names):
            if p_name == name:
                if years[index] > max_year:
                    max_year = years[index]
                elif years[index] < min_year:
                    min_year = years[index]
                dict1['form_title'] = titles[index]
                dict1['max_year'] = max_year
                dict1['min_year'] = min_year
        final_dict.append(dict1)
    print(json.dumps(final_dict))

format_responses(['FORM'])