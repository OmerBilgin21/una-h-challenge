from pydantic import BaseModel, Field


class ParsedCSVData(BaseModel):
	user_id: str
	gerat: str = Field(alias="Gerät")  # always there
	seriennummer: str = Field(alias="Seriennummer")  # always there
	geratezeitstempel: str = Field(alias="Gerätezeitstempel")  # always there
	aufzeichnungstyp: int = Field(alias="Aufzeichnungstyp")  # always there
	glukosewert_verlauf: float | None = Field(
		alias="Glukosewert-Verlauf mg/dL",
	)
	glukose_scan: float | None = Field(alias="Glukose-Scan mg/dL")
	nicht_numerisches_schnellwirkendes_insulin: str | None = Field(
		alias="Nicht numerisches schnellwirkendes Insulin",
	)
	schnellwirkendes_insulin_einheiten: str | None = Field(
		alias="Schnellwirkendes Insulin (Einheiten)",
	)
	nicht_numerische_nahrungsdaten: float | None = Field(
		alias="Nicht numerische Nahrungsdaten",
	)
	kohlenhydrate_gramm: str | None = Field(alias="Kohlenhydrate (Gramm)")
	kohlenhydrate_portionen: str | None = Field(alias="Kohlenhydrate (Portionen)")
	nicht_numerisches_depotinsulin: str | None = Field(
		alias="Nicht numerisches Depotinsulin",
	)
	depotinsulin_einheiten: str | None = Field(alias="Depotinsulin (Einheiten)")
	notizen: str | None = Field(alias="Notizen")
	glukose_teststreifen_mg_d_l: str | None = Field(alias="Glukose-Teststreifen mg/dL")
	keton_mmol_l: str | None = Field(alias="Keton mmol/L")
	mahlzeiteninsulin_einheiten: str | None = Field(
		alias="Mahlzeiteninsulin (Einheiten)",
	)
	korrekturinsulin_einheiten: str | None = Field(alias="Korrekturinsulin (Einheiten)")
	insulin_anderung_durch_anwender_einheiten: str | None = Field(
		alias="Insulin-Änderung durch Anwender (Einheiten)",
	)

	class Config:  # noqa: D106
		orm_mode: True
