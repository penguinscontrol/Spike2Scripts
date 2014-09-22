function [ psth_id, success ] = psth2DB( conn, ftp_conn, c_id, local_file )
%given a path to a .png file, adds it to the ftp and database
try
server_name = regexprep(local_file{1},'_cl_\d+',['_cl_' num2str(c_id)]);
cd(ftp_conn, '/myapp/figures');
copyfile([local_file{2} local_file{1}], [local_file{2} server_name]);
mput(ftp_conn, [local_file{2} server_name]);
delete([local_file{2} server_name]);
% update record
    col_names = {'cluster_id_fk','image_url','image_caption'};
    this_data = {c_id, server_name, ' '};
    datainsert(conn,'psth',col_names, this_data);
    commit(conn);
    query = 'SELECT LAST_INSERT_ID()';           
    results = fetch(conn, query);
    psth_id = results{1};
    success = 1;
catch
    psth_id = []
    success = 0;
end

end

