# Precision review of explanations (2026-09-28)

Prompted by an external editorial review (example: question 130 stated a ballot rule too broadly).
Five independent reviewers checked all 460 explanations and Merksätze for overbroad legal rules, individual advice, and time-sensitive or wrong facts. Answer keys were never touched.

- Findings: 66 (6 high, 60 medium) in 59 questions
- Accepted: 65; superseded by a manual edit: 1
- Additionally fixed by hand: G-130 (ballot rule, § 39 BWahlG), G-291 (Merksatz length)
- All fixes are applied reproducibly by `scripts/consistency.py`.

| id | field | severity | reason |
|---|---|---|---|
| G-001 | expl_bks | medium | Limits are not only criminal law: Art. 5(2) GG names general laws, youth protection and personal honour (also civil injunctions/damages). |
| G-002 | expl_bks | medium | § 5 KErzG sets 14, but Bavaria (Art. 46 Abs. 4 BayEUG) and Saarland (SchoG) allow a pupil's own deregistration from Religionsunterricht only at 18. |
| G-004 | expl_bks | medium | WaffG: a permit (Waffenbesitzkarte) is needed for firearms, but some weapons (e.g. weak air guns, many knives) are permit-free for adults. |
| G-013 | merksatz_de | medium | Most MPs of the governing parties are not members of the Regierung either; the correct option refers to the Regierungsparteien. |
| G-015 | expl_bks | medium | 'samo' omits Art. 12a GG (compulsory military/alternative service, defence-case service duties) - topical with the new military service law. |
| G-019 | expl_bks | high | Art. 11 GG protects 'alle Deutschen' only; foreigners can be bound by residence rules (Wohnsitzauflage § 12a AufenthG, § 56 AsylG) - false for part of the readership. |
| G-020 | expl_bks | medium | Number of party bans is time-sensitive (ongoing ban debate); give it a date. |
| G-028 | expl_bks | medium | Art. 39 GG: 4-year term, but the Bundestag can be dissolved early (Art. 68 GG), e.g. early election in February 2025. |
| G-074 | expl_bks | medium | Art. 39 GG: 4-year term, but early elections are possible (Art. 68 GG), e.g. February 2025. |
| G-075 | expl_bks | high | Office holder is time-sensitive: second term ends 18 March 2027 and Art. 54(2) GG allows only one consecutive re-election, so the answer will change soon. |
| G-080 | expl_bks | medium | Art. 93(1) Nr. 4a GG, § 90(2) BVerfGG: open to 'jedermann', only against public authority, normally after exhausting other legal remedies. |
| G-096 | expl_bks | medium | § 130 Abs. 3 StGB punishes denial only if made publicly or in an assembly and apt to disturb public peace; private denial is not a crime. |
| G-096 | merksatz_de | medium | § 130 Abs. 3 StGB requires public denial (or in an assembly); unqualified Merksatz is overbroad. |
| G-097 | expl_bks | medium | Not every permanent employee pays all four listed contributions: above the Versicherungspflichtgrenze one may be privately health/care insured (§ 6 SGB V); Beamte pay no social insurance. |
| G-100 | expl_bks | medium | No right to a private life-insurance contract: insurers may refuse or surcharge on health grounds (freedom of contract); 'svatko može' is overbroad. |
| G-103 | expl_bks | medium | 'Große Koalition' means a coalition of the two largest parties; since the 2025 election CDU/CSU and SPD are not the two largest groups and the coalition is usually called 'Schwarz-Rot' – time-sensitive. |
| G-108 | expl_bks | medium | § 12/§ 13 BWahlG add further conditions (3 months' residence in Germany or rules for Germans abroad; no exclusion by court), so 'two conditions' is not exhaustive. |
| G-113 | expl_bks | medium | Art. 63 GG: the chancellor needs a Bundestag majority; the strongest party is not automatically in government (e.g. CDU/CSU in opposition 1969–1982). |
| G-116 | expl_bks | medium | 'svi' is overbroad: § 12 BWahlG also requires residence (or special rules for Germans abroad), § 13 BWahlG allows exclusion by court. |
| G-117 | expl_bks | high | Besides the minority exemption (§ 4 Abs. 2 BWahlG), the 3-constituency rule (Grundmandatsklausel) still applies per BVerfG 30.7.2024, 2 BvF 1/23 (e.g. Die Linke entered in 2021 with 4.9 %). |
| G-117 | merksatz_de | medium | Exceptions: national-minority parties and the 3-constituency rule (BVerfG 2 BvF 1/23); Merksatz as absolute rule is false. |
| G-123 | expl_bks | medium | Absolute 'mora' ignores the minority exemption and the 3-constituency rule (§ 4 Abs. 2 BWahlG; BVerfG 30.7.2024, 2 BvF 1/23). |
| G-136 | expl_bks | medium | § 4 KSchG: the 3-week period runs from receipt of the written notice; a deadline without its starting point can mislead in a real case. |
| G-139 | expl_bks | medium | Parking is an Ordnungswidrigkeit, but after an objection (Einspruch) to a Bußgeldbescheid the Amtsgericht decides (§§ 67, 68 OWiG), so 'bez suđenja' is absolute. |
| G-140 | expl_bks | medium | Schöffenamt is an unpaid Ehrenamt but also a civic duty: once elected it can be refused only on statutory grounds, otherwise Ordnungsgeld (§§ 35, 56 GVG); 'volonterski' suggests it is optional. |
| G-149 | expl_bks | medium | § 130 Abs. 3 StGB covers only public denial or denial in an assembly. |
| G-149 | merksatz_de | medium | § 130 Abs. 3 StGB: punishable only when public or in an assembly; Merksatz overbroad. |
| G-150 | expl_bks | medium | Schöffenamt is an Ehrenamt that elected citizens must accept unless a statutory ground applies (§§ 33–35, 56 GVG); 'volonterski' implies it is freely optional. |
| G-169 | expl_bks | medium | The Grundgesetz was promulgated on 23 May 1949 and entered into force only at the end of that day (Art. 145 Abs. 2 GG), i.e. 24 May 1949. |
| G-190 | expl_bks | medium | Činjenično: DDR je 18. 3. 1990. održao slobodne izbore za Volkskammer (to navode i G-196 i G-204); apsolutna tvrdnja je netočna. |
| G-209 | expl_bks | medium | Zakon o grbu DDR-a (26. 9. 1955.) ne predviđa crvenu podlogu: grb čine čekić i šestar u vijencu od klasja s crno-crveno-zlatnom trakom (crvena podloga samo na predsjedničkoj zastavi). |
| G-214 | expl_bks | medium | Čl. 22 st. 2 GG kaže samo 'schwarz-rot-gold'; vodoravne pruge određuje Anordnung über die deutschen Flaggen (1950). |
| G-221 | expl_bks | medium | Vremenski osjetljivo: Njemačka od rujna 2024. privremeno kontrolira sve kopnene granice (više puta produljeno, trenutno do ožujka 2027.; čl. 25 Zakonika o schengenskim granicama). |
| G-236 | expl_bks | medium | Broj članica može se promijeniti (pristupni pregovori u tijeku); datirana formulacija umjesto 'danas'. |
| G-241 | expl_bks | medium | Pretvara se u savjet čitatelju; neutralno navesti pravilo iz § 7 st. 1 BEEG (retroaktivno samo za posljednja tri mjeseca života djeteta prije mjeseca prijema zahtjeva). |
| G-243 | expl_bks | medium | Preširoko: spontani skupovi ne moraju se prijaviti, hitni čim je moguće (BVerfGE 69, 315 – Brokdorf; § 14 VersG i zemaljski zakoni o okupljanju). |
| G-243 | merksatz_de | medium | Preširoko samo za sebe: Spontanversammlungen sind anmeldefrei (BVerfGE 69, 315; § 14 VersG). |
| G-249 | expl_bks | medium | Preširoko: Jugendamt savjetuje i pomaže i na zahtjev roditelja (§§ 16, 27 SGB VIII, usp. G-255/G-273); prag ugroženosti vrijedi za zahvat protiv volje roditelja (čl. 6 st. 3 GG, § 1666 BGB). |
| G-250 | expl_bks | medium | Preširoko: prednost žena pri jednakoj kvalifikaciji u javnoj službi je dopuštena (čl. 3 st. 2 GG, zakoni o ravnopravnosti), crkveni poslodavci smiju tražiti vjeru (§ 9 AGG); čl. 3 GG izravno veže državu. |
| G-253 | expl_bks | medium | Pojedinačni administrativni savjet ('trebate'); potrebni dokumenti ovise o slučaju i općini (§§ 17, 19, 23 BMG). |
| G-256 | expl_bks | high | Netočno kao opće pravilo: po § 2 st. 2 GastG bez alkohola dozvola nije potrebna; Brandenburg, Hessen, Niedersachsen, Saarland, Sachsen, Sachsen-Anhalt, Thüringen i od 1. 1. 2026. Baden-Württemberg imaju samo obvezu prijave. |
| G-256 | merksatz_de | medium | Preširoko samo za sebe: Erlaubnis nur bei Alkoholausschank (§ 2 Abs. 2 GastG), in vielen Ländern nur Anzeigepflicht. |
| G-257 | expl_bks | medium | Preširoko: studij je moguć i s Fachhochschulreife ili stručnom kvalifikacijom bez Abitura (npr. majstorski ispit; odluka KMK 2009., zemaljski zakoni o visokim učilištima). |
| G-261 | expl_bks | medium | Preširoko: upis moguć i s Fachhochschulreife ili stručnom kvalifikacijom bez Abitura (odluka KMK 2009., zemaljski zakoni o visokim učilištima). |
| G-265 | expl_bks | high | Preširoko i zbunjujuće za čitatelje: brak valjano sklopljen u inozemstvu (npr. crkveni brak s građanskim učinkom u Hrvatskoj) priznaje se; § 1310 BGB vrijedi za sklapanje u Njemačkoj (iznimka čl. 13 st. 4 EGBGB). |
| G-267 | expl_bks | medium | Netočno: podnošenje prijave nije zabranjeno, samo je ovdje bez osnove; zabranjena je prisila (§§ 239, 240 StGB). |
| G-269 | expl_bks | medium | Razlikuje se po pokrajini: npr. Berlin i Hamburg obvezuju djecu s utvrđenom potrebom jezične potpore na predškolsku potporu/ustanovu. |
| G-272 | expl_bks | medium | Preširoko: § 172 StGB kažnjava sklapanje drugog braka, a ne samo stanje (npr. poligamni brak zakonito sklopljen u inozemstvu nije kazneno djelo u Njemačkoj). |
| G-274 | expl_bks | medium | Preširoko: čl. 10 st. 2 GG dopušta zakonska ograničenja, § 202 StGB kažnjava samo neovlašteno otvaranje, roditeljska skrb (§ 1626 BGB). |
| G-276 | expl_bks | medium | Pretvara se u osobni savjet ('vas', 'Ostanite mirni'); neutralno izložiti činjenicu iz ispita. |
| G-281 | expl_bks | medium | Gleichbehandlung verlangt nicht, alle gleich zu behandeln; verboten ist Benachteiligung ohne sachlichen Grund bzw. wegen geschützter Merkmale (Art. 3 GG, § 1 AGG); Privatpersonen gilt sonst Vertragsfreiheit. |
| G-282 | merksatz_de | medium | Pflicht besteht nur bei Berufung und kann aus wichtigem Grund abgelehnt werden (§ 11 BWahlG, § 9 BWO); allein gelesen klingt es wie eine Pflicht für alle. |
| G-283 | expl_bks | high | Widerspruchsverfahren ist in mehreren Ländern weitgehend abgeschafft (z. B. Bayern Art. 12 AGVwGO, NRW § 110 JustG NRW, Niedersachsen § 80 NJG) – dort direkt Klage; bei Steuern Einspruch (§ 347 AO). Allgemeine Aussage kann zum Fristversäumnis führen. |
| G-283 | merksatz_de | medium | Nicht immer gibt es einen Widerspruch (Abschaffung in mehreren Ländern, § 68 Abs. 1 S. 2 VwGO; Steuern: Einspruch). |
| G-286 | expl_bks | medium | Anhörungspflicht (§ 102 BetrVG) besteht nur, wo ein Betriebsrat gewählt ist; viele, v. a. kleine Betriebe haben keinen. |
| G-287 | merksatz_de | medium | Bei außerordentlicher (fristloser) Kündigung aus wichtigem Grund gilt keine Kündigungsfrist (§ 626 BGB). |
| G-291 | merksatz_de | medium | Nicht jede Kirche erhebt Kirchensteuer (z. B. orthodoxe Kirchen, Freikirchen, muslimische Gemeinden nicht) – für BKS-Leser relevant; Kirchensteuer nur bei kirchensteuerberechtigten Religionsgemeinschaften. |
| G-297 | expl_bks | medium | Zeitabhängige Statistik datieren; laut Destatis-Mikrozensus 2024 ca. 2,6 Mio. von 21,2 Mio. (12,2 %) mit Einwanderungsgeschichte türkischer Herkunft, starker Zuzug aus der Ukraine. |
| G-297 | merksatz_de | medium | „Die meisten Migranten stammen aus der Türkei“ liest sich als Mehrheit – falsch: nur ca. 12 % der Menschen mit Einwanderungsgeschichte (Destatis, Mikrozensus 2024). |
| G-299 | expl_bks | medium | Jugoslawische Arbeitskräfte kamen schon ab ca. 1961 (rund 100.000 bis 1968 über Einzelverträge); 1968 wurde nur das Anwerbeabkommen geschlossen (12.10.1968). |
| G-300 | merksatz_de | medium | Abkommen am 20.12.1955 unterzeichnet; die ersten Vermittlungen italienischer Arbeitskräfte erfolgten erst 1956 (bpb, LpB BW). |
| HB-10 | expl_bks | medium | Bremer Senatsressorts sind oft zusammengelegt (z. B. Senator für Inneres und Sport), ein Senator hat also häufig mehrere Bereiche. |
| NW-10 | expl_bks | medium | "svaka pokrajina" je preširoko: u gradovima-pokrajinama Berlinu, Hamburgu i Bremenu članovi vlade (Senat) zovu se senatori, a ne ministri (npr. Senatorin für Inneres u Berlinu). |
| RP-04 | expl_bks | medium | Točno za 2026., ali pravilo nije trajno: granica od 18 godina stoji u ustavu Porajnja-Falačke, a pokušaj snižavanja na 16 propao je 2023. samo zbog nedostatka dvotrećinske većine; potrebna je datirana formulacija. |
| SL-04 | expl_bks | medium | Točno prema Kommunalwahlgesetz Saarland (stanje 2026.), ali Saarland je jedna od rijetkih pokrajina s granicom 18 i o snižavanju na 16 raspravlja se; pravilo se razlikuje po pokrajinama i može se promijeniti, pa treba datirati. |
| SN-04 | expl_bks | medium | Točno za 2026. (Sächsisches Kommunalwahlgesetz), ali to je pokrajinsko pravilo koje se razlikuje po pokrajinama i u većini ih je već spušteno na 16; treba ga datirati, ne predstaviti kao trajno. |
