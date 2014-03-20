function grid = whichGrid( subj, chamber, conn )
% whichGrid what is the index of a certain grid in the database?

if strcmp(subj, 'S')
    query = ['SELECT id FROM grid WHERE subject = ''Sixx'' and type = ''' chamber ''''];           
    grid = fetch(conn,query);
elseif strcmp(subj, 'R')
    query = ['SELECT id FROM grid WHERE subject = ''Rigel'' and type = ''' chamber ''''];           
    grid = fetch(conn,query);    
elseif strcmp(subj, 'H')
    query = ['SELECT id FROM grid WHERE subject = ''Hilda'' and type = ''' chamber ''''];           
    grid = fetch(conn,query);
end


end

