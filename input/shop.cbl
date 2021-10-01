000100 IDENTIFICATION DIVISION.
000200 PROGRAM-ID. SHOP.
000300 AUTHOR.
000400 SOURCE.
000500 ENVIRONMENT DIVISION.
000600 CONFIGURATION SECTION.
000700 SOURCE-COMPUTER. PC-MICROFOCUS.
000800 OBJECT-COMPUTER. PC-MICROFOCUS.
000900 DATA DIVISION.
001000 WORKING-STORAGE SECTION.
001100 01 SHOP.
001200     10 OP          PICTURE 9.
001300     10 QT-VEG      PICTURE 99.
001400     10 QT-MEAT     PICTURE 99.
001500     10 QT-BREAD    PICTURE 99.
001600     10 QT-MILK     PICTURE 99.
001700     10 QT-FRUIT    PICTURE 99.
001800     10 PR-VEG      PICTURE 9.
001900     10 PR-MEAT     PICTURE 9.
002000     10 PR-BREAD    PICTURE 9.
002100     10 PR-MILK     PICTURE 9.
002200     10 PR-FRUIT    PICTURE 9.
002300 77  MONEY        PICTURE 99, VALUE 50.
002400 77  REST         PICTURE 99.
002500 77  BAG          PICTURE 9.
002600 77  MAX-CAP      PICTURE 9, VALUE 10.
002700 77  RAND         PICTURE 9.
002800 77  NEED         PICTURE 9.	
002900 PROCEDURE DIVISION.
003000 INIT.
003200    IF OP = 1
003201      DISPLAY "SHOP IS OPEN"
003202      PERFORM INIT-PRD THROUGH INIT-PRD-FN
003203      GO TO INIT-FN
004300    ELSE
004301      DISPLAY "SHOP IS CLOSED"
004400    	GO TO INIT.
001200    END-IF.
004402 INIT-FN.
004403 EXIT.
004500 BUY-VEG.
004501 PERFORM ISNEEDED THROUGH ISNEEDED-FN.
004700 IF NEED = 1 AND QT-VEG > 0
004800    IF MONEY > PR-VEG AND BAG < MAX-CAP
004900 	ADD 1 TO BAG
005000 	COMPUTE MONEY = MONEY - PR-VEG
005100 	SUBTRACT 1 FROM QT-VEG
005101    ELSE
005102       GO TO PRINT
001000    END-IF.
005103 ELSE
005104     GO TO BUY-MEAT.
012001 END-IF.
005105 BUY-VEG-FN. 
005106 EXIT.
005200 BUY-MEAT.
005201 PERFORM ISNEEDED THROUGH ISNEEDED-FN.    		
005400 IF NEED = 1 AND QT-MEAT > 0
005500    IF MONEY > PR-MEAT AND BAG < MAX-CAP
005600 	ADD 1 TO BAG
005700 	COMPUTE MONEY = MONEY - PR-MEAT
005800 	SUBTRACT 1 FROM QT-MEAT
005801    ELSE
005802      GO TO PRINT
212121    END-IF.
005803 ELSE
005804     GO TO BUY-BREAD.
012001 END-IF.
005805 BUY-MEAT-FN. 
005806 EXIT.
005900 BUY-BREAD.
005901 PERFORM ISNEEDED THROUGH ISNEEDED-FN.    		
006100 IF NEED = 1 AND QT-BREAD > 0
006200    IF MONEY > PR-BREAD AND BAG < MAX-CAP
006300 	ADD 1 TO BAG
006400 	COMPUTE MONEY = MONEY - PR-BREAD
006500 	SUBTRACT 1 FROM QT-BREAD
006501    ELSE
006502      GO TO PRINT
900900    END-IF.
006503 ELSE
006504     GO TO BUY-MILK.
012001 END-IF.
006505 BUY-BREAD-FN. 
006506 EXIT.    		
006600 BUY-MILK.
006601 PERFORM ISNEEDED THRU ISNEEDED-FN.    		
006800 IF NEED = 1 AND QT-MILK > 0
006900    IF MONEY > PR-MILK AND BAG < MAX-CAP
007000 	ADD 1 TO BAG
007100 	COMPUTE MONEY = MONEY - PR-MILK
007200 	SUBTRACT 1 FROM QT-MILK
007201     ELSE
007202      GO TO PRINT
211212    END-IF.
007203 ELSE
007204     GO TO BUY-FRUIT.
012001 END-IF.
007205 BUY-MILK-FN. 
007206 EXIT.
007300 BUY-FRUIT.
007301 PERFORM ISNEEDED THRU ISNEEDED-FN.    		
007500 IF NEED = 1 AND QT-FRUIT > 0
007600    IF MONEY > PR-FRUIT AND BAG < MAX-CAP
007700 	ADD 1 TO BAG
007800 	COMPUTE MONEY = MONEY - PR-FRUIT
007900 	SUBTRACT 1 FROM QT-FRUIT
007901     ELSE
007902      GO TO PRINT
121212    END-IF.
007903 ELSE
007904     GO TO CHECK.
012001 END-IF.
007905 BUY-FRUIT-FN. 
007906 EXIT.
008000 CHECK.
008100 IF MONEY <= 0 OR BAG >= MAX-CAP
008200 	GO TO PRINT
008201 ELSE
008202     GO TO BUY-VEG.
012001 END-IF.
008203 CHECK-FN. 
008204 EXIT.
008300 PRINT.
008400 MOVE MONEY TO REST.
008401 DISPLAY "REST:" MONEY.
008402 DISPLAY "NB OF PRODUCTS:" BAG.			
008500 FIN.
008600    STOP RUN.
008601 ISNEEDED.
008602   COMPUTE NEED = FUNCTION RANDOM (1) * 2.
008603 ISNEEDED-FN.
008604 EXIT.
008605 INIT-PRD.
008606    COMPUTE QT-VEG = FUNCTION RANDOM (1) * 10
008607    COMPUTE QT-MEAT = FUNCTION RANDOM (1) * 10
008608    COMPUTE QT-BREAD = FUNCTION RANDOM (1) * 10
008609    COMPUTE QT-MILK = FUNCTION RANDOM (1) * 10
008610    COMPUTE QT-FRUIT = FUNCTION RANDOM (1) * 10
008611    COMPUTE PR-VEG = FUNCTION RANDOM (1) * 10 + 3
008612    COMPUTE PR-MEAT = FUNCTION RANDOM (1) * 10 + 5
008613    COMPUTE PR-BREAD = FUNCTION RANDOM (1) * 10 + 1
008614    COMPUTE PR-MILK = FUNCTION RANDOM (1) * 10 + 2
008615    COMPUTE PR-FRUIT = FUNCTION RANDOM (1) * 10 + 1.
008616 INIT-PRD-FN. 
008617 EXIT.