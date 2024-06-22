from app.database import Database

database = Database()

database.create_tables(["packages"])
