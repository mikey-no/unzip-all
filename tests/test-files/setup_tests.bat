@echo off
echo Setup for test-001
echo ----------------------
echo Remove working test files
rmdir /s /q test-001

: /s sub directories
: /q quietly don't ask any questions

echo Copy in the test files for the next test
xcopy /s /i /e /y test-001-copy-with-zip test-001

: /s sub directories
: /i assume directories
: /e do empty directories
: /y yes to all including overwrite
