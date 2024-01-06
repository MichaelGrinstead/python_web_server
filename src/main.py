import psycopg2
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


hostname = "localhost"
database = "users"
username = "mike"
password = "123456"
port_id = "5432"

conn = psycopg2.connect(
    host=hostname, user=username, password=password, dbname=database, port=port_id
)


@app.route("/add", methods=["POST"])
def add_user():
    data = request.json
    name = data["name"]
    try:
        with conn.cursor() as cursor:
            cursor.execute("INSERT INTO users (name) VALUES (%s)", (name,))
            conn.commit()
        return jsonify({"message": "success"})
    except Exception as e:
        return jsonify({"message": str(e)})


@app.route("/get/<int:id>", methods=["GET"])
def get_user(id):
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE id=%s", (id,))
            user = cursor.fetchone()
            if user:
                return jsonify({"id": user[0], "name": user[1]})
            else:
                return jsonify({"message": "user not found"})

    except Exception as e:
        return jsonify({"message": str(e)})


@app.route("/delete/<int:id>", methods=["DELETE"])
def delete_user(id):
    try:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM users WHERE id=%s", (id,))
            conn.commit()
            return jsonify({"message": "success"})
    except Exception as e:
        return jsonify({"message": str(e)})


if __name__ == "__main__":
    app.run(debug=True, port=3001)
    print("Server is running on port 3001")
