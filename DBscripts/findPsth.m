function psthLocs = findPsth( file_name, folder_name)
%findPsth finds all psth files that correspond to a given filename
dirlisting = dir(folder_name);
flist = {dirlisting.name};
matches = regexpi(flist,[file_name], 'match');
matches = cellfun(@(x) ~isempty(x), matches);

psthLocs = flist(matches);
for a = 1:length(psthLocs)
    psthLocs{a,2} = folder_name;
end
end

