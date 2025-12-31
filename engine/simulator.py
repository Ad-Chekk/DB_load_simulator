import random
import threading
import time
from typing import Callable

class LoadSimulator:
    """
    Core load simulation engine.
    Database-agnostic by design.
    """


    def __init__(
    self,
    get_connection_fn,
    insert_fn,
    update_fn,
    delete_fn,
):
            self.get_connection = get_connection_fn
            self.insert_fn = insert_fn
            self.update_fn = update_fn
            self.delete_fn = delete_fn

            self._stop_event = threading.Event()

            # Counters
            self.insert_count = 0
            self.update_count = 0
            self.delete_count = 0

    def stop(self):
        self._stop_event.set()

    print("LoadSimulator __init__ loaded")
    

    def run(self, qps: int, duration_seconds: int):
        """
        Executes random INSERT/UPDATE/DELETE at given QPS for duration.
        """
        conn = self.get_connection()
        cursor = conn.cursor()

        start_time = time.time()
        interval = 1 / qps            # how many query per second qps


        while time.time() - start_time < duration_seconds:
            if self._stop_event.is_set():
                break

            operation = random.choice(["insert", "update", "delete"])

            try:
                if operation == "insert":
                    self.insert_fn(cursor)
                    self.insert_count += 1

                elif operation == "update":
                    self.update_fn(cursor)
                    self.update_count += 1

                else:
                    self.delete_fn(cursor)
                    self.delete_count += 1

                conn.commit()

            except Exception as e:
                conn.rollback()
                print(f"Error executing {operation}: {e}")

            time.sleep(interval)

        cursor.close()
        conn.close()
