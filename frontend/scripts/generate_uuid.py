#!/usr/bin/env python3
"""
Script to generate UUIDs for database records.
This can be used to ensure that UUIDs are properly generated for the id fields.
"""

import uuid
import sys

def generate_uuid():
    """
    Generate a UUID in string format.
    
    Returns:
        str: A UUID string in the format xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
    """
    return str(uuid.uuid4())

def generate_multiple_uuids(count):
    """
    Generate multiple UUIDs.
    
    Args:
        count (int): The number of UUIDs to generate
        
    Returns:
        list: A list of UUID strings
    """
    return [generate_uuid() for _ in range(count)]

def main():
    """
    Main function to run when the script is executed directly.
    """
    # Check if a count argument was provided
    if len(sys.argv) > 1:
        try:
            count = int(sys.argv[1])
            uuids = generate_multiple_uuids(count)
            for uuid_str in uuids:
                print(uuid_str)
        except ValueError:
            print(f"Error: '{sys.argv[1]}' is not a valid integer")
            sys.exit(1)
    else:
        # If no count was provided, just generate one UUID
        print(generate_uuid())

if __name__ == "__main__":
    main()
