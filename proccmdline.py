import argparse

def proccmdline():
    parser = argparse.ArgumentParser(description = "Tee kayra-png:t lämpödatasta" )
    parser.add_argument("-d", "--debug", help="Testimoodi", action="store_true")
    args = parser.parse_args()
    return (args)
