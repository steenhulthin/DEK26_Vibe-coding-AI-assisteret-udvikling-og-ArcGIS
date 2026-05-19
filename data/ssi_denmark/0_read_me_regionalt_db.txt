Her finder du en beskrivelse af indeholdet af det regionale dashboard, herunder 
beskrivelser af tabellerne med tilhørende variabelnavne (søjlenavne).

Opdateret: 2023-04-26

NOTE 10. FEBRUAR 2022: Fra og med denne dag inkluderer alle opgørelser reinfektioner. I denne forbindelse omnavngives "bekræftede tilfælde" til "første infektion".

Forkortelser:
_______________________________________________________________________________
TCD = Test Center Danmark (Statens Serum Institut)
KMA = Klinisk Mikrobiologisk Afdeling (hospitaler)


Generel struktur:
_______________________________________________________________________________
Rækkerne i filerne er som udgangspunkt opdelt efter relevante 
parametre, eksempelvis aldersgruppering eller tidsopdeling. 
Der opdeles generelt efter variablen i første søjle. 
Enkelte tabeller kan have rækker, som afviger fra dette mønster. 
I disse tabeller specificeres dette i "Noter" under tabellens 
variabelbeskrivelse. Filerne er kommaseparerede.

Definitioner: 
_______________________________________________________________________________
Definitioner der benyttes i dette og datafilerne er beskrevet på SSI's COVID-19-
side under Datakilder og definitioner. 
https://covid19.ssi.dk/datakilder-og-definitioner
Den 8. december 2021 ændredes definitionen af "seneste 7 dage". 

Opdateringer:
_______________________________________________________________________________
Filerne bliver opdateret ugentlig om onsdagen. I den forbindelse kan tidsserier også 
ændre sig tilbage i tiden, hvis nyere data foreligger. Derfor anbefales det 
altid at benytte det senest tilgængelige data og for så vidt muligt, 
ikke at gemme filer og lave tidsserier på basis af gamle filer.

Typer af tests:
_________________________________________________________________________
Filerne baseres primært på PCR-opgørelser, medmindre andet er angivet. 
PCR-tests og antigentests bruges til hhv. at bekræfte eller mistænke covid-19-
smitte under et aktivt sygdomsforløb. 
Begreberne "PCR-prøver" og "PCR-test" betyder det samme og refererer til
antallet af podninger. Det samme gælder for begreberne "antigentest" og 
"antigenprøver".
Data indeholder ikke serologitest, som er den test, der udføres, 
når man skal undersøge, om raske mennesker tidligere har haft covid-19.

Filerne:
_______________________________________________________________________________


03_bekraeftede tilfaelde_doede_indlagte_pr_dag_pr_koen
-------------------------------------------------------------------------------
Dette er en opgørelse over antallet af bekræftede tilfælde i alt og døde pr. dag
fordelt på bopælsregioner og køn.

Regionskode: Regionskoden for regionen
Region: Bopælsregion (region man boede i ved prøvetagning)		
Dato: Dato for prøvetagning og eventuel indlæggelsesdag
Køn: Mænd og kvinder 
Bekræftede tilfælde i alt: Antallet af bekræftede tilfælde i alt
Døde: Antallet af covid-19-relaterede dødsfald (30 dags mortalitet)
Indlæggelser: Antallet af indlæggelser
Kumuleret antal døde: Alle dødsfald fra pandemiens start til den aktuelle dag
Kumuleret antal bekræftede tilfælde: Alle bekræftede tilfælde fra pandemiens start til den aktuelle dag
Kumuleret antal indlæggelser: Alle indlæggelser fra pandemiens start til den aktuelle dag
timestamp: tidsstempel for dataoprettelse i headeren

04_indlagte_pr_alders_grp_pr_region
-------------------------------------------------------------------------------
Dette er en opgørelse over antallet af indlagte pr. aldersgruppe pr. region.
Bemærk at blanke felter under variablen <Region> udgør de danskere,
som ikke har en tildelt bopælsregion.

Regionkode: Regionskoden for regionen
Region: Bopælsregion (region man boede i ved indlæggelsen)
Aldersgruppe: Den aldersgruppe en person tilhørte ved prøvetagningen
Indlæggelser: Kumulerede antal indlæggelser
timestamp: tidsstempel for dataoprettelse i headeren

05_bekraeftede_tilfaelde_doede_pr_region_pr_alders_grp
-------------------------------------------------------------------------------
Dette er en opgørelse over antallet af bekræftede tilfælde i alt og døde pr. region 
og pr. aldergruppe. Bemærk at blanke felter under variablen <Region> 
udgør de danskere, som ikke har en tildelt bopælsregion.

Regionkode: Regionskoden for regionen
Region: Bopælsregion (region man boede i ved prøvetagningen)
Aldersgruppe: Den aldersgruppe en person tilhørte ved prøvetagningen
Bekræftede tilfælde i alt: Kumulerede antal bekræftede tilælde i alt
Døde: Kumulerede antal af covid-19-relaterede dødsfald (30 dags mortalitet)
timestamp: tidsstempel for dataoprettelse i headeren

06_nye_indlaeggelser_pr_region_pr_dag
-------------------------------------------------------------------------------
Dette er en opgørelse over antallet af nye indlæggelser pr. region pr. dag.

Regionkode: Regionskoden for regionen
Region: Bopælsregion (region man boede i ved indlæggelsen)		
Dato: Dato for indlæggelsen
Indlæggelser: Antallet af indlæggelser på en given dag i en given region
timestamp: tidsstempel for dataoprettelse i headeren

07_antal_doede_pr_dag_pr_region
-------------------------------------------------------------------------------
Dette er en opgørelse over antallet af døde pr. region pr. dag. 
Bemærk at blanke felter under variablen <Region> udgør de danskere, 
som ikke har en tildelt bopælsregion.

Region: Bopælsregion (region man boede i ved prøvetagningen)
Dato: Dato for covid-19-relaterede dødsfald (30 dags mortalitet) registreret i Dødsårsagsregisteret
Kumulerede antal døde: Kumulerede antal af covid-19-relaterede dødsfald (30 dags mortalitet) siden pandemiens start
timestamp: tidsstempel for dataoprettelse i headeren

08_bekraeftede_tilfaelde_pr_dag_pr_regions
-------------------------------------------------------------------------------
Dette er en opgørelse over antallet af bekræftede tilfælde i alt pr. region pr.
dag siden pandemiens start.

Regionkode: Regionskoden for regionen
Region: Bopælsregion (region man boede i ved prøvetagningen)
Dato: Dato for covid-19-relaterede dødsfald (30 dags mortalitet) registreret i Dødsårsagsregisteret
Bekræftede tilfælde i alt: Antallet af bekræftede tilfælde i alt
timestamp: tidsstempel for dataoprettelse i headeren

11_noegletal_pr_region_pr_aldersgruppe
-------------------------------------------------------------------------------
Dette er en opgørelse af antallet af bekræftede tilfælde i alt, døde, indlagte, herunder på intensiv 
afdeling opgjort pr. region og pr. aldersgruppe.

Regionkode: Regionskoden for Bopælsregionen 
Region: Bopælsregion (region man boede i ved prøvetagningen)
Aldersgruppe: Den  aldersgruppe en person tilhørte ved prøvetagningen
Bekræftede tilfælde i alt: Antallet af bekræftede tilfælde i alt
Døde: Antallet af covid-19-relaterede dødsfald (30 dags mortalitet)
Indlæggelser: Antallet af indlagte
timestamp: tidsstempel for dataoprettelse i headeren

12_noegletal_pr_region_pr_aldersgruppe_de_seneste_7_dage
-------------------------------------------------------------------------------
Dette er en opgørelse af antallet af bekræftede tilfælde i alt, døde, indlagte,
herunder på intensiv afdeling opgjort pr. region og pr. aldersgruppe de seneste 7 dage.

Regionkode: Regionskoden for regionen
Region: Bopælsregion (region man boede i ved prøvetagningen)
Aldersgruppe: Den aldersgruppe en person tilhørte ved prøvetagningen
Bekræftede tilfælde i alt: Antallet af bekræftede tilfælde i alt
Døde: Antallet af covid-19-relaterede dødsfald (30 dags mortalitet)
Indlæggelser: Antallet af indlagte
timestamp: tidsstempel for dataoprettelse i headeren

13_regionale_kort
-------------------------------------------------------------------------------
Dette er en opgørelse af antallet af bekræftede tilfælde, incidensen, bekræftede
tilfælde de seneste 7 dage, incidensen de seneste 7 dage, PCR-testede personer,
PCR-testede pr. 100.000 borgere, PCR-testede de seneste 7 dage, PCR-testede pr. 
100.000 borgere de seneste 7 dage, samt positivprocenten de seneste 7 dage, opgjort pr. region. 
Læs mere om opgørelsesmetoden for de seneste 7 dage under "Definitioner og datakilder" på 
https://covid19.ssi.dk/datakilder-og-definitioner.

Region: Bopælsregion (region man boede i ved prøvetagningen)
Bekræftede tilfælde i alt: Antallet af bekræftede tilfælde i alt siden pandemiens start
Incidensen: Antallet af bekræftede tilfælde i alt pr. 100.000 borgere
Bekræftede tilfælde i alt de seneste 7 dage: Antallet af bekræftede tilfælde i alt de seneste 7 dage
Incidensen de seneste 7 dage: Antallet af bekræftede tilfælde i alt pr. 100.000 borgere de seneste 7 dage
Testede: Antallet af PCR-testede personer siden pandemiens start
Testede pr. 100.000 borgere: Antallet af PCR-testede pr. 100.000 borgere
Testede de seneste 7 dage: Antallet af PCR-testede personer de seneste 7 dage 
Testede pr. 100.000 borgere de seneste 7 dage: Antallet af PCR-testede pr. 100.000 borgere de seneste 7 dage
Positivprocent de seneste 7 dage: (antal covid-19-bekræftede personer i alt /antallet af PCR-testede personer) *100 for de seneste 7 dage
timestamp: tidsstempel for dataoprettelse i headeren

16_pcr_og_antigen_test_pr_region
-------------------------------------------------------------------------------
Uge: Årstal og ugenummer
Regionkode: Regionskoden for regionen
Region: Regionsnavn
Prøver: Antal prøver foretaget
Metode: Prøvetagningsmetode (Antigen eller PCR)
timestamp: tidsstempel for dataoprettelse i headeren

Note: Der forekommer rækker uden Regionsnavn. Det kan fx forekomme, hvis testede personer har et CPR-nummer, men ikke er bosat i Danmark. 

17_koen_uge_testede_positive_nye_indlaeggelser
-------------------------------------------------------------------------------
Dette er en opgørelse over testede, positivtestede og nye indlæggelser, angivet i antal personer pr. 100.000 personer.
Alle tre nøgletal er angivet på ugebasis og opdelt efter køn.

Uge: Den uge testen er blevet taget eller nyindlæggelsen er forekommet
Køn: M = Mænd, K = Kvinder
Testede pr. 100.000 borgere: Antal testede personer pr. 100.000 borgere i den pågældende uge
Positive pr. 100.000 borgere: Antal personer med positive tests pr. 100.000 borgere i den pågældende uge
Nye indlæggelser pr. 100.000 borgere: Antal nye indlæggelser pr. 100.000 borgere i den pågældende uge
timestamp: tidsstempel for dataoprettelse i headeren

18_fnkt_alder_uge_testede_positive_nye_indlaeggelser | OBS 5. oktober 2021: Se note i bunden af denne fil
-------------------------------------------------------------------------------
Dette er en opgørelse over testede, positivtestede og nye indlæggelser, angivet i antal personer pr. 100.000 personer.
Alle tre nøgletal er angivet på ugebasis og opdelt efter funktionelle aldersgrupper.

Uge: Den uge testen er blevet taget eller nyindlæggelsen er forekommet
Aldersgruppe: Aldersgruppe
Testede pr. 100.000 borgere: Antal testede personer pr. 100.000 borgere i den pågældende uge
Positive pr. 100.000 borgere: Antal personer med positive tests pr. 100.000 borgere i den pågældende uge
Positiv procent: (antal personer med positive tests/total antal tests) fordelt på aldersgrupper i den pågældende uge
Nye indlæggelser pr. 100.000 borgere: Antal nye indlæggelser pr. 100.000 borgere i den pågældende uge
Antal testede: Antal udført tests
Antal positive: Antal positive tests
timestamp: tidsstempel for dataoprettelse i headeren

19_indlagte_pr_fnkt_alder_pr_region
-------------------------------------------------------------------------------
Dette er en opgørelse over antallet af indlagte pr. aldersgruppe pr. region.
Bemærk at blanke felter under variablen <Region> udgør de danskere,
som ikke har en tildelt bopælsregion.

Regionkode: Regionskoden for regionen
Region: Bopælsregion (region man boede i ved indlæggelsen)
Aldersgruppe: Den aldersgruppe en person tilhørte ved prøvetagningen
Indlæggelser: Kumulerede antal indlæggelser
timestamp: tidsstempel for dataoprettelse i headeren

20_bekraeftede_tilfaelde_pr_region_pr_fnkt_alder
-------------------------------------------------------------------------------
Dette er en opgørelse over antallet af bekræftede tilfælde i alt pr. region 
og pr. aldergruppe. Bemærk at blanke felter under variablen <Region> 
udgør de danskere, som ikke har en tildelt bopælsregion.

Regionkode: Regionskoden for regionen
Region: Bopælsregion (region man boede i ved prøvetagningen)
Aldersgruppe: Den aldersgruppe en person tilhørte ved prøvetagningen
Bekræftede tilfælde i alt: Kumulerede antal bekræftede tilfælde i alt
timestamp: tidsstempel for dataoprettelse i headeren

21_noegletal_pr_region_pr_fnkt_alder
-------------------------------------------------------------------------------
Dette er en opgørelse af antallet af bekræftede tilfælde i alt, døde, indlagte, herunder på intensiv 
afdeling opgjort pr. region og pr. aldersgruppe.

Regionkode: Regionskoden for regionen
Region: Bopælsregion (region man boede i ved prøvetagningen)
Aldersgruppe: Den  aldersgruppe en person tilhørte ved prøvetagningen
Bekræftede tilfælde i alt: Antallet af bekræftede tilfælde i alt
Døde: Antallet af covid-19-relaterede dødsfald (30 dags mortalitet)
Indlæggelser: Antallet af indlagte
timestamp: tidsstempel for dataoprettelse i headeren

22_noegletal_pr_region_pr_fnkt_alder_de_seneste_7_dage
-------------------------------------------------------------------------------
Dette er en opgørelse af antallet af bekræftede tilfælde i alt, døde, indlagte,
herunder på intensiv afdeling opgjort pr. region og pr. aldersgruppe de seneste 7 dage.

Regionkode: Regionskoden for regionen
Region: Bopælsregion (region man boede i ved prøvetagningen)
Aldersgruppe: Den aldersgruppe en person tilhørte ved prøvetagningen
Bekræftede tilfælde i alt: Antallet af bekræftede tilfælde i alt
Døde: Antallet af covid-19-relaterede dødsfald (30 dags mortalitet)
Indlæggelser: Antallet af indlagte
timestamp: tidsstempel for dataoprettelse i headeren

23_reinfektioner_uge_region
-------------------------------------------------------------------------------
Uge: Den uge testen er blevet taget, hvor reinfektionen er forkommet.
Regionkode: Regionskoden for regionen
Region: Bopælsregion (region man boede i ved prøvetagningen)
Antal reinfektioner: Antallet af bekræftede reinfektioner
Reinfektioner pr. 100.000 borgere: Antal bekræftede reinfektioner pr. 100.000 borgere i den pågældende uge
Første reinfektion: Antallet af første reinfektioner
To eller flere reinfektioner: Antallet af to eller flere reinfektioner
timestamp: tidsstempel for dataoprettelse i headeren

24_reinfektioner_ugentlig_region
-------------------------------------------------------------------------------
Uge: Den uge testen er blevet taget, hvor reinfektionen er forkommet.
Regionkode: Regionskoden for regionen
Region: Bopælsregion (region man boede i ved prøvetagningen)
Antal tilfælde: Antallet af bekræftede tilfælde
Antal borgere: Antal personer i gruppen den pågældende måned
Type: Type af tilfælde
Type_count: Intern variable for at sortere type af tilfælde
timestamp: tidsstempel for dataoprettelse i headeren

27_indl_kategori_dag_region
-------------------------------------------------------------------------------
Denne opgørelse viser nye indlæggelser pr. dag og region, fordelt på følgende tre kategorier:
	1. Indlæggelse pga. covid-19.
	2. Indlæggelse, hvor covid-19 kan have spillet en rolle.
	3. Indlæggelse pga. andre forhold end covid-19.
Indlæggelserne drejer sig om personer, der indenfor 14 dage inden deres indlæggelse har fået en positiv PCR-test, eller har fået en positiv PCR-test under deres indlæggelse. Data i figuren er opgjort fra d. 1. juni 2020 og seneste opdatering vil være 14 dage før dags dato. Vær opmærksom på, at der mangler diagnosekoder for lidt over 1-2% af indlæggelser. Disse indlæggelser kan ikke klassificeres og er derfor ekskluderet fra disse opgørelser.
	
Dato: Dato for indlæggelsen
Regionkode: Regionskoden for regionen
Region: Bopælsregion (region man boede i på indlæggelsesdatoen)
Kategori: Se de tre kategorier ovenfor
Antal borgere: Antal indlagte i den givne kategori
timestamp: tidsstempel for dataoprettelse i headeren

28_plejehjem_ugeoversigt
-------------------------------------------------------------------------------
Denne fil indeholder en opgørelse over covid-19-tests og -tilfælde på danske plejehjem pr. uge siden uge 11 2020.
Denne opgørelse viser data for plejehjem summeret på ugeniveau. 

År: Årstal
Uge: Uge 
Bekræftede tilfælde beboere: Antal beboere på plejehjem, som er testet positiv for covid-19 med en PCR test inden for den givne uge. Alle personer tæller kun med med deres første positive test.
Dødsfald blandt bekræftede beboere: Antal beboere på plejehjem, som er døde i den givne uge, hvis det er inden for 30 dage, efter at de er testet positiv for covid-19 med en PCR-test for første gang. 
Plejehjem med bekræftede beboere: Antal plejehjem, hvor mindst én beboer er testet positiv for covid-19 med en PCR-test inden for den givne uge. Igen tæller kun beboernes første positive test.
Antal tests blandt beboere: Antal PCR-tests for covid-19 udført på beboere på plejehjem inden for den givne uge. Hver beboer kan tælle med flere gange. Beboere, som tidligere er testet positive, tæller fortsat med, hvis de bliver testet igen senere (uafhængigt af resultat).
Plejehjem med testede beboere: Antal plejehjem, hvor mindst én beboer er blevet PCR-testet for covid-19 inden for den givne uge.
timestamp: tidsstempel for dataoprettelse i headeren

Definition af reinfektion:
-------------------------------------------------------------------------------
Når en person modtager en positiv PCR-prøve tæller vedkommende som et bekræftet tilfælde. 
Hvis samme person 61 dage eller mere efter prøvetagningsdatoen for denne prøve modtager endnu en positiv PCR-prøve, 
vil vedkommende tælle med igen som en reinfektion. 
61 dage efter denne prøve er det muligt for samme person at blive reinficeret igen 
- bemærk at der ikke er krav om en negativ PCR-test mellem forskellige infektions-/reinfektionforløb, 
og at der ikke er nogen begrænsning på antallet af reinfektionsforløb én person kan have.