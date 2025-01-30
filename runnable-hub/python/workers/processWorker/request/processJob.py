

from pydantic import BaseModel
from typing import List, Dict
from .processStep import ProcessStep

class ProcessJob(BaseModel):
    steps: List[ProcessStep]
    needs: List[str] = []