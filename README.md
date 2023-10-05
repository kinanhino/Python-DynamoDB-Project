# Role a Poke Game 🎲
Welcome to the "Role a Poke" game, where you can randomly fetch details of a Pokémon from the Pokémon API and store them in an AWS DynamoDB table for future reference!

![Pokemon Logo](https://upload.wikimedia.org/wikipedia/commons/9/98/International_Pokémon_logo.svg)


Table of Contents
Description
Prerequisites
Setup & Running
Gameplay
DynamoDB Table Schema
Notes
Contributing
License
Description
The "Role a Poke" game allows you to roll a Pokémon from the Pokémon API. If the rolled Pokémon is already present in a DynamoDB table named pokemon-table, its details will be fetched and displayed. If not, it will be retrieved from the Pokémon API, showcased, and subsequently stored in the DynamoDB table for future references.

Prerequisites
Python: Ensure Python is installed on your system.

Dependencies: Install the required Python libraries using pip:

bash
Copy code
pip install python-dotenv requests boto3
AWS Credentials: These are essential. Set them up using the AWS CLI or by manually adding them in a .env file.

AWS DynamoDB: Ensure you have an active AWS account with the necessary permissions to create and manage DynamoDB tables.

Setup & Running
Environment Variables:

Store your credentials and other environment-specific settings in a .env file, like:

makefile
Copy code
AWS_ACCESS_KEY=YOUR_AWS_ACCESS_KEY
AWS_SECRET_KEY=YOUR_AWS_SECRET_ACCESS_KEY
AWS_SESSION_KEY=YOUR_OPTIONAL_AWS_SESSION_KEY
AWS_REGION=YOUR_AWS_REGION
Run the Game:

Navigate to your script's directory and execute:

bash
Copy code
python your_script_name.py
Gameplay
The game welcomes players with: "Welcome to Role a Poke Game".
Players then decide whether to roll a Pokémon (y) or exit (n).
Rolled Pokémon are checked against the pokemon-table in DynamoDB.
If present, their details are displayed.
If not, they're fetched from the Pokémon API, displayed, and then stored in the DynamoDB table.
Continue rolling or say goodbye!
DynamoDB Table Schema
pokemon-table in DynamoDB comprises:
id (Number) - Pokémon ID.
Name (String) - Pokémon's name.
Poke_Abilites (String Set) - Abilities of the Pokémon.
Types (String Set) - Types of the Pokémon.
Notes
Always handle AWS credentials securely. Do not expose them.
Be aware of potential costs related to AWS resources.
This game fetches Pokémon details via PokéAPI.
Contributing
Interested in making this game even better? Fork the repository, dive into the code, and send those pull requests!

License
This project is free to use. Be cautious with AWS credentials and stay updated on associated AWS costs.
