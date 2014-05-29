function subj = whichSubj(init)
% whichGrid what is the index of a certain grid in the database?   
if strcmp(init, 'S')
    subj = 'Sixx';
elseif strcmp(init, 'R')
    subj = 'Rigel';
elseif strcmp(init, 'H')
    subj = 'Hilda';
    end

end

