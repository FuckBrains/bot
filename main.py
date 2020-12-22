import os
os.system('python3 scrap.py')    
with open("requirements.txt","r") as f:
  for i in f.readlines():
    try:	
    	os.system(i)
    except:
		pass
# import os
import os
import nltk
import spacy
import nltk
origianl_direectory=os.getcwd()
try:
	os.mkdir("news")
except:
	pass
os.chdir(origianl_direectory+"/news/")
try:
	os.mkdir("video")
except:
	pass	
try:	
	os.mkdir("audio")
except:
	pass
try:
	os.mkdir("images")
except:
	pass	
try:	
	os.mkdir("csv")
except:
	pass
os.chdir(origianl_direectory)
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

import pandas as pd
database=pd.read_csv(origianl_direectory+'/youtube_last uploads/database.csv')
new_titles=[]
new_descriptions=[]
for i in range(len(titles)):
  if titles[i] not in database["title"]:
    # print(titles[i])
    new_titles.append(titles[i])
    new_descriptions.append(descriptions[i])
titles.clear()
descriptions.clear()
titles=new_titles
descriptions=new_descriptions

#comment end

#start
if len(titles)<=7:
    quit()

#end







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
    writer.writerow(["title", "description"])
    for k in range( len(titles)):
      writer.writerow([ titles[k],descriptions[k] ])


# #Remove old image
os.chdir(origianl_direectory+'/news/images') 

import os,shutil
try:
    for  i in os.listdir():
        os.remove(i)
except:
    pass
from bing_image_downloader import downloader
store_rename_image=[]
for head in titles:
  print(head)
  query_string=head#[0:20]
  downloader.download(query_string, limit=1,  output_dir='dataset', adult_filter_off=True, force_replace=False, timeout=60)
for  i in os.listdir(origianl_direectory+"/news/images/dataset/"):
    for j in os.listdir(origianl_direectory+"/news/images/dataset/"+i+"/"):
        os.chdir(origianl_direectory+"/news/images/dataset/"+i+"/")
        rename_image=i+".jpg"
        print(j)
        os.rename(j,rename_image)
        os.chdir(origianl_direectory+"/news/images/dataset/")
os.chdir(origianl_direectory+"/news/images/dataset/")
for  i in os.listdir(origianl_direectory+"/news/images/dataset/"):
    for j in os.listdir(origianl_direectory+"/news/images/dataset/"+i+"/"):
        os.chdir(origianl_direectory+"/news/images/dataset/"+i+"/")
        shutil.move(j,origianl_direectory+"/news/images/")
        os.chdir(origianl_direectory+"/news/images/dataset/")
for  i in os.listdir(origianl_direectory+"/news/images/dataset/"):
    os.rmdir(i)
os.chdir(origianl_direectory+"/news/images")    
os.rmdir("dataset")

#@title ##**Remove the damage images and contants** { display-mode: "form" }
os.system("clear")
#remove duplicate_data
print(len(titles))
print(len(descriptions))
if len(titles)==len(descriptions):
  data_store_dict={}
  for i in range(len(titles)):
    data_store_dict[titles[i]]=descriptions[i]
  u_titles=[]
  u_descriptions=[]
  for i,j in data_store_dict.items():
    u_titles.append(i)
    u_descriptions.append(j)
  titles.clear()
  descriptions.clear()
  titles=u_titles
  descriptions=u_descriptions  
  print(len(titles))
  print(len(descriptions))
# for i in range(len(titles)):
#   print(f"titles[{i}]:\n{titles[i]}\n")
#   print(f"descriptions[{i}]:\n{descriptions[i]}\n")
from PIL import Image
damage_file=[]
img_dir = origianl_direectory+"/news/images/"
for filename in os.listdir(img_dir):
  try:
    with Image.open(img_dir + "/" + filename) as im:
      # print('ok')
      pass
  except:
    print(img_dir + "/" + filename)
    damage_file.append(filename)
    os.remove(img_dir + "/" + filename)
    print(img_dir + "/" + filename)
    damge_path=img_dir + "/" + filename
damage_file_name=[]
for i in damage_file:
  temp=i.split(".jpg")
  damage_file_name.append(temp[0])
for i in damage_file_name:
  if i in data_store_dict.keys():
    del data_store_dict[i]
titles=[]
descriptions=[]
for i,j in data_store_dict.items():
  titles.append(i)
  descriptions.append(j)   


#now we resize images


#@title ##**Resize Images if can't delete the file from title and description** { display-mode: "form" }
# need_to_remove=[]
import cv2
from PIL import Image, ImageDraw, ImageFilter
image_folder = origianl_direectory+"/news/images/"
images = [img for img in os.listdir(image_folder) if img.endswith(".jpg")]
for i in range(len(images)):
  frame = cv2.imread(os.path.join(image_folder, images[i]))
  height, width, layers = frame.shape
  if height<=1000 and width<=1000:
    im1 = Image.open(origianl_direectory+'/youtube_news_scrap_tools/background.jpg')
    im2 = Image.open(images[i])
    back_im = im1.copy()
    back_im.paste(im2, (630,200))
    back_im.save(images[i], quality=100)
my_images=os.listdir()
for i in my_images:
    image = Image.open(i)
    new_image =image.resize((1920,1080))
    rgb_im = new_image.convert('RGB')
    rgb_im.save(i)


up_to=round(int(len(titles)/2))  
# @title ##**Create audio** { display-mode: "form" }
os.chdir(origianl_direectory+"/news/audio/")
try:
  for i in os.listdir():
    os.remove(i)
except:
  pass
from gtts import gTTS #Import Google Text to Speech
from IPython.display import Audio #Import Audio method from IPython's Display Class
import glob
from pydub import AudioSegment 
from pydub.playback import play 
import time
import cv2
def audio(story,f_name):
  tts = gTTS(text=story,lang='en',) #Provide the string to convert to speech
  save_file=f_name+".wav"
  tts.save(save_file) #save the string converted to speech as a .wav file
  sound_file = save_file
  Audio(sound_file, autoplay=True) 
for s in range( len(titles)):
  story=titles[s]+" "+descriptions[s]
  f_name=titles[s]
  audio(story,f_name)  


store_audio_duration=[]

store_path= os.listdir()
store_full_path=[]
for o in store_path:
  store_full_path.append(origianl_direectory+"/news/audio/"+o)
for j in store_full_path:
  file_path=j
  audio = AudioSegment.from_file(file_path)
  store_audio_duration.append(audio.duration_seconds)  

audio_path=origianl_direectory+"/news/audio/*.wav"
audios=glob.glob(audio_path)
store_path_for_iamge=glob.glob(audio_path)
wav_file_1 = AudioSegment.from_file(audios[0])  
for g in range(1,up_to):
   wav_file_2 = AudioSegment.from_file(audios[g]) 
   wav_file_1=wav_file_1+wav_file_2


wav_file_1.export(out_f = "wav_file_3.wav",format = "wav") 

new_wav_file_1 = AudioSegment.from_file(audios[up_to])  
for g in range(up_to+1,len(titles)):
   new_wav_file_2 = AudioSegment.from_file(audios[g]) 
   new_wav_file_1=new_wav_file_1+new_wav_file_2


new_wav_file_1.export(out_f = "new_wav_file_3.wav",format = "wav") 

#make video
os.chdir(origianl_direectory+"/news/video/")    
try:
  for i in os.listdir():
    os.remove(i)
except:
  pass
image_folder = origianl_direectory+"/news/images/"
video_name = 'video2.mp4'
img_list=[]

for i in store_path_for_iamge:
  img_list.append(str(i.split(".wav")[0]+".jpg").split("/")[-1])
each_image_duration = 5 # in secs
fourcc = cv2.VideoWriter_fourcc(*'mp4v') # define the video codec
images = [img for img in img_list if img.endswith(".jpg")]
frame = cv2.imread(os.path.join(image_folder, images[0]))
print(images)
height, width, layers = frame.shape
video = cv2.VideoWriter(video_name, fourcc, 1.0, (width, height))
for im in range(up_to):
  for i in range(round(store_audio_duration[im])):
      print("video2.mp4"+images[im])
      video.write(cv2.imread(os.path.join(image_folder, images[im])))
cv2.destroyAllWindows()
video.release()


#@title ##**Create video 2** { display-mode: "form" }
video_name = 'new_video2.mp4'
fourcc = cv2.VideoWriter_fourcc(*'mp4v') # define the video codec
video = cv2.VideoWriter(video_name, fourcc, 1.0, (width, height))
for im in range(up_to,len(titles)-1):
  for i in range(round(store_audio_duration[im])):
     print("new_video.mp4"+images[im])
     video.write(cv2.imread(os.path.join(image_folder, images[im])))
cv2.destroyAllWindows()
video.release()


f1 = open(origianl_direectory+'/youtube_last uploads/title_count1.csv', "r")
last_line =f1.readlines()[-1]
f1.close()
news_count=int(last_line[0])
news_count+=1


#@title ##**Create Intro 1 video** { display-mode: "form" }

import numpy as np
import cv2

image = cv2.imread(origianl_direectory+'/youtube_news_scrap_tools/intro.png',cv2.IMREAD_UNCHANGED)

position = ((int) (image.shape[1]/2 - 1000/2), (int) (image.shape[0]/2 - 36/2))
# position=(620,500)
title="Tech News Episode " +str(news_count)
cv2.putText(
     image, #numpy array on which text is written
     title, #text
     position, #position at which writing has to start
     cv2.FONT_HERSHEY_TRIPLEX, #font family
    3, #font size 209, 80, 0, 255  
     (0, 0, 0, 1), #font color
    4) #font stroke
cv2.imwrite('output.png', image)
import shutil
shutil.copy("output.png","thumb1.jpg")


image_folder = origianl_direectory+"/news/video/"
video_name = 'video1.mp4'
each_image_duration =8 # in secs
fourcc = cv2.VideoWriter_fourcc(*'mp4v') # define the video codec
images = [img for img in os.listdir(image_folder) if img.endswith(".png")]
frame = cv2.imread(os.path.join(image_folder, images[0]))
height, width, layers = frame.shape
video = cv2.VideoWriter(video_name, fourcc, 1.0, (width, height))
for im in range(len(images)):
  for i in range(each_image_duration):
      video.write(cv2.imread(os.path.join(image_folder, images[im])))
cv2.destroyAllWindows()
video.release()


#@title ##**Create Intro 2 video** { display-mode: "form" }

image = cv2.imread(origianl_direectory+'/youtube_news_scrap_tools/intro.png',cv2.IMREAD_UNCHANGED)

position = ((int) (image.shape[1]/2 - 1000/2), (int) (image.shape[0]/2 - 36/2))
# position=(620,500)
title="Tech News Episode " +str(news_count+1)
cv2.putText(
     image, #numpy array on which text is written
     title, #text
     position, #position at which writing has to start
     cv2.FONT_HERSHEY_TRIPLEX, #font family
    3, #font size 209, 80, 0, 255  
     (0, 0, 0, 1), #font color
    4) #font stroke
cv2.imwrite('output.png', image)
shutil.copy("output.png","thumb2.jpg")
image_folder = origianl_direectory+"/news/video/"
video_name = 'new_video1.mp4'
each_image_duration =8 # in secs
fourcc = cv2.VideoWriter_fourcc(*'mp4v') # define the video codec
images = [img for img in os.listdir(image_folder) if img.endswith(".png")]
frame = cv2.imread(os.path.join(image_folder, images[0]))
height, width, layers = frame.shape
video = cv2.VideoWriter(video_name, fourcc, 1.0, (width, height))
for im in range(len(images)):
  for i in range(each_image_duration):
      video.write(cv2.imread(os.path.join(image_folder, images[im])))
cv2.destroyAllWindows()
video.release()

#@title ##**add audio in intro1** { display-mode: "form" }
# from moviepy.editor import *
from moviepy.editor import *
videoclip = VideoFileClip(origianl_direectory+"/news/video/video1.mp4")
audioclip = AudioFileClip(origianl_direectory+"/youtube_news_scrap_tools/intro_audio.mp3")

new_audioclip = CompositeAudioClip([audioclip])
videoclip.audio = new_audioclip
videoclip.write_videofile("intro.mp4")

#@title ##**add audio in intro2** { display-mode: "form" }

videoclip = VideoFileClip(origianl_direectory+"/news/video/new_video1.mp4")
audioclip = AudioFileClip(origianl_direectory+"/youtube_news_scrap_tools/intro_audio.mp3")

new_audioclip = CompositeAudioClip([audioclip])
videoclip.audio = new_audioclip
videoclip.write_videofile("new_intro.mp4")



#@title ##**overlay music on news audio video1** { display-mode: "form" }

from pydub import AudioSegment
sound1 = AudioSegment.from_file(origianl_direectory+"/news/audio/wav_file_3.wav")
sound2 = AudioSegment.from_file(origianl_direectory+"/youtube_news_scrap_tools/youtube_music.mp3")
combined = sound1.overlay(sound2)
combined.export(origianl_direectory+"/news/audio/final.wav", format='wav')

#@title ##**overlay music on news audio video2** { display-mode: "form" }

from pydub import AudioSegment

sound1 = AudioSegment.from_file(origianl_direectory+"/news/audio/new_wav_file_3.wav")
sound2 = AudioSegment.from_file(origianl_direectory+"/youtube_news_scrap_tools/youtube_music.mp3")

combined = sound1.overlay(sound2)
combined.export(origianl_direectory+"/news/audio/new_final.wav", format='wav')

#@title ##**add main audio to the video1** { display-mode: "form" }

# from moviepy.editor import *
videoclip = VideoFileClip(origianl_direectory+"/news/video/video2.mp4")
audioclip = AudioFileClip(origianl_direectory+"/news/audio/final.wav")

new_audioclip = CompositeAudioClip([audioclip])
videoclip.audio = new_audioclip
videoclip.write_videofile("main.mp4")


#@title ##**add main audio to the video2** { display-mode: "form" }

# from moviepy.editor import *
videoclip = VideoFileClip(origianl_direectory+"/news/video/new_video2.mp4")
audioclip = AudioFileClip(origianl_direectory+"/news/audio/new_final.wav")

new_audioclip = CompositeAudioClip([audioclip])
videoclip.audio = new_audioclip
videoclip.write_videofile("new_main.mp4")



#@title ##**Make a .txt file which store all videos path** { display-mode: "form" }
shutil.copy(origianl_direectory+"/youtube_news_scrap_tools/outro_new.mp4",origianl_direectory+"/news/video/outro.mp4")
with open("list.txt","w") as f:
     f.write(f"file '{origianl_direectory}/news/video/intro1.mp4'\nfile '{origianl_direectory}/news/video/main1.mp4'\nfile '{origianl_direectory}/news/video/outro.mp4'"
)
with open("new_list.txt","w") as f:
    f.write(f"file '{origianl_direectory}/news/video/new_intro1.mp4'\nfile '{origianl_direectory}/news/video/new_main1.mp4'\nfile '{origianl_direectory}/news/video/outro.mp4'")

os.system("ffmpeg -i intro.mp4 -vf scale=1920:1080 intro1.mp4")
os.system("ffmpeg -i new_intro.mp4 -vf scale=1920:1080 new_intro1.mp4")
os.system("ffmpeg -i main.mp4 -vf scale=1920:1080 main1.mp4")
os.system("ffmpeg -i new_main.mp4 -vf scale=1920:1080 new_main1.mp4")
os.system("ffmpeg -f concat -safe 0 -i list.txt -c copy final_upload.mp4 ")
os.system("ffmpeg -f concat -safe 0 -i new_list.txt -c copy new_final_upload.mp4 ")
os.chdir(origianl_direectory+"/youtube_last uploads/")
try:
  os.remove("data.csv")
except:
    pass  
try:
  os.remove("thumb1.jpg")
except:
    pass
try:
  os.remove("thumb2.jpg")
except:
    pass
try:
  os.remove("video1.mp4")
except:
    pass
try:
  os.remove("video2.mp4")
except:
    pass
os.chdir(origianl_direectory+"/news/video/")
shutil.move(origianl_direectory+"/news/video/thumb1.jpg",origianl_direectory+"/youtube_last uploads/")
shutil.move(origianl_direectory+"/news/video/thumb2.jpg",origianl_direectory+"/youtube_last uploads/")
shutil.move(origianl_direectory+"/news/video/final_upload.mp4",origianl_direectory+"/youtube_last uploads/video1.mp4")
shutil.move(origianl_direectory+"/news/video/new_final_upload.mp4",origianl_direectory+"/youtube_last uploads/video2.mp4")
shutil.move(origianl_direectory+"/news/csv/data.csv",origianl_direectory+"/youtube_last uploads/")

#@title ##**Make tag, title, descriptions** { display-mode: "form" }
from rake_nltk import Rake
r = Rake()
#tag for video 1
mini_tag1=[]
tag1=[]
check1=0
for i in range(up_to):
  check1+=len(clean_title[i][:40])
  r.extract_keywords_from_text(clean_title[i][:50])
  key=r.get_ranked_phrases() 
  mini_tag1.append(key)
for i in mini_tag1:
  for j in i:
    if check1<=500:
      if len(j)>=15:
         tag1.append(j)      
if check1<=480:
  tag1.append("android iceland")


#tag for video 2
mini_tag2=[]
tag2=[]
check2=0
for i in range(up_to,len(titles)):
  check2+=len(clean_title[i][:40])
  r.extract_keywords_from_text(clean_title[i][:50])
  key=r.get_ranked_phrases() 
  mini_tag2.append(key)
for i in mini_tag2:
  for j in i:
    if check2<=500:
      if len(j)>=15:
         tag2.append(j)       
if check2<=470:
  tag2.append("android iceland")  


#title for video 1  
f1 = open(origianl_direectory+'/youtube_last uploads/title_count1.csv', "r")
last_line = f1.readlines()[-1]
f1.close()
new=int(last_line[0])
ti_1="Tech News #"+str(new+1)
ti_2="Tech News #"+str(new+2)


tit_len1=0
for i in tag1:
  tit_len1+=len(i)
  if tit_len1<=80:
    ti_1=ti_1+","+i

#title for video 1  
tit_len2=0
for i in tag2:
  tit_len2+=len(i)
  if tit_len2<=80:
    ti_2=ti_2+","+i


#descriptions
description_for_upload="DISCLAIMER::\nThis Channel DOES NOT Promote or encourage Any illegal activities,all contents provided by This Channel is meant for EDUCATIONAL PURPOSE only, this video is made for 'fair use' for purposes such as criticism, comment, news re- porting, teaching, scholarship,and research, this video is Non-profit, educational or personal use and fair use.\n\n'Subscribe 'Android Iceland':: \nhttps://www.youtube.com/channel/UC0Jp1opulANvXKgrcev755A?sub_confirmation=1 \n\nLike this video and Subscribe 'Android Iceland'\n \nAbout ::\nAndroid Iceland is a YouTube channel, where you will find technical video's mostly based on android , coding and some personal blogs."


with open ("tag_title(1).txt","w") as f:
  f.write( ti_1 +"\n\n")
  f.write(description_for_upload+"\n\n")
  for i in tag1:
    f.write(i+",")   


with open ("tag_title(2).txt","w") as f:
  f.write( ti_2 +"\n\n")
  f.write(description_for_upload+"\n\n")
  for i in tag2:
    f.write(i+",")   

#Update new count file by 2
with open(origianl_direectory+'/youtube_last uploads/title_count1.csv','w') as file:
    writer = csv.writer(file)
    writer.writerow([new+2])     
os.chdir(origianl_direectory+'/youtube_last uploads/')
#@title ##**Store title and description in database** { display-mode: "form" }

import pandas as pd
all_filenames = [origianl_direectory+"/youtube_last uploads/database.csv",origianl_direectory+"/youtube_last uploads/data.csv"]
#combine all files in the list
combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames ])
#export to csv
combined_csv.to_csv( origianl_direectory+"/youtube_last uploads/database.csv", index=False, encoding='utf-8-sig')
os.remove(origianl_direectory+"/youtube_last uploads/data.csv")

#last count number
f1 = open(origianl_direectory+'/youtube_last uploads/title_count1.csv', "r")
last_line = f1.readlines()[-1]
f1.close()
news_count=int(last_line[0])  
print(news_count)


#reset the count
# news_count_change = "2" 

# change=int(news_count_change)
# with open(origianl_direectory+'/youtube_last uploads/title_count1.csv', 'w', newline='') as file:
#     writer = csv.writer(file)
#     writer.writerow([change])
# f1 = open('/content/gdrive/My Drive/youtube_last uploads/title_count1.csv', "r")
# last_line = f1.readlines()[-1]
# f1.close()
# news_count=int(last_line[0])  
# print("reset news count at ",news_count)

with open ("tag_title(1).txt","w") as f:
  f.write( ti_1 +"\n \n")
  f.write(description_for_upload+"\n\n")
  for i in tag1:
    f.write(i+",")  
with open ("tag_title(2).txt","w") as f:
  f.write( ti_2 +"\n \n")
  f.write(description_for_upload+"\n \n")
  for i in tag2:
    f.write(i+",")  
