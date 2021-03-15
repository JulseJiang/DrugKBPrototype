from . import shortlist3
f2=open("shortlist4.py","w")
p={}
for i in shortlist3.set:
    p[i]={}
    for j in shortlist3.set[i]:
        if j[0] not in p[i]:
            p[i][j[0]]=[]
            p[i][j[0]].append(j)
        else:
            p[i][j[0]].append(j)
print("set=",file=f2,end="")
print(p,file=f2)
f2.close()
