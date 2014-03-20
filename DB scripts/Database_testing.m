clear;clc;
% http://www.mathworks.com/help/database/ug/mysql-jdbc-windows.html
conn = database('recordings_alpha','webroot','monkey',...
                'Vendor','MySQL',...
                'Server','152.3.216.217');

newrecord = struct('name', 'H135L4A6_21460', 'path',...
     'E:\Spike_Sorting\', 'date',...
     '2014-03-19', 'chamber', 'Thalamus');
[already, success] = addRecord(newrecord, conn);
% grid = whichGrid('R', 'Cerebellum', conn);
            
% col_names = {'lm_coord','ap_coord','depth','a_file','e_file','sp2_file','date','grid_id'};
% this_data = {3,3,8570,'L3A3_8570A','L3A3_8570E','L3A3_8570.smr','2014-03-19',12};
% datainsert(conn,'recordings',col_names, this_data);