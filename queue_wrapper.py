import asyncio
import multiprocessing as mp
import multiprocessing.queues as mp_q
import queue
from typing import Any, Callable, Optional
import uuid


def run(receive_queue: mp_q.JoinableQueue, send_queue: mp_q.Queue) -> None:
    while True:
        data: tuple[str, Callable[..., Any], list[Any], dict[str, Any]] | bool = receive_queue.get()
        if isinstance(data, bool):
            self.send_queue.put(True)
            break
        res: Any = data[1](*data[2], **data[3])
        send_queue.put((data[0], res))


class QueueWrapper:
    def __init__(self):
        self.send_queue: mp_q.JoinableQueue = mp.JoinableQueue()
        self.receive_queue: mp_q.Queue = mp.Queue()
        self.__res_funcs: dict[str, tuple[Callable[[Any], None], Any]] = {}
        self.__ctx = mp.get_context(method="spawn")
        self.__process: mp.Process = self.__ctx.Process(target=run, args=(self.send_queue, self.receive_queue))
        self.__process.start()

    def add(self, func: Callable[..., Any], args: Optional[list[Any]] = None, kwargs: Optional[dict[str, Any]] = None, callback: Optional[Callable[[Any], None]] = None) -> None:
        unique_id: str = str(uuid.uuid4())
        if callable is not None:
            self.__res_funcs[unique_id] = callback
        if args is None:
            args = []
        if kwargs is None:
            kwargs = {}
        self.send_queue.put((unique_id, func, args, kwargs))

    async def fetch(self) -> None:
        while True:
            try:
                while True:
                    res: tuple[str, Any] = self.receive_queue.get(False)
                    if res[0] in self.__res_funcs:
                        self.__res_funcs[res[0]][0](res[1])
            except queue.Empty as e:
                pass
            asyncio.sleep(0.05)

    def kill(self) -> bool:
        self.send_queue.put(True)
        while True:
            res: bool | tuple[str, Any] = self.receive_queue.get()
            if isinstance(res, bool):
                self.__process.join()
                return True
            if res[0] in self.__res_funcs:
                self.__res_funcs[res[0]][0](res[1])
        return False