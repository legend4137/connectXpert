# Take input from the user
user_name = input("Enter user_id: ")

# Define the filename
user_filename = "user_id.txt"

# Write the input to a text file
with open(user_filename, "w") as file:
    file.write(user_name)