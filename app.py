from flask import Flask, render_template, request, redirect, session, jsonify
import sqlite3, os, random, datetime

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "pixsecret")

DB = "db.sqlite3"

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT, email TEXT UNIQUE,
        senha TEXT, celular TEXT,
        pago INTEGER DEFAULT 0
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS draws (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tipo TEXT, numero INTEGER,
        data TEXT
    )''')
    conn.commit()
    conn.close()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/instant")
def instant():
    return render_template("instant.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        nome = request.form["nome"]
        senha = request.form["senha"]
        conn = sqlite3.connect(DB)
        c = conn.cursor()
        c.execute("SELECT id FROM users WHERE nome=? AND senha=?", (nome, senha))
        user = c.fetchone()
        conn.close()
        if user:
            session["user_id"] = user[0]
            return redirect("/")
        return "Login inválido"
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]
        senha = request.form["senha"]
        celular = request.form["celular"]
        conn = sqlite3.connect(DB)
        c = conn.cursor()
        c.execute("INSERT INTO users (nome,email,senha,celular) VALUES (?,?,?,?)",
                  (nome, email, senha, celular))
        conn.commit()
        conn.close()
        return redirect("/login")
    return render_template("register.html")

@app.route("/admin")
def admin():
    # Exibe lista de usuários e status de pagamento
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT id,nome,email,pago FROM users")
    users = c.fetchall()
    conn.close()
    return render_template("admin.html", users=users)

@app.route("/admin/pagar/<int:uid>")
def marcar_pago(uid):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("UPDATE users SET pago=1 WHERE id=?", (uid,))
    conn.commit()
    conn.close()
    return redirect("/admin")

@app.route("/api/sorteio-semanal")
def sorteio_semanal():
    numero = random.randint(100000, 999999)
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("INSERT INTO draws (tipo,numero,data) VALUES (?,?,?)",
              ("semanal", numero, datetime.datetime.utcnow().isoformat()))
    conn.commit()
    conn.close()
    return jsonify({"numero_sorteado": numero})

@app.route("/api/sorteio-instant")
def sorteio_instant():
    numero = random.randint(100000, 999999)
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("INSERT INTO draws (tipo,numero,data) VALUES (?,?,?)",
              ("instant", numero, datetime.datetime.utcnow().isoformat()))
    conn.commit()
    conn.close()
    return jsonify({"numero_sorteado": numero})

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
