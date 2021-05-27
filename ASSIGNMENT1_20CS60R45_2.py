from bs4 import BeautifulSoup
import os
import glob
import pickle



def getdate(str):
    months = ["January" , "February" , "March" , "April" , "May" , "June" , "July" , "August" , "September" , "October" , "November" , "December"]
    index=0
    for i in range(12):
        if str.find(months[i])>0:
            index=str.find(months[i])
            break

    date = str[index:-12]

    return date

def getparticipants(ptags):
    flag=1
    participants=[]
    i=1
    while flag:
        try:
            string = ptags[i].get_text()
        except:
            return -1 , participants

        i=i+1
        if string=="Company Participants " or string=="Conference Call Participants " or string=="Executives" or string=="Analysts":
            continue

        for j in range(len(participants)):
            if participants[j].find(string)>=0:
                flag=0
        
        if flag : 
            participants.append(string)
    
    return i , participants

def get_speaker_dict(index , participants , ptags):

    for p in range(len(participants)):
        h = participants[p].find('-')
        participants[p] = participants[p][0:h-1] 
        
    i=index
    flag=1
    cont=1
    dicti = {}
    presentspeaker=-1
    speakerstring=""
    string=ptags[index].get_text()

    for j in range(len(participants)):
            if participants[j].find(string)>=0:
                presentspeaker=j
                break

    i=i+1
    while flag:

        try:
            string = ptags[i].get_text()
        except:
            return -1 , dicti

        if string.find("Question-and-Answer")>=0:
            if participants[presentspeaker] not in dicti.keys():
                    tempdict = {participants[presentspeaker] : [speakerstring]}
                    dicti.update(tempdict)
            else:
                dicti[participants[presentspeaker]].append(speakerstring)
            flag=0
            index = i
            continue

            
        cont=1
        for j in range(len(participants)):
            if participants[j].find(string)>=0:
                if participants[presentspeaker] not in dicti.keys():
                    tempdict = {participants[presentspeaker] : [speakerstring]}
                    dicti.update(tempdict)
                else :
                    dicti[participants[presentspeaker]].append(speakerstring)
                presentspeaker=j
                speakerstring=""
                cont=0
                break

        if cont:        
            speakerstring += " " + string

        i=i+1
    
    return index , dicti

def get_QandA(index , ptags , participants):
    for p in range(len(participants)):
        h = participants[p].find('-')
        participants[p] = participants[p][0:h-1] 

    i = index + 1
    dicti = {}
    try:
        speaker = ptags[i].get_text()[4:-1]
    except:
        return -1 , dicti
    flag=1
    strflag=1
    num=1
    i=i+1
    speakerstr = ""
    while flag:

        strflag=1
        if(len(ptags)==i): 
            ques = {"Speaker" : speaker , "Remark" : speakerstr}
            dicti.update({num : ques})
            flag=0
            break

        for k in range(len(participants)):
            if participants[k].find(ptags[i].get_text()) >= 0 :
                ques = {"Speaker" : speaker , "Remark" : speakerstr}
                dicti.update({num : ques})
                speaker = participants[k]
                num = num + 1
                speakerstr = ""
                strflag=0
                break

        if strflag:
            speakerstr = speakerstr +" " + ptags[i].get_text()
        
        i = i + 1
    
    return 1 , dicti


path_orig = os.getcwd()
os.mkdir('ECTText')
path = path_orig + "/ECT"
os.chdir(path)
ECTText = {}
num=0

FileNames = [file for file in glob.glob("*.html")]
FileNames.sort()

for file in FileNames:
    print(file)
    dictionary ={}
    text = ""
    htmlfile = open(file)
    soup = BeautifulSoup(htmlfile, features="html.parser")
    ptags = soup.findAll("p")
    string = ptags[0].get_text()
    date = getdate(string)
    dictionary.update({"Date" : date})
    text = text + " " + "date "+date.lower()
    talkindex , participants = getparticipants(ptags)
    if talkindex == -1 :
        num = num + 1
        continue
    text = text + " " + "participants"
    for speaker in participants:
        text = text + " " + speaker.lower()
    dictionary.update({"Participants" : participants})
    sindex , speakerdict = get_speaker_dict(talkindex-1 , participants , ptags)
    if sindex == -1 :
        num = num + 1
        continue
    text = text + " " + "presentation"
    for speaker in speakerdict.keys():
        text = text + " " + speaker.lower() 
        for s in range(len(speakerdict[speaker])):
            text = text + " " + speakerdict[speaker][s].lower().replace("/" , " ").replace("www." , "").replace(".com" , "").replace("-" , " ")
    dictionary.update({"Presentation" : speakerdict})
    qindex , Questionnaire = get_QandA(sindex , ptags , participants)
    if qindex == -1 :
        num = num + 1
        continue
    text = text + " " + "questionnaire"
    for question in Questionnaire:
        text = text + " " + str(question)
        text = text + " " + "speaker" + " " + Questionnaire[question]["Speaker"].lower().replace("/" , " ").replace("www." , "").replace(".com" , "").replace("-" , " ") + " " + "remark" + " " +Questionnaire[question]["Remark"].lower().replace("/" , " ").replace("www." , "").replace(".com" , "").replace("-" , " ")
    dictionary.update({"Questionnaire" : Questionnaire})
    
    
    with open(path_orig + "/ECTText/" + str(num) + ".txt" , 'w', encoding='utf-8') as element:
            element.write(text)
    
    ECTText.update({num : dictionary})
    num = num + 1


os.chdir(path_orig)
picklefile = open('ECTNestedDict.pkl', 'wb')
pickle.dump(ECTText, picklefile)
picklefile.close()
