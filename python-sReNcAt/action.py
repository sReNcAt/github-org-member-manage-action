import requests
import yaml
import os
import sys

token = 'enter user token'

def f_put_collaborators(owner,repos,user_name,permission):
    payload = '{"permission":"'+permission+'"}'
    header = {'Authorization':'token '+token,
              'Accept':'application/vnd.github.v3+json'}
    uri = 'https://api.github.com/repos/'+owner+'/'+repos+'/collaborators/'+user_name

    r=requests.put(uri,data=payload,headers=header)
    if(r.status_code==201):
        return True
    else:
        print(r.status_code)
        print(r.text)
        return False

def f_check_collaborators(owner,repos,user_name):
    payload = {'get' : 'value'}
    header = {'Authorization':'token '+token,
              'Accept':'application/vnd.github.v3+json'}
    uri = 'https://api.github.com/repos/'+owner+'/'+repos+'/collaborators/'+user_name

    r=requests.get(uri,params=payload,headers=header)
    if(r.status_code==204):
        return True
    else:
        return False

def f_get_collaborators(owner,repos):
    payload = {'get' : 'value'}
    header = {'Authorization':'token '+token,
              'Accept':'application/vnd.github.v3+json'}
    uri = 'https://api.github.com/repos/'+owner+'/'+repos+'/collaborators'

    r=requests.get(uri,params=payload,headers=header)
    data = r.json()
    return data

def f_read_yml(path_arr):
    path = os.path.join(os.getcwd(),'yml')
    with open(os.path.join(path,path_arr[0],path_arr[1],path_arr[2])) as f:
        yml_data = yaml.load(f, Loader=yaml.FullLoader)
        yml_data=yml_data['Users']
    return yml_data

if (__name__ == '__main__'):
    path = os.path.join(os.getcwd(),'yml')
    file_list = os.listdir(path)
    full_list = [] #[[owner,repos,users.yml]]
    
    for file in file_list:
        if os.path.isdir(os.path.join(path,file)):
            for file2 in os.listdir(os.path.join(path,file)):
                print(file2)
                if os.path.isdir(os.path.join(path,file,file2)):
                    for file3 in os.listdir(os.path.join(path,file,file2)):
                        print(file3)
                        if file3.endswith(".yml"):
                            full_list.append([file,file2,file3])

    for z in range(len(full_list)):
        owner = full_list[z][0]
        repos = full_list[z][1]
        member_data_arr = f_read_yml(full_list[z])
        all_member_arr=[]
        all_member_data = f_get_collaborators(owner,repos)
        missing_member_data = []

        for i in range(len(member_data_arr)):
            all_member_arr.append(member_data_arr[i]['name'].lower())
            if f_check_collaborators(owner,repos,member_data_arr[i]['name']):
                print(member_data_arr[i]['name']+"'s already invite member");
            else:
                temp_permission = '';
                if(member_data_arr[i]['permission']['admin']):
                    temp_permission='admin'
                elif(member_data_arr[i]['permission']['maintain']):
                    temp_permission='maintain'
                elif(member_data_arr[i]['permission']['push']):
                    temp_permission='push'
                elif(member_data_arr[i]['permission']['triage']):
                    temp_permission='triage'
                elif(member_data_arr[i]['permission']['pull']):
                    temp_permission='pull'
                if(temp_permission!=''):
                    if(f_put_collaborators(owner,repos,member_data_arr[i]['name'],temp_permission)):
                        print(member_data_arr[i]['name']+"' invite user Success")
                    else:
                        print(member_data_arr[i]['name']+"' invite user Fail")

        for i in range(len(all_member_data)):
            if all_member_data[i]['login'].lower() not in all_member_arr:
                missing_member_data.append(all_member_data[i]['login']);

        if(len(missing_member_data)>0):
            print('\n\'s not found this member info in users.yml')
            for i in range(len(missing_member_data)):
                print(missing_member_data[i])