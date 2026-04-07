# MI Evolutionary Algorithms - N királynő probléma

## A feladat leírása

A N királynő probléma célja, hogy egy N×N-as sakktáblán úgy helyezzünk el N darab királynőt, hogy azok ne üssék egymást.

Elérhető lépések:

- vízszintesen,
- függőlegesen,
- átlósan.

Ezért egy helyes megoldásban:

- nincs két királynő ugyanabban a sorban,
- nincs két királynő ugyanabban az oszlopban,
- nincs két királynő ugyanazon az átlón.

## Megoldás pszeudokódja

```
NKiralynoProblema()

    Inicializálj egy P populációt véletlen permutációkkal
    Számítsd ki minden egyed fitness értékét

    ciklus amíg nem teljesül a leállási feltétel:
        ÚjPopuláció = legjobb egyedek (elitizmus)

        amíg ÚjPopuláció mérete kisebb, mint a kívánt populációméret:
            szülő1 = tournament_szelekció(P)
            szülő2 = tournament_szelekció(P)

            valószínűséggel pc:
                gyermek1, gyermek2 = keresztezés(szülő1, szülő2)
            különben:
                gyermek1 = szülő1 másolata
                gyermek2 = szülő2 másolata

            valószínűséggel pm:
                mutáció(gyermek1)

            valószínűséggel pm:
                mutáció(gyermek2)

            add hozzá gyermek1-et és gyermek2-t ÚjPopulációhoz

        P = ÚjPopuláció
        Számítsd ki az új populáció fitness értékeit

        ha van olyan egyed, amelynek fitness értéke N * (N - 1) / 2:
            állj le

    add vissza a legjobb megoldást
```

## Eredmények összehasonlítása különböző N értékekkel

| N  | Sikeres futás | Átlagos generációszám |
|----|---------------|-----------------------|
| 8  | 30/30         | 2.533                 |
| 10 | 29/30         | 30.793                |
| 12 | 24/30         | 30.333                |
| 14 | 22/30         | 43.182                |
