db = db.getSiblingDB("mydatabase");
db.createCollection("projects");
db.init_collection.insertOne({ message: "Database initialized!" });
