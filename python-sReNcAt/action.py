import requests
import yaml
import os
import sys

token = 'enter your token'

def f_put_collaborators(owner,repo,user_name,permission):
    payload = '{"permission":"'+permission+'"}'
    header = {'Authorization':'token '+token,
              'Accept':'application/vnd.github.v3+json'}
    uri = 'https://api.github.com/repos/'+owner+'/'+repo+'/collaborators/'+user_name
    r=requests.put(uri,data=payload,headers=header)
    if(r.status_code==201):
        return True
    else:
        print(r.status_code+" "+r.text)
        return False

def f_check_collaborators(owner,repo,user_name):
    payload = {'get' : 'value'}
    header = {'Authorization':'token '+token,
              'Accept':'application/vnd.github.v3+json'}
    uri = 'https://api.github.com/repos/'+owner+'/'+repo+'/collaborators/'+user_name
    r=requests.get(uri,params=payload,headers=header)
    if(r.status_code==204):
        return True
    else:
        return False

def f_get_collaborators(owner,repo):
    payload = {'get' : 'value'}
    header = {'Authorization':'token '+token,
              'Accept':'application/vnd.github.v3+json'}
    uri = 'https://api.github.com/repos/'+owner+'/'+repo+'/collaborators'
    r=requests.get(uri,params=payload,headers=header)
    data = r.json()
    return data

def f_read_yml():
    with open('members.yml') as f:
        yml_data = yaml.load(f, Loader=yaml.FullLoader)
        yml_data=yml_data['git']
    return yml_data

if (__name__ == '__main__'):
	members_data_arr = f_read_yml()
	for z in range(len(members_data_arr)):
		owner = members_data_arr[z]['owner']
		for x in range(len(members_data_arr[z]['repos'])):
			repo = members_data_arr[z]['repos'][x]['repo']
			members_data_arr = members_data_arr[z]['repos'][x]['Users']
			all_member_arr=[]
			all_member_data = f_get_collaborators(owner,repo)
			missing_member_data = []
			for i in range(len(members_data_arr)):
				all_member_arr.append(members_data_arr[i]['name'].lower())
				if f_check_collaborators(owner,repo,members_data_arr[i]['name']):
					print(members_data_arr[i]['name']+"'s already invite member");
				else:
					temp_permission = '';
					if(members_data_arr[i]['permission']['admin']):
						temp_permission='admin'
					elif(members_data_arr[i]['permission']['maintain']):
						temp_permission='maintain'
					elif(members_data_arr[i]['permission']['push']):
						temp_permission='push'
					elif(members_data_arr[i]['permission']['triage']):
						temp_permission='triage'
					elif(members_data_arr[i]['permission']['pull']):
						temp_permission='pull'
					if(temp_permission!=''):
						if(f_put_collaborators(owner,repo,members_data_arr[i]['name'],temp_permission)):
							print(members_data_arr[i]['name']+"' invite user Success")
						else:
							print(members_data_arr[i]['name']+"' invite user Fail")
			for i in range(len(all_member_data)):
				if all_member_data[i]['login'].lower() not in all_member_arr:
					missing_member_data.append(all_member_data[i]['login']);

			if(len(missing_member_data)>0):
				print('\n\'s not found this member info in members.yml')
				for i in range(len(missing_member_data)):
					print(missing_member_data[i])