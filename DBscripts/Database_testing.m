clear;clc;
% http://www.mathworks.com/help/database/ug/mysql-jdbc-windows.html
conn = connect2DB;

newrecord = struct('name', 'S115L4A6_12870', 'path',...
     'E:\Spike_Sorting\', 'date',...
     '2014-03-19', 'chamber', 'Cerebellum','user', 'Radu');
%[~, success] = addRecord(newrecord, conn);
[already, who, ids, howmany, fname] = checkSort(newrecord, conn);
sp2list = existingSortSp2Dlg(who, fname);
% grid = whichGrid('R', 'Cerebellum', conn);
            
% col_names = {'lm_coord','ap_coord','depth','a_file','e_file','sp2_file','date','grid_id'};
% this_data = {3,3,8570,'L3A3_8570A','L3A3_8570E','L3A3_8570.smr','2014-03-19',12};
% datainsert(conn,'recordings',col_names, this_data);