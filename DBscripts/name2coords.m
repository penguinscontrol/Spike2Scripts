function [subj, coord, depth] = name2coords(in)
%extract_info
%Gets information about the coordinates of a recording from the filename
subj = in(1);
if ~ismember('RSH',in)
   subj = input('Please input subject name','s');
end

coord = struct('lm',0,'ap',0);
[~,ei] = regexp(in,'\w*_');
depth = str2double(in(ei+1:end));
if isnan(depth)
    depth=0;
end

%We define Lateral and Anterior as positive, Medial and Posterior as negative

if ismember('A',in)
    [si,ei] = regexp(in(strfind(in(2:end),'A')+1:end),'^\w\d+');
    coord.ap = str2double(in(strfind(in(2:end),'A')+1+si:strfind(in(2:end),'A')+ei));
elseif ismember('P',in) 
    [si,ei] = regexp(in(strfind(in(2:end),'P')+1:end),'^\w\d+');
    coord.ap = -str2double(in(strfind(in(2:end),'P')+1+si:strfind(in(2:end),'P')+ei));
end
if ismember('L',in)
    [si,ei] = regexp(in(strfind(in(2:end),'L')+1:end),'^\w\d+');
    coord.lm = str2double(in(strfind(in(2:end),'L')+1+si:strfind(in(2:end),'L')+ei));       
elseif ismember('M',in)
    [si,ei] = regexp(in(strfind(in(2:end),'M')+1:end),'^\w\d+');
    coord.lm = -str2double(in(strfind(in(2:end),'M')+1+si:strfind(in(2:end),'M')+ei));
else
    errorstr=['name2coords says: Unable to get information from filename ' in];
    display(errorstr);
    coord.lm=0;
    coord.ap=0;
end
end

