import math
from datetime import datetime, timezone
from io import StringIO

import pandas as pd
from fastapi import UploadFile

from src.db.parser_schema import ParsedCSVData

# ruff: noqa: ERA001


def read_csv(file_in: StringIO) -> tuple[pd.DataFrame]:
	"""Reads and returns csv data

	Returns:
			tuple[pd.DataFrame]: DataFrame tuple
	"""
	return pd.read_csv(file_in, delimiter=",", skiprows=[0])


def adjust_data(data: pd.DataFrame, user_id: str) -> list[dict]:
	"""Adjust DataFrame data"""
	data_list = data.to_dict(orient="records")
	data = [row for row in data_list if row is not None]
	new = []
	for item in data:
		n_item = item
		if n_item is not None:
			for k, v in n_item.items():
				if isinstance(v, float) and math.isnan(v):
					n_item[k] = None

		date_of_data = datetime.now(tz=timezone.utc)

		if n_item["Gerätezeitstempel"] is not None:
			time_splitted = n_item["Gerätezeitstempel"].split(":")
			if len(time_splitted) == 2:  # noqa: PLR2004
				date_of_data = datetime.strptime(  # noqa: DTZ007
					n_item["Gerätezeitstempel"],
					# used chat-gpt to learn I have to use %Y
					# instead of %y
					# for four digit years at strptime function
					"%d-%m-%Y %H:%M",
				)
			elif len(time_splitted) == 3:  # noqa: PLR2004
				date_of_data = datetime.strptime(  # noqa: DTZ007
					n_item["Gerätezeitstempel"],
					"%d/%m/%y %H:%M:%S",
				)

		n_item["user_id"] = user_id
		n_item = ParsedCSVData(**n_item)

		n_item = n_item.dict()
		n_item["geratezeitstempel"] = date_of_data

		new.append(n_item)
	return new


async def process_csv(file_in: UploadFile, user_id: str) -> None:
	"""Write DataFrames to db"""
	a = await file_in.read()
	b = a.decode()

	# https://stackoverflow.com/questions/47741235/how-to-read-bytes-object-from-csv  # noqa: E501
	decoded_csv = StringIO(b)
	csv_data = read_csv(decoded_csv)

	return adjust_data(data=csv_data, user_id=user_id)
