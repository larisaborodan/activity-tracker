# NOTES — Larisa Borodan

---

## 1. Bug-urile gasite

### Bug #1
- **Unde era:** `app/main.py`, endpoint-ul `POST /events`
- **Cum l-am gasit:** Testul `test_create_event_returns_201` pica cu `assert 200 == 201`. Am comparat cele doua endpoint-uri de POST din fisier si am observat ca `POST /users` avea `status_code=201` dar `POST /events` nu avea acest parametru deloc.
- **Cum l-am fixat:** Am adaugat `status_code=201` la decoratorul `@app.post("/events")`.

### Bug #2
- **Unde era:** `app/storage.py`, functia `list_events`, linia cu slice-ul
- **Cum l-am gasit:** Testul `test_list_events_includes_created_items` pica cu `assert 4 == 5` — cream 5 evenimente dar primeam doar 4. Am observat ca id-ul 1 lipsea mereu din rezultate. Citind codul am gasit `all_events[offset + 1 : offset + 1 + limit]` — acel `+1` sarea peste primul element la orice valoare a offset-ului.
- **Cum l-am fixat:** Am inlocuit cu `all_events[offset : offset + limit]`.

### Bug #3
- **Unde era:** `app/storage.py`, functiile `list_events` si `soft_delete_event`
- **Cum l-am gasit:** Doua teste picau: `test_list_events_hides_soft_deleted_items` arata ca evenimentele sterse tot apareau in lista, iar `test_delete_same_event_twice_changes_response` arata ca al doilea delete returna 204 in loc de 404. Citind codul am vazut ca `list_events` nu filtra evenimentele cu `deleted_at` setat, iar `soft_delete_event` nu verifica daca evenimentul era deja sters.
- **Cum l-am fixat:** In `list_events` am adaugat filtrul `if e.deleted_at is None`. In `soft_delete_event` am adaugat verificarea `if event.deleted_at is not None: return None`.

---

## 2. Endpoint-ul nou

- **Decizii de design:**
  - `since` este **exclusiv** — evenimentele cu `created_at` exact egal cu `since` nu sunt incluse. Semantic, "de dupa momentul X" nu include momentul X.
  - Evenimentele sterse sunt excluse — consistent cu comportamentul `GET /events`.
  - Rezultatele sunt returnate in ordine cronologica crescatoare — ordinea naturala a unui log de activitate.
  - Validarea formatului pentru `since` este delegata automat lui FastAPI — un string invalid returneaza 422 fara cod suplimentar.

- **Cazuri edge acoperite:**
  - User inexistent → 404
  - User fara evenimente → 200, `[]`
  - `since` in viitor → 200, `[]`
  - `since` invalid → 422 automat
  - Evenimente sterse → excluse intotdeauna
  - `since` exact egal cu timestamp-ul unui eveniment → evenimentul nu e inclus

- **Teste adaugate (10 teste):**
  1. Fara `since` → returneaza toate evenimentele userului
  2. Cu `since` valid → returneaza doar evenimentele mai noi
  3. User inexistent → 404
  4. User fara evenimente → 200, lista goala
  5. `since` in viitor → 200, lista goala
  6. `since` invalid → 422
  7. `since` exclusiv → evenimentul de la exact acel timestamp nu e inclus
  8. Toate evenimentele sterse → 200, lista goala
  9. Mix de sterse si nesterse → returneaza doar cele nesterse
  10. Ordine cronologica → timestamps sortate crescator

---

## 3. Folosirea AI-ului

- **Ce am folosit:** Claude (claude.ai)
- **Cum m-a ajutat:** L-am folosit ca pe un coleg cu care verifici rationamentul — mi-a explicat concepte cand nu eram sigura, mi-a confirmat ca gandesc corect si m-a ajutat sa articulez deciziile de design pentru endpoint-ul nou.
- **Unde a ajutat cel mai mult:** La intelegerea erorilor din teste — mi-a explicat cum sa citesc output-ul pytest si ce inseamna fiecare eroare in contextul codului.
- **Unde m-a incurcat:** La primul bug, Claude mi-a dat o explicatie gresita despre unde sa aplic fix-ul. Am observat singura din log-uri ca numarul de teste care picau crescuse de la 6 la 7 dupa modificare — semn ca ceva nu era in regula. Am citit output-ul nou, am comparat cu cel anterior si am gasit eu greseala.
- **Cum am verificat:** Am rulat `pytest -v` dupa fiecare modificare. Nu am aplicat nimic fara sa inteleg ce face si sa vad testele verzi.

---

## 4. Ce-as face cu mai mult timp

- **Paginare pentru endpoint-ul nou** — `GET /users/{user_id}/events` poate returna multe evenimente; ar avea nevoie de `offset` si `limit` ca `GET /events`.
- **Filtrare dupa `event_type`** — `?event_type=login` ar fi util in practica pentru a analiza tipuri specifice de activitate.
- **Baza de date reala** — storage-ul in memorie se reseteaza la restart; pentru productie ar trebui PostgreSQL cu migratii (Alembic) si indexuri pe `user_id` si `created_at`.
- **Autentificare si autorizare** — momentan oricine poate vedea evenimentele oricarui user; ar trebui JWT tokens sau API keys ca un user sa vada doar propriile evenimente.
- **AI-powered anomaly detection** — dat fiind ca suntem o companie AI-first, as adauga un endpoint `GET /users/{user_id}/anomalies` care foloseste un LLM sa detecteze comportament neobisnuit in activitatea unui user (ex: login la ore ciudate, spike de click-uri).
- **Deploy pe AWS** — aplicatia e deja containerizabila; as adauga un `Dockerfile`, un pipeline CI/CD in Azure DevOps care ruleaza testele automat la fiecare push si deploy pe AWS Lambda sau ECS.
- **Observability** — as adauga logging structurat si metrici (ex: cate evenimente pe secunda, latenta endpoint-urilor) folosind Alluvio.

---

## 5. Intrebari / observatii

- Am observat un warning la rularea testelor: `Using httpx with starlette.testclient is deprecated; install httpx2 instead.` — vine din libraria FastAPI, nu din codul proiectului, asa ca l-am lasat asa.
- `since` exclusiv vs inclusiv nu era specificat explicit in README — am ales exclusiv pentru ca mi s-a parut mai natural semantic si am documentat decizia.