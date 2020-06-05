from __future__ import print_function, unicode_literals

from typing import Dict, List
from PyInquirer import prompt, Separator

import base64
import requests

from constants import BADGES


def handle_response(response, error_msg) -> Dict:
    if response.status_code != 200:
        # This means something went wrong.
        raise Exception(error_msg)

    return response.json()


def decode_content(encoded_content: str) -> str:
    base64_bytes = encoded_content.encode("utf-8")
    message_bytes = base64.b64decode(base64_bytes)
    return message_bytes.decode("utf-8")


def encode_content(str_content: str) -> str:
    message_bytes = str_content.encode("utf-8")
    base64_bytes = base64.b64encode(message_bytes)
    return base64_bytes.decode("utf-8")


def get_all_repos(user_name: str) -> List:
    resp = requests.get(f"https://api.github.com/users/{user_name}/repos?per_page=1000")

    resp_json = handle_response(
        resp, f"Error while fetching repos for user {user_name}"
    )
    return [r["name"] for r in resp_json] or []


def prompt_user_name():
    questions = [
        {
            "type": "input",
            "name": "user_name",
            "qmark": "",
            "message": "Enter your github username\n",
        }
    ]
    answers = prompt(questions)
    return answers["user_name"]


def prompt_auth_token():
    questions = [
        {"type": "password", "qmark": "", "name": "token", "message": "Github OAuth Token\n", }
    ]
    answers = prompt(questions)
    return answers["token"]


def prompt_repo_selection(repos):
    questions = [
        {
            "type": "checkbox",
            "qmark": "",
            "message": "Select Repos to add badges to",
            "name": "repos",
            "choices": [Separator("= Repo ="), ]
                       + [{"name": r, "checked": True} for r in repos],
        }
    ]
    repos = prompt(questions)
    if not repos or not repos["repos"]:
        raise Exception("No repo selected")

    return repos["repos"]


def prompt_badge_selection():
    questions = [
        {
            "type": "checkbox",
            "qmark": "",
            "message": "Select badges to add",
            "name": "badges",
            "choices": [Separator("= Badges ="), ]
                       + [{"name": k, "checked": True} for k, v in BADGES.items()],
        }
    ]
    badge_key = prompt(questions)
    if not badge_key or not badge_key["badges"]:
        raise Exception("No badge selected")

    return badge_key["badges"]


def add_badges_to_readme(user_name, repo, selected_badges):
    readme_resp = requests.get(
        f"https://api.github.com/repos/{user_name}/{repo}/readme"
    )
    readme_json = handle_response(
        readme_resp, f"Error while fetching readme for user {user_name}, repo {repo}"
    )
    readme_content = readme_json["content"]
    decoded_content = decode_content(readme_content)

    if "## Stats" in decoded_content:
        return

    decoded_content += "\n## Stats\n"
    decoded_content += "\t".join([BADGES[k](user_name, repo) for k in selected_badges])
    encoded = encode_content(decoded_content)
    resp = requests.put(
        f"https://api.github.com/repos/{user_name}/{repo}/contents/{readme_json['path']}",
        json={
            "message": "Adding badge to readme",
            "content": encoded,
            "sha": readme_json["sha"],
        },
        headers={"Authorization": f"token {token}"},
    )

    handle_response(resp, f"Failed updating readme for {repo}")


user_name = prompt_user_name()
token = prompt_auth_token()

repos = get_all_repos(user_name)

selected_repos = prompt_repo_selection(repos)
selected_badges = prompt_badge_selection()

for repo in selected_repos:
    print(f"Repo: {repo} , updating.")
    add_badges_to_readme(user_name, repo, selected_badges)
    print(f"Update finish.")
