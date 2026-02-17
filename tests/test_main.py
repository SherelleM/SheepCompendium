# Import TestClient to simulate API requests
from fastapi.testclient import TestClient

# Import the FastAPI app instance from the controller module
from main import app

# Create a TestClient instance for the FastAPI app
client = TestClient(app)

# Define a test function for reading a specific sheep
def test_read_sheep():
    # Send a GET request to the endpoint "/sheep/1"
    response = client.get("/sheep/1")

    # Assert that the response status code is 200 (OK)
    assert response.status_code == 200

    # Assert that the response JSON matches the expected data
    assert response.json() == {
        "id": 1,
        "name": "Spice",
        "breed": "Gotland",
        "sex": "ewe"
    }

# Define a test case function for adding a new sheep
def test_add_sheep():

    # Prepare new sheep data in dictionary format
    sheep_data_name = {
        "id": 7,
        "name": "Racey",
        "breed": "F1",
        "sex": "ram"
    }

    # Send a POST request to the endpoint "/sheep" with the new sheep data
    response = client.post("/sheep", json=sheep_data_name)

    # Assert that the response status code is 201 (Created)
    assert response.status_code == 201

    # Assert that the response status JSON matches the new sheep data
    assert response.json() == sheep_data_name

    # Verify that the sheep was actually added to the db by retrieving
    # the new sheep by ID.
    # Assert of new sheep data can be retrieved
    get_response = client.get("/sheep/7")
    assert get_response.status_code == 200
    assert get_response.json() == sheep_data_name

# Define a test case function for deleting a sheep
def test_delete_sheep():
    # Delete data at the endpoint "/sheep/1"
    response = client.delete("/sheep/1")

    # Assert the new sheep data has been removed
    assert response.status_code == 204

    # Verify that the sheep was actually deleted by asserting
    # that the new sheep data cannot be retrieved
    get_response = client.get("/sheep/1")
    assert get_response.status_code == 404

# Define a test case function for updating a sheep
def test_update_sheep():
    # Prepare updated sheep data in dictionary format
    sheep_data_name = {
        "id": 6,
        "name": "Baby",
        "breed": "Babydoll",
        "sex": "ewe"
    }

    # Check the state before
    current_response = client.get("/sheep/6")

    # Send a PUT request to the endpoint "/sheep/6"
    response = client.put("/sheep/6", json=sheep_data_name)

    # Assert that the response status code is 200 (OK)
    assert response.status_code == 200

    # Assert that the response status JSON matches the new sheep data
    assert response.json() == sheep_data_name

    # Verify that the sheep was actually updated in the db by retrieving
    # the new sheep by ID.
    get_response = client.get("/sheep/6")
    assert get_response.json() == sheep_data_name