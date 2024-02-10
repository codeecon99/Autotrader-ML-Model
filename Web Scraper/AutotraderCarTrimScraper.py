"""
Name: Jacob Fridman
Date: December, 28, 2023
Description: This program scrapes the canadian autotrader website to find all car trims for specific vehicles and then neatly stores the 
data in an excel file
"""

#imports
from AutotraderCarScraper import data_request
from AutotraderCarScraper import writer
from IPython.display import display    
from bs4 import BeautifulSoup
import pandas as pd
import re


def url(make,model):
    """
    This function creates the url for autotrader 

    Parameters
    ----------
    make : car make
    model : car model

    Returns
    -------
    url : url for specific car

    """
    
    url = str("https://www.autotrader.ca/cars/" + make + "/"+model+"/" + 
              "?rcp=100&rcs=0&srt=35&prx=-1&loc=M5V%203L9&hprc=True&wcp=True&sts=New-Used&inMarket=advancedSearch")
    return url


def final_dictionary():
    """
    The vehicles that will be searched

    Returns
    -------
    Dict : A dictionary of all vehicles of interest

    """
    
    Dict = {'toyota':['corolla','highlander','camry','prius','RAV4'], 
            'tesla':['model 3','model s','model x', 'model y'], 
             'porsche':['taycan'], ##
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


def find_max_list(list):
    """
    This function finds the largest list in a list of lists

    Parameters
    ----------
    list : a list

    Returns
    -------
    the largest list length

    """
    
    list_len = [len(i) for i in list]
    return max(list_len)
    
    
def headers(value):
    """
    This function is used to create the row header for the dataframe

    Parameters
    ----------
    value : A number for the largest trim number

    Returns
    -------
    lst : A list with all possible trims

    """
    
    lst = ['Make','Model']
    for i in range(value-2):
        add = "trim " + str(i)
        lst.append(add)
    return lst
      

def main():
    """  
    This is the main function of the program and it will find all the car trims for each vehicle in the dictionary. 
    If there are any errors in fetching the data then the code will continue to run and cars that produced errors
    will be put into a list so that each case can be investigated
    """
     
    Dict = final_dictionary()
    
    #test cases: 
    #Dict = { 'cadillac':['escalade','xt4','xt5','xt6']}
    #Dict = {'tesla':['model 3','model s','model x', 'model y'] , 'porsche':['taycan'] }
    
    failed_car = []
    final = []
    for key,value in Dict.items():
        for i in value:
            
            make = key
            model = i
            
            try:
                web_url = url(make,model)
                response = data_request(web_url)
                soup = BeautifulSoup(response.content, 'html.parser')
                trim = soup.find_all("ul", attrs={'id':'fbTrim'})
                
                #cleaning the data
                trim_lst = []
                for wrapper in trim:
                    s = wrapper.text
                    trim_lst.append(s.split("\n"))  
                trim_lst = trim_lst[0]
                trim_lst = [i for i in trim_lst if i]
                
                ff = [make,model]
                for item in trim_lst:
                    ff.append(re.sub(r" ?\([^)]+\)", "", item))
                final.append(ff)

            except Exception as error:
                failed_car.append(key)
                failed_car.append(model)
                pass
       
    features = find_max_list(final)
    f_header = headers(features)  
    df = pd.DataFrame(final, columns = f_header)   
    
    #sending dataframe to desired filepath
    filepath = "CarTrimData.xlsx" 
    writer(filepath,df)
    
    #display final results
    display(df)
    print(failed_car) 
      
main()