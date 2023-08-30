import os
import json

with open("dict_data.json", 'r') as f:
    datastore = json.load(f)
res_dir = os.path.join(os.getcwd(),"res")
creator_dir = os.path.join(res_dir,"creator")
mov_dir = os.path.join(res_dir, "movement")

l = ["context", "no_context"]
d = '[]\"\"'

for t in l:
    with open(os.path.join(os.path.join(creator_dir,t),"res.csv"), "r") as j:
        res = j.readlines()
        correct = 0
        total = 0
        for i in range(1,len(res),2):
            line = res[i]
            r = line.split("\t")
            # node = res[i-1].split("\t")[0]
            # print(r)
            y = r[1].lower()
            label = r[-1]
            label = label.strip("\n")
            label = label.strip('[')
            label = label.strip(']')
            label = label.strip('\'')
            label = label.lower()
            if t == "no_context":
                y = r[2].lower()
                label = r[-1]
                label = label.strip("\n")
                label = label.strip('[')
                label = label.strip(']')
                label = label.strip('\'')
                label = label.lower()
                print(y)
                print(label)

            # print(label)
            if label in y:
                correct += 1
            total += 1
        print("Accuracy creator " + t + ": " + str(correct / float(total)))

    with open(os.path.join(os.path.join(mov_dir,t),"res.csv"), "r") as j:
        res = j.readlines()
        correct = 0
        total = 0
        for i in range(1,len(res),2):
            line = res[i]
            r = line.split("\t")
            # node = res[i-1].split("\t")[0]
            y = r[1].lower()
            label = r[-1]
            label = label.strip("\n")
            label = label.strip('[')
            label = label.strip(']')
            label = label.strip('\'')
            label = label.lower()
            print(y)
            if t == "no_context":
                y = r[2].lower()
                label = r[-1]
                label = label.strip("\n")
                label = label.strip('[')
                label = label.strip(']')
                label = label.strip('\'')
                label = label.lower()
                print(y)
                print(label)
            if label == y:
                correct +=1
            total += 1
        print("Accuracy movement " + t + ": " + str(correct / float(total)))




