from fastapi import WebSocket


class WebsocketConnectionService:
    def __init__(self):
        self.__active_connections: dict[str, WebSocket] = {}
        self.__tg_bot: WebSocket = None
        self.associate_ids = {}

    async def connect(self, websocket: WebSocket, user_id: int, client_key: str):
        await websocket.accept()
        self.__active_connections.setdefault(user_id, {})
        self.__active_connections[user_id][client_key] = websocket

    async def tg_connect(self, websocket: WebSocket):
        await websocket.accept()
        self.__tg_bot = websocket

    async def tg_send_msg(self, message: dict):
        await self.__tg_bot.send_json(message)

    async def tg_disconnect(self):
        await self.__tg_bot.close()
        self.__tg_bot = None

    def tg_add_user(self, user_id: int, chat_id: int):
        self.associate_ids[user_id] = chat_id

    async def disconnect(self, user_id: int, client_key: str):
        if user_id in self.__active_connections:
            user_cons = self.__active_connections[user_id]
            s = user_cons.pop(client_key)
            await s.close()
            if len(user_cons) == 0:
                self.__active_connections.pop(user_id)

    async def send_personal_message(self, message: dict, user_id: int):
        if user_id in self.__active_connections:
            for c in self.__active_connections[user_id].values():
                await c.send_json(message)

        if user_id in self.associate_ids:
            chat_id = self.associate_ids[user_id]
            await self.__tg_bot.send_json({"message": message, "chat_id": chat_id})

    async def send_personal_message_to_device(
        self, message: dict, user_id: int, client_key: str
    ):
        if user_id in self.__active_connections:
            user_cons = self.__active_connections[user_id]
            await user_cons[client_key].send_json(message)

    async def broadcast(self, message: dict):
        for users in self.__active_connections.values():
            for connection in users.values():
                await connection.send_json(message)
