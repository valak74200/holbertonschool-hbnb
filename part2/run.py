from app import create_app
import sys

print("Starting the application...")

try:
    app = create_app()
    print("Application created successfully.")
except Exception as e:
    print(f"Error creating the application: {e}", file=sys.stderr)
    sys.exit(1)

if __name__ == '__main__':
    print("Running the application...")
    app.run(debug=True, use_reloader=False)
