clear;clc;
% http://www.mathworks.com/help/database/ug/mysql-jdbc-windows.html

conn = connect2DB;
 
%newrecord = struct('name', 'H135L4A6_21460',...
%       'date',...
%       '2014-03-19', 'chamber', 'Thalamus','user', 'Radu');
%[~, success, rec_id] = addRecord(newrecord, conn);
%[already, who, ids, howmany, fname] = checkSort(newrecord, conn);
%sp2list = existingSortSp2Dlg(who, fname);
 
%newsort = struct('name', 'Hilda_12870', 'comments', 'blabla',...
%      'user', 'Radu', 'origin', 'Spike2', 'parent', rec_id);
%[success, sort_id] = addSort( newsort, conn);

ftp_conn = ftp('152.3.216.217', 'Radu', 'monkey');
addPsth(40,conn, ftp_conn);
% deleteChildren(8, conn, ftp_conn);

%addCluster(8, 4, conn, ftp_conn);
% grid = whichGrid('R', 'Cerebellum', conn);
            
% col_names = {'lm_coord','ap_coord','depth','a_file','e_file','sp2_file','date','grid_id'};
% this_data = {3,3,8570,'L3A3_8570A','L3A3_8570E','L3A3_8570.smr','2014-03-19',12};
% datainsert(conn,'recordings',col_names, this_data);