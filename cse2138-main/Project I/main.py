# Author: Fatma Balcı
# Student Number: 150119744
# CSE 2138 - Project I
# Fatma Corut Ergin
# Fall 2020

# This is the class written to satisfy all the operations that the project needs to handled
class BinaryConverter:
    def __init__(self):
        '''
            attributes:
                - hexadecimalElements => This is the array consisting of hex symbols to be used by the class
                - dataTypes => This is the array containing data types that an hex number can be converted into
                - hexadecimalToBinary => This is a dictionary containing mappings from hex to binary
        '''
        self.hexadecimalElements = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F"]
        self.dataTypes = ["S", "U", "F"]
        self.hexadecimalToBinary = {
                                    "0": "0000",
                                    "1": "0001",
                                    "2": "0010",
                                    "3": "0011",
                                    "4": "0100",
                                    "5": "0101",
                                    "6": "0110",
                                    "7": "0111",
                                    "8": "1000",
                                    "9": "1001",
                                    "A": "1010",
                                    "B": "1011",
                                    "C": "1100",
                                    "D": "1101",
                                    "E": "1110",
                                    "F": "1111"
                                }

    # This is the function for converting an hex number to binary
    def convertToBinary(self, hexNumber):
        result = ''

        # Iterating over each hex num to map it to binary and sum them up in a string
        for item in hexNumber:
            result += self.hexadecimalToBinary[item]
        
        return result

    # This is the function for converting a binary number to decimal (integer only)
    def binaryToDecimal(self, binaryNumber):
        total = 0
        bit = len(binaryNumber)

        for i in range(bit-1, -1, -1):
            if binaryNumber[i] == '1':
                power = (bit-1) - i
                total += 2 ** power
        
        return total
    
    # This is the function for getting biases of floating points depending on their bits
    def getBias(self, numberOfBits):
        return 2 ** (numberOfBits - 1) - 1
    
    # This is the mapping function for getting the length of exponent part in any floating point number
    def getExponentBit(self, byte):
        if byte == 1:
            return 4
        elif byte == 2:
            return 6
        elif byte == 3:
            return 8
        else:
            return 10
    
    # This is the function returning the binary representation of the exponent value by getting binary and exponent bits
    def getExponentValue(self, binary, exponentBits):
        # Starting right after from the sign bit
        # it does splitting the binary number to get binary representation for exponent
        binaryValue = binary[1:(1 + exponentBits)]

        return binaryValue

    # This function returns the decimal value of fractional part of a binary number 
    def getFractionToDecimal(self, fraction):
        total = 0
        
        for i in range(len(fraction)):
            if fraction[i] == '1':
                total += 2 ** (-(i+1))

        return total
    
    # This function returns at max 13 characters-long fraction representation for a floating point number
    def getFractionValue(self, binary):
        byte = len(binary) / 8  # Getting byte

        expBits = self.getExponentBit(byte) # Getting exponent bits

        # If it is 3 or 4 bytes, it does rounding
        if byte == 3 or byte == 4:
            # rounding function is being called to apply nearest even
            roundedValue = self.roundFractionValue(binary[(1+expBits):])
            return roundedValue
        
        return binary[(1+expBits):]
    
    # This is the function returning the maximum unsigned value for given numberOfBits (UMax)
    def getMaxUnsignedValue(self, numberOfBits):
        return 2 ** numberOfBits - 1

    # This is the function for rounding the fraction part of a binary number to make it 13 bits long
    def roundFractionValue(self, fractionValue):
        isRounding = False
        # Case 1: if it is below the halfway
        if fractionValue[13] == '0':
            return fractionValue[:13]
        
        # Case 2: if it is greater than the halfway
        elif fractionValue[13] == '1' and '1' in fractionValue[14:]:
            isRounding = True
        
        # Case 3: if it is equal to the halfway and nearest even needed
        elif fractionValue[13] == '1' and fractionValue[12] == '1':
            isRounding = True
        
        # Case 4: if it is equal to the halfway and no need for nearest even rounding
        elif fractionValue[13] == '1' and fractionValue[12] == '0':
            return fractionValue[:13]
        
        # if rounding process is required, rounding process happens
        if isRounding:
            roundIndex = -1
            # Checking the round index to stop rounding
            for i in range(12, -1, -1):
                if fractionValue[i] == '0':
                    roundIndex = i
                    break
            
            roundedValue = ''
            # Rounding until the program sees roundIndex
            for i in range(13):
                if i == roundIndex:
                    roundedValue += '1'
                    continue
                if roundIndex != -1 and i >= (roundIndex + 1):
                    roundedValue += '0'
                    continue
                roundedValue += fractionValue[i]
            return roundedValue

    # This is the function checking if the fraction value is equal to zero or not
    def isFractionZero(self, binary):
        byte = len(binary) / 8
        expBits = self.getExponentBit(byte)
        fraction = binary[(1+expBits):]
        # Checking to make sure that each bit for fraction is zero
        for bit in fraction:
            if bit == '1':
                return False
        
        return True

    # This is the function checking if a given binary number is a valid floating point number
    def isValidFloatingNumber(self, binary):
        signBit = binary[0]  # sign bit
        returnText = ''

        if signBit == '1':
            returnText += '-'

        isDenormalized = False
        byte = len(binary) / 8  # byte of binary
        expBits = self.getExponentBit(byte)  # getting exp bit number
        exp = self.getExponentValue(binary,expBits)  # getting exp binary value
        expValue = self.binaryToDecimal(exp)  # getting exp as decimal
        isFractionZero = self.isFractionZero(binary) # checking is fraction zero or not
        maxValue = self.getMaxUnsignedValue(len(exp)) # getting UMax

        # if exp decimal equal to 0, this means the number is denormalized
        if (expValue == 0):
            isDenormalized = True

        # If a floating point is denormalized and the fraction zero, then result is +0 or -0
        if isDenormalized == True:
            if isFractionZero:
                if signBit == '1':
                    return False, '-0'
                return False, '+0'
        
        # if exp binary equals to all ones and fraction is zero
        if expValue == maxValue and isFractionZero:
            returnText += '∞'
            return False, returnText
        # if exp binary equals to all ones and fraction is not zero
        if expValue == maxValue and not isFractionZero:
            return False, 'NaN'
        
        # if none of them executed, the floating point number given is valid
        return True, ''
    
    # This is the function for taking 2's complement of a binary number
    def takeTwosComplement(self, binaryNumber):
        onesComplement = ''
        twosComplement = ''

        # Taking ones complement
        for ch in binaryNumber:
            if ch == '0':
                onesComplement += '1'
                continue
            onesComplement += '0'

        carry = 0
        
        # Adding 1 to ones complement starting from the least significant bit
        for i in range(len(onesComplement) - 1, -1, -1):
            if i == len(onesComplement) - 1:
                if onesComplement[i] == '1':
                    twosComplement += '0'
                    carry = 1
                    continue
                twosComplement += '1'
                continue
            
            if onesComplement[i] == '1':
                if carry == 1:
                    twosComplement += '0'
                    continue
                else:
                    twosComplement += '1'
                    continue
            
            if onesComplement[i] == '0':
                if carry == 1:
                    twosComplement += '1'
                    carry = 0
                    continue
                else:
                    twosComplement += '0'
                    continue
        
        result = twosComplement[::-1]  # reversing the twosComplement

        return result
    
    # This is the function for rounding floating point numbers to the precision of max 5 digits
    def roundResult(self, decimalValue):
        if "." in decimalValue:
            splittedValues = decimalValue.split('.')
            integerPart = splittedValues[0]
            fraction = splittedValues[1]
            exponent = ''
            # checking if the value contains e or not
            if 'e' in fraction:
                exponentSplitted = fraction.split('e')
                fraction = exponentSplitted[0]
                exponent = exponentSplitted[1]

            # If the length of fraction is greater than 5, else return the value itself
            if len(fraction) > 5:
                roundingCheckValue = fraction[5:]
                # checking the fraction part to get the operation for rounding
                isHalfway, operation = self.checkHalfWay(roundingCheckValue)

                # Case 1: If the fraction is below the halfway
                if not isHalfway:
                    returnText = '{0}.{1}'.format(integerPart, fraction[:5])
                    if exponent != '':
                        returnText += 'e{0}'.format(exponent)
                    
                    # return directly by just taking 5 digits after the integer part
                    return returnText

                # Case 2: If the fraction is above the halfway
                if isHalfway and operation == 'Greater Than':
                    # Starting from least significant bit, round it by adding 1 to each digit if required in each step
                    for i in range(4, -1, -1):
                        roundedValue = int(fraction[i]) + 1
                        if roundedValue != 10:
                            if i == 0:
                                fraction = str(roundedValue) + fraction[(i + 1):]
                            elif i == 4:
                                fraction = fraction[:i] + str(roundedValue)
                            else:
                                fraction = fraction[:i] + str(roundedValue) + fraction[(i + 1):]
                            break
                        else:
                            if i == 0:
                                fraction = '0' + fraction[(i + 1):]
                                integerPart += 1
                                break
                            elif i == 4:
                                fraction = fraction[:i] + '0'
                            else:
                                fraction = fraction[:i] + '0' + fraction[(i + 1):]
                    # revise the return text after rounding
                    returnText = '{0}.{1}'.format(integerPart, fraction[:5])
                    if exponent != '':
                        returnText += 'e{0}'.format(exponent)
                    return returnText
                # Case 3: If the fraction is halfway and it requires rounding because of nearest even
                if isHalfway and operation == 'Halfway' and int(fraction[4]) % 2 != 0:
                    for i in range(4, -1, -1):
                        roundedValue = int(fraction[i]) + 1
                        # Starting from least significant bit, round it by adding 1 to each digit if required in each step
                        if roundedValue != 10:
                            if i == 0:
                                fraction = str(roundedValue) + fraction[(i + 1):]
                            elif i == 4:
                                fraction = fraction[:i] + str(roundedValue)
                            else:
                                fraction = fraction[:i] + str(roundedValue) + fraction[(i + 1):]
                            break
                        else:
                            if i == 0:
                                fraction = '0' + fraction[(i + 1):]
                                if int(integerPart) < 0:
                                    integerPart = '{0}'.format(int(integerPart) - 1)
                                else:
                                    integerPart = '{0}'.format(int(integerPart) + 1)
                                break
                            elif i == 4:
                                fraction = fraction[:i] + '0'
                            else:
                                fraction = fraction[:i] + '0' + fraction[(i + 1):]
                    
                    returnText = '{0}.{1}'.format(integerPart, fraction[:5])
                    if exponent != '':
                        returnText += 'e{0}'.format(exponent)
                    return returnText

                # Case 4: If it is equal to the halfway and does not require rounding
                else:
                    returnText = '{0}.{1}'.format(integerPart, fraction[:5])
                    if exponent != '':
                        returnText += 'e{0}'.format(exponent)
                    return returnText

            # if the fraction length is smaller than 5, return it up to 5 digits without rounding
            return (integerPart + '.' + fraction[:5])
        
        # if there is no fraction in the value, no need for rounding
        return decimalValue
    
    # This is the function checking the fractional part to decide rounding activity
    def checkHalfWay(self, checkValue):
        # Returning values: 
        #   - [0] (bool): is rounding needed
        #   - [1] (str): if rounding needed, operation text
        
        # Case 1 : The value is greater than the halfway
        if int(checkValue[0]) > 5:
            return True, 'Greater Than'
        
        # Case 2 : The value is equal to the halfway
        elif int(checkValue[0]) == 5:
            # Checking till the end to make sure that it is exactly 5
            for i in range(1, len(checkValue)):
                if checkValue[i] != '0':
                    return True, 'Greater Than'
            return True, 'Halfway'

        # Case 3 : The value is below the halfway
        else:
            return False, ''
                 
    # This is base function of the whole program to test the program with other components
    def playground(self):
        number = 0
        while (number != "*"):
            number = input("Enter the number: ")

            if not number:
                print("You should enter an hexadecimal number!")
                continue

            isValidNumber = True
            invalidCharacter = ''
            number = number.upper()

            # Check if hex number is valid
            for ch in number:
                if ch not in self.hexadecimalElements:
                    isValidNumber = False
                    invalidCharacter = ch
                    break
            
            if not isValidNumber:
                print("Please enter an hexadecimal number! Invalid characters found: " + str(invalidCharacter))
                continue

            if (len(number) > 8):
                print("Please enter an hexadecimal in base of 1, 2, 3 or 4 bytes!")
                continue
            
            isValidDataType = True

            dataType = input("Data type: ").upper()
            
            # check if the given data type is valid
            for dt in dataType:
                if dt not in self.dataTypes:
                    isValidDataType = False
                    break
            
            if not isValidDataType:
                print("Please enter a valid data type! Our converter supports the following data types: \n1 - Signed Integer (S) \n2 - Unsigned Integer (U) \n3 - Floating Point (F)")
                continue

            result = self.run(number, dataType)  # Get result with given inputs
            print("Result: {0} ".format(result))
    
    # This is the main function for the program to execute all the steps with given number and data type
    def run(self, number, dataType):
        # adding 0 in case the length of hex number is odd
        if (len(number) % 2 != 0): 
            number = "0" + number
        
        # hex to binary conversion
        binary = self.convertToBinary(number)
        signBit = binary[0]

        # Case 1 : Unsigned integer conversion
        if dataType == "U":
            value = self.binaryToDecimal(binary)
            # print("Result: {0} ".format(value))
            return str(value)

        # Case 2 : Signed integer conversion
        elif dataType == "S":
            value = 0
            if signBit == '1':
                twosComplement = self.takeTwosComplement(binary)
                value = self.binaryToDecimal(twosComplement)
                value = -(value)
            else:
                value = self.binaryToDecimal(binary)
                
            # print("Result: {0} ".format(value))
            return str(value)

        # Case 3 : Floating point number conversion
        else:
            isValidFloatingNumber, message = self.isValidFloatingNumber(binary)

            # Checking if the given floating point number is valid
            if isValidFloatingNumber:
                value = 0
                byte = len(number) / 2
                exp_bits = self.getExponentBit(byte)
                exp = self.getExponentValue(binary,exp_bits)
                exponentValue = self.binaryToDecimal(exp)
                fraction = self.getFractionValue(binary)
                bias = self.getBias(exp_bits)
                
                if exponentValue == 0:
                    fractionValue = self.getFractionToDecimal(fraction)
                    power = 1 - bias
                else:
                    fractionValue = self.getFractionToDecimal(fraction) + 1
                    power = exponentValue - bias
                # applying the formula
                value = fractionValue * (2 ** power)
                
                # Checking if the number is negative by using sign bit
                if signBit == '1':
                    value = -(value)

                # rounding before returning the value if required
                return str(self.roundResult(str(value)))
            else:
                return message

myTest = BinaryConverter()  # Creation of the class instance
myTest.playground()  # Running the program