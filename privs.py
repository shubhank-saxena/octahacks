import sys
import json

def process(dest):
    l=len(dest)
    dest = list(dest)
    with open('res.json') as jsonf:
        data=json.load(jsonf)
    arr=[]
    for i in range(l):
        li= []
        for j in range(l):
            li.append(data[str(dest[i])][str(dest[j])]['distance'])
        arr.append(li)
    dist=[float('inf')]*l
    visited=[False]*l
    parent=[-1]*l
    dist[0]=0
    while l!=0:
        l-=1
        u=minimum(dist,visited)
        visited[u]=True
        for j in range(l):
            if visited[j]==False and dist[j]>arr[u][j]:
                dist[j]=arr[u][j]
                parent[j]=u
    l=len(dest)

    mst=[]
    for i in range(l):
        li = []
        for j in range(l):
            li.append(0)
        mst.append(li)

        
    for i in range(0,len(parent)):
        if i !=0:
            mst[parent[i]][i]=1
            mst[i][parent[i]]=1
    return mst


def minimum(dist,visited):
    mi= float('inf')
    node=0
    for x in range(len(dist)):
        if visited[x]==False and mi>dist[x]:
            mi=dist[x]
            node=x
    return node


def process2(se,mst,x,y):
    li = [se[x]]
    for i in range(len(mst)):
        if y!=i and mst[x][i]!=0:
            li+=process2(se,mst,i,x)
    return li 

def find_path(query, un):
    truck_cap=4
    query.sort(key=lambda tup: tup[0])
    le = len(query) 
    trucks=[]
    path=[]
    left=[]
    se = []
    p=0

    i = 0
    while i<le:
        if query[i][0]!=int(un):
            if i+truck_cap<le and query[i][0]==query[i+truck_cap][0]:
                trucks.append(query[i:i+truck_cap])
                path.append([query[i][0]])
                p+=1
                i+=truck_cap-1
            else:
                left.append(query[i])
                se.append(query[i][0])
        i+=1
    print("####")
    print(left)
    print("####")
    se = list(set(se))
    se.insert(0, int(un))
    print("####")
    print(se)
    print("####")
    
    
    mst=process(se)
    se2 = []
    for y in range(len(mst)):
        li=[]
        if mst[0][y]!=0:
            li+=process2(se,mst,y,0)
            se2.append(li)
    print("####")
    print(se2)
    print("####")
    truckcap=truck_cap
    temp=[]
    for x in se2:
        for a in left:
            if x.count(a[0])>0 and a[0]!=int(un):
                temp.append(a)
                truckcap-=1
                if truckcap==0:
                    trucks.append(temp)
                    path.append(x)
                    p+=1
                    temp=[]
                    truckcap=truck_cap

        p+=1
        if temp!=[]:
            trucks.append(temp)
        path.append(x)
        truckcap=truck_cap
        temp=[]

    return (trucks, path)