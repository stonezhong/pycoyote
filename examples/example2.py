#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os

from flask import Flask, render_template, redirect, url_for, request
from pycoyote import DIV, SPAN, Component

app = Flask(__name__, static_folder='static')

@app.route('/')
def home_page():
    return render_template(
        'index.html', 
        content = MainPage(
            {"color": "green"},
            DIV("Example ends here")
        )
    )

def main():
    app.run(debug=True)

class MainPage(Component):
    def render(self):
        return DIV(
            # You can pass class as list if you need multiple classes
            # You can pass style as dict if you need multiple styles
            SPAN(
                {
                    "class": ["bold","italic"], 
                    "style": {
                        "background-color": self.props['color'],
                        "font-family": "'Arial', sans-serif"
                    }
                },
                "Hello world!"
            ),
            *self.children
        )

if __name__ == '__main__':
    main()


