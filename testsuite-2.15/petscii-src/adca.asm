         *= $0801         .BYTE $4C,$16,$08,$00,$97,$32         .BYTE $2C,$30,$3A,$9E,$32,$30         .BYTE $37,$30,$00,$00,$00,$A9         .BYTE $01,$85,$02         JSR PRINT         .BYTE 13         .TEXT "�ADCA"         .BYTE 0         LDA #%00011011         STA DB         LDA #%11000110         STA AB         LDA #%10110001         STA XB         LDA #%01101100         STA YB         LDA #0         STA PB         TSX         STX SB         LDA #0         STA DB         STA ABNEXT     LDA PB         AND #%00001000         BNE DECMODE         LDA DB         STA DA         STA DR         STA CMD0+1         AND #$7F         STA CMD1+1         CLC         LDA PB         AND #1         BEQ NOC         SECNOC      PHP         LDA ABCMD0     ADC #0         STA AR         LDA PB         ORA #%00110000         AND #%00111100         BCC NOC1         ORA #1NOC1     TAX         LDA AB         AND #$7F         PLPCMD1     ADC #0         BMI NEG         TXA         AND #1         BEQ CONTSET      TXA         ORA #%01000000         TAX         JMP CONTNEG      TXA         AND #1         BEQ SETCONT     LDA AR         CMP #0         BNE NOZERO         TXA         ORA #%00000010         TAXNOZERO   LDA AR         BPL NONEG         TXA         ORA #%10000000         TAXNONEG    STX PR         JMP DECCONTDECMODE         .BLOCK         LDA DB         STA DA         STA DR         AND #$0F         STA L0+1         LDA PB         ORA #%00110000         AND #%00111100         TAX         LDA PB         LSR A         LDA AB         AND #$0FL0       ADC #0         LDY #$00         CMP #$0A         BCC L1         SEC         SBC #$0A         AND #$0F         LDY #$08L1       STA AR         STY L2+1         STY L3+1         LDA DB         AND #$F0         ORA L3+1         STA L3+1         LDA AB         AND #$F0L2       ORA #0         CLCL3       ADC #0         PHP         BCS L4         CMP #$A0         BCC L5L4       SEC         SBC #$A0         INXL5       ORA AR         STA AR         PLP         BVC NOV         PHP         TXA         ORA #%01000000         TAX         PLPNOV      BPL NON         TXA         ORA #%10000000         TAXNON      LDA PB         LSR A         LDA AB         ADC DB         BNE NOZ         TXA         ORA #%00000010         TAXNOZ      STX PR         .BENDDECCONT  LDA XB         STA XR         LDA YB         STA YR         LDA SB         STA SR         LDX SB         TXS         LDA PB         PHA         LDA AB         LDX XB         LDY YB         PLPCMD      ADC DA         PHP         CLD         STA AA         STX XA         STY YA         PLA         STA PA         TSX         STX SA         JSR CHECK         CLC         LDA DB         ADC #17         STA DB         BCC JMPNEXT         LDA #0         STA DB         CLC         LDA AB         ADC #17         STA AB         BCC JMPNEXT         LDA #0         STA AB         INC PB         BEQ NONEXTJMPNEXT  JMP NEXTNONEXT         JSR PRINT         .TEXT " - OK"         .BYTE 13,0         LDA 2         BEQ LOADWAIT     JSR $FFE4         BEQ WAIT         JMP $8000LOAD     JSR PRINTNAME     .TEXT "ADCAX"NAMELEN  = *-NAME         .BYTE 0         LDA #0         STA $0A         STA $B9         LDA #NAMELEN         STA $B7         LDA #<NAME         STA $BB         LDA #>NAME         STA $BC         PLA         PLA         JMP $E16FDB       .BYTE 0AB       .BYTE 0XB       .BYTE 0YB       .BYTE 0PB       .BYTE 0SB       .BYTE 0DA       .BYTE 0AA       .BYTE 0XA       .BYTE 0YA       .BYTE 0PA       .BYTE 0SA       .BYTE 0DR       .BYTE 0AR       .BYTE 0XR       .BYTE 0YR       .BYTE 0PR       .BYTE 0SR       .BYTE 0CHECK         .BLOCK         LDA DA         CMP DR         BNE ERROR         LDA AA         CMP AR         BNE ERROR         LDA XA         CMP XR         BNE ERROR         LDA YA         CMP YR         BNE ERROR         LDA PA         CMP PR         BNE ERROR         LDA SA         CMP SR         BNE ERROR         RTSERROR    JSR PRINT         .BYTE 13         .NULL "BEFORE  "         LDX #<DB         LDY #>DB         JSR SHOWREGS         JSR PRINT         .BYTE 13         .NULL "AFTER   "         LDX #<DA         LDY #>DA         JSR SHOWREGS         JSR PRINT         .BYTE 13         .NULL "RIGHT   "         LDX #<DR         LDY #>DR         JSR SHOWREGS         LDA #13         JSR $FFD2WAIT     JSR $FFE4         BEQ WAIT         CMP #3         BEQ STOP         RTSSTOP     LDA 2         BEQ BASIC         JMP $8000BASIC    JMP ($A002)SHOWREGS STX 172         STY 173         LDY #0         LDA (172),Y         JSR HEXB         LDA #32         JSR $FFD2         LDA #32         JSR $FFD2         INY         LDA (172),Y         JSR HEXB         LDA #32         JSR $FFD2         INY         LDA (172),Y         JSR HEXB         LDA #32         JSR $FFD2         INY         LDA (172),Y         JSR HEXB         LDA #32         JSR $FFD2         INY         LDA (172),Y         LDX #"N"         ASL A         BCC OK7         LDX #"�"OK7      PHA         TXA         JSR $FFD2         PLA         LDX #"V"         ASL A         BCC OK6         LDX #"�"OK6      PHA         TXA         JSR $FFD2         PLA         LDX #"0"         ASL A         BCC OK5         LDX #"1"OK5      PHA         TXA         JSR $FFD2         PLA         LDX #"B"         ASL A         BCC OK4         LDX #"�"OK4      PHA         TXA         JSR $FFD2         PLA         LDX #"D"         ASL A         BCC OK3         LDX #"�"OK3      PHA         TXA         JSR $FFD2         PLA         LDX #"I"         ASL A         BCC OK2         LDX #"�"OK2      PHA         TXA         JSR $FFD2         PLA         LDX #"Z"         ASL A         BCC OK1         LDX #"�"OK1      PHA         TXA         JSR $FFD2         PLA         LDX #"C"         ASL A         BCC OK0         LDX #"�"OK0      PHA         TXA         JSR $FFD2         PLA         LDA #32         JSR $FFD2         INY         LDA (172),Y         .BENDHEXB     PHA         LSR A         LSR A         LSR A         LSR A         JSR HEXN         PLA         AND #$0FHEXN     ORA #$30         CMP #$3A         BCC HEXN0         ADC #6HEXN0    JMP $FFD2PRINT    PLA         .BLOCK         STA PRINT0+1         PLA         STA PRINT0+2         LDX #1PRINT0   LDA !*,X         BEQ PRINT1         JSR $FFD2         INX         BNE PRINT0PRINT1   SEC         TXA         ADC PRINT0+1         STA PRINT2+1         LDA #0         ADC PRINT0+2         STA PRINT2+2PRINT2   JMP !*         .BEND