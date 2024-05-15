import json

with open("./dataset.json") as fp:
    data = json.load(fp)

hmap = {}
for prod in data:
    hmap[prod["categoryID"]] = {
        "name": f"{prod["category"]}",
        "image": prod["categoryImage"],
    }

hmap = dict(sorted(hmap.items()))
print(hmap)
