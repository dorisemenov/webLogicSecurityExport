# webLogicSecurityExport
Python 2 script using Web Logic Scripting Tool to extract all security in Web Logic and Enterprise Manager for OBIEE installations. Used to create flat files for submission to compliance testing but also creates human readable output files for analysis.

Security areas read and exported include: 

Web Logic Global Roles and Users
Web Logic embedded LDAP Groups and Users
Enterprise Manager Application Roles and Users

Exports content into a folder with server name, port and current date in the name which means it can be run multiple times without backing up the output.
