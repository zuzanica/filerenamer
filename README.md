Príklad obsluhy (použité na macOs, na windowse nutno použiť správne cesty k priečinkom):

1. premenovanie všetkých súborov v priečinku: /Users/zuzanastudena/private/filerenamer/data 
    a ich kopírovanie do priečinku: /Users/zuzanastudena/private/filerenamer/newtest.
   - python3, možno použiť aj python záleží od naištalovanej verzie
   - main.py názov hlavného programu (musí existovať v priečinku, v ktorom to spúštaš) prípadne použi celú cestu
   - -i ako input - vstupný priečinok
   - -d ako destination - vystupný priečinok
   - -c ako copy chceš kopírovať dáta

```
python3 main.py -i /Users/zuzanastudena/private/filerenamer/data -d /Users/zuzanastudena/private/filerenamer/newtest -c
```

2. premenovanie všetkých súborov v priečinku: /Users/zuzanastudena/private/filerenamer/data-test
    - python3, možno použiť aj python záleží od naištalovanej verzie
    - main.py názov hlavného programu (musí existovať v priečinku, v ktorom to spúštaš) prípadne použi celú cestu
    - -i ako input - vstupný priečinok
    - -r ako rename chceš iba premenovať existujúce súbory
    - -d v tomto prípade nepotrebuješ
```
python3 main.py -i /Users/zuzanastudena/private/filerenamer/data-test -r
```
