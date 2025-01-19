import sqlite3

from flask import (
    Flask,
    jsonify,
    make_response,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

app = Flask(__name__)
app.secret_key = "e6008a019495ffa0b29f43ad"
sqldbname = "database.db"


# Ham result_to_dict dung de chuyen products tu list ve dictionary
def user_result_to_dict(products):
    # Tao bien result la 1 empty list
    result = []
    conn = sqlite3.connect(sqldbname)
    c = conn.cursor()
    for item in products:
        c.execute("SELECT img1 FROM images WHERE productId = ?", (item[0],))
        # Tim kiem anh san pham tu table images theo productId va luu vao bien img
        img = c.fetchone()[0]
        new_dict = {
            "productId": item[0],
            "productName": item[1],
            "productPrice": item[2],
            "productImg": img,
        }
        # Tao moi 1 bien dict voi kieu dictionary va them vao list result
        result.append(new_dict)
    conn.close()
    # Tra ve bien result
    return result


# Ham get_max_id su dung de lay ra maxId tu 1 table
def get_max_id(table_name):
    conn = sqlite3.connect(sqldbname)
    c = conn.cursor()
    if table_name == "users":
        c.execute("SELECT MAX(userId) FROM users")
        # Tim kiem userId lon nhat trong table cart va luu vao max_id
        max_id = c.fetchone()[0]
        # Neu max_id == True (Trong table users co it nhat 1 row)
        if max_id:
            # Tang gia tri cua max_id len 1
            max_id = max_id + 1
        else:
            # Max_id == False (Trong table cart chua co ban ghi nao)
            # Gan max_id = 1
            max_id = 1
        # Tra ve max_id
        return max_id
    elif table_name == "carts":
        c.execute("SELECT MAX(cartId) FROM cart")
        # Tim kiem cartId lon nhat trong table cart va luu vao max_id
        max_id = c.fetchone()[0]
        # Neu max_id == True (Trong table cart co it nhat 1 row)
        if max_id:
            # Tang gia tri cua max_id len 1
            max_id = max_id + 1
        else:
            # Max_id == False (Trong table cart chua co ban ghi nao)
            # Gan max_id = 1
            max_id = 1
        # Tra ve max_id
        return max_id
    elif table_name == "products":
        c.execute("SELECT MAX(productId) FROM products")
        # Tim kiem productId lon nhat trong table products va luu vao max_id
        max_id = c.fetchone()[0]
        # Neu max_id == True (Trong table cart co it nhat 1 row)
        if max_id:
            # Tang gia tri cua max_id len 1
            max_id = max_id + 1
        else:
            # Max_id == False (Trong table cart chua co ban ghi nao)
            # Gan max_id = 1
            max_id = 1
        # Tra ve max_id
        return max_id
    elif table_name == "images":
        c.execute("SELECT MAX(imgId) FROM images")
        # Tim kiem imgId lon nhat trong table images va luu vao max_id
        max_id = c.fetchone()[0]
        if max_id:
            # Tang gia tri cua max_id len 1
            max_id = max_id + 1
            return max_id
        else:
            # Max_id == False (Trong table cart chua co ban ghi nao)
            # Gan max_id = 1
            max_id = 1
        # Tra ve max_id
        return max_id
    elif table_name == "order":
        c.execute('SELECT MAX(orderID) FROM "order"')
        # Tim kiem orderId lon nhat trong table order va luu vao max_id
        max_id = c.fetchone()[0]
        if max_id:
            # Tang gia tri cua max_id len 1
            max_id = max_id + 1
        else:
            # Max_id == False (Trong table cart chua co ban ghi nao)
            # Gan max_id = 1
            max_id = 1
        # Tra ve max_id
        return max_id


# Ham carousel dung de chon nhau nhien 1 so luong san pham nhat dinh tu table products
def carousel():
    conn = sqlite3.connect(sqldbname)
    c = conn.cursor()
    c.execute("SELECT productId, name, price FROM products ORDER BY RANDOM() LIMIT 5")
    # Chon ngau nhien 5 san pham tu table products va luu vao bien products
    products = c.fetchall()
    # Goi ham result_to_dict va truyen vao bien products
    return user_result_to_dict(products)


# Dinh tuyen ham index cho url '/'
@app.route("/", methods=["GET"])
def index():
    if "user" in session:
        # Kiem tra neu ton tai gia tri 'user' trong session (User da dang nhap)
        return render_template(
            "index.html", user=session["user_lname"], teams=teams(), carousel=carousel()
        )
    else:
        # Neu khong ton tai gia tri 'user' trong session (User chua dang nhap)
        return render_template("index.html", teams=teams(), carousel=carousel())


# Ham teams dung de hien lay ra cac record tu table teams
def teams():
    conn = sqlite3.connect(sqldbname)
    c = conn.cursor()
    c.execute("SELECT teamName, teamImg FROM teams")
    # Tim kiem teamName, teamImg tu table teams va luu vao bien teams
    teams = c.fetchall()
    conn.close()
    # Tao bien result la 1 empty list
    result = []
    for item in teams:
        new_dict = {"teamName": item[0], "teamImg": item[1]}
        # Tao moi bien dict voi kieu dictionary va them vao list result
        result.append(new_dict)
    # Tra ve bien result
    return result


# Dinh tuyen ham team cho url '/team'
@app.route("/team", methods=["GET"])
def team():
    if "user" in session:
        # Kiem tra neu ton tai gia tri 'user' trong session (User da dang nhap)
        return render_template(
            "displayTeam.html",
            user=session["user_lname"],
            teams=teams(),
            carousel=carousel(),
        )
    else:
        # Neu khong ton tai gia tri 'user' trong session (User chua dang nhap)
        return render_template("displayTeam.html", teams=teams(), carousel=carousel())


# Dinh tuyen ham get_team cho url '/team/ten doi bong' VD: '/team/manu'
@app.route("/team/<fteam>", methods=["GET"])
def get_team(fteam):
    conn = sqlite3.connect(sqldbname)
    c = conn.cursor()
    c.execute("SELECT productId, name, price FROM products WHERE team = ?", (fteam,))
    # Tim kiem cac san pham theo ten CLB duoc chon va luu vao products
    products = c.fetchall()
    c.execute("SELECT teamBanner FROM teams WHERE teamName = ?", (fteam,))
    # Tim kiem banner theo ten CLB duoc chon va luu vao bien banner
    banner = c.fetchone()[0]
    if "user" in session:
        # Kiem tra neu ton tai gia tri 'user' trong session (User da dang nhap)
        return render_template(
            "team.html",
            user=session["user_lname"],
            teams=teams(),
            items=user_result_to_dict(products),
            banner=banner,
        )
    else:
        # Neu khong ton tai gia tri 'user' trong session (User chua dang nhap)
        return render_template(
            "team.html",
            teams=teams(),
            items=user_result_to_dict(products),
            banner=banner,
        )


# Dinh tuyen ham nation cho url '/nations'
@app.route("/nations", methods=["GET"])
def nations():
    conn = sqlite3.connect(sqldbname)
    c = conn.cursor()
    c.execute("SELECT productId, name, price FROM products WHERE nation NOTNULL")
    # Tim kiem cac ban ghi co gia tri nation NOTNULL va luu vao products
    products = c.fetchall()
    # Render file nation.html va truyen vao gia tri cua bien products
    if "user" in session:
        # Kiem tra neu ton tai gia tri 'user' trong session (User da dang nhap)
        return render_template(
            "nation.html",
            user=session["user_lname"],
            items=user_result_to_dict(products),
        )
    else:
        # Neu khong ton tai gia tri 'user' trong session (User chua dang nhap)
        return render_template("nation.html", items=user_result_to_dict(products))


# Dinh tuyen ham search cho url '/search'
@app.route("/search", methods=["POST"])
def search():
    search_text = request.form["search"]
    conn = sqlite3.connect(sqldbname)
    c = conn.cursor()
    c.execute(
        "SELECT productId, name, price FROM products WHERE name LIKE '%"
        + search_text
        + "%'"
    )
    # Tim cac san pham co ten gan dung voi search_text va luu vao bien products
    products = c.fetchall()
    if "user" in session:
        # Kiem tra neu ton tai gia tri 'user' trong session (User da dang nhap)
        return render_template(
            "search.html",
            search=search_text,
            user=session["user_lname"],
            items=user_result_to_dict(products),
        )
    else:
        # Neu khong ton tai gia tri 'user' trong session (User chua dang nhap)
        return render_template(
            "search.html",
            search=search_text,
            items=user_result_to_dict(products),
        )


# Dinh tuyen ham product cho url '/product/id' VD: '/product/1/
@app.route("/product/<product_id>", methods=["GET"])
def product(product_id):
    conn = sqlite3.connect(sqldbname)
    c = conn.cursor()
    c.execute(
        "SELECT name, price, sizeTitle, infoTitle FROM products WHERE productId = ?",
        (product_id,),
    )
    # Tim kiem name, price, sizeTitle, infoTitle theo productId va luu vao bien item
    item = c.fetchone()
    c.execute(
        "SELECT img1, img2, img3, img4 FROM images WHERE productId = ?", (product_id,)
    )
    # Tim kiem img1-4 theo productId va luu vao bien img
    img = c.fetchone()
    result = {
        "productId": product_id,
        "productName": item[0],
        "productPrice": item[1],
        "productImg1": img[0],
        "productImg2": img[1],
        "productImg3": img[2],
        "productImg4": img[3],
        "sizeTitle": item[2],
        "infoTitle": item[3],
    }
    if "user" in session:
        # Kiem tra neu ton tai gia tri 'user' trong session (User da dang nhap)
        return render_template("product.html", user=session["user_lname"], item=result)
    else:
        # Neu khong ton tai gia tri 'user' trong session (User chua dang nhap)
        return render_template("product.html", item=result)


# Dinh tuyen ham login cho url '/login'
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Neu method la POST
        # Luu gia tri cua request json vao bien req
        req = request.get_json()
        username = req["username"]
        password = req["password"]
        conn = sqlite3.connect(sqldbname)
        c = conn.cursor()
        c.execute(
            "SELECT * FROM users WHERE username = ? AND password = ?",
            (username, password),
        )
        # Tim kiem ban ghi thoa man username va password luu vao bien user
        user = c.fetchone()
        if user:
            # Neu ton tai user, tao cac session can thiet
            session["user"] = True
            session["user_id"] = user[0]
            session["user_username"] = username
            session["user_fname"] = user[4]
            session["user_lname"] = user[5]
            cart = get_cart(user[0])
            session["cart"] = cart
            # Tao bien response co gia tri Status = 1
            response = make_response(jsonify({"Status": 1}))
            # Tra ve bien response
            return response
        else:
            # Neu khong ton tai user, tao bien response co gia tri Status = 1
            response = make_response(jsonify({"Status": 0}))
            # Tra ve bien response duoi dang json
            return response
    # Neu method la GET, render file login-form.html
    return render_template("login-form.html")


# Dinh tuyen ham logout cho url '/logout'
@app.route("/logout")
def logout():
    session.pop("user", None)
    session.pop("user_id", None)
    session.pop("user_username", None)
    session.pop("user_fname", None)
    session.pop("user_lname", None)
    # Xoa cac gia tri session va redirect ve index
    return redirect(url_for("index"))


# Dinh tuyen ham register cho url '/register'
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # Lay cac gia tri username, password, email, fname, lname, phone tu html form
        username = request.form["username"]
        password = request.form["password"]
        email = request.form["email"]
        fname = request.form["fname"]
        lname = request.form["lname"]
        phone = request.form["phone"]
        conn = sqlite3.connect(sqldbname)
        c = conn.cursor()
        c.execute(
            "SELECT * FROM users WHERE username = ? OR email = ?",
            (
                username,
                email,
            ),
        )
        # Tim kiem ban ghi thoa man username hoac email va luu vao bien check
        check = c.fetchone()
        if not check:
            # Neu check == False (username hoac email chua duoc su dung)
            # Goi ham get_max_id() voi tham so 'users' de lay id lon nhat trong table users
            max_id = get_max_id("users")
            c.execute(
                "INSERT INTO users VALUES (?,?,?,?,?,?,?)",
                (max_id, username, password, email, fname, lname, phone),
            )
            # Them ban ghi moi vao table users va redirect ve login
            conn.commit()
            return redirect(url_for("login"))
        else:
            # Neu check != False (username hoac email da duoc su dung)
            # Render file register.html, truyen vao thong bao loi
            return render_template(
                "register.html", error="Username or email already registered"
            )
    else:
        # Neu method la GET, render file register.html
        return render_template("register.html")


# Dinh tuyen ham user cho url '/user'
@app.route("/user", methods=["GET", "POST"])
def user():
    if "user" in session:
        # Kiem tra neu ton tai gia tri 'user' trong session (User da dang nhap)
        conn = sqlite3.connect(sqldbname)
        c = conn.cursor()
        if request.method == "POST":
            # Neu method la POST
            # Luu gia tri cua request json vao bien req
            req = request.get_json()
            user_id = session["user_id"]
            user_email = session["user_email"]
            user_fname = session["user_fname"]
            user_lname = session["user_lname"]
            user_phone = req["phone"]
            c.execute(
                "UPDATE users SET firstName = ?, lastName = ?, email = ?, phone = ? WHERE userId = ?",
                (user_fname, user_lname, user_email, user_phone, user_id),
            )
            # Cap nhat thong tin user, tao bien response co gia tri Status = 1
            conn.commit()
            response = make_response(jsonify({"Status": 1}))
            # Tra ve bien response
            return response
        else:
            # Neu method la GET
            user_id = session["user_id"]
            user_email = session["user_email"]
            user_fname = session["user_fname"]
            user_lname = session["user_lname"]
            c.execute("SELECT phone FROM users WHERE userId = ?", (user_id,))
            # Tim kiem SĐT theo userId va luu vao bien phone
            phone = c.fetchone()[0]
            data = {
                "user_id": user_id,
                "user_email": user_email,
                "user_fname": user_fname,
                "user_lname": user_lname,
                "phone": phone,
            }
            # Render file user.html
            return render_template("user.html", user=session["user_lname"], data=data)
    else:
        # Neu khong ton tai gia tri 'user' trong session (User chua dang nhap)
        return redirect(url_for("login"))


# Dinh tuyen ham user_change_password cho url '/user/change-password'
@app.route("/user/change-password", methods=["POST"])
def user_change_password():
    if "user" in session:
        # Kiem tra neu ton tai gia tri 'user' trong session (User da dang nhap)
        # Luu gia tri cua request json vao bien req
        req = request.get_json()
        user_id = session["user_id"]
        old_password = req["old_password"]
        new_password = req["new_password"]
        conn = sqlite3.connect(sqldbname)
        c = conn.cursor()
        c.execute("SELECT password FROM users WHERE userId = ?", (user_id,))
        # Tim kiem password theo userId va luu vao bien password
        password = c.fetchone()[0]
        if old_password != password:
            # Neu password user nhap != password trong database
            # Tao bien response co gia tri Status = 0
            response = make_response(jsonify({"code": 0}))
            # Tra ve bien response
            return response
        elif new_password == password:
            # Neu password moi == password trong database
            # Tao bien response co gia tri Status = 1
            response = make_response(jsonify({"code": 1}))
            # Tra ve bien response
            return response
        else:
            c.execute(
                "UPDATE users SET password = ? WHERE userId = ?",
                (new_password, user_id),
            )
            # Cap nhat password moi theo userId
            conn.commit()
            # Tao bien response co gia tri Status = 2
            response = make_response(jsonify({"code": 2}))
            # Tra ve bien response
            return response
    else:
        # Neu khong ton tai gia tri 'user' trong session (User chua dang nhap)
        return redirect(url_for("login"))


# Ham get_cart voi tham so id dung de lay ra cac ban ghi trong table cart
def get_cart(product_id):
    conn = sqlite3.connect(sqldbname)
    c = conn.cursor()
    c.execute(
        "SELECT productId, productName, productPrice, quantity FROM cart WHERE userId = ?",
        (product_id,),
    )
    # Tim kiem productId, productName, productPrice, quantity theo userId va luu vao bien products
    products = c.fetchall()
    # Tao bien result la 1 empty list
    result = []
    for item in products:
        c.execute("SELECT img1 FROM images WHERE productId = ?", (item[0],))
        # Tim kiem img1-4 theo productId va luu vao bien img
        img = c.fetchone()[0]
        new_dict = {
            "productId": item[0],
            "productName": item[1],
            "productPrice": item[2],
            "productImg": img,
            "quantity": item[3],
        }
        # Tao moi 1 bien dict voi kieu dictionary va them vao list result
        result.append(new_dict)
    conn.close()
    # Tra ve bien result
    return result


# Dinh tuyen ham add_to_cart cho url '/cart/add'
@app.route("/cart/add", methods=["POST"])
def add_to_cart():
    if "user" in session:
        # Kiem tra neu ton tai gia tri 'user' trong session (User da dang nhap)
        # Luu gia tri cua request json vao bien req
        req = request.get_json()
        product_id = int(req["productId"])
        quantity = int(req["quantity"])
        # Cap nhat cart
        cart = session.get("cart", [])
        check = False
        conn = sqlite3.connect(sqldbname)
        c = conn.cursor()
        for item in cart:
            # Kiem tra neu ton tai san pham trong cart => quantity
            if item["productId"] == product_id:
                item["quantity"] += quantity
                check = True
                c.execute(
                    "UPDATE cart SET quantity = ? WHERE productId = ?",
                    (item["quantity"], item["productId"]),
                )
                # Cap nhat lai quantity theo productId va thoat vong lap for
                conn.commit()
                break
        if not check:
            # Neu san pham chua co trong cart thi them moi san pham vao table cart
            max_id = get_max_id("carts")
            c.execute(
                "SELECT name, price FROM products WHERE productId = ?", (product_id,)
            )
            # Tim kiem name, price theo productId va luu vao bien result
            result = c.fetchone()
            c.execute(
                "INSERT INTO cart VALUES (?,?,?,?,?,?)",
                (
                    max_id,
                    session["user_id"],
                    product_id,
                    result[0],
                    result[1],
                    quantity,
                ),
            )
            # Them san pham moi vao table cart
            conn.commit()
            conn.close()
        # Cap nhat lai cart
        session["cart"] = get_cart(session["user_id"])
        # Tao bien response co gia tri Status = 1
        response = make_response(jsonify({"Status": 1}))
        # Tra ve bien response
        return response
    else:
        # Neu khong ton tai gia tri 'user' trong session (User chua dang nhap)
        # Tao bien response co gia tri Status = 0
        response = make_response(jsonify({"Status": 0}))
        # Tra ve bien response
        return response


# Dinh tuyen ham update_cart cho url '/cart/update'
@app.route("/cart/update", methods=["POST"])
def update_cart():
    if "user" in session:
        # Kiem tra neu ton tai gia tri 'user' trong session (User da dang nhap)
        # Luu gia tri cua request json vao bien req
        req = request.get_json()
        conn = sqlite3.connect(sqldbname)
        c = conn.cursor()
        # Duyet tung san pham trong request json
        for item in req:
            product_id = int(item["productId"])
            quantity = int(item["quantity"])
            c.execute(
                "UPDATE cart SET quantity = ? WHERE productId = ?",
                (quantity, product_id),
            )
            # Cap nhat quantity theo productId
            conn.commit()
        conn.close()
        # Cap nhat lai session['cart']
        session["cart"] = get_cart(session["user_id"])
        # Tao bien response co gia tri Status = 0
        response = make_response(jsonify({"Status": 1}))
        # Tra ve bien response
        return response
    else:
        # Neu khong ton tai gia tri 'user' trong session (User chua dang nhap)
        return redirect(url_for("login"))


# Dinh tuyen ham delete cho url '/delete'
@app.route("/cart/delete", methods=["POST"])
def delete_cart():
    if "user" in session:
        # Kiem tra neu ton tai gia tri 'user' trong session (User da dang nhap)
        # Luu gia tri cua request json vao bien req
        req = request.get_json()
        product_id = int(req["productId"])
        conn = sqlite3.connect(sqldbname)
        c = conn.cursor()
        c.execute("DELETE FROM cart WHERE productId = ?", (product_id,))
        # Xoa ban ghi trong table carts theo productId
        conn.commit()
        conn.close()
        # Tao bien response co gia tri Status = 1
        response = make_response(jsonify({"Status": 1}))
        # Tra ve bien response
        return response
    else:
        # Neu khong ton tai gia tri 'user' trong session (User chua dang nhap)
        return redirect(url_for("login"))


# Dinh tuyen ham cart cho url '/cart'
@app.route("/cart", methods=["GET"])
def view_cart():
    if "user" in session:
        # Kiem tra neu ton tai gia tri 'user' trong session (User da dang nhap)
        # Cap nhat lai session['cart']
        session["cart"] = get_cart(session["user_id"])
        # Tao bien cart luu gia tri session['cart'] hoac tao moi 1 empty list
        cart = session.get("cart", [])
        return render_template("cart.html", user=session["user_lname"], items=cart)
    else:
        # Neu khong ton tai gia tri 'user' trong session (User chua dang nhap)
        return render_template("login-form.html", cartError=True)


@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    if "user" in session and len(session.get("cart")) > 0:
        # Kiem tra neu ton tai gia tri 'user' trong session (User da dang nhap) va co san pham trong gio hang
        conn = sqlite3.connect(sqldbname)
        c = conn.cursor()
        if request.method == "POST":
            # Neu method la POST
            order_id = get_max_id("order")
            user_id = session["user_id"]
            # Luu gia tri cua request json vao bien req
            req = request.get_json()
            fname = req["fname"]
            lname = req["lname"]
            address = req["address"]
            email = req["email"]
            phone = req["phone"]
            note = req["note"]
            payment = req["payment"]
            total = req["total"]

            c.execute(
                "SELECT productId, quantity FROM cart WHERE userId = ?", (user_id,)
            )
            # Tim kiem productId, quantity theo userId va luu vao bien order
            order = c.fetchall()

            list_id = []
            list_quantity = []
            for i in range(len(order)):
                # Duyet mang order va them productId, quantity vao 2 mang list_id, list_quantity
                list_id.append(order[i][0])
                list_quantity.append(order[i][1])
            # Xu ly chuoi de chuyen list_id, list_quantity tu list => string
            list_id = str(list_id)[1:-1]
            list_quantity = str(list_quantity)[1:-1]

            c.execute("DELETE FROM cart WHERE userId = ?", (user_id,))
            # Xoa ban ghi trong table cart theo userId
            conn.commit()

            c.execute(
                'INSERT INTO "order" VALUES(?,?,?,?,?,?,?,?,?,?,?,?)',
                (
                    order_id,
                    user_id,
                    list_id,
                    list_quantity,
                    address,
                    phone,
                    payment,
                    fname,
                    lname,
                    note,
                    email,
                    total,
                ),
            )
            # Them moi ban ghi vao table order
            conn.commit()
            # Tra ve json
            return jsonify({"Msg": "Success"})
        else:
            # Neu method la GET
            # Cap nhat lai session['cart']
            session["cart"] = get_cart(session["user_id"])
            # Tao bien cart luu gia tri session['cart'] hoac tao moi 1 empty array
            cart = session.get("cart", [])
            user_id = session["user_id"]
            c.execute("SELECT phone, email FROM users WHERE userId = ?", (user_id,))
            # Tim kiem phone, email theo userId
            result = c.fetchone()
            phone = result[0]
            email = result[1]
            user = {
                "user_fname": session["user_fname"],
                "user_lname": session["user_lname"],
                "phone": phone,
                "email": email,
            }
            # Render file checkout.html
            return render_template("checkout.html", user=user, items=cart)
    else:
        # Neu khong ton tai gia tri 'user' trong session (User chua dang nhap)
        return redirect(url_for("index"))


# Ham check_admin dung de kiem tra tai khoan admin da duoc dang nhap chua
def check_admin():
    if "admin" in session:
        # Kiem tra neu 'admin' co trong session (Tai khoan admin da duoc dang nhap)
        # Neu co, tra ve gia tri True
        return True
    else:
        # Neu khong, tra ve gia tri False
        return False


# Ham admin_result_to_dict co chuc nang tuong tu ham user_result_to_dict
def admin_result_to_dict(products):
    result = []
    conn = sqlite3.connect(sqldbname)
    c = conn.cursor()
    for item in products:
        c.execute("SELECT img1 FROM images WHERE productId = ?", (item[0],))
        img = c.fetchone()[0]
        new_dict = {
            "productId": item[0],
            "productName": item[1],
            "productPrice": item[2],
            "quantity": item[3],
            "productImg": img,
        }
        result.append(new_dict)
    conn.close()
    return result


# Dinh tuyen ham admin_view cho url '/admin'
@app.route("/admin", methods=["GET"])
def admin_view():
    # Goi ham check admin (Kiem tra neu admin da dang nhap)
    if check_admin():
        # Render file adminView.html, truyen vao gia tri cua session['lname']
        conn = sqlite3.connect(sqldbname)
        c = conn.cursor()
        c.execute("SELECT productId, name, price, quantity FROM products")
        # Tim kiem productId, name, price, quantity trong table products va luu vao bien products
        products = c.fetchall()
        result = admin_result_to_dict(products)
        # Render file adminView.html
        return render_template(
            "adminView.html", admin=session["admin_lname"], items=result
        )
    else:
        # Neu admin chua dang nhap
        return redirect(url_for("admin_login"))


# Dinh tuyen ham admin_login cho url '/admin/login'
@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        req = request.get_json()
        # Meu method la POST, lay gia tri username, password tu request json
        username = req["username"]
        password = req["password"]
        conn = sqlite3.connect(sqldbname)
        c = conn.cursor()
        c.execute(
            "SELECT * FROM admin WHERE username = ? AND password = ?",
            (
                username,
                password,
            ),
        )
        # Tim kiem trong table admin theo gia tri username, password va luu vao admin
        admin = c.fetchone()
        if admin:
            # Neu ton tai admin, tao cac session can thiet
            session["admin"] = True
            session["admin_id"] = admin[0]
            session["admin_username"] = username
            session["admin_lname"] = admin[5]
            # Tao bien response co gia tri Status = 1
            response = make_response(jsonify({"Status": 1}))
            # Tra ve bien response
            return response
        else:
            # Tao bien response co gia tri Status = 0
            response = make_response(jsonify({"Status": 0}))
            # Tra ve bien response
            return response
    else:
        # Neu method la GET, render file adminLogin.html
        return render_template("adminLogin.html")


# Dinh tuyen ham admin_logout cho url '/admin/logout'
@app.route("/admin/logout")
def admin_logout():
    session.pop("admin", None)
    session.pop("admin_id", None)
    session.pop("admin_username", None)
    session.pop("admin_lname", None)
    # Xoa cac gia tri session va redirect ve admin_view
    return redirect(url_for("admin_view"))


# Dinh tuyen ham admin_search cho url '/admin/search'
@app.route("/admin/search", methods=["POST"])
def admin_search():
    if check_admin():
        # Goi ham check admin (Kiem tra neu admin da dang nhap)
        # Lay gia tri search tu html form
        search_text = request.form["search"]
        conn = sqlite3.connect(sqldbname)
        c = conn.cursor()
        c.execute(
            "SELECT productId, name, price, quantity FROM products WHERE name LIKE '%"
            + search_text
            + "%'"
        )
        # Tim cac san pham co ten gan dung voi search va luu vao bien products
        products = c.fetchall()
        result = admin_result_to_dict(products)
        # Render file adminSearch.html
        return render_template(
            "adminSearch.html", admin=session["admin_lname"], items=result
        )
    else:
        # Neu admin chua dang nhap
        return redirect(url_for("admin_login"))


# Ham check_none dung de kiem tra 1 string co gia tri 'None' hoac la 1 empty string
def check_none(text):
    if text == "None" or text == "":
        # Neu string co gia tri 'None' hoac la empty string
        # Tra ve None
        return None
    else:
        # Neu sai, tra ve gia tri cua string
        return text


# Dinh tuyen ham admin_update cho url '/admin/update/<product_id>', VD: '/admin/update/1'
@app.route("/admin/update/<product_id>", methods=["GET", "POST"])
def admin_update(product_id):
    if check_admin():
        # Goi ham check admin (Kiem tra neu admin da dang nhap)
        conn = sqlite3.connect(sqldbname)
        c = conn.cursor()
        if request.method == "POST":
            # Neu method la POST
            # Lay cac gia tri team, nation, name,... tu html form
            team = check_none(request.form["team"])
            nation = check_none(request.form["nation"])
            name = request.form["name"]
            price = request.form["price"]
            quantity = request.form["quantity"]
            size_title = request.form["sizeTitle"]
            info_title = request.form["infoTitle"]
            img1 = request.form["img1"]
            img2 = request.form["img2"]
            img3 = request.form["img3"]
            img4 = request.form["img4"]
            c.execute(
                "UPDATE products SET "
                "team = ?, nation = ?, name = ?, price = ?, quantity = ?, sizeTitle = ?, infoTitle = ? "
                "WHERE productId = ?",
                (
                    team,
                    nation,
                    name,
                    price,
                    quantity,
                    size_title,
                    info_title,
                    product_id,
                ),
            )
            # Cap nhat gia tri team, nation, name,... theo productId
            conn.commit()
            c.execute(
                "UPDATE images SET img1 = ?, img2 = ?, img3 = ?, img4 = ? WHERE productId = ?",
                (
                    img1,
                    img2,
                    img3,
                    img4,
                    product_id,
                ),
            )
            # Cap nhat gia tri img1-4 theo productId
            conn.commit()
            conn.close()
            # Redirect ve admin_view
            return redirect(url_for("admin_view"))
        else:
            # Neu method la GET
            conn = sqlite3.connect(sqldbname)
            c = conn.cursor()
            c.execute(
                "SELECT team, nation, name, price, quantity, sizeTitle, infoTitle FROM products WHERE productId = ?",
                (product_id,),
            )
            # Tim kiem team, nation, name,... theo productId va luu vao bien item
            item = c.fetchone()
            result = {
                "id": product_id,
                "team": item[0],
                "nation": item[1],
                "name": item[2],
                "price": item[3],
                "quantity": item[4],
                "sizeTitle": item[5],
                "infoTitle": item[6],
            }
            c.execute(
                "SELECT img1, img2, img3, img4 FROM images WHERE productId = ?",
                (product_id,),
            )
            # Tim kiem img1-4 theo productId va luu vao bien imgs
            imgs = c.fetchone()
            img = {"img1": imgs[0], "img2": imgs[1], "img3": imgs[2], "img4": imgs[3]}
            # Render file adminUpdate.html
            return render_template("adminUpdate.html", item=result, img=img)
    else:
        # Neu admin chua dang nhap
        return redirect(url_for("admin_login"))


# Dinh tuyen ham admin_price cho url '/admin/update/price/<product_id>' VD: '/admin/update/price/1'
@app.route("/admin/update/price/<product_id>", methods=["POST"])
def admin_price(product_id):
    if check_admin():
        # Goi ham check admin (Kiem tra neu admin da dang nhap)
        # Luu gia tri cua request json vao bien req
        req = request.get_json()
        new_price = req["price"]
        conn = sqlite3.connect(sqldbname)
        c = conn.cursor()
        c.execute(
            "UPDATE products SET price = ? WHERE productId = ?", (new_price, product_id)
        )
        # Cap nhat price theo productId
        conn.commit()
        # Tao bien response co gia tri Status = 1
        response = make_response(jsonify({"Status": 1}))
        # Tra ve bien response
        return response
    else:
        # Neu admin chua dang nhap
        return redirect(url_for("admin_login"))


# Dinh tuyen ham admin_quantity cho url '/admin/update/quantity/<product_id>' VD: '/admin/update/quantity/1'
@app.route("/admin/update/quantity/<product_id>", methods=["POST"])
def admin_quantity(product_id):
    if check_admin():
        # Goi ham check admin (Kiem tra neu admin da dang nhap)
        # Luu gia tri cua request json vao bien req
        req = request.get_json()
        new_quantity = req["quantity"]
        conn = sqlite3.connect(sqldbname)
        c = conn.cursor()
        c.execute(
            "UPDATE products SET quantity = ? WHERE productId = ?",
            (new_quantity, product_id),
        )
        # Cap nhat quantity theo productId
        conn.commit()
        # Tao bien response co gia tri Status = 1
        response = make_response(jsonify({"Status": 1}))
        # Tra ve bien response
        return response
    else:
        # Neu admin chua dang nhap
        return redirect(url_for("admin_login"))


# Dinh tuyen ham admin_quantity cho url '/admin/update/delete/<product_id>' VD: '/admin/update/delete/1'
@app.route("/admin/delete/<product_id>", methods=["POST"])
def admin_delete(product_id):
    if check_admin():
        # Goi ham check admin (Kiem tra neu admin da dang nhap)
        conn = sqlite3.connect(sqldbname)
        c = conn.cursor()
        c.execute("DELETE FROM products WHERE productId = ?", (product_id,))
        # Xoa ban ghi trong table products theo productId
        conn.commit()
        c.execute("DELETE FROM images WHERE productId = ?", (product_id,))
        # Xoa ban ghi trong table images theo productId
        conn.commit()
        conn.close()
        # Tao bien response co gia tri Status = 1
        response = make_response(jsonify({"Status": 1}))
        # Tra ve bien response
        return response
    else:
        # Neu admin chua dang nhap
        return redirect(url_for("admin_login"))


# Dinh tuyen ham admin_add cho url '/admin/add'
@app.route("/admin/add", methods=["GET", "POST"])
def admin_add():
    if check_admin():
        # Goi ham check admin (Kiem tra neu admin da dang nhap)
        conn = sqlite3.connect(sqldbname)
        c = conn.cursor()
        if request.method == "POST":
            # Neu method la POST
            # Lay cac gia tri team, nation, name,... tu html form
            team = check_none(request.form["team"])
            nation = check_none(request.form["nation"])
            name = request.form["name"]
            price = request.form["price"]
            quantity = request.form["quantity"]
            size_title = request.form["sizeTitle"]
            info_title = request.form["infoTitle"]
            img1 = request.form["img1"]
            img2 = request.form["img2"]
            img3 = request.form["img3"]
            img4 = request.form["img4"]
            product_id = get_max_id("products")
            img_id = get_max_id("images")
            c.execute(
                "INSERT INTO products VALUES(?,?,?,?,?,?,?,?)",
                (
                    product_id,
                    team,
                    nation,
                    name,
                    price,
                    quantity,
                    size_title,
                    info_title,
                ),
            )
            # Them san pham moi vao table products
            conn.commit()
            c.execute(
                "INSERT INTO images VALUES(?,?,?,?,?,?)",
                (img_id, product_id, img1, img2, img3, img4),
            )
            # Them hinh anh moi vao table imagee
            conn.commit()
            conn.close()
            # Redirect ve admin_view
            return redirect(url_for("admin_view"))
        else:
            # Neu method la GET
            # Render file adminAdd.html
            return render_template("adminAdd.html")
    else:
        # Neu admin chua dang nhap
        return redirect(url_for("admin_login"))


# Dinh tuyen ham admin_tracking cho url '/admin/tracking'
@app.route("/admin/tracking", methods=["GET"])
def admin_tracking():
    if check_admin():
        # Goi ham check admin (Kiem tra neu admin da dang nhap)
        conn = sqlite3.connect(sqldbname)
        c = conn.cursor()
        c.execute('SELECT * FROM "order"')
        # Lay ra cac ban ghi trong table order
        orders = c.fetchall()
        items = []
        for order in orders:
            # Duyet lan luot tung phan tu trong orders
            list_name = []
            list_price = []

            # Xu ly chuoi de lay ra productId va quantity
            if "," in order[2]:
                # Neu order[2] (Chuoi chua cac id) co chua ',' (Ton tai nhieu hon 1 id)
                list_id = order[2].split(",")
                list_quantity = order[3].split(",")
            else:
                # Neu order[2] khong chua ',' (Chi ton tai duy nhat 1 id)
                list_id = [order[2]]
                list_quantity = [order[3]]

            for product_id in list_id:
                # Duyet lan luot tung phan tu trong list_id
                c.execute(
                    "SELECT name, price FROM products WHERE productId = ?",
                    (product_id,),
                )
                # Tim kiem name, price theo productId va luu vao bien product
                product = c.fetchone()
                list_name.append(product[0])
                list_price.append(product[1])

            payment = ""
            if order[6] == 1:
                payment = "CK"
            elif order[6] == 2:
                payment = "COD"

            data = {
                "orderId": order[0],
                "productName": list_name,
                "price": list_price,
                "quantity": list_quantity,
                "address": order[4],
                "phone": order[5],
                "payment": payment,
                "fname": order[7],
                "lname": order[8],
                "note": order[9],
                "email": order[10],
                "total": order[11],
            }
            items.append(data)
        # Render file tracking.html
        return render_template(
            "tracking.html", admin=session["admin_lname"], items=items
        )
    else:
        # Neu admin chua dang nhap
        return redirect(url_for("admin_login"))


# Dinh tuyen ham admin_tracking cho url '/admin/tracking/<order_id>' VD: '/admin/tracking/1'
@app.route("/admin/tracking/<order_id>", methods=["GET", "POST"])
def admin_tracking_order(order_id):
    if check_admin():
        # Goi ham check admin (Kiem tra neu admin da dang nhap)
        conn = sqlite3.connect(sqldbname)
        c = conn.cursor()
        if request.method == "POST":
            # Neu method la POST
            # Lay gia tri order tu html form
            order = request.form["order"]
            c.execute('DELETE FROM "order" WHERE orderId = ?', (order,))
            # Xoa ban ghi trong table order theo orderId
            conn.commit()
            # Redirect ve admin_tracking
            return redirect(url_for("admin_tracking"))
        else:
            # Neu method la GET
            c.execute('SELECT * FROM "order" WHERE orderId = ?', (order_id,))
            # Tim kiem theo orderId va luu vao bien order
            order = c.fetchone()

            list_name = []
            list_price = []

            # Xu ly chuoi de lay ra productId va quantity
            if "," in order[2]:
                # Neu order[2] (Chuoi chua cac id) co chua ',' (Ton tai nhieu hon 1 id)
                list_id = order[2].split(",")
                list_quantity = order[3].split(",")
            else:
                # Neu order[2] khong chua ',' (Chi ton tai duy nhat 1 id)
                list_id = [order[2]]
                list_quantity = [order[3]]

            for product_id in list_id:
                # Duyet lan luot tung phan tu trong list_id
                c.execute(
                    "SELECT name, price FROM products WHERE productId = ?",
                    (product_id,),
                )
                # Tim kiem name, price theo productId va luu vao bien product
                product = c.fetchone()
                list_name.append(product[0])
                list_price.append(product[1])

            payment = ""
            if order[6] == 1:
                payment = "CK"
            elif order[6] == 2:
                payment = "COD"

            item = {
                "orderId": order[0],
                "productName": list_name,
                "price": list_price,
                "quantity": list_quantity,
                "address": order[4],
                "phone": order[5],
                "payment": payment,
                "fname": order[7],
                "lname": order[8],
                "note": order[9],
                "email": order[10],
                "total": order[11],
            }
            # Render file order.html
            return render_template("order.html", item=item)
    else:
        # Neu admin chua dang nhap
        return redirect(url_for("admin_login"))


@app.route("/admin/manage", methods=["GET"])
def admin_manage():
    if check_admin():
        conn = sqlite3.connect(sqldbname)
        c = conn.cursor()
        c.execute("SELECT username, email, lastName FROM admin")
        results = c.fetchall()
        admins = []
        for result in results:
            admin = {"username": result[0], "email": result[1], "lastName": result[2]}
            admins.append(admin)
        return render_template("adminManage.html", admins=admins)
    else:
        return redirect(url_for("admin_login"))


# @app.route('/admin/manage/<admin_id>', methods=['GET', 'POST'])
# def admin_manage_account(admin_id):
#     if check_admin():
#         conn = sqlite3.connect(sqldbname)
#         c = conn.cursor()
#         if request.method == 'POST':
#
#
#             return
#         else:
#             c.execute('SELECT email, firstName, lastName FROM admin WHERE adminId = ?', (admin_id,))
#             result = c.fetchone()
#             admin = {'email': result[0], 'firstName': result[1], 'lastName': result[2]}
#             return render_template('adminManageAccount.html', admin=admin)
#
#     else:
#         return redirect(url_for('admin_login'))

if __name__ == "__main__":
    app.run(debug=True, port=5005)
