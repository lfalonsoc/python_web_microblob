import os
import datetime
from typing import Any

from dotenv import load_dotenv
from flask import Flask, render_template, request
from pymongo import MongoClient

load_dotenv()


def create_app() -> Any:
    app: Flask = Flask(__name__)
    client: MongoClient = MongoClient(os.getenv("MONGODB_URL"))
    app.db: Any = client.microblog


    @app.route("/", methods=["GET", "POST"])
    def home() -> Any:
        if request.method == "POST":
            entry_content: Any = request.form.get("content")
            formatted_date: str = datetime.datetime.today().strftime("%Y-%m-%d")
            app.db.entries.insert_one(
                {"content": entry_content, "date": formatted_date}
            )
            
        entries_with_date: list[Any] = [
            (
                entry["content"],
                entry["date"],
                datetime.datetime.strptime(entry["date"], "%Y-%m-%d").strftime("%b %d")
            )
            for entry in app.db.entries.find({})
        ]
        return render_template("home.html", entries=entries_with_date)
    
    return app
