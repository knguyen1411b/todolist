from app import create_app

app = create_app()

if __name__ == "__main__":
    import os

    host = os.getenv("HOST") or "0.0.0.0"
    port = int(os.getenv("PORT", 5000))
    debug_flag = (os.getenv("DEBUG") or "").lower() in {"1", "true", "yes", "on"}

    app.run(host=host, port=port, debug=debug_flag, use_reloader=debug_flag)
