import urllib.request
import urllib.error  # For handling HTTP and URL errors
# This script demonstrates how to make a GET request to an API using Python's urllib library.
# It includes error handling for common issues like HTTP errors and URL errors.
# The script retrieves data from the NOAA Climate Data Online API and parses the JSON response.
# The script is designed to be run as a standalone program, but the main functionality is encapsulated in the call_api function.
# The script uses the urllib library to make HTTP requests and handle responses.
# The script is designed to be run as a standalone program, but the main functionality is encapsulated in the call_api function.
import json
import os

web_site = 'https://www.ncdc.noaa.gov/cdo-web/api/v2/locations'
token = 'UHXohzHdhMmtTMDEsZrzsNJYqXsORDFt'

def call_api(url, token):
    """
    Make a GET request to the API and return a JSON response

    Args:
        url (str): The API endpoint URL
        token (str): The API token for authentication
    Returns:
        dict: The parsed JSON response from the API
    Summary of What Happens
    1. A Request object is created for the URL.
    2. A custom header (token) is added to the request.
    3. The request is sent to the server using urlopen.
    4. The server's response is read, decoded from bytes to a string, and parsed as JSON.
    5. The resulting Python object (data) contains the parsed JSON data.
    """
    try:
        req = urllib.request.Request(url)
        req.add_header('token', token)
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            # Get the remaining rate limit from the headers
            rate_limit_remaining = int(response.headers.get('X-RateLimit-Remaining', 0))
            return data, rate_limit_remaining

    except urllib.error.HTTPError as e:
        # Handle HTTP errors (e.g., 404, 401)
        print(f"HTTP Error: {e.code} - {e.reason}")
    except urllib.error.URLError as e:
        # Handle URL errors (e.g., network issues)
        print(f"URL Error: {e.reason}")
    except json.JSONDecodeError as e:
        # Handle JSON parsing errors
        print(f"JSON Decode Error: {e.msg}")
    except Exception as e:
        # Handle any other unexpected errors
        print(f"An unexpected error occurred: {e}")

    return None,0  # Return None if an error occurs

def save_json_to_file(data, filename):
    """
    Save JSON data to a file

    Args:
        data (dict): The JSON data to save
        filename (str): The name of the file to save the data to
    """
    try:
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4) # Pretty print the JSON, the indentation level is 4 spaces
            print(f'Data saved to {filename}')
    except IOError as e:
        # Handle file I/O errors
        print(f'File I/O Error: {e}')
    except Exception as e:
        # Handle any other unexpected errors
        print(f'An unexpected error occurred while saving the file: {e}')



if __name__ == '__main__':
    remaining_requests = 1 #  Initialize remaining requests to 1
    offset = 0 # # offset is used to paginate through the API results. 
    limit = 1000 # The maximum number of records to retreieve in one request
    file_counter = 0 # Initialize file counter to 0

    while remaining_requests > 0 and file_counter < 39:
        # construct the URL with the offset and limit parameters
        url = f'{web_site}?offset={offset}&limit={limit}' # what is happening here on this line?
        # Call the API and get the response

        response, remaining_requests = call_api(url, token)
        
        # Check if the response is valid
        if response:
            # save response to a file
            output_file = f'locations_{file_counter}.json'
            save_json_to_file(response, output_file)

            # Increment the file counter
            offset += limit
            file_counter += 1
        else:
            print('Failed to retrieve data from API, exiting loop')
            break
        
    
    print('All files saved successfully.')

