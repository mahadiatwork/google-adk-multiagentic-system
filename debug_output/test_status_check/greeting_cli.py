def greet(name: str) -> None:
    """Prints a greeting message to the user."""
    print(f"Hello, {name}! Welcome to the CLI tool.")

if __name__ == "__main__":
    try:
        user_name = input("Please enter your name: ").strip()
        while not user_name:
            print("Name cannot be empty. Please try again.")
            user_name = input("Please enter your name: ").strip()
        greet(user_name)
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")