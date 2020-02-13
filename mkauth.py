import yaml

with open("authors.yml") as f:
    d = yaml.load(f, Loader=yaml.FullLoader)

auths = d["auth"]

star = len(d["inst"])
affil_dict = {}
affil_print = []
for n, a in enumerate(d["inst"]):
    for k, v in a.items():
        num = n + 1
        if num == star:
            num = "*"
        affil_dict.update({k: num})
        affil_print.append(f"\\affil[{num}]{{{v}}}")

with open("authors.tex", "w") as f:
    for auth in auths:
        for name, i in auth.items():
            insts = ",".join(
                [str(item) for item in [affil_dict[ins] for ins in i["institute"]]]
            )
            insts = f"[{insts}]"
            f.write(f"\\author{insts}{{{name}}}")
            f.write("\n")
    for affil in affil_print:
        f.write(affil)
        f.write("\n")
