import os
import uvicorn


def main() -> None:
    uvicorn.run(
        "src.server.server:app",
        host="127.0.0.1",
        port=4567,
        log_level="info",
        timeout_keep_alive=300,
        # reload=True,
        # reload_dirs=[str(package / "server")]
    )


if __name__ == "__main__":
    # with os.popen(f"npm start --prefix {package / 'client'}"):
    main()
