from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import sqlite3

app = Flask(__name__)
sqldbname = 'database.db'
app.secret_key = 'e6008a019495ffa0b29f43ad'


if __name__ == '__main__':
    app.run(debug=True, port=5005)
