// All nodes //
MATCH (n) RETURN n

//ALL PERSONS WHICH IS ME
match (Basliel: PERSON) return Basliel

//ALL SKILLS IN MY RESUME
match (skill: SKILL) return skill

//ALL HOBBIES
match (hobbies:HOBBIE) return hobbies

//ALL SKILLS THAT BASLIEL HAS
match (basliel:PERSON) - [:HAS_SKILL] -> (skill:SKILL) return basliel, skill

//ALL LANGUAGES THAT BASLIEL CAN SPEAK
match (basliel:PERSON) - [:SPEAKS] -> (language:LANGUAGE) return basliel, language

//ALL ORGANIZATIONS BASLIEL HAS WORKED FOR
match (basliel:PERSON) - [:WORKED_AT] -> (organization:ORGANIZATION) return basliel, organization

//ALL SKILLS BASLIEL HAS AQUIRED AT SCHOOL
match (skill:SKILL) - [:AQUIRED_AT] -> (school:SCHOOL) return skill, school

//ALL PROJECTS THAT USE SPECIFIC SKILL THAT BASLIEL HAS WORKED ON
match (basliel:PERSON) - [:WORKED_IN] ->(project:PROJECT) - [:BUILT_BY]-> (skill:SKILL) where skill.name = "MongoDB" return project