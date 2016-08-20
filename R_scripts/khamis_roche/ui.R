
source("../uifunctions.R")
initialize('ath',TRUE)


shinyUI(bootstrapPage(
  head(),
  navigation(),
  titlePanel("Khamis-Roche method of height-determination"),
  beginPage(),
  
  beginPanel('1/3'),
  textInput(inputId="uniqueID", label = "Unique ID", value = "id_57n662948"),
  textInput("current_height", "Current height (cm)",value="130"),
  textInput("current_age", "Current age (years)",value="10"),
  textInput("current_weight", "Current weight (kg)",value="40"),
  textInput("mother_height", "Mother height (cm)",value="165"),
  textInput("father_height", "Father height (cm)",value="175"),
  radioButtons("gender", "Gender", c("Male"="Male","Female" = "Female"), selected = "Male", inline = TRUE),
  actionButton("goButton","Run analysis"),
  endPanel(),
  
  beginPanel('2/3'),
  HTML("This module provides the basic calculations as laid out in the Khamis-Roche height prediction paper. I'm currently working on these additional things:
       <li>'Adding-on' the genetics. I want to show the genetic estimate on top of this. Currently I prefer on-top showing over a merged guess-value, since that let's us still claim we are using to large public studies (Wood et al and Khamis et al)</li>
       <li>Double-checking and completing the Khamis-Roche table 1. I typed in several lines of the table 1 <i>by-hand</i> in the airplane. While drinking wine. I think it's best to do using OCR, also to get the complete set of values. Help wanted - see file <i>2016-05-22_khamis_roche_coefficents.txt</i></li>
      <li>Working on this median absolute deviation (MAD50 / MAD90) reporting. I have no clue why Khamis-Roche chose to use this. It's much less frequently used than the confidence intervals we use. THey should be sort of similar. Sort-of. So I have to figure out a way to translate between the two, setting up some computational simulation experiment or something.</li>
      <li>Somehow also adding in the growth-spurt yes/no data.</li>
      <li>That's it</li>
      <br>"),
  plotOutput("plot1"),
  endPanel(),
  
  endPage(),
  footer()
))	