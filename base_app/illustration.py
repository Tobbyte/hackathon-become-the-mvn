from rich.console import Console
from rich.text import Text

yoda_ascii = r"""
   _______________________________________________

 <         EIN FRAGE, ICH EUCH STELLEN MUSS        >
   _______________________________________________
                          /
                         /
              _______                   
            _/  \^^^ \_               
   ~..-..._/   ^^\  ^^ \_...-..~
    \__  --  (o) .. (o)     __/
        --..(  ./_T\   )..--
                \__/                     
             T-TTTTTTT                           
                                            
                                         
                                        
"""

pirat_ascii = r"""
   _______________________________________________________

 <     ARRR, Ihr Landraten, eine Frage oder die Planke!    >
   _______________________________________________________
                          /
                         /
         _______                        
       /         \
      /           \___                  
  ___/   ________     \                 
 /      /   _/   \ ____\     
/_____ |_~_/    ~_|                        
     [ /(__) \ O ]                                     
      J      A
        |  ,__   |                       
         L______|  
   .-----  VVVV  -----.   
  / 
"""


console = Console()
formatted_text = Text()

lines = pirat_ascii.split("\n")

for line_index, line in enumerate(lines):
    for char_index, char in enumerate(line):
        g = (char_index * 5) % 256  # macht zeile von links nach rechts verlauf
        r = 10
        b = (
            (line_index * 10) % 256
        )  # line index läuft von oben nach unten hoch und mischt mehr blau rein

        style = f"rgb({r},{g},{b})"
        formatted_text.append(char, style=style)

    formatted_text.append("\n")

console.print(formatted_text)
