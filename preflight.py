import json,glob,os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
S={}
for f in glob.glob("*.json"):
    d=json.load(open(f)); S[d["sheet"]]=d
ids={n:{r["id"] for r in d["rows"]} for n,d in S.items()}
bad=[]
for n,d in S.items():
    for r in d["rows"]:
        for c in d["columns"]:
            if r.get(c) is None and not (n=="items" and c=="damage") and not (n=="building" and c=="upgradeFrom"):
                bad.append(f"UNFILLED {n}.{r['id']}.{c}")
            if c=="verified" and r.get(c) is False: bad.append(f"UNVERIFIED {n}.{r['id']}")
refs=[("items","rustAsset","assets"),("recipes","output","items"),("raiders","weapon","items"),("raiders","targets","building"),("building","upgradeFrom","building")]
for s,c,t in refs:
    for r in S[s]["rows"]:
        v=r.get(c)
        if v is not None and v not in ids[t]: bad.append(f"BROKEN REF {s}.{r['id']}.{c} -> {v}")
for r in S["recipes"]["rows"]:
    for k in r["inputs"]:
        if k not in ids["items"]: bad.append(f"BROKEN REF recipes.{r['id']}.inputs -> {k}")
for r in S["building"]["rows"]:
    for k in r["cost"]:
        if k not in ids["items"]: bad.append(f"BROKEN REF building.{r['id']}.cost -> {k}")
print(len(bad),"findings"); print("\n".join(bad[:40])); 
unf=[b for b in bad if b.startswith("UNFILLED")]; unv=[b for b in bad if b.startswith("UNVERIFIED")]; br=[b for b in bad if b.startswith("BROKEN")]
print(f"\nsummary: {len(unf)} unfilled cells, {len(unv)} unverified rows, {len(br)} broken refs")
