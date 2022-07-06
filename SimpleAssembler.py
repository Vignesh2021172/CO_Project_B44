#*************taking assembly code input through console***************************# 
import sys                                    
program = sys.stdin.read().splitlines()

#**********************lists created for each Type*********************************#
A=["add","sub","mul","xor","or","and"]
B=["movB","rs","ls"]
C=["movC","div","not","cmp"]
D=["ld","st"]
E=["jmp","jlt","jgt","je"]
F=["hlt"] 

#***************dictionary is created to map registers with their code***************#
RegandAddress = {"R0":"000","R1":"001","R2":"010","R3":"011",
              "R4":"100","R5":"101","R6":"110","FLAGS":"111"}

#********dictionary is created to map instructions with their opcode********#
operations = {"add":["10000"],"sub":["10001"],"movB":["10010"],"movC":["10011"],
              "ld":["10100"],"st":["10101"],"mul":["10110"],"div":["10111"],
              "rs":["11000"],"ls":["11001"],"xor":["11010"],"or":["11011"],
              "and":["11100"],"not":["11101"],"cmp":["11110"],"jmp":["11111"],
              "jlt":["01100"],"jgt":["01101"],"je":["01111"],"hlt":["01010"]}

#*******************list is created for all the operands available*******************#
operands = ["add","sub","mov","ld","st","mul","div","rs","ls",
            "xor","or","and","not","cmp","jmp","jlt","jgt","je","hlt"]

#*******************list is created for all the registers available******************#
registers = [ "R0", "R1" , "R2" , "R3" , "R4" , "R5" , "R6"]

#************************list for registers imcluding "FLAGS"***********************#
flags=RegandAddress.keys()

#***********************************list with "hlt"*********************************#
labels=["hlt"]
variables=[]
error=False

#********************function is created to handle all the error cases of the type A************************#
def errorA(content):
    global error
    if(len(content)==4):
        pass
    else:
        print("wrong syntax is used for",content[0],"instruction at line number",line_number)
        error=True
        return
    a=1
    while(a!=len(content)):
        if(content[a] not in registers):
            print(content[a],"is a invalid register name at line number",line_number)
            error=True
        elif(content[a]=="FLAGS"):
            print("invalid usage of flags at line number",line_number)
            error=True
        a+=1

#********************function is created to handle all the error cases of the type B************************#
def errorB(content):
    global error
    if(len(content)==3):
        pass
    else:
        print("wrong syntax is used for",content[0],"instruction at line number",line_number)
        error=True
        return   
    value=content[2]
    if(value[0]=="$"):
        checking_immediate(value)
    else:
        print("usage of",value[0],"is invalid at line number",line_number)
        error=True
    if(content[1] not in registers):
        print(content[1],"is an invalid register name at line number",line_number)
        error=True
    elif(content[1]=="FLAGS"):
        print("invalid usage of flags at line number",line_number)
        error=True
    else:
        pass

#*********************function created to check error in immediate values**********************#
def checking_immediate(a):    
    global error
    try:
        num = int(a[1:])
        if(num>=0 and num<=255):
            pass
        else:
            print(num,"is not in range [0,255] at line number",line_number)
            error=True
    except:
        print("invalid immediate value at line number",line_number)
        error=True

#********************function is created to handle all the error cases of the type C************************#
def errorC(content):
    global error
    if(len(content)==3):
        pass
    else:
        print("wrong syntax is used for",content[0],"instruction at line number",line_number)
        error=True
        return
    if(content[1] not in registers):
        print(content[1],"is a invalid register name at line number",line_number)
        error=True
    elif(content[1]=="FLAGS"):
        print("invalid usage of flags at line number",line_number)
        error=True
    else:
        pass
    if(content[0]!="mov2"):
        if(content[2] in registers):
            pass
        else:
            print("invalid register name at line number",line_number)
            error=True
    else:
        if(content[2] in flags):
            pass
        else:
            print("invalid register or flag name at line number",line_number)
            error=True 

#********************function is created to handle all the error cases of the type D************************#
def errorD(content):
    global error
    if(len(content)==3):
        pass
    else:
        print("wrong syntax is used for",content[0],"instruction at line number",line_number)
        error=True
        return
    if(content[2] not in variables):
        print(content[2],"is undefined variable at line number",line_number)
        error=True
    elif(content[2] in labels):
        print("labels cannot be used inplace of variables at line number",line_number)
        error=True

#********************function is created to handle all the error cases of the type E************************#
def errorE(content):
    global error
    if(len(content)==2):
        pass
    else:
        print("wrong syntax is used for",content[0],"instruction at line number",line_number)
        error=True
        return
    if(content[1] not in labels):
        print(content[1],"is undefined labelat line number",line_number)
        error=True
    elif(content[1] in variables):
        print("variables cannot be used inplace of labels at line number",line_number)
        error=True

#********************function is created to handle all the error cases of the type F************************#
def errorF(content):
    if(line_number!=len(program)):
        print("hlt must be at the end at line number",line_number)
        error=True
        exit()
    elif(len(content)==1):
        pass
    elif(len(content)!=1):
        print("wrong syntax is used for",content[0],"instruction at line number",line_number)
        error=True
    
#***********************************function is created to handle Halt****************************************#
def handling_hlt(content):
    global error
    if ((len(content) == 2) and content[1] != "hlt" or len(content) != 2 and content[0] != "hlt"):
        print("no hlt instruction at the end of line number",line_number+1)
        error=True

#********************************function is created to handle cases of Variables***************************#
def handling_variables(content): 
    global error
    global flag
    if (content[0]=="var"):
        if (len(content)==2):
            pass
        else:
            print("invalid syntax at line number",line_number)
            error=True
            return
    else:
        flag=1
    if (content[0]=="var" and flag==1):
            print("variable is not decalared at line number",line_number)
            error=True
    if(content[0]=="var" and content[1] not in variables):
            variables.append(content[1])  
    elif(content[0]=="var" and content[1] in variables):
            print("mulitiple declaration of variable",content[1],"at line number",line_number)
            error = True

#**************************code for handling all the cases of Variables***************************#
line_number =0 
flag=0
while(line_number<len(program)):
    each_line=program[line_number]                                               
    line_number=line_number+1
    if(len(each_line)==0):
        continue
    content=list(each_line.split())
    handling_variables(content)

#*************************function is created to handle cases of Labels*************************************#
def handling_labels(content):   
    global error
    if (content[0][-1]==":"):
        if(content[0][:-1] not in labels):
            labels.append(content[0][:-1])
        elif(content[0][:-1] in labels):
            print("multiple definations of label",content[0],"at line number",line_number)
            error=True

#***************************code for handling all the cases of Labels*******************************#
line_number=0                                                         
while(line_number<len(program)):
    each_line=program[line_number]              
    line_number=line_number+1
    if(len(each_line)==0):
        continue
    content=list(each_line.split())
    handling_labels(content)

#*************************code for handling all the cases of Normal Instructions*******************#
line_number=0                                                      
while(line_number<len(program)):
    each_line=program[line_number]
    line_number=line_number+1
    if(len(each_line)==0):
        continue
    content=list(each_line.split())
    if line_number==len(program):  
        handling_hlt(content)
    if(content[0]=="var"):
        continue
    if(content[0][0:-1] not in labels):
        pass
    else:
        content.pop(0)
    if(len(content)!=0):
        pass
    else:
        print("invalid defnation of labels at line number",line_number)
        error=True
        continue
    if(content[0] in operands):
        pass
    else:
        print(content[0],"is an invalid instruction name at line number",line_number)
        error=True
        continue
    if(content[0]=="mov" and len(content)>=2):
        c=content[2][0]
        if(65<=ord(c)<=90 or 97<=ord(c)<=122):
            content[0]="movC"
        else:
            content[0]="movB"
    if (content[0] in A):
        errorA(content)
    elif (content[0] in B):
        errorB(content)
    elif (content[0] in C):
        errorC(content)
    elif (content[0] in D):
        errorD(content)
    elif (content[0] in E):
        errorE(content)
    elif (content[0] in F):
        errorF(content)
    else:
        print("invalid syntax at line number",line_number)
        error=True

#**********************************code for printing the Binary code part**********************************#

#********************this code will run only when there are no errors in the assembly code*****************#
address=-1
labels={}
integer=1
variables={}

#********************if there is an error then exit**********************#
if(error==True):
    exit()

#**********loop created to store the address of all the Labels in the dictionary************#
i=0
while(i<len(program)):
    each_line=program[i]
    i=i+1
    if len(each_line)==0:
        continue
    content=list(each_line.split())
    if(content[0] not in operands):
        pass
    else:
        address=address+1
    if content[0]!="hlt":
        pass
    else:
        labels[content[0]+":"]=address
    if(content[0][-1]!=":"):
        pass
    else:
        address=address+1
        labels[content[0]]=address
        
#************loop is created to store the address of all the Variables in the dictionary***********#
i=0
while(i<len(program)):
    each_line=program[i]
    i=i+1
    if(len(each_line)==0):
        continue
    content=list(each_line.split())
    if (content[0]=="var"):
        if(len(content)!=2):
            pass
        else:
            variables[content[1]]=integer+address
            integer=integer+1
    
#***********************loop is created to convert Assembly code to Binary code*********************#
i=0
while(i<len(program)):
    each_line=program[i]
    i=i+1
    if(len(each_line)==0):
        continue
    content=list(each_line.split())
    if( len(content)>1 and content[0] in labels and content[1] in operands):
        content.pop(0)
    if (content[0] in operands):
        if(content[0]=="mov" ):
            if(content[2][0]!="$"):
                content[0]="movC"
            elif(content[2][0]=="$"):
                content[0]="movB"
        if (content[0] in A):
            answer=operations[content[0]][0]+"00"+RegandAddress[content[1]]+RegandAddress[content[2]]+RegandAddress[content[3]]
        elif (content[0] in B):
            b=bin(int(content[2][1:]))[2:]
            answer=operations[content[0]][0]+RegandAddress[content[1]]+(8-len(b))*"0"+b 
        elif (content[0] in C):
            answer=operations[content[0]][0]+"00000"+RegandAddress[content[1]]+RegandAddress[content[2]]
        elif (content[0] in D):
            d=bin(variables[content[2]])[2:]
            answer=operations[content[0]][0]+RegandAddress[content[1]]+(8 - len(d))*"0"+d
        elif (content[0] in E):
            e=bin(labels[content[1]+":"])[2:]
            answer=operations[content[0]][0]+"000"+(8 - len(e))*"0"+e
        elif (content[0] in F):
            answer=operations[content[0]][0]+"00000000000"
        print(answer)

#******************************************-THE END-***************************************#

    












































