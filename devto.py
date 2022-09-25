import requests

class DevtoPoster:
    def __init__(self, token, domain):
        self._token = token
        self._domain = domain
        self._endpoint = "https://dev.to/api/"
        self._headers = {
            "Accept": "application/json",
            "api-key": self._token,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36",
        }
        self._session = self._create_devto_session()

    def _create_devto_session(self):
        session = requests.session()
        session.headers.update(self._headers)
        return session

    def create_post_devto(
        self,
        title,
        body_markdown,
        published=False,
        series="",
        main_image="",
        canonical_url="",
        description="",
        tags=[],
    ):
        data = {
            "article": {
                "title": title,
                "body_markdown": body_markdown,
                "published": published,
                "tags": tags,
            }
        }
        if canonical_url:
            data["article"]["canonical_url"] = canonical_url
        if main_image:
            data["article"]["main_image"] = main_image
        if series:
            data["article"]["series"] = series
        if description:
            data["article"]["description"] = description

        response = self._session.post(f"{self._endpoint}articles", json=data)
        if response.status_code == 201:
            return 'https://dev.to/dashboard'
        else: 
            return 'ERROR'