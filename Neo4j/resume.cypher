CREATE 
(Basliel: PERSON{name:"Basliel Amsalu", age: 22, email: "baslielamsalu@gmail.com", github: "https://github.com/Basliel-Amsalu", linkedin: "https://www.linkedin.com/in/basliel-amsalu-1a51a7298/"}),

(tvseries: HOBBIE{type: "Tv series"}),
(movie: HOBBIE{type: "Movie"}),
(anime: HOBBIE{type: "Anime"}),
(reading: HOBBIE{type: "Book"}),

(AAU: SCHOOL{name:"Addis Ababa University", location: "5 kilo" }),

(react: SKILL{name: "React"}),
(node: SKILL{name: "Node.js"}),
(next: SKILL{name: "Next.js"}),
(remix: SKILL{name: "Remix.js"}),
(tailwind: SKILL{name: "tailwindCSS"}),
(django: SKILL{name: "Django"}),
(mongodb: SKILL{name: "MongoDB"}),
(mysql: SKILL{name: "mysql"}),
(javascript: SKILL{name: "Javascript"}),
(typescript: SKILL{name: "Typescript"}),
(python: SKILL{name: "Python"}),

(english: LANGUAGE{name: "English"}),
(amharic: LANGUAGE{name: "Amharic"}),

(oeee: ORGANIZATION{name:"1888ec", location: "Bole, Atlas"}),

(proshop: PROJECT{name: "Proshop"}),
(ethiospare: PROJECT{name: "Ethiospare"}),

(Basliel) -[:HAS_HOBBIE]-> (tvseries),
(Basliel) -[:HAS_HOBBIE]-> (movie),
(Basliel) -[:HAS_HOBBIE]-> (anime),
(Basliel) -[:HAS_HOBBIE]-> (reading),

(Basliel) -[:HAS_SKILL{proficiency_level: "Professional Working Proficiency"}]-> (react),
(Basliel) -[:HAS_SKILL{proficiency_level: "Professional Working Proficiency"}]-> (node),
(Basliel) -[:HAS_SKILL{proficiency_level: "Professional Working Proficiency"}]-> (next),
(Basliel) -[:HAS_SKILL{proficiency_level: "Professional Working Proficiency"}]-> (remix),
(Basliel) -[:HAS_SKILL{proficiency_level: "Professional Working Proficiency"}]-> (tailwind),
(Basliel) -[:HAS_SKILL{proficiency_level: "Professional Working Proficiency"}]-> (django),
(Basliel) -[:HAS_SKILL{proficiency_level: "Professional Working Proficiency"}]-> (mongodb), 
(Basliel) -[:HAS_SKILL{proficiency_level: "Professional Working Proficiency"}]-> (mysql),
(Basliel) -[:HAS_SKILL{proficiency_level: "Professional Working Proficiency"}]-> (javascript),
(Basliel) -[:HAS_SKILL{proficiency_level: "Professional Working Proficiency"}]-> (typescript),
(Basliel) -[:HAS_SKILL{proficiency_level: "Professional Working Proficiency"}]-> (python),

(Basliel) -[:SPEAKS{proficiency_level: "Fluent"}]-> (english),
(Basliel) -[:SPEAKS{proficiency_level: "Native or Bilingual"}]-> (amharic),

(Basliel) -[:WORKED_AT{position: "Fullstack developer", duration: "Jan1 - April30, 2024"}]-> (oeee),

(Basliel) -[:LEARNED_AT{department: "Software Engineering", duration: "June21, 2021 - June30, 2025", grade: 3.6}]-> (AAU),

(Basliel) -[:WORKED_IN{type:"Organization project"}]-> (ethiospare),
(Basliel) -[:WORKED_IN{type:"Personal project"}]-> (proshop),

(oeee) -[:USES_TECH_STACK]-> (react),
(oeee) -[:USES_TECH_STACK]-> (remix),
(oeee) -[:USES_TECH_STACK]-> (tailwind),
(oeee) -[:USES_TECH_STACK]-> (node),

(ethiospare) -[:MADE_BY]-> (oeee),

(ethiospare) -[:BUILT_BY]-> (react),
(ethiospare) -[:BUILT_BY]-> (remix),
(ethiospare) -[:BUILT_BY]-> (tailwind),
(ethiospare) -[:BUILT_BY]-> (node),

(proshop) -[:BUILT_BY]-> (react),
(proshop) -[:BUILT_BY]-> (node),
(proshop) -[:BUILT_BY]-> (mongodb),

(react) -[:AQUIRED_AT]-> (AAU),
(node) -[:AQUIRED_AT]-> (AAU),
(python) -[:AQUIRED_AT]-> (AAU),
(javascript) -[:AQUIRED_AT]-> (AAU),
(mysql) -[:AQUIRED_AT]-> (AAU)
