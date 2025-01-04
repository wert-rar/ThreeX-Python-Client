import asyncio
import json
from logging import Logger

import aiohttp
from aiohttp import ClientResponse
import logging

from src.DefaultPayload import DefaultPayload
from src.Payload import Payload
from src.errors import ClientError

class ThreeXClientAsync:
    def __init__(self, login, password, login_key, panel_host, root_url, sub_host, sub_path, inbound_id, panel_port = None, sub_port = None, logging_enabled = False,timeout = 300):


        self.inbound = inbound_id

        self.login_payload = {
            "username": login,
            "password": password,
            "loginSecret": login_key
        }

        self.logger: Logger | None = None

        if logging_enabled:
            self.logger = logging.getLogger(__name__)
            self.logger.setLevel(logging.DEBUG)
            self.logger.formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        self.base_url = f'https://{panel_host}:{panel_port}/{root_url}' if panel_port else f'https://{panel_host}/{root_url}'
        self.sub_url = f'https://{sub_host}:{sub_port}/{sub_path}/' if sub_port else f'https://{sub_host}/{sub_path}/'

        self.cookie = None
        self.timeout = timeout


        asyncio.create_task(self.update_cookies_periodically())

    async def __fetch_cookies(self):
        """Get new cookies from server by /login POST request"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(f'{self.base_url}/login', data=self.login_payload) as response:
                    if response.status == 200:
                        self.cookie = session.cookie_jar
                        if self.logger:
                            self.logger.info('Updated cookies. ')
                    else:
                        if self.logger:
                            self.logger.error(f'Failed to update cookies. Wrong status : {response.status}')
        except Exception as e:
            if self.logger:
                self.logger.error(f'Failed to update cookies.\nError: {repr(e)}')


    async def update_cookies_periodically(self):
        """Update cookies every  5 minutes."""
        while True:
            await self.__fetch_cookies()
            await asyncio.sleep(self.timeout)

    async def __post_request(self, url: str, payload: Payload|None) -> ClientResponse:
        """
            Sends an asynchronous POST request to a specified URL with the given payload.

            This function handles the login process before sending the request and ensures
            the session is closed after the request is completed.

            Parameters:
            url (str): The URL to which the POST request is sent.
            payload (dict): The data to be sent in the body of the POST request.

            Returns:
            aiohttp.ClientResponse: The response object from the POST request.

            Raises:
            ClientError: If there is an issue connecting to the panel or if the client encounters an error.
        """
        async with aiohttp.ClientSession() as session:
            try:
                resp = await session.post(url, data=payload.format(), cookies=self.cookie)
                if self.logger:
                    self.logger.info(f'POST {url} [{resp.status}]')

            except Exception as e:
                if self.logger:
                    self.logger.error(f'Failed to send POST request.\nUrl: {url}\nPayload : {payload}\nError: {repr(e)}')
                raise ClientError('Client error: ' + repr(e))
            finally:
                await session.close()

                return resp

    async def __get_request(self, url: str) -> ClientResponse:
        """
        Sends an asynchronous GET request to a specified URL.

        This function handles the login process before sending the request and ensures
        the session is closed after the request is completed.

        Parameters:
        url (str): The URL to which the GET request is sent.

        Returns:
        aiohttp.ClientResponse: The response object from the GET request.

        Raises:
        ClientError: If there is an issue connecting to the panel or if the client encounters an error.
        """
        async with aiohttp.ClientSession() as session:
            try:
                resp = await session.get(url,cookies=self.cookie)
                if self.logger:
                    self.logger.info(f'GET {url} [{resp.status}]')
            except Exception as e:
                raise ClientError('Client error: ' + repr(e))
            finally:
                await session.close()
                return resp

    async def add_client_to_inbound(self, payload:DefaultPayload, inbound = None) -> str:
        """
        Adds a client to the specified inbound.

        Args:
        payload (DefaultPayload): The payload containing the client's details.'

        Returns:
        - tuple: A tuple containing the sublink and expiryTime of the added client.

        Raises:
        - ClientError: If there is an issue connecting to the panel or if the client encounters an error.
        """
        if inbound is None:
            inbound = self.inbound

        post_request_url = f"https://{self.base_url}/panel/api/inbounds/{self.inbound}/addClient"
        resp = await self.__post_request(post_request_url, payload)
        if resp.ok:
            sublink = self.sub_url + str(payload["settings"]["clients"][0]["subID"])  # ссылка на подписку
            return sublink

    async def get_clients_in_inbound(self, inbound = None) -> list:
        """
        Getting all clients on inbound
        :param inbound:int : inbound id, if None then uses self.inbound
        :return: clients:  List of clients
        """

        if inbound is None:
            inbound = self.inbound

        get_request_url = f'{self.base_url}//panel/api/inbounds/get/{inbound}'

        resp = await self.__get_request(get_request_url)
        data = await resp.text()
        if resp.ok:
            data = json.loads(data)
            data = json.loads(data['obj']['settings'])
            clients = data['clients']
            return clients  # возвращает список клиентов

    async def delete_client(self, client_id: str, inbound=None) -> None:
        """
        Deleting a client by its client_id
        :param inbound:int : inbound id, if None then uses self.inbound
        :param client_id:str :  Client id
        """
        if inbound is None:
            inbound = self.inbound

        post_request_url = f"{self.base_url}/panel/api/inbounds/{inbound}/delClient/{client_id}"

        resp = await self.__post_request(post_request_url, {})
        text = await resp.text()
        if resp.ok:
            print(text)

    async def delete_depleted_clients(self) -> None:
        """
        Deleting clients whose key has expired
        (it can be used to clean keys when, for example, 60 days are not extended)
        :return:
        """

        post_request_url = f'{self.base_url}/panel/api/inbounds/delDepletedClients/{self.inbound}'

        resp = await self.__post_request(post_request_url, None)


    async def update_client(self, client_id : str, payload : DefaultPayload) -> None:
        """
        Update client info in inbound

        :param client_id:str : Client id
        :param payload: DefaultPayload : New client info

        :return: sublink: str :   Link to the subscription
        """
        post_request_url = f'{self.base_url}/panel/api/inbounds/updateClient/{client_id}'
        resp = await self.__post_request(post_request_url, payload)


    async def info_about_key(self, client_id: str) -> (str, str):
        """
           Fetches and returns the enable status and total traffic of a specific client key.

           :param client_id:str : Client id

           :return enable: bool : The enable status of the client key.
           :return trafic: int : The total traffic (in bytes) of the client key.

        """
        get_request_url = f'{self.base_url}/panel/api/inbounds/getClientTrafficsById/{client_id}'
        resp = await self.__get_request(get_request_url)
        data = await resp.text()

        enable = None
        trafic = 0
        if resp.ok:
            data = json.loads(data)['obj'][0]
            enable = data["enable"],
            trafic = data["up"] + data["down"]

        return enable, trafic

    # async def info_about_keys_old(self, client_ids: list[str]) -> list[str]:
    #     """
    #       Fetches and returns the enable status of specific client keys.
    #
    #       Parameters:
    #       - client_ids (list[str]): A list of client IDs for which the information is requested.
    #
    #       Returns:
    #       - list[str]: A list of enable statuses for the specified client keys.
    #
    #       Raises:
    #       - ClientError: If there is an issue connecting to the panel or if the client encounters an error.
    #     """
    #     info = []
    #     get_request_url = f"{self.base_url}/panel/api/inbounds/get/{self.inbound}"
    #     resp = await self.__get_request(get_request_url)
    #     data = await resp.text()
    #     if resp.ok:
    #         data = json.loads(data)['obj']['settings']
    #         data = json.loads(data)['clients']
    #         for client in data:
    #             if client["id"] in client_ids:
    #                 info.append((client["enable"]))
    #
    #     return info
    #
    async def info_about_keys(self, client_ids: list[str]) -> list[str]:
        """
        Fetches and returns the enable status of specific client keys.

        :param client_ids: list[str] : A list of client IDs for which the information is requested.
        :return: list: list[dict] : A list of info about keys.

        """
        info = []
        for client_id in client_ids:
            get_request_url = f'{self.base_url}/panel/api/inbounds/getClientTrafficsById/{client_id}'

            resp = await self.__get_request(get_request_url)

            data = await resp.text()
            if resp.ok:
                data = json.loads(data)['obj'][0]
                info.append(data)

        return info


