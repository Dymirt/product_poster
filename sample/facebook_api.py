from facebook import GraphAPI


class FacebookPage:
    def __init__(self, user_access_token, page_id):
        self.__user_access_token = user_access_token
        self.__page_id = page_id
        self.__page_graph = GraphAPI(access_token=self.__get_page_access_token())

    def __get_page_access_token(self):
        graph = GraphAPI(access_token=self.__user_access_token)
        return graph.get_object(self.__page_id, fields="access_token")["access_token"]

    def put_object(self, link, message=""):
        self.__page_graph.put_object(
            self.__page_id, connection_name="feed", link=link, message=message
        )

    def get_page_id(self):
        return self.__page_id
