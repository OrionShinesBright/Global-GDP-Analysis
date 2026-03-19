from typing import List, Any, Dict
from multiprocessing import Queue

class QueueImplementation:
    def __init__(self, maxSize: int = 1000) -> None:
        self.DataStream = Queue(maxSize)
        self.maxSize = maxSize

    def SendToStream(self, raw_data: List[Any]):
        self.DataStream.put(raw_data, block=True)

    def PickFromStream(self) -> List[Any]:
        data = self.DataStream.get(block=True)
        return data

    def get_size(self) -> int:
        return self.DataStream.qsize()

    def get_MaxSize(self) -> int:
        return self.maxSize
