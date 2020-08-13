import sklearn

"""
name: Last name, First name [Can appear multiple times]
posit: Nominated for Chief or Associate Justice 
       0. Chief justice. 
       1. Associate justice.
recess: 0. Not appointed. 
        1. Appointed.
id: Unique ID in reference to the names.
analu: Unit of Analysis 
       1. First record. 
       2. Second record for individuals in the database twice. 
       3. Third record for individuals in the database trice.
spaethid: Justice ID 
childst:  Nominee’s Childhood Location—State or Country 
          999. Unknown
childsur: Childhood env. 
          1. Family farm.
          2. Rural.
          3. Small town
          4. Small city
          5. Urban
          6. Family plantation
          999. Unknown 
famses: Family Economic Status
        1. Lower
        2. Lower-middle
        3. Middle
        4. Upper-middle
        5. Upper
        999. Unclear
nomrelig: Religion
          1. Baptist
          2. Church of England
          3. Congregationalist
          4. Disciples of Christ
          5. Dutch Reform
          6. Episcopalian
          7. Jewish
          8. Lutheran
          9. Methodist
          10. Presbyterian
          11. Protestant
          12. Quaker
          13. Roman Catholic
          14. Unitarian
          999. Unknown
natorig: National Origin
         1. African
         2. Austrian
         3. Dutch
         4. English
         5. English/Dutch
         6. English/German
         7. English/Irish
         8. English/Scotch
         9. English/Swiss
         10. English/Welsh
         11. French
         12. French/Dutch
         13. German
         14. German/Romanian/Prussian/Polish
         15. Irish
         16. Italian
         17. Russian
         18. Scandinavian
         19. Scotch
         20. Scotch/Dutch
         21. (empty)
         22. Scotch/Irish
         23. Scotch/ Irish/ German
         24. Spanish
         25. Swiss/German
         26. Welsh/Dutch/Scotch/Irish
         27. Welsh/ French Huguenot
         28. English/Czech
         29. Puerto Rican
         30. English/Irish/German
         999. Unknown
race: 0. White
      1. Black
      2. Hispanic
gender: 0. Male
        1. Female 
fathoccu: Father's Occupation, Page 33            
lawschn: Number of Law Schools attended
         888. Not applicable
         999. Unknown
marryn: Number of marriages
        0. Never married
        999. Unknown
militbr: Military Branch Service
         1. Army
         2. Army Air Force
         3. Army Reserve
         4. Confederate Army
         5. Continental Army
         6. Georgia Militia
         7. Kentucky Volunteers
         8. Marines
         9. Maryland Militia
         10. Massachusetts Volunteer Regiment
         11. Minutemen
         12. National Guard
         13. Navy
         14. New York Militia
         15. North Carolina Militia
         16. Union Army
         888. Not applicable:  Did not serve in the military
         999. Unknown
barst1: First State in which Nominee was Admitted to the Bar
privtyp1: Type of Nominee’s First Private Law Practice
          1. Solo practice
          2. Counsel for a corporation
          3. Small partnership
          4. Law firm
          888. Not applicable
          999. Unclear or unknown
schn: Number of law schools taught
      888. Not applicable
      999. Unknown
agenom: Age at time of nomination
stnom: Official home state of nomination, Appendix B.
parnom: Political party affiliation at time of nomination, Appendix C
presname: Name of nominating president, Appendix F
prespart: Political party affiliation of the nominating president, Appendix C
nompres: Nominate ideology score
         888. Not applicable. Data not available
socpres: Social Liberalism Score of the Nominating President
         888. Not applicable. Data not available
econpres: Economic Liberalism Score of the Nominating Pres-ident
          888. Not applicable. Data not available
senparty:   Dominant Political Party of the U.S. Senate at theTime of Nomination, Appendix C.
nomsen: NOMINATE Ideology Score of the Score of the Me-dian Member of the U.S. Senate at the Time of Nomination
        888. Not applicable. Data not available
ideo: Segal & Cover Score of the Nominee’s Ideology
      777. Recess appointment
      888. Not applicable. Data not available
mednmq1: Name of Martin & Quinn’s Most Likely Medianin Term Prior to Nomination
         888. Not applicable. Data not available
medmq1: Martin & Quinn’s Median in Term Prior to the Nomination
        888. Not applicable. Data not available 
mednmq2: Name of Martin & Quinn’s Most Likely Medianin the Term of Nomination
         888. Not applicable. Data not available
medmq2: Martin & Quinn’s Median in Term of Nomination
        888. Not applicable. Data not available
"""

#  FOLDERS
JudgeDemographics = "\\Judge Demographics"

MajorityJudgeCases = "\\Majority Judges"


