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
        # Makes sure we don't add a product with missing values:
        for i in [category, title, desc, favorite, price, img_url]:
            if i == "":
                return json.dumps({"STATUS": "ERROR", "MSG": "Some parameters are missing", "CODE": "400"})
        print(type(price))

        with connection.cursor() as cursor:
            # The if / else differenciate our actions for add/edit of product
            if id_product == "":
                sql = "INSERT INTO product (title, category_name, description, favorite, price, img_url) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}')".format(title,
                                                                                                                                                          category,
                                                                                                                                                          desc,
                                                                                                                                                          favorite,
                                                                                                                                                          price,
                                                                                                                                                          img_url)
            else:
                sql = "UPDATE product SET title = '{0}', category_name = '{1}', description = '{2}', favorite = '{3}', price = '{4}', img_url = '{5}' WHERE id_product = '{6}' ".format(title,
                                                                                                                                                                                        category,
                                                                                                                                                                                        desc,
                                                                                                                                                                                        favorite,
                                                                                                                                                                                        price,
                                                                                                                                                                                        img_url,
                                                                                                                                                                                        id_product)
            cursor.execute(sql)
            connection.commit()
            return json.dumps({"STATUS": "SUCCESS", "MSG": "Product was added/updated successfully", "PRODUCT_ID": cursor.lastrowid, "CODE": "201"})

    except Exception as e:
        if response.status_code == 404:
            return json.dumps({"STATUS": "ERROR", "MSG": "Category not found", "CODE": "404"})
        elif response.status_code == 500:
            return json.dumps({"STATUS": "ERROR", "MSG": "Internal Error", "CODE": "500"})
        else:
            return json.dumps({"STATUS": "ERROR", "MSG": str(e)})


# Delete a product
@delete('/product/<id>')
def delete_product(id):
    try:
        with connection.cursor() as cursor:
            sql = "DELETE FROM product WHERE id = '{}'".format(id)
            cursor.execute(sql)
            connection.commit()
            return json.dumps({"STATUS": "SUCCESS", "MSG": "Product {} was successfully deleted".format(id), "CODE": "201"})
    except:
        if response.status_code == 404:
            return json.dumps({"STATUS": "ERROR", "MSG": "Product {} not found".format(id), "CODE": response.status_code})
        elif response.status_code == 500:
            return json.dumps({"STATUS": "ERROR", "MSG": "Internal error", "CODE": response.status_code})
        else:
            return json.dumps({"STATUS": "ERROR", "MSG": "Product {} was not deleted due to an error".format(id), "CODE": response.status_code})


# run(host='0.0.0.0', port=argv[1])
if __name__ == "__main__":
    run(host='localhost', port=7000)
