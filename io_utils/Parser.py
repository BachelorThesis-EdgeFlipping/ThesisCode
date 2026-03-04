from abc import ABC, abstractmethod
from Globals import DATA_DIR
import os

class Parser(ABC):
  @staticmethod
  @abstractmethod
  def getJSONString(filename: str) -> str:
    filepath = os.path.join(DATA_DIR, filename)
    with open(filepath, 'r') as f:
      json_str = f.read()
    return json_str
  
  @staticmethod
  @abstractmethod
  def parse(json_str: str):
    pass 