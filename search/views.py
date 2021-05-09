from django.shortcuts import render, redirect
from .forms import SearchForm
import urllib
import requests
import json
import pandas as pd
from .models import Video

YOUTUBE_API_KEY = 'AIzaSyA-PddeHxoBEmK9Y0COA-eoyt9a0316jYk'


def home(request):
    return render(request, 'search/index.html')


def about(request):
    return render(request, 'search/about.html')


def covidhome(request):
    df2 = pd.read_excel('search/StateHelpLine.xlsx')

    names_list1 = df2['State'].to_list()
    help_list1 = df2['Number'].to_list()
    n = range(1, len(names_list1) + 1)

    my_list = zip(n, names_list1, help_list1)

    data = {
        'my_list': my_list,
    }
    return render(request, 'search/covidhome.html', data)


def search(request):
    if request.method == 'GET':
        return render(request, 'search/search.html', {'form': SearchForm})
    sub = SearchForm()
    if request.method == 'POST':
        try:
            sub = SearchForm(request.POST)
            if sub.is_valid():
                term = sub.cleaned_data['isbn']
                return redirect('search:searchresult')
        except Exception as e:
            return render(request, 'search/search.html',
                          {'form': sub, 'error': 'Invalid Drug/Drug Not found, Please try again.'})
        return render(request, 'search/search.html', {'form': SearchForm})


global string1


def searchresult(request):
    global string1
    string1 = request.POST.get('search').lower()
    # PMBJP
    df = pd.read_excel('search/Product.xlsx')

    df = df.rename(
        columns={'Drug Code': 'Drug_Code', 'Generic Name of the Medicine': 'Generic_Name', 'Unit Size': 'Unit_Size',
                 'Therapeutic Category': 'Therapeutic_Category'})
    df['Generic_Name'] = df['Generic_Name'].str.lower()

    drug_name = string1
    df2 = df.loc[df['Generic_Name'].str.contains(drug_name, na=False), ['Generic_Name', 'MRP']]
    generic_names_list = df2['Generic_Name'].to_list()
    df2['MRP'] = df2['MRP'].astype(str)
    df2['MRP'] = df2['MRP'].str.replace(r'\n0', '')
    df2['MRP'] = df2['MRP'].str.replace(r'\n1', '')
    df2['MRP'] = df2['MRP'].str.replace(r'\n2', '')
    df2['MRP'] = df2['MRP'].str.replace(r'\n3', '')
    df2['MRP'] = df2['MRP'].str.replace(r'\n4', '')
    df2['MRP'] = df2['MRP'].str.replace(r'\n5', '')
    df2['MRP'] = df2['MRP'].str.replace(r'\n6', '')

    MRP_list = df2['MRP'].map(float).to_list()

    mylist = zip(generic_names_list, MRP_list)
    if not MRP_list:
        minName = 'N/A'
        minPrice = 'N/A'
    else:
        temp = min(MRP_list)
        res = [i for i, j in enumerate(MRP_list) if j == temp]
        minName = generic_names_list[res[0]]
        minPrice = MRP_list[res[0]]

    # Medicine Database
    df_brand = pd.read_excel('search/Sample.xlsx')

    df_brand['Salt'] = df_brand['Salt'].str.lower()
    drug_name = string1
    df3 = df_brand.loc[
        df_brand['Salt'].str.contains(drug_name, na=False), ['Medicine Name', 'Salt', 'Manufacturer', 'MRP',
                                                             'Side Effects', 'Uses', 'Habit Forming']]

    names_list = df3['Medicine Name'].to_list()
    manufacturer_list = df3['Manufacturer'].to_list()
    MRP_list1 = df3['MRP'].map(float).to_list()
    se_list = df3['Side Effects'].to_list()
    use_list = df3['Uses'].to_list()
    habit_list = df3['Habit Forming'].to_list()

    mylist1 = zip(names_list, manufacturer_list, MRP_list1)

    if not MRP_list1:
        minName1 = 'N/A'
        minPrice1 = 'N/A'
        side_effect = 'N/A'
        uses = 'N/A'
        habit = 'N/A'
    else:
        temp = min(MRP_list1)
        res = [i for i, j in enumerate(MRP_list1) if j == temp]
        minName0 = names_list[res[0]]
        minName2 = manufacturer_list[res[0]]
        minName1 = minName0 + " " + minName2
        minPrice1 = MRP_list1[res[0]]
        side_effect = se_list[res[0]]
        uses = use_list[res[0]]
        habit = habit_list[res[0]]
    if minPrice == 'N/A' or minPrice1 == 'N/A':
        bestname = 'N/A'
        bestsection = '(Data not sufficient)'
        worstsection = '(Data not sufficient)'
        bestprice = 'N/A'
        savings = 0
        difference = 0

    elif minPrice1 > minPrice:
        bestname = minName
        bestsection = 'Jan Aushadhi'
        worstsection = 'Open Market'
        bestprice = minPrice
        savings = ((minPrice1 - minPrice) / minPrice) * 100
        difference = (minPrice1 - minPrice)
        difference = format(difference, '.2f')
        savings = format(savings, '.2f')

    else:
        bestname = minName1
        bestsection = 'Open Market'
        worstsection = 'Jan Aushadhi'
        bestprice = minPrice1
        savings = ((minPrice - minPrice1) / minPrice1) * 100
        difference = (minPrice - minPrice1)
        difference = format(difference, '.2f')
        savings = format(savings, '.2f')

    # Youtube Videos
    encoded_search_term = urllib.parse.quote(string1)
    response = requests.get(
        'https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=6&q=' + encoded_search_term + '&key=' + YOUTUBE_API_KEY)
    json = response.json()

    url_id1 = json['items'][0]['id']['videoId']
    url_id2 = json['items'][1]['id']['videoId']
    url_id3 = json['items'][2]['id']['videoId']
    title1 = json['items'][0]['snippet']['title']
    title2 = json['items'][1]['snippet']['title']
    title3 = json['items'][2]['snippet']['title']

    data = {
        'entered': drug_name,
        'list1': generic_names_list,
        'list2': MRP_list,
        'mylist': mylist,
        'minName': minName,
        'minPrice': minPrice,

        'list3': names_list,
        'list4': manufacturer_list,
        'list5': MRP_list1,
        'minName1': minName1,
        'minPrice1': minPrice1,
        'mylist1': mylist1,

        'bestname': bestname,
        'bestprice': bestprice,
        'bestsection': bestsection,
        'worstsection': worstsection,
        'savings': savings,
        'difference': difference,

        'url1': url_id1,
        'url2': url_id2,
        'url3': url_id3,

        'title1': title1,
        'title2': title2,
        'title3': title3,

        'side_effect': side_effect,
        'uses': uses,
        'habit': habit

    }

    return render(request, 'search/show.html', data)


def allresult(request):
    print(string1)
    df = pd.read_excel('search/Product.xlsx')
    df = df.rename(
        columns={'Drug Code': 'Drug_Code', 'Generic Name of the Medicine': 'Generic_Name', 'Unit Size': 'Unit_Size',
                 'Therapeutic Category': 'Therapeutic_Category'})
    df['Generic_Name'] = df['Generic_Name'].str.lower()
    drug_name = string1
    df2 = df.loc[df['Generic_Name'].str.contains(drug_name, na=False), ['Generic_Name', 'MRP']]
    generic_names_list = df2['Generic_Name'].to_list()
    df2['MRP'] = df2['MRP'].astype(str)
    df2['MRP'] = df2['MRP'].str.replace(r'\n0', '')
    df2['MRP'] = df2['MRP'].str.replace(r'\n1', '')
    df2['MRP'] = df2['MRP'].str.replace(r'\n2', '')
    df2['MRP'] = df2['MRP'].str.replace(r'\n3', '')
    df2['MRP'] = df2['MRP'].str.replace(r'\n4', '')
    df2['MRP'] = df2['MRP'].str.replace(r'\n5', '')
    df2['MRP'] = df2['MRP'].str.replace(r'\n6', '')

    MRP_list = df2['MRP'].map(float).to_list()
    mylist = zip(generic_names_list, MRP_list)
    if not MRP_list:
        minName = 'N/A'
        minPrice = 'N/A'
    else:
        temp = min(MRP_list)
        res = [i for i, j in enumerate(MRP_list) if j == temp]
        minName = generic_names_list[res[0]]
        minPrice = MRP_list[res[0]]

    # Medicine Database
    df_brand = pd.read_excel('search/Sample.xlsx')
    df_brand['Salt'] = df_brand['Salt'].str.lower()

    drug_name = string1
    df3 = df_brand.loc[
        df_brand['Salt'].str.contains(drug_name, na=False), ['Medicine Name', 'Salt', 'Manufacturer', 'MRP']]

    names_list = df3['Medicine Name'].to_list()
    manufacturer_list = df3['Manufacturer'].to_list()
    MRP_list1 = df3['MRP'].map(float).to_list()

    mylist1 = zip(names_list, manufacturer_list, MRP_list1)

    if not MRP_list1:
        minName1 = 'N/A'
        minPrice1 = 'N/A'
    else:
        temp = min(MRP_list1)
        res = [i for i, j in enumerate(MRP_list1) if j == temp]
        minName0 = names_list[res[0]]
        minName2 = manufacturer_list[res[0]]
        minName1 = minName0 + " " + minName2
        minPrice1 = MRP_list1[res[0]]

    if minPrice == 'N/A' or minPrice1 == 'N/A':
        bestname = 'N/A'
        bestsection = 'Data not sufficient'
        bestprice = 'N/A'
        savings = 0

    elif minPrice1 > minPrice:
        bestname = minName
        bestsection = 'Jan Aushadhi'
        bestprice = minPrice
        savings = ((minPrice1 - minPrice) / minPrice) * 100
        savings = format(savings, '.2f')

    else:
        bestname = minName1
        bestsection = 'Medicine Database'
        bestprice = minPrice1
        savings = ((minPrice - minPrice1) / minPrice1) * 100
        savings = format(savings, '.2f')

    data = {
        'list1': generic_names_list,
        'list2': MRP_list,
        'mylist': mylist,
        'minName': minName,
        'minPrice': minPrice,

        'list3': names_list,
        'list4': manufacturer_list,
        'list5': MRP_list1,
        'minName1': minName1,
        'minPrice1': minPrice1,
        'mylist1': mylist1,

        'bestname': bestname,
        'bestprice': bestprice,
        'bestsection': bestsection,
        'savings': savings,
        'entered': drug_name,
    }
    return render(request, 'search/allshow.html', data)


# Covid Section
def showrem(request):
    entered = request.POST.get('captions')
    string = request.POST.get('captions').lower()
    df = pd.read_excel('search/Remdesevir.xlsx')
    df['State'] = df['State'].str.lower()
    df2 = df.loc[
        df['State'].str.contains(string, na=False), ['Distributor Name', 'Address', 'E-Mail Address', 'Telephone']]

    names_list1 = df2['Distributor Name'].to_list()
    names_list = []
    [names_list.append(x) for x in names_list1 if x not in names_list]
    add_list1 = df2['Address'].to_list()
    add_list = []
    [add_list.append(x) for x in add_list1 if x not in add_list]
    tele_list1 = df2['Telephone'].to_list()
    tele_list = []
    [tele_list.append(x) for x in tele_list1 if x not in tele_list]
    mail_list1 = df2['E-Mail Address'].to_list()
    mail_list = []
    [mail_list.append(x) for x in mail_list1 if x not in mail_list]

    n = range(1, len(names_list) + 1)

    my_list = zip(n, names_list, add_list, tele_list, mail_list)

    data = {
        'my_list': my_list,
        'entered': entered,
    }

    return render(request, 'search/showrem.html', data)


def tozi(request):
    entered = request.POST.get('captions')
    string = request.POST.get('captions').lower()
    df = pd.read_excel('search/Tocilizumab.xlsx')
    df['State'] = df['State'].str.lower()
    df2 = df.loc[
        df['State'].str.contains(string, na=False), ['Distributor Name', 'Address']]

    names_list1 = df2['Distributor Name'].to_list()
    names_list = []
    [names_list.append(x) for x in names_list1 if x not in names_list]
    add_list1 = df2['Address'].to_list()
    add_list = []
    [add_list.append(x) for x in add_list1 if x not in add_list]

    n = range(1, len(names_list) + 1)

    my_list = zip(n, names_list, add_list)

    data = {
        'my_list': my_list,
        'entered': entered,
    }

    return render(request, 'search/tozi.html', data)


def bloodamb(request):
    entered = request.POST.get('captions')
    string = request.POST.get('captions').lower()
    df = pd.read_excel('search/BloodBank.xlsx')
    df['State'] = df['State'].str.lower()
    df2 = df.loc[
        df['State'].str.contains(string, na=False), ['Name', 'City', 'Address', 'Details', 'Phone']]

    names_list1 = df2['Name'].to_list()
    city_list1 = df2['City'].to_list()
    add_list1 = df2['Address'].to_list()
    tele_list1 = df2['Phone'].to_list()
    mail_list1 = df2['Details'].to_list()

    n = range(1, len(names_list1) + 1)

    my_list = zip(n, city_list1, mail_list1, names_list1, add_list1, tele_list1)

    data = {
        'my_list': my_list,
        'entered': entered,
    }

    return render(request, 'search/bloodamb.html', data)


def vaccine(request):
    entered = request.POST.get('captions')
    string = request.POST.get('captions').lower()
    df = pd.read_excel('search/Vaccine.xlsx')
    df['District'] = df['District'].str.lower()
    df2 = df.loc[
        df['District'].str.contains(string, na=False), ['Name of the Vaccination Site', 'State', 'District', 'Address',
                                                        'Contact Person', 'Mobile Number']]

    names_list = df2['Name of the Vaccination Site'].to_list()
    state_list = df2['State'].to_list()

    df2['District'] = df2['District'].str.upper()
    dist_list = df2['District'].to_list()

    address_list = df2['Address'].to_list()
    contact_list = df2['Contact Person'].to_list()
    mob_list = df2['Mobile Number'].to_list()
    n = range(1, len(names_list) + 1)

    my_list = zip(n, names_list, state_list, dist_list, address_list, contact_list, mob_list)

    data = {
        'my_list': my_list,
        'entered': entered,
    }

    return render(request, 'search/vaccine.html', data)
