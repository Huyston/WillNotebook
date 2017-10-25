%$Id: abnt.cls,v 1.21.2.1 2003/05/30 10:16:07 gweber Exp $
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
% ABNTEPUSP.CLS
%
%
%   Licence: LPPL (LaTeX Project Public License)
%     You can change this file in the terms of LPPL
%     (http://www.latex-project.org/lppl.html)
% 
%   Licenca: LPPL (LaTeX Project Public License)
%     Esta licenca diz basicamente que se voce editar o codigo desta
%     classe, mesmo localmente (no seu micro), voce DEVE RENOMEAR o arquivo
%     da classe!! Como sempre, nao eh dada nenhuma garantia.
%     Para o texto completo da licenca, favor seguir o endereco
%        http://www.latex-project.org/lppl.html
%
%   Classe para confeccao de monografias, dissertacoes ou teses
%   de acordo com as normas da Associacao Brasileira de Normas
%   Tecnicas (ABNT). Esta classe, junto com o estilo bibTeX, foram
%   desenvolvidos no grupo de trabalho abnTeX (ABsurd Norms for TeX :-)
%   (http://abntex.codigolivre.org.br) 
%
%   Class to make theses or monographies following norms defined by
%   Brazilian Association for Tecnical Norms. This class is developed
%   by abnTeX group (http://abntex.codigolivre.org.br), together with two
%   bibTeX styles.
%
%   Author (class): Miguel Vinicius Santini Frasson
%
%   Author of adaptations to the particular rules of the Escola Politécnica, University of São Paulo: Paulo Barreto (original version: 2003)
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
%  Implementation of this class:
%
%  preamble
%    class identification
%    including required packages
%    option declarations
%      pnumabnt (default), pnumplain, pnumromarab
%      sumariocompleto (default), sumarioincompleto
%      abnttocpagnum (default), tocpagnumnormal
%      abntfigtabnum (default), normalfigtabnum
%      noheader, header,  plainheader (default), ruledheader,
%      capchap, capsec
%      anapmaiusc (default), anapnormal
%      apapindentindic (default), anapindentcustom
%      anapname (default), anapnoname
%      espacosimples, espacoumemeio (default), espacoduplo
%      sempaccomuns (default), paccomuns
%          -> no longer supported (kept for compatibility)
%      autobm (default), noautobm
%      times, notimes (default)
%      indentfirst (default), noindentfirst
%    mechanism for saving other options names
%    perform tests to set fontsize, openright and paper properly 
%      (in order to get 12pt, a4 and openright as default, but user can change)
%    option procession
%    work around for prevent report to add figure and table counter in the
%      reset list of chapter counter (option disables it)
%    class 'report' loaded
%    undo work figure and table around if necessary.
%
%  implementation
%    setting default spacings
%    (NOT) loading commom packages
%       inputenc[latin1], amsmath, amssymb,
%       amsbsy, dsfont, eucal[mathscr]
%    loading 'setspace' package, but providing 'workaround' if user don't
%      use it.
%    setting margins with simple commands
%    creating page styles 'plainheader', 'header' and 'ruledheader'
%    Page numbering section
%      setting switches and defining \ABNTBeginOfTextualPart according to
%      the page numbering scheme in option
%    line spacing commands and environments
%    Chapter and section: titles, page numbering, etc
%        This is a very delicated part. Let's give a flavour of what
%        happened. See comments in implementation for details.
%      redefining \chapter
%        - tests for determine begin of textual part and make changes at this
%          event.
%        - \pretextualchapter: a started chapter in the pre-textual part
%        - ProximoForaDoSumario -> switches off \ABNTaddcontentsline.
%        - Marks: care is they are inserted by default or not.
%        - redefinig \@schapter: now \chapter* is almost equal to \chapter,
%          appart from the title display. It also includes an entry in TOC.
%        - \@part and \@spart redefined: font purposes.
%        - defined \ABNTstartsection: stared section with centralized titles
%           and inclusion in TOC.
%        - new \@dottedtoline for compleance with NBR 6027-1989
%        - \@makechapterhead and \@makeschapterheadredefined to fit
%          norms. Paying attention to capchap and fonts.
%        - redefined all \section like commands (apply last redefinitions
%          and font purposes)
%        - \anexo and \apendice -> apply old \appendix changes and
%          replaces \@chapter by \@anapchapter. 


%    redefining important commands (those that set page marks, getting rid
%      of explicit \MakeUppercase)
%        \tableofcontents
%        \listoffigures
%        \listoftables 
%        thebibliography
%        theindex (now balanced columns) or use \IndiceNaoBalanceado
%    custumizable caption separator -> temporarely commented (not required)
%    environment citado = citacao, for long quotations
%    pre-textual elements
%      Capa (cover) and Folha de rosto (face page): defining commands
%        \instituicao
%        \autor
%        \orientador
%        \coorientador
%        \titulo
%        \comentario
%        \areaConcentracao
%        \local
%        \data
%      and
%        \capa, displaying what is required according to norms.
%        \folhaderosto, that prints the face page, according to norms.
%      \paginadedicatoria
%      Environment agradecimentos
%      Resumo and Abstract.
%      Environment folhadeaprovacao  and \assinatura(*){}
%      prototype for list of symbols -> no future, I think.
%   Loading fonts if required.
%   Auto bold math
%   Indentation of first paragraph
%   commented announcements.
%
%  That is it ;-D
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
%  List of Changes
%  ---------------
% $Log: abnt.cls,v $
% Revision 1.21.2.1  2003/05/30 10:16:07  gweber
% Correction of bug 137 which causes the class to fail when loading
% the package hyperref and using \tableofcontents.
% This also resolves partially bugs 82 and 51.
%
%
% Added in version 1.1 patch 1
%
% - fixed bug of undefined \ABNT<section name>mark, which shows twice the
%   section name (only for subsection, subsubsection, and paragraph)
%
% Added in version 1.1
%
% - Fixed bug of missing paragraphy after \chapter
% - \ProximoForaDoSumario has optional parameter to et page marks
% - Fixed bug of abscense of package setspace.
% - Added options `abntfigtabnum' and `normalfigtabnum' to deal with
%   figure and table counters.
% - Added abnt style for toc. Options `abnttoc' and
%   `normaltoc' were added.
% - Fixed bug of defining pagestyles only if non-noheader.
%
% Added in version 1 (finally)
%
% - Fixed mispelling on command \espaco.
% - Fixed "capsec" (not working before).
% - Added full support for Annex and Appendix, with several class options
%   and commands for customization.
% - Not using package "textcase" anymore, since there is a undesirable
%   extra space included with \MakeUppercase.
% - Fixed default options. Now "openright" is really default.
% - Now using feature of "setspace" to avoid extra spacing on display
%   math. No bugs if the version of setspace is not up to date.
% - Added \ProximoForaDoSumario, to avoid one to not include all \chapter*
%   if one wants to set diferently the title and contents of such chapters.
% - Fixed bug on \part toc entries (buggy extra space)
% - Now font size for \capter(*) is given by \ABNTchaptersize, preventing a
%   boring redefinition of \ABNTtocchapterfont.
% - Option paccomuns no longer default.
%
% Added in version 1 beta 3
%
% - Fixed bug in page marks for \section*{}.
% - "setspace" no longer require especific (new) version.
% - Added "no displayskip stretch" support offered by 'setspace' for better
%   aesthetic.
% - Added compatibility with "hyperref" package (no more incompatible
%   optional parameter on \chapter* -- hyperref redefines some commands)
% - Useless commands removed: \cabecalhoesq and \cabecalhodir.
%
% Added in version 1 beta 2
%
% - Correct figure and table counter.
% - Some support to "folha de apresentacao", including environment
%     \begin{folhadeapresentacao} e \assinatura{} (signature).
% - Fixed bug in pnumplain and headers.
% - Fixed bug in page marks for \@schapter.
%
% Added in version 1 beta
%
%   Total reformulation of the class! The main added feature are:
% - Good machanism for "Folha de Rosto" (face page) added.
% - Page numbering squemes according to the norms.
% - Right page headings.
% - Correct section titles.
% - Several options added.
% - Features removed, like margin care
% ...too many changes to list. Just like a "new" class.
%
% Added in version 0.4.3
%
% - Stupid but severe bug on \listoffigures and \listoftables 
%     left from previous version finally removed
% - Bug fixes in theindex and thebibliography
% - Redefinition of \cleardoublepage (empty page => page style empty)
% - This `list of changes' added
%
% Added in version 0.4.2
%
% - Added \StarChaptersInTOC, \StarChaptersNotInTOC to differenciate  
%    from "standard" (old) stared chapters like \tableofcontents,
%    \listoffigures, \listoftables, thebibliography and theindex.
% - Huge bugs in commands or environments \tableofcontents, \listoffigures,
%    \listoftables, thebibliography and theindex fixed.
% - Command \SpAcEs changed to \spABNT (more reliable than before)
%
% Added in version 0.4.1
%
% - Extract forgotten debug command
% - Fix conflict (\Sp command) in final messagem, creating \SpAcEs (and
%     hoping nobody made it before)
%
%
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%                                                                  %
%                            PREAMBLE                              %
%                                                                  %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


%%%%%%%%%%%%        IDENTIFICATION        %%%%%%%%%%%%

\def\ABNTdata{2002/11/27}
\def\ABNTversion{1.1 patch 1}

\NeedsTeXFormat{LaTeX2e}%
\ProvidesClass{abntepusp}%
 [\ABNTdata\space versao \ABNTversion\space da Classe LaTeX2e ABNT]

% \NeedsTeXFormat{LaTeX2e}%
% \ProvidesClass{abnt}%
%  [2002/05/20 version 1 da Classe LaTeX2e ABNT]

%%%%%%   Required packages for the implementation of this class  %%%%%%

% ifthen - conditions in LaTeX
\RequirePackage{ifthen}

% calc - standard package for length and number easy calculations
\RequirePackage{calc}

% multicol - better multicolunms
\RequirePackage{multicol}

% ----- begin Jomi fix -----
   % novo pageref para corrigir o erro da dupla hyperref x abnt
   %\renewcommand{\pageref}[1]{%
     %\meupageref{#1}
   %}
   %\newcommand{\meupageref}[1]{%
     %\hyperlink{page.\hypergetpageref{#1}}{\hypergetpageref{#1}}%
   %}
% ----- end Jomi fix -----

%%%%%%%%%%%%%      OPTION DECLARATION      %%%%%%%%%%%%

%% Page numbering squeme
\providecommand{\ABNTpnum}{}
\DeclareOption{pnumabnt}       {\renewcommand{\ABNTpnum}{ABNT}}
\DeclareOption{pnumplain}      {\renewcommand{\ABNTpnum}{plain}}
\DeclareOption{pnumromarab} {\renewcommand{\ABNTpnum}{RomSumArab}}
\ExecuteOptions{pnumabnt}


%% Automatically include in TOC bibliography, index and stared chapters
\newboolean{ABNTincludeintoc}
\DeclareOption{sumariocompleto}   {\setboolean{ABNTincludeintoc}{true}}
\DeclareOption{sumarioincompleto} {\setboolean{ABNTincludeintoc}{false}}
\ExecuteOptions{sumariocompleto}

%% Style of page numbers in TOC
\newboolean{ABNTpagenumstyle}
\DeclareOption{abnttoc}   {\setboolean{ABNTpagenumstyle}{true}}
\DeclareOption{normaltoc} {\setboolean{ABNTpagenumstyle}{false}}
\ExecuteOptions{abnttoc}

%% Figures and tables independent of sections?

\newboolean{ABNTfigtabnumbers}
\DeclareOption{abntfigtabnum}{\setboolean{ABNTfigtabnumbers}{true}}
\DeclareOption{normalfigtabnum}{\setboolean{ABNTfigtabnumbers}{false}}
\ExecuteOptions{abntfigtabnum}

%% Option: page headers
\newboolean{ABNTheader}
\providecommand{\ABNTheadertype}{\relax}
\DeclareOption{noheader}    {\setboolean{ABNTheader}{false}}
\DeclareOption{header}      {\setboolean{ABNTheader}{true}
                             \renewcommand{\ABNTheadertype}{normal}}
\DeclareOption{plainheader} {\setboolean{ABNTheader}{true}
                             \renewcommand{\ABNTheadertype}{plain}}
\DeclareOption{ruledheader} {\setboolean{ABNTheader}{true}
                             \renewcommand{\ABNTheadertype}{ruled}}
\ExecuteOptions{plainheader}

%% Option `capchap', `capsec': 
%%   titles of chapters or sections in capital letters 
\newboolean{ABNTcapchap}
\setboolean{ABNTcapchap}{false}
\newboolean{ABNTcapsec}
\setboolean{ABNTcapsec}{false}

\DeclareOption{capchap}{\setboolean{ABNTcapchap}{true}
                        \setboolean{ABNTCapAnnexAppendix}{true}}
\DeclareOption{capsec}{\setboolean{ABNTcapsec}{true}}

%% Option `anapmaiusc' and `anapnormal'
%%   should \annexname and \appendixname be on capital letters?

\newboolean{ABNTCapAnnexAppendix}
\setboolean{ABNTCapAnnexAppendix}{true}  % manual execution of option for
                                         % cooperation between `capchap'
                                         % and `anexapendnormal'

\DeclareOption{anapmaiusc}{\setboolean{ABNTCapAnnexAppendix}{true}}
\DeclareOption{anapnormal}{\setboolean{ABNTCapAnnexAppendix}{false}}

%% Option `anapindentindic' in order to \anexo or \apendice make ABNT
%% strict indentation on its titles.

\newboolean{ABNTAnApIndicativoIndent}

\DeclareOption{anapindicindent}{\setboolean{ABNTAnApIndicativoIndent}{true}}
\DeclareOption{anapcustomindent}{\setboolean{ABNTAnApIndicativoIndent}{false}}

\ExecuteOptions{anapindicindent}

%% Option `anapindentindic' in order to \anexo or \apendice make ABNT
%% strict indentation on its titles.

\newboolean{ABNTAnApName}
\DeclareOption{anapname}{\setboolean{ABNTAnApName}{true}}
\DeclareOption{anapnoname}{\setboolean{ABNTAnApName}{false}}

\ExecuteOptions{anapname}

%% Line Spacing options: change current setting.
\newcommand*{\ABNTespacodefault}{} %
\DeclareOption{espacoumemeio} {\renewcommand*{\ABNTespacodefault}%
                                  {\taxaespacoumemeio}} % default
\DeclareOption{espacosimples} {\renewcommand*{\ABNTespacodefault}%
                                  {\taxaespacosimples}}
\DeclareOption{espacoduplo}   {\renewcommand*{\ABNTespacodefault}%
                                  {\taxaespacoduplo}}
\ExecuteOptions{espacoumemeio}

%% Margin care --> Removed since version 1 beta

%% Options `spacednotes': removed since version 0.3
%  Assuming notes single spaced always (no alternative if using setspace ;-D

%% Option: loading common packages NO LONGER SUPPORTED!!!
\newboolean{ABNTcommonpack}
\DeclareOption{paccomuns}    {\setboolean{ABNTcommonpack}{true}}
\DeclareOption{sempaccomuns} {\setboolean{ABNTcommonpack}{false}}
\ExecuteOptions{sempaccomuns}

%% Auto bold math: bold math version ir text font is in bold face
\newboolean{ABNTautobm}
\DeclareOption{autobm}   {\setboolean{ABNTautobm}{true}}
\DeclareOption{noautobm} {\setboolean{ABNTautobm}{false}}
\ExecuteOptions{autobm}

%% font option: times as default or not
\newboolean{ABNTtimesfont}
\DeclareOption{times}   {\setboolean{ABNTtimesfont}{true}}
\DeclareOption{notimes} {\setboolean{ABNTtimesfont}{false}}
\ExecuteOptions{notimes}

%% Option to indent the first paragraph of each section or chapter
\newboolean{ABNTindentfirst}
\DeclareOption{indentfirst}   {\setboolean{ABNTindentfirst}{true}}
\DeclareOption{noindentfirst} {\setboolean{ABNTindentfirst}{false}}
\ExecuteOptions{indentfirst}

\newboolean{ABNTdraft}
\DeclareOption{draft}   {\setboolean{ABNTdraft}{true}}
\DeclareOption{nodraft}   {\setboolean{ABNTdraft}{false}}
\ExecuteOptions{nodraft}

\def\ABNTcurrentoptions{}
\newcommand{\AddCurrentOptionToList}{%
  \ifx\ABNTcurrentoptions\@empty%
     \edef\ABNTcurrentoptions{\CurrentOption}%
  \else%
     \edef\ABNTcurrentoptions{\ABNTcurrentoptions,\CurrentOption}%
  \fi%
}

%% All options not defined are passed to `report'
\DeclareOption*{%
  \AddCurrentOptionToList
% if some font or paper option is passed, a flag is set.
  \ifthenelse{\equal{\CurrentOption}{10pt}\or\equal{\CurrentOption}{11pt}}%
    {\setboolean{ABNTfontsize}{true}}{}%
  \ifthenelse{\equal{\CurrentOption}{a5paper}\or%
              \equal{\CurrentOption}{b5paper}\or%
              \equal{\CurrentOption}{letterpaper}}%
    {\setboolean{ABNTpaper}{true}}{}%
  \ifthenelse{\equal{\CurrentOption}{openany}}%
    {\setboolean{ABNTopen}{true}}{}%
  \PassOptionsToClass{\CurrentOption}{report}}


% testing if user use other options for font size or paper
% than 12pt, a4paper and openright
\newboolean{ABNTfontsize}
\setboolean{ABNTfontsize}{false}
\newboolean{ABNTpaper}
\setboolean{ABNTpaper}{false}
\newboolean{ABNTopen}
\setboolean{ABNTopen}{false}

% Process options (without star -> in the order of definition!).
\ProcessOptions

% After process options, flags are properly set.
% Passing options to class, that will be loaded in \LoadClass
\ifthenelse{\boolean{ABNTfontsize}}%
  {}{\PassOptionsToClass{12pt}{report}}
\ifthenelse{\boolean{ABNTpaper}}%
  {}{\PassOptionsToClass{a4paper}{report}}
\ifthenelse{\boolean{ABNTopen}}%
  {}{\PassOptionsToClass{openright}{report}}


%%%%%%%%% Lying to report :-)         ->  working
%%
%% Report says:  \newcounter{figure}[chapter], \newcounter{table}[chapter]
%% But this is not ABNT (figure counter should not reset to 1 if chapter
%% increments). There is no straight forward way to "\renewcounter" 
%% then. So I have to make an work around.
%%
%% Idea: redefine \newcounter s.t. id newcounter is figure or table, then do
%% what I want (do not include [chapter] in the command). Otherwise, do
%% normal \newcounter.
%%
%% Advantage of this: some package may suppose that the counters of figure
%% and table are actually figure and table, and not ABNTfigure, ABNTtable,
%% as in previous versions

\ifthenelse{\boolean{ABNTfigtabnumbers}}
 {
   % saving old \newcounter
   \let\ABNToldnewcounter\newcounter\relax
   \def\ABNTeatbrackets[#1]{\relax}
   \renewcommand{\newcounter}[1]%
     {\ifthenelse{\equal{#1}{figure}\or\equal{#1}{table}}%
        {\ABNToldnewcounter{#1}\@ifnextchar[{\ABNTeatbrackets}{}}%
        {\ABNToldnewcounter{#1}}%
     }
 }
 {}

%%%%%%%%%%%%       LOADIND  REPORT CLASS       %%%%%%%%%%%%
% Load base class using current setting for basic options.
\LoadClass{report}

\ifthenelse{\boolean{ABNTfigtabnumbers}}
 {
  %% undoing redefinition of \newcounter and fixing \the(counters)
  \let\newcounter\ABNToldnewcounter\relax
  \renewcommand{\thefigure}{\arabic{figure}}
  \renewcommand{\thetable}{\arabic{table}}
 }
 {}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%                                                                  %%
%%                         IMPLEMENTATION                           %%
%%                                                                  %%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%% Stretch factor for default line spacing schemes

\newcommand*{\taxaespacosimples}{1.}
\newcommand*{\taxaespacoumemeio}{1.35}
\newcommand*{\taxaespacoduplo}{1.7}


%%%%%%%%   Load interesting packages : OBSOLET!!!   %%%%%%%%%%%%%%%%


\ifthenelse{\boolean{ABNTcommonpack}}%
 {%
   \typeout{ABNT: Opcao 'pacotescomuns' ativa!}
   % fontenc[T1] --> removed for possible pdf compatibility
   % inputenc[latin1]: more common input encoding
   \typeout{ABNT -> incluindo inputenc[latin1]}%
   \RequirePackage[latin1]{inputenc}%
   % amsmath: AMS math environments for LaTeX
   \typeout{ABNT -> incluindo amsmath}%
   \RequirePackage{amsmath}%
   % amssymb: AMS symbols
   \typeout{ABNT -> incluindo amssymb}%
   \RequirePackage{amssymb}%
   % amsbsy: bold version of symbols in amssymb
   \typeout{ABNT -> incluindo amsbsy}%
   \RequirePackage{amsbsy}%
   % dsfont: double stroke fonts (as IR, IN, etc)
   \IfFileExists{dsfont.sty}{%
     \typeout{ABNT -> incluindo dsfont}%
     \RequirePackage{dsfont}}{}%
   % eucal[mathscr]: new calligraphic letters
   \typeout{ABNT -> incluindo eucal[mathscr]}%
   \RequirePackage[mathscr]{eucal}%
   % makeidx -> removed. Useless if the user don't care about.  
 }%
 {}%

%%%%%%   Package for proper line spacing commands and environments

\IfFileExists{setspace.sty}%
{\RequirePackage{setspace}}% then
% else
{% 
% first a warning at the end of the document and than 
% fake the \setstretch command, not provided by setspace.
\AtEndDocument{\ClassWarningNoLine{abnt}%
% warning text
%   Package 'setspace' needed and was not found.
%   Please install it or check for errors in loading it.
%   It can be found at CTAN (www.ctan.org), for example.
%   For more information, refer to the class manual.
{-----------------------------------------------\MessageBreak%
O pacote 'setspace' eh necessario e nao foi\MessageBreak%
encontrado. Favor instala-lo propriamente ou\MessageBreak%
checar por erros em sua leitura. Ele pode ser\MessageBreak%
encontrado na CTAN (www.ctan.org), por exemplo.\MessageBreak%
Para mais informacoes, leia o manual da classe.\MessageBreak%
-----------------------------------------------}%
}%
\ifthenelse{\isundefined{\@currsize}}
  {\providecommand{\setstretch}[1]{\def\baselinestretch{#1}\normalsize}}
  {\providecommand{\setstretch}[1]{\def\baselinestretch{#1}\@currsize}}
}

% This command is defined by 'setspace' package, to ajust extra spacing
% before and after display math. It depends on if your setspace.sty is of
% 21 march 1998 or ouder. 
\providecommand{\setdisplayskipstretch}[1]{\relax}

% equivalent to the option 'nodisplayskipstretch' of setspace.
\setdisplayskipstretch{1.0}


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%    Setting margins
%%       (old Margin care mechanism removed since version 1 beta.)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\ifthenelse{\boolean{ABNTheader}}%
  {%
   %%%%   VERTICAL LENGHTS  %%%%
   % The distance beetwen the top of the header and the top of the text is
   % 1cm, this is,  1cm=\headheight+\headsep
   % ...but, we have to consider the depth of the header, addin 2mm.
   \setlength{\headsep}{1.2cm-\headheight}
   % The distance beetwen the paper border and the number must be 2cm
   % 2cm=\topmargin+\voffset+1in
    \setlength{\topmargin}{2cm-1in-\voffset} 
   % The inferior border must be 2.5cm % Paulo Barreto
    \setlength{\textheight}% 
      {\paperheight-\voffset-1in-\topmargin-\headheight-\headsep-2.5cm} % Paulo Barreto
  }%
  {% no header is not ABNT!!!
   % Let's fake it: 2cm each vertical margin and de same horizontal margin.
   \setlength{\topmargin}{2cm-\headheight-\headsep-\voffset-1in}
   \setlength{\textheight}% 
      {\paperheight-2cm-\footskip-2cm}
  }%

%%%%   HORIZONTAL LENGHTS   %%%%
% The left margin is 4cm, and the right margin equals to 2.5cm. % Paulo Barreto
\setlength{\oddsidemargin}{4cm-\hoffset-1in} % Paulo Barreto
% for compatibility with twoside print, the length of the margins must
% be exchanged.
\setlength{\evensidemargin}{2.5cm-\hoffset-1in} % Paulo Barreto
% \paperwidth=\textwidth+\oddsidemargin+\hoffset+1in+2.5cm % Paulo Barreto
\setlength{\textwidth}{\paperwidth-\oddsidemargin-\hoffset-1in-2.5cm} % Paulo Barreto


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%    Page styles available: 
%         plainheader, header, ruledheader
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% fontstyle for header elements
\newcommand{\rightmarkformat}{\small\itshape}
\newcommand{\leftmarkformat}{\itshape}
\newcommand{\thepageformat}{\small}

% 

\newcommand{\ABNTmarkboth}[2]{%
 \ifthenelse{\boolean{ABNTNextOutOfTOC}}
     {\markboth{\ABNTnextmark}{\ABNTnextmark}}
     {\markboth{#1}{#2}}%
 }

\newcommand{\ABNTmarkright}[1]{%
 \ifthenelse{\boolean{ABNTNextOutOfTOC}}
     {\markright{\ABNTnextmark}}
     {\markright{#1}}%
 }


%%%%%%%  Defining pagestyle "header"
%
\newcommand{\ps@header}{%
  \renewcommand{\@oddfoot}{}%
  \renewcommand{\@evenfoot}{}%
  \renewcommand{\@oddhead}%
    {{\rightmarkformat\rightmark}\hfill{\thepageformat\thepage}}%
  \renewcommand{\@evenhead}%
       {{\thepageformat\thepage}\hfill{\leftmarkformat\leftmark}}%
% Para \chapter* mostrar o cabecalho
  \let\@mkboth\ABNTmarkboth%
% Definindo a maneira como o comando o \chapter marca o cabecalho
  \renewcommand{\chaptermark}[1]{%
    \markboth%
       {\ifnum \c@secnumdepth >\m@ne%
            \thechapter{}  %
        \fi%
        ##1}%
       {\ifnum \c@secnumdepth >\m@ne%
            \thechapter{}  %
        \fi%
        ##1}%
  }%
  \renewcommand{\sectionmark}[1]{%
    \markright{%
      \ifnum \c@secnumdepth >\z@%
        \thesection\ \ %
      \fi%
      ##1}%
  }%   
}% 
 %%  Defining pagestyle plainheader
%
\newcommand{\ps@plainheader}{%
  \renewcommand{\@oddfoot}{}%
  \renewcommand{\@evenfoot}{}%
  \renewcommand{\@oddhead}{\hfill{\thepageformat\thepage}}%
  \renewcommand{\@evenhead}{{\thepageformat\thepage}\hfill}%
% Para \chapter* mostrar o cabecalho
  \let\@mkboth\ABNTmarkboth%
% Definindo a maneira como o comando o \chapter marca o cabecalho
  \renewcommand{\chaptermark}[1]{%
    \markboth%
       {\ifnum \c@secnumdepth >\m@ne%
            \thechapter\ \ %
        \fi%
        ##1}%
       {\ifnum \c@secnumdepth >\m@ne%
            \thechapter\ \ %
        \fi%
        ##1}%
  }%
  \renewcommand{\sectionmark}[1]{%
    \markright{%
      \ifnum \c@secnumdepth >\z@%
        \thesection\ \ %
      \fi%
      ##1}%
  }%   
}% 
 %%  Defining pagestyle ruledheader
%
\newcommand{\ps@ruledheader}{%
  \renewcommand{\@oddfoot}{}%
  \renewcommand{\@evenfoot}{}%
  \renewcommand{\@oddhead}%
     {\underline{\makebox[\textwidth]{\raisebox{-.5ex}{}%
       {\rightmarkformat\rightmark}\hfill{\thepageformat\thepage}}}}%
  \renewcommand{\@evenhead}%
     {\underline{\makebox[\textwidth]{\raisebox{-.5ex}{}%
       {\thepageformat\thepage}\hfill{\leftmarkformat\leftmark}}}}%
% Para \chapter* mostrar o cabecalho
  \let\@mkboth\ABNTmarkboth%
% Definindo a maneira como o comando o \chapter marca o cabecalho
  \renewcommand{\chaptermark}[1]{%
    \markboth%
       {\ifnum \c@secnumdepth >\m@ne%
            \thechapter\ \ %
        \fi%
        ##1}%
       {\ifnum \c@secnumdepth >\m@ne%
            \thechapter\ \ %
        \fi%
        ##1}%
  }%
  \renewcommand{\sectionmark}[1]{%
    \markright{%
      \ifnum \c@secnumdepth >\z@%
        \thesection\ \ %
      \fi%
      ##1}%
  }%   
}% 


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%    Page numbering 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\newboolean{ABNTinpretext}
\setboolean{ABNTinpretext}{true}

\newboolean{ABNTaftertoc}
\setboolean{ABNTaftertoc}{false}

% The command \ABNTBeginOfTextualPart is executed by \tableofcontents at
% its end. It's intented to page style and page number settings.
\providecommand{\ABNTBeginOfTextualPart}{}

\newcommand{\chaptertitlepagestyle}{plain}

\ifthenelse{\equal{\ABNTpnum}{plain}}
  {%
    \setboolean{ABNTinpretext}{false}
    \setboolean{ABNTaftertoc}{true}
    \ifthenelse{\boolean{ABNTheader}}
       {%
        \ifthenelse{\equal{\ABNTheadertype}{plain}}%
          {\pagestyle{plainheader}}
          {%
           \ifthenelse{\equal{\ABNTheadertype}{normal}}%
             {\pagestyle{header}}%
             {\pagestyle{ruledheader}}%
          }%
        \renewcommand{\chaptertitlepagestyle}{plainheader}%
       }%
       {%
        \pagestyle{plain}%
        \renewcommand{\chaptertitlepagestyle}{plain}
       }%
  }% 
  {%
   \ifthenelse{\equal{\ABNTpnum}{ABNT}}%
     {% ABNT strict
      % - pagestyle is empty until \tableofcontents, when it becames with
      %   numeration (depending on `header' or `plain' header style)
      % - page counter starts AT `folha de rosto'.
      %
      % Makeing titlepage environment increase page counter
      \let\ABNToldendtitlepage\endtitlepage\relax
      \renewcommand{\endtitlepage}{\ABNToldendtitlepage\addtocounter{page}{1}}
      \pagestyle{empty}
      \renewcommand{\thepage}{}
      \renewcommand{\chaptertitlepagestyle}{empty}
      \renewcommand{\ABNTBeginOfTextualPart}%
        {%
         \renewcommand{\thepage}{\arabic{page}}
         \ifthenelse{\boolean{ABNTheader}}
           {%
            \ifthenelse{\equal{\ABNTheadertype}{plain}}%
              {\pagestyle{plainheader}}
              {%
               \ifthenelse{\equal{\ABNTheadertype}{normal}}%
                 {\pagestyle{header}}%
                 {\pagestyle{ruledheader}}%
              }%
            \renewcommand{\chaptertitlepagestyle}{plainheader}%
           }%
           {%
            \pagestyle{plain}%
            \renewcommand{\chaptertitlepagestyle}{plain}
           }%

        }%
     }%
     {% RomArab
      % - page style with numeration 
      % - BEFORE \tableofcontents
      %     \thepage in roman
      %     page counter starts AFTER `folha de rosto'
      % - AFTER \tableofcontents
      %     \thepage in arabic
      %     page counter starts again
      %
      \ifthenelse{\boolean{ABNTheader}}
        {%
         \ifthenelse{\equal{\ABNTheadertype}{plain}}%
           {\pagestyle{plainheader}}
           {%
            \ifthenelse{\equal{\ABNTheadertype}{normal}}%
              {\pagestyle{header}}%
              {\pagestyle{ruledheader}}%
           }%
         \renewcommand{\chaptertitlepagestyle}{plainheader}%
        }%
        {%
         \pagestyle{plain}%
         \renewcommand{\chaptertitlepagestyle}{plain}
        }%
      \renewcommand{\thepage}{\roman{page}}
      \renewcommand{\ABNTBeginOfTextualPart}%
        {%
         \renewcommand{\thepage}{\arabic{page}}
         \setcounter{page}{1}
        }%
     }%
  }%



%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%  Line spacing stuff
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Since version 0.3 the `setspace' package is used.

% Space scheme in notes (footnotes and margin notes) removed since
% version 0.3 since setspace do not support it; footnotes are always
% single spaced!

% \espaco{} - ativa o espacamento para um numero dado (taxa de
% esticamento), mas aceita os parametros simples, umemeio, e duplo.

\newcommand{\espaco}[1]%
{\ifthenelse{\equal{#1}{simples}}% se espacamentos simples
  {\setstretch{\taxaespacosimples}} % entao
  { %senao (espaco simples)
   \ifthenelse{\equal{#1}{umemeio}}% se espaco 1 1/2
     {\setstretch{\taxaespacoumemeio}} % entao
     {%senao (espaco 1 1/2)
      \ifthenelse{\equal{#1}{duplo}}% se espaco duplo
        {\setstretch{\taxaespacoduplo}}% entao
        {\setstretch{#1}} % senao espaco dado
     } %fim se espaco 1 1/2
  } %fim se espaco simples
}%fim newcommand

\newenvironment{espacosimples}
  {\begin{spacing}{\taxaespacosimples}}{\end{spacing}}

\newenvironment{espacoumemeio}
  {\begin{spacing}{\taxaespacoumemeio}}{\end{spacing}}

\newenvironment{espacoduplo}%
  {\begin{spacing}{\taxaespacoduplo}}{\end{spacing}}

\newboolean{ABNThypertoc}
\AtBeginDocument{%
% default spacing (set by class options)
\espaco{\ABNTespacodefault}%
\@ifpackageloaded{hyperref}{\setboolean{ABNThypertoc}{true}}{\setboolean{ABNThypertoc}{false}}%
}


% Font track mechanism (like in utthesis.cls)
% - removed from implementation since version 0.3.
% - use instead package `relsize'.



%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%    Chapter title page style
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Redefining \chapter and \part. The changes are
%  - \chapteritlepagestyle instead of explict plain page style
%  - \ABNTchaptermark instead of \chaptermark (must be before
%       \addcontentsline !!!) 
% - several commands were replaced by abntversions due to nuances of the
%   norms :-( it can create several uncompatibilities with packages that
%   change explictily these important commands, although I have tried very
%   hard to make as less damage on compatibility as possible. As a result
%   of this, package hyperref is totally broken with abnt.cls.

%%%%%%%%%%%%%%%%%%%%%%   Special definitions   %%%%%%%%%%%%%%%%%%%%
% What is going on here?
%   
%  This class supports auto include in toc for both \chapter* and
%  \section* (and similars). As we know, the command \chapter admits an
%  optional argument, which goes to the toc and the marks, if it's present
%  (otherwise the main parameter of \chapter is used in toc and marks also.)
%  
%  To allow exactly the same mechanism for \chapter and \chapter*, \section
%  and \section*, \subsection and \subsection*, etc, I had to define
%  similar commands to some important core commands in LaTeX, like \secdef
%  (we make a new one to avoid conflicts with other packages) and
%  \@startsection (I make a new one too).
%
%  Now, \ABNTstartsection, appart from make the stared version of a
%  section-like command to include the title in toc (if a boolean is set to
%  true), the title is centered for stared form.
%
%  Now, \chapter* and \part* are almost equal to \chapter and \part
%
%  The origin of this material are the files 
%     $texmfDIR/tex/latex/base/latex.ltx  (codigo fonte do LaTeX)
%     $texmfDIR/tex/latex/base/report.cls (classe standard)

% From the definition of \secdef -> stared version now admits optional
% param (after bug with hyperref, it was no longer used.)
\def\ABNTsecdef#1#2{\@ifstar{\@dblarg{#2}}{\@dblarg{#1}}}

% Changed explicit \thispagestyle{empty}
\renewcommand\chapter%
    {%
     \if@openright\cleardoublepage\else\clearpage\fi%
     \thispagestyle{\chaptertitlepagestyle}
     \ifthenelse{\boolean{ABNTinpretext}}%
       {%
        \ifthenelse{\boolean{ABNTaftertoc}}%
          {% change to textual part
           \setboolean{ABNTinpretext}{false}%
           \ABNTBeginOfTextualPart%
          }%
          {}%
       }% 
       {}%
     \global\@topnum\z@%
     \@afterindentfalse%
%     \ABNTsecdef\@chapter\@schapter%
     \secdef\@chapter\@schapter%
    }%

% To make tre-textual chapters (that fits page numbering squeme...)
% this is equal to \chapter*{}, but ignores in witch part is it. It does
% not change any tags.
\newcommand\pretextualchapter%
    {%
     \if@openright\cleardoublepage\else\clearpage\fi%
     \thispagestyle{\chaptertitlepagestyle}
     \global\@topnum\z@%
     \@afterindentfalse%
     \@schapter%
    }%

% Created useful \resetsubcounters from the code of \stepcounter.
\newcommand{\resetsubcounters}[1]{%
  \begingroup
    \let\@elt\@stpelt
    \csname cl@#1\endcsname
  \endgroup}

%% \ProximoForaDoSumario -> taking out some chapter or section from toc.

\newboolean{ABNTNextOutOfTOC}
\setboolean{ABNTNextOutOfTOC}{false}

%% \ProximoForaDoSumario[mark text]
% Now \ProximoForaDoSumario (re)sets the marks too. If one still want the
% marks, he/she must use it as the optional parameter of this command.

\newcommand{\ABNTnextmark}{}
\newcommand{\ProximoForaDoSumario}[1][]
  {
   \setboolean{ABNTNextOutOfTOC}{true}
   \renewcommand{\ABNTnextmark}{#1}
  }


\let\ABNToldaddcontentsline\addcontentsline\relax
\newcommand{\ABNTaddcontentsline}[3]%
  {\ifthenelse{\boolean{ABNTNextOutOfTOC}}
     {\setboolean{ABNTNextOutOfTOC}{false}}
     {\ifthenelse{\boolean{ABNThypertoc}}%
     {\addtocontents{#1}{\protect\contentsline{#2}{#3}{\thepage}{#2.\csname the#2\endcsname}}}%
     {\ABNToldaddcontentsline{#1}{#2}{#3}}%
     }}

\newcommand{\ABNTchaptermark}[1]
  {%
   \ifthenelse{\boolean{ABNTNextOutOfTOC}}
     {\markboth{\ABNTnextmark}{\ABNTnextmark}}
     {\chaptermark{#1}}%
  }

\newcommand{\ABNTsectionmark}[1]
  {%
   \ifthenelse{\boolean{ABNTNextOutOfTOC}}
     {\markright{\ABNTnextmark}}
     {\sectionmark{#1}}%
  }




% \@chapter : 
\def\@chapter[#1]#2%
      {\ABNTchaptermark{#1}% This command MUST came before addcontentsline
       \ifnum \c@secnumdepth >\m@ne
         \refstepcounter{chapter}%
         \typeout{\@chapapp\space\thechapter.}%
         \ifthenelse{\boolean{ABNTaftertoc}}
           {\ABNTaddcontentsline{toc}{chapter}%
                   {\protect\numberline{\thechapter}#1}}
           {}
       \else
         \ifthenelse{\boolean{ABNTaftertoc}}%
           {\ABNTaddcontentsline{toc}{chapter}{#1}}%
           {}%
       \fi       
       \if@twocolumn
         \@topnewpage[\@makechapterhead{#2}]%
       \else
         \@makechapterhead{#2}%
         \@afterheading
       \fi\par}

%% From the \@chapter code. Now \@schapter does almost the same as
%% \@chapter. Added \resetsubcounters.
\def\@schapter#1{%
      \if@twocolumn
        \@topnewpage[\@makeschapterhead{#1}]
      \else
        \@makeschapterhead{#1}
        \@afterheading
      \fi
      \@mkboth{#1}{#1}  % <-- inserted (must be before addcontentsline)
      \ifthenelse{\boolean{ABNTincludeintoc}}%
        {%
         \ifthenelse{\boolean{ABNTaftertoc}}
           {\ABNTaddcontentsline{toc}{chapter}{#1}}
           {}
        }%
        {}
      \resetsubcounters{chapter}\par
    }%

% Fonts in \@part and \@part* changed. Some \resetsubcounters added.
\def\@part[#1]#2{%
    \ifnum \c@secnumdepth >-2\relax
      \refstepcounter{part}%
      \ABNTaddcontentsline{toc}{part}{\protect\numberline{\thepart}#1}%
    \else
      \resetsubcounters{part}
      \ABNTaddcontentsline{toc}{part}{#1}%
    \fi
    \markboth{}{}%
    {\centering
     \interlinepenalty \@M
     \normalfont
     \ifnum \c@secnumdepth >-2\relax
       \ABNTchapterfont\ABNTchaptersize\ifthenelse{\boolean{ABNTcapchap}}%
          {\MakeUppercase{\partname~\thepart}}%
          {\partname~\thepart} %\partname~\thepart% Paulo Barreto
       \par
       \vskip 20\p@
     \fi
     \ABNTchapterfont\ABNTcapchapsize\ifthenelse{\boolean{ABNTcapchap}}%
          {\MakeUppercase{#2}}%
          {#2}\par}%
    \@endpart}

\def\@spart#1{%
    \ABNTaddcontentsline{toc}{part}{#1}%    
    \markboth{}{}%
    {\centering
     \interlinepenalty \@M
     \normalfont
     \ABNTchapterfont\ABNTcapchapsize\ifthenelse{\boolean{ABNTcapchap}}%
          {\MakeUppercase{#1}}%
          {#1}\par}%
    \@endpart}


% From \@startsection. The only difference is that it calls \@ssect
% changing the meaning id the first parameter. Now, instead of indentation,
% it gives section level for TOC purposes.
\def\ABNTstartsection#1#2#3#4#5#6{%
  \if@noskipsec \leavevmode \fi
  \par
  \@tempskipa #4\relax
  \@afterindenttrue
  \ifdim \@tempskipa <\z@
    \@tempskipa -\@tempskipa \@afterindentfalse
  \fi
  \if@nobreak
    \everypar{}%
  \else
    \addpenalty\@secpenalty\addvspace\@tempskipa
  \fi
  \@ifstar
    {\ABNTssect{#1}{#4}{#5}{#6}}% #3 replaced by #1 here
    {\@dblarg{\ABNTsect{#1}{#2}{#3}{#4}{#5}{#6}}}}

% I change the meaning of the first paramenter here. Instead of an indent
% skip, it is now the name of the section, for `toc' purposes.
\def\ABNTssect#1#2#3#4#5{%
  \@tempskipa #3\relax
  \ifdim \@tempskipa>\z@
    \begingroup
      #4{%
         \interlinepenalty \@M \centering
         \ifthenelse{\boolean{ABNTcapsec}}
             {\MakeUppercase{#5}}{#5}\@@par}%
    \endgroup
    \@ifundefined{ABNT#1mark}{}{\csname ABNT#1mark\endcsname{#5}}
    \ifthenelse{\boolean{ABNTincludeintoc}}
      {\ABNTaddcontentsline{toc}{#1}{#5}}
     {}
  \else
    \def\@svsechd{#4{#5}%
      \@ifundefined{ABNT#1mark}{}{\csname ABNT#1mark\endcsname{#5}}
      \ifthenelse{\boolean{ABNTincludeintoc}}%
         {\ABNTaddcontentsline{toc}{#1}{#5}}{}
    }%
  \fi
  \@xsect{#3}}

\def\ABNTsect#1#2#3#4#5#6[#7]#8{%
  \ifnum #2>\c@secnumdepth
    \let\@svsec\@empty
  \else
    \refstepcounter{#1}%
    \protected@edef\@svsec{\@seccntformat{#1}\relax}%
  \fi
  \@tempskipa #5\relax
  \ifdim \@tempskipa>\z@
    \begingroup
      #6{%
        \@hangfrom{\hskip #3\relax\@svsec}%
          \interlinepenalty \@M
          \ifthenelse{\boolean{ABNTcapsec}}
             {\MakeUppercase{#8}}{#8}\@@par}%
    \endgroup
    \@ifundefined{ABNT#1mark}{}{\csname ABNT#1mark\endcsname{#7}}
    \ABNTaddcontentsline{toc}{#1}{%
      \ifnum #2>\c@secnumdepth \else
        \protect\numberline{\csname the#1\endcsname}%
      \fi
      #7}%
  \else
    \def\@svsechd{%
      #6{\hskip #3\relax
      \@svsec \ifthenelse{\boolean{ABNTcapsec}}
             {\MakeUppercase{#8}}{#8}}%
      \@ifundefined{ABNT#1mark}{}{\csname ABNT#1mark\endcsname{#7}}
      \ABNTaddcontentsline{toc}{#1}{%
        \ifnum #2>\c@secnumdepth \else
          \protect\numberline{\csname the#1\endcsname}%
        \fi
        #7}}%
  \fi
  \@xsect{#5}}


%%%%%%%%%%%%%%%%%%   end of Special definitions   %%%%%%%%%%%%%%%%


% adding style for page numbers required by NBR 6027

\let\old@dottedtocline\@dottedtocline
\renewcommand{\@dottedtocline}[5]{%
  \ifthenelse{\boolean{ABNTpagenumstyle}}
     {%
      {\renewcommand{\@pnumwidth}{2.5em}%
       \renewcommand{\@tocrmarg}{3.5em}
       \old@dottedtocline{#1}{#2}{#3}{#4}%
             {\ifthenelse{\equal{#5}{}}{}{p.\thinspace#5}}}%
     }%
     {\old@dottedtocline{#1}{#2}{#3}{#4}{#5}}%
}



%% Font which chapter titles will be printed
\ifthenelse{\boolean{ABNTcapchap}}
  {\newcommand{\ABNTchapterfont}{\bfseries\upshape}}
  {\newcommand{\ABNTchapterfont}{\bfseries\itshape}}

\newcommand{\ABNTtocchapterfont}{\ABNTchapterfont\upshape}

%% Font which section titles will be printed
\newcommand{\ABNTsectionfont}{\bfseries}

%% In order to \MakeUppercase do not apply to math mode in chapter or
%% section titles, package textcase used
%
% Sorry, a bug on textcase adds extra space before text. User can fix it by
% him/herself.
%
%\ifthenelse{\boolean{ABNTcapchap}\or\boolean{ABNTcapsec}}
%  {\IfFileExists{textcase.sty}
%     {\RequirePackage[overload]{textcase}}
%     {}
%  }
%  {}

\newcommand{\ABNTchaptersize}{\Large}
\newcommand{\ABNTcapchapsize}{\Large}
\newcommand{\ABNTtitulosize}{\Large}

% Defining how is typeset the \chapter
\def\@makechapterhead#1{%
  {%
%  \noindent\rule{\textwidth}{1.7pt}\\\par
  \normalfont\ABNTchaptersize\ABNTchapterfont%
  \espaco{simples}%
  \vspace*{30pt}%
  \noindent%
  \parbox[b]{\textwidth}{%
    \parbox[t]{4ex}{\thechapter}%
    \parbox[t]{\textwidth-4ex-1ex}%
      {\interlinepenalty\@M\raggedright%
        \ifthenelse{\boolean{ABNTcapchap}}%
          {\MakeUppercase{#1}}%
          {#1}
      }%
    \vspace*{0cm}
    }\\[2pt]%
  \vspace{50pt}%
  }%
}

\newif\ifotherhead
\otherheadfalse

% Defining how is typeset the \chapter*
\def\@makeschapterhead#1{%
\ifotherhead
  % MUDA O COMPRIMENTO AQUI
  \vspace*{-1.2cm}\par
  {\centering\normalfont\ABNTchaptersize\ABNTchapterfont%
   \ifthenelse{\boolean{ABNTcapchap}}%
     {\MakeUppercase{#1}}%
     {#1} 
    \par}%
  \vspace{45pt}%
  \par
  \otherheadfalse % atribui falso para o boolean otherhead
\else
  \vspace*{0pt}\par
  {\centering\normalfont\ABNTchaptersize\ABNTchapterfont%
   \ifthenelse{\boolean{ABNTcapchap}}%
     {\MakeUppercase{#1}}%
     {#1}
    \par}%
  \vspace{45pt}%
  \par
\fi
}

% redefining to apply tocnumpageabnt
\renewcommand\l@chapter[2]{%
  \ifnum \c@tocdepth >\m@ne
    \addpenalty{-\@highpenalty}%
    \vskip 1.0em \@plus\p@
    \setlength\@tempdima{1.5em}%
    \begingroup
      \ifthenelse{\boolean{ABNTpagenumstyle}}
        {\renewcommand{\@pnumwidth}{3.5em}}
        {}
      \parindent \z@ \rightskip \@pnumwidth
      \parfillskip -\@pnumwidth
      \leavevmode \normalsize\ABNTtocchapterfont
      \advance\leftskip\@tempdima
      \hskip -\leftskip
      #1\nobreak\hfil \nobreak%
      \ifthenelse{\boolean{ABNTpagenumstyle}}
         {%
          \hb@xt@\@pnumwidth{\hss 
            \ifthenelse{\not\equal{#2}{}}{{\normalfont p.\thinspace#2}}{}}\par
         }
         {%
          \hb@xt@\@pnumwidth{\hss #2}\par
         }
      \penalty\@highpenalty
    \endgroup
  \fi}

% redefine to apply style
\renewcommand\part{%
  \if@openright\cleardoublepage\else\clearpage\fi%
  \thispagestyle{\chaptertitlepagestyle}%
  \if@twocolumn\onecolumn\@tempswatrue\else\@tempswafalse\fi%
  \null\vfil\secdef\@part\@spart}%

\renewcommand\l@part[2]{%
  \ifnum \c@tocdepth >-2\relax
    \addpenalty{-\@highpenalty}%
    \addvspace{2.25em \@plus\p@}%
    \begingroup
      \parindent \z@ \rightskip \@pnumwidth
      \parfillskip -\@pnumwidth
      \noindent{\leavevmode
       \ABNTtocchapterfont\large\noindent%
          #1\hfil \hb@xt@\@pnumwidth{\hss #2}}\par
       \nobreak
         \global\@nobreaktrue
         \everypar{\global\@nobreakfalse\everypar{}}%
    \endgroup
  \fi}


\renewcommand\section{\ABNTstartsection{section}{1}{\z@}%
                           {-3.5ex \@plus -1ex \@minus -.2ex}%
                           {2.3ex \@plus.2ex}%
                           {\espaco{simples}\normalfont%
                            \ABNTsectionfont\Large}}
\renewcommand\subsection{\ABNTstartsection{subsection}{2}{\z@}%
                           {-3.25ex\@plus -1ex \@minus -.2ex}%
                           {1.5ex \@plus .2ex}%
                           {\espaco{simples}\normalfont%
                            \ABNTsectionfont\large}}
\renewcommand\subsubsection{\ABNTstartsection{subsubsection}{3}{\z@}%
                           {-3.25ex\@plus -1ex \@minus -.2ex}%
                           {1.5ex \@plus .2ex}%
                           {\espaco{simples}\normalfont%
                            \ABNTsectionfont\normalsize}}
\renewcommand\paragraph{\ABNTstartsection{paragraph}{4}{\z@}%
                           {3.25ex \@plus1ex \@minus.2ex}%
                           {-1em}%
                           {\espaco{simples}\normalfont%
                            \ABNTsectionfont\normalsize}}
\renewcommand\subparagraph{\ABNTstartsection{subparagraph}{5}{\parindent}%
                           {3.25ex \@plus1ex \@minus .2ex}%
                           {-1em}%
                           {\espaco{simples}\normalfont%
                            \ABNTsectionfont\normalsize}}

%\renewcommand*\l@section{\@dottedtocline{1}{1.5em}{2.3em}}
%\renewcommand*\l@subsection{\@dottedtocline{2}{3.8em}{3.2em}}
%\renewcommand*\l@subsubsection{\@dottedtocline{3}{7.0em}{4.1em}}
%\renewcommand*\l@paragraph{\@dottedtocline{4}{10em}{5em}}
%\renewcommand*\l@subparagraph{\@dottedtocline{5}{12em}{6em}}

%%%%%%%%%% Implementation for Annex and Appendix
%

\providecommand{\annexname}{Anexo}
\providecommand{\appendixname}{Ap\^endice} % for completeness ;-)
\newcommand{\anapchaptername}{\relax}

\newcommand*{\ABNTtravessao}{-$\!$-}

\def\@anapchapter[#1]#2%
      {
       \refstepcounter{chapter}%
       \ifthenelse{\boolean{ABNTAnApName}}
        {
         \begingroup
         \ifthenelse{\equal{#1}{}}
            {\def\thechapter{\anapchaptername{} \Alph{chapter}}}
            {\def\thechapter{\anapchaptername{} \Alph{chapter}{}
                                \ABNTtravessao{} #1}} 
         \ABNTchaptermark{}
         \endgroup
         \if@twocolumn
           \@topnewpage[\@makeanapchapterhead{#2}]%
         \else
           \@makeanapchapterhead{#2}%
           \@afterheading
         \fi
        }
        {
         \ABNTchaptermark{#1}
         \if@twocolumn
            \@topnewpage[\@makechapterhead{#2}]%
         \else
            \@makechapterhead{#2}%
            \@afterheading
         \fi
        }
       \ifnum \c@secnumdepth >\m@ne
         \typeout{\@chapapp\space\thechapter.}%
         \ifthenelse{\boolean{ABNTAnApName}}{
           \ifthenelse{\equal{#1}{}}
              {\ABNTaddcontentsline{toc}{chapter}%
                  {\anapchaptername{} \thechapter}}
              {\ABNTaddcontentsline{toc}{chapter}%
                  {\anapchaptername{} \thechapter{} \ABNTtravessao{} #1}}
         }
         {
          \ABNTaddcontentsline{toc}{chapter}%
                   {\protect\numberline{\thechapter}#1}
         }  
       \else
         \ABNTaddcontentsline{toc}{chapter}{#1}
       \fi
       \par
      }


\newlength{\ABNTanapindent}
\setlength{\ABNTanapindent}{0cm}

\newcommand{\ABNTanapsize}{\LARGE}

\newcommand{\ABNTaposindicativoanap}{\relax}

\def\@makeanapchapterhead#1{%
  {%
%  \noindent\rule{\textwidth}{1.7pt}\\\par
  \normalfont\ABNTchapterfont\ABNTanapsize
  \espaco{simples}
  \ifthenelse{\boolean{ABNTAnApIndicativoIndent}}
    {\ifthenelse{\boolean{ABNTCapAnnexAppendix}}
       {\settowidth{\ABNTanapindent}{\MakeUppercase{\anapchaptername}
          \thechapter{} \ABNTtravessao{} }}
       {\settowidth{\ABNTanapindent}{\anapchaptername} 
          \thechapter{} \ABNTtravessao{} }
    }
    {}
  \vspace*{30pt}
%
  \raggedright\espaco{1.2}\par  
  \begin{list}{}{%
       \setlength{\listparindent}{0cm}%
       \setlength{\itemindent}{-\ABNTanapindent}%
       \setlength{\rightmargin}{0cm}%
       \setlength{\leftmargin}{\ABNTanapindent}%
       \setlength{\parsep}{0pt}}%
    \item %
      \ifthenelse{\equal{#1}{}}
         {\ifthenelse{\boolean{ABNTCapAnnexAppendix}}
            {\MakeUppercase{\anapchaptername}}
            {\anapchaptername} 
          \thechapter \ABNTaposindicativoanap}
         {\ifthenelse{\boolean{ABNTCapAnnexAppendix}}
            {\MakeUppercase{\anapchaptername}}
            {\anapchaptername}
          \thechapter{} \ABNTtravessao{} \ABNTaposindicativoanap 
            \ifthenelse{\boolean{ABNTcapchap}}%
              {\MakeUppercase{#1}}%
              {#1}}
  \end{list}
  \par\vspace{50pt}%
  }%
}

\renewcommand{\appendix}{
  \setcounter{chapter}{0}
  \resetsubcounters{chapter}
  \gdef\thechapter{\Alph{chapter}}
  \gdef\@chapapp{Apendice}
  \renewcommand{\anapchaptername}{\appendixname}
  \global\let\@chapter\@anapchapter}

\let\apendice\appendix

\newcommand{\annex}{
  \setcounter{chapter}{0}
  \resetsubcounters{chapter}
  \gdef\thechapter{\Alph{chapter}}
  \gdef\@chapapp{Anexo}
  \renewcommand{\anapchaptername}{\annexname}
  \global\let\@chapter\@anapchapter}

\let\anexo\annex

%%%%%%%%%%  end of code for Annex and Appendix

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%  Redefing important commands (those that set marks)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Redefining \tableofcontents, \listoffigures, \listoftables, 
% thebibliography, theindex extracing explicit \MakeUpercase in page marks

\newboolean{ABNTrestorecol} % new boolean to avoid conflicts

%\newcommand{\upspace}{\vspace{-1.2cm}}

% ====  \tableofcontents  ====
% do exactly what old \tableofcontents used to do, but had to be redefined
% since \chapter* (used in \tableofcontents' old definition) was redefined.
\renewcommand{\tableofcontents}{%
  \ifthenelse{\boolean{@twocolumn}}%
    {\setboolean{ABNTrestorecol}{true}\onecolumn}%
    {\setboolean{ABNTrestorecol}{false}}%
  \if@openright\cleardoublepage\else\clearpage\fi
  \thispagestyle{\chaptertitlepagestyle}
  \global\@topnum\z@
  \@afterindentfalse
  \otherheadtrue\@makeschapterhead{\contentsname}%
  \@afterheading
  \@mkboth{\contentsname}{\contentsname}
  \@starttoc{toc}%
  \ifthenelse{\boolean{ABNTrestorecol}}{\twocolumn}{}%
  \if@openright\cleardoublepage\else\clearpage\fi%
  \setboolean{ABNTaftertoc}{true}
}%

\let\sumario\tableofcontents\relax
%\newcommand{\sumario}
%  {\otherheadtrue\pretextualchapter{Sumario}\@starttoc{toc}}

% ====  \listoffigures  ====
% In the same spirit of table of contents, it does the same as the old one,
% but now a test was included due "complete contents" feature.
\renewcommand{\listoffigures}{%
  \ifthenelse{\boolean{@twocolumn}}%
    {\setboolean{ABNTrestorecol}{true}\onecolumn}%
    {\setboolean{ABNTrestorecol}{false}}%
  \renewcommand{\listfigurename}{Lista de Ilustrações}
  \otherheadtrue\pretextualchapter{\listfigurename}
  \@starttoc{lof}%
  \ifthenelse{\boolean{ABNTrestorecol}}{\twocolumn}{}%
}%

\let\listadefiguras\listoffigures\relax

% ====  \listoftables  ====
% Same comments in \listoffigures
\renewcommand\listoftables{%
  \ifthenelse{\boolean{@twocolumn}}%
    {\setboolean{ABNTrestorecol}{true}\onecolumn}%
    {\setboolean{ABNTrestorecol}{false}}%
  \otherheadtrue\pretextualchapter{\listtablename}
  \@starttoc{lot}%
  \ifthenelse{\boolean{ABNTrestorecol}}{\twocolumn}{}%
}%

\let\listadetabelas\listoftables\relax

% ====  \listofabbrv  ====
\newcommand{\listabbrvname}{Lista de Abreviaturas e Siglas}
\newenvironment{listofabbrv}[1]{
        \otherheadtrue\pretextualchapter{\listabbrvname}
        \begin{list}{\textbf{??}}{
                \settowidth{\labelwidth}{#1}
                \setlength{\labelsep}{1em}
                \setlength{\itemindent}{0mm}
                \setlength{\leftmargin}{\labelwidth}
                \addtolength{\leftmargin}{\labelsep}
                \setlength{\rightmargin}{0mm}
                \setlength{\itemsep}{.1\baselineskip}
                \renewcommand{\makelabel}[1]{\makebox[\labelwidth][l]{##1}}
        }
}{
        \end{list}
}

% ====  \listofsymbols  ====
\newcommand{\listsymbolname}{Lista de Símbolos}
\newenvironment{listofsymbols}[1]{
        \otherheadtrue\pretextualchapter{\listsymbolname}
        \begin{list}{\textbf{??}}{
                \settowidth{\labelwidth}{#1}
                \setlength{\labelsep}{1em}
                \setlength{\itemindent}{0mm}
                \setlength{\leftmargin}{\labelwidth}
                \addtolength{\leftmargin}{\labelsep}
                \setlength{\rightmargin}{0mm}
                \setlength{\itemsep}{.1\baselineskip}
                \renewcommand{\makelabel}[1]{\makebox[\labelwidth][l]{##1}}
        }
}{
        \end{list}
}

% ====  thebibliography  ====
% Almost equal to old thebibliography, but without capital page marks
% and automatically in toc if active ``sumario completo''
\renewenvironment{thebibliography}[1]%
  {% replacing \chapter*{\bibname\@mkboth...}
   \if@openright\cleardoublepage\else\clearpage\fi%
   \thispagestyle{\chaptertitlepagestyle}%
   \global\@topnum\z@%
   \@afterindentfalse%
\renewcommand{\bibname}{Refer\^encias} % adaptação para ABNT/EPUSP
   \@mkboth{\bibname}{\bibname}% end \chapter*{\bibname...}
   \ifthenelse{\boolean{ABNTincludeintoc}}%
      {\ABNTaddcontentsline{toc}{chapter}{\bibname}}%
      {}%
    \if@twocolumn%
      \@topnewpage[\@makeschapterhead{\bibname}]%
    \else%
      \@makeschapterhead{\bibname}%
      \@afterheading%
    \fi%
   \list{\@biblabel{\@arabic\c@enumiv}}%
        {\settowidth\labelwidth{\@biblabel{#1}}%
         \leftmargin\labelwidth%
         \advance\leftmargin\labelsep%
         \@openbib@code%
         \usecounter{enumiv}%
         \let\p@enumiv\@empty%
         \renewcommand\theenumiv{\@arabic\c@enumiv}}%
   \sloppy%
   \espaco{simples}
   \clubpenalty4000%
   \@clubpenalty \clubpenalty%
   \widowpenalty4000%
   \sfcode`\.\@m%
  }% end of \begin{thebibliography}
  {\def\@noitemerr
       {\@latex@warning{Empty `thebibliography' environment}}%
   \endlist%
  }% end of \end{thebibliography}

\newboolean{ABNTbalancedindex}
\setboolean{ABNTbalancedindex}{true}

\newcommand*\IndiceNaoBalanceado{\setboolean{ABNTbalancedindex}{false}}

% ====  theindex  ====
% Similar to old theindex, but without capital page marks, automatically
% in toc and now with balanced colunms
\renewenvironment{theindex}%
  {%
   \ifthenelse{\boolean{@twocolumn}}%
     {\setboolean{ABNTrestorecol}{true}\onecolumn}%
     {\setboolean{ABNTrestorecol}{false}}%
   \if@openright\cleardoublepage\else\clearpage\fi%
   \thispagestyle{\chaptertitlepagestyle}%
   \global\@topnum\z@%
   \@afterindentfalse%
   \@mkboth{\indexname}{\indexname}% 
   \ifthenelse{\boolean{ABNTincludeintoc}}%
      {\ABNTaddcontentsline{toc}{chapter}{\indexname}}%
      {}%
   \@makeschapterhead{\indexname}%
   \@afterheading%
   \begingroup%
   \setlength{\columnsep}{35pt}%
   \setlength{\columnseprule}{0pt}
   \ifthenelse{\boolean{ABNTbalancedindex}}
     {\begin{multicols}{2}}
     {\begin{multicols*}{2}}%
   \espaco{simples}%
   \setlength{\parindent}{0cm}%
   \setlength{\parskip}{.3pt}%
   \let\item\@idxitem%
  }%
  {%
   \ifthenelse{\boolean{ABNTbalancedindex}}
     {\end{multicols}}
     {\end{multicols*}}%
   \endgroup%
   \ifthenelse{\boolean{ABNTrestorecol}}{\twocolumn}{}%
  }%

%%%%%%%%%%%%%% Flexibility on captions %%%%%%%%%%%%%%%%%
%
% Temporarely removed. Not really required.
%
%\newcommand{\ABNTcaptionsep}{: }
%
%\long\def\@makecaption#1#2{%
%  \vskip\abovecaptionskip
%  \sbox\@tempboxa{#1\ABNTcaptionsep #2}%
%  \ifdim \wd\@tempboxa >\hsize
%    #1\ABNTcaptionsep #2\par
%  \else
%    \global \@minipagefalse
%    \hb@xt@\hsize{\hfil\box\@tempboxa\hfil}%
%  \fi
%  \vskip\belowcaptionskip}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%% Environment `citado'=`citacao', similar to quoation, but with 4cm of
%% extra left margin, in a smaller font and simple line spacing.
 
\newenvironment{citado}%
  {\begin{espacosimples}%
   \small
   \begin{list}{}{%
       \setlength{\listparindent}{0cm}%
       \setlength{\itemindent}{\listparindent}%
       \setlength{\rightmargin}{0cm}%
       \setlength{\leftmargin}{4cm}%
       \setlength{\parsep}{0pt}}%
    \item\relax}%
  {\end{list}\end{espacosimples}}

\newenvironment{citacao}%
  {\begin{citado}}%
  {\end{citado}}%

%% Contents shows up to subsubsection. 
\setcounter{tocdepth}{4}

%% Section number will appear up to \subsubsection
\setcounter{secnumdepth}{3}



%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%                   Pre-textual elements                   %%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% CAPA - contem autor, titulo (com subtitulo incluido), local e data.
%
% FOLHA DE ROSTO - contem, no anverso : autor, titulo (com subtitulo
% incluido, se houver), nome do curso e area de concentracao, orientador e
% co-orientador (se for o caso), local e ano da apresentacao.

%\newcommand{\fcformat}{\bfseries\textsf}
\newcommand{\fcformat}{\textsf}

\providecommand{\ABNTinstituicaodata}{}
\newcommand{\instituicao}[1]{\renewcommand{\ABNTinstituicaodata}{#1}}
\newcommand{\instituicaoformat}{\scshape}

\providecommand{\ABNTautordata}{}
\newcommand{\autor}[1]{\renewcommand{\ABNTautordata}{#1}}
\newcommand{\autorformat}{\large\ABNTsectionfont}

\providecommand{\ABNTorientadordata}{}
\providecommand{\ABNTorientadorname}{}
\newcommand{\orientador}[2][Orientador:\vspace{1mm}\\]%
  {\renewcommand{\ABNTorientadorname}{#1}%
   \renewcommand{\ABNTorientadordata}{#2}}
\newcommand{\orientadornameformat}{}
\newcommand{\orientadorformat}{}

\providecommand{\ABNTcoorientadordata}{}
\providecommand{\ABNTcoorientadorname}{}
\newcommand{\coorientador}[2][Co-orientador:\vspace{1mm}\\]%
  {\renewcommand{\ABNTcoorientadorname}{#1}%
   \renewcommand{\ABNTcoorientadordata}{#2}}
\newcommand{\coorientadornameformat}{}
\newcommand{\coorientadorformat}{}

\providecommand{\ABNTtitulodata}{}
\providecommand{\ABNTuppercasetitulodata}{}
\newcommand{\titulo}[1]{
\renewcommand{\ABNTtitulodata}{#1}
\renewcommand{\ABNTuppercasetitulodata}{\uppercase{#1}}
}
\newcommand{\tituloformat}{\ABNTtitulosize\ABNTchapterfont}

\providecommand{\ABNTcomentariodata}{}
\newcommand{\comentario}[1]{\renewcommand{\ABNTcomentariodata}{#1}}
\newcommand{\comentarioformat}{}

\providecommand{\ABNTareaconcdata}{}
\providecommand{\ABNTareaconcname}{}
\newcommand{\areaConcentracao}[2][Área de Concentração:\vspace{1mm}\\]%
  {\renewcommand{\ABNTareaconcname}{#1}%
   \renewcommand{\ABNTareaconcdata}{#2}}
\newcommand{\areaconcnameformat}{}
\newcommand{\areaconcformat}{}

\providecommand{\ABNTlocaldata}{}
\newcommand{\local}[1]{\renewcommand{\ABNTlocaldata}{#1}}
\newcommand{\localformat}{}

\providecommand{\ABNTdatadata}{}
\newcommand{\data}[1]{\renewcommand{\ABNTdatadata}{#1}}
\newcommand{\dataformat}{}

\providecommand{\ABNTdedicatoriadata}{}
\newcommand{\dedicatoria}[1]{\renewcommand{\ABNTdedicatoriadata}{#1}}
\newcommand{\dedicatoriaformat}{}

\newcommand{\ABNTifnotempty}[2]{\ifthenelse{\not\equal{#1}{}}{#2}{}}

\newcommand{\capa}{%
%  \hypersetup{pdftitle=\ABNTtitulodata,pdfauthor=\ABNTautordata}
  \begin{center} 
    \espaco{1.2}
    {\autorformat \ABNTautordata} \\[8cm] 
    {\tituloformat \ABNTuppercasetitulodata}

    % comentário
    \vspace{2cm}
    \hspace{.45\textwidth} % posicionando a minipage 
    \begin{minipage}{.52\textwidth} 
      \begin{espacoumemeio} 
        \begin{sloppypar}
          {\comentarioformat
           \ABNTcomentariodata\\[0.3cm]
          }
        \end{sloppypar}
      \end{espacoumemeio} 
    \end{minipage} 

    % local e data
    \vspace*{\stretch{1}}
    \begin{espacosimples} 
      {\localformat\ABNTlocaldata}\\
      {\dataformat\ABNTdatadata}
    \end{espacosimples}
    \if@openright\cleardoublepage\else\clearpage\fi%
  \end{center} 
}% end of \capa


\newcommand{\folhaderosto}{%
  \begin{center} 
    \espaco{1.2}
    {\autorformat \ABNTautordata} \\[8cm] 
    {\tituloformat \ABNTuppercasetitulodata}

    % comentário
    \vspace{2cm}
    \hspace{.45\textwidth} % posicionando a minipage 
    \begin{minipage}{.52\textwidth} 
      \begin{espacoumemeio} 
        \begin{sloppypar}
          { \comentarioformat
            \ABNTcomentariodata\\[0.3cm]
          }
        \end{sloppypar}

        \ABNTifnotempty{\ABNTareaconcdata}%
          {%
            %\vspace{.8cm}
            {\areaconcnameformat\ABNTareaconcname}
            {\areaconcformat\ABNTareaconcdata}\par%\protect\\
          }
				\ABNTifnotempty{\ABNTorientadordata}%
				    {%
	            \vspace{.8cm}
				      {\orientadornameformat\ABNTorientadorname}
				      {\orientadorformat\ABNTorientadordata}\protect\\
				    }
				\ABNTifnotempty{\ABNTcoorientadordata}
					  {%
	            \vspace{.8cm}
					    {\coorientadornameformat\ABNTcoorientadorname}
					    {\coorientadorformat\ABNTcoorientadordata}
					  }
      \end{espacoumemeio} 
    \end{minipage} 

    % local e data
    \vspace*{\stretch{1}}
    \begin{espacosimples} 
      {\localformat\ABNTlocaldata}\\
      {\dataformat\ABNTdatadata}
    \end{espacosimples} 
    \clearpage
  \end{center} 
}% end of folhaderosto



% comandos para o tipo de documento
% ----------------------------------

\newcommand{\autorPoli}[5]{%
  \autor{\uppercase{{#1 #4 #5}}}%
  \renewcommand{\PoliAutorFichaCatalografica}{{#5, #1 #3}}%
  \renewcommand{\PoliAutorIniciaisMaisSobrenome}{{#2 #4 #5}}%
}

\newcommand{\PoliDepartamentoData}{}
\newcommand{\departamento}[1]{\renewcommand{\PoliDepartamentoData}{#1}}
\newcommand{\departamentoformat}{}

\newcommand{\PoliTipoDocData}{}

\newcommand{\monografiaFormatura}{%
  \renewcommand{\PoliTipoDocData}{Monografia (Graduação em Engenharia de Computação)}
  \comentario{\vspace{1.0cm}
    Texto apresentado à Escola
    Politécnica da Universidade
    de São Paulo como requisito
    para a conclusão do curso de
    graduação em Engenharia de Computação,
    junto ao \PoliDepartamentoData.}%
}

\newcommand{\monografiaMBA}{%
  \renewcommand{\PoliTipoDocData}{Monografia (MBA em Redes de Computadores)}
  \comentario{\vspace{1.0cm}
    Texto apresentado à Escola
    Politécnica da Universidade
    de São Paulo como requisito
    para obtenção do Título de
    Especialista (MBA) em Redes de
    Computadores, junto ao 
    \PoliDepartamentoData.}%
}

\newcommand{\qualificacaoMSc}[1]{%
  \renewcommand{\PoliTipoDocData}{Exame de Qualificação (Mestrado)}
  \comentario{\vspace{1.0cm}
    Documento apresentado à Escola
    Politécnica da Universidade
    de São Paulo para a realização
    do Exame de Qualificação
    de Mestrado em #1.}%
}

\newcommand{\dissertacao}[1]{%
  \renewcommand{\PoliTipoDocData}{Dissertação (Mestrado)}
  \comentario{\vspace{1.0cm}
    Dissertação apresentada à Escola
    Politécnica da Universidade de
    São Paulo para obtenção do
    Título de Mestre em #1.}%
}

\newcommand{\qualificacaoDr}[1]{%
  \renewcommand{\PoliTipoDocData}{Exame de Qualificação (Doutorado)}
  \comentario{\vspace{1.0cm}
    Documento apresentado à Escola
    Politécnica da Universidade
    de São Paulo para a realização
    do Exame de Qualificação
    de Doutorado em #1.}%
}

\newcommand{\teseDr}[1]{%
  \renewcommand{\PoliTipoDocData}{Tese (Doutorado)}
  \comentario{\vspace{1.0cm}
    Tese apresentada à Escola
    Politécnica da Universidade de
    São Paulo para obtenção do
    Título de Doutor em #1.}%
}

\newcommand{\teseLD}{%
  \renewcommand{\PoliTipoDocData}{Tese (Livre Docência)}
  \comentario{\vspace{1.0cm}
    Tese apresentada à Escola
    Politécnica da Universidade
    de São Paulo como requisito
    para obtenção do Título de
    \mbox{Livre}-Docente junto ao
    \PoliDepartamentoData.}%
  \orientador[~]{}%
}

\newcommand{\memorialLD}{%
  \renewcommand{\PoliTipoDocData}{Memorial (Livre Docência)}
  \comentario{\vspace{1.0cm}
    Texto apresentado à Escola
    Politécnica da Universidade
    de São Paulo como requisito
    para obtenção do Título de
    \mbox{Livre}-Docente junto ao
    \PoliDepartamentoData.}%
  \orientador[~]{}%
}


% Ficha catalográfica
% ------------------------
\usepackage{lastpage}

\newcommand{\PoliAutorFichaCatalografica}{}
\newcommand{\PoliAutorIniciaisMaisSobrenome}{}

\newcommand{\PoliRefFichaCatalografica}{%
  \PoliTipoDocData~ --- Escola Politécnica da Universidade de São Paulo.
  \PoliDepartamentoData.}

\newcommand{\PoliFichaCatalograficaData}{}

\newboolean{PoliRevisao}
\setboolean{PoliRevisao}{false}
\newcommand{\PoliEdicaoRevisadaData}{-- ed.~rev. --}
\newcommand{\PoliDataDaRevisao}{\today}
\newcommand{\PoliQuadroDeRevisaoData}{Este exemplar foi revisado e alterado em relação à versão original, sob responsabilidade única do autor e com a anuência de seu orientador.}
\newcommand{\PoliAssinaturaAutor}{Assinatura do autor}
\newcommand{\PoliAssinaturaOrientador}{Assinatura do orientador}

\newcommand{\PoliQuadroDeRevisao}{%
\begin{espacosimples}
\begin{flushleft}
%\hspace{-1.5cm}
\begin{tabular}{| @{\hspace{.5cm}} p{\textwidth-1cm} @{\hspace{.5cm}}|}
  \hline

  \vspace{.1cm}
  \noindent\fcformat\PoliQuadroDeRevisaoData \\

  \vspace{.1cm}
  \noindent\fcformat\ABNTlocaldata, \fcformat\PoliDataDaRevisao. \\

  \vspace{.5cm}%
  \noindent\fcformat\PoliAssinaturaAutor \\

  \vspace{.5cm}%
  \noindent\fcformat\PoliAssinaturaOrientador \\
  \vspace{.5cm}
  \\

  \hline
\end{tabular}
\end{flushleft}
\end{espacosimples}
}

\newcommand{\fichacatalografica}{%
\newpage

\ifthenelse{\boolean{PoliRevisao}}{\PoliQuadroDeRevisao}{}

\vspace*{\stretch{1}}

\begin{espacosimples}
  
\begin{center}
%\hspace{2.7cm}%
\textbf{\textsf{\uppercase{Ficha Catalográfica}}}
\end{center}
\begin{flushleft}
%\hspace{-1.5cm}
\begin{tabular}{| @{\hspace{1cm}} p{\textwidth-2cm} @{\hspace{1cm}}|}
  \hline

  \vspace{.1cm}
  \noindent\fcformat\PoliAutorFichaCatalografica \\

  \hspace{.8cm}%
  \fcformat\ABNTtitulodata/ \fcformat\PoliAutorIniciaisMaisSobrenome.
  \ifthenelse{\boolean{PoliRevisao}}{\fcformat\PoliEdicaoRevisadaData}{}
  \fcformat\ABNTlocaldata, \fcformat\ABNTdatadata.\\
  \hspace{.8cm}%
  \fcformat{\pageref{LastPage}~p.} \\

  \vspace{.1cm}\hspace{.8cm}%
  \fcformat\PoliRefFichaCatalografica \\

  \vspace{.1cm}\hspace{.8cm}%
  \fcformat\PoliFichaCatalograficaData
  \vspace{.3cm}
  \\

  \hline
\end{tabular}
\end{flushleft}

\end{espacosimples}

}

	\newcommand{\paginadedicatoria}
	{%
	\begin{titlepage}
	\espaco{1.1}
	\vfill\vfill\vfill
	\vspace{6cm}
	\ABNTifnotempty{\ABNTdedicatoriadata}%
	  {%
	   \hspace{.47\textwidth}
	     \begin{minipage}{.5\textwidth}
	       \begin{espacosimples}
	         \vspace{20cm}
	         {\comentarioformat\ABNTdedicatoriadata}\protect\\\par
	       \end{espacosimples}
	     \end{minipage}
	   }%
	\vspace{.8cm}
	\vfill\vfill\vfill
	\end{titlepage}
	}

	\newcommand{\ABNTagradecimentosname}{Agradecimentos}
	\newenvironment{agradecimentos}%
	  {%
	   \if@openright\cleardoublepage\else\clearpage\fi%
	   \otherheadtrue\pretextualchapter{\ABNTagradecimentosname}%
	   \begin{espacosimples}%
	  }%
	  {\end{espacosimples}\newpage}%agradecimentos


%%%%%%%%%%%   abstract  %%%%%%%%%%%
% Ambiente para Abstract. Por default, coloca fonte de tamanho 10pt
% e com espaco simples entre linhas.

% Obs.: this code will be reimplemented for better LaTeX concept support
\newcommand{\ABNTabstractname}{Abstract}
\renewenvironment{abstract}%
  {%
   \if@openright\cleardoublepage\else\clearpage\fi%
   \otherheadtrue\pretextualchapter{\ABNTabstractname}%
   \begin{espacosimples}%
  }%
  {\end{espacosimples}\newpage}%abstract

%%%%%%%%%%%   resumo  %%%%%%%%%%%
% Ambiente para Resumo. O mesmo efeito do abstract, mas em portugues. 
%
\newcommand{\resumoname}{Resumo}
\newenvironment{resumo}%
  {%
   \if@openright\cleardoublepage\else\clearpage\fi%
   \otherheadtrue\pretextualchapter{\resumoname}%
   \begin{espacosimples}%
  }%
  {\end{espacosimples}\newpage}%resumo


%%%%%%%%%%%   résumé  %%%%%%%%%%%
% Ambiente para Résumé. O mesmo efeito do abstract, mas em francês.
%
\newcommand{\resumename}{R\'esum\'e}
\newenvironment{resume}%
  {%
   \if@openright\cleardoublepage\else\clearpage\fi%
   \otherheadtrue\pretextualchapter{\resumename}%
   \begin{espacosimples}%
  }%
  {\end{espacosimples}\newpage}%résumé


%%%%%%%%%%%   Zusammenfassung  %%%%%%%%%%%
% Ambiente para Zusammenfassung. O mesmo efeito do abstract, mas em alemão.
%
\newcommand{\zusammenfassungname}{Zusammenfassung}
\newenvironment{zusammenfassung}%
  {%
   \if@openright\cleardoublepage\else\clearpage\fi%
   \otherheadtrue\pretextualchapter{\zusammenfassungname}%
   \begin{espacosimples}%
  }%
  {\end{espacosimples}\newpage}%zusammenfassung


%%%%%%% Folha de aprovacao %%%%%%%

% Command \assinatura for signature

% width of the line and text under the line
\newlength{\ABNTsignwidth}
\setlength{\ABNTsignwidth}{8cm}

% thickness of the line
\newlength{\ABNTsignthickness}
\setlength{\ABNTsignthickness}{0pt}

% ammount of space left between previous text and th signature line
\newlength{\ABNTsignskip}
\setlength{\ABNTsignskip}{2.5cm}

% \assinatura{name} -> types a line with name under the line, centralized
%
% \assinatura*{name} -> Creates the box with the line and name under
%     it, but the box has no position assigned. However the line and the
%     name are centralized with respect to each other.

\newcommand{\assinatura}{\@ifstar{\ABNTsign}{\ABNTcsign}}

\newcommand{\ABNTsign}[1]{%
  \parbox[t]{\ABNTsignwidth}{\espaco{simples}\vspace*{\ABNTsignskip}\centering%
  \rule{\ABNTsignwidth}{\ABNTsignthickness}\\%
  \nopagebreak #1\par}%
}

\newcommand{\ABNTcsign}[1]%
  {\begingroup\par\centering\ABNTsign{#1}\par\endgroup}

% environment "folhadeaprovacao" 
%   just clearpage correctly to twoside and openright compatibility
%
\newenvironment{folhadeaprovacao}%
  {\if@openright\cleardoublepage\else\clearpage\fi\begingroup}%
  {\endgroup\if@openright\cleardoublepage\else\clearpage\fi}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%% I will no longer include List of Symbols in the wishlist for this class.

%%%%%%    Opcao de fonte Times como romano default

\ifthenelse{\boolean{ABNTtimesfont}}% if `times'option enabled...
 {\IfFileExists{mathptmx.sty}%  try `mathptmx' first
    {\RequirePackage{mathptmx}}% 
    {\IfFileExists{mathptm.sty}% if not installed, try `mathptm'
       {\RequirePackage{mathptm}}%
       {\IfFileExists{times.sty} % 
         {\RequirePackage{times}}%
         {\renewcommand{\rmdefault}{ptm}}%
       }%
    }%
  \IfFileExists{helvet.sty}% including also Helvetica as sans serif.
    {\RequirePackage{helvet}}%
    {\IfFileExists{helvetic.sty}%
       {\RequirePackage{helvetic}}%
       {\renewcommand{\rmdefault}{phv}}%
    }%
 }%
 {}



%%%%% auto bold math (try follow bold face in text)

% plan: redefine commands that change font to bold to ALSO change math
% version; I don't change all commands that change font weight because I
% suppose this uses are local

\AtBeginDocument{
\ifthenelse{\boolean{ABNTautobm}\and\not\isundefined{\mv@bold}}%
 {%
  % \bfseries
  \let\ABNToldbfseries\bfseries\relax%
  \renewcommand{\bfseries}{\mathversion{bold}\ABNToldbfseries}%
  %
  % \textbf{}
  \let\ABNToldtextbf\textbf\relax%
  \renewcommand{\textbf}[1]{\ABNToldtextbf{\mathversion{bold}#1}}%
  %
  % \bf
  \let\ABNToldbf\bf\relax%
  \renewcommand{\bf}{\mathversion{bold}\ABNToldbf}%
  %
 }%
 {}%
}

%%%%%%    Indent code 

% indenting first paragraph of each section
\ifthenelse{\boolean{ABNTindentfirst}}%
 {\RequirePackage{indentfirst}}%
 {}

% paragraph indentation size and skip
\setlength{\parindent}{.7cm}
\setlength{\parskip}{.25cm}


% logo
\newcommand{\abnTeX}{{\scshape a\kern-.13exb\kern-.13exn}\kern-.13ex\TeX}

%%% final message - announcement %%%%

\AtEndDocument{%
\newcommand{\spABNT}{\space\space\space\space\space\space\space\space}%
\typeout{+-------------------------------------------------------------------+}
\typeout{%
| Comentario, sugestao ou critica sobre o abnTeX? Entre em contato: |}%
\typeout{%
|\spABNT\spABNT\space\space
http://abntex.codigolivre.org.br\space\spABNT\spABNT|}%
%\typeout{%
%| Sua opiniao eh de grande ajuda para nos.\spABNT Ass: grupo abnTeX |}%
\typeout{+-------------------------------------------------------------------+}
}%

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%  End of ABNT.CLS
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\endinput

