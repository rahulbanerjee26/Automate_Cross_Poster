import requests
import base64

"""
Wordpress Class
"""


class WordpressPoster:
    def __init__(self, domain, username, password) -> None:
        self._domain = domain
        self._endpoint = f'{self._domain}wp-json/wp/v2/'
        self._username = username
        self._password = password
        self._credentials = f"{self._username}:{self._password}"
        self._token = base64.b64encode(self._credentials.encode())
        self._headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36",
            "Authorization": "Basic " + self._token.decode("utf-8"),
        }
        self.session = self._create_wp_session()

    def _create_wp_session(self):
        session = requests.session()
        session.headers.update(self._headers)
        return session

    def get_category_ids(self, categories):
        category_ids = []
        category_endpoint = f"{self._endpoint}categories"
        for category in categories:
            response = self.session.post(category_endpoint, json={"name": category})
            # The term already exists
            if "data" in response.json():
                category_ids.append(response.json()["data"]["term_id"])
            elif "id" in response.json():
                category_ids.append(response.json()["id"])

        return category_ids

    def get_tag_ids(self, tags):
        tag_ids = []
        tags_endpoint = f"{self._endpoint}tags"
        for tag in tags:
            response = self.session.post(tags_endpoint, json={"name": tag})

            # The term already exists
            if "data" in response.json():
                tag_ids.append(response.json()["data"]["term_id"])
            elif "id" in response.json():
                tag_ids.append(response.json()["id"])

        return tag_ids

    def upload_media(self, filePath, alt_text="", caption=""):
        new_session = self.session
        data = open(filePath, "rb").read()
        new_session.headers.update(
            {
                "Content-Type": "",
                "Content-Disposition": f'attachment; filename="{filePath}"',
            }
        )

        upload_media_endpoint = f"{self._endpoint}media"

        response = new_session.post(
            upload_media_endpoint,
            json={"alt_text": alt_text, "caption": caption},
            data=data,
        )
        return response.json()["id"]

    def create_post_wordpress(
        self,
        title,
        content,
        publish_status="draft",
        categories=[],
        tags=[],
        featuredImageId=None,
    ):
        response = self.session.post(
            f"{self._endpoint}posts",
            json={
                "title": title,
                "content": content,
                "status": publish_status,
                "categories": categories,
                "tags": tags,
                "featured_media": featuredImageId,
            },
        )

        return response.json()
