function ftp_conn=connect2ftp(user)
% created VP 8/13/2014

%if ftp needed

ftp_conn = ftp('152.3.33.41',user,pwd);

%Radu's parameters
% ftp_conn = ftp('152.3.216.217', 'Radu', 'monkey');

%cygwin can help 
% mysql connection
% system('C:\cygwin64\bin\bash -c -l "mysql -h ccn-sommerserv.win.duke.edu -u vp35 -p"')
% listing directory
% system('C:\cygwin64\bin\bash --login -c -l "ls //ccn-sommerserv.win.duke.edu/*/vincedata"')
% creating a directory 
% system('C:\cygwin64\bin\bash --login -c -l "cd //ccn-sommerserv.win.duke.edu/*/vincedata; mkdir test"')
% copying a file from computer to server
% system('C:\cygwin64\bin\bash --login -c -l "cd E:\Data; cp testcopy.txt //ccn-sommerserv.win.duke.edu/*/vincedata/test/"');
% and delete file
% system('C:\cygwin64\bin\bash --login -c -l "cd //ccn-sommerserv.win.duke.edu/*/vincedata/test/; rm testcopy.txt"');

end

