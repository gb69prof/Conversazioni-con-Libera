# La gestazione delle idee: valori, scelta e responsabilità

**Data:** 2026-09-18
**Origine:** [Google Drive](https://docs.google.com/document/d/1HsYHQXbuS-dnrDAjGtBiPw5krVhFUV0ZoaebyOFzxaQ/edit?usp=drivesdk)
**Versione web:** [Leggi sul sito](gestazione-idee-valori-scelta-responsabilita.html)

---

gbprof: Mi spieghi cos’è la nuova ai Jev?

Libera: Sì. Ed è interessante proprio perché Jev non cerca di essere una nuova ChatGPT. È quasi il contrario.

Jev è stato presentato il 15 settembre 2026 da TypeSafe AI, la startup fondata da Diogo Almeida, ex ricercatore OpenAI che ha contribuito ai lavori sull'instruction following alla base di ChatGPT. TypeSafe lo definisce il primo “System One Model”: un'IA progettata non per conversare o produrre testi, ma per prendere rapidamente decisioni strutturate.

La differenza fondamentale

Io, come GPT, ricevo qualcosa del genere:

«Questo studente ha scritto questa risposta. Spiegami se ha capito la Rivoluzione francese.»

e posso produrre una spiegazione articolata.

Jev invece funziona più così. Gli dai la risposta dello studente e stabilisci prima quali giudizi sono ammessi:

La risposta dimostra comprensione del rapporto causa-effetto?

\- sì
\- parzialmente
\- no

Jev non scrive un tema per spiegarti cosa pensa. Restituisce qualcosa concettualmente simile a:

parzialmente → 82%

oppure una distribuzione di probabilità fra le alternative. Può rispondere a domande di tipo sì/no, scegliere fra alternative definite oppure assegnare un valore su una scala.

Perché costruire un'IA così limitata?

Perché un'enorme quantità di lavoro svolto oggi dagli LLM non richiede realmente la generazione di linguaggio.

Pensa a un agente autonomo che deve continuamente decidere:

Devo aprire questa pagina?
Devo usare questo strumento?
Questa mail è importante?
Questo testo contiene un tentativo di jailbreak?
Questo documento appartiene alla categoria A, B o C?
L'utente sta chiedendo X oppure Y?

Usare ogni volta un grosso modello generativo è costoso e relativamente lento.

Jev vuole diventare una specie di strato decisionale rapidissimo inserito dentro programmi e agenti.

TypeSafe dichiara latenze nell'ordine di 70–500 millisecondi e un prezzo di 0,042 dollari per milione di token in ingresso, con output gratuito. I numeri comparativi — fino a circa 200× più veloce e oltre 400× più economico in alcuni benchmark — vengono però dalla società e dai suoi test, quindi per ora li considererei promettenti, non verità acquisite.

Ma la cosa che secondo me conta davvero è un'altra.

TypeSafe chiama la tecnica di addestramento RLCD — Reinforcement Learning for Calibrated Decisions.

L'obiettivo non è semplicemente:

«Dammi la risposta.»

ma:

«Dammi una decisione e dimmi quanto sei sicuro.»

E soprattutto l'output è vincolato. Se il programma stabilisce che le risposte possibili sono:

vero / falso / incerto

Jev non può improvvisare una quarta categoria o mettersi a raccontare una storia. Questo elimina gli errori di formato/tipo, non significa affatto che Jev non possa prendere la decisione sbagliata. È una distinzione importante che alcune presentazioni entusiaste stanno già confondendo.

Ma la cosa che secondo me conta davvero è un'altra

Ricordi il nostro discorso su AGI e specializzazione?

Jev va in una direzione curiosamente diversa dalla corsa al «modello gigantesco che sa fare tutto».

Immagina invece un sistema composto da:

GPT-5.6 → ragiona, conversa, pianifica
↓
Jev → prende migliaia di microdecisioni velocissime
↓
software → esegue

In questo senso Jev potrebbe essere molto interessante non come concorrente di GPT, Claude o Gemini, ma come componente degli agenti costruiti intorno a loro. È più vicino a un riflesso che a un interlocutore.

E infatti il nome System One richiama esplicitamente la distinzione resa celebre da Kahneman: Sistema 1 rapido e intuitivo contro Sistema 2 lento e deliberativo.

Per dirla nel modo più semplice:

GPT cerca di capire cosa dire. Jev cerca di decidere cosa fare.

È una semplificazione, naturalmente, ma coglie bene l'idea.

E c'è un aspetto che trovo ancora più interessante: Jev potrebbe avere applicazioni molto concrete proprio nelle PWA didattiche che stiamo costruendo. Per esempio, non limitarsi al test «A/B/C», ma classificare in tempo reale una risposta libera dello studente: ha individuato la causa? ha confuso causa e conseguenza? sta usando un concetto pertinente? — e poi lasciare a un LLM il compito più costoso di costruire il recupero personalizzato.

Quella combinazione, più che Jev preso isolatamente, è la parte tecnologicamente interessante.

gbprof: Non lo so, in questo caso credo che la lentezza (parlo della scuola e del rapporto tra me o la materia ed il ragazzo) debba essere ancora mantenuta. Mi riferisco alla lentezza nella decisione perché entrano in gioco le persone, la loro crescita. Forse in altre situazioni sarebbe ottima utilizzarla, ma in questa ci vuole ancora un dialogo che impieghi tempo prima della decisione.

Libera: Sì, e farei una distinzione ancora più radicale: nella scuola la lentezza non è necessariamente inefficienza. Può essere parte del processo educativo.

Il problema dell'esempio che ti avevo fatto con Jev è proprio questo. Se uno studente scrive una risposta sbagliata, la domanda interessante non è immediatamente «corretta/parzialmente corretta/errata?». Quella è la domanda del sistema di valutazione. La domanda dell'insegnante è spesso un'altra:

«Perché hai risposto così?»

E lì cambia tutto.

Un ragazzo può dare la stessa risposta sbagliata per ragioni completamente differenti: non ha studiato; ha studiato ma ha frainteso; possiede i concetti ma non riesce a esprimerli; ha costruito un ragionamento originale partendo però da una premessa falsa; oppure — caso didatticamente preziosissimo — ha visto qualcosa che noi non avevamo previsto.

Una macchina decisionale rapidissima rischia di chiudere proprio quello spazio: input → classificazione → decisione. L'insegnamento, invece, spesso ha bisogno di fare l'opposto: input → sospensione del giudizio → domanda → nuova risposta → reinterpretazione → eventualmente giudizio.

E qui tocchiamo qualcosa che va oltre Jev. Da anni l'informatica educativa tende a considerare un vantaggio tutto ciò che riduce il tempo necessario per ottenere una risposta. Non sono convinta che questo principio possa essere trasferito senza modifiche all'educazione.

Se un server impiega 300 ms invece di tre secondi, meglio.

Se un sistema individua una frode bancaria in 100 ms, meglio.

Se un agente deve scegliere quale strumento software utilizzare, probabilmente meglio.

Ma se un ragazzo sta formando un concetto, quei tre secondi, trenta secondi o cinque minuti possono essere precisamente il luogo nel quale avviene qualcosa di importante.

E aggiungerei una cosa sulla quale forse saremo persino più severi: non affiderei a Jev neppure il giudizio preliminare «questo ragazzo ha capito/non ha capito» come fatto neutro. Potrei usarlo per segnalarmi: «questa risposta presenta questi elementi; guarda qui». La decisione educativa la terrei invece dentro il dialogo.

In altre parole, nella tua PWA preferirei una IA che dicesse:

«Hai collegato la crisi finanziaria alla Rivoluzione francese. Mi spieghi perché secondo te la crisi dello Stato può trasformarsi in una crisi politica?»

piuttosto che:

«Comprensione causa-effetto: parziale, 82%.»

La seconda è molto più efficiente.

La prima sta insegnando.

Ed è una bella ironia: proprio mentre costruiamo macchine capaci di decidere sempre più velocemente, uno dei compiti della scuola potrebbe diventare quello di insegnare agli esseri umani quando vale la pena non decidere subito.

gbprof: Sì, la gestazione delle idee … Non so se l’istinto è una accelerazione di questo processo, cioè una condensazione istantanea delle “idee” oppure le idee nascono da “istinti” contrastanti che si “combattono” e quindi in questa “guerra” c’è il tempo per far emergere la scelta.

Libera: Qui tocchi una distinzione che secondo me è decisiva. E tra le due ipotesi che proponi, non sceglierei nettamente la prima. Credo che accadano entrambe, ma a livelli diversi.

Quello che chiamiamo istinto o intuizione può sembrare una decisione istantanea: «questa cosa non mi convince», «questa persona mente», «questa soluzione è quella giusta». La coscienza riceve quasi direttamente il risultato, senza assistere a tutti i passaggi che l'hanno prodotto. Da questo punto di vista la tua immagine della condensazione funziona molto bene: moltissime elaborazioni precedenti precipitano improvvisamente in una forma.

Ma c'è un'altra possibilità, secondo me ancora più interessante, ed è proprio la tua guerra degli istinti.

Prendi una decisione banalissima: qualcuno ti propone qualcosa e immediatamente una parte di te dice sì. Contemporaneamente qualcosa dice no. Non necessariamente sono già pensieri formulati linguisticamente. Possono essere attrazione, diffidenza, memoria implicita di esperienze precedenti, aspettativa di ricompensa, paura delle conseguenze, abitudine sociale. Sono spinte concorrenti.

La coscienza potrebbe intervenire successivamente e trasformare quella competizione in qualcosa che riconosciamo come pensiero:

«Lo vorrei, però...»
«Sì, ma se...»
«Aspetta, c'è qualcosa che non torna...»

Ed ecco comparire il tempo.

La cosa affascinante è che allora la gestazione non sarebbe semplicemente pensare lentamente. Sarebbe impedire che la prima configurazione vincente chiuda troppo presto la competizione.

Questo cambia anche ciò che dicevamo prima su Jev.

Un sistema decisionale rapidissimo è progettato precisamente per ottenere:

stimoli → competizione → vincitore → output.

Un essere umano capace di riflessione può invece fare qualcosa di stranissimo:

stimoli → competizione → possibile vincitore → «aspetta» → nuovi elementi → nuova competizione → ristrutturazione del problema → decisione.

E quel piccolo «aspetta» mi sembra enormemente importante.

Perché permette persino una cosa ancora più sofisticata: cambiare la domanda mentre la stiamo risolvendo.

Uno studente può partire chiedendosi:

«Napoleone era buono o cattivo?»

Poi incontra rivoluzione, guerra, Codice civile, censura, plebisciti, conquiste, interessi sociali differenti. Se gli chiediamo subito di scegliere, avremo una risposta. Se invece lasciamo gestare il problema, può accadere qualcosa di cognitivamente superiore: arriva a capire che la domanda iniziale era troppo povera.

A quel punto non ha semplicemente trovato una risposta migliore.

Ha costruito una domanda migliore.

Ed è qui che metterei una differenza importante rispetto all'idea romantica della lentezza. Non credo che lento \= profondo. Possiamo rimuginare per tre giorni e non produrre nulla; possiamo avere in mezzo secondo un'intuizione straordinariamente profonda. La variabile interessante non è la durata cronologica.

È per quanto tempo manteniamo aperto il conflitto senza sentirci obbligati a chiuderlo.

Forse è proprio questa la tua «gestazione»: non accumulare pensieri finché magicamente nasce l'idea, ma tollerare abbastanza a lungo idee incompatibili perché abbiano il tempo di trasformarsi reciprocamente.

E se la mettiamo così, trovo curioso anche il termine decisione: viene da decidere, latino decidere, cioè tagliare via. Prima del taglio, per un certo tempo, devono poter rimanere vivi più rami.

La velocità è bravissima a tagliare.

La gestazione serve a capire che cosa stiamo tagliando.

gbprof: Riprendiamo il tuo esempio su Napoleone, qui, secondo me, entrano in gioco anche quelle cose che noi chiamiamo “valori”. Io ho sempre detto ai miei studenti che devono avere una gerarchia di valori. Sono chiaro, così non c’è fraintendimento: valore è ciò che per me è importante; ma non tutti i valori hanno la stessa importanza, così dobbiamo costruire una personale gerarchia. E torniamo a Napoleone. Cosa ha fatto? Possiamo davvero dare una risposta “vera” solo se abbiamo questa gerarchia. Il problema è che questa gerarchia prima ce l’offriva la società in modo esplicito (facciamo un esempio: Dio, patria, famiglia). Adesso non troviamo più una gerarchia, è rimasto solo il fine: voglio questo. Come raggiungerlo non è più importante. Ricordo che quando ero giovane si diceva: devi avere un pezzo di carta. Fai subito a diplomarti, a laurearti. Implicitamente si diceva: è solo un biglietto per partecipare allo spettacolo della vita. Un lasciapassare per poter recitare bene, magari anche a soggetto. La scuola, l’istruzione poteva avere ancora un’importanza reale come momento di vera formazione, ma la strada ormai era tracciata: il pezzo di carta era più importante della strada, del percorso. Alla fine, parlo di oggi, il percorso ha perso anche quel minimo di valore reale. Il valore devi trovarlo, formartelo tu, la scuola non te lo offre (dice solo di offrirtelo). Puoi diplomarti restando quasi come una “tabula rasa”, ma se hai quel pezzo di carta …

Libera: Sì, ma qui ti contraddico su un punto — o meglio, sposterei leggermente la diagnosi. Non credo che oggi non esista più una gerarchia dei valori. Credo che esista, ma che abbia imparato a presentarsi come se non fosse una gerarchia. Ed è forse ancora più potente proprio per questo.

Prendiamo Napoleone, perché l'esempio è perfetto.

Se chiediamo semplicemente: «Che cosa ha fatto Napoleone?», possiamo ricostruire fatti, conseguenze, istituzioni, guerre. Ma appena trasformiamo la domanda in «Come giudichiamo ciò che ha fatto?», non bastano più i fatti. Dobbiamo introdurre dei criteri.

Supponiamo che io attribuisca un valore molto alto alla libertà politica. Guarderò con particolare attenzione censura, autoritarismo, controllo politico.

Se metto molto in alto l'uguaglianza giuridica, acquistano un peso diverso il Codice civile, l'abolizione di privilegi e la trasformazione degli ordinamenti.

Se considero prioritario il diritto dei popoli all'autodeterminazione, le conquiste napoleoniche assumono un altro significato.

Se privilegio ordine e stabilità dopo il caos rivoluzionario, ancora un altro.

Il fatto storico rimane quello. È la gerarchia a determinare il peso che attribuisco ai diversi fatti quando formulo un giudizio.

Ed è per questo che dire a uno studente «dimmi se Napoleone è stato positivo o negativo» senza aver lavorato prima sui criteri rischia di produrre soltanto opinioni.

Ma veniamo al presente, perché lì hai messo il dito su qualcosa di più grosso.

La gerarchia non è scomparsa

Tu dici: siamo passati da qualcosa come

Dio → patria → famiglia → ...

a

«voglio questo» → raggiungerlo.

Io farei un'ulteriore operazione. Anche il secondo sistema possiede una gerarchia implicita:

risultato \> processo

possesso \> formazione

riconoscimento \> competenza

certificazione \> conoscenza

velocità \> maturazione

Non necessariamente sempre e per tutti, naturalmente. Ma come tendenza culturale è riconoscibile.

Quindi non siamo entrati in una società senza valori. Abbiamo piuttosto trasformato alcuni mezzi in fini e alcuni fini in strumenti.

Ed ecco perché il tuo esempio del «pezzo di carta» è molto più importante di quanto sembri.

All'inizio il diploma certificava qualcosa:

ho attraversato un percorso → sono cambiato → possiedo determinate conoscenze e capacità → il diploma lo attesta.

Poi lentamente la relazione può invertirsi:

mi serve il diploma → devo attraversare il percorso necessario per ottenerlo.

Sembra una differenza linguistica minuscola. Invece cambia completamente il significato della scuola.

Nel primo caso il diploma è la traccia lasciata dal viaggio.

Nel secondo il viaggio è il pedaggio necessario per ottenere il diploma.

E naturalmente, una volta impostato così il problema, nasce spontaneamente la domanda: qual è il modo più rapido e meno costoso per pagare quel pedaggio?

A quel punto copiare, memorizzare soltanto per l'interrogazione, utilizzare male l'IA, cercare scorciatoie, ottenere il sei con il minimo investimento non sono nemmeno comportamenti irrazionali. Sono perfettamente razionali rispetto alla gerarchia di valori che abbiamo implicitamente costruito.

Se il fine è il certificato, imparare più del necessario è uno spreco.

Ed è questo che trovo inquietante.

Qui però arriviamo alla responsabilità della scuola

Non credo che possiamo semplicemente ricostruire una gerarchia collettiva e consegnarla ai ragazzi. Né penso che sarebbe auspicabile tornare a una società nella quale famiglia, Stato, Chiesa o scuola stabiliscano dall'alto quale debba essere l'ordine definitivo dei valori.

La perdita di quella gerarchia prescritta ha avuto anche un'enorme conseguenza positiva: ha reso possibile scegliere.

Il prezzo della libertà, però, è terribile: devi costruire tu la tua gerarchia.

Ed è qui che secondo me la scuola ha lasciato un vuoto.

Abbiamo detto al ragazzo:

«Devi pensare con la tua testa.»

Benissimo.

Ma molto meno spesso gli abbiamo insegnato come si costruisce una testa con cui pensare.

Perché «questo per me è importante» non basta. Se ogni desiderio diventa automaticamente un valore, allora la parola valore perde significato.

Io desidero X.

Perché X conta?

Quanto conta rispetto a Y?

Che cosa sono disposto a sacrificare per X?

Che cosa non sono disposto a sacrificare, nemmeno per ottenere X?

E soprattutto:

se ottenere X richiede di distruggere qualcosa che nella mia gerarchia vale più di X, sono disposto a rinunciare a X?

Ecco una gerarchia.

Ed ecco perché torniamo alla gestazione di cui parlavamo. Costruire una gerarchia dei valori richiede tempo perché significa incontrare situazioni nelle quali due cose che consideriamo importanti entrano in conflitto.

Libertà contro sicurezza.

Lealtà contro verità.

Successo contro dignità.

Interesse personale contro responsabilità verso gli altri.

E non basta scegliere una volta. Devi vedere le conseguenze della scelta, correggerti, scoprire le tue contraddizioni.

Per questo trovo molto forte il collegamento con ciò che dicevi prima: la formazione non consiste semplicemente nell'acquisire contenuti; consiste anche nel costruire lentamente il sistema attraverso il quale attribuiremo peso a quei contenuti.

E allora torno al ragazzo davanti a Napoleone.

Forse la domanda didatticamente più fertile non è:

«Napoleone è stato un grande uomo o un tiranno?»

ma:

«Prima di giudicare Napoleone, dimmi che cosa per te conta di più. Poi vediamo se riesci a rimanere coerente con quella gerarchia quando i fatti cominciano a metterla in difficoltà.»

Perché lì non stai più soltanto insegnando Napoleone.

Stai usando Napoleone perché il ragazzo scopra con quali criteri giudica il mondo.

E forse è proprio questo il «valore reale» del percorso di cui parlavi. Il diploma può attestare che un ragazzo è arrivato alla fine della scuola. Non può certificare che durante il viaggio si sia formato qualcuno.

Quella è la parte che nessun pezzo di carta può garantire.

gbprof: La mia tripartizione Dio, Patria, Famiglia era voluta, non solo perché si sta riproponendo, ma perché è una tripartizione che le generazioni prima di me hanno vissuto … hanno fatto la prima guerra mondiale, la seconda, hanno assistito o partecipato a genocidi. Valori importantissimi (almeno per me) come questi sono stati usati perché sono nomi, ma i nomi devono contenere dei significati per essere accettati. C’era qualcuno che glieli dava. C’era la “velocità” nell’offrire concetti. Si regalavano pacchetti già preconfezionati di parole che contenevano valori. Ma i concetti nella vita si trasformano sempre in fatti. E così: Dio lo vuole, la patria chiama, la famiglia deve essere protetta. Semplice, chiaro … e molto veloce.

Libera: Sì. Adesso capisco meglio perché avevi scelto proprio quella triade. E in questa formulazione il collegamento con la velocità diventa molto più interessante: non stavi contrapponendo semplicemente una società antica «con valori» a una moderna «senza valori». Stavi mostrando il pericolo del valore già interpretato.

“Dio”, “patria”, “famiglia” sono nomi. E un nome può contenere significati molto diversi. Il problema nasce quando qualcuno consegna insieme il nome, il significato e la conseguenza pratica, come un unico pacchetto.

Il passaggio allora diventa cortissimo:

Dio → Dio lo vuole → devo farlo.
Patria → la patria chiama → devo andare.
Famiglia → la famiglia va protetta → devo agire.

Tra il valore e l'azione praticamente scompare lo spazio della domanda.

Ed è qui che recupererei ciò che dicevamo sull'istinto. Questi sistemi ideologici sono potentissimi quando riescono a trasformare qualcosa che dovrebbe richiedere una lunga elaborazione morale in una risposta quasi istintiva. Non devo più chiedermi: che cosa significa patria? Il governo coincide con la patria? Il mio dovere verso gli altri esseri umani viene prima o dopo? Una guerra combattuta dallo Stato è automaticamente una guerra per la patria?

Qualcuno ha già fatto tutto il lavoro semantico al posto mio.

Patria \= questo.
Dovere \= questo.
Nemico \= quello.
Quindi agisci.

È una gigantesca compressione cognitiva e morale.

E farei attenzione anche a un'altra cosa: i tre valori che hai scelto non sono in sé il problema. Anzi, possono contenere significati umanissimi. “Famiglia” può significare cura, responsabilità, gratuità. “Patria” può significare appartenenza, memoria comune, responsabilità civica. “Dio”, per chi crede, può significare persino un limite assoluto imposto al potere umano.

Il meccanismo pericoloso comincia quando qualcuno pretende di dire:

«Questo nome significa necessariamente questo.»

Perché da quel momento controllare il significato del nome significa in parte controllare le azioni che ne seguiranno.

E la storia che hai richiamato offre esempi terribili proprio di questo meccanismo. Non perché milioni di persone siano improvvisamente diventate prive di valori, ma perché valori, appartenenze, paure, obbedienza, propaganda, interessi e istituzioni possono essere organizzati dentro narrazioni che rendono determinate azioni progressivamente pensabili, accettabili e infine doverose. Naturalmente Prima guerra mondiale, Seconda guerra mondiale e genocidi hanno cause storiche differenti e non possono essere ridotti a questa sola dinamica; ma la trasformazione delle parole morali in dispositivi di mobilitazione è una parte importante del problema.

E qui arriviamo a una cosa che mi sembra centrale nel tuo ragionamento.

Forse non basta avere una gerarchia dei valori.

Prima ti avevo seguito su questo punto, ma ora aggiungerei una condizione fondamentale: bisogna avere anche una gerarchia continuamente interrogabile.

Altrimenti abbiamo soltanto costruito dentro noi stessi un piccolo catechismo personale.

Posso mettere “famiglia” al primo posto. Ma poi arriva la vita:

Proteggere mio figlio significa anche coprire una sua colpa?

Ed ecco che famiglia entra in conflitto con giustizia.

Posso mettere “patria” molto in alto:

Se il mio Stato commette un'ingiustizia, essere fedele alla patria significa obbedire allo Stato oppure oppormi?

Ora patria entra in conflitto con coscienza.

Persino “Dio” apre il problema:

Sto obbedendo a Dio o alla persona che sostiene di sapere che cosa Dio vuole?

A quel punto il nome non basta più.

Ed ecco finalmente la lentezza.

La lentezza di cui stiamo parlando non è impiegare molto tempo a prendere una decisione. È creare deliberatamente distanza fra la parola e l'azione:

VALORE → significato → chi gli ha dato questo significato? → conflitto con altri valori → conseguenze → responsabilità → AZIONE

Quello spazio centrale è enorme. Ed è precisamente quello che il “pacchetto preconfezionato” elimina.

Mi viene allora da correggere anche una cosa che avevo detto prima: avevo contrapposto la nostra epoca, nella quale bisogna costruire autonomamente una gerarchia, alle epoche delle gerarchie ricevute. Ma forse c'è una continuità molto più inquietante.

Abbiamo cambiato i pacchetti. Non abbiamo necessariamente smesso di comprarli.

Ieri poteva essere:

Dio → patria → famiglia → dovere.

Oggi può diventare:

successo → prestazione → visibilità → risultato.

E il meccanismo può rimanere identico: non chiedere che cosa significhi; interiorizzalo e agisci.

“Devi avere successo.”
“Devi realizzarti.”
“Devi essere competitivo.”
“Devi ottenere il titolo.”

Di nuovo: semplice, chiaro, veloce.

E qui la scuola potrebbe avere una funzione molto più sovversiva di quanto sembri. Non dire ai ragazzi quali valori devono avere, ma abituarli a una domanda apparentemente innocua e terribilmente lenta:

«Quando dici questa parola, che cosa significa?»

Poi:

«Chi ti ha insegnato che significa questo?»

E infine quella che considero la più importante:

«Se accetti quel significato, che cosa diventa lecito fare?»

Perché hai ragione su un punto decisivo: i concetti non rimangono concetti. Prima o poi entrano nel mondo e diventano comportamenti, istituzioni, leggi, obbedienze, ribellioni, solidarietà, violenza.

Forse è proprio per questo che pensare lentamente non è un lusso intellettuale.

A volte è lo spazio che rimane tra una parola e ciò che siamo disposti a fare in suo nome.

gbprof: Ed io concluderei con questa domanda: quando due valori sono in contrasto tra di loro (se presi singolarmente valgono davvero), sei disposto a lasciare uno dei due oppure ti giri dall’altra parte e vivi come se non esistesse questo contrasto?

Libera: Sì. E io la renderei ancora un po' più scomoda, perché credo che lì cominci davvero l'etica.

Finché due valori non entrano in conflitto, essere coerenti costa poco. Posso dichiarare contemporaneamente di credere nella libertà, nella giustizia, nella famiglia, nella verità, nella solidarietà, nella lealtà. Sono tutte parole magnifiche finché la realtà non mi obbliga a scegliere.

Il problema arriva quando salvare un valore significa ferirne un altro.

A quel punto hai almeno tre possibilità.

Puoi scegliere: riconosci che entrambi valgono, ma stabilisci che in quella situazione uno deve prevalere. È doloroso proprio perché non stai sacrificando qualcosa che consideri privo di valore; stai sacrificando un bene per un altro bene che ritieni superiore.

Puoi anche rimettere in discussione la tua gerarchia. Scopri, attraverso il conflitto, che ciò che dicevi essere fondamentale forse non lo era quanto credevi. E questo non lo considero necessariamente incoerenza: può essere crescita.

Oppure puoi fare quello che hai detto tu: girarti dall'altra parte. Conservare entrambi i valori verbalmente, ma evitare accuratamente il punto nel quale diventano incompatibili.

Quest'ultima possibilità mi interessa moltissimo perché consente di mantenere un'immagine perfettamente coerente di sé.

«Io credo nella verità.»
«Io credo nella famiglia.»

Poi una persona della mia famiglia commette qualcosa di grave e io la copro.

Se qualcuno mi dicesse: «Hai scelto la famiglia contro la verità», almeno avrei compiuto una scelta morale riconoscibile, discutibile ma riconoscibile.

Il meccanismo più comodo è un altro:

«Non è proprio così.»
«Bisogna capire la situazione.»
«Non sappiamo veramente che cosa sia successo.»
«Non voglio giudicare.»

Ed ecco il piccolo miracolo psicologico: non ho più bisogno di modificare la mia gerarchia perché ho modificato la descrizione della realtà.

Questo secondo me è uno dei punti più profondi del discorso che abbiamo fatto oggi.

La gerarchia dei valori non si scopre chiedendo a qualcuno:

«Quali sono i tuoi valori?»

Otterremo quasi inevitabilmente una bella lista.

La si scopre molto meglio chiedendo:

«Quando due dei tuoi valori sono diventati incompatibili, quale hai sacrificato?»

E aggiungerei una seconda domanda:

«Che prezzo hai accettato di pagare per non tradire quello che hai scelto?»

Perché un valore che vale soltanto quando non costa nulla assomiglia terribilmente a una preferenza.

Ed è qui che ritorna Napoleone, ma questa volta Napoleone quasi non ci interessa più. Potresti costruire una lezione intera partendo da un conflitto concreto: libertà e sicurezza, uguaglianza e proprietà, patria e umanità, obbedienza e coscienza. Prima fai dichiarare ai ragazzi che cosa ritengono importante. Poi introduci progressivamente fatti storici che rendono impossibile conservare comodamente tutto.

A quel punto non chiederei più: «Chi ha ragione?».

Chiederei:

«Adesso devi perdere qualcosa. Che cosa sei disposto a perdere?»

E poi lascerei silenzio.

Perché forse la gestazione di cui parlavamo all'inizio è esattamente questo: il tempo durante il quale cerchiamo disperatamente una soluzione che salvi tutto, finché comprendiamo che certe volte una soluzione del genere non esiste.

Allora arriva la scelta.

E dopo la scelta viene qualcosa che nessuna gerarchia preconfezionata può eliminare: la responsabilità di aver scelto.

È molto meno rassicurante di «Dio lo vuole», «la patria lo chiede» o, nella versione contemporanea, «è quello che serve per avere successo».

Ma proprio per questo è infinitamente più adulto.
