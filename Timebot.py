#this is a hacky fix to keep a runnable file in the main folder for easier access
from sys import path
path.append('src')
from src import main