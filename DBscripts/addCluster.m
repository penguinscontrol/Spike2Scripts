function [ success, c_id ] = addCluster(s_id, c_name, conn, ftp_con)
%addCluster Adds an entry for a cluster to the database and all relevant
%jpegs to the database

try
    % Get parent sort name
    query = ['SELECT a_file FROM sorts s INNER JOIN recordings r on s.recording_fid = r.recording_id WHERE sort_id = ' num2str(s_id) ];
    ssdirq = ['SELECT path FROM machines WHERE m_name = ' getenv('username')];
    ssdir = fetch(conn,ssdirq); ssdir = ssdir{1};
    name_results = fetch(conn,query);
    % format to wfrm and jpeg name
    wvfrm_name = [name_results{1}(1:end-1) '_cl_' num2str(c_name) '_Wvfrm.jpeg'];
    isi_name = [name_results{1}(1:end-1) '_cl_' num2str(c_name) '_INTH.jpeg'];
    path = [ssdir 'figures\'];
   
    
    col_names = {'average_wvfrm', 'isi', 'phenotype', 'name', 'sort_fid'};
    first_data = {' ', ' ', ' ', c_name, s_id}; % add as much as we can, don't know c_id yet
    
    datainsert(conn,'clusters',col_names, first_data);
    commit(conn);
    query = 'SELECT LAST_INSERT_ID()';           
    results = fetch(conn, query);
    c_id = results{1};
    
    wvfrm_ftp_name = '';
    isi_ftp_name = '';
    cd(ftp_con, '/myapp/figures');
    
    % Upload waveform jpeg
    try
        wvfrm_ftp_name = [name_results{1}(1:end-1) '_cl_' num2str(c_id)  '_Wvfrm.jpeg'];
        copyfile([path wvfrm_name], [path wvfrm_ftp_name]);
        mput(ftp_con, [path wvfrm_ftp_name]);
        delete([path wvfrm_ftp_name]);
    catch    
    end
    
    % Upload waveform jpeg
    try
        isi_ftp_name = [name_results{1}(1:end-1) '_cl_' num2str(c_id) '_INTH.jpeg'];
        copyfile([path isi_name], [path isi_ftp_name]);
        mput(ftp_con, [path isi_ftp_name]);
        delete([path isi_ftp_name]);    
    catch
    end
    
    % look for a putatives txt file
    putatives = ' ';
        subj = whichSubj(name_results{1}(1));
        fhandle = fopen([ssdir subj '\Spike2Exports\' name_results{1}(1:end-1) 'n.txt']);
    
    % if found one, upload putative names
    if fhandle ~= -1
        thisline = fgetl(fhandle);
        foundit = false;
        while ischar(thisline) && ~foundit
            cur_c = str2num(thisline(1));
            if cur_c == c_name
                foundit = true;
                putatives = cellstr(thisline);
            end
            thisline = fgetl(fhandle);
        end
        fclose(fhandle);
    end
    
    % update record
    col_names = {'average_wvfrm', 'isi', 'phenotype'};
    second_data = {wvfrm_ftp_name, isi_ftp_name, putatives};
    
    update(conn,'clusters',col_names,second_data,['WHERE cluster_id = ' num2str(c_id) ';']);
    commit(conn);
    success = 1;
catch
        success = 0;
        c_id = nan;
end
end

