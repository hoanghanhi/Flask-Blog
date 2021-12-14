from website.initial import create_app
from flask import Flask, render_template, request, redirect, url_for

app = create_app()

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500

if __name__== '__main__':
    app.run(debug=True)
