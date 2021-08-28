REM --------------------------------------------------------------------------
REM build and run.
REM COPYRIGHT (C) 2021 kWatanabe
REM --------------------------------------------------------------------------

SET HEAD_HTML=src\head.html
SET FOOT_HTML=src\foot.html
SET OUTPUT_HTML=index.html

TYPE %HEAD_HTML% > %OUTPUT_HTML%
TYPE src\main.py >> %OUTPUT_HTML%
TYPE %FOOT_HTML% >> %OUTPUT_HTML%
START %OUTPUT_HTML%
