import sys
from dictionary import ENtoHE, HEtoEN

def is_he(string):
    he_chars = [char for char in HEtoEN.keys()]

    # remove special charters that could result in false positives
    he_chars.remove('.')
    he_chars.remove(',')
    he_chars.remove('/')
    he_chars.remove("'")

    # check if any hebrew letters are present in the string
    # by checking if the set intersection has any values
    if set(he_chars) & set(string):
        return True
    return False

def convert(string):
    dict = HEtoEN if is_he(string) else ENtoHE
    return "".join([dict[char] if char in dict.keys() else char for char in string])

if __name__ == '__main__':
    # print(convert(sys.argv[1])) # use the function with a cmd parameter
    print(convert('v,ufbh, vzu nnhrv yexy ngcrh, ktbdkh,'))
    print(convert("איןד פרםערשצ בםמהקראד אקסא נקא'קקמ קמעךןדי שמג יקנרק'"))