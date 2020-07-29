from flask import Flask, render_template, url_for

app = Flask(__name__)


def main():
    app.run(port=8080)


@app.route('/')
def test():
    return render_template('test.html')


if __name__ == '__main__':
    main()
