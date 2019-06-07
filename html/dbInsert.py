from pymongo import MongoClient

# Enter the ip and port the database is hosted at
client = MongoClient("127.0.0.1", 27017)
db = client.pgmdb

def insertDoc(name, file_path, type, title):
    content = open(file_path).read()
    db.static.insert_one({"name": name, "content": content, "type": type, "title": title})

if __name__ == "__main__":
    # Removes anything currently in the static collection
    db.static.delete_many({})

    # Places files with necessary attributes into the database
    # Should be done with all static files siting in the same directory as this
    # file
    insertDoc("home", "./home.html", "home", "Geologic Mapping: Project Details")
    insertDoc("menu", "./menu.html", "menu", "")
    insertDoc("Guidelines", "./Guidelines.html", "page", "Geologic Mapping: Mapping Guidelines")
    insertDoc("Resources", "./Resources.html", "page", "Geologic Mapping: Resources for Planetary Geologic Mappers")
    insertDoc("Meetings", "./Meetings.html", "page", "Geologic Mapping: Meetings and Abstracts")
    insertDoc("Milestones", "./Milestones.html", "page", "Geologic Mapping: Milestones")
    insertDoc("FAQ", "./FAQ.html", "page", "Geologic Mapping: Frequently Asked Questions")
