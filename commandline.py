import sys, ai, json, random
def depth(d):
    depth=0
    q = [(i, depth+1) for i in d.values() if isinstance(i, dict)]
    max_depth = 0
    while (q):
        n, depth = q.pop()
        max_depth = max(max_depth, depth)
        q = q + [(i, depth+1) for i in n.values() if isinstance(i, dict)]

    return max_depth

def usage():
    print("Usage: {} train training-file=stdin model-file=stdout max-history=10".format(sys.argv[0]))
    print("OR:    {} predict model-file=stdin length=200 output-file=stdout".format(sys.argv[0]))
    sys.exit(1)

data = {}

if sys.argv[1] == "train":
    data = {"training-file": "stdin", "model-file": "stdout", "max-history": 10}
elif sys.argv[1] == "predict":
    data = {"model-file": "stdin", "length": 200, "output-file": "stdout", "max-history": 10}
else:
    usage()

for arg in sys.argv[2:]:
    if "=" in arg:
        key = arg.split("=")[0]
        val = arg.split("=")[1]
        if data.get(key) != None:
            data[key] = val
        else:
            usage()
    else:
        usage()

if sys.argv[1] == "train":
    if data["training-file"] == "stdin":
        tdata = input()
    else:
        with open(data["training-file"], "r") as f:
            tdata = f.read()

    model = ai.train(tdata, int(data["max-history"]))
    if data["model-file"] == "stdout":
        print(json.dumps(model))
    else:
        with open(data["model-file"], "w") as f:
            f.write(json.dumps([model, tdata]))

elif sys.argv[1] == "predict":
    if data["model-file"] == "stdin":
        model = json.loads(input())
    else:
        with open(data["model-file"], "r") as f:
            a = json.loads(f.read())
            model = a[0]
            txt = a[1]
            
    
    size = int(data["max-history"])
    idx = random.randint(0, len(txt) - size - 1)
            
    output = ai.predict(txt[idx:idx+size],
                        int(data["length"]), model)

    if data["output-file"] == "stdout":
        print(output)
    else:
        with open(data["output-file"], "w") as f:
            f.write(output)
