import requests
from bs4 import BeautifulSoup
result=requests.get("https://gadgets.ndtv.com/android/news")
src=result.content
soup=BeautifulSoup(src,"lxml")
descriptions = []
titles=[]
urls=[]
for caption_box in soup.find_all(class_="caption_box"):
  a_tag= caption_box.find("a")
  urls.append(a_tag.attrs["href"])
for url in urls:
  re=requests.get(url)
  sr=re.content
  soop=BeautifulSoup(sr,"lxml")
  for h1_tag in soop.find_all("h1"):
    titles.append(h1_tag.text)
  for des in soop.findAll("div", {"class": "content_text row description"}):
    descriptions.append(des.find('p').text)



#@title ##**Find news the verge** { display-mode: "form" }

result1=requests.get("https://www.theverge.com/tech")
src1=result1.content
soup1=BeautifulSoup(src1,"lxml")
urls1=[]
titles1=[]
store_u=[]
for caption_box in soup1.find_all(class_="c-entry-box--compact__body"):
  a_tag= caption_box.find("a")
  store_u.append(a_tag)
for url in store_u:
  urls1.append(url.attrs["href"])
  titles1.append(url.text)  
if 'https://www.theverge.com/circuitbreaker' in urls1:
  urls1.remove('https://www.theverge.com/circuitbreaker')
if '\nCircuit Breaker\n'in titles1:
  titles1.remove('\nCircuit Breaker\n')  
from newspaper import Article
import nltk
nltk.download('punkt')
descriptions1=[]
for i in urls1:
  article = Article(i)
  article.download()
  article.parse()
  article.nlp()
  descriptions1.append(article.summary)
titles.extend(titles1)  
descriptions.extend(descriptions1)  
# clear_output()



#@title ##**Find news from cnet.com** { display-mode: "form" }

urls2=[]
titles2=[]
store_u2=[]
u="https://www.cnet.com/news"
result2=requests.get(u)
src2=result2.content
soup2=BeautifulSoup(src2,"lxml")
for caption_box in soup2.find_all(class_="col-5 assetText"):
  a_tag= caption_box.find("a")
  store_u2.append(a_tag)
for url in store_u2:
  urls2.append("https://www.cnet.com"+url.attrs["href"])
  titles2.append(url.text.strip())    
for i in range(2,4): 
  visit=u+str(i)
  result2=requests.get(visit)
  src2=result2.content
  soup2=BeautifulSoup(src2,"lxml")
  for caption_box in soup2.find_all(class_="col-5 assetText"):
    a_tag= caption_box.find("a")
    store_u2.append(a_tag)
  for url in store_u2:
    urls2.append("https://www.cnet.com"+url.attrs["href"])
    titles2.append(url.text.strip())   
descriptions2=[]
for i in urls2:
  article = Article(i)
  article.download()
  article.parse()
  article.nlp()
  descriptions2.append(article.summary)
titles.extend(titles2)  
descriptions.extend(descriptions2)

backup_t=titles
backup_d=descriptions





# print(urls)  
# %cd /content
open('titles.txt', 'w').close() 
open('descriptions.txt', 'w').close()
with open("titles.txt","w") as f:
  for i in titles:
    i="^^^^"+i
    # print(i)
    f.write(i)

with open("descriptions.txt","w") as f:
  for i in descriptions:
    i="^^^^"+i
    # print(i)
    f.write(i)
