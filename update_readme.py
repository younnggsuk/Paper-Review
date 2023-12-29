import os
import github
import json
from github import Github
from github import Auth


REPO_TITLE_DESC = """
# Paper Review
This repo contains paper reviews. All reviews are listed below.
    
## Reviews
"""

TABLE_HEADER = """
| # | Date | Paper | Tags |
| - | ---- | ----- | ---- |
"""


def get_label_badge(name, color):
    name = name.replace(" ", "%20")
    name = name.replace("-", "--")
    url = f"https://img.shields.io/badge/{name}-{color}"
    label_badge = f"![]({url})"
    return label_badge


def main():
    # get access token
    auth = Auth.Token(os.environ["ACCESS_TOKEN"])
    g = Github(auth=auth)
    
    # Get the repository object
    repo = g.get_repo("younnggsuk/git_actions_test")
    open_issues = repo.get_issues(state='open')

    # Get all issues
    issue_lists = []
    for i, issue in enumerate(open_issues):
        issue_lists.append({
            "number": issue.number,
            "review": issue.html_url,
            "date": issue.created_at.strftime("%Y/%m/%d"),
            "title_paper": issue.body.split("\n")[0],
            "labels": [(label.name, label.color) for label in issue.labels] if len(issue.labels) > 0 else None
        })
    issue_lists.sort(key=lambda x: x["number"], reverse=True)

    # readme
    readme = REPO_TITLE_DESC
    readme += TABLE_HEADER
    
    for issue in issue_lists:
        number = f"{issue['number']}"
        date = issue['date']
        review = issue["review"]
        title_paper = f"{issue['title_paper']}"
        title_paper = title_paper.replace("\r", "").replace("\n", "")
        title_paper = title_paper.replace("# ", "")
        
        title = title_paper.split("[")[1].split("]")[0]
        paper = title_paper.split("(")[1].split(")")[0]
        title_paper = f"{title} \[[paper]({paper})\]"
        title_paper_review = title_paper + f" \[[review]({review})\]"
        
        if issue["labels"] is not None:
            issue['labels'].sort(key=lambda x: x[0].split(" ")[-1])
            tags = " ".join([get_label_badge(label, color) for label, color in issue['labels']])
        else:
            tags = " "
        readme += " | ".join([number, date, title_paper_review, tags]) + "\n"
    
    # write README.md
    with open("./README.md", "w") as f:
        f.write(readme)


if __name__ == "__main__":
    main()
