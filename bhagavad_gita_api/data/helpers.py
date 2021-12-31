from urllib.request import urlopen


def remote_txt_file(url: str) -> str:
    string = ""
    file = urlopen(url)

    for line in file:
        decoded_line = line.decode("utf-8")
        string += decoded_line
    return string


# change branch after merge
def gh_file_url(
    file, owner="gita", repo="gita", branch="feat--new-languages", folder="data"
):
    base = "https://raw.githubusercontent.com"
    return f"{base}/{owner}/{repo}/{branch}/{folder+'/' if folder else ''}{file}"


def get_file(file):
    return remote_txt_file(gh_file_url(file))
