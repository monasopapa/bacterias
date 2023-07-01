#Calculates the number of bacteria after n days given a reproduction rate, life expectancy, maturation period, and an initial state of bacteria.

#RUN PROJECT
- create a file and clone project from git@github.com:monasopapa/bacterias.git
- inside this file create a virtualenviroment if you do not have an virtual enviroment run : pip install virtualenvwrapper, this will install virtualenvwrapper
- run mkvirtualenv bacterias
- this will put us inside the virtual environment
- run pip install -r requeriments.txt, this will install the necesary libraries to run the project
- run uvicorn bacterias:app --reload this will start the api

#HOW TO USE
- Go to http://127.0.0.1:8000/bacterias/ and pass the following parameters:
   *p: represent maturation_period of the bacteria -> Integer
   *e: represent life_expectancy of the bacteria -> Integer
   *d: represent iteration days of the bacteria -> Integer
   *t: represent reproduction_rate of the bacteria -> Integer
   *bacterias: initial bacteria state -> 2,3,3,1,2 -> Integer array

For example: http://127.0.0.1:8000/bacterias/?p=1&e=3&d=60&t=2&bacterias=2,3,3,1,2

This will show you:
{ 
    "total_bacterias":7301991,
    "maturation_period":1,
    "life_expectancy":3,
    "reproduction_rate":2,
    "days":60
}
where:
    --total_bacterias: Number of bacterias after n days
    --maturation_period: Maturation period of the bacteria
    --life_expectancy: Life expectancy of the bacteria
    --reproduction_rate: Reproduction rate of the bacteria
    --days: Initial bacteria state

**It was tested with 1000000 days and run perfectly!




