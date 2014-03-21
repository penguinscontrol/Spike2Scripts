function [already_exists, success] = addRecord( newrecord, conn )
%addRecord Adds a new recording session to the database, if none already
%exists.

% Check for existing record
query = ['SELECT recording_id, location FROM recordings r INNER JOIN grid g ON r.grid_fid = g.id WHERE a_file = ''' newrecord.name 'A'''];           
results = fetch(conn,query);
already_exists = ~isempty(results);
success = true;
if ~already_exists
    try
        col_names = {'recording_id','lm_coord','ap_coord','depth','path','a_file','e_file','sp2_file','date','grid_fid'};
        [subj, coord, depth] = name2coords(newrecord.name);
        grid = whichGrid(subj, newrecord.chamber, conn);
        this_data = {[],coord.lm,coord.ap,depth,newrecord.path, [newrecord.name 'A'], [newrecord.name 'E'], [newrecord.name '.smr'], newrecord.date,grid{1}};
        datainsert(conn,'recordings',col_names, this_data);
        commit(conn);
    catch
        success = false;
    end
end

% If this record has an unspecified grid and there is one available, update
% it
if already_exists
if strcmp(results{2},'UNKNOWN') && ~strcmp(newrecord.chamber,'UNKNOWN')
    [subj, ~, ~] = name2coords(newrecord.name);
    grid = {whichGrid(subj, newrecord.chamber, conn)};
    col_names = {'grid_fid'};
    update(conn,'recordings',col_names,grid{1},['WHERE recording_id = ' num2str(results{1}) ';']);
    commit(conn);
end
end

end

