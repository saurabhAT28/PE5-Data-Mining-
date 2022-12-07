import streamlit as st
import pandas as pd
import validators
from urllib.request import urljoin
from bs4 import BeautifulSoup
import requests
from urllib.request import urlparse

def app(dataset):
    st.header("Assignment -8")
    topic = st.selectbox("Select the clustering algorithm",("Crawler","Page Rank","HITS"))
    if topic == "Crawler":
        urls = set()
        url_with_depths = []
        btnClicked = False
        def next_level_links(seed):
            new_urls = set()
            #current_url_domain = urlparse(seed).netloc

            beautiful_soap_object = BeautifulSoup(requests.get(seed).content,"html.parser")

            for anchor in beautiful_soap_object.find_all("a"):
                href = anchor.attrs.get("href")
                if(href != "" or href != None):
                    href = urljoin(seed,href)
                    href_parsed = urlparse(href)
                    href = href_parsed.scheme
                    href += "://"
                    href += href_parsed.netloc
                    href += href_parsed.path
                    final_parsed_href = urlparse(href)
                    is_valid = bool(final_parsed_href.scheme) and bool(final_parsed_href.netloc)
                    if is_valid and href not in urls:
                        urls.add(href)
                        new_urls.add(href)
            return new_urls
        def crawlbfs(seed,depth,btnClicked):
            btnClicked = True
            queue = []
            queue.append([seed,0])
            url_with_depths.append([seed,0])
            while(len(queue)>0):
                print(queue)
                cur_url_pair = queue.pop(0)
                cur_url = cur_url_pair[0]
                cur_url_depth = cur_url_pair[1]
                #print(cur_url_depth)
                if cur_url_depth == depth:
                    break
                all_next_urls = next_level_links(cur_url)
                for i in all_next_urls:
                    queue.append([i,cur_url_depth+1])
                    url_with_depths.append([i,cur_url_depth+1])
            st.write("All urls")
            for i in url_with_depths:
                st.write("Depth: ",i[1],"    URL : ",i[0])
        def crawldfs(seed,level,depth):
            url_with_depths.append([seed,level])
            if level == depth:
                return
            all_next_urls = next_level_links(seed)
            for i in all_next_urls:
                crawldfs(i,level+1,depth)

        seed = st.text_input("Enter the seed url")
        if seed != "":
            if validators.url(seed):
                #print(seed)
                depth = st.number_input("Enter the depth to crawl upto",min_value=None,max_value=None,value = 0)
                btn1 = st.button("Crawl - DFS",on_click=crawlbfs,args=[seed,depth,btnClicked])
                btn2 = st.button("Crawl - BFS",on_click=crawlbfs,args=[seed,depth,btnClicked])
                if btnClicked == True:
                    st.write("All Urls")
                    for i in url_with_depths:
                        st.write("Depth: ",i[1],"    URL : ",i[0])
            else:
                st.write("Wrong url entered")
                st.write("Enter url again")        
    if topic == "Page Rank":
        file = st.file_uploader("Choose a file")
        # file = open("C:\Users\mohdn\OneDrive\Desktop\Files\DM Assignments\Assignment 8\stnfordgraph.txt", "r")
        flg = 0
        content = file.readlines()

        adj_mat = {}
        for line in content:
            # print(line)
            if(flg==0):
                lin = line.split(' ')
                vertex = int(lin[0])
                edges = int(lin[1][:])
                # print(edges)
                flg = 1
                adj_mat = {new_list: [] for new_list in range(vertex+1)}
                in_deg = [0]*(vertex+1)
                out_deg = [0]*(vertex+1)
            else:
                lin = line.split(' ')
                tmp = lin[0].split('\t')
                # print(tmp)  
                adj_mat[int(tmp[1][:-1])].append(int(tmp[0]))
                in_deg[int(tmp[1][:-1])] += 1
                out_deg[int(tmp[0])] += 1
        file = open('geek.txt','w')
        # print(out_deg)
        def calclute_pagerank():
            cnt = 0
            itr = 1
            while(cnt<=vertex+1):
                file.write(str("******Iteration" +str(itr)+" ******"))
                for i in range(1,vertex+1):
                    tmp_prnk[i] = 0 
                    for no in adj_mat[i]:
                        tmp_prnk[i] += (page_Rank[no]/out_deg[no])
                    if((abs(tmp_prnk[i]-page_Rank[i])/(page_Rank[i]))*100<=0.0001):
                        cnt += 1
                    if(tmp_prnk[i]):
                        page_Rank[i] = tmp_prnk[i]
                    file.write(str(page_Rank[i])+" ")
                itr+=1 
        page_Rank = [1/(vertex)]*(vertex+1)
        tmp_prnk = [0]*(vertex+1) 
        page_Rank[0] = 0
        # out_deg = [0,2,0,3,2,2,1]
        # file.write(str(page_Rank))
        calclute_pagerank()
        index = {}
        for i in range(1,vertex+1):
            index[page_Rank[i]] = i 
        page_Rank.sort()
        for i in range(1,11):
            st.write("Top ",i, "web page number is ", index[page_Rank[-i]] , "page rank is ",page_Rank[-i]);
                # st.write("Web and their Page rank")
                # for i in range(1,vertex+1):
                    # st.write(i," page their ",page_Rank[-i])
# if topic == "HITS":
#     input_list = []
    
#     st.subheader("Dataset")
#     st.dataframe(Data.head(1000), width=1000, height=500)
#     vertex = set()
#     for i in range(len(Data)):
#             input_list.append([Data.loc[i, 'fromNode'],Data.loc[i, 'toNode']])
#             vertex.add(Data.loc[i, 'fromNode'])
#             vertex.add(Data.loc[i, 'toNode'])
#     size = len(vertex)
#     adj_matrix = np.zeros([size+1,size+1])

#     for i in input_list:
#         adj_matrix[i[0]][i[1]] = 1
    
#     printf("No of Nodes: "+str(size))
#     printf("No of Edges: "+str(len(Data)))
#     st.subheader("Adjecency Matrix")
#     st.dataframe(adj_matrix, width=1000, height=500)
#     A = adj_matrix
#     # st.dataframe(A)
#     At = adj_matrix.transpose()
#     st.subheader("Transpose of Adj matrix")
#     st.dataframe(At)

#     u = [1 for i in range(size+1)]
#     printf("Hub weight matrix (U)")
#     st.dataframe(u)
#     # printf("Hub weight vector (V)")
#     # printf(u)
#     v = np.matrix([])
#     for i in range(5):
#         v = np.dot(At,u)
#         u = np.dot(A,v)

#     # u.sort(reverse=True)
#     hubdict = dict()
#     for i in range(len(u)):
#         hubdict[i]= u[i]
    
#     authdict = dict()
#     for i in range(len(v)):
#         authdict[i]=v[i]

#     hubdict = dict( sorted(hubdict.items(), key=operator.itemgetter(1),reverse=True))
#     authdict = dict( sorted(authdict.items(), key=operator.itemgetter(1),reverse=True))
#     # printf(sorted_rank)
#     printf("HubPages : ")
#     i = 1
#     printf(f"Rank ___ Node ________ Hubs score")
#     for key, rank in hubdict.items():
#         if i == 11:
#             break
#         printf(f"{i} _____ {key} ________ {rank}")
#         i += 1

#     printf("Authoritative Pages : ")
#     i = 1
#     printf(f"Rank ___ Node ________ Auth score")
#     for key, rank in authdict.items():
#         if i == 11:
#             break
#         printf(f"{i} _____ {key} ________ {rank}")
#         i += 1
