"""Hack assembler (Nand to Tetris). K = 85 -> K mod 3 = 1:
extra feature = clear error messages with line numbers instead of crashing.
Usage: python assembler.py Prog.asm   (writes Prog.hack)
"""
import sys

COMP = {
    '0': '0101010', '1': '0111111', '-1': '0111010', 'D': '0001100',
    'A': '0110000', '!D': '0001101', '!A': '0110001', '-D': '0001111',
    '-A': '0110011', 'D+1': '0011111', 'A+1': '0110111', 'D-1': '0001110',
    'A-1': '0110010', 'D+A': '0000010', 'D-A': '0010011', 'A-D': '0000111',
    'D&A': '0000000', 'D|A': '0010101',
    'M': '1110000', '!M': '1110001', '-M': '1110011', 'M+1': '1110111',
    'M-1': '1110010', 'D+M': '1000010', 'D-M': '1010011', 'M-D': '1000111',
    'D&M': '1000000', 'D|M': '1010101',
}
DEST = {'': '000', 'M': '001', 'D': '010', 'MD': '011', 'A': '100',
        'AM': '101', 'AD': '110', 'AMD': '111'}
JUMP = {'': '000', 'JGT': '001', 'JEQ': '010', 'JGE': '011',
        'JLT': '100', 'JNE': '101', 'JLE': '110', 'JMP': '111'}


def predefined():
    t = {'SP': 0, 'LCL': 1, 'ARG': 2, 'THIS': 3, 'THAT': 4,
         'SCREEN': 16384, 'KBD': 24576}
    for i in range(16):
        t['R%d' % i] = i
    return t


def valid_symbol(s):
    return (s != '' and not s[0].isdigit()
            and all(c.isalnum() or c in '_.$:' for c in s))


def clean(line):
    return line.split('//')[0].replace(' ', '').replace('\t', '').strip()


def assemble(lines):
    errors = []
    symbols = predefined()
    code = []            # (line_number, instruction)

    # ---- First pass: remove comments/blanks, record labels ----
    for n, raw in enumerate(lines, 1):
        line = clean(raw)
        if not line:
            continue
        if line.startswith('('):
            if not line.endswith(')') or not valid_symbol(line[1:-1]):
                errors.append('Line %d: invalid label "%s"' % (n, line))
            else:
                name = line[1:-1]
                if name in symbols:
                    errors.append('Line %d: label "%s" already defined' % (n, name))
                else:
                    symbols[name] = len(code)
            continue
        code.append((n, line))

    # ---- Second pass: translate to 16 bits ----
    next_var = 16
    out = []
    for n, line in code:
        if line.startswith('@'):
            sym = line[1:]
            if sym.isdigit():
                val = int(sym)
                if val > 32767:
                    errors.append('Line %d: address %d too large (max 32767)' % (n, val))
                    continue
            elif valid_symbol(sym):
                if sym not in symbols:
                    symbols[sym] = next_var
                    next_var += 1
                val = symbols[sym]
            else:
                errors.append('Line %d: invalid A-instruction "%s"' % (n, line))
                continue
            out.append(format(val, '016b'))
        else:
            dest, comp, jump = '', line, ''
            if '=' in comp:
                dest, comp = comp.split('=', 1)
            if ';' in comp:
                comp, jump = comp.split(';', 1)
            if dest not in DEST:
                errors.append('Line %d: invalid destination "%s"' % (n, dest))
            elif comp not in COMP:
                errors.append('Line %d: invalid instruction "%s"' % (n, line))
            elif jump not in JUMP:
                errors.append('Line %d: invalid jump "%s"' % (n, jump))
            else:
                out.append('111' + COMP[comp] + DEST[dest] + JUMP[jump])
    return out, errors


def main():
    if len(sys.argv) != 2 or not sys.argv[1].endswith('.asm'):
        print('Usage: python assembler.py Prog.asm')
        sys.exit(1)
    try:
        with open(sys.argv[1]) as f:
            lines = f.read().splitlines()
    except OSError as e:
        print('Cannot open file:', e)
        sys.exit(1)
    out, errors = assemble(lines)
    if errors:
        for e in errors:
            print(e)
        print('%d error(s). No .hack file written.' % len(errors))
        sys.exit(1)
    path = sys.argv[1][:-4] + '.hack'
    with open(path, 'w') as f:
        f.write('\n'.join(out) + '\n')
    print('Wrote %s (%d instructions)' % (path, len(out)))


if __name__ == '__main__':
    main()