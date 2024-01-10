from pymongo import MongoClient 
import numpy as np
from bson import ObjectId
from datetime import datetime
from flask import Flask, jsonify,request
from bson.json_util import dumps
import cv2
import requests
import os


app = Flask(__name__)

# Your connection details
connection_string = r'mongodb://aromongo:%40r0dek%40412@mongodb.arodek.com:27017/?authMechanism=DEFAULT'
database_name = r'Cogniquest'
#users_collection = r'users'

#Naming Test(Q3)
def naming_test(answer_new):
    value = [string.lower() for string in answer_new]
    list_1=[]
    list_2=[]
    list_3=[]
    j = 0
    result_dict={}
    text = ["lion", "camel", ["rhinoceros", "rhino"]]
 
    for index, i in enumerate(value):
        if isinstance(text[index], list):
            if i in text[index]:
                list_1.append(i)
                list_2.append(index)
            else:
                list_3.append("not in list")
        else:
            if i == text[index]:
                list_1.append(i)
                list_2.append(index)
            else:
                list_3.append("not in list")
    try:
        for i in range(len(list_2)):
            result_dict[list_2[i]] = list_1[i]
        for i in result_dict.keys():
            if isinstance(text[i], list):  
                if value[i] in text[i]:
                    j += 1
            elif value[i] == text[i]:
                j += 1
        score_3 = j
        return score_3
    except TypeError:
        return 0 

#Attention Test(Q4)
def attention_test(answer_new):
    value = [answer_new[key] for key in answer_new]
    j=0
    text=['2159836','253407']
    for i,(val, txt) in enumerate(zip(value, text)):
        if val == txt:
            j += 1
    score_4=j
    return score_4

#Language Test(Q5)
def language_test(answer_new):
    value_answer=answer_new.split(',' ' ')
    value = [word.lower() for word in value_answer]
    text = ['cab', 'can', 'cub', 'cot', 'cow', 'cry', 'care', 'crow', 'chair', 'charm', 'chore', 'choir', 'chamber', 'charity', 'clove', 'cloud', 'centre', 'convent', 'concern', 'covenant', 'caricature', 'character', 'courage', 'counterpart', 'catch', 'cover', 'clone', 'cut', 'cast', 'crave', 'cite', 'cede', 'climb', 'close', 'chirp', 'colour','come', 'cave', 'cheer', 'count', 'crack', 'certify', 'comfort', 'crumble', 'challenge', 'characterise', 'cute', 'calm', 'clean', 'correct', 'cunning', 'conducive', 'courageous', 'charitable', 'canned', 'careful', 'careless', 'carefree', 'crumbled', 'closed', 'crunchy', 'creepy', 'critical', 'covered', 'colourful', 'concerned', 'chapped', 'clouded', 'cheerful', 'call', 'class', 'clutter', 'chatter', 'classy', 'cone', 'case', 'cupboard', 'conceive', 'cubicle', 'clad', 'clueless', 'cobweb', 'cope', 'cease', 'cleft', 'cracker', 'cough', 'cost', 'chandelier', 'cat', 'camel', 'coupon', 'clear', 'cloudy', 'caring', 'creative', 'clumsy', 'comfortable', 'clock', 'computer', 'cap', 'candy', 'cotton', 'captain', 'camera', 'coal', 'cucumber', 'cottage', 'chalk', 'car', 'curd', 'cart', 'card', 'cabin', 'cabinet', 'cock', 'cake', 'cashew', 'chocolate', 'comb', 'candle', 'crocodile', 'cross', 'christmas', 'cluster', 'cup', 'coin']
    common_words = set(value) & set(text)
    if len(common_words)>=11:
        score_5=1
    else:
        score_5=0
    return score_5

#Abstraction Test(Q6)
def abstraction_test(answer_new):
    j=0
    value = answer_new.lower()
    new_value=[letter.replace(" " ,"_") for letter in value]
    my_lst_str = ''.join(map(str, new_value))
    text = ["vehicle","vehicle_","used_for_transportation","transport_","transport_vehicle"]

    if my_lst_str in [item for item in text]:
        j +=1
    else:
        j=j

    if j==1:
        score6=1
    else:
        score6=0
    return score6

#Delayed Recall Test(Q7)
def delayed_recall_test(answer_new):
    value = [string.lower().strip() for string in answer_new]
    list_1 = []
    list_2 = []
    list_3 = []
    j = 0
    result_dict = {}
    text = ["banana", "milk", "deer"]

    for index, i in enumerate(value):
        if i in text:
            list_1.append(i)
            list_2.append(index)
        else:
            list_3.append("not in list")

    try:
        for i in range(len(list_2)):
            result_dict[list_2[i]] = list_1[i]
        for i in result_dict.keys():
            if value[i] == text[i]:
                j += 1
        score7 = j
        return score7
    except TypeError:
        return 0
    
def image_intensity(test_id,collection):
    intial_score=0
    try:
        file_path = collection.find_one({'testId': ObjectId('659d26dbf4483fd92fa766e5')})['filesPath']
        image_path=f'https://cogniquest.arodek.com/{file_path}'
        response = requests.get(image_path)
        #image_data = BytesIO(response.content)
        image_data = np.frombuffer(response.content, dtype=np.uint8)
        cv_image = cv2.imdecode(image_data, cv2.IMREAD_COLOR)
        average_intensity = cv_image.mean()
        if average_intensity > 0:
            score=intial_score+1
        else:
            score=intial_score
        return score
    except Exception as e:
        return intial_score

def get_result(useid:str,testid:str):
    global connection_string,database_name
    info_dict={'collection_name_3': r'qcollection2',
                'collection_name_4': r'qcollection4',
                'collection_name_5':r'qcollection5',
                'collection_name_6': r'qcollection6',
                'collection_name_7': r'qcollection7',
                'collection_name_1': r'qcollection1',
                'user':r'users',
                'Result':r'Result_Display',
                'userId':useid,
                'testId':testid}
    keys_to_exclude = ['userId', 'user','Result','testId','collection_name_1']
    original_score=0
    filtered_values = [value for key, value in info_dict.items() if key not in keys_to_exclude]
    object_id_user=ObjectId(info_dict['userId'])
    object_id=ObjectId(info_dict['testId'])
    client = MongoClient(connection_string)  
    db = client.get_database(database_name)
    age = db[info_dict['user']].find_one({'_id': object_id_user})['age']
    end_time=db[info_dict['collection_name_7']].find_one({"testId": object_id})['testTime']
    score_6=image_intensity(testid,db[info_dict['collection_name_1']])
    #score calculation
    collection_name = [db[collection] for collection in filtered_values]
    for i in collection_name:
        try:
            result_test =i.find_one({'testId':object_id})['testData']
            try:
                score_1=delayed_recall_test(result_test)
            except:
                score_1=0
            try:
                score_2=abstraction_test(result_test)
            except:
                score_2=0
            try:
                score_3=language_test(result_test)
            except:
                score_3=0
            try:
                score_4=attention_test(result_test)
            except:
                score_4=0
            try:
                score_5=naming_test(result_test)
            except:
                score_5=0
            overall_score=max(score_1,score_2,score_3,score_4,score_5,score_6)
            original_score=overall_score+original_score
        except:
            print("ERROR")
    user_report={ 
    'user_id':ObjectId(useid),
    'test_id':ObjectId(testid),
    'age':age,
    'MOCA_Score':original_score,
    'Accuracy':0,
    'Speed':0,
    'ICA_Index':1,
    'timestamp':datetime.now().strftime("%Y-%m-%d %H")
    }
    
    db[info_dict['Result']].insert_one(user_report)
    client.close()
    #print(age)
    return dumps(user_report)


@app.route('/result/<string:user_id>/<string:test_id>', methods=['GET'])
def get_result_by_test_id(user_id,test_id):
    list_inputs =[user_id,test_id]
    if user_id and test_id not in list_inputs:
        return jsonify({'error': '404 User not found'})
    else:
        try:
            return get_result(user_id,test_id)
        except TypeError as e:
            return jsonify({"error": 'data_missing'})
        except KeyError :
            return jsonify({"error": 'key_error'})



if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
