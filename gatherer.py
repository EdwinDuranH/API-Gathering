#Database Creation Using API
#Import Libraries
import time
import requests
import pandas as pd

#Define a list of relevant variables to automatize information acquisition
relevant_vars = ["year","ocid","date","region","title","description","method","suppliers","buyer","amount"\
                 ,"budget"]

#Access to API's data
#API number 1: "Búsqueda de procesos de contratación por medio de palabra"

#Need an initial response to start while loop
def firstResponse():
    url_t = "https://datosabiertos.compraspublicas.gob.ec/PLATAFORMA/api/search_ocds"
    payload = {"year":"2015","page":"2"}
    r = requests.get(url_t,params = payload)
    return r

#Individual information saver.
def infoSave(variables,response,item):
    temp = []
    for i in variables:
        i = response["data"][item][str(i)]
        temp.append(i)   
    return temp 

#Information gatherer
def infoGet(yr,url,varlist,obs=0,page=0):
    start = time.time()
    rp = firstResponse().json()
    observations = 0
    page_count = page
    debug_count = 0
    #Creation of empty Pandas Dataframe to save all the pertinent information from the database.
    data_collected = pd.DataFrame(columns = varlist)
    #If no observations parameter is set, automatically gather all available data for that year.
    #Make all the API calls for the specific year (each page represents a call)
    
    #Also, only run the code if and only if the response from the API is equal to 200.
    while rp["pages"] - rp["page"] > 1:
    #If we try to scrape all the data without giving the API some time it will eventually
    #block access to it, which will raise an error for some unspecified amount of time. The
    #try except statement allows the script to wait some time in case the error is raised, and
    #start over the iteration as soon as access is regained.
        try:
            if obs == 0:
                pass
            elif observations >= obs:
                break
            #API Call that contains the relevant information.
            page_count = page_count + 1
            url_n = url 
            payload = {"page":str(page_count),"year":str(yr)}
            #DEBUG
            #print(payload)
            r = requests.get(url_n,params=payload)
            rp = r.json()

            #Now that the call has been made, save this information in many variables.
            for item in range(len(rp["data"])):
                #DEBUG
                #print(f"iteration number: {item}")
                observations = observations + 1
                #Store the information in a pandas dataframe.
                b = infoSave(varlist,rp,item) #List containing the values of the variables
                c = dict(zip(varlist,b)) #create a dict using the relevant_variables as key and b as their vaulues
                #After storing the information in the variables, append it to the pandas dataframe
                data_collected = data_collected.append(c,ignore_index=True)
                #DEBUG
                #print(f"Number of observations so far is: {observations}")
                if obs == observations:
                    break
        except:
            #DEBUG
            print("Too many requests. Waiting for API to grant access again...")
            time.sleep(10)
            page_count = page_count - 1
    end = time.time()
    print(f"Success! Total iteration time:{end-start}")
    return data_collected
