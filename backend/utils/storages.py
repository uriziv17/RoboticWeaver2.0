import os
import aiofiles


class LocalFileStorage:
    SHARED_DIR = "/shared"

    def get_path(self, file_name: str) -> str:
        file_path = os.path.join(self.SHARED_DIR, file_name)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        return file_path

    def save(self, file_path: str, data: bytes) -> None:
        raise NotImplementedError("Save method not implemented.")

    def read(self, file_path: str) -> bytes:
        raise NotImplementedError("Read method not implemented.")


class AsyncFileStorage(LocalFileStorage):
    async def save(self, file_name: str, data: bytes) -> None:
        file_path = super().get_path(file_name)
        async with aiofiles.open(file_path, "wb") as f:
            await f.write(data)
        return file_path

    async def read(self, file_name: str) -> bytes:
        file_path = os.path.join(self.SHARED_DIR, file_name)
        async with aiofiles.open(file_path, "rb") as f:
            return await f.read()


class SyncFileStorage(LocalFileStorage):
    def save(self, file_name: str, data: bytes) -> None:
        file_path = super().get_path(file_name)
        with open(file_path, "wb") as f:
            f.write(data)
        return file_path

    def read(self, file_name: str) -> bytes:
        file_path = os.path.join(self.SHARED_DIR, file_name)
        with open(file_path, "rb") as f:
            return f.read()