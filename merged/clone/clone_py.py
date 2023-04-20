import pandas as pd
import requests
import json
import time
from git import Repo

df = pd.read_csv("../louvain/project_id_mapping.csv")

m = {}
for k,v in df.iterrows():
  m[v[2]] = v[1]

df2 = pd.read_csv("../louvain/graph_node2comm_level2_merged")


m2 = {}
for ind,row in df2.iterrows():
  splitting = row[0].split(" ")
  node = int(splitting[0])
  cluster = int(splitting[1])

  if cluster not in m2:
    m2[cluster] = []
  m2[cluster].append(node)

print(m2[19])

username = "abhilashdzr"
token = "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"
gh_session = requests.Session()
gh_session.auth = (username, token)

common = "https://github.com/"
api_url = "https://api.github.com"

for i in m2[19]: 
    print(m[i])
    github_owner = common + str(m[i])

    url = api_url + f'/users/{str(m[i])}/repos'

    page = 1
    another_page = True
    repo_list = []
    try:
        while another_page:
            gh_session.params = {'page':page, 'per-page':100}
            r = gh_session.get(url)

            json_response = json.loads(r.text)
            for each in json_response:
                repo_name = each["name"]
                clone_url = github_owner+"/"+repo_name+".git"
                print(clone_url)
                print(repo_name)
                print(each["fork"]==True)
                if each["fork"] is False: 
                  Repo.clone_from(clone_url,f"./2nd_cluster/{m[i]}/{repo_name}")
                  time.sleep(5)
            exit()
            if 'next' in r.links:
                page +=1
                time.sleep(500)
            else:
                page = 1
                another_page = False

    except:
        pass
