import os
# os.system('python3 scrap.py')    
# with open("requirements.txt","r") as f:
#   for i in f.readlines():
#     os.system(i)
import os
import os
import nltk
import spacy
import nltk
origianl_direectory=os.getcwd()
with open("titles.txt","r") as f:
  titl_backup=f.readlines()    
titl_backup=str(titl_backup).split("^^^^")  
del titl_backup[0]
with open("descriptions.txt","r") as f:
  des_backup=f.readlines()    
des_backup=str(des_backup).split("^^^^")  
del des_backup[0]
titles=[]
descriptions=[]
titles=titl_backup
titles[-1].replace("]","").split('"')[0]
descriptions=des_backup
descriptions[-1].replace("]","").split('"')[0]


if  len(titles)==len(descriptions):
  print("Welcome bro!")
bad_punc=["#","!","/","’","‘",'"',"[","]","\\n",'"]',",","'"]
clean_titles=[]
for i in titles:
  for j in bad_punc:
    if j in i:
      i=i.replace(j,"")
  clean_titles.append(i.lower().lstrip("\n").rstrip("\n").rstrip(" ").lstrip(" "))
titles=[] 
titles=clean_titles 

bad_punc_des=["#","!","’",'"',"[","]","\\n",'"]',"'"]
clean_descriptions=[]
for i in descriptions:
  for j in bad_punc_des:
    if j in i:
      i=i.replace(j,"")
  clean_descriptions.append(i.lower().lstrip("\n").rstrip("\n").rstrip(" ").lstrip(" ").replace("/",""))
descriptions=[]
descriptions=clean_descriptions


#remove duplicate_data
dupli={}
for i in range(len(titles)):
  dupli[titles[i]]=descriptions[i]
u_titles=[]
u_descriptions=[]
for i,j in dupli.items():
  u_titles.append(i)
  u_descriptions.append(j)
titles.clear()
descriptions.clear()
titles=u_titles
descriptions=u_descriptions  
print(len(titles))
print(len(descriptions))


webname=["verges","verge","cnet","https://gadgets.ndtv.com/","https://www.cnet.com/","https://www.theverge.com/","theverge"]
dic_values=[]
dic_values=[i for i in dupli.keys()]
for i in dic_values :
  for j in webname:
    if j in i:
    #   print(i)
      try:
        del dupli[i]
      except:
        pass

def get_key(val):
	for key, value in dupli.items():
		if val == value:
			return key

	return "key doesn't exist"

for i in [i for i in dupli.values()]:
  for j in webname:
    # print(j)
    if j in i:
      # print(i)
      try:
        del dupli[get_key(i)]
      except:
        pass

remove_links=[".com","https","pic.twitter"]
for i in [i for i in dupli.values()]:
 for j in i.split(" "):
   for k in remove_links:
     if k in j:
    #    print(i)
       try:
        del dupli[get_key(i)]
       except:
        pass
titles=[]        
descriptions=[]
for i,j in  dupli.items():
    titles.append(i)
    descriptions.append(j)
print(len(titles))    
print(len(descriptions))

#comment start

# import pandas as pd
# database=pd.read_csv(origianl_direectory+'/youtube_last uploads/database.csv')
# new_titles=[]
# new_descriptions=[]
# for i in range(len(titles)):
#   if titles[i] not in database["title"]:
#     print(titles[i])
#     new_titles.append(titles[i])
#     new_descriptions.append(descriptions[i])
# titles.clear()
# descriptions.clear()
# titles=new_titles
# descriptions=new_descriptions


#comment end



#clean news
import spacy
clean_title=[]
for i in titles:
  word=""
  sentence  = i
  tokenizer = nltk.RegexpTokenizer(r"\w+")
  new_words = tokenizer.tokenize(sentence)
  for k in new_words:
    word+=k+" "
  clean_title.append(word.lower())
my_tt=""
for i in clean_title:
  i=i.lower()
  i=i.replace(",","")
  my_tt+=i+"."
# import spacy
from spacy.lang.en.stop_words import  STOP_WORDS
from string import punctuation
stopwards=list(STOP_WORDS)
nlp=spacy.load("en_core_web_sm")
doc=nlp(my_tt)
tokens=[token.text for token in doc]
word_frequencies={}
for word in doc:
  if word.text.lower() not in stopwards:
    if word.text.lower() not in punctuation:
      if word.text not in word_frequencies.keys():
        word_frequencies[word.text]=1
      else:
        word_frequencies[word.text]+=1
max_frequency=max(word_frequencies.values())
for word in word_frequencies.keys():
  word_frequencies[word]= word_frequencies[word]/max_frequency
sentence_tokens=clean_title
sentence_scores={}
for sent in sentence_tokens:
  for word in sent:
    if word.lower() in word_frequencies.keys():
      if sent not in sentence_scores.keys():
        sentence_scores[sent]=word_frequencies[word.lower()]
      else:
        sentence_scores[sent]+=word_frequencies[word.lower()]
sentence_scores_clean = {}
for key,value in sentence_scores.items():
    if value not in sentence_scores_clean.values():
        sentence_scores_clean[key] = value        
from heapq import nlargest
select_length=int(len(sentence_tokens)*0.4)                  
summary=nlargest(select_length,sentence_scores_clean,key=sentence_scores_clean.get)

important_titles=[]
important_descriptions=[]
for i in range(len(clean_title)):
  if clean_title[i] in summary:
    important_titles.append(titles[i])
    important_descriptions.append(descriptions[i])
titles.clear()
descriptions.clear()    
titles=important_titles
descriptions=important_descriptions   

print(len(titles))
print(len(descriptions))

os.chdir(origianl_direectory+'/news/csv/')
open('data.csv', 'w').close() 
import csv
with open('data.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    # writer.writerow(["title", "description"])
    for k in range( len(titles)):
      writer.writerow([ titles[k],descriptions[k] ])
import shutil      

shutil.copy(origianl_direectory+"/news/csv/data.csv",origianl_direectory+"/youtube_last uploads/")
os.chdir(origianl_direectory+"/youtube_last uploads/")
os.remove("data.csv")
import pandas as pd
all_filenames = [origianl_direectory+"/youtube_last uploads/database.csv",origianl_direectory+"/youtube_last uploads/data.csv"]
#combine all files in the list
combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames ])
#export to csv
combined_csv.to_csv( origianl_direectory+"/youtube_last uploads/database.csv", index=False, encoding='utf-8-sig')
# os.remove(origianl_direectory+"/youtube_last uploads/data.csv")


