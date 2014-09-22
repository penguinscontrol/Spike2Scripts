function grid = whichGrid( subj, chamber, conn )
% whichGrid what is the index of a certain grid in the database?   
if strcmp(subj, 'S')
    query = ['SELECT grid_id FROM grid WHERE subject = ''Sixx'' and location = ''' chamber ''''];           
    grid = fetch(conn,query);
elseif strcmp(subj, 'R')
    query = ['SELECT grid_id FROM grid WHERE subject = ''Rigel'' and location = ''' chamber ''''];           
    grid = fetch(conn,query);    
elseif strcmp(subj, 'H')
    query = ['SELECT grid_id FROM grid WHERE subject = ''Hilda'' and location = ''' chamber ''''];           
    grid = fetch(conn,query);   
end

end

