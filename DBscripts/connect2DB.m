function conn=connect2DB(dbname) 
% modified VP 8/8/2014

%connect2DB opens a connection to the database and returns its handle

[~,slash,~,dbdir]=SetUserDir;
conn = database(dbname,'vp35',fscanf(fopen([dbdir,slash,'dbpd.txt']),'%c'),...
        'Vendor','MySQL',...
        'Server','ccn-sommerserv.win.duke.edu');
%       'URL','jdbc:mysql://ccn-sommerserv.win.duke.edu');
%       default port number is 3306, no need to specify it
%       'PortNumber',3306

set(conn, 'AutoCommit', 'off');

% 
%       %example of database interaction using exec
%       %ex. 1
%       selectDBdata =exec(conn,'select * from vp_sldata');
%       % ex. 2
%       %Use the SQL CREATE command to create the "subject" table, with fields names.
%       sqlquery = ['CREATE TABLE subject(name VARCHAR(20),'...
%           'trainer VARCHAR(20), sex CHAR(1), YOB DATE, YOD DATE)'];  


%created users and machines tables directly in mysql 
% 
% CREATE TABLE machines(user_fid INT NOT NULL AUTO_INCREMENT, m_name CHAR(20) NOT NULL, PRIMARY KEY (user_fid));
% INSERT INTO machines (m_name) VALUES ('DangerZone'), ('Vincent'), ('SommerVD');
% CREATE TABLE users(user_id INT NOT NULL AUTO_INCREMENT, name CHAR(20) NOT NULL, PRIMARY KEY (user_id)); 
% INSERT INTO users (name) VALUES ('Vincent'), ('Vincent'), ('generic');


%       %Create the table for the database connection object conn.
%       exec(conn,sqlquery); %or e=exec(conn,sqlquery); to get a return handle. Don't forget to close the cursor: close(e);
%       %Use the SQL ALTER command to add a new column to the table.
%       sqlquery = 'ALTER TABLE Subject ADD YOB int'; 
%       curs = exec(conn,sqlquery);
%       %After you are finished with the cursor object, close the cursor.
%       close(curs);
%       %delete table using DROP
%       curs = exec(conn, 'DROP TABLE subject_test');
%       close(curs);
%       
%       % see http://www.mathworks.com/help/database/ug/exec.html
%       % and http://www.mathworks.com/help/database/ug/exporting-data-using-the-bulk-insert-command.html#bsl2k0j-4
%       
%       %insert data with fastinsert
%       tablename = 'subject';
%       colnames = {'name','YOB'};
%       sbjdata = {'Hilda',1998};
%       
%       fastinsert(conn,tablename,colnames,sbjdata);

%Radu's parameters
% conn = database('recordings_alpha','webroot','monkey',...
%                 'Vendor','MySQL',...
%                 'Server','152.3.216.217');


% example of connection to Microsoft Access database with .accdb format
% dbpath = ['C:\Data\Matlab\MyDatabase.accdb']; 
% url = [['jdbc:odbc:Driver={Microsoft Access Driver (*.mdb, *.accdb)};DSN='';DBQ='] dbpath];
% con = database('','','','sun.jdbc.odbc.JdbcOdbcDriver', url); 

end

