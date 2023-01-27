import requests
from bs4 import BeautifulSoup
import json

headers = {
    'Host': 'github.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
}

class Github:
    def __init__(self):
        self.session = requests.Session()
        self.timeline = []
        self.name = ""
        self.user=""
        self.password=""

    def login(self):
        self.user = input("Enter your username: ")
        self.password = input("Enter your password: ")
        html = self.session.get("https://github.com/login", headers=headers).text
        authencity_token = BeautifulSoup(html, "html.parser").find("input", {"name": "authenticity_token"})["value"]
        data = {
            "commit": "Sign in",
            "utf8": "✓",
            "authenticity_token": authencity_token,
            "login": self.user,
            "password": self.password
        }
        html = self.session.post("https://github.com/session", data=data, headers=headers).text
        if "Incorrect username or password." in html:
            print("Incorrect username or password.")
            self.login()
        else:
            print("Login successful.")
            self.name = BeautifulSoup(html, "html.parser")#.find("span", {"class": "css-truncate-target"}).text
            print(self.name)
    
    def get_timeline(self):
        html = self.session.get("https://github.com/dashboard", headers=headers).text
        table = BeautifulSoup(html, "html.parser").find("div", {"class": "alert"})
        for item in table:
            line = {}
            line["thing"] = item.find("div",{'class':'title'}).get_text().replace("\r","").replace("\n","").replace("\t","")
            line["time"] = item.find("relative-time").get("datetime")
            self.timeline.append(line)

    def show_timeline(self):
        keys = ["who", "do", "to", "time"]
        for item in self.timeline:
            text = item["time"]+"......."+item["thing"]
            print('*'+text+''+'*'*(100-len(text) - 2)+'*')
            print('*_*_*'*16)
    
    def overview(self, user=None):
        if user == None:
            user = self.user
        html = self.session.get("https://github.com/"+user, headers=headers).text
        return html

    def get_repos(self, user=None):
        if user == None:
            user = self.user
        html = self.overview(user)
        repos = []
        for item in BeautifulSoup(html, "html.parser").find_all("a", {"itemprop": "name codeRepository"}):
            repos.append(item.get("href"))
        return repos
    
    def get_repo(self, repo):
        html = self.session.get("https://github.com"+repo, headers=headers).text
        return html

    def get_repo_files(self, repo):
        html = self.get_repo(repo)
        files = []
        for item in BeautifulSoup(html, "html.parser").find_all("a", {"class": "js-navigation-open Link--primary"}):
            files.append(item.get("href"))
        return files

    def get_file(self, file):
        html = self.session.get("https://github.com"+file, headers=headers).text
        return html

    def get_file_content(self, file):
        html = self.get_file(file)
        content = BeautifulSoup(html, "html.parser").find("div", {"class": "blob-wrapper data type-text"}).get_text()
        return content

    def get_repo_commits(self, repo):
        html = self.get_repo(repo)
        commits = []
        for item in BeautifulSoup(html, "html.parser").find_all("a", {"class": "commit-tease-sha"}):
            commits.append(item.get("href"))
        return commits

    def get_commit(self, commit):
        html = self.session.get("https://github.com"+commit, headers=headers).text
        return html

    def get_commit_files(self, commit):
        html = self.get_commit(commit)
        files = []
        for item in BeautifulSoup(html, "html.parser").find_all("a", {"class": "link-gray-dark"}):
            files.append(item.get("href"))
        return files

    def get_commit_file(self, file):
        html = self.session.get("https://github.com"+file, headers=headers).text
        return html

    def get_commit_file_content(self, file):
        html = self.get_commit_file(file)
        content = BeautifulSoup(html, "html.parser").find("div", {"class": "blob-wrapper data type-text"}).get_text()
        return content

    def get_repo_issues(self, repo):
        html = self.get_repo(repo)
        issues = []
        for item in BeautifulSoup(html, "html.parser").find_all("a", {"class": "Link--primary v-align-middle no-underline h4 js-navigation-open"}):
            issues.append(item.get("href"))
        return issues

    def get_issue(self, issue):
        html = self.session.get("https://github.com"+issue, headers=headers).text
        return html

    def get_issue_comments(self, issue):
        html = self.get_issue(issue)
        comments = []
        for item in BeautifulSoup(html, "html.parser").find_all("a", {"class": "Link--primary"}):
            comments.append(item.get("href"))
        return comments

    def get_comment(self, comment):
        html = self.session.get("https://github.com"+comment, headers=headers).text
        return html

    def get_comment_content(self, comment):
        html = self.get_comment(comment)
        content = BeautifulSoup(html, "html.parser").find("div", {"class": "comment-body markdown-body js-comment-body"}).get_text()
        return content

    def get_repo_pulls(self, repo):
        html = self.get_repo(repo)
        pulls = []
        for item in BeautifulSoup(html, "html.parser").find_all("a", {"class": "Link--primary v-align-middle no-underline h4 js-navigation-open"}):
            pulls.append(item.get("href"))
        return pulls

    def get_pull(self, pull):
        html = self.session.get("https://github.com"+pull, headers=headers).text
        return html

    def get_pull_comments(self, pull):
        html = self.get_pull(pull)
        comments = []
        for item in BeautifulSoup(html, "html.parser").find_all("a", {"class": "Link--primary"}):
            comments.append(item.get("href"))
        return comments

    def get_pull_comment(self, comment):
        html = self.session.get("https://github.com"+comment, headers=headers).text
        return html

    def get_pull_comment_content(self, comment):
        html = self.get_pull_comment(comment)
        content = BeautifulSoup(html, "html.parser").find("div", {"class": "comment-body markdown-body js-comment-body"}).get_text()
        return content

    def get_repo_stars(self, repo):
        html = self.get_repo(repo)
        stars = []
        for item in BeautifulSoup(html, "html.parser").find_all("a", {"class": "Link--primary"}):
            stars.append(item.get("href"))
        return stars

    def get_repo_watchers(self, repo):
        html = self.get_repo(repo)
        watchers = []
        for item in BeautifulSoup(html, "html.parser").find_all("a", {"class": "Link--primary"}):
            watchers.append(item.get("href"))
        return watchers

    def get_repo_forks(self, repo):
        html = self.get_repo(repo)
        forks = []
        for item in BeautifulSoup(html, "html.parser").find_all("a", {"class": "Link--primary"}):
            forks.append(item.get("href"))
        return forks

    def get_repo_contributors(self, repo):
        html = self.get_repo(repo)
        contributors = []
        for item in BeautifulSoup(html, "html.parser").find_all("a", {"class": "Link--primary"}):
            contributors.append(item.get("href"))
        return contributors

    def get_repo_branches(self, repo):
        html = self.get_repo(repo)
        branches = []
        for item in BeautifulSoup(html, "html.parser").find_all("a", {"class": "Link--primary"}):
            branches.append(item.get("href"))
        return branches

    def get_repo_releases(self, repo):
        html = self.get_repo(repo)
        releases = []
        for item in BeautifulSoup(html, "html.parser").find_all("a", {"class": "Link--primary"}):
            releases.append(item.get("href"))
        return releases

    def get_repo_tags(self, repo):
        html = self.get_repo(repo)
        tags = []
        for item in BeautifulSoup(html, "html.parser").find_all("a", {"class": "Link--primary"}):
            tags.append(item.get("href"))
        return tags

test = Github()

print(test.login())
print(test.get_timeline())

    

