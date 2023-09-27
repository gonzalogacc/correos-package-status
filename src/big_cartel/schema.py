from typing import List

from pydantic import BaseModel

## Very barebones objects to solve the problem i have now!, not done with this

class BigCartelAccount(BaseModel):
    id: int

class BigCartelResponse(BaseModel):
    data: List[BigCartelAccount]
