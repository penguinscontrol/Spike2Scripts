function grid = whichGrid(init, chamber, conn )
% whichGrid what is the index of a certain grid in the database?   

subj = whichSubj(init);
query = ['SELECT grid_id FROM grid WHERE subject = ''' subj ''' and location = ''' chamber ''''];           
grid = fetch(conn,query);
if isempty(grid) %unreferenced grid
    grid ={8};
end
end

