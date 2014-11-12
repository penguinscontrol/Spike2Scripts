function [ already, who, ids, howmany, fname] = checkSort( newrecord, conn )
%CheckSort Checks the database for a duplicate sort
query = ['SELECT sort_id, user, a_file FROM sorts s INNER JOIN recordings r ON s.recording_id_fk = r.recording_id WHERE a_file = ''' newrecord.name 'A'''];           
results = fetch(conn,query);
already = 0;
howmany = 0;
if ~isempty(results)
    already = 1;
    howmany = size(results,1);
end
if isempty(results)
    who = {' '};
    fname = {' '};
    ids = [];
else
    who = results(:,2);
    fname = results(:,3);
    ids = cast(cell2mat(results(:,1)),'int32');
end
end

