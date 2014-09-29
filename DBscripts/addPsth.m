function [ success, psth_id ] = addPsth(c_id, clusnum, conn) % removed ftp_conn
%addPsth Scan local figures folder and add any psth's that correspond to
%the cluster indicated by c_id to the database
global directory

try
    psth_id = [];
%     ssdir = getSsdir(conn);
    figdir = [directory 'figures\'];
    sacdir = [figdir 'sac\'];
    visdir = [figdir 'vis\'];
    rewdir = [figdir 'rew\'];
    folds = {figdir, sacdir, visdir, rewdir};
    quer = ['SELECT s.processed_mat, c.name, origin FROM clusters c' ...
        ' INNER JOIN sorts s ON c.sort_id_fk = s.sort_id WHERE '...
        'c.cluster_id = ' num2str(c_id)];
    results = fetch(conn, quer);
    
    clusters = results{:,2};
    origins = results{:,3};
    origins = regexprep(origins,'Spike2','_Sp2');
    origins = regexprep(origins,'Rex','_REX');
    
    %names = cellfun(@(x) regexpi(x,'\\\w*\.','match'), results(:,1), 'UniformOutput', false);
    %names = cellfun(@(x) x{:}(2:end-1), names,'UniformOutput',false);
    names = regexpi(results(:,1),'\\\w*\.','match');
    names = cellfun(@(x) x{:}(2:end-1), names,'UniformOutput',false);
    for a = 1:length(names) % For every cluster
        if iscell(origins)
            names{a} = [names{a} origins{a} '_cl_' num2str(clusters(a))];
        else
            names{a} = [names{a} origins '_cl_' num2str(clusters(a))];
        end
        listPsth = {};
        for b = 1:length(folds) % Get local filenams
            listPsth = [listPsth; findPsth(names{a}, folds{b})];
        end
        
        for c = 1:length(listPsth) % add the psth's
            [t_psth_id, success] = psth2DB(conn, c_id, clusnum, listPsth(c,:)); %ftp_conn
            psth_id = [psth_id t_psth_id];
        end
    end
    
    success = 1;
catch
    psth_id = [];
    success = 0;
end


end

