%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% LaTeX class ~ 'tau-book.cls'
% Version 2.1 (04/03/2024)
%
% Description: 
% The LaTeX class "tau-book.cls" contains all the settings, 
% packages and commands for producing lab reports or academic 
% papers. Due to its clean and structured code, users can 
% easily customize this class to their needs and preferences. 
% The class integrates BibLaTeX to manage the bibliography.
% 
% Author: 
% Guillermo Jimenez (memo.notess1@gmail.com)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%----------------------------------------------------------
% Article class requirements
%----------------------------------------------------------

\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{tau-book}[2024/03/04 Tau-book LaTeX class]
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{extarticle}}
\ProcessOptions\relax
\LoadClass[twocolumn]{extarticle}

%----------------------------------------------------------
% Required packages
%----------------------------------------------------------

\RequirePackage[utf8]{inputenc}
\RequirePackage{etoolbox}
\RequirePackage[framemethod=tikz]{mdframed}
\RequirePackage{titling}
\RequirePackage{lettrine}
\RequirePackage{microtype}
\RequirePackage[bottom,hang,flushmargin,ragged,symbol*]{footmisc}
\RequirePackage{abstract}
\RequirePackage{fancyhdr}
\RequirePackage{xifthen}
\usepackage{adjustbox}
\usepackage{adforn}
\usepackage{lastpage}
\RequirePackage[explicit]{titlesec}
\RequirePackage{caption}
\RequirePackage{setspace}
\RequirePackage{iflang}

%----------------------------------------------------------
% Other important configurations
%----------------------------------------------------------

\setlength{\columnsep}{15pt}
\graphicspath{{Figures/}{./}} 
% \renewcommand{\baselinestretch}{1}    % To change the line spacing

%----------------------------------------------------------
% New commands
%----------------------------------------------------------

\newcommand{\professor}[1]{\def\@professor{#1}}
\newcommand{\keywords}[1]{\def\@keywords{#1}}
\newcommand{\theabstract}[1]{\def\@theabstract{#1}\ignorespaces}

%----------------------------------------------------------
% Personalized colors
%----------------------------------------------------------

\definecolor{black50}{gray}{0.5}

%----------------------------------------------------------
% Geometry package setup
%----------------------------------------------------------

\RequirePackage[
	left=1.25cm,
	right=1.25cm,
	top=2cm,
	bottom=2cm,
        headsep=0.75cm,
	% showframe
]{geometry}

%----------------------------------------------------------
% Header and footer 
%----------------------------------------------------------

\newcommand{\footerfont}{\normalfont\fontsize{7}{9} \selectfont}
\newcommand{\theday}[1]{\renewcommand{\theday}{#1}}
\newcommand{\institution}[1]{\def\@institution{#1}}
\newcommand{\ftitle}[1]{\def\@ftitle{#1}}
\newcommand{\etal}[1]{\def\@etal{#1}}
\newcommand{\course}[1]{\def\@course{#1}}
\pagestyle{fancy}

\fancypagestyle{firststyle}{
   \fancyfoot[R]{\footerfont\@institution\hspace{7pt}|\hspace{7pt}\textbf{\theday}\hspace{7pt}|\hspace{7pt}\@ftitle\hspace{7pt}|\hspace{7pt}\textbf{\thepage\textendash\pageref{LastPage}}}
   \fancyfoot[L]{\footerfont\@ifundefined{@course}{}{\@course}}
   \fancyhead[C]{}
}

% Header

\fancyhead[C]{\footerfont\it\@title}
\fancyhead[LE,RO]{}
\fancyhead[LO,RE]{}

% Footer

\lfoot{}%
\cfoot{}%
\rfoot{}%

\fancyfoot[LE]{\footerfont\textbf{\thepage}\hspace{7pt}|\hspace{7pt}\@ifundefined{@course}{}{\@course}}
\fancyfoot[RO]{\footerfont\@institution\hspace{7pt}|\hspace{7pt}\textbf{\theday}\hspace{7pt}|\hspace{7pt}\@ftitle\hspace{7pt} |\hspace{7pt}\textbf{\thepage}}
\fancyfoot[RE,LO]{\footerfont\@ifundefined{@etal}{}{\@etal}\ifnum \value{authors} > 1\hspace{5pt}\textit{}\fi}

\renewcommand{\headrulewidth}{0pt}% % No header rule
\renewcommand{\footrulewidth}{0pt}% % No footer rule

%----------------------------------------------------------
% Tau start (lettrine)
%----------------------------------------------------------

\newcommand{\dropcapfont}{\bfseries\fontsize{26pt}{28pt}\selectfont}
\newcommand{\taustart}[1]{\lettrine[lines=2,lraise=0,findent=2pt, nindent=0em]{{\dropcapfont{#1}}}{}}

%----------------------------------------------------------
% Font used
%----------------------------------------------------------

\usepackage{stix2}

%----------------------------------------------------------
% Abstract preferences
%----------------------------------------------------------

\newcommand{\abslangague}{
    \iflanguage{spanish}{
        {\bfseries\itshape Resumen—}%
    }{%
        {\bfseries\itshape Abstract—}%
    }%
}

\newcommand{\abscontent}{%
    \noindent
        \parbox{\dimexpr\linewidth}{%
        {
            \ignorespaces\small{\itshape\bfseries\abslangague}{\itshape\@theabstract}}%
        }
        \vskip10pt
    \noindent
        \parbox{\dimexpr\linewidth}{%
        {
            \hspace{10pt}\small{\itshape\bfseries Keywords—}{\itshape\@keywords}}%
        }
    \vskip-3pt
}

%----------------------------------------------------------
% Title preferences
%----------------------------------------------------------

\setlength{\droptitle}{-25\baselineskip} % Move the title up

\renewcommand{\@maketitle}{%
        \vskip-25pt
    \rule{\textwidth}{0.5pt}
        \vskip3pt
    {\raggedright\bfseries\LARGE\@title\par}
	\vskip10pt
    {\raggedright\normalsize\@author\par}
        \vskip8pt
    {\raggedright\fontsize{7pt}{8pt}\selectfont\@professor\par}
        \vskip2pt
    \rule{\textwidth}{0.5pt}
        \vskip20pt
}%

%----------------------------------------------------------
% Affil setup
%----------------------------------------------------------

\usepackage{authblk} % For custom environment affiliation

\newcommand{\andlanguage}{
    \iflanguage{spanish}{
        { y }%
    }{%
        { and }%
    }%
}

\setlength{\affilsep}{8pt}
\renewcommand\Authfont{\normalfont\bfseries\fontsize{9}{11}}
\renewcommand\Affilfont{\normalfont\fontsize{7}{8}}
\renewcommand\AB@affilsepx{; \protect\Affilfont}
\makeatletter
\renewcommand\Authands{, }
\renewcommand\Authand{\ignorespaces\andlanguage}

%----------------------------------------------------------
% Section formating
%----------------------------------------------------------

\setcounter{secnumdepth}{5}
% \renewcommand{\thesubsection}{\Alph{subsection}}

\titleformat{\section}
  {\large\bfseries}
  {\thesection.}
  {0.5em}
  {#1}
  []
  
\titleformat{name=\section,numberless}
  {\large\bfseries}
  {}
  {0em}
  {#1}
  []  
  
\titleformat{\subsection}[block] % You may change it to "runin"
  {\bfseries}
  {\thesubsection.}
  {0.5em}
  {#1}    % If using runin, change #1 to '#1. ' (space at the end)
  []
  
\titleformat{\subsubsection}[runin]
  {\small\bfseries\itshape}
  {\thesubsubsection.}
  {0.5em}
  {#1. }
  []    
  
\titleformat{\paragraph}[runin]
  {\small\bfseries}
  {}
  {0em}
  {#1} 
  
\titlespacing*{\section}{0pc}{3ex \@plus4pt \@minus3pt}{5pt}
\titlespacing*{\subsection}{0pc}{2.5ex \@plus3pt \@minus2pt}{2pt}
\titlespacing*{\subsubsection}{0pc}{2ex \@plus2.5pt \@minus1.5pt}{2pt}
\titlespacing*{\paragraph}{0pc}{1.5ex \@plus2pt \@minus1pt}{12pt}

%----------------------------------------------------------
% Table of contents
%----------------------------------------------------------

\newlength{\tocsep} 
\setlength\tocsep{1.5pc} % Sets the indentation of the sections in the table of contents
\setcounter{tocdepth}{5} % Three levels in the table of contents section: sections, subsections and subsubsections

\usepackage{titletoc}
\contentsmargin{0cm}

\titlecontents{section}[\tocsep]
    {\addvspace{4pt}\selectfont\bfseries}
    {\contentslabel[\thecontentslabel]{\tocsep}}
    {}
    {\hfill\thecontentspage}
    []

\titlecontents{subsection}[\tocsep]
    {\addvspace{4pt}\selectfont}
    {\contentslabel[\thecontentslabel]{\tocsep}}
    {}
    {\ \titlerule*[.5pc]{.}\ \thecontentspage}
    []

\titlecontents*{subsubsection}[\tocsep]
    {\footnotesize\selectfont}
    {}
    {}
    {}
    [\ \textbullet\ ]

%----------------------------------------------------------
% Figures caption style
%----------------------------------------------------------

\captionsetup[figure]{format=plain, labelsep=period, textfont={footnotesize, it}, justification=centering, labelfont={footnotesize,bf}}

%----------------------------------------------------------
% Table caption style
%----------------------------------------------------------

\captionsetup*[table]{labelfont+={footnotesize,bf},textfont+={footnotesize,it},skip=10pt,position=below,labelsep=period} % Change it to "above" if you prefer the caption above the table.

%----------------------------------------------------------
% Footnotes
%----------------------------------------------------------

\definecolor{black50}{gray}{0.5}
\renewcommand*{\footnotelayout}{\normalfont\fontsize{6}{8}}
\renewcommand{\footnoterule}{
  \kern -3pt
  {\color{black50} \hrule width 72pt height 0.25pt}
  \kern 2.5pt
}

%----------------------------------------------------------
%  URL font
%----------------------------------------------------------

\RequirePackage{url}
\renewcommand\UrlFont{\selectfont}

%----------------------------------------------------------
% BibTeX (using natbib instead of BibLaTeX)
%----------------------------------------------------------

\usepackage[numbers,sort&compress]{natbib}
\bibliographystyle{ieeetr}

%----------------------------------------------------------

\endinput