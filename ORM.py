from sqlalchemy import create_engine
from sqlalchemy import func
from datetime import datetime
from sqlalchemy import desc
from xlrd import open_workbook
from time import mktime
from os import listdir
from os.path import isfile, join
from pprint import pprint
import os
import json
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.orm import sessionmaker
Base = declarative_base()

if os.environ.get('DATABASE') != None:
  connectionString = os.environ.get('DATABASE')

engine = create_engine(connectionString, echo=False)

class Nadlansale(Base):
  __tablename__ = 'nadlansale'

  Id = Column(Integer, primary_key=True)

  URL = Column(String)
  Price = Column(String)
  Contact = Column(String)
  Area = Column(String)
  City = Column(String)

  Created = Column(DateTime)


  Phone1 = Column(String)
  Phone2 = Column(String)
  Description = Column(String)

  Available = Column(String)

  Latitude = Column(String)
  Longitude = Column(String)
  Type = Column(String)

  Size = Column(Integer)
  Neighbourhood = Column(String)

  def __init__(self, result):
    self.Id = result['id']
    self.URL = result["url"]
    self.Price = int(result['price']) if result['price'].isdigit() else 0
    self.Contact = result['contact']
    self.Area = result['area']
    self.City = result['city']
    self.Created = result['created']
    self.Phone1 = result['phone1']
    self.Phone2 = result['phone2']
    self.Description = result['description']
    self.Available = result['available']
    self.Latitude = result['latitude']
    self.Longitude = result['longitude']
    self.Type = result['type']
    self.Size = int(result['size']) if result['size'].isdigit() else 0
    self.Neighbourhood = result['neighbourhood']

class Operations:

  def BulkUpdate(items):
    session.bulk_save_objects(items)
    session.commit()

  def GetIDDict():
    return { x[0]: None for x in session.query(Nadlansale.Id).all()}


Base.metadata.create_all(engine)

Session = sessionmaker()
Session.configure(bind=engine)
session = Session()
session = Session()


if __name__ == "__main__":
  d = Operations.GetIDDict()
  print(d)
  print(1437186 in d)
  print(1403006 in d)