#!/usr/bin/env python3

import sys

import github
import pickle


token = sys.argv[1]

# Using a token/login is required to download these statistics:
g = github.Github(token)
numpy = g.get_repo('numpy/numpy')

# Closed will ignore PRs that are not yet merged...
merged_pulls = numpy.get_pulls(state="closed")

NUMPY_ORG_MEMBER_IDS = {u.id for u in numpy.get_collaborators()}

try:
    with open("pr_data.pkl", "rb") as pickle_file:
        pr_list = pickle.load(pickle_file)

    if "number" not in pr_list[0]:
        for pr in pr_list:
            pr["number"] = int(pr["url"].replace("https://github.com/numpy/numpy/pull/", ""))

except Exception as e:
    print("no data loaded:", e)
    pr_list = []

known = {pr["number"] for pr in pr_list}


for pr in merged_pulls:
    if pr.number in known:
        print("Already knew PR number:", pr.number)
        continue

    if not pr.base.label == "numpy:master":
        # skip non-master (usually not interesting w.r.t. review)
        continue

    if not pr.merged:
        continue

    user = pr.user
    pr_author_id = user.id
    pr_author = user.login

    merger = pr.merged_by
    try:

        merged_by = merger.login
        merged_by_id = merger.id
    except:
        merged_by = merger
        merged_by_id = None

    info = {
        "number": pr.number,
        "title": pr.title,
        # There is probably a better way to get the URL...
        "url": pr.url.replace("//api.", "//").replace("/pulls/", "/pull/").replace("/repos/", "/"),
        "created_at": pr.created_at,
        "merged_at": pr.merged_at,
        "merged_by": merged_by,
        "merged_by_id": merged_by_id,
        "author": pr_author,
        "author_id": pr_author_id,
        "is_collaborator": pr_author_id in NUMPY_ORG_MEMBER_IDS,
        "merge_commit_sha": pr.merge_commit_sha,
        "labels": [l.name for l in pr.labels],
        }
    print(info)
    pr_list.append(info)


with open("pr_data.pkl", "wb") as pickle_file:
    pickle.dump(pr_list, pickle_file)
