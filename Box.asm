// Box.asm  --  K = 85
// Black box while any key is pressed, white (erased) when released.
// Start row 85, 20 rows tall, 32 pixels (2 words) wide, left edge.
// First address = SCREEN + 32*85 = 16384 + 2720 = 19104

(LOOP)
    @KBD
    D=M
    @BLACK
    D;JNE           // key pressed -> black
    @color
    M=0             // no key -> white
    @DRAW
    0;JMP
(BLACK)
    @color
    M=-1            // -1 = 1111111111111111 (all pixels on)

(DRAW)
    @19104
    D=A
    @addr
    M=D             // addr = first word of row 85
    @20
    D=A
    @n
    M=D             // n = 20 rows left

(ROW)
    @color
    D=M
    @addr
    A=M
    M=D             // left word
    A=A+1
    M=D             // right word
    @addr
    D=M
    @32
    D=D+A
    @addr
    M=D             // addr += 32 (next row)
    @n
    MD=M-1
    @ROW
    D;JGT           // more rows?
    @LOOP
    0;JMP