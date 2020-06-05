BADGES = {
    "visitors": lambda user_name, repo_name: f"![visitors](https://visitor-badge.glitch.me/badge?page_id={user_name}"
    f".{repo_name})",
    "code_size": lambda user_name, repo_name: f"![code-size](https://img.shields.io/github/languages/code-size"
    f"/{user_name}"
    f"/{repo_name})",
}

LABEL_DEFINITION = (
    lambda user_name, repo_name, issue_tag: f"https://badgen.net/github/label-issues/{user_name}/{repo_name}/{issue_tag}/open"
)
