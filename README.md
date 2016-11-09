# WillNotebook

[![Join the chat at https://gitter.im/WillNotebook/Lobby](https://badges.gitter.im/WillNotebook/Lobby.svg)](https://gitter.im/WillNotebook/Lobby?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

[![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=C58FUYGZW7QDA&lc=US&item_name=WillNotebook&item_number=willnotebook&currency_code=USD&bn=PP%2dDonationsBF%3abtn_donateCC_LG%2egif%3aNonHosted)

WillNotebook is inspired by jupyter (notebook) project, but aims the specifics of academic writing. The idea is to merge the advantages and functionalities of Word, Latex and Python together into one powerful and hackable software.

## What can I do with WillNotebook

- Add titles, subtitles, etc
- Add normal text
- Add python code and execute it within the document
- Call python variables into the text
- Add equations with latex and sympy
- Reference equations in the text in the latex style
- Add figures

## Export formats

The default format is ".will" and it is the recommended format for holding all the information that WillNotebook needs. However you can export to other formats like:

- .tex (clean LaTeX file)
- .docx (Equations and Figures are not included yet)
- .pdf (from pdflatex)
- .pdf (from WillNotebook browser printing)

## How is it different from Jupyter Notebook

It is focused on academic writting. And so it provides an automatic section numbering, equation numbering, referencing system, figure with captions and sources and it is more clean and readable (like a report or a paper with hidden code).

## How to use it

### Dependencies

WillNotebook needs Python3 to run, so if you don't have it installed download it [here](https://www.python.org/ftp/python/3.5.2/Python-3.5.2.tar.xz).
To run the server you will need to have installed the following packages:

- Cherrypy (To run the server)
- Dill (to save the code state)
- [Optional] LaTeX (to produce the pdflatex)
- [Optional] Python-docx (to produce .docx documents)
- [Optional] Sympy (To do math calculations)

You can install Python packages using pip:
```bash
# pip install cherrypy dill python-docx sympy
```
To install LaTeX, install TexLive (Linux) or MiKTeX(Windows).
**Note**: Windows compatibility is not tested and probably PDF creation with pdflatex won't work. Export to .tex should work on all platforms even without LaTeX installed.
Ubuntu
```bash
# apt-get install texlive
```
ArchLinux
```bash
# pacman -S texlive
```
# Start the server
Download all the files and run the server "main.py". After this, visit "127.0.0.1:8080" on your browser and have fun :)
You should read the example for instructions on how to create your first document, by opening the "example.will" file in the blue bar.

## The future

I made this to write my PhD thesis, so I shall improve it to be easy, hackable, and with many features that improve writting efficiency.

## Hackable?

Yes! WillNotebook runs in a browser and all the code is easily hackable. It's written in Python (even the browser code thanks to Brython!). So, if you need to change how the .tex exporter handles the figures, you can change the code yourself very easily. I'll try to make a good documentation of how it works so anyone can play with it.

And more! It's also html! You can play with the Notebook html within the document, but it's on your own :)

## WARNING VERY EARLY ALPHA

This is still in development, but fell free to play with it, request features and help me code it ;)

I think it's all for now.

Have fun :)
