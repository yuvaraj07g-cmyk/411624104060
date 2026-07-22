import json


l=["1","2","3","4","5","Hi",True,3.14]
l.append("Hello")
l.pop(3)
print(l)

d={1:"a",2:"b",3:"c"}
for k,v in d.items():
    print(k,v)

def function1():
    print("Hello")

function1()

class MyClass:
    def __init__(self, i):
        self.i = i
    def function1(self):
        print(self.i)
    def function2(self,j):
        print(j)    
m = MyClass(10)
m.function1()
m.function2(20)        

user={"name":"John","age":30,"city":"New York"}
json_string = json.dumps(user)
print(json_string)

f=open("jsonfile.json","w")
f.write(json_string)
f.close()

#f=open("jsonfile.json","r")
#print(f.readline())
#f.close()

with open("jsonfile.json","r") as f:
    data = json.load(f)
    print(data)