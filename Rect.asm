@0
D=A
@pos
M=D

@R0
D=M
@n
M=D

(LOOP)
@n
D=M
@END
D;JLE

@pos
D=M
@SCREEN
A=D+A
M=-1

@32
D=A
@pos
M=D+M

@n
MD=M-1
@LOOP
D;JGT

(END)
@END
0;JMP