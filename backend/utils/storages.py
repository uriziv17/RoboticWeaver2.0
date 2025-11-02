import os
import aiofiles


class BaseFileStorage:
    def save(self, file_path: str, data: bytes) -> None:
        raise NotImplementedError("Save method not implemented.")

    def read(self, file_path: str) -> bytes:
        raise NotImplementedError("Read method not implemented.")


class LocalFileStorage(BaseFileStorage):
    SHARED_DIR = "/shared"

    async def save(self, file_name: str, data: bytes) -> None:
        file_path = os.path.join(self.SHARED_DIR, file_name)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        async with aiofiles.open(file_path, "wb") as f:
            await f.write(data)

    async def read(self, file_name: str) -> bytes:
        file_path = os.path.join(self.SHARED_DIR, file_name)
        async with aiofiles.open(file_path, "rb") as f:
            return await f.read()
