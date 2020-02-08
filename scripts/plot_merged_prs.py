#!/usr/bin/env python3

import numpy as np
import pickle
import datetime
import pandas

from matplotlib import pyplot as plt

from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Choose either "CURRENT_MAINTAINERS" (list of those with commit rights
# and users who had commit rights based on having done a merge),
# or "HAS_MERGED_A_PR" which defines a "Maintainer" as anyone who has
# merged a PR _before_ their PR was merged.
DEFINE_MAINTAINERS_BY = "CURRENT_MAINTAINERS"  #  "HAS_MERGED_A_PR"


# List of maintainers (NumPy users with commit rights)
CURRENT_MAINTAINERS = """
    ahaldane
    certik
    charris
    cournape
    eric-wieser
    FrancescAlted
    jaimefrio
    jjhelmus
    juliantaylor
    mhvk
    mwiebe
    njsmith
    pv
    rgommers
    rkern
    seberg
    shoyer
    stefanv
    teoliphant
    matthew-brett
    mattip
    tylerjereddy
    WarrenWeckesser
    """.split()
assert(len(CURRENT_MAINTAINERS) == 23)

# Users who have merged a PR and/or served on the Steering Council
OLDER_MAINTAINERS = """
    argriffing
    timcera
    pletnes
    jennystone
""".split()
CURRENT_MAINTAINERS.extend(OLDER_MAINTAINERS)


def is_current_maintainer(user_login):
    return user_login in CURRENT_MAINTAINERS

# Filled using the date they first merged a PR.
MAINTAINERS_SINCE = {}

with open("pr_data.pkl", "rb") as pickle_file:
    pr_list = pickle.load(pickle_file)


def maintainer_by_first_merge(pr_list):
    maintainer_since = MAINTAINERS_SINCE
    names = {}
    for pr in pr_list:
        merger = pr["merged_by_id"]
        if merger is None:
            print("PR merged by unknown user:", pr["number"])
        if pr["merged_by"] == "homu":
            continue

        if merger not in maintainer_since:
            maintainer_since[merger] = pr["merged_at"]
            names[merger] = pr["merged_by"]
            continue


        old = maintainer_since[merger]
        new = pr["merged_at"]
        maintainer_since[merger] = min(old, new)

    del maintainer_since[None]

    for m in sorted(maintainer_since.keys()):
        print(f"    {names[m]}: {maintainer_since[m]}")

    print("Total Number of maintainers by 'merged':", len(maintainer_since))

maintainer_by_first_merge(pr_list)


# Use dataframe to plot all the PRs:

prs = pandas.DataFrame(pr_list)



if True:
    # Filter by time, so autoscaling works...
    prs = prs.iloc[(prs["merged_at"] > datetime.datetime(2012, 1, 1)).values]

prs = prs.set_index("merged_at")

plt.figure(figsize=(6*0.75, 4*0.75))
plt.ylabel("PRs merged each quarter")


def find_category(row):
    """Function to define who is a Maintainer and who is not"""
    if DEFINE_MAINTAINERS_BY == "CURRENT_MAINTAINERS":
        if row["is_collaborator"]:
            return "Maintainer"
        return "Other"

    elif DEFINE_MAINTAINERS_BY == "HAS_MERGED_A_PR":
        author_id = row["author_id"]
        if author_id in MAINTAINERS_SINCE:
            if row.name >= MAINTAINERS_SINCE[author_id]:
                return "Maintainer"

        return "Other"

    else:
        raise AssertionError()


prs["category"] = prs.apply(find_category, axis=1)

groups = {}
for g, comm in prs.groupby("category"):
    resampled = comm["category"].resample(
            # Resample starting at each quarter and shift by about 1/2 quarter
            "QS", loffset=0 * datetime.timedelta(days=30*3/2)).count()
    groups[g] = resampled

categories = ["Maintainer", "Other"]
stacked = []
# other color:  "#0e50a8", "#077a0a" OR   "#cce0fb", "#71f775"
for color, cat in zip(["#0e50a8aa", "#077a0aaa"], categories):
    next_stack = groups[cat]

    if len(stacked) > 0:
        prev_vals = stacked[-1].values
        next_stack = next_stack + stacked[-1]
    else:
        prev_vals = np.zeros_like(next_stack.values)

    stacked.append(next_stack)

    plt.fill_between(
        next_stack.index.repeat(2) + np.array([0, datetime.timedelta(days=30*3)] * len(next_stack.index), dtype="m8[D]"),
        next_stack.values.repeat(2), prev_vals.repeat(2),
        label=cat, lw=0, zorder=4 if cat == "Community" else 3,
        color=color)
    if False:
        plt.plot(
            next_stack.index + datetime.timedelta(days=30*3/2), next_stack.values, "o",
            zorder=4 if cat == "Community" else 3, color="none",
            mec="k", ms=4)

    print(f"Total number for {cat}:", (next_stack.values - prev_vals).sum())

plt.xlim(resampled.index.min(), resampled.index[-1])
plt.ylim(0, None)

plt.legend(loc="upper left")

plt.tight_layout()

plt.savefig(f"PRs-using-{DEFINE_MAINTAINERS_BY}.pdf")
plt.show()

print()
print("Number of unique users:", len({pr["author_id"] for pr in pr_list}))
