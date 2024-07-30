from typing import Any

from sqlalchemy import Column, DateTime, Float, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from src.config import db_connection_str

engine = create_engine(db_connection_str)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class User(Base):
	__tablename__ = "user_data"

	id = Column(Integer, primary_key=True, autoincrement=True)
	user_id = Column(String)
	gerat = Column(String)
	seriennummer = Column(String)
	geratezeitstempel = Column(DateTime)
	aufzeichnungstyp = Column(Integer)
	glukosewert_verlauf = Column(Float, nullable=True)
	glukose_scan = Column(Float, nullable=True)
	nicht_numerisches_schnellwirkendes_insulin = Column(String, nullable=True)
	schnellwirkendes_insulin_einheiten = Column(String, nullable=True)
	nicht_numerische_nahrungsdaten = Column(String, nullable=True)
	kohlenhydrate_gramm = Column(String, nullable=True)
	kohlenhydrate_portionen = Column(String, nullable=True)
	nicht_numerisches_depotinsulin = Column(String, nullable=True)
	depotinsulin_einheiten = Column(String, nullable=True)
	notizen = Column(String, nullable=True)
	glukose_teststreifen_mg_d_l = Column(String, nullable=True)
	keton_mmol_l = Column(String, nullable=True)
	mahlzeiteninsulin_einheiten = Column(String, nullable=True)
	korrekturinsulin_einheiten = Column(String, nullable=True)
	insulin_anderung_durch_anwender_einheiten = Column(String, nullable=True)

	def model_to_dict(instance: Any) -> dict:  # noqa: N805
		"""Convert to dict"""
		return {
			column.name: getattr(instance, column.name)
			for column in instance.__table__.columns
		}


Base.metadata.create_all(engine)
