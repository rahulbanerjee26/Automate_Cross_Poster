import requests


class HashnodePoster:
    def __init__(self, token, domain):
        self._token = token
        self._endpoint = "https://api.hashnode.com"
        self._domain = domain
        self._headers = {"Authorization": self._token}
        self._session = self._create_hashnode_session()

    def _create_hashnode_session(self):
        session = requests.session()
        session.headers.update(self._headers)
        return session

    def create_post_hashnode(
        self,
        title,
        content,
        publicationID,
        tags=[],
        canonicalUrl="",
        hideFromHashnodeFeed=True,
    ):
        query = """
        mutation createPublicationStory($input: CreateStoryInput!,$publicationId: String!,$hideFromHashnodeFeed: Boolean) {
          createPublicationStory(input: $input,publicationId: $publicationId, hideFromHashnodeFeed: $hideFromHashnodeFeed) {
            code
            success
            message,
            post{
              type,
              isDelisted,
              isActive,
              slug,
              cuid,
              _id,
            }
          }
        }
      """

        variables = {
            "input": {
                "title": title,
                "contentMarkdown": content,
                "tags": [{"_id": tag, "slug": tag, "name": tag} for tag in tags],
                "isRepublished": {"originalArticleURL": canonicalUrl},
            },
            "publicationId": publicationID,
            "hideFromHashnodeFeed": hideFromHashnodeFeed,
        }

        response = requests.post(
            self._endpoint,
            json={"query": query, "variables": variables},
            headers=self._headers,
        )

        return self._domain + response.json()["data"]["createPublicationStory"]["post"]["slug"]
