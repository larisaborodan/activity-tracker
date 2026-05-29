# Software Engineering Intern — Take-Home Task

Bine ai venit! Acest task este parte din procesul de selecție pentru poziția de **Software Engineering Intern**.

Scopul nostru nu este să vedem dacă știi „răspunsul corect”, ci **cum gândești, cum găsești soluții la probleme și cum comunici**.

---

## Contextul

Suntem o companie AI-first și folosim zilnic asistenți AI (ChatGPT, Cursor, Copilot etc.). **Te încurajăm să-i folosești și tu** pentru acest task, exact așa cum ai face într-o zi normală de muncă.

Singurele reguli:

1. **Înțelege ce livrezi.** Dacă AI-ul generează cod pe care nu-l poți explica, asta e o problemă.
2. **Fii transparent.** În `NOTES.md` scrie scurt ce-ai făcut tu și unde te-a ajutat AI-ul.
3. **Verifică rezultatul.** Codul care „pare să meargă” nu e suficient. Rulează testele.

---

## Cum începi
1.	Dezarhivează fișierul atașat la acest email
2.	Citește documentația din arhivă înainte să începi
3.	Lucrezi local cu stack-ul tău preferat și organizezi codul cum vrei


## Task-ul

Ai primit o aplicație FastAPI care urmărește **evenimente de activitate** ale unor utilizatori (logins, page views, clicks etc.).

Aplicația **are cel puțin 3 bug-uri** și **îi lipsește un endpoint nou**.

### Ce trebuie să faci

1. **Pornește aplicația local** și rulează testele.
2. **Găsește și rezolvă bug-urile.** Toate sunt acoperite de teste existente — când le repari, testele devin verzi.
3. **Adaugă un endpoint nou:** `GET /users/{user_id}/events?since=<ISO_date>`
   - Returnează doar evenimentele utilizatorului respectiv, mai noi decât data primită.
   - Dacă `since` lipsește, returnează toate evenimentele utilizatorului.
   - Dacă utilizatorul nu există, returnează `404`.
4. **Scrie cel puțin 2 teste** pentru endpoint-ul nou.
5. **Completează `NOTES.md`** (vezi mai jos).

Pe lângă cerințele explicite, evaluăm și robustețea implementării în cazuri-limită.

---

## Cum rulezi proiectul

Ai nevoie de Python 3.11+.

```bash
pip install -e ".[dev]"
uvicorn app.main:app --reload
```

Pentru teste:

```bash
pytest -v
```

Documentația API o vezi la http://localhost:8000/docs după ce pornești serverul.

---

## Cum livrezi
Răspunde la email-ul inițial cu soluția ta, până duminică 7 iunie, ora 23:59. O poți livra cum îți e mai comod:
   - un link către un repo public (GitHub, GitLab, Bitbucket sau altele), sau
   - O arhivă .zip atașată la răspuns
   
Înainte de deadline, asigură-te că:
   - Ai documentat cum rulezi totul și ce decizii ai luat
   - Soluția e completă și o putem rula local
   - Răspunsul tău e trimis înainte de deadline

**Deadline: duminică, 7 iunie, ora 23:59.** Dacă ai nevoie de mai mult timp, scrie-ne — preferăm să livrezi ceva îngrijit decât să te grăbești.

---

## Cum evaluăm

Punctăm 7 dimensiuni, fiecare 1-5:

| Criteriu | Ce căutăm |
|---|---|
| **Corectitudine** | Bug-urile sunt găsite și rezolvate. Endpoint-ul nou funcționează. |
| **Calitatea codului** | Cod citibil, denumiri bune, fără cod mort, structură consistentă cu restul proiectului. |
| **Teste** | Teste relevante, nu doar happy-path. Cazuri edge tratate. |
| **Debugging** | În NOTES.md explică **cum** ai găsit bug-urile, nu doar **ce** ai schimbat. |
| **Git workflow** | Commits mici, mesaje clare, istoric coerent. |
| **NOTES.md** | Scurt, clar, onest despre folosirea AI-ului și deciziile luate. |
| **Comunicare** | Cum explici deciziile și ce ai face cu mai mult timp. |


---

## Sfaturi

- Citește tot codul existent înainte să începi. E foarte puțin.
- Dacă te blochezi 30 de minute pe ceva, scrie în NOTES.md unde te-ai blocat și treci mai departe.
- Întreabă orice neclaritate — preferăm întrebări bune decât presupuneri proaste.

Succes! Suntem curioși să vedem ce livrezi.
