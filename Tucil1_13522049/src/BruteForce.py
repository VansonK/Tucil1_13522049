import time
import random

class Token :
    def __init__(self, content, point, list_of_coordinate=[]):
        self.content = content
        self.list_of_coordinate = list_of_coordinate
        self.point = point

class Coordinate :
    def __init__ (self, row, col) :
        self.row = row
        self.col = col

# variabel global
hasil = Token("Nan", 0, [])
bank = []

# fungsi pendukung
def resetMatrixUsage(matrix) :
    for i in range(len(matrix)) :
        for j in range(len(matrix[0])) :
            matrix[i][j][1] = False

def fillMatrixUsage(matrix, list_of_coordinate) :
    for i in range(len(list_of_coordinate)) :
        matrix[list_of_coordinate[i].row][list_of_coordinate[i].col][1] = True

def stringCheck(string, sequence) :
    global hasil
    string.point = 0
    for i in range(len(sequence)) :
        if (sequence[i][0] in string.content) :
            string.point += sequence[i][1]

    if (string.point > hasil.point) :
        hasil.content = string.content
        hasil.point = string.point
        hasil.list_of_coordinate = string.list_of_coordinate

    if (string.point == hasil.point) :
        if (len(string.content) < len(hasil.content)) :
            hasil.content = string.content
            hasil.point = string.point
            hasil.list_of_coordinate = string.list_of_coordinate    

def createCopy(b) :
    temp = []
    for i in range(len(b)) :
        temp.append(b[i])
    return temp

def displayCoordinate(string) :
    for i in range(len(string.list_of_coordinate)) :
        print(f"{string.list_of_coordinate[i].col+1},{string.list_of_coordinate[i].row+1}")

def generateBank(matrix, count, arah, answer) : # arah = 0 = ver , arah = 1 = hor
    if (count == 0) : # basis
        global bank
        bank.append(answer)
    else :
        count -= 1
        if (arah == 0) :
            alamat = answer.list_of_coordinate[-1]
            alamatcol = alamat.col
            for i in range(len(matrix)) :
                resetMatrixUsage(matrix)
                fillMatrixUsage(matrix, answer.list_of_coordinate)
                if (matrix[i][alamatcol][1] == True) :
                    continue
                else :
                    temp = createCopy(answer.list_of_coordinate)
                    answer2 = Token(answer.content, answer.point, temp)
                    matrix[i][alamatcol][1] = True
                    answer2.content += " " + matrix[i][alamatcol][0]
                    answer2.list_of_coordinate.append(Coordinate(i, alamatcol))
                    stringCheck(answer2, sequence)

                    generateBank(matrix, count, 1, answer2)
        else :
            alamat = answer.list_of_coordinate[-1]
            alamatrow = alamat.row
            for i in range(len(matrix[0])) :
                resetMatrixUsage(matrix)
                fillMatrixUsage(matrix, answer.list_of_coordinate)                
                if (matrix[alamatrow][i][1] == True) :
                    continue
                else :
                    temp = createCopy(answer.list_of_coordinate)
                    answer2 = Token(answer.content, answer.point, temp)
                    matrix[alamatrow][i][1] = True
                    answer2.content += " " + matrix[alamatrow][i][0]
                    answer2.list_of_coordinate.append(Coordinate(alamatrow, i))
                    stringCheck(answer2, sequence)

                    generateBank(matrix, count, 0, answer2)

def saveFile(executionTime) :
    while (True) :
            save = str(input("Do you want to save the solution? (y/n) "))
            if (save == "y") :
                nama = str(input("Enter file name : "))
                if (".txt" not in nama) :
                    nama += ".txt"
                file = open("../test/" + nama, "w")
                file.write("")
                file = open("../test/" + nama, "a")
                file.write(str(hasil.point) + "\n")
                if (hasil.point != 0) :
                    file.write(hasil.content + "\n")
                    for i in range(len(hasil.list_of_coordinate)) :
                        file.write(f"{hasil.list_of_coordinate[i].col+1},{hasil.list_of_coordinate[i].row+1}\n")
                file.write("\n" + str(executionTime) + " ms")

                break
            elif (save == "n") :
                break
            else :
                print("Wrong input! \n")
    
# main program
print("--------------------------------------")
print("|| BREACH PROTOCOL OPTIMAL SOLUTION ||")
print("--------------------------------------")

load = str(input("\nDo you want to load existing txt file? (y/n) "))
if (load == "y") :
    while(True) :
        nama = str(input("Enter file name : "))
        if (".txt" not in nama) :
            nama += ".txt"
        try :    
            file = open("../test/" + nama, "r")
        except FileNotFoundError :
            print("File tidak ditemukan\n")
        else :
            break 
    
    print("\nLoading...\n")
    buffer_size = int(file.readline())
    col = int(file.read(2))
    row = int(file.readline())

    matrix = [[[0 , False] for i in range(col)] for j in range(row)]
    for i in range (row) :
        for j in range(col) :
            matrix[i][j][0] = file.read(2)
            blank = file.read(1)

    number_of_sequence = int(file.readline())

    sequence = [["Nan" , 0] for i in range (number_of_sequence)]
    for i in range(number_of_sequence) :
        sequence[i][0] = file.readline() [:-1]
        sequence[i][1] = int(file.readline())

    start = time.time()
    for i in range(len(matrix[0])) :
        a = []
        a.append(Coordinate(0,i))
        coba = Token(matrix[0][i][0], 0, a)
        generateBank(matrix, buffer_size-1, 0, coba)
    end = time.time()
    executionTime = round((end - start) * 1000)

    print("--------------")
    print("|| Solution ||")
    print("--------------")
    print(hasil.point)
    if (hasil.point <= 0) :
        print("Tidak ada solusi yang optimal!")
    else :
        print(hasil.content)
        displayCoordinate(hasil)

    print("\n")
    print(executionTime, "ms")

    saveFile(executionTime)


elif (load == "n") :
    print("\nRequesting Information...")
    jumlah_token_unik = int(input("Number of unique token : "))
    token_unik = []
    template = str(input(f"Enter {jumlah_token_unik} unique token separated by blank: "))
    if (len(template) < ((jumlah_token_unik*3) - 1)) :
        print("\nInput invalid! Abort program... \n")
    else :
        for i in range(jumlah_token_unik) :
            temp = template[i*3] + template[(i*3)+1]
            token_unik.append(temp)

        buffer_size = int(input("\nBuffer size : "))
        print("\n|| Matrix size ||")
        col = int(input("Column size : "))
        row = int(input("Row size : "))

        matrix = [[[token_unik[random.randint(0,jumlah_token_unik-1)], False] for i in range(col)] for j in range(row)]

        while(True) :
            number_of_sequence = int(input("\nNumber of Sequence : "))
            sequence_size = int(input("Maximum sequence size : "))
            if ((sequence_size <= 1) or (number_of_sequence < 1)) :
                print("Minimum number of 1 sequence and sequence size of 2!")
            else :
                break

        sequence = [["Nan" , 0] for i in range (number_of_sequence)]
        for i in range(number_of_sequence) :
            temp = ""
            for j in range(0, random.randint(2, sequence_size)) :
                temp += token_unik[random.randint(0, jumlah_token_unik-1)]
                temp += " "
            sequence[i][0] = temp [:-1]
            sequence[i][1] = random.randint(2,6) * 5

        print("\nGenerating...")
        
        print("\n|| Generated Matrix ||" , end="")
        for i in range(row) :
            print("")
            for j in range(col) :
                print(matrix[i][j][0], end=" ")
        
        print("\n\n|| Generated Sequences ||")
        for i in range(number_of_sequence) :
            print(sequence[i][0]) 
            print(sequence[i][1] , "points\n")

        print("Loading...\n")

        start = time.time()
        for i in range(len(matrix[0])) :
            a = []
            a.append(Coordinate(0,i))
            coba = Token(matrix[0][i][0], 0, a)
            generateBank(matrix, buffer_size-1, 0, coba)
        end = time.time()
        executionTime = round((end - start) * 1000)

        print("--------------")
        print("|| Solution ||")
        print("--------------")
        print(hasil.point)
        if (hasil.point <= 0) :
            print("Tidak ada solusi yang optimal!")
        else :
            print(hasil.content)
            displayCoordinate(hasil)

        print("\n")
        print(executionTime, "ms")
    
        saveFile(executionTime)

else :
    print("Sorry! Wrong input")