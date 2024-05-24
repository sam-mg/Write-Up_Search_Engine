# Import the necessary libraries
from googleapiclient.discovery import build
import gnupg
import os

# Define the custom search engine ID
my_cse_id = "e1dbd25a8766b4a9c"

# Function to decrypt the API key using GPG
def decrypt_api_key(gpg, password):
    """
    Decrypts the API key file using the provided password.

    Args:
        gpg (gnupg.GPG): The GPG object for encryption and decryption.
        password (str): The password to unlock the encrypted API key.

    Returns:
        bool: True if the decryption is successful, False otherwise.
    """
    with open("api_key.txt.gpg", "rb") as f:
        # Decrypt the API key file using the provided password
        status = gpg.decrypt_file(f, passphrase=password, output="api_key.txt")
        return status.ok

# Function to securely delete a file by overwriting it with random data
def secure_delete(file_path):
    """
    Securely deletes a file by overwriting it with random data.

    Args:
        file_path (str): The path to the file to be deleted.
    """
    with open(file_path, "wb") as f:
        # Overwrite the file with random data
        f.write(os.urandom(os.path.getsize(file_path)))

# Ask user for password to unlock the encrypted API key
gpg = gnupg.GPG()

while True:
    # Prompt the user to enter the password to unlock the API key
    password = input("\nEnter the password to unlock the API key (Ctrl+C to quit): ")

    if decrypt_api_key(gpg, password):
        # If the decryption is successful, print a success message and break the loop
        print("API key unlocked successfully!")
        break
    else:
        # If the decryption fails, print an error message and prompt the user again
        print("Wrong password. Please try again.")

# Read the decrypted API key
with open("api_key.txt", "r") as f:
    # Read the decrypted API key from the file
    my_api_key = f.read().strip()

# Prompt the user to enter the search query
search = input("\n\nEnter the Write-Up you want to Search for: ")
# Prepend "Writeup for " to the search query
search = "Writeup for " + search
# Set the number of links to retrieve
num_of_links = 10

def google_search(search, api_key, cse_id, **kwargs):
    """
    Performs a Google custom search using the provided API key and search query.

    Args:
        search (str): The search query.
        api_key (str): The API key for the custom search engine.
        cse_id (str): The custom search engine ID.
        **kwargs: Additional keyword arguments for the search query.

    Returns:
        list: A list of search results.
    """
    # Build the custom search service using the API key
    service = build("customsearch", "v1", developerKey=api_key)
    # Execute the search query and retrieve the results
    res = service.cse().list(q=search, cx=cse_id, **kwargs).execute()
    return res['items']

try:
    # Perform the Google custom search
    results = google_search(search, my_api_key, my_cse_id, num=num_of_links)

    # Initialize a counter for the search results
    n = 1
    for result in results:
        # Print each search result with its title and link
        print(f"\n{n}. {result['title']}\n{result['link']}")
        n += 1

    # Securely delete the API key file
    secure_delete("api_key.txt")
    os.remove("api_key.txt")

    print("\nExiting...")

except KeyboardInterrupt:
    # Handle the KeyboardInterrupt exception (e.g., when the user presses Ctrl+C)
    print("\nProgram terminated by user.")