function [ success, stats_id ] = addStats(c_id, aligndata, alignment, conn) % removed ftp_conn
%addPsth Scan local figures folder and add any psth's that correspond to
%the cluster indicated by c_id to the database
% global directory

try
    stats_id = NaN(1,3);
    %     alignment={'sac', 'vis', 'rew'};
    for algn=1:3
        quer = ['SELECT p.psth_id FROM psth p' ...
            ' WHERE p.alignment = ''' alignment{algn} ''' AND p.cluster_id_fk = ''' num2str(c_id) ''''];
        results = fetch(conn, quer);
        if ~isempty(results)
            psth_id_fk=results{1};
        else
            psth_id_fk=[];
        end
            
        col_names = {'alignment','cluster_id_fk','psth_id_fk','coll_h','bestdir_h','bestdir',...
            'coll_p_base_vs_pre','coll_p_pre_post','coll_p_base_peri',...
            'coll_max_t','bestdir_min_p','bd_auc','bd_peakt','bd_nadirt','bd_slopes1','bd_slopes2'};
        
        if sum(~cellfun('isempty',arrayfun(@(x) x.stats, cell2mat(arrayfun(@(x) x, aligndata(algn))),'UniformOutput',false))) &&...
                nansum(cell2mat(arrayfun(@(x) x.stats.h, cell2mat(arrayfun(@(x) x, aligndata(algn))),...
                'UniformOutput',false)))
             
                hvals=cell2mat(arrayfun(@(x) nanmax(x.stats.h), cell2mat(arrayfun(@(x) x, aligndata(algn))),'UniformOutput',false));
            coll_h=hvals(end);  % Char(1)
            bestdir_h=nanmax(hvals(1:end-1)); % Char(1)
                pvals=cell2mat(arrayfun(@(x) nanmax(x.stats.p), cell2mat(arrayfun(@(x) x, aligndata(algn))),'UniformOutput',false));
            bestdir=find(pvals==nanmax(pvals(1:end-1))); % Char(3)
                collpvals=cell2mat(arrayfun(@(x) x.stats.p, aligndata{algn}(end),'UniformOutput',false));
            coll_p_base_vs_pre=collpvals(2); % Char(11)
            coll_p_pre_post=collpvals(4); % Char(11)
            coll_p_base_peri=collpvals(6); % Char(11)
                coll_t=cell2mat(arrayfun(@(x) x.stats.h, aligndata{algn}(end),'UniformOutput',false));coll_t=(coll_t(1,[2,4,6]));
            coll_max_t=coll_t(abs(coll_t)==nanmax(abs(coll_t)));% Char(11)
            bestdir_min_p=min(cell2mat(arrayfun(@(x) x.stats.p, aligndata{algn}(bestdir),'UniformOutput',false))); % Char(11)
            bd_auc=cell2mat(arrayfun(@(x) x.peakramp.auc, aligndata{algn}(bestdir),'UniformOutput',false)); % Char(10)
            bd_peakt=cell2mat(arrayfun(@(x) x.peakramp.peaksdft, aligndata{algn}(bestdir),'UniformOutput',false)); % Char(10)
            bd_nadirt=cell2mat(arrayfun(@(x) x.peakramp.nadirsdft, aligndata{algn}(bestdir),'UniformOutput',false)); % Char(10)
                slopes=cell2mat(arrayfun(@(x) x.peakramp.slopes, aligndata{algn}(bestdir),'UniformOutput',false)); % Char(10)
            bd_slopes1=slopes(1); % Char(10)
            bd_slopes2=slopes(2); % Char(10)
            
            if ~isempty(aligndata{algn}(bestdir).dir)
                    bestdir=aligndata{algn}(bestdir).dir;
            end
                
        else  
            coll_h=0;
            bestdir_h=0;
            bestdir='NaN';
            coll_p_base_vs_pre='NaN';
            coll_p_pre_post='NaN';
            coll_p_base_peri='NaN';
            coll_max_t='NaN';
            bestdir_min_p='NaN';
            bd_auc='NaN';
            bd_peakt='NaN';
            bd_nadirt='NaN';
            bd_slopes1='NaN';
            bd_slopes2='NaN';
        end
        
        this_data = {alignment{algn}, c_id, psth_id_fk, num2str(coll_h), num2str(bestdir_h), ...
            num2str(bestdir),num2str(coll_p_base_vs_pre),num2str(coll_p_pre_post),...
            num2str(coll_p_base_peri),num2str(coll_max_t),num2str(bestdir_min_p),...
            num2str(bd_auc),num2str(bd_peakt),num2str(bd_nadirt),num2str(bd_slopes1),...
            num2str(bd_slopes2)};
        datainsert(conn,'stats',col_names, this_data);
        commit(conn);
        query = 'SELECT LAST_INSERT_ID()';
        results = fetch(conn, query);
        stats_id(algn) = results{1};
    end
    success = 1;
catch
    stats_id = [];
    success = 0;
end

end