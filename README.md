# Phishing URL Classification

Malicious Web sites are a cornerstone of Internet criminal activities.
These Web sites contain various unwanted content such as spam-advertised products, phishing sites, dangerous "drive-by"
harness that infect a visitor's system with malware. The most influential approaches to the malicious
URL problem are manually constructed lists in which all malicious web page`s URLs are listed, as
well as users systems that analyze the content or behavior of a Web site as it is visited.

The disadvantage of _Blacklisting_ approach is that we have to do the tedious task of searching the list for
presence of the entry. And the list can be very large considering the amount of web sites on the Internet.
Also the list cannot be kept upto date because of the evergrowing growth of web link each and every hour.

In the given System we are using **Machine-Learning** techniques to classify a URL as either **Safe** or **Unsafe** in _Real Time_ without even the need to download the webpage.

Algorithms we are using in this system are :

*	[Random Forest] (https://en.wikipedia.org/wiki/Random_forest)
*	[Logistic Regression] (https://en.wikipedia.org/wiki/Logistic_regression)
*	[Decision Trees] (https://en.wikipedia.org/wiki/Decision+Trees)
* [Gradiant Boosting]

The system is presently working only on **Lexical** features(Simple text features of a URL) which includes:

*	Length of URL
*	Domain Length
*	Presence of Ip Address in Host Name
*	Presence of Security Sensitive Words in URL

and many more(around 22 total). The Host Based Features like country code in which site is hosted, creation date, updation date etc. are still yet to be added to the system and increase accuracy of the classifier but increase the _Latency time_ in classifying the URL as we have to query **WHOIS** servers in order to come up with the Host Based Features.
For this query purpose the **PyWhois** module has been used.

##  About Dataset
For this given system we are using two sources to collect our data,namely:

####  Phishtank.com
For the phishing/malicious URLs we are collecting data from [Phishtank] (https://www.phishtank.com/).
