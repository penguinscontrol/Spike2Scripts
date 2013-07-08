function [subj, coordlm, coordap, depth] = extract_info_pyel(in)
%extract_info
%Gets information about the coordinates of a recording from the filename
subj = in(1);
%if ~ismember('RSH',in)
%    subj = input('Please input subject name','s');
%end

coordlm = 0;
coordap = 0;
[si,ei] = regexp(in,'_\w*.');
depth = str2double(in(si+1:ei-1));

if ismember('L',in)&& ismember('A',in)
    [si,ei] = regexp(in,'L\w*A');
    coordlm = -str2double(in(si+1:ei-1));
    [si,ei] = regexp(in,'A\w*_\d');
    coordap = str2double(in(si+1:ei-2));
elseif ismember('L',in)&& ismember('P',in) 
    [si,ei] = regexp(in,'L\w*P');
    coordlm = -str2double(in(si+1:ei-1));
    [si,ei] = regexp(in,'P\w*_\d');
    coordap = -str2double(in(si+1:ei-2));
elseif ismember('M',in)&& ismember('A',in)
    [si,ei] = regexp(in,'M\w*A');
    coordlm = str2double(in(si+1:ei-1));
    [si,ei] = regexp(in,'A\w*_\d');
    coordap = str2double(in(si+1:ei-2));        
elseif ismember('M',in)&& ismember('P',in)
    [si,ei] = regexp(in,'M\w*P');
    coordlm = str2double(in(si+1:ei-1));
    [si,ei] = regexp(in,'P\w*_\d');
    coordap = -str2double(in(si+1:ei-2));
else
    error('Unable to get information from filename');
end
end

