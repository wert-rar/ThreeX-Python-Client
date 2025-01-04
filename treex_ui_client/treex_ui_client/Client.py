import json
import logging

from logging import Logger

from aiohttp import InvalidURL
from requests import Session, Response

from treex_ui_client.treex_ui_client.default_payload import DefaultPayload
from treex_ui_client.treex_ui_client.payload import Payload
from treex_ui_client.treex_ui_client.errors import ClientError


class Client3XUI:
    def __init__(self, login, password, login_key,
                 panel_host, root_url,
                 sub_host, sub_path,
                 inbound_id,
                 panel_port=None, sub_port=None, logging_enabled=False):

        self.inbound = inbound_id

        self.login_payload = {
            "username": login,
            "password": password,
            "loginSecret": login_key
        }


        self.base_url = f'https://{panel_host}:{panel_port}/{root_url}' if panel_port else f'https://{panel_host}/{root_url}'
        self.sub_url = f'https://{sub_host}:{sub_port}/{sub_path}/' if sub_port else f'https://{sub_host}/{sub_path}/'

        self.logger: Logger | None = None

        if logging_enabled:

            self.logger = logging.getLogger(__name__)
            self.logger.setLevel(logging.INFO)
            self.logger.formatter = logging.Formatter('%(ascitime)s - %(name)s - %(levelname)s - %(message)s')

            self.logger.info('Client logging enabled\n')
            self.logger.info(f'Panel base url : {self.base_url}\n')
            self.logger.info(f'Panel sub url : {self.sub_url}\n')
            self.logger.info('Client initialization complete')
            self.logger.info('Starting client session\n')

        self.session = self.__get_session()

        if self.session is None:
            raise ClientError('Failed to set client session')



    def __del__(self):
        """Close the session"""
        if self.session:
            self.session.close()
            if self.logger:
                self.logger.info('Client session closed')

    def __get_session(self) -> Session:
        """Get client session"""
        try:
            session: Session = Session()
            with session.post(f'{self.base_url}/login', data=self.login_payload) as response:
                if response.status_code == 200:

                    if self.logger:
                        self.logger.info('Set client session')
                    return session
                else:
                    raise ClientError('Failed to set client session. Wrong status :', str(response.status_code))

        except InvalidURL as e:
            if self.logger:
                self.logger.error(f'Invalid URL: {repr(e)}')
            raise ClientError('Invalid URL', 0)

        except ClientError as e:
            if self.logger:
                self.logger.error(repr(e))
            raise e

        except Exception as e:
            if self.logger:
                self.logger.error(f'Failed to set client session.\nError: {repr(e)}')
            raise ClientError('Failed to set client session \nError: {repr(e)}', 0)

    def __post_request(self, url: str, payload: Payload | None) -> Response:
        """
            Sends an asynchronous POST request to a specified URL with the given payload.

            This function handles the login process before sending the request and ensures
            the session is closed after the request is completed.


            :param url: str : The URL to which the POST request is sent.
            :param payload: Payload: The data to be sent in the body of the POST request.

            :return resp: Responce : The response object from the POST request.

            :raise: ClientError: If there is an issue connecting to the panel or if the client encounters an error.
        """


        try:
            resp = self.session.post(url, data=payload.format())
            if self.logger:
                self.logger.info(f'POST {url} [{resp.status_code}]')
            return resp

        except Exception as e:
            if self.logger:
                self.logger.error(f'Failed to send POST request.\nUrl: {url}\nPayload : {payload}\nError: {repr(e)}')
            raise ClientError('Client error: ' + repr(e), 0)

    def __get_request(self, url: str) -> Response:
        """
        Sends an asynchronous GET request to a specified URL.

        This function handles the login process before sending the request and ensures
        the session is closed after the request is completed.

        Parameters:
        :param url: str:  The URL to which the GET request is sent.

        :return resp: Response : The response object from the GET request.

        :raise ClientError : If there is an issue connecting to the panel or if the client encounters an error.
        """
        try:
            resp = self.session.get(url)
            if self.logger:
                self.logger.info(f'GET {url} [{resp.status_code}]')
            return resp
        except Exception as e:
            raise ClientError('Client error: ' + repr(e), 0)

    def add_client_to_inbound(self, payload: DefaultPayload, inbound_id=None) -> str:
        """
        Adds a client to the specified inbound.


        :param payload: DefaultPayload : The payload containing the client's details.
        :param inbound_id:int:  Inbound id, if None then uses self.inbound
        :return sublink: str : A sublink
        """

        if inbound_id is None:
            inbound_id = self.inbound
        else:
            # add warning about weak inbound_id
            if self.logger:
                self.logger.warning(f'Using weak inbound_id: {inbound_id}. Consider using the inbound id of client')

        post_request_url = f"https://{self.base_url}/panel/api/inbounds/{inbound_id}/addClient"
        resp = self.__post_request(post_request_url, payload)
        if resp.ok:
            sublink = self.sub_url + payload.settings[0]["subID"]  # ссылка на подписку
            return sublink

    def get_clients_in_inbound(self, inbound_id=None) -> list:
        """
        Getting all clients on inbound
        :param inbound_id:int : inbound id, if None then uses self.inbound
        :return: clients:  List of clients
        """

        if inbound_id is None:
            inbound_id = self.inbound
        else:
            # add warning about weak inbound_id
            if self.logger:
                self.logger.warning(f'Using weak inbound_id: {inbound_id}. Consider using the inbound id of client')

        get_request_url = f'{self.base_url}//panel/api/inbounds/get/{inbound_id}'

        resp = self.__get_request(get_request_url)
        data = resp.text

        if resp.ok:
            data = json.loads(data)
            data = json.loads(data['obj']['settings'])
            clients = data['clients']
            return clients  # возвращает список клиентов

    def delete_client(self, client_id: str, inbound_id=None) -> None:
        """
        Deleting a client by its client_id
        :param inbound_id:int : inbound id, if None then uses self.inbound
        :param client_id:str :  Client id
        """
        if inbound_id is None:
            inbound_id = self.inbound
        else:
            # add warning about weak inbound_id
            if self.logger:
                self.logger.warning(f'Using weak inbound_id: {inbound_id}. Consider using the inbound id of client')

        post_request_url = f"{self.base_url}/panel/api/inbounds/{inbound_id}/delClient/{client_id}"

        resp = self.__post_request(post_request_url, None)
        text = resp.text

        if resp.ok:
            print(text)

    def delete_depleted_clients(self, inbound_id=None) -> None:
        """
        Deleting clients whose key has expired
        (it can be used to clean keys when, for example, 60 days are not extended)
        """
        if inbound_id is None:
            inbound_id = self.inbound
        else:
            # add warning about weak inbound_id
            if self.logger:
                self.logger.warning(f'Using weak inbound_id: {inbound_id}. Consider using the inbound id of client')

        post_request_url = f'{self.base_url}/panel/api/inbounds/delDepletedClients/{inbound_id}'

        self.__post_request(post_request_url, None)

    def update_client(self, client_id: str, payload: DefaultPayload) -> str:
        """
        Update client info in inbound

        :param client_id:str : Client id
        :param payload: DefaultPayload : New client info

        :return: sublink: str :   Link to the subscription
        """
        post_request_url = f'{self.base_url}/panel/api/inbounds/updateClient/{client_id}'
        resp = self.__post_request(post_request_url, payload)

        if resp.ok:
            return self.sub_url + payload.settings[0]["subID"]

    def info_about_client(self, client_id: str) -> dict | None:
        """
           Fetches and returns the enable status and total traffic of a specific client key.

           :param client_id:str : Client id

           :return info: dict: A info about key

        """
        get_request_url = f'{self.base_url}/panel/api/inbounds/getClientTrafficsById/{client_id}'
        resp = self.__get_request(get_request_url)
        data = resp.text
        if resp.ok:
            data = json.loads(data)['obj'][0]
            return data
        else:
            return None

    def info_about_all_clients(self, inbound_id=None) -> list[str]:
        """
          Fetches and returns the enable status of specific client keys.

          :return list[str]: A list of enable statuses for the specified client keys.

        """
        if inbound_id is None:
            inbound_id = self.inbound
        else:
            # add warning about weak inbound_id
            if self.logger:
                self.logger.warning(f'Using weak inbound_id: {inbound_id}. Consider using the inbound id of client')

        info = []
        get_request_url = f"{self.base_url}/panel/api/inbounds/get/{inbound_id}"
        resp = self.__get_request(get_request_url)
        data = resp.text
        if resp.ok:
            data = json.loads(data)['obj']['settings']
            data = json.loads(data)['clients']
            for client in data:
                info.append(client)

        return info

    def info_about_clients(self, client_ids: list[str]) -> list[str]:
        """
        Fetches and returns the enable status of specific client keys.

        :param client_ids: list[str] : A list of client IDs for which the information is requested.
        :return: list: list[dict] : A list of info about keys.

        """
        info = []
        for client_id in client_ids:
            get_request_url = f'{self.base_url}/panel/api/inbounds/getClientTrafficsById/{client_id}'

            resp = self.__get_request(get_request_url)
            data = resp.text

            if resp.ok:
                data = json.loads(data)['obj'][0]
                info.append(data)

        return info
