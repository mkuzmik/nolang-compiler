FILENAME = "foo"
FILEDIR = "../input_files/"

with open(FILEDIR + FILENAME) as source:
    while True:
        char = source.read(1)
        if not char:
            print("End of file")
            break
        print("Read a character: " + char)

