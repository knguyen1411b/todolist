from app import create_app
import os

app = create_app()

if __name__ == '__main__':
    host = os.getenv('HOST') or os.getenv('FLASK_RUN_HOST') or '0.0.0.0'
    port_env = os.getenv('PORT') or os.getenv('FLASK_RUN_PORT') or '5000'
    try:
        port = int(port_env)
    except ValueError:
        port = 5000

    debug_flag = (os.getenv('DEBUG') or '').lower() in {'1', 'true', 'yes', 'on'}

    app.run(host=host, port=port, debug=debug_flag, use_reloader=debug_flag, threaded=True)
