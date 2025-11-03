
from config import BASE_PATH


try:
    file = open(f"{BASE_PATH}/requirements.txt")
    try:
        process(file)
    except OSError as e:
        print("OSError:", e)
    finally:
        file.close()
except Exception as e:
    print("Generic Error:", e)
else:
    # runs only when no error block is executed
    print("No error occured")
finally:
    print("End of program")


