function [ conn ] = connect2DB(  )
%connect2DB opens a connection to the database and returns its handle
conn = database('recordings_alpha','webroot','monkey',...
                'Vendor','MySQL',...
                'Server','152.3.216.217');
set(conn, 'AutoCommit', 'off')
end

