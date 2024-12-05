import os
from dotenv import load_dotenv
import psycopg2
from fastapi import FastAPI, Request, HTTPException, Query

app = FastAPI()
def database():
    try:
        load_dotenv()
        connection = psycopg2.connect(
            database=os.getenv("database"),
            user=os.getenv("user"),
            password=os.getenv("password"),
            host=os.getenv("host"),
            port=os.getenv("port"),
        )
        return connection
    except Exception as e:
        return ("An Error Occured in Db connection", e)


@app.get("/hello")
async def res():
    try:
        connection = database()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM student order by id asc")
        records = cursor.fetchall()
        print("Records", records)
        response_data = {"resposeMessage": 1, "responseCode": 200, "data": records}
        return response_data
    except Exception as e:
        error_message = e
        response_data = {
            "resposeMessage": 0,
            "responseCode": 400,
            "data": [],
            "error": error_message,
        }
        return response_data
    finally:
        cursor.close()
        connection.close()


@app.post("/data-insert")
async def root(request: Request):
    try:
        body = await request.json()
        print("Body", body)
        id = body.get("id")
        name = body.get("name")

        address = body.get("address")
        mobileno = body.get("mobileno")
        print("id", id)

        if not name or not id:
            print("Insert check is running")
            raise HTTPException(status_code=400, detail="Name and id must be provided")

        connection = database()
        cursor = connection.cursor()
        print("id", id)
        cursor.execute(
            "INSERT INTO student (id, name, address, mobileno) VALUES (%s, %s,%s,%s)",
            (id, name, address, mobileno),
        )
        print("Hello")
        connection.commit()
        print("Hello")
        response_data = {
            "responseMessage": 1,
            "responseCode": 200,
            "data": {"id": id, "name": name},
        }
        print("Ritik")
        return response_data

    except Exception as e:
        error_message = str(e)
        print("error_message", error_message)
        response_data = {
            "responseMessage": 0,
            "responseCode": 400,
            "data": [],
            "error": error_message,
        }
        return response_data

    finally:
        cursor.close()
        connection.close()


@app.delete("/data-delete")
async def root(request: Request):
    try:
        body = await request.json()
        id = body.get("id")
        print("id", id)

        if id is None:
            response_data = {
                "responseMessage": 0,
                "responseCode": 400,
                "data": [],
                "error": "Id shoud not be none",
            }
            print(response_data)
            return response_data

        connection = database()
        cursor = connection.cursor()
        print("id1", id)
        query = "delete From student where id =%s"
        cursor.execute(query % (id))
        print("Hello")
        connection.commit()
        print("Hello2")
        response_data = {
            "responseMessage": 1,
            "responseCode": 200,
            "message": "Data Delete Successfully",
            "data": {"id": id},
        }
        print("Ritik")
        return response_data

    except Exception as e:
        error_message = str(e)
        print("error_message", error_message)
        response_data = {
            "responseMessage": 0,
            "responseCode": 400,
            "data": [],
            "error": error_message,
        }
        return response_data
    finally:
        cursor.close()
        connection.close()


@app.put("/data-update")
async def root(request: Request):
    try:
        body = await request.json()
        id = body.get("id")
        name = body.get("name")
        address = body.get("address")
        mobileno = body.get("mobileno")
        print("id", id)
        if id is None:
            response_data = {
                "responseMessage": 0,
                "responseCode": 400,
                "data": [],
                "error": "id is Mandatory to update the data",
            }
            return response_data

        connection = database()
        cursor = connection.cursor()

        query = "SELECT * FROM student WHERE id = %s"
        cursor.execute(query, (id,))
        records = cursor.fetchall()
        print("records", records)
        if not records:
            response_data = {
                "responseMessage": 0,
                "responseCode": 404,
                "data": [],
                "error": "No record found with the given id",
            }
            return response_data

        query = (
            "UPDATE student SET name = %s, address = %s, mobileno = %s WHERE id = %s"
        )
        cursor.execute(query, (name, address, mobileno, id))
        connection.commit()

        response_data = {
            "responseMessage": 1,
            "responseCode": 200,
            "message": "Data updated Successfully",
            "error": "",
        }

        return response_data

    except Exception as e:
        error_message = str(e)
        print("error_message", error_message)
        response_data = {
            "responseMessage": 0,
            "responseCode": 400,
            "data": [],
            "error": error_message,
        }
        return response_data

    finally:
        cursor.close()
        connection.close()


@app.patch("/id/")
async def get_student(id: int = Query(...)):
    try:
        print("ID Details")
        connection = database()
        cursor = connection.cursor()
        query = "SELECT * FROM student WHERE id = %s"
        cursor.execute(query, (id,))
        records = cursor.fetchall()
        print("Records", records)
        response_data = {"responseMessage": 1, "responseCode": 200, "data": records}
        return response_data
    except Exception as e:
        error_message = str(e)
        response_data = {
            "responseMessage": 0,
            "responseCode": 400,
            "data": [],
            "error": error_message,
        }
        return response_data
    finally:
        cursor.close()
        connection.close()
