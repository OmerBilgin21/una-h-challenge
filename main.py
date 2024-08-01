import os
from datetime import datetime
from typing import Literal

import uvicorn
from fastapi import FastAPI, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import desc

from src.models.models import Session, User
from src.utils.parser import process_csv

app = FastAPI()
session = Session()


@app.get("/", response_model=list)
async def get_user_data(
	start_date: datetime | None = None,
	end_date: datetime | None = None,
	limit: float | None = None,
	user_id: str | None = None,
	# https://stackoverflow.com/questions/69087120/how-to-allow-specific-parameter-values-in-openapi-specification-swagger-ui-usi # noqa: ERA001, E501
	sort_type: Literal["asc", "dsc"] | None = None,
) -> list:
	"""Get health data with different query options

	Args:
		start_date (datetime | None): Query filter.
			Defaults to None.
		end_date (datetime | None): Query filter.
			Defaults to None.
		limit (float | None): Query filter.
			Defaults to None.
		user_id (str | None): Query filter.
			Defaults to None.
		sort_type (Literal["asc"|"dsc"] | None): Sort query outcome.
			Defaults to None.

	Raises:
		HTTPException: if db query fails

	Returns:
		list: Obtained data
	"""
	query = session.query(User)

	if start_date:
		query = query.filter(User.geratezeitstempel > start_date)
	if end_date:
		query = query.filter(User.geratezeitstempel < end_date)
	if limit:
		query = query.filter(User.glukosewert_verlauf < limit)
	if user_id:
		query = query.filter(User.user_id == user_id)
	if sort_type == "asc":
		query.order_by(User.geratezeitstempel)
	if sort_type == "dsc":
		query.order_by(desc(User.geratezeitstempel))

	try:
		user_data = query.all()

		user_data = [User.model_to_dict(user) for user in user_data]

	except Exception as exc:
		raise HTTPException(
			status_code=500,
			detail="Error while getting user data",
		) from exc

	return user_data


@app.post("/upload-csv", response_model=list)
async def parse_csv_into_db(file_in: UploadFile) -> list:
	"""Parses an incoming csv file and adds it into the db

	Args:
		file_in (UploadFile): Incoming CSV file

	Raises:
		HTTPException: The file extension is not csv
		HTTPException: There is an error with db operations

	Returns:
		list[ParsedCSVData]: List of parsed ParsedCSVData objects
	"""
	name = file_in.filename.split(".")

	if name[1] != "csv":
		raise HTTPException(status_code=400, detail="Only CSV files are allowed")

	data = await process_csv(file_in=file_in, user_id=name[0])
	user_instances = [User(**item) for item in data]
	session.add_all(user_instances)

	try:
		session.commit()
	except Exception as e:
		raise HTTPException(status_code=500, detail="Error while adding to db!") from e

	return data


app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)

if __name__ == "__main__":
	env = os.environ.get("ENV", "dev")
	if env == "dev":
		uvicorn.run(
			"main:app",
			host="0.0.0.0",
			port=8000,
			reload=True,
			log_level="info",
		)
	else:
		uvicorn.run(
			"main:app",
			host="0.0.0.0",
			port=8000,
			log_level="info",
		)
