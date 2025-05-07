# Scryfall Thief

A Python-based tool to fetch Magic: The Gathering card data from the Scryfall API and save it as a JSON file, wrapped in a sleek vaporwave-style GUI.

## Features
- Browse and select MTG sets from a dropdown.
- Download all cards from the chosen set.
- Save data to a JSON file with a customizable location.
- Stylish GUI with a custom background and rounded elements.

## Requirements
- Python 3.x
- Libraries:
  - `requests` (`pip install requests`)
  - `Pillow` (`pip install Pillow`)

## Installation
1. Clone the repository:
   git clone https://github.com/your-username/scryfall-thief.git
   cd scryfall-thief
2. Install dependencies:
   pip install -r requirements.txt
   (Create a `requirements.txt` file with `requests` and `Pillow` if needed.)
3. Run the script:
   python pobieracz_danych_scryfall.py

## Usage
1. Launch the app.
2. Select a Magic: The Gathering set from the dropdown.
3. Click "Pobierz i Zapisz" (Download and Save) to fetch data.
4. Choose a location to save the JSON file via the dialog.
5. Enjoy your freshly stolen data!

## Notes
- Requires an internet connection to fetch data from the Scryfall API.
- The GUI uses a custom background image hosted online – ensure the link is active.
- Handles pagination to get all cards from a set.

## Contributing
Feel free to fork, improve, or report issues. Pull requests are welcome!

## License
[MIT License]

## Contact
Questions? Hit me up at [brawlsmons@proton.me].
