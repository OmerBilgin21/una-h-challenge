import os
from datetime import datetime, timedelta, timezone

import uvicorn
from fastapi import FastAPI, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from src.db.models import Session, User
from src.db.parser_schema import ParsedCSVData
from src.utils.parser import process_csv

app = FastAPI()
session = Session()


@app.get("/", response_model=list)
async def get_user_data(
	start_date: datetime | None = datetime.now(tz=timezone.utc),
	end_date: datetime | None = datetime.now(tz=timezone.utc) + timedelta(hours=2),
	limit: int | None = None,
) -> list:
	"""_summary_

	Args:
		start_date (datetime | None, optional): _description_.
			Defaults to datetime.now(tz=timezone.utc).
		end_date (datetime | None, optional): _description_.
			Defaults to datetime.now(tz=timezone.utc)+timedelta(hours=2).
		limit (int | None, optional): _description_.
			Defaults to None.

	Raises:
		HTTPException: _description_

	Returns:
		list: _description_
	"""
	try:
		user_data = session.query(User).all()
		return [User.model_to_dict(user) for user in user_data]

	except Exception as exc:
		raise HTTPException(
			status_code=500, detail="Error while getting user data"
		) from exc
	return []


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
