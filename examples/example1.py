#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os

from flask import Flask, render_template, redirect, url_for, request
from pycoyote import DIV, Component

app = Flask(__name__, static_folder='static')

@app.route('/')
def home_page():
    return render_template(
        'index.html', 
        content = MainPage()
    )

def main():
    app.run(debug=True)

class MainPage(Component):
    def render(self):
        return DIV({"class": "bold"},
            "Hello world!"
        )

if __name__ == '__main__':
    main()


