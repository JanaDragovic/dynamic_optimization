# Viterbi Algoritam

## Opis problema

Implementiran je Viterbi algoritam za dekodovanje skrivenog Markovljevog lanca sa tri skrivena stanja (🌧️, ☁️, ☀️) i dva moguća opservaciona simbola (NE - loše raspoloženje, DA - dobro raspoloženje).

Parametri modela:

Tranziciona matrica:
```
          🌧️     ☁️      ☀️
🌧️       0.5     0.3     0.2
☁️       0.4     0.2     0.4
☀️       0.0     0.3     0.7
```

Emisiona matrica:
```
          NE      DA
🌧️       0.9     0.1
☁️       0.6     0.4
☀️       0.2     0.8
```

Početno stanje: 🌧️.

## Opis programa

Program se sastoji od dve glavne funkcije:
- `viterbi()` - implementira Viterbi algoritam za pronalaženje najverovanije sekvence stanja
- `izracunaj_sve_verovatnoce()` - računa verovatnoće svih mogucih sekvenci stanja radi verifikacije

## Rezultati

### Test 1: Sekvenca iz zadatka
Opservaciona sekvenca: NE, DA, NE, NE, NE

Viterbi rezultat: 🌧️ -> ☁️ -> 🌧️ -> 🌧️ -> 🌧️
Verovatnoća: 7.873200e-03

Top 5 sekvenci:
1. 🌧️, ☁️, 🌧️, 🌧️, 🌧️ : 7.873200e-03 (Viterbi)
2. 🌧️, ☀️, ☁️, 🌧️, 🌧️ : 4.199040e-03
3. 🌧️, 🌧️, 🌧️, 🌧️, 🌧️ : 4.100625e-03
4. 🌧️, ☁️, 🌧️, 🌧️, ☁️ : 3.149280e-03
5. 🌧️, ☁️, 🌧️, ☁️, 🌧️ : 2.519424e-03

_Algoritam je prepoznao da jedini DA u sekvenci odgovara oblačnom vremenu (emisiona verovatnoca 0.4), dok preostali NE simboli odgovaraju kiši (emisiona verovatnoca 0.9)._


### Test 2: Stalno dobro raspoloženje
Opservaciona sekvenca: DA, DA, DA, DA, DA

Viterbi rezultat: 🌧️ -> ☀️ -> ☀️ -> ☀️ -> ☀️
Verovatnoća: 2.809856e-03

Top 5 sekvenci:
1. 🌧️, ☀️, ☀️, ☀️, ☀️ : 2.809856e-03 (Viterbi)
2. 🌧️, ☁️, ☀️, ☀️, ☀️ : 1.204224e-03
3. 🌧️, ☀️, ☀️, ☀️, ☁️ : 6.021120e-04
4. 🌧️, ☀️, ☁️, ☀️, ☀️ : 3.440640e-04
5. 🌧️, ☀️, ☀️, ☁️, ☀️ : 3.440640e-04

_Pošto je osoba stalno u dobrom raspoloženju, algoritam brzo prelazi na sunčano vreme koje ima najvecu verovatnoću emitovanja DA (0.8). ☀️ takodje ima veliku verovatnoću ostanka u istom stanju (0.7)._


### Test 3: Stalno loše raspoloženje
Opservaciona sekvenca: NE, NE, NE, NE, NE

Viterbi rezultat: 🌧️ -> 🌧️ -> 🌧️ -> 🌧️ -> 🌧️
Verovatnoća: 3.690563e-02

Top 5 sekvenci:
1. 🌧️, 🌧️, 🌧️, 🌧️, 🌧️ : 3.690563e-02 (Viterbi)
2. 🌧️, 🌧️, 🌧️, 🌧️, ☁️ : 1.476225e-02
3. 🌧️, ☁️, 🌧️, 🌧️, 🌧️ : 1.180980e-02
4. 🌧️, 🌧️, 🌧️, ☁️, 🌧️ : 1.180980e-02
5. 🌧️, 🌧️, ☁️, 🌧️, 🌧️ : 1.180980e-02

_Kišno vreme ima najvecu verovatnocu emitovanja NE (0.9), pa algoritam ostaje u stanju kise. Ovo je i najerovatnija sekvenca od svih testova (3.7%), sto je ocekivano jer 🌧️ dominantno emituje NE._


### Test 4: Naizmenično raspoloženje
Opservaciona sekvenca: NE, DA, NE, DA, NE

Viterbi rezultat: 🌧️ -> ☀️ -> ☀️ -> ☀️ -> ☁️
Verovatnoća: 2.032128e-03

Top 5 sekvenci:
1. 🌧️, ☀️, ☀️, ☀️, ☁️ : 2.032128e-03 (Viterbi)
2. 🌧️, ☁️, 🌧️, ☁️, 🌧️ : 1.679616e-03
3. 🌧️, ☀️, ☀️, ☀️, ☀️ : 1.580544e-03
4. 🌧️, ☀️, ☁️, ☀️, ☁️ : 1.492992e-03
5. 🌧️, ☀️, ☁️, ☀️, ☀️ : 1.161216e-03

_U ovom primeru imamo situaciju da algoritam bira sunčano vreme koje moze da emituje i NE (sa verovatnocom 0.2) umesto čestih prelaza izmedju kiše i sunca. Ovo je zato sto Sunce ima veliku verovatnocu ostanka u istom stanju (0.7), pa je ukupna verovatnoća veća nego kod čestih promena stanja._


## Zaključak

U sva četiri testa, Viterbijev algoritam je pronašao sekvencu sa najvećom verovatnoćom, sto je potvrđeno poređenjem sa svim mogućim sekvencama. Viterbi rezultat se uvek nalazi na prvom mestu liste sortirane po verovatnoći.
Broj mogucih sekvenci za sekvencu duzine T je 3^(T-1) jer je prvo stanje fiksirano (🌧️). Za T=5 to je 81 sekvenca.

