function [ success, c_id ] = addCluster(s_id, c_name, conn, ftp_con)
%addCluster Adds an entry for a cluster to the database and all relevant
%jpegs to the database
global directory;
[~,~,~,~,~,servrep,mapddataf]=SetUserDir;

try
    % Get parent sort name
    query = ['SELECT a_file FROM sorts s INNER JOIN recordings r on s.recording_id_fk = r.recording_id WHERE sort_id = ' num2str(s_id) ];
    %     ssdir = getSsdir(conn); % not really interesting to define that in
    %     the database
    name_results = fetch(conn,query);
    % format to wfrm and jpeg name
    wvfrm_name = [name_results{1}(1:end-1) '_cl_' num2str(c_name) '_Wvfrm.jpeg'];
    isi_name = [name_results{1}(1:end-1) '_cl_' num2str(c_name) '_INTH.jpeg'];
    figdir = [directory, 'figures\'];
    
    col_names = {'average_wvfrm', 'isi', 'phenotype', 'name', 'sort_id_fk'}; %sort_id_fk was sort_fid
    first_data = {' ', ' ', ' ', c_name, s_id}; % add as much as we can, don't know c_id yet
        %if it's REX, 99.9% there wil be only channel
%         c_origin=fetch(conn,['SELECT s.origin FROM sorts s WHERE s.sort_id = ' num2str(s_id)]);
%         if strcmp('Rex',c_origin{:})
%             first_data{1}= fetch(conn,['SELECT cluster_id FROM sorts s INNER JOIN clusters c WHERE s.sort_id = ' num2str(s_id)]);
%         end
        
    datainsert(conn,'clusters',col_names, first_data);
    commit(conn);
    query = 'SELECT LAST_INSERT_ID()';
    results = fetch(conn, query);
    c_id = results{1};
    
    %wvfrm_ftp_name = '';
    isi_ftp_name = '';
    %     cd(ftp_con, '/myapp/figures');
    
    % Upload waveform jpeg
    try
        %chek if file exists
        if  exist([figdir wvfrm_name], 'file') == 2 
        %wvfrm_ftp_name = [name_results{1}(1:end-1) '_cl_' num2str(c_id)  '_Wvfrm.jpeg'];
        %copyfile([figdir wvfrm_name], [figdir wvfrm_ftp_name]);
        %mput(ftp_con, [figdir wvfrm_ftp_name]);
        system(['C:\cygwin64\bin\bash --login -c -l "cd ', regexprep(figdir,'\','/'),'; cp ',wvfrm_name,' ',servrep,'/',mapddataf,'/figures/"']);
        %delete([figdir wvfrm_ftp_name]);
        % update record
        col_names = {'average_wvfrm'};
        second_data = {wvfrm_name};
        update(conn,'clusters',col_names,second_data,['WHERE cluster_id = ' num2str(c_id) ';']);
        commit(conn);
        end
    catch
    end
    
    % Upload isi jpeg
    try
        %chek if file exists
        if  exist([figdir isi_name], 'file') == 2 
%         isi_ftp_name = [name_results{1}(1:end-1) '_cl_' num2str(c_id) '_INTH.jpeg'];
%         copyfile([figdir isi_name], [figdir isi_ftp_name]);
        %         mput(ftp_con, [figdir isi_ftp_name]);
        system(['C:\cygwin64\bin\bash --login -c -l "cd ', regexprep(figdir,'\','/'),'; cp ',isi_name,' ',servrep,'/',mapddataf,'/figures/"']);
%         delete([figdir isi_ftp_name]);
        % update record
        col_names = {'isi'};
        second_data = {isi_name};
        update(conn,'clusters',col_names,second_data,['WHERE cluster_id = ' num2str(c_id) ';']);
        commit(conn);
        end
    catch
    end
    
    % look for a putatives txt file
    putatives = ' ';
    subj = whichSubj(name_results{1}(1));
    try
        fhandle = fopen([directory subj '\Spike2Exports\' name_results{1}(1:end-1) 'n.txt']);
        
        % if found one, upload putative names
        if fhandle ~= -1
            thisline = fgetl(fhandle);
            foundit = false;
            while ischar(thisline) && ~foundit
                cur_c = str2num(thisline(1));
                if cur_c == c_name
                    foundit = true;
                    putatives = cellstr(thisline);
                    % update record
                    col_names = {'phenotype'};
                    second_data = {putatives};
                    update(conn,'clusters',col_names,second_data,['WHERE cluster_id = ' num2str(c_id) ';']);
                    commit(conn);
                end
                thisline = fgetl(fhandle);
            end
            fclose(fhandle);
        end
        
    catch
    end
    success = 1;
catch
    success = 0;
    c_id = nan;
end
end

