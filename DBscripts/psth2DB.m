function [ psth_id, success ] = psth2DB( conn, c_id, clusnum, local_file ) %ftp_conn
%given a path to a .png file, adds it to the files on server and to database
[~,~,~,~,~,servrep,mapddataf]=SetUserDir;
try
server_name = regexprep(local_file{1},'_cl_\d+',['_cl_' num2str(clusnum)]);
% cd(ftp_conn, '/myapp/figures');
try
copyfile([local_file{2} local_file{1}], [local_file{2} server_name]);
catch
    %file probabaly already exists
end

% mput(ftp_conn, [local_file{2} server_name]);
system(['C:\cygwin64\bin\bash --login -c -l "cd ', regexprep(local_file{2},'\','/'),'; cp ',server_name,' ',servrep,'/',mapddataf,'/figures/"']);    
delete([local_file{2} server_name]);

% update record
    col_names = {'cluster_id_fk','alignment','image_url','image_caption'};
    alignment=regexp(local_file{2},'\w+.{1}$','match');alignment=alignment{:}(1:end-1);
    if size(alignment,2)>3
        alignment='unkn';
    end
    this_data = {c_id, alignment, server_name, ' '};
    datainsert(conn,'psth',col_names, this_data);
    commit(conn);
    query = 'SELECT LAST_INSERT_ID()';           
    results = fetch(conn, query);
    psth_id = results{1};
    success = 1;
catch
    psth_id = [];
    success = 0;
end

end

