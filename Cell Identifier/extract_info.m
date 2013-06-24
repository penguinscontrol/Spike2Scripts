function [subj, coord, depth] = extract_info(in)
%extract_info
%Gets information about the coordinates of a recording from the filename
subj = in(1);
if ~ismember('RSH',in)
    subj = input('Please input subject name','s');
end

coord = struct('lm',0,'ap',0);
[si,ei] = regexp(in,'_\w*_');
depth = str2double(in(si+1:ei-1));

if ismember('L',in)&& ismember('A',in)
    [si,ei] = regexp(in,'L\w*A');
    coord.lm = -str2double(in(si+1:ei-1));
    [si,ei] = regexp(in,'A\w*_\d');
    coord.ap = str2double(in(si+1:ei-2));
elseif ismember('L',in)&& ismember('P',in) 
    [si,ei] = regexp(in,'L\w*P');
    coord.lm = -str2double(in(si+1:ei-1));
    [si,ei] = regexp(in,'P\w*_\d');
    coord.ap = -str2double(in(si+1:ei-2));
elseif ismember('M',in)&& ismember('A',in)
    [si,ei] = regexp(in,'M\w*A');
    coord.lm = str2double(in(si+1:ei-1));
    [si,ei] = regexp(in,'A\w*_\d');
    coord.ap = str2double(in(si+1:ei-2));        
elseif ismember('M',in)&& ismember('P',in)
    [si,ei] = regexp(in,'M\w*P');
    coord.lm = str2double(in(si+1:ei-1));
    [si,ei] = regexp(in,'P\w*_\d');
    coord.ap = -str2double(in(si+1:ei-2));
else
    error('Unable to get information from filename');
end
end

