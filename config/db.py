from sqlalchemy import create_engine, MetaData

engine = create_engine("mysql+pymysql://reader:library@localhost:3306/mediapro")

meta = MetaData()

conn = engine.connect()