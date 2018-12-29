from bottle import route, run, template, static_file, get, post, delete, request, response
from sys import argv
import json
import pymysql


connection = pymysql.connect(host="localhost",
                             user="root",
                             password="admin",
                             db="store",
                             charset="utf8",
                             cursorclass=pymysql.cursors.DictCursor)


@get("/admin")
def admin_portal():
    return template("pages/admin.html")


@get("/")
def index():
    return template("index.html")


@get('/js/<filename:re:.*\.js>')
def javascripts(filename):
    return static_file(filename, root='js')


@get('/css/<filename:re:.*\.css>')
def stylesheets(filename):
    return static_file(filename, root='css')


@get('/images/<filename:re:.*\.(jpg|png|gif|ico)>')
def images(filename):
    return static_file(filename, root='images')


# Add a category
@post('/category')
def create_category():
    new_cat = request.POST.get("name")
    if len(new_cat) == 0:
        return json.dumps({"STATUS": "ERROR", "MSG": "Name parameter is missing"})
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO category (name) VALUES ('{}')".format(new_cat)
            cursor.execute(sql)
            connection.commit()
            return json.dumps({"STATUS": "SUCCESS", "MSG": "The category was successfully created", "CAT_ID": cursor.lastrowid, "CODE": "201"})
    except Exception as e:
        if response.status_code == 200:
            return json.dumps({"STATUS": "ERROR", "MSG": "category {} already exists".format(new_cat), "CODE": "200"})
        elif response.status_code == 400:
            return json.dumps({"STATUS": "ERROR", "MSG": "bad request", "CODE": "400"})
        elif response.status_code == 400:
            return json.dumps({"STATUS": "ERROR", "MSG": "internal error", "CODE": "500"})
        else:
            return json.dumps({"STATUS": "ERROR", "MSG": str(e)})


# Delete a category
@delete('/category/<id>')
def delete_category(id):
    try:
        with connection.cursor() as cursor:
            sql = "DELETE FROM category WHERE id = '{}'".format(id)
            cursor.execute(sql)
            connection.commit()
            return json.dumps({"STATUS": "SUCCESS", "MSG": "Category {} was successfully deleted".format(id), "CAT_ID": id, "CODE": "201"})
    except:
        if response.status_code == 404:
            return json.dumps({"STATUS": "ERROR", "MSG": "Category {} not found".format(id), "CAT_ID": id, "CODE": response.status_code})
        elif response.status_code == 500:
            return json.dumps({"STATUS": "ERROR", "MSG": "Internal error", "CAT_ID": id, "CODE": response.status_code})
        else:
            return json.dumps({"STATUS": "ERROR", "MSG": "Category {} was not deleted due to an error".format(id), "CAT_ID": id, "CODE": response.status_code})


# Fetch the list of categories to display in the store
@get('/categories')
def fetch_categories():
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM category"
            cursor.execute(sql)
            categories = cursor.fetchall()
            return json.dumps({"STATUS": "SUCCESS", "CATEGORIES": categories, "CODE": "200"})

    except Exception as e:
        return json.dumps({"STATUS": "ERROR", "MSG": str(e), "CODE": "500"})


# Add / Edit a product
@post('/product')
def add_or_edit_product():
    id_product = request.forms.get('id')
    category = request.forms.get('category')
    title = request.forms.get('title')
    desc = request.forms.get('desc')
    favorite = request.forms.get('favorite')
    price = request.forms.get('price')
    img_url = request.forms.get('img_url')

    # Need to convert the favorite value, as specified in the assignment
    if favorite == "on":
        favorite = 1
    else:
        favorite = 0

    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO product (title, category_name, description, favorite, price, img_url) VALUES ('{}', '{}', '{}', '{}', '{}', '{}')".format(title,
                                                                                                                                                      category,
                                                                                                                                                      desc,
                                                                                                                                                      favorite,
                                                                                                                                                      price,
                                                                                                                                                      img_url)
            cursor.execute(sql)
            connection.commit()
            return json.dumps({"STATUS": "SUCCESS", "PRODUCT_ID": cursor.lastrowid, "CODE": "201"})
    except Exception as e:
        return json.dumps({"STATUS": "ERROR", "MSG": str(e), "CODE": "404"})


# run(host='0.0.0.0', port=argv[1])
if __name__ == "__main__":
    run(host='localhost', port=7000)
