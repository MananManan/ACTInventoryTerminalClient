import sys
sys.path.append("..")
from CmdDatabaseClient.util_methods import *

def make_English_list():
    assert format_into_English_list(["Abel"]) == "Abel"
    assert format_into_English_list(["Abel", "Andrew"]) == "Abel and Andrew"
    assert format_into_English_list(["Abel", "Andrew", "Beerus"]) == "Abel, Andrew and Beerus"
    assert format_into_English_list(["Abel", "Andrew", "Beerus", "Vegita"]) == "Abel, Andrew, Beerus and Vegita"
