function [already_exists, success] = addRecord( newrecord, conn )
%addRecord Adds a new recording session to the database, if none already
%exists.

% Check for existing record
query = ['SELECT recording_id FROM recordings WHERE a_file = ''' newrecord.name 'A'''];           
results = fetch(conn,query);
already_exists = ~isempty(results);
success = true;
if ~already_exists
    try
        col_names = {'recording_id','lm_coord','ap_coord','depth','path','a_file','e_file','sp2_file','date','grid_fid'};
        [subj, coord, depth] = name2coords(newrecord.name);
        grid = whichGrid(subj, newrecord.chamber, conn);
        this_data = {[],coord.lm,coord.ap,depth,newrecord.path, [newrecord.name 'A'], [newrecord.name 'E'], [newrecord.name '.smr'], newrecord.date,grid{1}};
        this_data
        datainsert(conn,'recordings',col_names, this_data);
    catch
        success = false;
    end
end

end

