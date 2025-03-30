from project_package.fast_api_app import app

if __name__ == "__main__":
    import uvicorn  # Use Uvicorn to start the app

    uvicorn.run(app, host="0.0.0.0", port=8000)