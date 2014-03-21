function [ success, c_id ] = addCluster(s_id, c_name, conn, ftp_con)
%addCluster Adds an entry for a cluster to the database and all relevant
%jpegs to the database

try
    % Get parent sort name
    query = ['SELECT a_file, path FROM sorts s INNER JOIN recordings r on s.recording_fid = r.recording_id WHERE sort_id = ' num2str(s_id) ];           
    results = fetch(conn,query);
    % format to wfrm and jpeg name
    wvfrm_name = [results{1}(1:end-1) '_Wvfrm_cl_' num2str(c_name) '.jpeg'];
    isi_name = [results{1}(1:end-1) '_INTH_cl_' num2str(c_name) '.jpeg'];
    path = [results{2} 'figures\'];
    
    col_names = {'average_wvfrm', 'isi', 'phenotype', 'name', 'sort_fid'};
    first_data = {' ', ' ', ' ', c_name, s_id}; % add as much as we can, don't know c_id yet
    
    datainsert(conn,'clusters',col_names, first_data);
    commit(conn);
    query = 'SELECT LAST_INSERT_ID()';           
    results = fetch(conn, query);
    c_id = results{1};
    
    wvfrm_ftp_name = '';
    isi_ftp_name = '';
    try
        cd(ftp_con, 'myapp/figures');
        wvfrm_ftp_name = [results{1}(1:end-1) '_Wvfrm_cl_' num2str(c_id) '.jpeg'];
        copyfile([path wvfrm_name], [path wvfrm_ftp_name]);
        mput(ftp_con, [path wvfrm_ftp_name]);
        delete([path wvfrm_ftp_name]);
    catch    
    end
    try
        cd(ftp_con, 'myapp/figures');
        isi_ftp_name = [results{1}(1:end-1) '_INTH_cl_' num2str(c_id) '.jpeg'];
        copyfile([path isi_name], [path isi_ftp_name]);
        mput(ftp_con, [path isi_ftp_name]);
        delete([path isi_ftp_name]);    
    catch
    end
    success = 1;
catch
        success = 0;
        c_id = nan;
end
end

