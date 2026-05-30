# Kosmosa matemātikas misija 🚀📐

Izglītojoša interaktīva spēle Python vidē, kas apvieno kosmosa ceļojumu simulāciju ar matemātikas uzdevumu risināšanu. Projekts ir izstrādāts, izmantojot objektorientētās programmēšanas (OOP) principus.

## 👥 Projekta izstrādātāji / Komanda

* Aleksandrs Travinovs
* Pāvels Oniščenko 

---

## 🌌 Projekta ideja un mērķis

Spēlētājs iejūtas kosmosa kuģa pilota lomā, kuram jāvada kuģis starp planētām. Lai veiksmīgi sasniegtu galamērķi, pilotam jārisina dažādi matemātikas uzdevumi (procenti, daļskaitļi, vienādojumi). Pareizas atbildes papildina kuģa degvielas rezerves un stabilizē kursu, savukārt kļūdas ietekmē resursus.

**Mērķis:** Veicināt matemātikas apguvi pamatskolas un vidusskolas skolēniem (10–17 gadi) caur spēles elementiem un tūlītēju atgriezenisko saiti, nodrošinot adaptīvu grūtības pakāpi.

---

## ⚙️ Galvenās funkcijas

1. **Daudzveidīgi uzdevumi:** Formulu aprēķini, procenti, daļskaitļi un vienādojumi.
2. **Adaptīvā grūtības sistēma:** Spēle automātiski pielāgojas spēlētāja zināšanu līmenim (paaugstina vai pazemina grūtību).
3. **Resursu pārvaldība:** Degvielas (`fuel`) un ātruma (`speed`) kontrole atkarībā no atbildēm.
4. **Progresa saglabāšana:** Spēlētāju profilu datu un statistikas glabāšana failā (JSON/CSV formatā).
5. **Rangu tabula (Leaderboard):** Labāko rezultātu vizualizācija konsolē.

---

## 🏗️ Programmas arhitektūra (OOP Struktūra)

Projekta pamatā ir stingra klašu hierarhija un moduļu struktūra:

* `Spaceship` — Pārvalda kuģa stāvokli (degviela, ātrums, pozīcija).
* `Player` — Glabā spēlētāja profilu, punktus un sesijas statistiku.
* `Task` — Bāzes klase matemātiskajiem uzdevumiem.
  * *Atvasinātās klases:* `FormulaTask`, `PercentTask`, `FractionTask`, `EquationTask`.
* `Mission` — Atbild par konkrētā maršruta un uzdevumu secības izpildi.
* `GameEngine` — Galvenā spēles loģika, kas apvieno visas sistēmas un vada spēles gaitu.
* `FileManager` — Nodrošina datu lasīšanu un rakstīšanu failos.
* `Leaderboard` — Atbild par spēlētāju rangu apstrādi un attēlošanu.

---

## 🛠️ Tehnoloģijas

* **Valoda:** Python 3.x
* **Datu glabāšana:** JSON / CSV (Python iebūvētās bibliotēkas)
* **Saskarne:** Konsoles izvade (CLI)
