@echo on
setlocal enabledelayedexpansion

set d=%date:~0,2%
set m=%date:~3,2%
set y=%date:~6,4%
set yesterday=%m:~-2%/%d:~-2%/%y%
set yesterday2=%m:~-2%.%d:~-2%.%y%
cd %~dp0
dir "files\%yesterday2%.xml" /a-D 2>nul >nul  && findstr "^" "files\%yesterday2%.xml">nul&& exit || del "files\%yesterday2%.xml"
:m4
wget.exe "https://www.nbrb.by/Services/XmlExRates.aspx?ondate=%yesterday%" --output-document=files\%yesterday2%.xml --output-file=log\log.txt
dir "files\%yesterday2%.xml" /a-D 2>nul >nul && findstr "^" "files\%yesterday2%.xml">nul&& echo OK || goto m4

:m2
if %d:~0,1%==0 set d=%d:~1%
if %m:~0,1%==0 set m=%m:~1%

set /a feb=y%%4
if %feb%==0 (set feb=29) else (set feb=28)

set /a tok=m-1
if %tok%==0 set tok=12
for /f "tokens=%tok%" %%i in ("31 %feb% 31 30 31 30 31 31 30 31 30 31") do (
:: минус 1 день  set /a d-=1
   set /a d-=1
    if !d!==0 (
        set d=%%i
        set m=%tok%
        if !m!==12 set /a y-=1
    )
)
set d=0%d%
set m=0%m%

set yesterday=%m:~-2%/%d:~-2%/%y%
set yesterday2=%m:~-2%.%d:~-2%.%y%


cd %~dp0
dir "files\%yesterday2%.xml" /a-D 2>nul >nul && findstr "^" "files\%yesterday2%.xml">nul&& exit || del "files\%yesterday2%.xml"
:m3
wget.exe "https://www.nbrb.by/Services/XmlExRates.aspx?ondate=%yesterday%" --output-document=files\%yesterday2%.xml --output-file=log\log.txt
dir "files\%yesterday2%.xml" /a-D 2>nul >nul && findstr "^" "files\%yesterday2%.xml">nul&& echo OK || goto m3
echo %yesterday%


goto m2
