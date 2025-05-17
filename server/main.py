from app import app

import context

if __name__ == '__main__':
    app.run(debug=True, port=8080)

    context.close()
