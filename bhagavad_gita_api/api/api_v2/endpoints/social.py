import requests
import os
from datetime import datetime
import json
from bs4 import BeautifulSoup as bs
import time
import random
import string

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class MyIGBot:
    def __init__(self, username, password, use_cookie = True, proxy=None):
        self.username = username
        self.password = password
        self.use_cookie = use_cookie
        self.proxy = proxy

        self.path = os.getcwd()

        if use_cookie == False or os.path.exists(self.path+f'//cookie_{self.username}.bot') == False:
            link = 'https://www.instagram.com/'
            login_url = 'https://www.instagram.com/accounts/login/ajax/'

            time_now = int(datetime.now().timestamp())
            response = requests.get(link, proxies=self.proxy)
            try:
                csrf = response.cookies['csrftoken']
            except:
                letters = string.ascii_lowercase
                csrf = ''.join(random.choice(letters) for i in range(8))

            payload = {
                'username': self.username,
                'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{time_now}:{self.password}',
                'queryParams': {},
                'optIntoOneTap': 'false'
            }

            login_header = {
                "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36",
                "X-Requested-With": "XMLHttpRequest",
                "Referer": "https://www.instagram.com/accounts/login/",
                "x-csrftoken": csrf
            }

            login_response = requests.post(login_url, data=payload, headers=login_header, proxies=self.proxy)
            json_data = json.loads(login_response.text)

            cookies = login_response.cookies
            cookie_jar = cookies.get_dict()
            try:
                self.csrf_token = cookie_jar['csrftoken']
            except:
                self.csrf_token = csrf

            try:
                if json_data["authenticated"]:
                    pass
                else:
                    print(bcolors.FAIL+"[✗] Login Failed!"+bcolors.ENDC, login_response.text)
                    quit()
            except KeyError:
                try:
                    if json_data["two_factor_required"]:
                        self.ig_nrcb = cookie_jar['ig_nrcb']
                        self.ig_did = cookie_jar['ig_did']
                        self.mid = cookie_jar['mid']

                        otp = input(bcolors.OKBLUE+'[!] Two Factor Auth. Detected! Enter Code Here: '+bcolors.ENDC)
                        twofactor_url = 'https://www.instagram.com/accounts/login/ajax/two_factor/'
                        twofactor_payload = {
                            'username': self.username,
                            'verificationCode': otp,
                            'identifier': json_data["two_factor_info"]["two_factor_identifier"],
                            'queryParams': {}
                        }

                        twofactor_header = {
                            "accept": "*/*",
                            "accept-encoding": "gzip, deflate, br",
                            "accept-language": "en-US,en;q=0.9",
                            "content-type": "application/x-www-form-urlencoded",
                            "cookie": 'ig_did='+self.ig_did+'; ig_nrcb='+self.ig_nrcb+'; csrftoken='+self.csrf_token+'; mid='+self.mid,
                            "origin": "https://www.instagram.com",
                            "referer": "https://www.instagram.com/accounts/login/two_factor?next=%2F",
                            "sec-fetch-dest": "empty",
                            "sec-fetch-mode": "cors",
                            "sec-fetch-site": "same-origin",
                            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36",
                            "x-csrftoken": self.csrf_token,
                            "x-ig-app-id": "936619743392459",
                            "x-ig-www-claim": "0",
                            "x-instagram-ajax": "00c4537694a4",
                            "x-requested-with": "XMLHttpRequest"
                        }

                        login_response = requests.post(twofactor_url, data=twofactor_payload, headers=twofactor_header, proxies=self.proxy)
                        try:
                            if login_response.headers['Set-Cookie'] != 0:
                                pass
                        except:
                            try:
                                if json_data["message"]=="checkpoint_required":
                                    self.ig_nrcb = cookie_jar['ig_nrcb']
                                    self.ig_did = cookie_jar['ig_did']
                                    self.mid = cookie_jar['mid']
                                    url='https://www.instagram.com'+json_data['checkpoint_url']
                                    header = {
                                        "accept": "*/*",
                                        "accept-encoding": "gzip, deflate, br",
                                        "accept-language": "en-US,en;q=0.9",
                                        "content-type": "application/x-www-form-urlencoded",
                                        "cookie": 'ig_did='+self.ig_did+'; ig_nrcb='+self.ig_nrcb+'; csrftoken='+self.csrf_token+'; mid='+self.mid,
                                        "origin": "https://www.instagram.com",
                                        "referer": 'https://instagram.com'+json_data['checkpoint_url'],
                                        "sec-fetch-dest": "empty",
                                        "sec-fetch-mode": "cors",
                                        "sec-fetch-site": "same-origin",
                                        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36",
                                        "x-csrftoken": self.csrf_token,
                                        "x-ig-app-id": "936619743392459",
                                        "x-ig-www-claim": "0",
                                        "x-instagram-ajax": "e8e20d8ba618",
                                        "x-requested-with": "XMLHttpRequest"
                                    }
                                    code=input(bcolors.OKBLUE+json.loads(requests.post(url, headers=header, data={'choice': '1'}).text, proxies=self.proxy)['extraData']['content'][1]['text']+' > '+bcolors.ENDC)
                                    if json.loads(requests.post(url, headers=header, data={'security_code': code}).text, proxies=self.proxy)['type']=='CHALLENGE_REDIRECTION':
                                        login_response = requests.post(login_url, data=payload, headers=login_header, proxies=self.proxy)
                                    else:
                                        print(bcolors.FAIL+'[✗] Login Failed!'+bcolors.ENDC)
                                        quit()
                            except:
                                print(bcolors.FAIL+'[✗] Login Failed!'+bcolors.ENDC)
                                quit()

                except KeyError:
                    try:
                        if json_data["message"]=="checkpoint_required":
                            self.ig_nrcb = cookie_jar['ig_nrcb']
                            self.ig_did = cookie_jar['ig_did']
                            self.mid = cookie_jar['mid']
                            url='https://www.instagram.com'+json_data['checkpoint_url']
                            header = {
                                "accept": "*/*",
                                "accept-encoding": "gzip, deflate, br",
                                "accept-language": "en-US,en;q=0.9",
                                "content-type": "application/x-www-form-urlencoded",
                                "cookie": 'ig_did='+self.ig_did+'; ig_nrcb='+self.ig_nrcb+'; csrftoken='+self.csrf_token+'; mid='+self.mid,
                                "origin": "https://www.instagram.com",
                                "referer": 'https://instagram.com'+json_data['checkpoint_url'],
                                "sec-fetch-dest": "empty",
                                "sec-fetch-mode": "cors",
                                "sec-fetch-site": "same-origin",
                                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36",
                                "x-csrftoken": self.csrf_token,
                                "x-ig-app-id": "936619743392459",
                                "x-ig-www-claim": "0",
                                "x-instagram-ajax": "e8e20d8ba618",
                                "x-requested-with": "XMLHttpRequest"
                            }
                            code=input(bcolors.OKBLUE+json.loads(requests.post(url, headers=header, data={'choice': '1'}).text, proxies=self.proxy)['extraData']['content'][1]['text']+' > '+bcolors.ENDC)
                            if json.loads(requests.post(url, headers=header, data={'security_code': code}).text, proxies=self.proxy)['type']=='CHALLENGE_REDIRECTION':
                                login_response = requests.post(login_url, data=payload, headers=login_header, proxies=self.proxy)
                            else:
                                print(bcolors.FAIL+'[✗] Login Failed!'+bcolors.ENDC)
                                quit()
                    except:
                        print(bcolors.FAIL+'[✗] Login Failed!'+bcolors.ENDC)
                        quit()

            self.sessionid = login_response.headers['Set-Cookie'].split('sessionid=')[1].split(';')[0]                
            self.userId =   login_response.headers['Set-Cookie'].split('ds_user_id=')[1].split(';')[0]              
            self.cookie = "sessionid=" + self.sessionid + "; csrftoken=" + self.csrf_token + "; ds_user_id=" + self.userId + ";"
            create_cookie = open(self.path+f'//cookie_{self.username}.bot', 'w+', encoding='utf-8')
            create_cookie.write(self.cookie)
            create_cookie.close()
            self.session = requests.session()
            cookie_obj = requests.cookies.create_cookie(
                    name='sessionid', secure=True, value=self.sessionid)
            self.session.cookies.set_cookie(cookie_obj)

        elif os.path.exists(self.path+f'//cookie_{self.username}.bot'):
            try:
                read_cookie = open(self.path+f'//cookie_{self.username}.bot', 'r', encoding='utf-8')
                self.cookie = read_cookie.read()
                read_cookie.close()
                homelink = 'https://www.instagram.com/op/'
                self.session = requests.session()
                self.sessionid = self.cookie.split('=')[1].split(';')[0]
                self.csrf_token = self.cookie.split('=')[2].split(';')[0]
                cookie_obj = requests.cookies.create_cookie(
                    name='sessionid', secure=True, value=self.sessionid)
                self.session.cookies.set_cookie(cookie_obj)
                login_response = self.session.get(homelink, proxies=self.proxy)
                time.sleep(1)
                soup = bs(login_response.text, 'html.parser')
                soup.find("strong", {"class": "-cx-PRIVATE-NavBar__username -cx-PRIVATE-NavBar__username__"}).get_text()
            except AttributeError:
                print(bcolors.FAIL+"[✗] Login Failed! Cookie file is corupted!"+bcolors.ENDC)
                os.remove(self.path+f'//cookie_{self.username}.bot')
                print(bcolors.WARNING+"[-] Deleted Corupted Cookie File! Try Again!"+bcolors.ENDC)
                quit()
            

    def already_liked(self, post_link):
        if post_link.find('/tv/') != -1:
            post_link = post_link.replace('/tv/', '/p/')
        try:
            post_link = post_link.replace(post_link.split('/p/')[1].split('/')[1], '')
        except:
            pass
        resp = self.session.get(post_link, proxies=self.proxy)
        time.sleep(1)
        soup = bs(resp.text, 'html.parser')
        scripts = soup.find_all('script')
        data_script = str(scripts[15])
        time.sleep(1)
        try:
            shortcode = post_link.split('/p/')[1].replace('/', '')
            data_script = data_script.replace(
                f'''<script type="text/javascript">window.__additionalDataLoaded('/p/{shortcode}/',''', '')
        except:
            shortcode = post_link.split('/tv/')[1].replace('/', '')
            data_script = data_script.replace(
                f'''<script type="text/javascript">window.__additionalDataLoaded('/tv/{shortcode}/',''', '')
        data_object = data_script.replace(");</script>", '')
        data_json = json.loads(data_object)
        liked = data_json["graphql"]["shortcode_media"]["viewer_has_liked"]
        
        return bool(liked)

    def like(self, post_link):
        if post_link.find('/tv/') != -1:
            post_link = post_link.replace('/tv/', '/p/')
        try:
            post_link = post_link.replace(post_link.split('/p/')[1].split('/')[1], '')
        except:
            pass
        try:
            if self.already_liked(post_link) == False:
                resp = self.session.get(post_link, proxies=self.proxy)
                time.sleep(1)
                soup = bs(resp.text, 'html.parser')
                scripts = soup.find_all('script')
                data_script = str(scripts[15])
                time.sleep(1)
                try:
                    shortcode = post_link.split('/p/')[1].replace('/', '')
                    data_script = data_script.replace(
                        f'''<script type="text/javascript">window.__additionalDataLoaded('/p/{shortcode}/',''', '')
                except:
                    shortcode = post_link.split('/tv/')[1].replace('/', '')
                    data_script = data_script.replace(
                        f'''<script type="text/javascript">window.__additionalDataLoaded('/tv/{shortcode}/',''', '')
                data_object = data_script.replace(");</script>", '')
                data_json = json.loads(data_object)
                id_post = data_json["graphql"]["shortcode_media"]["id"]
                
                url_post = f"https://www.instagram.com/web/likes/{id_post}/like/"

                headers = {
                    "accept": "*/*",
                    "accept-encoding": "gzip, deflate, br",
                    "accept-language": "en-US,en;q=0.9",
                    "content-length": "0",
                    "content-type": "application/x-www-form-urlencoded",
                    "cookie": self.cookie,
                    "origin": "https://www.instagram.com",
                    "referer": post_link,
                    "sec-fetch-dest": "empty",
                    "sec-fetch-mode": "cors",
                    "sec-fetch-site": "same-origin",
                    "user-agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36",
                    "x-csrftoken": self.csrf_token,
                    "x-ig-app-id": "936619743392459",
                    "x-ig-www-claim": "hmac.AR3dC7naiVtTKkwrEY0hwTO9zj4kLxfvf4Srvp3wFyoZFqSx",
                    "x-instagram-ajax": "d3d3aea32e75",
                    "x-requested-with": "XMLHttpRequest"
                }
                response = requests.request("POST", url_post, headers=headers, proxies=self.proxy)

                if response.status_code != 200:
                    return response.status_code
            else:
                return 208
        except:
            return 403

        return 200

    def unlike(self, post_link):
        if post_link.find('/tv/') != -1:
            post_link = post_link.replace('/tv/', '/p/')
        try:
            post_link = post_link.replace(post_link.split('/p/')[1].split('/')[1], '')
        except:
            pass
        try:
            if self.already_liked(post_link) == True:
                resp = self.session.get(post_link, proxies=self.proxy)
                time.sleep(1)
                soup = bs(resp.text, 'html.parser')
                scripts = soup.find_all('script')
                data_script = str(scripts[15])
                time.sleep(1)
                try:
                    shortcode = post_link.split('/p/')[1].replace('/', '')
                    data_script = data_script.replace(
                        f'''<script type="text/javascript">window.__additionalDataLoaded('/p/{shortcode}/',''', '')
                except:
                    shortcode = post_link.split('/tv/')[1].replace('/', '')
                    data_script = data_script.replace(
                        f'''<script type="text/javascript">window.__additionalDataLoaded('/tv/{shortcode}/',''', '')
                data_object = data_script.replace(");</script>", '')
                data_json = json.loads(data_object)
                id_post = data_json["graphql"]["shortcode_media"]["id"]
                
                url_post = f"https://www.instagram.com/web/likes/{id_post}/unlike/"

                headers = {
                    "accept": "*/*",
                    "accept-encoding": "gzip, deflate, br",
                    "accept-language": "en-US,en;q=0.9",
                    "content-length": "0",
                    "content-type": "application/x-www-form-urlencoded",
                    "cookie": self.cookie,
                    "origin": "https://www.instagram.com",
                    "referer": post_link,
                    "sec-fetch-dest": "empty",
                    "sec-fetch-mode": "cors",
                    "sec-fetch-site": "same-origin",
                    "user-agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36",
                    "x-csrftoken": self.csrf_token,
                    "x-ig-app-id": "936619743392459",
                    "x-ig-www-claim": "hmac.AR3dC7naiVtTKkwrEY0hwTO9zj4kLxfvf4Srvp3wFyoZFqSx",
                    "x-instagram-ajax": "d3d3aea32e75",
                    "x-requested-with": "XMLHttpRequest"
                }
                response = requests.request("POST", url_post, headers=headers, proxies=self.proxy)

                if response.status_code != 200:
                    return response.status_code
            else:
                return 208
                
        except:
            return 403
            
        return 200

    def like_recent(self, username):  
        resp = self.session.get('https://www.instagram.com/'+username+'/', proxies=self.proxy)
        time.sleep(1)
        soup = bs(resp.text, 'html.parser')
        scripts = soup.find_all('script')
        try:
            data_script = str(scripts[4])
            time.sleep(1)
            data_script = data_script.replace(
                '''<script type="text/javascript">window._sharedData = ''', '')
            data_object = data_script.replace(";</script>", '')
            data_json = json.loads(data_object)
        except:
            data_script = str(scripts[3])
            time.sleep(1)
            data_script = data_script.replace(
                '''<script type="text/javascript">window._sharedData = ''', '')
            data_object = data_script.replace(";</script>", '')
            data_json = json.loads(data_object)
        try:
            shortcode = data_json["entry_data"]["ProfilePage"][0]["graphql"]['user']["edge_owner_to_timeline_media"]["edges"][0]["node"]["shortcode"]
            return self.like('https://www.instagram.com/p/'+shortcode+'/')
        except IndexError:
            return 404
        except KeyError:
            return 404

    def comment(self, post_link, comment_text):
        if post_link.find('/tv/') != -1:
            post_link = post_link.replace('/tv/', '/p/')
        try:
            post_link = post_link.replace(post_link.split('/p/')[1].split('/')[1], '')
        except:
            pass
        try:
            resp = self.session.get(post_link, proxies=self.proxy)
            time.sleep(1)
            soup = bs(resp.text, 'html.parser')
            scripts = soup.find_all('script')
            data_script = str(scripts[15])
            time.sleep(1)
            try:
                shortcode = post_link.split('/p/')[1].replace('/', '')
                data_script = data_script.replace(
                    f'''<script type="text/javascript">window.__additionalDataLoaded('/p/{shortcode}/',''', '')
            except:
                shortcode = post_link.split('/tv/')[1].replace('/', '')
                data_script = data_script.replace(
                    f'''<script type="text/javascript">window.__additionalDataLoaded('/tv/{shortcode}/',''', '')
            data_object = data_script.replace(");</script>", '')
            data_json = json.loads(data_object)
            id_post = data_json["graphql"]["shortcode_media"]["id"]

            url_post = f"https://www.instagram.com/web/comments/{id_post}/add/"

            headers = {
                "accept": "*/*",
                "accept-encoding": "gzip, deflate, br",
                "accept-language": "en-US,en;q=0.9",
                "content-length": "39",
                "content-type": "application/x-www-form-urlencoded",
                "cookie": self.cookie,
                "origin": "https://www.instagram.com",
                "referer": post_link,
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "same-origin",
                "user-agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36",
                "x-csrftoken": self.csrf_token,
                "x-ig-app-id": "936619743392459",
                "x-ig-www-claim": "hmac.AR3dC7naiVtTKkwrEY0hwTO9zj4kLxfvf4Srvp3wFyoZFvZV",
                "x-instagram-ajax": "d3d3aea32e75",
                "x-requested-with": "XMLHttpRequest"
            }

            response = requests.request("POST", url_post, headers=headers, data=f"comment_text={comment_text}&replied_to_comment_id=".encode('utf-8'), proxies=self.proxy)
                
            if response.status_code != 200:
                return response.status_code
        except:
            return 403

        return 200

    def comment_recent(self, username, comment_text):  
        resp = self.session.get('https://www.instagram.com/'+username+'/', proxies=self.proxy)
        time.sleep(1)
        soup = bs(resp.text, 'html.parser')
        scripts = soup.find_all('script')
        try:
            data_script = str(scripts[4])
            time.sleep(1)
            data_script = data_script.replace(
                '''<script type="text/javascript">window._sharedData = ''', '')
            data_object = data_script.replace(";</script>", '')
            data_json = json.loads(data_object)
        except:
            data_script = str(scripts[3])
            time.sleep(1)
            data_script = data_script.replace(
                '''<script type="text/javascript">window._sharedData = ''', '')
            data_object = data_script.replace(";</script>", '')
            data_json = json.loads(data_object)
        try:
            shortcode = data_json["entry_data"]["ProfilePage"][0]["graphql"]['user']["edge_owner_to_timeline_media"]["edges"][0]["node"]["shortcode"]
            return self.comment('https://www.instagram.com/p/'+shortcode+'/', comment_text)
        except IndexError:
            return 404
        except KeyError:
            return 404

    def already_followed(self, username):
        resp = self.session.get('https://www.instagram.com/'+username+'/', proxies=self.proxy)
        time.sleep(1)
        soup = bs(resp.text, 'html.parser')
        scripts = soup.find_all('script')
        try:
            data_script = str(scripts[4])
            time.sleep(1)
            data_script = data_script.replace(
                '''<script type="text/javascript">window._sharedData = ''', '')
            data_object = data_script.replace(";</script>", '')
            data_json = json.loads(data_object)
        except:
            data_script = str(scripts[3])
            time.sleep(1)
            data_script = data_script.replace(
                '''<script type="text/javascript">window._sharedData = ''', '')
            data_object = data_script.replace(";</script>", '')
            data_json = json.loads(data_object)
        followed = data_json["entry_data"]["ProfilePage"][0]["graphql"]['user']['followed_by_viewer']
        return bool(followed)

    def follow(self, username):
        try:
            if self.already_followed(username) == False:
                resp = self.session.get('https://www.instagram.com/'+username+'/', proxies=self.proxy)
                time.sleep(1)
                soup = bs(resp.text, 'html.parser')
                scripts = soup.find_all('script')
                try:
                    data_script = str(scripts[4])
                    time.sleep(1)
                    data_script = data_script.replace(
                        '''<script type="text/javascript">window._sharedData = ''', '')
                    data_object = data_script.replace(";</script>", '')
                    data_json = json.loads(data_object)
                except:
                    data_script = str(scripts[3])
                    time.sleep(1)
                    data_script = data_script.replace(
                        '''<script type="text/javascript">window._sharedData = ''', '')
                    data_object = data_script.replace(";</script>", '')
                    data_json = json.loads(data_object)
                id_page = data_json["entry_data"]["ProfilePage"][0]["graphql"]['user']['id']

                url_page = f"https://www.instagram.com/web/friendships/{id_page}/follow/"

                headers = {
                    'accept': '*/*',
                    'accept-encoding': 'gzip, deflate, br',
                    'accept-language': 'en-US,en;q=0.9',
                    'content-length': '0',
                    'content-type': 'application/x-www-form-urlencoded',
                    'cookie': self.cookie,
                    "origin": "https://www.instagram.com",
                    "referer": f"https://www.instagram.com/{username}/",
                    "sec-fetch-dest": "empty",
                    "sec-fetch-mode": "cors",
                    "sec-fetch-site": "same-origin",
                    "user-agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36",
                    "x-csrftoken": self.csrf_token,
                    "x-ig-app-id": "936619743392459",
                    "x-ig-www-claim": "hmac.AR3dC7naiVtTKkwrEY0hwTO9zj4kLxfvf4Srvp3wFyoZFvZV",
                    "x-instagram-ajax": "d3d3aea32e75",
                    "x-requested-with": "XMLHttpRequest"
                }

                response = requests.request("POST", url_page, headers=headers, proxies=self.proxy)
                if response.status_code == 200:
                    return 200
                else:
                    return response.status_code
            else:
                return 208
                
        except KeyError:
            return 404

    def unfollow(self, username):
        try:
            if self.already_followed(username) == True:
                resp = self.session.get('https://www.instagram.com/'+username+'/', proxies=self.proxy)
                time.sleep(1)
                soup = bs(resp.text, 'html.parser')
                scripts = soup.find_all('script')
                try:
                    data_script = str(scripts[4])
                    time.sleep(1)
                    data_script = data_script.replace(
                        '''<script type="text/javascript">window._sharedData = ''', '')
                    data_object = data_script.replace(";</script>", '')
                    data_json = json.loads(data_object)
                except:
                    data_script = str(scripts[3])
                    time.sleep(1)
                    data_script = data_script.replace(
                        '''<script type="text/javascript">window._sharedData = ''', '')
                    data_object = data_script.replace(";</script>", '')
                    data_json = json.loads(data_object)
                id_page = data_json["entry_data"]["ProfilePage"][0]["graphql"]['user']['id']

                url_page = f"https://www.instagram.com/web/friendships/{id_page}/unfollow/"

                headers = {
                    'accept': '*/*',
                    'accept-encoding': 'gzip, deflate, br',
                    'accept-language': 'en-US,en;q=0.9',
                    'content-length': '0',
                    'content-type': 'application/x-www-form-urlencoded',
                    'cookie': self.cookie,
                    "origin": "https://www.instagram.com",
                    "referer": f"https://www.instagram.com/{username}/",
                    "sec-fetch-dest": "empty",
                    "sec-fetch-mode": "cors",
                    "sec-fetch-site": "same-origin",
                    "user-agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36",
                    "x-csrftoken": self.csrf_token,
                    "x-ig-app-id": "936619743392459",
                    "x-ig-www-claim": "hmac.AR3dC7naiVtTKkwrEY0hwTO9zj4kLxfvf4Srvp3wFyoZFvZV",
                    "x-instagram-ajax": "d3d3aea32e75",
                    "x-requested-with": "XMLHttpRequest"
                }

                response = requests.request("POST", url_page, headers=headers, proxies=self.proxy)
                if response.status_code == 200:
                    return 200
                else:
                    return response.status_code
            else:
                return 208
        except KeyError:
            return 404

    def story_view(self, username):
        try:
            resp = self.session.get('https://www.instagram.com/'+username+'/', proxies=self.proxy)
            time.sleep(1)
            soup = bs(resp.text, 'html.parser')
            scripts = soup.find_all('script')
            try:
                data_script = str(scripts[4])
                time.sleep(1)
                data_script = data_script.replace(
                    '''<script type="text/javascript">window._sharedData = ''', '')
                data_object = data_script.replace(";</script>", '')
                data_json = json.loads(data_object)
            except:
                try:
                    data_script = str(scripts[3])
                    time.sleep(1)
                    data_script = data_script.replace(
                        '''<script type="text/javascript">window._sharedData = ''', '')
                    data_object = data_script.replace(";</script>", '')
                    data_json = json.loads(data_object)
                except:
                    return 404
            page_id = data_json["entry_data"]["ProfilePage"][0]["graphql"]['user']['id']
            surl = f'https://www.instagram.com/graphql/query/?query_hash=c9c56db64beb4c9dea2d17740d0259d9&variables=%7B%22reel_ids%22%3A%5B%22{page_id}%22%5D%2C%22tag_names%22%3A%5B%5D%2C%22location_ids%22%3A%5B%5D%2C%22highlight_reel_ids%22%3A%5B%5D%2C%22precomposed_overlay%22%3Afalse%2C%22show_story_viewer_list%22%3Atrue%2C%22story_viewer_fetch_count%22%3A50%2C%22story_viewer_cursor%22%3A%22%22%2C%22stories_video_dash_manifest%22%3Afalse%7D'
            resp = self.session.get(surl, proxies=self.proxy)
            time.sleep(1)
            soup = bs(resp.text, 'html.parser')        
            data_json = json.loads(str(soup))
            story_count =  len(data_json["data"]["reels_media"][0]["items"])

            for i in range(0, story_count):
                id_story = data_json["data"]["reels_media"][0]["items"][i]['id']
                taken_at_timestamp = data_json["data"]["reels_media"][0]["items"][i]['taken_at_timestamp']
                stories_page = f"https://www.instagram.com/stories/reel/seen"

                headers = {
                    'accept': '*/*',
                    'accept-encoding': 'gzip, deflate, br',
                    'accept-language': 'en-US,en;q=0.9',
                    'content-length': '127',
                    'content-type': 'application/x-www-form-urlencoded',
                    'cookie': self.cookie,
                    "origin": "https://www.instagram.com",
                    "referer": f"https://www.instagram.com/stories/{username}/{id_story}/",
                    "sec-fetch-dest": "empty",
                    "sec-fetch-mode": "cors",
                    "sec-fetch-site": "same-origin",
                    "user-agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36",
                    "x-csrftoken": self.csrf_token,
                    "x-ig-app-id": "936619743392459",
                    "x-ig-www-claim": "hmac.AR3dC7naiVtTKkwrEY0hwTO9zj4kLxfvf4Srvp3wFyoZFvZV",
                    "x-instagram-ajax": "d3d3aea32e75",
                    "x-requested-with": "XMLHttpRequest"
                }

                data = {
                    'reelMediaId': id_story,
                    'reelMediaOwnerId': page_id,
                    'reelId': page_id,
                    'reelMediaTakenAt': taken_at_timestamp,
                    'viewSeenAt': taken_at_timestamp
                }

                requests.request("POST", stories_page, headers=headers, data=data, proxies=self.proxy)

        except IndexError:
            return 404
            
        except KeyError:
            return 404
            
        return 200


    def upload_post(self, image_path, caption=''):
        micro_time = int(datetime.now().timestamp())

        headers = {
            "content-type": "image / jpg",
            "content-length": "1",
            "X-Entity-Name": f"fb_uploader_{micro_time}",
            "Offset": "0",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36",
            "x-entity-length": "1",
            "X-Instagram-Rupload-Params": f'{{"media_type": 1, "upload_id": {micro_time}, "upload_media_height": 1080, "upload_media_width": 1080}}',
            "x-csrftoken": self.csrf_token,
            "x-ig-app-id": "1217981644879628",
            "cookie": self.cookie
        }

        upload_response = requests.post(f'https://www.instagram.com/rupload_igphoto/fb_uploader_{micro_time}',
                                        data=open(image_path, "rb"), headers=headers, proxies=self.proxy)

        json_data = json.loads(upload_response.text)
        upload_id = json_data['upload_id']

        if json_data["status"] == "ok":
            url = "https://www.instagram.com/create/configure/"

            payload = 'upload_id=' + upload_id + '&caption=' + caption + '&usertags=&custom_accessibility_caption=&retry_timeout='
            headers = {
                'authority': 'www.instagram.com',
                'x-ig-www-claim': 'hmac.AR2-43UfYbG2ZZLxh-BQ8N0rqGa-hESkcmxat2RqMAXejXE3',
                'x-instagram-ajax': 'adb961e446b7-hot',
                'content-type': 'application/x-www-form-urlencoded',
                'accept': '*/*',
                'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
                'x-requested-with': 'XMLHttpRequest',
                'x-csrftoken': self.csrf_token,
                'x-ig-app-id': '1217981644879628',
                'origin': 'https://www.instagram.com',
                'sec-fetch-site': 'same-origin',
                'sec-fetch-mode': 'cors',
                'sec-fetch-dest': 'empty',
                'referer': 'https://www.instagram.com/create/details/',
                'accept-language': 'en-US,en;q=0.9,fa-IR;q=0.8,fa;q=0.7',
                'cookie': self.cookie
            }

            response = requests.request("POST", url, headers=headers, data=payload, proxies=self.proxy)
            json_data = json.loads(response.text)

            if json_data["status"] == "ok":
                return 200

        else:
            return 400

    def upload_story(self, image_path):
        micro_time = int(datetime.now().timestamp())

        headers = {
            "content-type": "image / jpg",
            "content-length": "1",
            "X-Entity-Name": f"fb_uploader_{micro_time}",
            "Offset": "0",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36",
            "x-entity-length": "1",
            "X-Instagram-Rupload-Params": f'{{"media_type": 1, "upload_id": {micro_time}, "upload_media_height": 1080, "upload_media_width": 1080}}',
            "x-csrftoken": self.csrf_token,
            "x-ig-app-id": "1217981644879628",
            "cookie": self.cookie
        }

        upload_response = requests.post(f'https://www.instagram.com/rupload_igphoto/fb_uploader_{micro_time}',
                                        data=open(image_path, "rb"), headers=headers, proxies=self.proxy)

        json_data = json.loads(upload_response.text)
        upload_id = json_data['upload_id']

        if json_data["status"] == "ok":
            url = "https://www.instagram.com/create/configure_to_story/"

            payload = 'upload_id=' + upload_id + '&caption=&usertags=&custom_accessibility_caption=&retry_timeout='
            headers = {
                'authority': 'www.instagram.com',
                'x-ig-www-claim': 'hmac.AR2-43UfYbG2ZZLxh-BQ8N0rqGa-hESkcmxat2RqMAXejXE3',
                'x-instagram-ajax': 'adb961e446b7-hot',
                'content-type': 'application/x-www-form-urlencoded',
                'accept': '*/*',
                'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
                'x-requested-with': 'XMLHttpRequest',
                'x-csrftoken': self.csrf_token,
                'x-ig-app-id': '1217981644879628',
                'origin': 'https://www.instagram.com',
                'sec-fetch-site': 'same-origin',
                'sec-fetch-mode': 'cors',
                'sec-fetch-dest': 'empty',
                'referer': 'https://www.instagram.com/create/details/',
                'accept-language': 'en-US,en;q=0.9,fa-IR;q=0.8,fa;q=0.7',
                'cookie': self.cookie
            }

            response = requests.request("POST", url, headers=headers, data=payload, proxies=self.proxy)
            json_data = json.loads(response.text)

            if json_data["status"] == "ok":
                return 200

        else:
            return 400

    def hashtag_posts(self, hashtag, limit=20):
        headers = self._get_headers()

        response = self.session.get(f'https://www.instagram.com/graphql/query/?query_hash=9b498c08113f1e09617a1703c22b2f32&variables=%7B%22tag_name%22%3A%22{hashtag}%22%2C%22first%22%3A{limit}%7D', headers=headers, proxies=self.proxy).text
        post_count = len(json.loads(response)['data']['hashtag']['edge_hashtag_to_media']['edges'])

        if limit > post_count:
            limit = post_count

        links=[]
        for i in range(0, limit):
            links.append('https://instagram.com/p/'+json.loads(response)['data']['hashtag']['edge_hashtag_to_media']['edges'][i]['node']['shortcode'])

        return links

    def location_posts(self, location_url, limit=20):
        id_location = location_url.split('/locations/')[1].split('/')[0]
        headers = self._get_headers()

        response = self.session.get(f'https://www.instagram.com/graphql/query/?query_hash=36bd0f2bf5911908de389b8ceaa3be6d&variables=%7B%22id%22%3A%22{id_location}%22%2C%22first%22%3A{limit}%7D', headers=headers, proxies=self.proxy).text
        post_count = len(json.loads(response)['data']['location']['edge_location_to_media']['edges'])

        if limit > post_count:
            limit = post_count

        links=[]
        for i in range(0, limit):
            links.append('https://instagram.com/p/'+json.loads(response)['data']['location']['edge_location_to_media']['edges'][i]['node']['shortcode'])

        return links

    def user_posts_count(self, username):
        headers = self._get_headers()

        response = self.session.get(f'https://www.instagram.com/{username}/?__a=1', headers=headers, proxies=self.proxy).text
        post_count = json.loads(response)['graphql']['user']['edge_owner_to_timeline_media']['count']

        return post_count

    def user_followers_count(self, username):
        headers = self._get_headers()

        response = self.session.get(f'https://www.instagram.com/{username}/?__a=1', headers=headers, proxies=self.proxy).text
        followers_count = json.loads(response)['graphql']['user']['edge_followed_by']['count']

        return followers_count

    def user_follow_count(self, username):
        headers = self._get_headers()

        response = self.session.get(f'https://www.instagram.com/{username}/?__a=1', headers=headers, proxies=self.proxy).text
        follow_count = json.loads(response)['graphql']['user']['edge_follow']['count']

        return follow_count

    def like_count(self, post_link):
        if post_link.find('/tv/') != -1:
            post_link = post_link.replace('/tv/', '/p/')
        try:
            post_link = post_link.replace(post_link.split('/p/')[1].split('/')[1], '')
        except:
            pass
        headers = self._get_headers()

        if post_link[-1] == '/':
            post_link = post_link[:-1]

        response = self.session.get(f'{post_link}/?__a=1', headers=headers, proxies=self.proxy).text
        like_count = json.loads(response)['graphql']['shortcode_media']['edge_media_preview_like']['count']

        return like_count

    def comment_count(self, post_link):
        if post_link.find('/tv/') != -1:
            post_link = post_link.replace('/tv/', '/p/')
        try:
            post_link = post_link.replace(post_link.split('/p/')[1].split('/')[1], '')
        except:
            pass
        headers = self._get_headers()

        if post_link[-1] == '/':
            post_link = post_link[:-1]

        response = self.session.get(f'{post_link}/?__a=1', headers=headers, proxies=self.proxy).text
        comment_count = json.loads(response)['graphql']['shortcode_media']['edge_media_preview_comment']['count']

        return comment_count
        
    def user_posts(self, username, limit=50):
        posts_have = self.user_posts_count(username)
        
        if posts_have < limit:
            limit=posts_have

        limit_k=limit
        headers = self._get_headers()

        response = self.session.get(f'https://www.instagram.com/{username}/?__a=1', headers=headers, proxies=self.proxy).text
        user_id = json.loads(response)['graphql']['user']['id']

        links=[]

        response = self.session.get(f'https://www.instagram.com/graphql/query/?query_hash=003056d32c2554def87228bc3fd9668a&variables=%7B%22id%22%3A%22{user_id}%22%2C%22first%22%3A{limit}%7D', headers=headers, proxies=self.proxy).text
        post_count = len(json.loads(response)['data']['user']['edge_owner_to_timeline_media']['edges'])

        if limit > post_count:
            limit = post_count

        for i in range(0, limit):
            links.append('https://instagram.com/p/'+json.loads(response)['data']['user']['edge_owner_to_timeline_media']['edges'][i]['node']['shortcode'])

        if limit_k > 50:
            limit = limit_k - 50
            limit_k = limit
            while limit_k > 0:
                try:
                    after = json.loads(response)['data']['user']['edge_owner_to_timeline_media']['page_info']['end_cursor']
                    response = self.session.get(f'https://www.instagram.com/graphql/query/?query_hash=003056d32c2554def87228bc3fd9668a&variables=%7B%22id%22%3A%22{user_id}%22%2C%22first%22%3A50%2C%22after%22%3A%22{after.replace("==","")}%3D%3D%22%7D', headers=headers, proxies=self.proxy).text
                    post_count = len(json.loads(response)['data']['user']['edge_owner_to_timeline_media']['edges'])

                    if limit > post_count:
                        limit = post_count

                    limit_k -= limit
                    for i in range(0, limit):
                        links.append('https://instagram.com/p/'+json.loads(response)['data']['user']['edge_owner_to_timeline_media']['edges'][i]['node']['shortcode'])
                    limit = limit_k
                except:
                    break
        return links

    def user_follows(self, username, limit=49):
        followed = self.user_follow_count(username)
        
        if followed < limit:
            limit=followed

        limit_k=limit
        headers = self._get_headers()

        response = self.session.get(f'https://www.instagram.com/{username}/?__a=1', headers=headers, proxies=self.proxy).text
        user_id = json.loads(response)['graphql']['user']['id']

        usernames=[]

        response = self.session.get(f'https://www.instagram.com/graphql/query/?query_hash=d04b0a864b4b54837c0d870b0e77e076&variables=%7B%22id%22%3A%22{user_id}%22%2C%22first%22%3A{limit}%7D', headers=headers, proxies=self.proxy).text
        follow_count = len(json.loads(response)['data']['user']['edge_follow']['edges'])

        if limit > follow_count:
            limit = follow_count

        for i in range(0, limit):
            usernames.append(json.loads(response)['data']['user']['edge_follow']['edges'][i]['node']['username'])

        if limit_k > 49:
            limit = limit_k - 49
            limit_k = limit
            while limit_k > 0:
                try:
                    after = json.loads(response)['data']['user']['edge_follow']['page_info']['end_cursor']
                    response = self.session.get(f'https://www.instagram.com/graphql/query/?query_hash=d04b0a864b4b54837c0d870b0e77e076&variables=%7B%22id%22%3A%22{user_id}%22%2C%22first%22%3A50%2C%22after%22%3A%22{after.replace("==","")}%3D%3D%22%7D', headers=headers, proxies=self.proxy).text
                    follow_count = len(json.loads(response)['data']['user']['edge_follow']['edges'])

                    if limit > follow_count:
                        limit = follow_count

                    limit_k -= limit
                    for i in range(0, limit):
                        usernames.append(json.loads(response)['data']['user']['edge_follow']['edges'][i]['node']['username'])
                    limit = limit_k
                except:
                    break
        return usernames

    def user_followers(self, username, limit=49):
        follower = self.user_followers_count(username)
        
        if follower < limit:
            limit=follower

        limit_k=limit
        headers = self._get_headers()

        response = self.session.get(f'https://www.instagram.com/{username}/?__a=1', headers=headers, proxies=self.proxy).text
        user_id = json.loads(response)['graphql']['user']['id']

        usernames=[]

        response = self.session.get(f'https://www.instagram.com/graphql/query/?query_hash=c76146de99bb02f6415203be841dd25a&variables=%7B%22id%22%3A%22{user_id}%22%2C%22first%22%3A{limit}%7D', headers=headers, proxies=self.proxy).text
        follower_count = len(json.loads(response)['data']['user']['edge_followed_by']['edges'])

        if limit > follower_count:
            limit = follower_count

        for i in range(0, limit):
            usernames.append(json.loads(response)['data']['user']['edge_followed_by']['edges'][i]['node']['username'])

        if limit_k > 49:
            limit = limit_k - 49
            limit_k = limit
            while limit_k > 0:
                try:
                    after = json.loads(response)['data']['user']['edge_followed_by']['page_info']['end_cursor']
                    response = self.session.get(f'https://www.instagram.com/graphql/query/?query_hash=c76146de99bb02f6415203be841dd25a&variables=%7B%22id%22%3A%22{user_id}%22%2C%22first%22%3A50%2C%22after%22%3A%22{after.replace("==","")}%3D%3D%22%7D', headers=headers, proxies=self.proxy).text
                    follower_count = len(json.loads(response)['data']['user']['edge_followed_by']['edges'])

                    if limit > follower_count:
                        limit = follower_count

                    limit_k -= limit
                    for i in range(0, limit):
                        usernames.append(json.loads(response)['data']['user']['edge_followed_by']['edges'][i]['node']['username'])
                    limit = limit_k
                except:
                    break
        return usernames

    def post_likers(self, post_link, limit=50):
        if post_link.find('/tv/') != -1:
            post_link = post_link.replace('/tv/', '/p/')
        try:
            post_link = post_link.replace(post_link.split('/p/')[1].split('/')[1], '')
        except:
            pass
        likers = self.like_count(post_link)
        
        if likers < limit:
            limit=likers

        limit_k=limit
        headers = self._get_headers()

        shortcode = post_link.split('/p/')[1].replace('/', '')
        usernames=[]

        response = self.session.get(f'https://www.instagram.com/graphql/query/?query_hash=d5d763b1e2acf209d62d22d184488e57&variables=%7B%22shortcode%22%3A%22{shortcode}%22%2C%22first%22%3A{limit}%7D', headers=headers, proxies=self.proxy).text
        like_count = len(json.loads(response)['data']['shortcode_media']['edge_liked_by']['edges'])

        if limit > like_count:
            limit = like_count

        for i in range(0, limit):
            usernames.append(json.loads(response)['data']['shortcode_media']['edge_liked_by']['edges'][i]['node']['username'])

        if limit_k > 50:
            limit = limit_k - 50
            limit_k = limit
            while limit_k > 0:
                try:
                    after = json.loads(response)['data']['shortcode_media']['edge_liked_by']['page_info']['end_cursor']
                    response = self.session.get(f'https://www.instagram.com/graphql/query/?query_hash=d5d763b1e2acf209d62d22d184488e57&variables=%7B%22shortcode%22%3A%22{shortcode}%22%2C%22first%22%3A50%2C%22after%22%3A%22{after.replace("==","")}%3D%3D%22%7D', headers=headers, proxies=self.proxy).text
                    like_count = len(json.loads(response)['data']['shortcode_media']['edge_liked_by']['edges'])

                    if limit > like_count:
                        limit = like_count
                    
                    limit_k -= limit
                    for i in range(0, limit):
                        usernames.append(json.loads(response)['data']['shortcode_media']['edge_liked_by']['edges'][i]['node']['username'])
                    limit = limit_k
                except:
                    break
        return usernames

    def post_commenters(self, post_link, limit=50):
        if post_link.find('/tv/') != -1:
            post_link = post_link.replace('/tv/', '/p/')
        try:
            post_link = post_link.replace(post_link.split('/p/')[1].split('/')[1], '')
        except:
            pass
        commenters = self.comment_count(post_link)
        
        if commenters < limit:
            limit=commenters

        limit_k=limit
        headers = self._get_headers()

        shortcode = post_link.split('/p/')[1].replace('/', '')

        usernames=[]

        response = self.session.get(f'https://www.instagram.com/graphql/query/?query_hash=bc3296d1ce80a24b1b6e40b1e72903f5&variables=%7B%22shortcode%22%3A%22{shortcode}%22%2C%22first%22%3A{limit}%7D', headers=headers, proxies=self.proxy).text
        comment_count = len(json.loads(response)['data']['shortcode_media']['edge_media_to_parent_comment']['edges'])

        if limit > comment_count:
            limit = comment_count

        for i in range(0, limit):
            usernames.append(json.loads(response)['data']['shortcode_media']['edge_media_to_parent_comment']['edges'][i]['node']['owner']['username'])

        if limit_k > 50:
            limit = limit_k - 50
            limit_k = limit
            while limit_k > 0:
                try:
                    response = self.session.get('https://www.instagram.com/graphql/query/?query_hash=bc3296d1ce80a24b1b6e40b1e72903f5&variables={%22shortcode%22:%22'+shortcode+'%22,%22first%22:50,%22after%22:'+json.dumps(json.loads(response)['data']['shortcode_media']['edge_media_to_parent_comment']['page_info']['end_cursor'])+'}', headers=headers, proxies=self.proxy).text
                    comment_count = len(json.loads(response)['data']['shortcode_media']['edge_media_to_parent_comment']['edges'])

                    if limit > comment_count:
                        limit = comment_count
                    
                    limit_k -= limit
                    for i in range(0, limit):
                        usernames.append(json.loads(response)['data']['shortcode_media']['edge_media_to_parent_comment']['edges'][i]['node']['owner']['username'])
                    limit = limit_k
                except:
                    break
        return usernames

    def feed_posts(self):
        headers = self._get_headers()
        response = self.session.get('https://www.instagram.com/graphql/query/?query_hash=c699b185975935ae2a457f24075de8c7', headers=headers, proxies=self.proxy).text

        post_count = len(json.loads(response)['data']['user']['edge_web_feed_timeline']['edges'])
        feed_posts = []
        for i in range(0, post_count):
            feed_posts.append('https://instagram.com/p/'+json.loads(response)['data']['user']['edge_web_feed_timeline']['edges'][i]['node']['shortcode'])

        return feed_posts

    def post_owner(self, post_link):
        if post_link.find('/tv/') != -1:
            post_link = post_link.replace('/tv/', '/p/')
        try:
            post_link = post_link.replace(post_link.split('/p/')[1].split('/')[1], '')
        except:
            pass
        headers = self._get_headers()

        if post_link[-1] == '/':
            post_link = post_link[:-1]

        response = self.session.get(f'{post_link}/?__a=1', headers=headers, proxies=self.proxy).text
        owner = json.loads(response)['graphql']['shortcode_media']['owner']['username']

        return owner

    def post_caption(self, post_link):
        if post_link.find('/tv/') != -1:
            post_link = post_link.replace('/tv/', '/p/')
        try:
            post_link = post_link.replace(post_link.split('/p/')[1].split('/')[1], '')
        except:
            pass
        headers = self._get_headers()

        if post_link[-1] == '/':
            post_link = post_link[:-1]

        response = self.session.get(f'{post_link}/?__a=1', headers=headers, proxies=self.proxy).text
        caption = json.loads(response)['graphql']['shortcode_media']['edge_media_to_caption']['edges'][0]['node']['text']

        return caption

    def post_location(self, post_link):
        if post_link.find('/tv/') != -1:
            post_link = post_link.replace('/tv/', '/p/')
        try:
            post_link = post_link.replace(post_link.split('/p/')[1].split('/')[1], '')
        except:
            pass
        headers = self._get_headers()

        if post_link[-1] == '/':
            post_link = post_link[:-1]

        response = self.session.get(f'{post_link}/?__a=1', headers=headers, proxies=self.proxy).text
        location = {"id": json.loads(response)['graphql']['shortcode_media']['location']['id'], "name": json.loads(response)['graphql']['shortcode_media']['location']['name']}

        return location

    def post_hashtags(self, post_link):
        if post_link.find('/tv/') != -1:
            post_link = post_link.replace('/tv/', '/p/')
        try:
            post_link = post_link.replace(post_link.split('/p/')[1].split('/')[1], '')
        except:
            pass
        hashtag_filter = self.post_caption(post_link).replace('\n', ' ').split()
        hashtags=[]
        for hashtag in hashtag_filter:
            if hashtag.startswith('#'):
                hashtags.append(hashtag)

        return hashtags


    def post_tagged_user(self, post_link):
        if post_link.find('/tv/') != -1:
            post_link = post_link.replace('/tv/', '/p/')
        try:
            post_link = post_link.replace(post_link.split('/p/')[1].split('/')[1], '')
        except:
            pass
        headers = self._get_headers()

        if post_link[-1] == '/':
            post_link = post_link[:-1]
        
        tagged_users = []
        try:
            response = self.session.get(f'{post_link}/?__a=1', headers=headers, proxies=self.proxy).text
            tag_count = len(json.loads(response)['graphql']['shortcode_media']['edge_sidecar_to_children']['edges'][0]['node']['edge_media_to_tagged_user']['edges'])

            for i in range(0, tag_count):
                tagged_users.append(json.loads(response)['graphql']['shortcode_media']['edge_sidecar_to_children']['edges'][0]['node']['edge_media_to_tagged_user']['edges'][i]['node']['user']['username'])
        except:
            try:
                response = self.session.get(f'{post_link}/?__a=1', headers=headers, proxies=self.proxy).text
                tag_count = len(json.loads(response)['graphql']['shortcode_media']['edge_media_to_tagged_user']['edges'])

                for i in range(0, tag_count):
                    tagged_users.append(json.loads(response)['graphql']['shortcode_media']['edge_media_to_tagged_user']['edges'][i]['node']['user']['username'])
            except:
                pass

        return tagged_users

    def post_time(self, post_link):
        if post_link.find('/tv/') != -1:
            post_link = post_link.replace('/tv/', '/p/')
        try:
            post_link = post_link.replace(post_link.split('/p/')[1].split('/')[1], '')
        except:
            pass
        headers = self._get_headers()

        if post_link[-1] == '/':
            post_link = post_link[:-1]

        response = self.session.get(f'{post_link}/?__a=1', headers=headers, proxies=self.proxy).text
        time = {"timestamp": json.loads(response)['graphql']['shortcode_media']['taken_at_timestamp'], "datetime": str(datetime.fromtimestamp(json.loads(response)['graphql']['shortcode_media']['taken_at_timestamp']))}

        return time

    def post_type(self, post_link):
        if post_link.find('/tv/') != -1:
            post_link = post_link.replace('/tv/', '/p/')
        try:
            post_link = post_link.replace(post_link.split('/p/')[1].split('/')[1], '')
        except:
            pass
        headers = self._get_headers()

        if post_link[-1] == '/':
            post_link = post_link[:-1]

        response = self.session.get(f'{post_link}/?__a=1', headers=headers, proxies=self.proxy).text
        if bool(json.loads(response)['graphql']['shortcode_media']['is_video']):
            post_type='video'
        else:
            post_type='picture'

        return post_type

    def video_views_count(self, post_link):
        if post_link.find('/tv/') != -1:
            post_link = post_link.replace('/tv/', '/p/')
        try:
            post_link = post_link.replace(post_link.split('/p/')[1].split('/')[1], '')
        except:
            pass
        if self.post_type(post_link) == 'video':
            headers = self._get_headers()

            if post_link[-1] == '/':
                post_link = post_link[:-1]

            response = self.session.get(f'{post_link}/?__a=1', headers=headers, proxies=self.proxy).text
            view_count = json.loads(response)['graphql']['shortcode_media']['video_view_count']

            return view_count
        
    def followed_by_me(self, username):
        headers = self._get_headers()

        response = self.session.get(f'https://www.instagram.com/{username}/?__a=1', headers=headers, proxies=self.proxy).text
        followed_by_viewer = bool(json.loads(response)['graphql']['user']['followed_by_viewer'])

        return followed_by_viewer
        
    def follows_me(self, username):
        headers = self._get_headers()

        response = self.session.get(f'https://www.instagram.com/{username}/?__a=1', headers=headers, proxies=self.proxy).text
        follows_viewer = bool(json.loads(response)['graphql']['user']['follows_viewer'])

        return follows_viewer

    def user_external_url(self, username):
        headers = self._get_headers()

        response = self.session.get(f'https://www.instagram.com/{username}/?__a=1', headers=headers, proxies=self.proxy).text
        url = json.loads(response)['graphql']['user']['external_url']

        return url

    def verified_user(self, username):
        headers = self._get_headers()

        response = self.session.get(f'https://www.instagram.com/{username}/?__a=1', headers=headers, proxies=self.proxy).text
        is_verified = bool(json.loads(response)['graphql']['user']['is_verified'])

        return is_verified

    def private_user(self, username):
        headers = self._get_headers()

        response = self.session.get(f'https://www.instagram.com/{username}/?__a=1', headers=headers, proxies=self.proxy).text
        is_private = bool(json.loads(response)['graphql']['user']['is_private'])

        return is_private

    def user_bio(self, username):
        headers = self._get_headers()

        response = self.session.get(f'https://www.instagram.com/{username}/?__a=1', headers=headers, proxies=self.proxy).text
        bio = json.loads(response)['graphql']['user']['biography']

        return bio

    def user_dp(self, username):
        headers = self._get_headers()

        response = self.session.get(f'https://www.instagram.com/{username}/?__a=1', headers=headers, proxies=self.proxy).text
        dp_url = json.loads(response)['graphql']['user']['profile_pic_url_hd']

        return dp_url
    
    def _get_headers(self, options=None):
        if options is None:
            options = dict()

        headers = {
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US,en;q=0.9",
            "content-length": "0",
            "content-type": "application/x-www-form-urlencoded",
            "cookie": self.cookie,
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36",
            "x-csrftoken": self.csrf_token,
            "x-ig-app-id": "936619743392459",
            "x-ig-www-claim": "hmac.AR3dC7naiVtTKkwrEY0hwTO9zj4kLxfvf4Srvp3wFyoZFqSx",
            "x-instagram-ajax": "d3d3aea32e75",
            "x-requested-with": "XMLHttpRequest"
        }
        
        for key, value in options.items():
            headers[key] = value
        
        return headers
