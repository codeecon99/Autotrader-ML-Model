
"""
Name: Jacob Fridman
Date: December, 28, 2023
Description: This program scrapes the canadian autotrader website to find specific information on selected vehicles and then neatly stores the 
data in an excel file
"""

# Import packages
import requests
from bs4 import BeautifulSoup
import re
import random
import math
import itertools
from random import randint
import time
import pandas
import pandas as pd
from IPython.display import display
from time import sleep


def data_request(url):
    """
    This function provides the html for a given url

    Parameters
    ----------
    url : a url

    Returns
    -------
    response : the html present on that url

    """

    #updated to most recent headers
    user_agent_list = [
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/116.0',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
                'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0',
                'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/116.0',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.188'
                 ]
    
    #valid proxies
    valid_proxies = [
                    '66.225.254.16:80',
                    '159.203.61.169:8080',
                    '35.203.65.254:80',
                    '67.43.228.250:5285',
                    '159.203.13.121:80',
                    '69.70.244.34:80',
                   '64.56.150.102:3128',
                    '69.70.244.34:80',
                    '162.223.116.54:80',
                    '184.107.90.1:3128',
                    ]
    
    #randomize user agent to prevent server blocks
    user_agent = random.choice(user_agent_list)
    header = ({'User-Agent': user_agent}) 
    response = requests.get(url, headers = header, timeout = 15)

    #randomize time between calls
    time.sleep(randint(3,6))
    return response


def roundup(x):
    """
    This function rounds up the page number to show desired number of webpages

    Parameters
    ----------
    x : number

    Returns
    -------
    desired number

    """

    return int(math.ceil(x / 100.0)) * 100


def combo_lst(input_nestedlist):
    """
    This function changes a nested list into the desired form

    Parameters
    ----------
    input_nestedlist : a nested list

    Returns
    -------
    resultList : desired list

    """
    
    # creating a new empty list for storing result
    resultList = []
    for m in range(len(input_nestedlist)):
        for n in range (len(input_nestedlist[m])):
            resultList.append(input_nestedlist[m][n])        
    return resultList


def url_counter(soup_):
    """
    This function find the number of webpages availible for a given car

    Parameters
    ----------
    soup_ : pass in html soup of the first webpage

    Returns
    -------
    count_plug : find the number webpages that could be searched

    """

    num_page = soup_.find_all("span", attrs={'class':'at-results-count pull-left'}) #fix soup out not very dynamic!
    for wrapper in num_page:
        count = wrapper.text

    count = int(count.replace(",", ""))
    count_val = int(roundup(count)/100)
    
    count_plug = []
    for i in range(count_val):
        count_plug.append(i*100)
    return count_plug


def url_composer(make,model,count):
    """
    This function creates a list of all the neccesary urls 

    Parameters
    ----------
    make : make of the vehicle
    model : model of the vehicle
    count : total number of webpages

    Returns
    -------
    out_url : a list of all main webpages
    
    """
    
    out_url = []
    for i in count:
        count_p = str(i)
        url = str("https://www.autotrader.ca/cars/" + make + "/"+model+"/" + 
          "?rcp=100&rcs="+ count_p + "&srt=35&prx=-1&loc=M5V%203L9&hprc=True&wcp=True&sts=New-Used&inMarket=advancedSearch")
        out_url.append(url)
    return out_url


def inner_links_final(soupy):
    """
    This function finds all the urls of a given webpage

    Parameters
    ----------
    soup_ : HTML soup

    Returns
    -------
    clean_list : a list of all urls for a given webpage

    """
    
    links = soupy.find_all("a") # Find all elements with the tag <a>
    clean_list = []
    for link in links:
        url_link = link.get("href")
        if url_link != None:
            if url_link.startswith("/a/",0,3) == True:
                clean_list.append(url_link)
    clean_list = list(set(clean_list))
    return clean_list


def dict_maker(soup_s):
    """
    This function creates a dictionary with the desired car features

    Parameters
    ----------
    soup_s : html soup

    Returns
    -------
    dict_ : a final dictionary with the feautres of interest
    """
    
    for wrapper in soup_s.find_all('script',{'type': 'text/javascript'}):
        s = wrapper.text
        i = re.search("hero", s, re.IGNORECASE)
        i2 = re.search("ssoUserInfo", s, re.IGNORECASE)
        str_dic = ''

        if i != None and i2 != None:
            search_i = i.span()[1]
            search_i2 = i2.span()[1]
            str_dic = s[search_i + 3:search_i2 - 13] #feed empty dictionary if not found
            dic1 = "{"+str_dic+"}"
            dict_ = eval(dic1)
            return dict_
        else:
            dic1 = "{"+str_dic+"}"
            dict_ = eval(dic1)   
    return dict_
            

def dict_convert(lst):
    """
    This function converts a list into a dictionary

    Parameters
    ----------
    lst : a list

    Returns
    -------
    Dict_ : a dictionary

    """
    
    Dict_ = {}
    for i in range(len(lst)):
        Dict_[lst[i]['key'].lower()] = lst[i]['value']  
    return Dict_


def dict_maker_extra(soup_s):  
    """
    This function provides more details on the car

    Parameters
    ----------
    soup_s : html soup
    Returns
    -------
    Dict_ : a dictionary with even more feaures on the vehicle 

    """
    
    for wrapper in soup_s.find_all('script',{'type': 'text/javascript'}):
        s = wrapper.text
        j = re.search("specifications", s, re.IGNORECASE)
        j2 = re.search("showMadeIn", s, re.IGNORECASE)
        
        if j != None and j2 != None:
            search_j = j.span()[1]
            search_j2 = j2.span()[1]
            str_lst = s[search_j + 11:search_j2 - 12]
            str_lst = eval(str_lst)
            dict_ =  dict_convert(str_lst)
            return dict_
        else:
            dict_ = eval("{" + "" + "}")    
    return dict_


def checkKey(dic, key):
    """
    This function is a helper function to key_value_out

    Parameters
    ----------
    dic : a dictionary
    key : a key in dictionary

    Returns
    -------
    either a 1 or 0

    """
    
    if key in dic.keys():
        return 1
    else:
        return 0


def key_value_out_str(dic,key):
    """
    This function makes sure that a key is present in the dictionary, if not it will replace the key
    with the values below

    Parameters
    ----------
    dic : a dictionary
    key : a key

    Returns
    -------
    out : either a 'N/A' or value

    """
    
    check = checkKey(dic,key)
    if check == 0:
        out = 'N/A'
    if check == 1:
        out = dic[key]
    return out


def key_value_out_int(dic,key):
    """
    This function makes sure that a key is present in the dictionary, if not it will replace the key
    with the values below

    Parameters
    ----------
    dic : a dictionary
    key : a key

    Returns
    -------
    out : either a 'N/A' or value

    """
    
    check = checkKey(dic,key)
    if check == 0:
        out = 0
    if check == 1:
        out = dic[key]
    return out


def writer(filpath,df):
    """
    This function writes a dataframe to an excel file

    Parameters
    ----------
    filpath : filepath of excel file
    df : the dataframe which is being updated

    Returns
    -------
    None.

    """

    with pd.ExcelWriter(filpath, engine='openpyxl',mode='a',if_sheet_exists='overlay') as writer:
        reader = pd.read_excel(filpath)
        df.to_excel(writer, startrow=reader.shape[0] + 1,index=True,header=False)
    return 


def dict_output(dict1,dict2):
    """
    This function builds the final dictionary that will be created by the script

    Parameters
    ----------
    dict1 : the dictionary with the first features
    dict2 : the dictionary with the other features

    Returns
    -------
    vehicle_dict : a single dictionary with all the desired features

    """

    dict_ = dict1 
    Dict_ = dict2

    make = key_value_out_str(dict_, 'make').lower()
    model = key_value_out_str(dict_, 'model').lower()
    trim = key_value_out_str(dict_, 'trim')
    year = int(key_value_out_int(dict_, 'year'))
    price = int(key_value_out_int(dict_, 'price').replace(",", ""))
    location = key_value_out_str(dict_, 'location') 
    mileage =  key_value_out_str(dict_, 'mileage')  #int((key_value_out_int(dict_, 'mileage').replace("km","")).replace(",",""))#clean this up later!
    transmission = key_value_out_str(Dict_, 'transmission') 
    drivetrain = key_value_out_str(Dict_, 'drivetrain') 
    engine = key_value_out_str(Dict_, 'engine') #new!!!
    fuel_type = key_value_out_str(Dict_, 'fuel type') 
    status = key_value_out_str(dict_, 'status') 
    exterior_colour = key_value_out_str(Dict_, 'exterior colour') 
    interior_colour = key_value_out_str(Dict_, 'interior colour') #new
    doors = key_value_out_str(Dict_, 'doors') 
    vin = key_value_out_str(dict_, 'vin')  
    vehicleAge = key_value_out_str(dict_, 'vehicleAge')  
    priceAnalysis = key_value_out_str(dict_, 'priceAnalysis') 
    priceAnalysisDescription = key_value_out_str(dict_, 'priceAnalysisDescription')  
    carfax = key_value_out_str(dict_, 'carfax')  

    vehicle_dict = {   'make' : make, 
                       'model':model, 
                       'trim': trim, 
                       'year':year,  
                       'price': price, 
                       'location': location,
                       'mileage':mileage,
                       'transmission': transmission,
                       'drivetrain': drivetrain,
                       'engine': engine,
                       'fuel type':fuel_type,
                       'status' :status,
                       'exterior colour':exterior_colour,
                       'interior colour':interior_colour,
                       'doors' :doors,
                       'vin':vin,
                       'vehicleAge':vehicleAge,
                       'priceAnalysis' :priceAnalysis,
                       'priceAnalysisDescription':priceAnalysisDescription,
                       'carfax': carfax
                   }
    return vehicle_dict


def driver(make,model):
    """
    This is the main driver for the script, it find the features of a speciic make and model by scraping the web

    Parameters
    ----------
    make : vehicle make
    model : vehicle model

    Returns
    -------
    all_data : a final list of dictionaries, where each dictionary is the features 
               of a single car

    """
    
    # Compose the URL based on user input. Set to 100 items per page to minimize get requests
    #rcs = 0 means the first page, need to use this initial link to figure out final rcs
    url = str("https://www.autotrader.ca/cars/" + make + "/"+model+"/" + 
              "?rcp=100&rcs=0&srt=35&prx=-1&loc=M5V%203L9&hprc=True&wcp=True&sts=New-Used&inMarket=advancedSearch")

    #request the data for the first link
    soup = data_request(url)
    soup_out = BeautifulSoup(soup.content, 'html.parser')

    #find number of links using soup_out
    #generate a list of all the outer urls 
    num_link = url_counter(soup_out)
    all_outer_url = url_composer(make,model,num_link)
    
    #get all adds availible for the car
    all_links = []
    for link in all_outer_url:
        inner_soup = data_request(link)
        soup_out = BeautifulSoup(inner_soup.content, 'html.parser')
        inner_links_ = inner_links_final(soup_out)
        all_links.append(inner_links_)   

    #return all_links
    combo_lst = list(itertools.chain.from_iterable(all_links))
    
    combo_lst_clean = []
    for i in combo_lst:
        new_link = "https://www.autotrader.ca" + i
        combo_lst_clean.append(new_link)

    #ads that where blocked
    blocked_ads = []
    all_data = []
    blocked_consecutive = 0
    counter = 0
    blocks = 0
    total = len(combo_lst_clean)
    for ad in combo_lst_clean:
        try:
            ads = data_request(ad)
            soup_2 = BeautifulSoup(ads.text, 'lxml')
            dict_1 = dict_maker(soup_2)
            dict_2 = dict_maker_extra(soup_2)
            vehicle_data = dict_output(dict_1,dict_2)
            all_data.append(vehicle_data)
            counter = counter + 1 
            perc = ((counter/total)*100)
            print('Make: ' + make + ' Model: '+ model + ' Ad: ' + str(counter) + "/" + str(total) + "------" + '{:.1f}'.format(perc) + "% complete")
            blocked_consecutive = 0
        #if error occurs try link 4 more times
        except Exception as error:
            print('Server has blocked request: trying Ad Again')
            for x in range(0, 4):  # try 4 times
                try:
                    ads = data_request(ad)
                    soup_2 = BeautifulSoup(ads.text, 'lxml')
                    dict_1 = dict_maker(soup_2)
                    dict_2 = dict_maker_extra(soup_2)
                    vehicle_data = dict_output(dict_1,dict_2)
                    all_data.append(vehicle_data)
                    counter = counter + 1 
                    perc = ((counter/total)*100)
                    print('Success!')
                    print('Make: ' + make + ' Model: '+ model + ' Ad: ' + str(counter) + "/" + str(total) + "------" + '{:.1f}'.format(perc) + "% complete")
                    str_error = None
                except Exception as error:
                    str_error= str(error)                
                if str_error:
                    print('Server is still blocking resuts')
                    blocks = blocks + 1
                    sleep(2)  # wait for 2 seconds before trying to fetch the data again
                else:
                    blocks = 0
                    break
            if blocks == 4:   
                print('Server has completely blocked request - Moving to next ad ')
                #return combo_lst_clean[count:total] #this will get the remainder of the list that I missed 
                blocked_ads.append(ad)
                blocked_consecutive += 1
            if blocks == 60:
                print('The server has locked ip out')
                rest_lst = combo_lst_clean[counter:total]
                blocked_ads = blocked_ads + rest_lst
                break
            pass     
    return all_data, blocked_ads


def master_dict():
    """
    This is the dictionary with all the car makes and model to get data on

    Returns
    -------
    Dict : the dictionary

    """
    
    Dict = {'toyota':['corolla','highlander','camry','prius','RAV4'], 
            'tesla':['model 3','model s','model x', 'model y'], 
             'porsche':['taycan'], 
             'honda': ['accord','civic', 'odyssey','civic coupe', 'civic type r'],
             'acura': ['ilx', 'integra','mdx','nsx','rdx','tl','tlx'],
             'audi':['a3', 'a4','a5','a6','a7','a8','e-tron','q3','q4','q5','q7','q8','s3','s4','s5','s6','s7','s8','rs 3','rs 4','rs 5','rs 6','rs 7','tt','sq5','sq7','sq8'],
             'bmw':['3 series','4 series','5 series','6 series','7 series','8 series','i3','i4','i5','i7','i8','ix','m2','m3','m4','m6','m8','x3','x4','x5','x6','x7','z3','x3 m','x4 m','x5 m','x6 m','z3'],
             'cadillac':['escalade','xt4','xt5','xt6'],
             'chevrolet':['bolt ev','camaro','corvette','cruze'],
             'dodge':['challenger','charger'],
             'ford':['f-150 lightning','mustang mach-e'],
             'infiniti':['q50','q60','qx50','qx60','qx80'],
             'lexus':['is','nx','rx'], 
             'mazda':['cx-5','mazda3'],
             'mercedes-benz':['c-class','cla','s-class'], 
             'subaru':['wrx','crosstrek'],
             'volkswagen':['e-golf','golf','golf gti','golf r','jetta','passat','taos','atlas']
             }
    return Dict


def main():
    """
    This is the main function of the program and it will find all the required features for each vehicle in the dictionary. 
    If there are any errors in fetching the data then the code will continue to run and cars or ads that produced errors
    will be put into a list so that each case can be investigated
    """
    
    #These are the features that will be filled for each car
    vehicle_feautures = [ 'make', 
                          'model', 
                          'trim', 
                          'year', 
                          'price', 
                          'location', 
                          'mileage', 
                          'transmission', 
                          'drivetrain', 
                          'engine',
                          'fuel type',
                          'status', 
                          'exterior colour',
                          'interior colour',
                          'doors', 
                          'vin',
                          'vehicleAge', 
                          'priceAnalysis', 
                          'priceAnalysisDescription',
                          'carfax'   
                        ]
    
    #test cases:
    #make,model = "toyota","camry"
    #Dict = {'toyota':['corolla','highlander'], 'honda': ['civic', 'odyssey']}
    
    Dict = master_dict()
    blocked_lst = []
    failed_car = []
    
    #runs the program on each vehicle in the dictionary
    for key,value in Dict.items():
        for i in value:
            make = key
            model = i
            try:
                #creates the header
                df = pd.DataFrame(columns=vehicle_feautures)
                
                #runs the program and builds the df #make,model
                run_program, blocked = driver(make,model)
                blocked_lst.append(blocked)
                df = pd.DataFrame(run_program)
                
                #This is the filepath where the data will be pushed to
                filepath = "CarDataset.xlsx" 
                writer(filepath,df)
                display(df)
                print(blocked) 
            except Exception as error:
                failed_car.append(key)
                failed_car.append(model)
                pass
    #prints any vehicles that where blocked so that they can be run again at a later time
    #prints cars that failed all together so that they can be re run
    print(blocked_lst)
    print("")
    print(failed_car) 
            
    
#main()
