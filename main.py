from frontend.frontend import app

if __name__ == '__main__':
    app.run_server(debug=False, host='0.0.0.0', port=80)