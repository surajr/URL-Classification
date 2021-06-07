# -*- coding: utf-8 -*-
"""
Created on Sun May 30 21:40:37 2021

@author: debanjan
"""


from flask import Flask, render_template, request
import sklearn.ensemble as ek
import ipaddress as ip
import pandas as pd
from os.path import splitext
import tldextract
from urllib.parse import urlparse
from joblib import load
from sklearn import svm,tree
import pickle

app = Flask(__name__)
app.config['SECRET_KEY']='debanjan';


@app.route("/")

def home():
    return render_template("index.html")

Suspicious_TLD=['zip','cricket','link','work','party','gq','kim','country','science','tk']
Suspicious_Domain=['luckytime.co.kr','mattfoll.eu.interia.pl','trafficholder.com','dl.baixaki.com.br','bembed.redtube.comr','tags.expo9.exponential.com','deepspacer.com','funad.co.kr','trafficconverter.biz']
def countdots(url):  
    return url.count('.')

def countdelim(url):
    count = 0
    delim=[';','_','?','=','&']
    for each in url:
        if each in delim:
            count = count + 1
    
    return count

def isip(uri):
    try:
        if ip.ip_address(uri):
            return 1
    except:
        return 0
    
def isPresentHyphen(url):
    return url.count('-')

def isPresentAt(url):
    return url.count('@')

def isPresentDSlash(url):
    return url.count('//')

def countSubDir(url):
    return url.count('/')
def get_ext(url):
    """Return the filename extension from url, or ''."""
    
    root, ext = splitext(url)
    return ext
def countSubDomain(subdomain):
    if not subdomain:
        return 0
    else:
        return len(subdomain.split('.'))
def countQueries(query):
    if not query:
        return 0
    else:
        return len(query.split('&'))
featureSet = pd.DataFrame(columns=('url','no of dots','presence of hyphen','len of url','presence of at',\
'presence of double slash','no of subdir','no of subdomain','len of domain','no of queries','is IP','presence of Suspicious_TLD',\
'presence of suspicious domain','label'))
    

def getFeatures(url, label): 
    result = []
    url = str(url)
    
    #add the url to feature set
    result.append(url)
    
    #parse the URL and extract the domain information
    path = urlparse(url)
    ext = tldextract.extract(url)
    
    #counting number of dots in subdomain    
    result.append(countdots(ext.subdomain))
    
    #checking hyphen in domain   
    result.append(isPresentHyphen(path.netloc))
    
    #length of URL    
    result.append(len(url))
    
    #checking @ in the url    
    result.append(isPresentAt(path.netloc))
    
    #checking presence of double slash    
    result.append(isPresentDSlash(path.path))
    
    #Count number of subdir    
    result.append(countSubDir(path.path))
    
    #number of sub domain    
    result.append(countSubDomain(ext.subdomain))
    
    #length of domain name    
    result.append(len(path.netloc))
    
    #count number of queries    
    result.append(len(path.query))
    
    #Adding domain information
    
    #if IP address is being used as a URL     
    result.append(isip(ext.domain))
    
    #presence of Suspicious_TLD
    result.append(1 if ext.suffix in Suspicious_TLD else 0)
    
    #presence of suspicious domain
    result.append(1 if '.'.join(ext[1:]) in Suspicious_Domain else 0 )
   #result.append(get_ext(path.path))
    result.append(str(label))
    return result    



@app.route('/model', methods=['GET','POST'])
def model():
    url = request.form['search']
    result = pd.DataFrame(columns=('url','no of dots','presence of hyphen','len of url','presence of at',\
    'presence of double slash','no of subdir','no of subdomain','len of domain','no of queries','is IP','presence of Suspicious_TLD',\
    'presence of suspicious domain','label'))
    
    results = getFeatures(url, '0')
    
    model_1=pickle.load(open('model_colab.pkl','rb'))
    #model_1=load('model.joblib')
    result.loc[0] = results
    result = result.drop(['url','label'],axis=1).values
    pos=0
    neg=0
    pred=model_1.predict(result)
    if(pred=='0'):    
        neg=neg+1
    if(pred=='1'):
        pos=pos+1

    if(pos>neg):    
        res="URL seems to be safe"
    else:
        res="URL seems to be not safe"    
    
    return render_template("index.html",Result=res)
    
if __name__ == "__main__":
    
    
    app.run()