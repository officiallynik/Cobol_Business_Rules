000100 IDENTIFICATION DIVISION.
000200 PROGRAM-ID. ATM.
000300 AUTHOR.
000400 SOURCE.
000500 ENVIRONMENT DIVISION.
000600 CONFIGURATION SECTION.
000700 SOURCE-COMPUTER. PC-MICROFOCUS.
000800 OBJECT-COMPUTER. PC-MICROFOCUS.
000900 DATA DIVISION.
001000 WORKING-STORAGE SECTION.
001000 77  BALANCE            pic x(9).
001000 77  NEW-BALANCE        pic x(9).
001000 77  WITHDRAW-AMT       pic x(5).
001000 77  WITHDRAW-LIMIT     pic x(5).
002800 77  ALLOW         PICTURE 9.
002900 PROCEDURE DIVISION.
003000 INIT.
003200    IF BALANCE > 0
004301      DISPLAY "ENTER WITHDRAW AMOUNT"
004400    	GO TO WITHDRAW.	      
004300    ELSE
008606      DISPLAY "YOU HAVE NO BALANCE"
008500      GO TO ENDATM
001200    END-IF.
004402 INIT-FN.
004403 EXIT.
004500 WITHDRAW.
004501 PERFORM CheckWithdrawAMT THROUGH CheckWithdrawAMT-FN.
000000 IF ALLOW = 1
004501      PERFORM CalculateBalance THROUGH CalculateBalance-FN.
000000      IF NEW-BALANCE >= 0
000000          MOVE NEW-BALANCE TO BALANCE
000000          GO TO PRINT
000000      ELSE
008606          DISPLAY "YOU DO NOT HAVE ENOUGH BALANCE: " NEW-BALANCE
000000      END-IF.
000000 ELSE
000000      GO TO ERRORLIMIT
000000 END-IF.
008300 PRINT.
008402 DISPLAY "WITHDRAW AMOUNT:" WITHDRAW-AMT.
008402 DISPLAY "NEW BALANCE:" BALANCE.
008500 GO TO ENDATM		
008601 CheckWithdrawAMT.
008600 IF WITHDRAW-AMT > 0 AND WITHDRAW-AMT <= WITHDRAW-LIMIT
008602   COMPUTE ALLOW = 1.
000000 ELSE
000000   COMPUTE ALLOW = 0.
000000 END-IF 
008603 CheckWithdrawAMT-FN.
008601 CalculateBalance.
000000      COMPUTE NEW-BALANCE = BALANCE - WITHDRAW-AMT.
008603 CalculateBalance-FN.
000000 EXIT. 
008605 ERRORLIMIT.
008606      DISPLAY "PLEASE WITHDRAW AMOUNT LESS THAN THE LIMIT: " WITHDRAW-LIMIT.
008616 ERRORLIMIT-FN. 
008617 EXIT.
000000 ENDATM.
008500 FIN.
008600    STOP RUN.