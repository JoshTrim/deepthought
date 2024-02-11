from models import BaseModel 
import time

class Timer(BaseModel):
    start_time: time = None
    duration: time = None

    def model_post_init(self, *args, **kwargs):
        self.start_time = time.time()

    def stop(self):
        self.duration = time.time() - self.start_time
        print(f"--- {self.duration} seconds ---")
