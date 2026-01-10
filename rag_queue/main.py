import pathlib
import uvicorn
from rag_queue.server import app

def main():
    # Use an import string so the reload subprocess can re-import the app.
    uvicorn.run(
        "rag_queue.server:app",
        # app,
        host="0.0.0.0",
        port=8080,
        reload=True,
        reload_dirs=[str(pathlib.Path(__file__).parent)],
    )


if __name__ == "__main__":
    main()
