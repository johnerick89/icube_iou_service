# IOU
IOU service for setting up users, ious and calculating what each user owes the other user

## Environment:
- Python version: 3.7
- Django version: 3.0.6
- Django REST framework version: 3.11.0


## Data:
Example of a user JSON object
```
{
   "name": "Adam",
   "phone": "1234"
}
```

Example of a iou JSON object:
```
{   "lender":2,
    "borrower":1,
    "amount":7500
}
```

## Users
POST request to `/api/users/`:
- creates a new user data record
- expects a valid user object as its body payload, except that it does not have an id property; you can assume that the given object is always valid
- adds the given object to the collection and assigns a unique integer id to it
- the response code is 201 and the response body is the created record, including its unique id

GET request to `/api/users/`:
- the response code is 200
- the response body is an array of matching records, ordered by their ids in increasing order

GET request to `/api/users/<id>/`:
- returns a record with the given id
- if the matching record exists, the response code is 200 and the response body is the matching object
- if there is no record in the collection with the given id, the response code is 404

DELETE request to `/api/users/<id>/`:
- deletes the record with the given id from the collection
- if matching record existed, the response code is 204
- if there was no record in the collection with the given id, the response code is 404


## IOUs
POST request to `/api/ious/`:
- creates a new iou record
- expects a valid  object as its body payload, except that it does not have an id property; you can assume that the given object is always valid
- updates the user record with current iou information for lender and borrower
- adds the given object to the collection and assigns a unique integer id to it
- the response code is 201 and the response body is the created record, including its unique id

GET request to `/api/v1/ious/`:
- the response code is 200
- the response body is an array of matching records, ordered by their ids in increasing order

GET request to `/api/v1/ious/<id>/`:
- returns a record with the given id
- if the matching record exists, the response code is 200 and the response body is the matching object
- if there is no record in the collection with the given id, the response code is 404

DELETE request to `/api/v1/ious/<id>/`:
- deletes the record with the given id from the collection
- if matching record existed, the response code is 204
- if there was no record in the collection with the given id, the response code is 404


## Running Locally
Make sure you have Python 3.7 [installed locally](http://install.python-guide.org). 

```sh
$ source ../env/bin/activate
$ pip3 install -r requirements.txt

# Create model then make migrations
$ python3 manage.py makemigrations api
$ python3 manage.py migrate

# delete previous migrations so as to redo migrations
$ python3 manage.py migrate api zero 

# run app
$ python3 manage.py runserver

For python deployment your app should now be running on [127.0.0.1:8000](http://127.0.0.1:8000/) or 
[localhost:8000](http://127.0.0.1:8000/) 
