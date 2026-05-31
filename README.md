# Kosmosa matemātikas misija 🚀📐

Izglītojoša 2D datorspēle Python vidē, kas apvieno kosmosa kuģa vadīšanas simulāciju ar dažādu tēmu un sarežģītības matemātikas uzdevumu risināšanu. Projekts ir izstrādāts, izmantojot **Pygame** bibliotēku un balstīts uz stingriem objektorientētās programmēšanas (OOP) principiem un arhitektūras vadlīnijām.

## 👥 Projekta izstrādātāji / Komanda

* Aleksandrs Travinovs
* Pāvels Oniščenko

---

## 🌌 Projekta ideja un mērķis

Spēlētājs vada kosmosa kuģi, kas automātiski pārvietojas uz augšu cauri asteroīdu joslām (kosmosa fons slīd uz leju). Lai veiksmīgi sasniegtu galamērķi - zaļo finiša līniju līmeņa augšdaļā -, spēlētājam ar bultiņām jāvada kuģis pa labi/kreiski, jāizvairās no sadursmēm ar asteroīdiem, jāvāc resursi un regulāri jāatrisina matemātiskie uzdevumi, kas uz laiku aptur spēles laika tecējumu.

**Mērķis:** Veicināt matemātikas prasmes pamatskolas un vidusskolas skolēniem vecumā no 10 līdz 17 gadiem caur spēles elementiem, piedāvājot tūlītēju vizuālo un skaitlisko atgriezenisko saiti, kā arī adaptīvu, līmeņos strukturētu grūtības progresu.

---

## ⚙️ Galvenās funkcijas

1. **Dinamiska 2D vide:**
   * Nepārtraukti no augšas krītošu asteroīdu plūsma. Asteroīdiem ir elastīga sadursmju fizika un horizontālie atsitieni no ekrāna malām.
   * Nejauši izvietoti un vizuāli animēti veselības (`HealthPickup`) un degvielas (`FuelPickup`) resursu objekti.

2. **Strukturēta līmeņu sistēma (10 līmeņi):**
   * Katrā nākamajā līmenī pieaug kuģa lidojuma ātrums, asteroīdu blīvums un kustības ātrums, kā arī saīsinās uzdevumu risināšanas laiks.
   * Līmeņu garums ir balansēts robežās no 44 līdz 65 sekundēm reālā laika (pārrēķināts pasaules augstumā un pikseļu slīdēšanas ātrumā).

3. **Resursu un HUD sistēma:**
   * **Dzīvības un degvielas joslas:** HUD apakšā vizualizē resursus un attēlo skaitliskās vērtības (`HP/100` un `Degviela/100`).
   * **Kļūdu indikators (Strikes):** Spēlētājam ir atļautas maksimāli 3 kļūdas. Katra nepareiza atbilde vai laika pārsniegšana aktivizē sarkanu krustu HUD centrā.
   * **Progresa skala:** Labajā pusē izvietotais vertikālais indikators reāllaikā attēlo kuģa attālumu līdz finiša līnijai.

4. **Īpašie mehānismi:**
   * **Dzinēja kļūme (Breakdown):** Pēkšņi rodas tehnisks bojājums. Pareiza atbilde aktivizē degvielas taupīšanas režīmu uz 4.5 sekundēm, nepareiza - atņem 20 degvielas vienības un piešķir sodu (Strike).
   * **Pēdējā iespēja (Last Chance):** Kad degviela nokrītas līdz 0, spēle tiek pauzēta un spēlētājam tiek dots viens mēģinājums atrisināt grūtāku uzdevumu, lai saņemtu 50 degvielas vienības. Ja uzdevums netiek atrisināts, iestājas zaudējums.

5. **Efekti un partikulas:**
   * Trīs slāņu parallax zvaigžņu fons kopā ar nejauši ģenerētiem fona miglājiem (nebulae).
   * Ekrāna trīcēšanas efekts (`Screen Shake`) sadursmju brīžos.
   * Animētas liesmas pie kuģa dzinējiem, pastāvīgas dzinēja dūmu partikulas un krāsaini sprādzieni pēc sadursmēm vai objektu savākšanas.

6. **Progresa saglabāšana:**
   Pabeigtie un atbloķētie līmeņi tiek saglabāti un nolasīti lokālā JSON failā (`save_data.json`). Līmeņu izvēlne bloķē nepieejamos līmeņus un attēlo pabeigtos ar zelta ķeksīti.

---

## 🏗️ Programmas arhitektūra un moduļi

Projekta struktūra ir modularizēta, nodrošinot augstu koda lasāmību un vieglu uzturēšanu:

* `main.py` - Programmas ieejas punkts. Satur galveno `Game` klasi, kas darbojas kā stāvokļu mašīna (`MainMenu`, `LevelSelect`, `Gameplay`, `ResultScreen`).
* `gameplay.py` - Vada vienas spēles sesijas loģiku, reāllaika laika atskaiti, objektu sadursmes un spēles pauzēšanu uzdevumu laikā.
* `background.py` - Atbild par kosmosa fona un parallax zvaigžņu slāņu renderēšanu.
* `particles.py` - Realizē vizuālo daļiņu izveides un dzīves cikla apstrādi.
* `math_tasks.py` - Matemātikas uzdevumu ģenerators ar 5 grūtības pakāpēm (no aritmētikas līdz vienādojumiem un procentiem).
* `level_config.py` - Glabā un padod līmeņu parametru konfigurācijas.
* `game_state.py` - Nodrošina progresu datu saglabāšanu JSON failā.
* `ui.py` - Satur lietotāja saskarnes komponentus (Pogas, HUD, uznirstošo uzdevumu logu `TaskPopup`).
* `entities/` - Spēles fizisko objektu pakotne:
  * `base_entity.py` - Abstraktā bāzes klase `BaseEntity` (manto no `abc.ABC`).
  * `ship.py` - Spēlētāja kuģis (kustība, vizuālais dizains, dzinēju dūmu izvade).
  * `asteroid.py` - Asteroīdi ar neregulāru formu, rotācijas fiziku un krāteriem.
  * `pickup.py` - Resursu vākšanas objekti (`HealthPickup` un `FuelPickup`).

---

## 💎 OOP principu realizācija projektā

Projekts tika izstrādāts ar mērķi demonstrēt akadēmiskās objektorientētās programmēšanas (OOP) zināšanas:

### 1. Abstraktā klase un virtuālās funkcijas (Abstraction)
Fails `entities/base_entity.py` definē bāzes klasi `BaseEntity`, kas manto no Python iebūvētās `abc.ABC` klases. Šajā klasē ir deklarētas tīri virtuālas (abstraktas) metodes, kuras bērnu klasēm ir obligāti jāpārraksta:
```python
@abstractmethod
def update(self, dt: float) -> None:
    ...

@abstractmethod
def draw(self, surface: pygame.Surface, cam_offset_y: float) -> None:
    ...

@abstractmethod
def get_rect(self) -> pygame.Rect:
    ...
```

### 2. Mantošana (Inheritance)
Kods izmanto daudzlīmeņu mantošanas hierarhiju, tādējādi izvairoties no koda dublēšanās:
```
           [ BaseEntity ]
           /      |     \
          /       |      \
     [ Ship ] [ Asteroid ] [ Pickup ] (Abstraktā klase)
                            /      \
                           /        \
             [ HealthPickup ]      [ FuelPickup ]
```
Klasēs `HealthPickup` un `FuelPickup` kopīgā peldēšanas animācijas un pozicionēšanas loģika ir mantota no vecāka klases `Pickup`, bet specifiskā iedarbība - no abstraktās metodes `apply()`.

### 3. Iekapsulēšana un datu slēpšana (Encapsulation)
Visas objektu iekšējās mainīgo vērtības (piemēram, veselība, ātrums, pozīcija) ir aizsargātas, izmantojot vienas pasvītras `_` (protected) un dubultās pasvītras `__` (private) konvenciju. Piekļuve šiem datiem un to modifikācija no ārpuses ir iespējama tikai caur publiskajām metodēm vai `@property` dekoratoriem, kas veic datu validāciju:
```python
@property
def health(self) -> float:
    return self._health

@health.setter
def health(self, value: float) -> None:
    # Novērš vērtības iziešanu ārpus pieļaujamajām robežām (0..100)
    self._health = max(0.0, min(float(value), float(SHIP_MAX_HEALTH)))
```

### 4. Polimorfisms (Polymorphism)
Dinamiskais polimorfisms tiek izmantots spēles galvenajā ciklā failā `gameplay.py`. Visi krītošie objekti, neatkarīgi no to tipa, tiek glabāti un apstrādāti vienā sarakstā, izmantojot vienotu saskarni, lai gan katra objekta zīmēšanas un kustības loģika būtiski atšķiras:
```python
# gameplay.py update ciklā:
for pickup in self._pickups:
    pickup.update(dt)  # Polimorfs izsaukums

for ast in self._asteroids:
    ast.update(dt)     # Polimorfs izsaukums
```

---

## 🛠️ Tehnoloģijas

* **Programmēšanas valoda:** Python 3.11+
* **Bibliotēkas:** Pygame 2.6+
* **Datu glabāšana:** JSON (`save_data.json` progresa sinhronizācijai)

---

## 🎮 Kā palaist spēli un vadība

1. Pārliecinieties, ka jūsu datorā ir uzstādīts Python un Pygame bibliotēka:
   ```bash
   pip install pygame
   ```
2. Lejupielādējiet projekta mapi un palaidiet spēli caur termināli:
   ```bash
   python main.py
   ```

### Vadība spēles laikā:
* **Bultiņa pa kreisi / pa labi** - kuģa pārvietošana horizontāli.
* **[ENTER]** - apstiprināt atbildi matemātikas uzdevuma logā.
* **[BACKSPACE]** - dzēst pēdējo ievadīto ciparu/simbolu.
* **[E]** - aktivizēt ārkārtas degvielas uzdevumu (kad kuģim beidzas degviela).
* **[F11]** - pārslēgt pilnekrāna (Fullscreen) režīmu.